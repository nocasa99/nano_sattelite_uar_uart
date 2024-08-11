import serial

class UARTReader:
    def __init__(self, port='COM4', baudrate=115200):
        self.ser = None
        self.connect(port, baudrate)

    def connect(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

    def read_line(self):
        if self.ser and self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').strip()
            print(f"Received line: {line}")  # Debug statement
            try:
                data_values = line.split(',')
                required_fields = ['Temperature', 'Humidity', 'Pressure', 'Altitude', 'Velocity', 'Latitude', 'Longitude']
                numeric_values = []
                for field in required_fields:
                    matched = False
                    for value in data_values:
                        if value.strip().startswith(field):
                            try:
                                numeric_value = float(value.split(':')[1].strip())
                                numeric_values.append(numeric_value)
                                matched = True
                                break
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing value: {value}. {e}")
                                return None
                    if not matched:
                        print(f"Field {field} not found in received line.")
                        return None
                if len(numeric_values) == len(required_fields):
                    return numeric_values
                else:
                    print("Incomplete data received.")
                    return None
            except ValueError as e:
                print(f"Error parsing line: {line}. {e}")
                return None
        return None
