# python version 3.12.4
# pip install opencv-python
# pip install Pillow

import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_capture = cv2.VideoCapture(0)
        self.face_img = None
        self.detected = False
        self.canvas = tk.Canvas(window, width=self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="ถ่ายและบันทึกรูปภาพ", command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.delay = 15  
        self.update()

        self.window.mainloop()

    def snapshot(self):
        if self.detected and self.face_img is not None:
            cv2.imwrite('face.jpg', self.face_img)
            print("บันทึกรูปภาพสำเร็จ")
        else:
            print("ไม่มีการตรวจจับใบหน้า ไม่สามารถบันทึกรูปภาพได้")

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            self.detected = False  

            for (x, y, w, h) in faces:
                self.detected = True
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                self.face_img = gray[y:y+h, x:x+w]

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk  

        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

App(tk.Tk(), "การตรวจจับใบหน้าพร้อมปุ่มบันทึก")
