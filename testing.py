# import openpyxl
# import sys
# import pyqtgraph as pg
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from PyQt6.QtCore import QTimer
# from datetime import datetime

# class ExcelHandler:
#     def __init__(self, filename='uno_data.xlsx'):
#         self.filename = filename
#         self.load_workbook()

#     def load_workbook(self):
#         try:
#             self.workbook = openpyxl.load_workbook(self.filename, data_only=True)
#             self.worksheet = self.workbook.active
#         except FileNotFoundError:
#             self.workbook = openpyxl.Workbook()
#             self.worksheet = self.workbook.active
#             self.worksheet.append(['Time', 'Temperature', 'Humidity', 'Pressure', 'Altitude', 'Velocity', 'Latitude', 'Longitude'])

#     def read_data(self):
#         rows = list(self.worksheet.iter_rows(min_row=2, values_only=True))
#         parsed_rows = [(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), *row[1:]) for row in rows]
#         return parsed_rows

#     # def save_data(self, timestamp, data_points):
#     #     self.worksheet.append([timestamp.strftime('%Y-%m-%d %H:%M:%S')] + data_points)
#     #     self.workbook.save(self.filename)


# # Create a DataFrame with test data
# # data = {
# #     'Time': ['2024-07-03 12:00:00', '2024-07-03 12:01:00', '2024-07-03 12:02:00'],
# #     'Temperature': [22.5, 22.6, 22.7],
# #     'Humidity': [60, 61, 62],
# #     'Pressure': [1013, 1012, 1011],
# #     'Altitude': [150, 155, 160],
# #     'Velocity': [10, 12, 14],
# #     'Latitude': [35.6895, 35.6896, 35.6897],
# #     'Longitude': [139.6917, 139.6918, 139.6919]
# # }

# # # Create a DataFrame
# # df = pd.DataFrame(data)

# # # Save the DataFrame to an Excel file
# # excel_file = 'uno_data.xlsx'
# # df.to_excel(excel_file, index=False)

# # print(f"Test data saved to {excel_file}")

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Temperature vs Time Plot')
#         self.setGeometry(100, 100, 800, 600)

#         self.main_widget = QWidget()
#         self.layout = QVBoxLayout(self.main_widget)
#         self.setCentralWidget(self.main_widget)

#         self.plot_widget = pg.PlotWidget(title='Temperature vs Time')
#         self.plot_widget.setLabel('bottom', 'Time')
#         self.plot_widget.setLabel('left', 'Temperature (°C)')
#         self.layout.addWidget(self.plot_widget)
#         self.temperature_plot = self.plot_widget.plot(pen='y')

#          # Temperature vs Altitude plot
#         self.temp_alt_plot_widget = pg.PlotWidget(title='Temperature vs Altitude')
#         self.temp_alt_plot_widget.setLabel('bottom', 'Altitude (m)')
#         self.temp_alt_plot_widget.setLabel('left', 'Temperature (°C)')
#         self.layout.addWidget(self.temp_alt_plot_widget)
#         self.temp_alt_plot = self.temp_alt_plot_widget.plot(pen='b')

#         self.excel_handler = ExcelHandler()

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start(1000)  # Update every 1 second

#         self.start_time = datetime.now()

#     def update_plot(self):
#         rows = self.excel_handler.read_data()
#         times = [(row[0] - self.start_time).total_seconds() for row in rows]
#         temperatures = [row[1] for row in rows]
#         altitudes = [row[4] for row in rows]


#         self.temperature_plot.setData(times, temperatures)

#         # Update Temperature vs Altitude plot
#         self.temp_alt_plot.setData(altitudes, temperatures)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())



class vaccine():
    def __init__(self, vacc, origin, interval):
        self.vacc = vacc
        self.origin = origin
        self.interval = interval

    
    
class Person():
    def __init__(self,name, age, prof):
        self.name = name
        self.age = age
        self.prof = prof

    def pushVaccine(self, vaccine):
        self.vaccine = vaccine

        print(f"Name: {self.name} Age: {self.age} Type: {self.prof}")
        

    def showDetail(self):