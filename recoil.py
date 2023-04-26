import ctypes
import win32con
import win32api
import time
# Define the MouseInput structure
import ctypes
import win32con
import win32api
import time

# Define the MouseInput structure
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    def __init__(self, dx, dy, mouseData=0, dwFlags=win32con.MOUSEEVENTF_MOVE, time=0, dwExtraInfo=None):
        self.dx = ctypes.c_long(int(dx))
        self.dy = ctypes.c_long(int(dy))
        self.mouseData = ctypes.c_ulong(mouseData)
        self.dwFlags = ctypes.c_ulong(dwFlags)
        self.time = ctypes.c_ulong(time)
        if dwExtraInfo is not None:
            self.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(dwExtraInfo))
        else:
            self.dwExtraInfo = None

# Define the Input_I union
class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

# Define the Input structure
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Define the POINT structure
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

# Loop until the program is terminated
while True:
    # Check if the left mouse button is held down
    if win32api.GetKeyState(0x01) < 0:
        # Get the current position of the mouse
        pos = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))

        # Set the movement of the mouse
        dx = 0
        dy = 2

        # Move the mouse down
        mouse_input = MouseInput(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, None)
        input_data = Input(win32con.INPUT_MOUSE, Input_I(mi=mouse_input))
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_data), ctypes.sizeof(input_data))


    time.sleep(0.001)
