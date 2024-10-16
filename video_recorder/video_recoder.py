import os
import cv2
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap


class VideoRecorder(QWidget):
    CODEC_EXTENSIONS = {
        "XVID": ".avi",
        "MJPG": ".avi",
        "X264": ".mp4",
        "AVC1": ".mp4",
        "H264": ".mp4",
        "PIM1": ".avi",
        "MJ2C": ".mj2",
        "MP4V": ".mp4",
        "DIB ": ".avi",
        "THEO": ".ogv",
        "FLV1": ".flv",
        "VP80": ".webm",
        "FFV1": ".avi",
    }

    def __init__(
        self,
        frame_size=(640, 480),
        initial_rtsp="0",
        apply_grayscale=False,
        fourcc="XVID",
        fps=30,
        encode_param=[cv2.IMWRITE_JPEG_QUALITY, 95],
    ):
        super().__init__()
        self.cap = cv2.VideoCapture(initial_rtsp)
        self.out = None
        self.frame_width = frame_size[0]
        self.frame_height = frame_size[1]
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self._is_recording = False
        self._apply_grayscale = apply_grayscale
        self._fourcc = cv2.VideoWriter.fourcc(*fourcc)
        self._fps = fps

        os.makedirs("data", exist_ok=True)
        self._save_to_images = False
        self._frame_count = 0
        self._encode_param = encode_param

        self.initUI(rtsp_address=initial_rtsp)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 / self._fps + 0.5))  # Update every 30 ms

    def initUI(self, rtsp_address="0"):
        self.setWindowTitle("Video Recorder")
        geometry_size = self.frame_height + 20, self.frame_width + 50
        self.setGeometry(0, 0, geometry_size[1], geometry_size[0])

        self.image_label = QLabel(self)
        self.quit_button = QPushButton("Quit", self)
        self.gray_button = QPushButton("Enable Grayscale", self)

        self.rtsp_input = QLineEdit(
            self,
            placeholderText='Input RTSP address, if "0" or blank is webcam',
            text=rtsp_address if rtsp_address not in ["0", "", 0, None] else "",
        )
        self.rtsp_button = QPushButton("Update RTSP", self)

        self.record_codec = QLineEdit(
            self,
            placeholderText="Input fourcc e.g. XVID",
        )

        self.save_images_button = QPushButton("Save to Images", self)

        self.record_button = QPushButton("Record", self)

        self.record_button.clicked.connect(self.toggle_record)
        self.quit_button.clicked.connect(self.close)
        self.rtsp_button.clicked.connect(self.update_rtsp)
        self.gray_button.clicked.connect(self.toggle_grayscale)
        self.save_images_button.clicked.connect(self.toggle_save_images)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()

        vbox.addWidget(self.image_label)
        hbox.addWidget(self.quit_button)
        hbox.addWidget(self.rtsp_input)
        hbox.addWidget(self.rtsp_button)

        hbox2.addWidget(self.record_codec)
        hbox2.addWidget(self.save_images_button)
        hbox2.addWidget(self.record_button)
        hbox2.addWidget(self.gray_button)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

        self.setFocus()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self._apply_grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            display_frame = frame.copy()
            if self._apply_grayscale:
                display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2RGB)
            else:
                display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

            if self._is_recording:
                self.out.write(frame)
                cv2.circle(display_frame, (30, 30), 10, (255, 0, 0), -1)

            if self._save_to_images:
                file_name = os.path.join("data", f"{self._frame_count:05d}.jpg")
                cv2.imwrite(file_name, frame, self._encode_param)
                cv2.circle(display_frame, (60, 30), 10, (0, 255, 0), -1)
                self._frame_count += 1

            h, w, ch = display_frame.shape
            bytes_per_line = ch * w
            qimage_format = QImage.Format.Format_RGB888

            convert_to_Qt_format = QImage(
                display_frame.data, w, h, bytes_per_line, qimage_format
            )
            p = convert_to_Qt_format.scaled(
                self.frame_width, self.frame_height, Qt.AspectRatioMode.KeepAspectRatio
            )
            self.image_label.setPixmap(QPixmap.fromImage(p))

    def create_video_writer(self, file_name, is_color):
        ext = VideoRecorder.CODEC_EXTENSIONS.get(self._fourcc, ".avi")
        return cv2.VideoWriter(
            f"{file_name}{ext}",
            self._fourcc,
            self._fps,
            (self.frame_width, self.frame_height),
            isColor=is_color,
        )

    def toggle_record(self):
        self._is_recording = not self._is_recording
        if self._is_recording:
            self.record_button.setText("Stop Recording")
            self.update_codec()
            if self._apply_grayscale:
                self.out = self.create_video_writer("data/output", is_color=False)
            else:
                self.out = self.create_video_writer("data/output", is_color=True)
        else:
            self.record_button.setText("Record")
            if self.out:
                self.out.release()

    def update_rtsp(self):
        rtsp_address = self.rtsp_input.text()
        if rtsp_address == "0" or rtsp_address == "":
            rtsp_address = 0
        self.cap.release()
        self.cap = cv2.VideoCapture(rtsp_address)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)

        self.setFocus()

    def update_codec(self):
        fourcc = self.record_codec.text().upper()
        print(fourcc)
        if fourcc in VideoRecorder.CODEC_EXTENSIONS:
            self._fourcc = cv2.VideoWriter.fourcc(*fourcc)
        else:
            self._fourcc = cv2.VideoWriter.fourcc(*"XVID")

        if self._is_recording and self.out:
            self.out.release()
            self.out = self.create_video_writer("output", not self._apply_grayscale)

        self.setFocus()

    def toggle_grayscale(self):
        self._apply_grayscale = not self._apply_grayscale
        if self._apply_grayscale:
            self.gray_button.setText("Disable Grayscale")
        else:
            self.gray_button.setText("Enable Grayscale")
        self.setFocus()

    def toggle_save_images(self):
        self._save_to_images = not self._save_to_images
        if self._save_to_images:
            self.save_images_button.setText("Stop Saving")
        else:
            self.save_images_button.setText("Save to Images")
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.toggle_record()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.KeyboardModifier.ControlModifier:
            pass
        elif event.key() == Qt.Key.Key_Return:
            self.update_rtsp()
        elif event.key() == Qt.Key.Key_G:
            self.toggle_grayscale()
        elif event.key() == Qt.Key.Key_S:
            self.toggle_save_images()

    def closeEvent(self, event):
        self.cap.release()
        if self.out:
            self.out.release()
        event.accept()
