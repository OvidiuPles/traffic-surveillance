import os

import cv2


class DataFactory:
    @staticmethod
    def modify_class_labels(dir_path, old_class, new_class):
        for filename in os.listdir(dir_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(dir_path, filename)
                with open(filepath, 'r') as file:
                    lines = file.readlines()

                modified_lines = []
                for line in lines:
                    if line.startswith(str(old_class)):
                        modified_line = str(new_class) + line[1:]
                        modified_lines.append(modified_line)
                    else:
                        modified_lines.append(line)

                with open(filepath, 'w') as file:
                    file.writelines(modified_lines)
        print("class " + str(old_class) + " modified to " + str(new_class))

    @staticmethod
    def video_to_frames(video_path, output_path, n=4):
        video_name = video_path.split("\\")[-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        cap = cv2.VideoCapture(video_path)

        frame_idx = 0
        saved_frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % n == 0:
                frame_file_path = os.path.join(output_path, f"{video_name}_frame_{saved_frame_idx}.jpg")
                cv2.imwrite(frame_file_path, frame)
                print(f"saved {frame_file_path}")
                saved_frame_idx += 1

            frame_idx += 1

        cap.release()
        print("frames saved in " + output_path)


DataFactory.video_to_frames(video_path=r'C:\Licenta\data\raw_data\videos\video_6_processed.mp4',
                            output_path=r'C:\Licenta\data\raw_data\videos\wtf',
                            n=1)


# DataFactory.modify_class_labels(r"C:\Licenta\data\raw_data\yolo_labels\5", 5, 4)
