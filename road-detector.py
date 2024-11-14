
import cv2
import numpy as np

def detect_vertical_lines(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    # Initial heading
    heading = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 100, 300)

        # Use Hough Line Transform to detect lines
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

        deviations = []  # List to store deviations from vertical

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Calculate the angle of the line
                angle = np.arctan2(y2 - y1, x2 - x1) * (180.0 / np.pi)
                # Calculate deviation from vertical (0 degrees)
                deviation = angle if angle >= 0 else angle + 180
                deviation_from_vertical = deviation - 90
                deviations.append(deviation_from_vertical)
                # Draw the line on the original frame
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the average deviation from vertical
        if deviations:
            average_deviation = np.mean(deviations)
            # Adjust heading based on average deviation
            heading += average_deviation

        # Display the calculated heading
        cv2.putText(frame, f"Heading: {heading:.2f} degrees", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display frames
        cv2.imshow("Frame", frame)
        cv2.imshow("Canny", canny)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_vertical_lines("videoplayback.mp4")
