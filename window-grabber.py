
import cv2
import numpy as np
import subprocess
import threading

def read_frames(process, frame_size, frame_queue):
    while True:
        raw_frame = process.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            break
        frame = np.frombuffer(raw_frame, np.uint8).reshape((frame_height, frame_width, 3))
        frame_queue.append(frame)

def display_frames(frame_queue):
    while True:
        if frame_queue:
            frame = frame_queue.pop(0)
            cv2.imshow('Image from FIFO', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Define the ffmpeg command with an input framerate
input_framerate = '30'  # Example: 30 frames per second
ffmpeg_cmd = [
    'ffmpeg',
   # '-r', input_framerate,  # Specify the input framerate
    '-flags', 'low_delay',
    '-i', '/tmp/wf-record.pipe',
    '-f', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-vcodec', 'rawvideo',
    '-flags', 'low_delay',
    '-analyzeduration', '0',
    '-probesize', '32',
    'pipe:1'
]

# Start the ffmpeg process
process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)

# Define the frame size and initialize a queue for frames
frame_width = 1920
frame_height = 1200
frame_size = frame_width * frame_height * 3
frame_queue = []

# Start threads for reading and displaying frames
read_thread = threading.Thread(target=read_frames, args=(process, frame_size, frame_queue))
display_thread = threading.Thread(target=display_frames, args=(frame_queue,))

read_thread.start()
display_thread.start()

read_thread.join()
display_thread.join()

# Clean up
cv2.destroyAllWindows()
process.terminate()
