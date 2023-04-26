# best one so far. aimbot + fov + tracking
# 1.9 mouse speed, 140 FOV
# MSS VERSION
import time
import ctypes
import mss
import torch
import win32api
import win32con
import numpy as np
from termcolor import colored


# define the MouseInput, Input_I, Input, and POINT ctypes classes
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

print(colored('''                                                                     
        .--.                __.....__      
        |__|            .-''         '.    
.-,.--. .--.           /     .-''"'-.  `.  
|  .-. ||  |          /     /________\   \ 
| |  | ||  |.--------.|                  | 
| |  | ||  ||____    |\    .-------------' 
| |  '- |  |    /   /  \    '-.____...---. 
| |     |__|  .'   /    `.             .'  
| |          /    /___    `''-...... -'    
|_|         |         |                    
            |_________|                                                                                             
          MSS VERSION ''', "blue"))
time.sleep(3)

fullscreen = (1280, 720) # <-- Set to your desktop resolution
#fullscreen = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
#width = int(input(colored(''' Enter your game screen width: ''',"light_blue")))
#height = int(input(colored(''' Enter your game screen width: ''',"light_blue")))
#fullscreen = (width, height)
right, bottom = 200, 200
left = (fullscreen[0] - right) // 2
top = (fullscreen[1] - bottom) // 2
right = left + right
bottom = top + bottom
rejoin = (left, top, right, bottom)

mouse_speed = int(input('mouse: '))
rio_center = 100

fov = 150
fov_width = fov
fov_height = fov
fov_left = rio_center - fov_width // 2
fov_right = rio_center + fov_width // 2
fov_top = rio_center - fov_height // 2
fov_bottom = rio_center + fov_height // 2
model = torch.hub.load('D:\RIZE\yolov5', 'custom', path=r'D:\RIZE\aim.pt', source='local')
model.conf = 0.5
model.apm = True

#nigger = float(input('Mouse speed: '))

print(colored(''' Successfully Loaded MSS VERSION! ''',"light_green"))
with mss.mss() as sct:
    while True:
        screenshot = np.array(sct.grab(rejoin))
        df = model(screenshot, size=416).pandas().xyxy[0]
        rio_center = 100

        min_distance = float('inf')
        closest_object = None
        for i in range(len(df)):
            xmin = int(df.iloc[i, 0])
            ymin = int(df.iloc[i, 1])
            xmax = int(df.iloc[i, 2])
            ymax = int(df.iloc[i, 3])
            object_center = ((xmin + xmax) // 2 , (ymin + ymax) // 2)
            distance = ((object_center[0] - rio_center) ** 2 + (object_center[1] - rio_center) ** 2) ** 0.6

            if distance < min_distance:
                min_distance = distance
                closest_object = object_center

        if win32api.GetKeyState(0x02) in (-127, -128) or win32api.GetKeyState(
                0xA0) > 0 or win32api.GetKeyState(0x01) in (-127, -128):
            if closest_object is not None and closest_object[0] >= fov_left and closest_object[0] <= fov_right and \
                    closest_object[1] >= fov_top and closest_object[1] <= fov_bottom:
                dx = int((closest_object[0] - rio_center) / mouse_speed)
                dy = int((closest_object[1] - rio_center) / mouse_speed)
                mouse_input = MouseInput(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, None)
                input_data = Input(win32con.INPUT_MOUSE, Input_I(mi=mouse_input))
                ctypes.windll.user32.SendInput(1, ctypes.byref(input_data), ctypes.sizeof(input_data))

            #cv2.imshow('Screen', screenshot)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
    cv2.release()
    cv2.destroyAllWindows()
