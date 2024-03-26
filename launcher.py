import os
import random

import cv2
import numpy as np

from ultralytics import YOLO

from source.variables import colors


class Vehicle:
    def __init__(self, id, box):
        self.id = id
        self.box = box


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


def assign_vehicle_ids(previous_vehicles, current_bboxes, threshold=0.5):
    assigned_ids = []
    unassigned_ids = list(range(len(previous_vehicles)))

    for bbox in current_bboxes:
        max_iou = -np.inf
        max_id = None

        for vehicle_id, vehicle in enumerate(previous_vehicles):
            iou = calculate_iou(vehicle.bbox, bbox)
            if iou > max_iou and iou > threshold:
                max_iou = iou
                max_id = vehicle_id

        if max_id is not None:
            assigned_ids.append(max_id)
            unassigned_ids.remove(max_id)
        else:
            assigned_ids.append(len(previous_vehicles) + len(assigned_ids))

    return assigned_ids


def assign_id(vehicle, result):
    pass


def launcher():
    # training
    # model = YOLO("yolov8n.yaml")
    # model.train(data=r"source/config.yaml", epochs=1)

    # #  prediction
    VIDEOS_DIR = r'C:\Licenta\backup\data\raw_data\videos'

    video_path = os.path.join(VIDEOS_DIR, 'video_5_night.mp4')
    video_path_out = '{}_processed.mp4'.format(video_path)

    cap = cv2.VideoCapture(video_path)

    # model_path = os.path.join('.', 'runs', 'detect', 'train15', 'weights', 'last.pt')
    model = YOLO("yolov8n.pt")

    vehicle_id = 0
    unassigned_id = 0
    previous_vehicles = []
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if frame is None:
            break

        threshold = 0.5
        results = model(frame)[0]

        for result in results.boxes.data.tolist():

            x1, y1, x2, y2, score, class_id = result
            if current_frame > 0:
                max_iou = 0
                matching_vehicle = None
                for vehicle in previous_vehicles:
                    iou = calculate_iou([vehicle.box[0], vehicle.box[1], vehicle.box[2], vehicle.box[3]], [x1, y1, x2, y2])
                    if iou > max_iou:
                        max_iou = iou
                        matching_vehicle = vehicle
                if max_iou > 0.4:
                    vehicle_id = matching_vehicle.id
                    previous_vehicles.remove(matching_vehicle)
                    previous_vehicles.append(Vehicle(vehicle_id, [x1, y1, x2, y2]))
                else:
                    vehicle_id = random.randint(1, 1000)
                    previous_vehicles.append(Vehicle(vehicle_id, [x1, y1, x2, y2]))
            else:
                vehicle_id = random.randint(1, 1000)
                previous_vehicles.append(Vehicle(id=vehicle_id, box=[x1, y1, x2, y2]))

            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[0], 4)
                cv2.putText(frame, results.names[int(class_id)].upper() + " ID: " + str(vehicle_id), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, colors[0], 3, cv2.LINE_AA)

        current_frame += 1
        frame = cv2.resize(frame, (1200, 700))
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    launcher()
