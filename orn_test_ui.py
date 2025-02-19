import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from ultralytics import YOLO
import cv2
from tinydb import TinyDB
import torch


class OrnamentDetectorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Ornament Detector")
        self.geometry("800x600")

        # Create video label for displaying the camera feed
        self.video_label = Label(self)
        self.video_label.pack()

        # Create status label for displaying the detection status
        self.status_label = Label(self, text="Detection Status: Waiting for detections...", font=("Arial", 12))
        self.status_label.pack()

        # YOLO model
        self.model = YOLO(r"D:\ornament_weights.pt")

        # Database
        self.db = TinyDB(r"D:\Window_APP_4\Window_APP\tinydb1.json")
        self.table = self.db.table('Counter :')

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.config(text="Error: Camera not detected!")
            return

        # Start updating frames
        self.update_frame()

    def update_frame(self):
        # Capture frame from camera
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Error: Failed to capture frame.")
            return

        # YOLO prediction
        results = self.model.predict(frame, conf=0.65)

        # Check if the results object has detections
        if len(results[0].obb) == 0:
            self.status_label.config(text="Detection Status: No objects detected.")
            return

        # Plot the results
        new_frame = results[0].plot()

        # Ensure obb.cls exists before proceeding
        if results[0].obb.cls is None:
            self.status_label.config(text="Error: No valid detections.")
            return

        # Fetch expected counts from database
        try:
            # Debugging: Check if table has any documents
            all_entries = self.table.all()
            if not all_entries:
                self.status_label.config(text="Error: No entries found in database!")
                print("Database is empty.")
                return
            else:
                print("Database entries:", all_entries)

            db_count = self.table.get(doc_id=self.table._get_next_id() - 1)
            if db_count is None:
                self.status_label.config(text="Error: No data found in database!")
                return
            print("Fetched data from DB:", db_count)

            # Fetch counts
            earing_counts = int(db_count.get('earing1_cnt', 0))
            earing_counts1 = int(db_count.get('earing2_cnt', 0))
            earing_counts2 = int(db_count.get('earing3_cnt', 0))

            print(f"Earring 1 count from DB: {earing_counts}")
            print(f"Earring 2 count from DB: {earing_counts1}")
            print(f"Earring 3 count from DB: {earing_counts2}")

            # Detection counts
            class_counts = [torch.sum(results[0].obb.cls == 0).item()]
            class_counts1 = [torch.sum(results[0].obb.cls == 1).item()]
            class_counts2 = [torch.sum(results[0].obb.cls == 2).item()]

            # Calculate differences
            status = []
            diff1 = earing_counts - class_counts[0]
            diff2 = earing_counts1 - class_counts1[0]
            diff3 = earing_counts2 - class_counts2[0]

            if diff1 > 0:
                status.append(f"Earring 1: {diff1} missing")
            elif diff1 < 0:
                status.append(f"Earring 1: {abs(diff1)} extra")
            else:
                status.append("Earring 1: OK")

            if diff2 > 0:
                status.append(f"Earring 2: {diff2} missing")
            elif diff2 < 0:
                status.append(f"Earring 2: {abs(diff2)} extra")
            else:
                status.append("Earring 2: OK")

            if diff3 > 0:
                status.append(f"Earring 3: {diff3} missing")
            elif diff3 < 0:
                status.append(f"Earring 3: {abs(diff3)} extra")
            else:
                status.append("Earring 3: OK")

            # Update status label
            self.status_label.config(text=" | ".join(status))
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

        # Convert the frame to an Image for Tkinter
        rgb_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Update the image on the label
        self.video_label.config(image=tk_image)
        self.video_label.image = tk_image

        # Repeat the process
        self.after(30, self.update_frame)

    def on_closing(self):
        # Cleanup when closing the window
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()


if __name__ == "__main__":
    # Create the application window
    app = OrnamentDetectorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
