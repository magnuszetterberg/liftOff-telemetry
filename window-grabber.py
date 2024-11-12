import cv2
import subprocess
import numpy as np
import json

# Ask the user for the display number they want to capture
display_number = input("Enter display number (e.g., :0, :1): ")

def click_and_capture(display_number):
    print(f"Click on a window on display {display_number} and press Enter when you're done.")
    input()
    
    # Get the current time
    import time
    current_time = int(time.time())
    
    # Wait for 2 seconds to allow the user to interact with the window
    time.sleep(2)
    
    # Use wlprop to get the window's ID
    cmd = f"wlprop --display {display_number} --get 'active_window'"
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    import json
    data = json.loads(output)
    
    if "None" in data:
        print("No matching window found")
        return None
    
    # Get the window's ID from the output
    window_id = int(data['window'])
    
    # Capture the window
    cmd = f"wlprop --display {display_number} --get 'window {window_id}'"
    output = subprocess.check_output(cmd, shell=True)
    frame = np.frombuffer(output, dtype=np.uint8)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Print window properties
    print("Window Properties:")
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f" {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    # Display the captured window
    cv2.imshow('Region', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

data = click_and_capture(display_number)
if data is not None:
    pass  # No need to do anything here as wlprop will output the requested information directly
