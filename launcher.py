from ultralytics import YOLO

from source.processing.analyzer import Analyzer


def launcher():
    # training
    # model = YOLO("yolov8n.yaml")
    # model.train(data=r"source/training/config.yaml", epochs=1)

    # prediction
    analyzer = Analyzer()
    # analyzer.process_video(input_path=r"C:\Licenta\backup\data\raw_data\videos\video_5_night.mp4")
    analyzer.process_stream(input_path=r"C:\Licenta\backup\data\raw_data\videos\video_5_night.mp4")


if __name__ == '__main__':
    launcher()
