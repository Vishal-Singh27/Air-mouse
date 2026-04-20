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

    def process_hands(self, hands_data, sensitivity_bound):
        status = "NOT MOVING"
        color = (255, 255, 255)

        for hand_info in hands_data:
            fingers = hand_info["fingers"]
            hand = hand_info["landmarks"]

            if hand_info["is_right"]:
                # --- MOUSE MOVEMENT ---
                if fingers["index"]:
                    status = "MOVING"
                    raw_x = np.interp(hand[8].x, [sensitivity_bound, 1 - sensitivity_bound], [0, self.screen_w])
                    raw_y = np.interp(hand[8].y, [sensitivity_bound, 1 - sensitivity_bound], [0, self.screen_h])
                    
                    self.x_history.append(raw_x)
                    self.y_history.append(raw_y)
                    
                    smooth_x = sum(self.x_history) / len(self.x_history)
                    smooth_y = sum(self.y_history) / len(self.y_history)
                    pyautogui.moveTo(smooth_x, smooth_y, _pause=False)

                # --- CLICKS ---
                # Left Click
                if fingers["index"] and fingers["thumb"] and not fingers["middle"]:
                    self.l_click_count += 1
                    if self.l_click_count >= self.click_threshold and not self.l_pressed:
                        self.mouse.press(Button.left)
                        self.l_pressed = True
                else:
                    self.l_click_count = 0
                    if self.l_pressed:
                        self.mouse.release(Button.left)
                        self.l_pressed = False

                # Right Click
                if fingers["index"] and not fingers["thumb"]:
                    self.r_click_count += 1
                    if self.r_click_count >= self.click_threshold and not self.r_pressed:
                        self.mouse.press(Button.right)
                        self.r_pressed = True
                else:
                    self.r_click_count = 0
                    if self.r_pressed:
                        self.mouse.release(Button.right)
                        self.r_pressed = False

            else:
                # --- MACRO GESTURES (LEFT HAND) ---
                current_time = time.time()
                if current_time > self.gesture_cooldown:
                    if fingers["index"] and fingers["middle"] and fingers["thumb"] and not fingers["ring"] and not fingers["pinky"]:
                        pyautogui.hotkey('win', 'shift', 's')
                        self.gesture_cooldown = current_time + 2.0 
                        status = "SCREENSHOT!"
                        color = (0, 255, 255)
                        
                    elif fingers["pinky"] and fingers["thumb"] and not fingers["index"] and not fingers["middle"] and not fingers["ring"]:
                        pyautogui.hotkey('win', 'ctrl', 'o')
                        self.gesture_cooldown = current_time + 2.0
                        status = "KEYBOARD!"
                        color = (255, 0, 255)

        # Override status if dragging
        if self.l_pressed: status, color = "LEFT DRAG", (0, 255, 0)
        if self.r_pressed: status, color = "RIGHT DRAG", (0, 0, 255)

        return status, color
