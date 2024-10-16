import sys
import cv2
from PyQt6.QtWidgets import QApplication
from video_recorder.video_recoder import VideoRecorder


if __name__ == "__main__":
    # RTSP address for testing
    RTSP_SAMPLE = "rtsp://210.99.70.120:1935/live/cctv001.stream"

    app = QApplication(sys.argv)
    ex = VideoRecorder(
        frame_size=(640, 480),
        initial_rtsp="0",
        apply_grayscale=False,
        fourcc="XVID",
        fps=30,
        encode_param=[cv2.IMWRITE_JPEG_QUALITY, 90],
    )
    # ex = VideoRecorder(frame_size=(1280, 720))
    ex.show()
    sys.exit(app.exec())
