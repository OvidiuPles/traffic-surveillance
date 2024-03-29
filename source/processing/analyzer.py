import time

import cv2
import numpy as np
from ultralytics import YOLO

from source.processing.vehicle import Vehicle
from source.variables.colors import class_colors


class Analyzer:
    def __init__(self, confidence=0.5):
        # model_path = os.path.join('.', '.', 'runs', 'detect', 'train15', 'weights', 'last.pt')
        self.model = YOLO("yolov8n.pt")
        self.model_confidence = confidence
        self.previous_vehicles = []
        self.unassigned_id = 0

    def process_video(self, input_path, output_path=None, tracking_depth=5):
        if output_path is None:
            path = input_path.split(".mp4")[0:-1]
            output_path = "\\".join(path) + "_processed.mp4"  # same dir as input

        cap = cv2.VideoCapture(input_path)
        ret, frame = cap.read()
        h, w, _ = frame.shape
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (w, h))

        while ret:
            frame = self.process_frame(frame)
            out.write(frame)
            ret, frame = cap.read()

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def process_stream(self, input_path, tracking_depth=5):
        cap = cv2.VideoCapture(input_path)

        while True:
            ret, frame = cap.read()
            if frame is None:
                break

            frame = self.process_frame(frame)
            frame = cv2.resize(frame, (1200, 700))
            cv2.imshow('Stream', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        results = self.model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > self.model_confidence:
                vehicle_id = self.assign_vehicle_id(vehicle_box=[x1, y1, x2, y2])
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), class_colors[0], 4)
                cv2.putText(frame, results.names[int(class_id)].upper() + " ID: " + str(vehicle_id) + ";x1=" + str(int(x1)) + ";y1=" + str(int(y1)),
                            (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, class_colors[0], 3, cv2.LINE_AA)
        return frame

    def assign_vehicle_id(self, vehicle_box):
        x1, y1, x2, y2 = vehicle_box
        max_iou = 0
        matching_vehicle = None
        for vehicle in self.previous_vehicles:
            if abs(vehicle.box[0] - x1) < 200 and abs(vehicle.box[1] - y1) < 400:  # calculate iou only if the potential matching vehicle is nearby
                iou = self.calculate_iou([vehicle.box[0], vehicle.box[1], vehicle.box[2], vehicle.box[3]], [x1, y1, x2, y2])
                if iou > max_iou:
                    max_iou = iou
                    matching_vehicle = vehicle
        if max_iou > 0.3:
            vehicle_id = matching_vehicle.id
            self.previous_vehicles.remove(matching_vehicle)
            self.previous_vehicles.append(Vehicle(vehicle_id, [x1, y1, x2, y2]))
        else:
            vehicle_id = self.unassigned_id
            self.unassigned_id += 1
            if self.unassigned_id >= 100:
                self.unassigned_id = 0
            self.previous_vehicles.append(Vehicle(vehicle_id, [x1, y1, x2, y2]))
        return vehicle_id

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

    def assign_vehicle_ids(self, previous_vehicles, current_bboxes, threshold=0.5):
        assigned_ids = []
        unassigned_ids = list(range(len(previous_vehicles)))

        for bbox in current_bboxes:
            max_iou = -np.inf
            max_id = None

            for vehicle_id, vehicle in enumerate(previous_vehicles):
                iou = self.calculate_iou(vehicle.bbox, bbox)
                if iou > max_iou and iou > threshold:
                    max_iou = iou
                    max_id = vehicle_id

            if max_id is not None:
                assigned_ids.append(max_id)
                unassigned_ids.remove(max_id)
            else:
                assigned_ids.append(len(previous_vehicles) + len(assigned_ids))

        return assigned_ids
