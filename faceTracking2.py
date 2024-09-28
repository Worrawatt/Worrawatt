# python version 3.12.4
# pip install opencv-python
# pip install Pillow

import cv2
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoRecorder:
    def __init__(self, filename, fourcc, fps, frame_size):
        self.open = True
        self.filename = filename
        self.fourcc = fourcc
        self.fps = fps
        self.frame_size = frame_size
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)

    def write(self, frame):
        if self.open:
            self.video_writer.write(frame)

    def stop(self):
        self.open = False
        self.video_writer.release()

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_capture = cv2.VideoCapture(0)
        self.width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="เริ่มบันทึก", width=15, command=self.start_recording)
        self.btn_start.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_stop = tk.Button(window, text="หยุดบันทึก", width=15, command=self.stop_recording, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10, pady=5)

        self.recording = False
        self.out = None

        self.delay = 15
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # เปลี่ยนเป็น 'mp4v'
            self.out = VideoRecorder('video_output.mp4', fourcc, 20.0, (self.width, self.height))  # เปลี่ยนนามสกุลเป็น .mp4
            messagebox.showinfo("การบันทึก", "เริ่มการบันทึกวิดีโอ")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.out.stop()
            messagebox.showinfo("การบันทึก", "หยุดการบันทึกวิดีโอ และบันทึกไฟล์ 'video_output.mp4'")

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk  

            if self.recording:
                self.out.write(frame)

        self.window.after(self.delay, self.update)

    def on_closing(self):
        if self.recording:
            self.stop_recording()
        self.video_capture.release()
        self.window.destroy()

App(tk.Tk(), "videoDectection")
