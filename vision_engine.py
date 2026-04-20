import cv2
import mediapipe as mp
import time

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task'):
        BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7
        )
        self.landmarker = self.HandLandmarker.create_from_options(options)
        self.cap = None

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()

    def stop_camera(self):
        if self.cap:
            self.cap.release()

    def get_finger_states(self, hand_landmarks):
        """Returns a dict of which fingers are up."""
        return {
            "thumb": hand_landmarks[4].y < hand_landmarks[3].y,
            "index": hand_landmarks[8].y < hand_landmarks[6].y,
            "middle": hand_landmarks[12].y < hand_landmarks[10].y,
            "ring": hand_landmarks[16].y < hand_landmarks[14].y,
            "pinky": hand_landmarks[20].y < hand_landmarks[18].y
        }

    def process_frame(self):
        """Reads a frame, processes it, and returns data."""
        if not self.cap or not self.cap.isOpened():
            return False, None, None

        success, frame = self.cap.read()
        if not success:
            return False, None, None

        frame = cv2.flip(frame, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        res = self.landmarker.detect_for_video(mp_image, int(time.time() * 1000))

        hands_data = []
        if res.hand_landmarks:
            for hand in res.hand_landmarks:
                fingers = self.get_finger_states(hand)
                is_right_hand = hand[0].x > 0.5
                hands_data.append({"landmarks": hand, "fingers": fingers, "is_right": is_right_hand})

        return True, frame, hands_data