import cv2
import pandas as pd
from PySide6.QtGui import QImage, QPixmap
from easyocr import easyocr
from openpyxl.reader.excel import load_workbook
from pandas import ExcelWriter
from ultralytics import YOLO

from source.processing.counter import Counter
from source.processing.stream_recorder import StreamRecorder
from source.processing.vehicle import Vehicle
from source.utils.colors import class_colors
from source.utils.variables import *


class Analyzer:
    def __init__(self, confidence=0.5, tracking_depth=12, on_tracked_found=None, stream_output=None):
        # processing parameters
        self.model_confidence = confidence
        self.tracking_depth = tracking_depth  # number of previous frames to keep for vehicle tracking
        self.plates_confidence = 0.4
        self.reading_attempts = 2

        # models
        self.text_reader = easyocr.Reader(['en'], gpu=True)
        self.vehicles_model = YOLO(VEHICLES_MODEL_PATH)
        self.number_plates_model = YOLO(PLATES_MODEL_PATH)
        # self.model = YOLO("yolov8n.pt") # to be deleted from source/processing after distinction with custom model is done

        self.stream_output = stream_output
        self.counter = Counter()
        self.previous_vehicles = []
        self.unassigned_id = 0
        self.image_height = 0
        self.image_width = 0
        self.counting_line_height = 0
        self.stop_stream = False
        self.statistics_generated = False
        self.stream_recorder = StreamRecorder()

        self.recorded_plate_numbers = []
        self.recorded_tracked_and_found = []

        self.tracked_plate_numbers = []
        self.on_tracked_found = on_tracked_found

        #  processing options
        self.show_boxes = True
        self.show_classes = True
        self.show_number_plates = True
        self.show_total_counting = True
        self.show_class_counting = True
        self.show_lane_counting = True
        self.show_lanes = True
        self.show_ids = True
        self.show_counting_line = True

    def process_video(self, input_path, output_path=None, generate_statistics=True):
        self.reset_data()
        if output_path is None:
            path = input_path.split(".mp4")[0:-1]
            output_path = "\\".join(path) + "_processed.mp4"  # same dir as input

        cap = cv2.VideoCapture(input_path)
        ret, frame = cap.read()
        self.image_height, self.image_width, _ = frame.shape
        self.counting_line_height = int(self.image_height / 2) - PIXELS_UPPER_CNT_LINE
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (self.image_width, self.image_height))

        while ret:
            self.count_vehicles()
            frame = self.process_frame(frame)
            self.update_previous_vehicles(record_number_plates=True)

            out.write(frame)
            ret, frame = cap.read()

        if generate_statistics:
            self.generate_statistics(output_path)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def process_stream(self, input_path):
        self.reset_data()
        self.stop_stream = False
        cap = cv2.VideoCapture(input_path)
        got_image_size = False
        while True:
            ret, frame = cap.read()
            if frame is None:
                break
            if not got_image_size:
                self.image_height, self.image_width, _ = frame.shape
                self.counting_line_height = int(self.image_height / 2) - PIXELS_UPPER_CNT_LINE
                got_image_size = True

            self.count_vehicles()
            frame = self.process_frame(frame)
            self.update_previous_vehicles(record_number_plates=False)

            if self.stream_recorder.recording:
                self.stream_recorder.out.write(frame)
                self.stream_recorder.recorded_frames += 1
                if self.stream_recorder.recorded_frames >= FRAMES_TO_RECORD:
                    self.stream_recorder.reset()

            if self.stream_output is None:
                frame = cv2.resize(frame, (STREAM_WIDTH, STREAM_HEIGHT))
                cv2.imshow('Stream', frame)
            else:
                frame = self.convert_cv2_to_qpixmap(frame)
                self.stream_output.setPixmap(frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or self.stop_stream is True:
                break

        self.stream_recorder.reset()
        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        original_frame = frame.copy()
        results = self.vehicles_model(frame)[0]

        if self.show_counting_line:
            cv2.line(frame, (0, self.counting_line_height), (int(self.image_width), self.counting_line_height), (0, 255, 0), 7)

        if self.show_total_counting:
            cv2.putText(frame, "counted vehicles: " + str(self.counter.vehicles),
                        (int(self.image_width - 1800), self.counting_line_height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.2, class_colors[4], 3, cv2.LINE_AA)

        if self.show_class_counting:
            cv2.putText(frame, f"cars: {self.counter.cars}, trucks:{self.counter.trucks}, busses:{self.counter.busses}, vans:{self.counter.vans}",
                        (int(self.image_width - 2000), self.counting_line_height + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, class_colors[4], 2, cv2.LINE_AA)

        if self.stream_recorder.recording and (
                self.stream_recorder.recorded_frames % 6 == 0 or (self.stream_recorder.recorded_frames + 1) % 6 == 0 or (
                self.stream_recorder.recorded_frames + 2) % 6 == 0):
            center = (self.image_width - 100, 100)
            cv2.circle(frame, center, 50, (0, 0, 255), -1)

        frame = self.draw_lane_lines(frame)

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score >= self.model_confidence and self.valid_width(x1, x2, y2):
                vehicle_id, tracked_and_found = self.assign_vehicle_id(vehicle_box=[x1, y1, x2, y2], class_id=class_id)
                box_color = class_colors[class_id] if not tracked_and_found else class_colors[2]
                plates_color = class_colors[2] if not tracked_and_found else class_colors[3]

                if self.show_number_plates:
                    number_plate = self.assign_number_plate(vehicle_id, original_frame)
                    if number_plate is not None:
                        cv2.putText(frame, str(number_plate),
                                    (int(x1 + 15), int(y1 + 50)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.7, plates_color, 3, cv2.LINE_AA)

                if self.show_boxes:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), box_color, 4)
                class_name = results.names[int(class_id)].upper() if self.show_classes else ""
                displayed_id = " ID: " + str(vehicle_id) if self.show_ids else ""
                cv2.putText(frame, class_name + displayed_id,
                            (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, box_color, 3, cv2.LINE_AA)
        return frame

    def assign_vehicle_id(self, vehicle_box, class_id):
        x1, y1, x2, y2 = vehicle_box
        max_iou = 0
        matching_vehicle = None
        for vehicle in self.previous_vehicles:
            if (abs(vehicle.x1 - x1) < MAX_DIST_TRACKING_X
                    and abs(vehicle.y1 - y1) < MAX_DIST_TRACKING_Y):  # calculate iou only if the potential matching vehicle is nearby
                iou = self.calculate_iou([vehicle.x1, vehicle.y1, vehicle.x2, vehicle.y2], [x1, y1, x2, y2])
                if iou > max_iou:
                    max_iou = iou
                    matching_vehicle = vehicle
        if max_iou > 0.3:
            tracked_and_found = matching_vehicle.tracked_and_found
            vehicle_id = matching_vehicle.id
            self.previous_vehicles.remove(matching_vehicle)
            self.previous_vehicles.append(
                Vehicle(x1, y1, x2, y2, vehicle_id, is_counted=matching_vehicle.is_counted, number_plate=matching_vehicle.number_plate,
                        reading_attempts=matching_vehicle.reading_attempts, class_id=class_id, tracked_and_found=matching_vehicle.tracked_and_found))
        else:
            tracked_and_found = False
            vehicle_id = self.unassigned_id
            self.unassigned_id += 1
            if self.unassigned_id >= MAX_ID:
                self.unassigned_id = 0
            self.previous_vehicles.append(Vehicle(x1, y1, x2, y2, vehicle_id, class_id=class_id))
        return vehicle_id, tracked_and_found

    def assign_number_plate(self, vehicle_id, frame):
        for vehicle in self.previous_vehicles:
            if vehicle.id == vehicle_id:
                if vehicle.number_plate is not None:
                    return vehicle.number_plate

                if not self.is_in_reading_zone(vehicle.x2, vehicle.y2) or vehicle.reading_attempts >= self.reading_attempts:
                    return None

                vehicle.reading_attempts += 1
                cropped_vehicle = frame[int(vehicle.y1):int(vehicle.y2), int(vehicle.x1):int(vehicle.x2)]
                results = self.number_plates_model(cropped_vehicle)[0]

                if len(results.boxes.data.tolist()) == 0:
                    return None

                x1, y1, x2, y2, score, class_id = results.boxes.data.tolist()[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cropped_plate = cropped_vehicle[y1:y2, x1:x2]

                plate = self.preprocess_plate(cropped_plate)
                result = self.text_reader.readtext(plate)

                if self.valid_number_plate(result):
                    string_result = result[0][1].upper()
                    string_result = self.sanitize_number_plate(string_result)
                    vehicle.number_plate = string_result
                    return string_result
                else:
                    return None

    def valid_number_plate(self, plate):
        if len(plate) > 0:
            if plate[0][2] > self.plates_confidence and len(plate[0][1]) > 6:
                return True
        return False

    @staticmethod
    def preprocess_plate(image):
        new_width = 4 * image.shape[1]
        new_height = 4 * image.shape[0]
        image = cv2.resize(image, (new_width, new_height))
        image = image[0: int(image.shape[0]), int(image.shape[1] / 10): int(image.shape[1])]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def count_vehicles(self):
        for vehicle in self.previous_vehicles:
            if not vehicle.is_counted:
                if self.vehicle_in_counting_zone(vehicle.y1, vehicle.y2):
                    self.counter.count(vehicle)
                    vehicle.is_counted = True

    def vehicle_in_counting_zone(self, y1, y2):
        return y1 < self.counting_line_height < y2

    @staticmethod
    def calculate_iou(box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou

    def update_previous_vehicles(self, record_number_plates):
        updated_vehicles = []
        for vehicle in self.previous_vehicles:
            vehicle.frame_depth += 1
            if record_number_plates and vehicle.number_plate is not None and vehicle.number_plate not in self.recorded_plate_numbers:
                self.recorded_plate_numbers.append(vehicle.number_plate)
            if vehicle.number_plate in self.tracked_plate_numbers and not vehicle.tracked_and_found:
                if not record_number_plates:  # notification and recording only for streaming
                    self.on_tracked_found(vehicle.number_plate)
                    self.start_recording(name=vehicle.number_plate)
                else:
                    if vehicle.number_plate not in self.recorded_tracked_and_found:
                        self.recorded_tracked_and_found.append(vehicle.number_plate)
                vehicle.tracked_and_found = True
            if vehicle.frame_depth <= self.tracking_depth:
                updated_vehicles.append(vehicle)
        self.previous_vehicles = updated_vehicles

    def is_in_reading_zone(self, x2, y2):
        return self.counting_line_height < y2 < self.image_height - 10 and x2 > THIRD_LINE

    @staticmethod
    def sanitize_number_plate(number_plate):
        if number_plate[0].isdigit() or len(number_plate.replace(" ", "")) != 7:
            return number_plate  # unknown format, can't sanitize

        sanitized_number_plate = ""
        initial_number_plate = number_plate
        try:
            number_plate = number_plate.replace(" ", "")
            if number_plate[0] == "B" and number_plate[1] not in ["C", "H", "N", "T", "V", "R", "Z"]:  # specific format for romanian capital city
                for i, char in enumerate(number_plate):
                    if i in [0, 4, 5, 6] and char.isdigit():
                        char = dict_figure_to_letter[char]
                    elif i in [1, 2, 3] and char.isalpha():
                        char = dict_letter_to_figure[char]
                    sanitized_number_plate += char
                sanitized_number_plate = sanitized_number_plate[:1] + " " + sanitized_number_plate[1:4] + " " + sanitized_number_plate[4:]
            else:
                for i, char in enumerate(number_plate):
                    if i in [0, 1, 4, 5, 6] and char.isdigit():
                        char = dict_figure_to_letter[char]
                    elif i in [2, 3] and char.isalpha():
                        char = dict_letter_to_figure[char]
                    sanitized_number_plate += char
                sanitized_number_plate = sanitized_number_plate[:2] + " " + sanitized_number_plate[2:4] + " " + sanitized_number_plate[4:]
        except KeyError:
            return initial_number_plate
            # other unknown formats, ignore them

        return sanitized_number_plate

    def draw_lane_lines(self, frame):
        if self.show_lanes:
            cv2.line(frame, LINE1_PT1, LINE1_PT2, (0, 255, 0), 7)  # first (right to left)
            cv2.line(frame, LINE2_PT1, LINE2_PT2, (0, 255, 0), 7)
            cv2.line(frame, LINE3_PT1, LINE3_PT2, (0, 255, 0), 7)
            cv2.line(frame, LINE4_PT1, LINE4_PT2, (0, 255, 0), 7)
            cv2.line(frame, LINE5_PT1, LINE5_PT2, (0, 255, 0), 7)
            cv2.line(frame, LINE6_PT1, LINE6_PT2, (0, 255, 0), 7)

        if self.show_lane_counting:
            cv2.putText(frame, str(self.counter.fifth_lane),
                        (5, int(2100 / 3)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, class_colors[4], 3, cv2.LINE_AA)
            cv2.putText(frame, str(self.counter.fourth_lane),
                        (5, int(2100 / 1.3)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, class_colors[4], 3, cv2.LINE_AA)
            cv2.putText(frame, str(self.counter.third_lane),
                        (600, 2100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, class_colors[4], 3, cv2.LINE_AA)
            cv2.putText(frame, str(self.counter.second_lane),
                        (1750, 2100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, class_colors[4], 3, cv2.LINE_AA)
            cv2.putText(frame, str(self.counter.first_lane),
                        (2800, 2100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, class_colors[4], 3, cv2.LINE_AA)

        return frame

    def valid_width(self, x1, x2, y2):
        width = x2 - x1
        if (y2 > self.counting_line_height and width < 340) or (y2 < self.counting_line_height and width < 200):
            return False
        return True

    @staticmethod
    def convert_cv2_to_qpixmap(cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_pixmap = QPixmap.fromImage(q_image)

        return q_pixmap

    def generate_statistics(self, output_path):
        try:
            output_path = output_path.split("\\")
            video_name = output_path[-1].split("_")
            video_name = "_".join(video_name[0: -1])
            output_path = "\\".join(output_path[0: -1])
            output_path = output_path + f"\\{video_name}_statistics.xlsx"

            whites = [' ' for _ in range(len(self.recorded_plate_numbers) - 1)]  # all arrays need to be the same length for some reason
            whites2 = [' ' for _ in range(len(self.recorded_plate_numbers) - len(self.recorded_tracked_and_found))]
            data = {'Recorded plate numbers': self.recorded_plate_numbers,
                    'Tracked plate numbers': self.recorded_tracked_and_found + whites2,
                    'Vehicles': [self.counter.vehicles] + whites,
                    'Cars': [self.counter.cars] + whites,
                    'Trucks': [self.counter.trucks] + whites,
                    'Busses': [self.counter.busses] + whites,
                    'Vans': [self.counter.vans] + whites,
                    'First lane': [self.counter.first_lane] + whites,
                    'Second lane': [self.counter.second_lane] + whites,
                    'Third lane': [self.counter.third_lane] + whites,
                    'Fourth lane': [self.counter.fourth_lane] + whites,
                    'Fifth lane': [self.counter.fifth_lane] + whites}
            df = pd.DataFrame(data)

            writer = ExcelWriter(path=output_path)
            df.to_excel(writer, sheet_name="Traffic statistics", index=False)
            writer.close()

            wb = load_workbook(output_path)
            ws = wb.active
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 25
            ws.column_dimensions['H'].width = 12
            ws.column_dimensions['I'].width = 12
            ws.column_dimensions['J'].width = 12
            ws.column_dimensions['K'].width = 12
            ws.column_dimensions['L'].width = 12

            wb.save(output_path)
            self.statistics_generated = True
        except PermissionError:
            self.statistics_generated = False

    def reset_data(self):
        self.counter.reset()
        self.previous_vehicles = []
        self.unassigned_id = 0
        self.recorded_plate_numbers = []
        self.statistics_generated = False

    def clear_tracking_list(self):
        self.tracked_plate_numbers = []
        self.recorded_tracked_and_found = []

        updated_vehicles = []
        for vehicle in self.previous_vehicles:
            vehicle.tracked_and_found = False
            updated_vehicles.append(vehicle)
        self.previous_vehicles = updated_vehicles

        if self.stream_recorder.recording:
            self.stream_recorder.reset()

    def start_recording(self, name):
        name = name.replace(" ", "_") + ".mp4"
        no_videos_same_name = 0

        if not os.path.exists(os.getcwd() + "\\recordings"):
            os.makedirs(os.getcwd() + "\\recordings")

        for video in os.listdir(os.getcwd() + "\\recordings"):
            if name in video:
                no_videos_same_name += 1
        if no_videos_same_name != 0:
            name = str(no_videos_same_name) + "_" + name

        output_path = os.getcwd() + "\\recordings" + f"\\{name}"

        self.stream_recorder.out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 11, (self.image_width, self.image_height))
        self.stream_recorder.recording = True
