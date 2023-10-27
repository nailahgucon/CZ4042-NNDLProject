import torch
from torchvision.models.efficientnet import efficientnet_v2_s
import keyboard
from PIL import Image, ImageGrab
import numpy as np
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from tqdm import tqdm

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = efficientnet_v2_s()
model.classifier = torch.nn.Linear(in_features = 1280, out_features = 2)
# Load the model with the appropriate map_location parameter
model.load_state_dict(torch.load("models/efficientnet_s.pth"))
model.to(device)
model.eval()

transformer = Compose([
    Resize([480,480]),
    CenterCrop(480),
    Normalize(mean =[0.485, 0.456, 0.406], std =[0.229, 0.224, 0.225])
])

def generator():
    while(not keyboard.is_pressed("esc")):
      yield

for _ in tqdm(generator()):
    image = ImageGrab.grab(bbox = (520, 210, 1380, 420))
    image = ToTensor()(image)
    image = image.to(device)
    image = transformer(image)
    outputs = model(image[None , ...])
    _,preds = torch.max(outputs.data, 1)
    if preds.item() == 1:
        keyboard.press_and_release("space")