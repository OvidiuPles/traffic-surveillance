import os

import cv2
from easyocr import easyocr
from ultralytics import YOLO

from source.processing.vehicle import Vehicle
from source.utils.colors import class_colors
from source.utils.variables import PIXELS_UPPER_CNT_LINE, STREAM_WIDTH, STREAM_HEIGHT, MAX_DIST_TRACKING_X, MAX_DIST_TRACKING_Y, MAX_ID, THIRD_LINE, \
    dict_figure_to_letter, dict_letter_to_figure


class Analyzer:
    def __init__(self, confidence=0.5, tracking_depth=12):
        self.model_confidence = confidence
        self.tracking_depth = tracking_depth  # number of previous frames to keep for vehicle tracking

        # models
        self.text_reader = easyocr.Reader(['en'], gpu=False)
        vehicles_model_path = os.path.join('.', '.', '.', 'runs', 'detect', 'train11', 'weights', 'last.pt')
        self.vehicles_model = YOLO(vehicles_model_path)
        plates_model_path = os.path.join('.', '.', '.', 'runs', 'detect', 'train18', 'weights', 'last.pt')
        self.number_plates_model = YOLO(plates_model_path)
        # self.model = YOLO("yolov8n.pt")

        self.previous_vehicles = []
        self.unassigned_id = 0
        self.image_height = 0
        self.image_width = 0
        self.counting_line_height = 0
        self.counted_vehicles = 0

    def process_video(self, input_path, output_path=None):
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
            self.update_previous_vehicles()

            out.write(frame)
            ret, frame = cap.read()

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def process_stream(self, input_path):
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
            self.update_previous_vehicles()

            frame = cv2.resize(frame, (STREAM_WIDTH, STREAM_HEIGHT))
            cv2.imshow('Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        original_frame = frame.copy()
        results = self.vehicles_model(frame)[0]

        # counting line
        cv2.line(frame, (0, self.counting_line_height), (int(self.image_width), self.counting_line_height), (0, 255, 0), 7)
        cv2.putText(frame, "counted vehicles: " + str(self.counted_vehicles),
                    (int(self.image_width - 1750), self.counting_line_height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.2, class_colors[4], 3, cv2.LINE_AA)

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > self.model_confidence:
                vehicle_id = self.assign_vehicle_id(vehicle_box=[x1, y1, x2, y2])
                number_plate = self.assign_number_plate(vehicle_id, original_frame)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), class_colors[class_id], 4)
                cv2.putText(frame, results.names[int(class_id)].upper() + " ID: " + str(vehicle_id),
                            (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, class_colors[class_id], 3, cv2.LINE_AA)
                if number_plate is not None:
                    cv2.putText(frame, str(number_plate),
                                (int(x1 + 15), int(y1 + 50)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.7, class_colors[2], 3, cv2.LINE_AA)
        return frame

    def assign_vehicle_id(self, vehicle_box):
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
            vehicle_id = matching_vehicle.id
            self.previous_vehicles.remove(matching_vehicle)
            self.previous_vehicles.append(
                Vehicle(x1, y1, x2, y2, vehicle_id, is_counted=matching_vehicle.is_counted, number_plate=matching_vehicle.number_plate))
        else:
            vehicle_id = self.unassigned_id
            self.unassigned_id += 1
            if self.unassigned_id >= MAX_ID:
                self.unassigned_id = 0
            self.previous_vehicles.append(Vehicle(x1, y1, x2, y2, vehicle_id))
        return vehicle_id

    def assign_number_plate(self, vehicle_id, frame):
        for vehicle in self.previous_vehicles:
            if vehicle.id == vehicle_id:
                if vehicle.number_plate is not None:
                    return vehicle.number_plate

                if not self.is_in_reading_zone(vehicle.x1, vehicle.y1, vehicle.x2, vehicle.y2):
                    return None

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

    @staticmethod
    def valid_number_plate(plate):
        if len(plate) > 0:
            if plate[0][2] > 0.4 and len(plate[0][1]) > 6:
                return True
        return False

    @staticmethod
    def preprocess_plate(image):
        new_width = 4 * image.shape[1]
        new_height = 4 * image.shape[0]
        image = cv2.resize(image, (new_width, new_height))
        image = image[0: int(image.shape[0]), int(image.shape[1] / 12): int(image.shape[1])]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def count_vehicles(self):
        for vehicle in self.previous_vehicles:
            if not vehicle.is_counted:
                if self.vehicle_in_counting_zone(vehicle.y1, vehicle.y2):
                    self.counted_vehicles += 1
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

    def update_previous_vehicles(self):
        updated_vehicles = []
        for vehicle in self.previous_vehicles:
            vehicle.frame_depth += 1
            if vehicle.frame_depth <= self.tracking_depth:
                updated_vehicles.append(vehicle)
        self.previous_vehicles = updated_vehicles

    def is_in_reading_zone(self, x1, y1, x2, y2):
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
