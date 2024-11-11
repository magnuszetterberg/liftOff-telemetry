
import socket
import struct
import cv2
import numpy as np

def parse_telemetry_data(data):
    
    format_string = '<' + 'f' + 'f' * 3 + 'f' * 4 + 'f' * 3 + 'f' * 4 + 'f' * 2 + 'B' + 'f' * 4
    try:
        unpacked_data = struct.unpack(format_string, data)

        
    
    except struct.error as e:
        print(f"Unpacking error: {e}")
        return None

    telemetry = {
        'timestamp': unpacked_data[0],
        'position': (unpacked_data[1], unpacked_data[2], unpacked_data[3]),
        'attitude': (unpacked_data[4], unpacked_data[5], unpacked_data[6], unpacked_data[7]),
        'gyro': (unpacked_data[8], unpacked_data[9], unpacked_data[10]),
        'input': (unpacked_data[11], unpacked_data[12], unpacked_data[13], unpacked_data[14]),
        'battery': (unpacked_data[15], unpacked_data[16]),
        'num_motors': unpacked_data[17],
        'motor_rpms': unpacked_data[18:18 + unpacked_data[17]]
    }
    return telemetry

def display_telemetry():
    udp_ip = "127.0.0.1"
    udp_port = 9001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    cv2.namedWindow('Telemetry', cv2.WINDOW_AUTOSIZE)

    while True:
        data, addr = sock.recvfrom(1024)
        telemetry = parse_telemetry_data(data)
        if telemetry is None:
            continue

        img = np.zeros((600, 1024, 3), dtype=np.uint8)

        cv2.putText(img, f"Timestamp: {telemetry['timestamp']:.2f} s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f"Position: {telemetry['position']}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f"Battery: {telemetry['battery'][1]:.2f}v", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f"Motors: {telemetry['motor_rpms']}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f"Gyro: {telemetry['gyro']}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255,255), 2)
        # Draw a rectangle to verify image updates
        #cv2.rectangle(img, (10, 10), (200, 200), (255, 0, 0), 3)

        cv2.imshow('Telemetry', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_telemetry()
