from typing import TYPE_CHECKING
import cv2
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QApplication,
    QFrame,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_capture_frame import (
        SequenceRecorderCaptureFrame,
    )


class SequenceRecorderVideoDisplayFrame(QFrame):
    def __init__(self, capture_frame: "SequenceRecorderCaptureFrame") -> None:
        super().__init__()
        self.capture_frame = capture_frame
        self.sequence_recorder_widget = capture_frame.sequence_recorder_widget

        self.capture = None
        self.recording = False
        self.recording_frames = []
        self.video_frame_rate = 30  # Adjust frame rate as needed
        self.video_writer = None
        self.init_ui()

    def init_ui(self) -> None:
        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_display.setFont(QFont("Arial", 12))
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_display)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # self.init_webcam()

    def init_webcam(self) -> None:
        available_cameras = self.find_available_cameras()
        if available_cameras:
            self.capture = cv2.VideoCapture(available_cameras[0], cv2.CAP_MSMF)
            if not self.capture.isOpened():
                QMessageBox.warning(
                    self, "Webcam Error", "Unable to access the webcam."
                )
                return
            self.video_timer = QTimer(self)
            self.video_timer.timeout.connect(self.update_video_feed)
            self.update_timer_interval()

    def find_available_cameras(self) -> list[int]:
        available_cameras = []
        for i in range(1):  # Check first 5 indices.
            cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def update_timer_interval(self) -> None:
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)

    def update_video_feed(self) -> None:
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.recording:
                self.recording_frames.append(frame)
            self.display_frame(frame)

    def display_frame(self, frame) -> None:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
        )
        p = QPixmap.fromImage(convert_to_Qt_format)
        self.video_display.setPixmap(p)

    def toggle_recording(self) -> None:
        self.recording = not self.recording
        if self.recording:
            self.recording_frames = []
            QApplication.processEvents()  # Process existing events to update UI
        else:
            self.save_video()

    def save_video(self) -> None:
        if self.recording_frames:
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(
                "output.avi", fourcc, self.video_frame_rate, (640, 480)
            )
            for frame in self.recording_frames:
                out.write(frame)
            out.release()
            QMessageBox.information(
                self, "Recording Saved", "The video was saved successfully."
            )
        self.recording_frames = []  # Clear the frames after saving

    def closeEvent(self, event) -> None:
        if self.capture is not None:
            self.capture.release()

    def resize_video_display_frame(self) -> None:
        if not hasattr(self, "beat_frame"):
            self.beat_frame = self.capture_frame.sequence_beat_frame

        height = self.beat_frame.height()
        self.setFixedHeight(height)
        self.video_display.setFixedHeight(height)
