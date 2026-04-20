# 🖱️ AI Virtual Mouse - Advanced Gesture Control

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-lightgrey)

An advanced, dual-hand gesture-controlled virtual mouse built with computer vision and machine learning. This project replaces traditional physical mouse interactions with real-time hand tracking, featuring a modern graphical control panel for sensitivity and system adjustments. 

Developed as an academic project at **Christ University, School of Sciences**.

---

## ✨ Features

* **Dual-Hand Tracking:** Distinct operational modes for left and right hands.
* **Right-Hand Navigation:** Smooth cursor movement, left-clicking, and right-clicking using intuitive finger pinches.
* **Left-Hand Macro System:** Trigger system-level macros (like taking screenshots or opening the on-screen keyboard) using specific hand poses.
* **Modern GUI:** A sleek, dark-mode control panel built with `CustomTkinter` to adjust cursor sensitivity and toggle the vision engine on the fly.
* **Modular Architecture:** Clean separation of concerns (Vision, Logic, UI) to facilitate collaborative Git workflows and easy debugging.

---

## 📂 Project Structure

To support team development and distinct Git commits, the codebase is divided into three core modules:

* `main.py` **(Main Interface):** The entry point. Handles the `CustomTkinter` GUI, video feed rendering, and system integration.
* `vision_engine.py` **(Vision Engine):** Manages the OpenCV video capture and MediaPipe Hand Landmarker model inference.
* `action_controller.py` **(System Controller):** Translates raw landmark coordinates into smoothed PyAutoGUI movements and debounced click events.

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.8+ installed. 

### 2. Install Dependencies
Run the following command to install the required Python packages:


```bash
pip install opencv-python mediapipe pyautogui pynput customtkinter Pillow numpy
````

### 3\. Download the MediaPipe Model

This project uses the optimized MediaPipe task model. You must download the `hand_landmarker.task` file and place it in the root directory of the project.

  * [Download hand\_landmarker.task from Google Storage](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task)

-----

## ✋ Gesture Guide

### Right Hand (Mouse Control)

| Gesture | Action |
| :--- | :--- |
| **Index Finger UP** (Others down) | Move Cursor |
| **Index + Thumb UP** (Pinch) | Left Click / Drag |
| **Index + Middle UP** (Thumb down) | Right Click |

### Left Hand (System Macros)

| Gesture | Action |
| :--- | :--- |
| **Peace Sign ✌️** (Index + Middle UP) | Take Screenshot (`Win + Shift + S`) |
| **Pinky UP 🤙** (Others down) | Open On-Screen Keyboard (`Win + Ctrl + O`) |

-----

## 💻 Usage

Start the application by running the main module:

```bash
python main.py
```

1.  Click **"Start Tracking"** in the control panel to initialize the webcam and AI models.
2.  Adjust the **Cursor Sensitivity** slider to match your physical distance from the camera (lower value = larger bounding box).
3.  Raise your hands into the frame and start controlling your system\!

-----

## 👥 Team & Credits

* **Vishal Singh**, **Yasmin Devargattu**  - Handled vision control, and integration of tkinter app with all modules
* **Angela Anna Antonny**, **Tanvi Sheoran** - Handled mouse control, and handled the documentations
