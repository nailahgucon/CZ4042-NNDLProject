import cv2
from PIL import ImageGrab
import numpy as np
import keyboard
import os
from datetime import datetime

# declare necessary variables
temp = []
pressed_key = ""
i = 0

# check if folder named 'captures' exists.
# If not, create it.
if not os.path.exists("captures"):
    os.mkdir("captures")

# Define a function for keyboard events
# keyboardCallBack function is called every time a key is pressed or released.
# Updates the temp list with the pressed keys
def keyboardCallBack(key: keyboard.KeyboardEvent):
    global pressed_key

    # if key is pressed
    if key.event_type == "down" and key.name not in temp:
        temp.append(key.name)

    if key.event_type == "up":
        temp.remove(key.name)

    temp.sort()
    pressed_key = " ".join(temp)

# set up the keyboard hook to monitor key events
keyboard.hook(callback=keyboardCallBack)

# while the "esc" key is not pressed
while (not keyboard.is_pressed("esc")):
    # Screenshot the screen
    image = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)

    # if key pressed, incorporate into filename
    if len(temp) != 0:
        cv2.imwrite("captures/" + str(datetime.now()).replace("-", "_").replace(":", "_").replace(" ", "_")+" " + pressed_key + ".png", image)

    # if no key pressed, incorporate "n" into filename
    else:
        cv2.imwrite("captures/" + str(datetime.now()).replace("-", "_").replace(":", "_").replace(" ", "_") + " n" + ".png", image)
    i = i + 1