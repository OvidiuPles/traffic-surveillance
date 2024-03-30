from ultralytics import YOLO

model = YOLO("yolov8n.yaml")
model.train(data=r"config.yaml", epochs=100)
# remove motorcyle/bicycle?
