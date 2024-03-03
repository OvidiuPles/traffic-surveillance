import cv2
import os


class Training:
    @staticmethod
    def video_to_frames(video_path, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error opening video file {video_path}")
            return

        frame_idx = 0
        saved_frame_idx = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_idx % 4 == 0:
                frame_file_path = os.path.join(output_path, f"frame_{saved_frame_idx}.jpg")
                cv2.imwrite(frame_file_path, frame)
                print(f"Saved {frame_file_path}")
                saved_frame_idx += 1

            frame_idx += 1

        cap.release()
        print("Done saving frames.")

