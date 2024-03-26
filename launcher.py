import os

import cv2
import numpy as np

from ultralytics import YOLO

from source.variables import colors


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


def launcher():
    # training
    # model = YOLO("yolov8n.yaml")
    # model.train(data=r"source/config.yaml", epochs=1)

    # #  prediction
    VIDEOS_DIR = r'C:\Licenta\traffic-surveillance-backend\data\raw_data\videos'

    video_path = os.path.join(VIDEOS_DIR, 'video_5_night.mp4')
    video_path_out = '{}_processed.mp4'.format(video_path)

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('.', 'runs', 'detect', 'train15', 'weights', 'last.pt')
    model = YOLO(model_path)

    threshold = 0.5

    x = 0
    y = 0
    while ret:
        x += 1
        results = model(frame)[0]
        boxes = results.boxes.data.tolist()

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            y += 1
            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[class_id], 4)
                cv2.putText(frame, results.names[int(class_id)].upper() + " ID:" + str(x) + str(y), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, colors[class_id], 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    launcher()
