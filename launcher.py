from source.processing.analyzer import Analyzer


def launcher():
    analyzer = Analyzer()
    # analyzer.process_video(input_path=r"C:\Licenta\backup\data\raw_data\videos\video_5_night.mp4")
    analyzer.process_stream(input_path=r"C:\Licenta\backup\data\raw_data\videos\video_5_night.mp4")


if __name__ == '__main__':
    launcher()
