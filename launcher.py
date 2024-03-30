from source.processing.analyzer import Analyzer


def launcher():
    analyzer = Analyzer(confidence=0.6)
    # analyzer.process_video(input_path=r"C:\Licenta\data\raw_data\videos\video_5_night.mp4")
    analyzer.process_stream(input_path=r"C:\Licenta\data\raw_data\videos\video_4.mp4")


if __name__ == '__main__':
    launcher()
