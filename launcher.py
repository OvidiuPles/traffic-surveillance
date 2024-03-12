import cv2

from ultralytics import YOLO


def launcher():
    # training
    model = YOLO("yolov8n.yaml")
    model.train(data=r"source/config.yaml", epochs=1)

    # prediction
    # VIDEOS_DIR = r'C:\Licenta\raw_data\videos'
    #
    # video_path = os.path.join(VIDEOS_DIR, 'video_5_night.mp4')
    # video_path_out = '{}_processed.mp4'.format(video_path)
    #
    # cap = cv2.VideoCapture(video_path)
    # ret, frame = cap.read()
    # H, W, _ = frame.shape
    # out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))
    #
    # model_path = os.path.join('.', 'runs', 'detect', 'train6', 'weights', 'last.pt')
    #
    # # Load a model
    # model = YOLO(model_path)
    #
    # threshold = 0.2
    #
    # while ret:
    #
    #     results = model(frame)[0]
    #     for result in results.boxes.data.tolist():
    #         x1, y1, x2, y2, score, class_id = result
    #
    #         if score > threshold:
    #             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[class_id], 4)
    #             cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1.3, colors[class_id], 3, cv2.LINE_AA)
    #
    #     out.write(frame)
    #     ret, frame = cap.read()
    #
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    launcher()
