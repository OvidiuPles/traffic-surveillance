class StreamRecorder:
    def __init__(self):
        self.recording = False
        self.out = None
        self.recorded_frames = 0

    def reset(self):
        self.recording = False
        if self.out is not None:
            self.out.release()
        self.recorded_frames = 0
