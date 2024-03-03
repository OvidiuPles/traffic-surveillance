import os

import cv2

from training.training import Training
from ultralytics import YOLO


def launcher():
    # training
    # model = YOLO("yolov8n.yaml")
    # model.train(data="config.yaml", epochs=70)

    # prediction
    VIDEOS_DIR = r'C:\Licenta\inregistrari'

    video_path = os.path.join(VIDEOS_DIR, 'vlc-record-2024-02-13-14h14m13s-rtsp___192.168.82.149_live-.mp4')
    video_path_out = '{}_out.mp4'.format(video_path)

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('.', 'runs', 'detect', 'train5', 'weights', 'last.pt')

    # Load a model
    model = YOLO(model_path)

    threshold = 0.1

    while ret:

        results = model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    launcher()
