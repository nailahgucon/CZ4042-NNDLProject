import time

import torch
from torchvision.models.efficientnet import efficientnet_v2_s
from PIL import Image, ImageGrab
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from tqdm import tqdm
import keyboard
import pydirectinput

# check for cuda
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Instantiate EfficientNet V2 s model
model = efficientnet_v2_s()
model.classifier = torch.nn.Linear(in_features = 1280, out_features = 3)
# load pre-trained weights
model.load_state_dict(torch.load("models/efficientnet_s_20E_8BS.pth"))
model.to(device)
# set it to evaluation mode
model.eval()

# define image transformation pipeline (similar to training)
transformer = Compose([Resize([480,480]), CenterCrop(480), Normalize(mean =[0.485, 0.456, 0.406], std =[0.229, 0.224, 0.225])])

# function to make code run until the "esc" key is pressed
def runGameBot():
    while(not keyboard.is_pressed("esc")):
      yield

for _ in tqdm(runGameBot()):
    # capture screenshot of whole screen
    rt_image = ImageGrab.grab()
    # convert captured image to PyTorch tensor
    rt_image = ToTensor()(rt_image)
    # move image tensor to cuda
    rt_image = rt_image.to(device)
    # apply image transformation pipeline
    rt_image = transformer(rt_image)
    # make predictions using the pre-trained model for the transformed image
    rt_outputs = model(rt_image[None, ...])
    # extract the predicted class with the highest probability
    _, kb_predictions = torch.max(rt_outputs.data, 1)

    # check if the predicted class is 1 (JUMP)
    # and simulate space keyboard event
    if kb_predictions.item() == 1:
        print("Wizard Lah JUMP")
        pydirectinput.keyDown('space')
        time.sleep(1)
        pydirectinput.keyUp('space')
    # check if the predicted class is 2 (DUCK)
    # and simulate down keyboard event
    elif kb_predictions.item() == 2:
        print("Wizard Lah DUCK")
        pydirectinput.keyDown('down')
        time.sleep(1)
        pydirectinput.keyUp('down')
