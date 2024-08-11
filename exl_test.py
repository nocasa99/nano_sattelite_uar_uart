import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import QTimer
from datetime import datetime
import save_to_excel
import numpy as np

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

        self.grid_layout = QGridLayout()
        self.scroll_layout.addLayout(self.grid_layout)

        self.temp_plot_widget = pg.PlotWidget(title="Temperature")
        self.temp_plot_widget.setLabel('bottom', 'Time')
        self.temp_plot_widget.setLabel('left', 'Temperature')
        self.temp_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.temp_plot_widget, 0, 1, 1, 2)
        self.temp_plot = self.temp_plot_widget.plot()
        self.temp_data = []

        self.hum_plot_widget = pg.PlotWidget(title="Humidity")
        self.hum_plot_widget.setLabel('bottom', 'Time')
        self.hum_plot_widget.setLabel('left', 'Humidity')
        self.hum_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.hum_plot_widget, 0, 3, 1, 2)
        self.hum_plot = self.hum_plot_widget.plot()
        self.hum_data = []

        self.pres_plot_widget = pg.PlotWidget(title="Pressure")
        self.pres_plot_widget.setLabel('bottom', 'Time')
        self.pres_plot_widget.setLabel('left', 'Pressure')
        self.pres_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.pres_plot_widget, 1, 1, 1, 2)
        self.pres_plot = self.pres_plot_widget.plot()
        self.pres_data = []

        self.alt_plot_widget = pg.PlotWidget(title="Altitude")
        self.alt_plot_widget.setLabel('bottom', 'Time')
        self.alt_plot_widget.setLabel('left', 'Altitude')
        self.alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.alt_plot_widget, 1, 3, 1, 2)
        self.alt_plot = self.alt_plot_widget.plot()
        self.alt_data = []

        self.vel_plot_widget = pg.PlotWidget(title="Velocity")
        self.vel_plot_widget.setLabel('bottom', 'Time')
        self.vel_plot_widget.setLabel('left', 'Velocity')
        self.vel_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.vel_plot_widget, 2, 1, 1, 2)
        self.vel_plot = self.vel_plot_widget.plot()
        self.vel_data = []

        self.lat_long_plot_widget = pg.PlotWidget(title="Latitude vs Longitude")
        self.lat_long_plot_widget.setLabel('bottom', 'Longitude')
        self.lat_long_plot_widget.setLabel('left', 'Latitude')
        self.lat_long_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.lat_long_plot_widget, 2, 3, 1, 2)
        self.lat_long_plot = self.lat_long_plot_widget.plot(pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
        self.lat_long_data = []

        self.temp_alt_plot_widget = pg.PlotWidget(title="Temperature vs Altitude")
        self.temp_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.temp_alt_plot_widget.setLabel('left', 'Temperature')
        self.temp_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.temp_alt_plot_widget, 3, 1, 1, 2)
        self.temp_alt_plot = self.temp_alt_plot_widget.plot()
        self.temp_alt_data = []

        self.hum_alt_plot_widget = pg.PlotWidget(title="Humidity vs Altitude")
        self.hum_alt_plot_widget.setLabel('bottom', 'Altitude')
        self.hum_alt_plot_widget.setLabel('left', 'Humidity')
        self.hum_alt_plot_widget.setFixedSize(500, 400)
        self.grid_layout.addWidget(self.hum_alt_plot_widget, 3, 3, 1, 2)
        self.hum_alt_plot = self.hum_alt_plot_widget.plot()
        self.hum_alt_data = []

        self.last_timestamp = None  # To keep track of the last timestamp read

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000)  # Update plots every 1 second

    def update_plots(self):
        excel_handler = save_to_excel.ExcelHandler(filename='uart_data.xlsx')
        data = excel_handler.read_data()

        if not data:
            return

        if self.last_timestamp:
            new_data = [record for record in data if record[0] and record[0] > self.last_timestamp]
        else:
            new_data = data

        if not new_data:
            return

        # Update the last timestamp
        self.last_timestamp = new_data[-1][0]

        # Filter out rows with None or invalid data
        def is_valid_row(row):
            try:
                return all(val is not None and (i == 0 or isinstance(val, (int, float))) for i, val in enumerate(row))
            except (TypeError, ValueError):
                return False

        new_data = [row for row in new_data if is_valid_row(row)]

        # Unpack the data, converting all values to float where applicable
        timestamps = [float(record[0]) for record in new_data if record[0] is not None]
        temps = [float(record[1]) for record in new_data if record[1] is not None]
        hums = [float(record[2]) for record in new_data if record[2] is not None]
        press = [float(record[3]) for record in new_data if record[3] is not None]
        alts = [float(record[4]) for record in new_data if record[4] is not None]
        vels = [float(record[5]) for record in new_data if record[5] is not None]
        lats = [float(record[6]) for record in new_data if record[6] is not None]
        longs = [float(record[7]) for record in new_data if record[7] is not None]

        # Append new data to the existing data
        self.temp_data.extend(zip(timestamps, temps))
        self.hum_data.extend(zip(timestamps, hums))
        self.pres_data.extend(zip(timestamps, press))
        self.alt_data.extend(zip(timestamps, alts))
        self.vel_data.extend(zip(timestamps, vels))
        self.lat_long_data.extend(zip(longs, lats))
        self.temp_alt_data.extend(zip(alts, temps))
        self.hum_alt_data.extend(zip(alts, hums))

        # Convert to numpy arrays for plotting
        def plot_data(plot, data):
            if data:
                data_array = np.array(data)
                # Ensure all data is float
                if not np.issubdtype(data_array.dtype, np.number):
                    data_array = data_array.astype(float)
                plot.setData(data_array[:, 0], data_array[:, 1])

        plot_data(self.temp_plot, self.temp_data)
        plot_data(self.hum_plot, self.hum_data)
        plot_data(self.pres_plot, self.pres_data)
        plot_data(self.alt_plot, self.alt_data)
        plot_data(self.vel_plot, self.vel_data)
        plot_data(self.lat_long_plot, self.lat_long_data)
        plot_data(self.temp_alt_plot, self.temp_alt_data)
        plot_data(self.hum_alt_plot, self.hum_alt_data)

def main():
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
