import io
import cv2
import torch
import torchvision
from pathlib import Path
from ultralytics import YOLO
from torchvision.io import read_image
from torchvision.utils import draw_bounding_boxes

model_path_gpu = 'weights/best_2.pt'
model_path_cpu = 'weights/best_2.pt'

def Predict(image:Path):
    image = cv2.imread(image) #numpy.ndarray
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == 'cuda':
        model = YOLO(model_path_gpu)
    model = YOLO(model_path_cpu)
    results = model.predict(source=image, device=device, save_txt=False)
    return results

def Count_vis(res, image:Path):
    bbox = res[0].boxes.xyxy # bounding boxes -->torch.tensor
    num_colonies = bbox.shape[0]
    im_tensor = read_image(image)
    pred_im = draw_bounding_boxes(image=im_tensor, boxes= bbox, colors=(255, 0, 0))
    pred_im = torchvision.transforms.ToPILImage()(pred_im)

    return pred_im, num_colonies

if __name__ == '__main__':
    image = 'MicroBio_img_009.jpg'
    pred_image, colonies = Count_vis(Predict(image), image)
    pred_image.show()
    pred_image.save(fp='pred_image.jpg')
    print(colonies)
