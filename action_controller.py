import pyautogui
from pynput.mouse import Button, Controller
import numpy as np
from collections import deque
import time

class SystemController:
    def __init__(self):
        self.mouse = Controller()
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.PAUSE = 0
        
        # Stability vars
        self.x_history = deque(maxlen=10)
        self.y_history = deque(maxlen=10)
        self.click_threshold = 3 
        
        self.l_click_count = 0
        self.r_click_count = 0
        self.l_pressed = False
        self.r_pressed = False
        self.gesture_cooldown = 0.0

