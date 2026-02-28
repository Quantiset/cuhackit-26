import cv2
import numpy as np

cap = cv2.VideoCapture("minecraft.mp4")

prev_gray = None
jump_frames = []

frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is not None:
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        vertical_motion = np.mean(flow[..., 1])

        if vertical_motion < -1.5:
            jump_frames.append(frame_idx)

    prev_gray = gray
    frame_idx += 1

cap.release()