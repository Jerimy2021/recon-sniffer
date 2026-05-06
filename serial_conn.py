import serial
import requests
import time


SERIAL_PORT = 'COM5'   # Linux: '/dev/ttyUSB0'
BAUD_RATE = 9600

# Server endpoint
SERVER_URL = "http://127.0.0.1:5000/api/auth"


def parse_data(line):
    """
    Parse Arduino string like:
    ID:23,STATUS:OK,SCORE:87
    """
    try:
        parts = line.strip().split(',')
        data = {}
        for p in parts:
            key, value = p.split(':')
            data[key] = value
        return data
    except Exception:
        return None


def send_to_server(url, data):
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"Sent: {data} | Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # wait for connection
        print("Listening to Arduino...")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore')
                print(f"Raw: {line.strip()}")

                parsed = parse_data(line)
                if parsed:
                    send_to_server(SERVER_URL, parsed)

    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()