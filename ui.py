import sys
import serial.tools.list_ports
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QPushButton, QScrollArea, QSizePolicy, QComboBox
from PyQt6.QtCore import QTimer, QThread,pyqtSignal
from datetime import datetime
import save_to_excel
import numpy as np
import datetime as dt
from pyqtgraph import AxisItem



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UART Dashboard')
        self.setStyleSheet("background-color: black;")

        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.input_layout = QGridLayout()

        self.port_input = QComboBox()
        self.port_input.setStyleSheet("background-color: white; color: black;")
        self.refresh_ports()

        self.input_layout.addWidget(self.port_input, 0, 0, 1, 2)

        self.apply_button = QPushButton("Apply Port")
        self.apply_button.clicked.connect(self.change_port)
        self.apply_button.setStyleSheet("background-color: white; color: black;")
        self.input_layout.addWidget(self.apply_button, 0, 4, 1, 1)

        self.scroll_layout.addLayout(self.input_layout)

        self.plots = {}
        self.data = {}
        self.grid_layout = QGridLayout()
        self.scroll_layout.addLayout(self.grid_layout)

        # sensors = ['Temperature']
        # for i, sensor in enumerate(sensors):
        #     plot_widget = pg.PlotWidget(title=sensor)
        #     plot_widget.setLabel('bottom', 'Time')
        #     plot_widget.setLabel('left', sensor)
        #     plot_widget.setFixedSize(500, 400)

        #     self.grid_layout.addWidget(plot_widget, i // 2, (i % 2) * 2 + 1, 1, 2)
        #     plot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #     plot_widget.setXRange(1 * 60, 0)
        #     plot_widget.setMouseEnabled(x=True, y=False)

        #     self.plots[sensor] = plot_widget.plot()
        #     self.data[sensor] = []

        self.temp_plot_widget = pg.PlotWidget(title="Temperature")
        self.temp_plot_widget.setLabel('bottom', 'Time')
        self.temp_plot_widget.setLabel('left', 'Temperature')
        self.temp_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.temp_plot_widget, 0, 1, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.temp_plot = self.temp_plot_widget.plot()
        self.temp_data = []

        self.hum_plot_widget = pg.PlotWidget(title="Humidity")
        self.hum_plot_widget.setLabel('bottom', 'Time')
        self.hum_plot_widget.setLabel('left', 'Humidity')
        self.hum_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.hum_plot_widget, 0, 3, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.hum_plot = self.hum_plot_widget.plot()
        self.hum_data = []

        self.pres_plot_widget = pg.PlotWidget(title="Pressure")
        self.pres_plot_widget.setLabel('bottom', 'Time')
        self.pres_plot_widget.setLabel('left', 'Pressure')
        self.pres_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.pres_plot_widget, 1, 1, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.pres_plot = self.pres_plot_widget.plot()
        self.pres_data = []

        self.alt_plot_widget = pg.PlotWidget(title="Altitude")
        self.alt_plot_widget.setLabel('bottom', 'Time')
        self.alt_plot_widget.setLabel('left', 'Altitude')
        self.alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.alt_plot_widget, 1, 3, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.alt_plot = self.alt_plot_widget.plot()
        self.alt_data = []

        self.vel_plot_widget = pg.PlotWidget(title="Velocity")
        self.vel_plot_widget.setLabel('bottom', 'Time')
        self.vel_plot_widget.setLabel('left', 'Velociy')
        self.vel_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.vel_plot_widget, 2, 1, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.vel_plot = self.vel_plot_widget.plot()
        self.vel_data = []

        self.lat_long_plot_widget = pg.PlotWidget(title="Latitude vs Longitude")
        self.lat_long_plot_widget.setLabel('bottom', 'Longitude')
        self.lat_long_plot_widget.setLabel('left', 'Latitude')
        self.lat_long_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.lat_long_plot_widget, 2, 3, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.lat_long_plot = self.lat_long_plot_widget.plot(pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
        self.lat_long_data = []

        self.temp_alt_plot_widget = pg.PlotWidget(title="Temperature vs Altitude")
        self.temp_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.temp_alt_plot_widget.setLabel('left', 'Temperature')
        self.temp_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.temp_alt_plot_widget, 6, 1, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.temp_alt_plot = self.temp_alt_plot_widget.plot(pen='y', fillLevel=-0.3, brush=(50, 50, 200, 100))
        self.temp_alt_data = []

        self.hum_alt_plot_widget = pg.PlotWidget(title="Humidity vs Altitude")
        self.hum_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.hum_alt_plot_widget.setLabel('left', 'Humidity')
        self.hum_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.hum_alt_plot_widget, 6, 3, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.hum_alt_plot = self.hum_alt_plot_widget.plot()
        self.hum_alt_data = []

        self.pres_alt_plot_widget = pg.PlotWidget(title="Pressure vs Altitude")
        self.pres_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.pres_alt_plot_widget.setLabel('left', 'Pressure')
        self.pres_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.pres_alt_plot_widget, 8, 1, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.pres_alt_plot = self.pres_alt_plot_widget.plot()
        self.pres_alt_data = []

        self.vel_alt_plot_widget = pg.PlotWidget(title="Velocity vs Altitude")
        self.vel_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.vel_alt_plot_widget.setLabel('left', 'Velocity')
        self.vel_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.vel_alt_plot_widget, 8, 3, 1, 2)
        self.temp_plot_widget.setMouseEnabled(x=True, y=False)
        self.vel_alt_plot = self.vel_alt_plot_widget.plot()
        self.vel_alt_data = []

        for i in range(9):
            self.grid_layout.setRowStretch(i, 2)
        for i in range(6):
            self.grid_layout.setColumnStretch(i, 2)

        # self.uart_reader = save_to_excel.UARTReader()
        # self.excel_handler = save_to_excel.ExcelHandler()


        # if self.uart_reader.ser:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # update data every 1 second

        # self.start_time = datetime.now()
        # print(f"Start time: {self.start_time}")

    


    def update_plot(self):

        excel_handler = save_to_excel.ExcelHandler(filename='uart_data.xlsx')

        print("Updating plot...")  # Debug statement
        last_row = excel_handler.read_last_row()  # Modify your ExcelHandler to include this method
        print(f"Last row: {last_row}")  # Debug statement

        if last_row:
            time_str, temperature, humidity, pressure, altitude, velocity, latitude, longitude = last_row
            print(f"Row data: {last_row}")  # Debug statement

            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')  # Convert string to datetime object


            if not self.temp_data:  # If there's no data yet, initialize start_time
                self.start_time = time
                print(f"Start time: {self.start_time}")
            
            elapsed_time = (time - self.start_time).total_seconds()
            print(f"Elapsed time: {elapsed_time}, Temp: {temperature}, Hum: {humidity}, Pres: {pressure}, Alt: {altitude}, Vel: {velocity}, Lat: {latitude}, Long: {longitude}")

            # self.data['Temperature'].append((elapsed_time, temperature))
            # self.data['Humidity'].append((elapsed_time, humidity))
            # self.data['Pressure'].append((elapsed_time, pressure))
            # self.data['Altitude'].append((elapsed_time, altitude))
            # self.data['Velocity'].append((elapsed_time, velocity))

            self.temp_data.append((elapsed_time, temperature))
            self.hum_data.append((elapsed_time, humidity))
            self.pres_data.append((elapsed_time, pressure))
            self.alt_data.append((elapsed_time, altitude))
            self.vel_data.append((elapsed_time, velocity))
            self.lat_long_data.append((latitude, longitude))
            self.temp_alt_data.append((altitude, temperature))
            self.hum_alt_data.append((altitude, humidity))
            self.pres_alt_data.append((altitude, pressure))
            self.vel_alt_data.append((altitude, velocity))

        # sensors = ['Temperature']
        # for sensor in sensors:
        #     if self.data[sensor]:
        #         times, values = zip(*self.data[sensor])
        #         self.plots[sensor].setData(times, values)
        #         print(f"Sensor: {sensor}, Times: {times}, Values: {values}")  # Debug statement


        if self.temp_data:
            times, temps = zip(*self.temp_data)
            self.temp_plot.setData(times, temps)
            self.temp_plot_widget.setXRange(max(times) - 60, max(times))  # Display last 60 seconds

        if self.hum_data:
            times, humiditys = zip(*self.hum_data)
            self.hum_plot.setData(times, humiditys)
            self.hum_plot_widget.setXRange(max(times) - 60, max(times))  # Display last 60 seconds

        if self.pres_data:
            times, pressures = zip(*self.pres_data)
            self.pres_plot.setData(times, pressures)
            self.pres_plot_widget.setXRange(max(times) - 60, max(times))  # Display last 60 seconds

        if self.alt_data:
            times, altitude = zip(*self.alt_data)
            self.alt_plot.setData(times, altitude)
            self.alt_plot_widget.setXRange(max(times) - 60, max(times))  # Display last 60 seconds

        if self.vel_data:
            times, velocity = zip(*self.vel_data)
            self.vel_plot.setData(times, velocity)
            self.vel_plot_widget.setXRange(max(times) - 60, max(times))  # Display last 60 seconds

        if self.lat_long_data:
            latitudes, longitudes = zip(*self.lat_long_data)
            self.lat_long_plot.setData(longitudes, latitudes)

        if self.temp_alt_data:
            altitudes_temp, temperatures = zip(*self.temp_alt_data)
            self.temp_alt_plot.setData(altitudes_temp, temperatures)

        if self.hum_alt_data:
            altitudes_hum, humidities = zip(*self.hum_alt_data)
            self.hum_alt_plot.setData(altitudes_hum, humidities)

        if self.pres_alt_data:
            altitudes_pres, pressures = zip(*self.pres_alt_data)
            self.pres_alt_plot.setData(altitudes_pres, pressures)

        if self.vel_alt_data:
            altitudes_vel, velocities = zip(*self.vel_alt_data)
            self.vel_alt_plot.setData(altitudes_vel, velocities)



    def refresh_ports(self):  # adds available ports to drop down list
        self.port_input.clear()
        ports = serial.tools.list_ports.comports()
        print("Available ports:")  # Debug statement
        for port in ports:
            print(port.device)  # Debug statement
            self.port_input.addItem(port.device)
    
        if not ports:
            print("No available ports found.")  # Debug statement

    def change_port(self):
        port_name = self.port_input.currentText()

        
        if port_name:
            self.uart_reader.connect(port_name, 115200)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()