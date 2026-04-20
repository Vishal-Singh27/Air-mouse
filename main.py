import customtkinter as ctk
import cv2
from PIL import Image
from vision_engine import HandTracker
from action_controller import SystemController

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AirMouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Virtual Mouse")
        self.geometry("900x600")

        # Initialize Modules
        self.tracker = HandTracker()
        self.controller = SystemController()

        # UI Layout setup (keeping it brief for the structure)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.video_label = ctk.CTkLabel(self, text="Camera Offline", font=("Arial", 16))
        self.video_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.toggle_btn = ctk.CTkButton(self.control_frame, text="Start Tracking", command=self.toggle_system)
        self.toggle_btn.pack(pady=20)

        self.sens_slider = ctk.CTkSlider(self.control_frame, from_=0.1, to=0.4)
        self.sens_slider.set(0.2)
        self.sens_slider.pack(pady=20)

        self.is_tracking = False

    def toggle_system(self):
        if not self.is_tracking:
            if self.tracker.start_camera():
                self.is_tracking = True
                self.toggle_btn.configure(text="Stop Tracking", fg_color="red")
                self.update_loop()
        else:
            self.is_tracking = False
            self.tracker.stop_camera()
            self.toggle_btn.configure(text="Start Tracking", fg_color=["#3B8ED0", "#1F6AA5"])
            self.video_label.configure(image="", text="Camera Offline")

    def update_loop(self):
        if self.is_tracking:
            success, frame, hands_data = self.tracker.process_frame()
            
            if success:
                # Pass data to the controller
                status, color = self.controller.process_hands(hands_data, self.sens_slider.get())

                # Draw UI overlay on the frame
                cv2.rectangle(frame, (10, 10), (320, 60), (0,0,0), -1)
                cv2.putText(frame, f"MODE: {status}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                # Convert to CustomTkinter image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
                
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk, text="")

            self.after(16, self.update_loop)

if __name__ == "__main__":
    app = AirMouseApp()
    app.mainloop()