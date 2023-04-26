# best one so far. aimbot + fov + tracking
# 1.8 mouse speed, 150 FOV
# DXCAM VERSION
import dxcam
import time
import ctypes
import mss
import torch
import cv2
import win32api
import win32con
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
          DX CAM VERSION ''', "blue"))
time.sleep(3)

fullscreen = (1280, 720) # <-- Set to your desktop resolution
#fullscreen = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
#width = int(input(colored(''' Enter your game screen width: ''', "light_blue")))
#height = int(input(colored(''' Enter your game screen width: ''', "light_blue")))
#fullscreen = (width, height)
right, bottom = 210, 210
left = (fullscreen[0] - right) // 2
top = (fullscreen[1] - bottom) // 2
right = left + right
bottom = top + bottom
rejoin = (left, top, right, bottom)

rio_center = 105

fov = 140
fov_width = fov
fov_height = fov
fov_left = rio_center - fov_width // 2
fov_right = rio_center + fov_width // 2
fov_top = rio_center - fov_height // 2
fov_bottom = rio_center + fov_height // 2

nigger = 1.5
model = torch.hub.load(r'D:\TEN\yolov5', 'custom', path=r'D:\TEN\half.engine', source="local").cuda()
model.conf = 0.51
model.apm = True 


camera = dxcam.create(output_color="BGRA")  # normal color

print(colored(''' Successfully Loaded DXCAM VERSION ''', "light_green"))
while True:
    screenshot = camera.grab(rejoin)
    if screenshot is None:
        continue
    df = model(screenshot, size=416).pandas().xyxy[0]
    rio_center = 105

    min_distance = float('inf')
    closest_object = None
    for i in range(len(df)):
        xmin = int(df.iloc[i, 0])
        ymin = int(df.iloc[i, 1])
        xmax = int(df.iloc[i, 2])
        ymax = int(df.iloc[i, 3])
        object_center = ((xmin + xmax) // 2, (ymin + ymax) // 2)  # THE ENEMY CENTER BOX
        # cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)
        distance = ((object_center[0] - rio_center) ** 2 + (object_center[1] - rio_center) ** 2) ** 0.6

        if distance < min_distance:
            min_distance = distance
            closest_object = object_center

    if win32api.GetKeyState(0x02) in (-127, -128) or win32api.GetKeyState(0x01) in (-127, -128):
        mouse_speed = nigger
        if closest_object is not None and closest_object[0] >= fov_left and closest_object[0] <= fov_right and \
                closest_object[1] >= fov_top and closest_object[1] <= fov_bottom:
            dx = int((closest_object[0] - rio_center) / mouse_speed)
            dy = int((closest_object[1] - rio_center) / mouse_speed)
            mouse_input = MouseInput(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, None)
            input_data = Input(win32con.INPUT_MOUSE, Input_I(mi=mouse_input))
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_data), ctypes.sizeof(input_data))
        # cv2.imshow('Screen', screenshot)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
cv2.release()
cv2.destroyAllWindows()
