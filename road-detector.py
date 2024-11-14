import cv2
import numpy as np

def detect_vertical_lines(video_path):
    # Initialize the video capture object
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get the frame rate and dimensions of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize lists to store the detected vertical lines and their scores
    lines = []
    line_scores = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 100, 150)  # Adjust these values as needed

        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Adjust this value as needed
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w)/h
                if 4 < aspect_ratio < 6:  # Adjust these values as needed
                    lines.append((x, y))

        line_scores = [len(lines)]

        # Draw the detected vertical lines
        for i, (x, y) in enumerate(lines):
            cv2.rectangle(frame, (x-5, y-10), (x+5, y+20), (0, 255, 0), 2)
            cv2.putText(frame, f"Line {i+1}", (x-15, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Update the display
        cv2.imshow("Frame", frame)
        cv2.imshow("Canny", canny)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_vertical_lines("videoplayback.mp4")
