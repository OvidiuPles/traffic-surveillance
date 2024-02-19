import time

import torch
from PIL import Image, ImageDraw
from torchvision import models
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms import Compose, ToTensor


def launcher():
    model = models.detection.fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
    model.eval()

    image = Image.open(r"C:\Licenta\inregistrari\frame.png")

    transform = Compose([
        ToTensor()
    ])

    transformed_img = transform(image)

    print("detection begins")
    start_time = time.time()
    with torch.no_grad():
        prediction = model([transformed_img])
    end_time = time.time()
    print("detection ends: " + str(end_time - start_time))

    vehicle_labels = [2, 3, 5, 7]
    for element in range(len(prediction[0]['labels'])):
        if prediction[0]['labels'][element].item() in vehicle_labels:
            box = prediction[0]['boxes'][element].numpy()
            score = prediction[0]['scores'][element].item()
            if score > 0.5:
                draw = ImageDraw.Draw(image)
                draw.rectangle((box[0], box[1], box[2], box[3]), outline="red", width=3)

    image.show()


if __name__ == '__main__':
    launcher()
