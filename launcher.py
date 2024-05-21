from source.processing.analyzer import Analyzer


def launcher():
    for i in range(1, 10):
        analyzer = Analyzer(confidence=0.5, tracking_depth=12)
        analyzer.process_video(input_path=fr"C:\Licenta\data\raw_data\videos\video_{i}.mp4")


# analyzer.process_stream(input_path=r"C:\Licenta\data\raw_data\videos\video_5_night.mp4")


if __name__ == '__main__':
    launcher()
