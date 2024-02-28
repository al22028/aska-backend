import csv
import functools

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def log_comment(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Function %s with %s %s", func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return wrapper

class CSVAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_csv()
    
    @log_comment
    def read_csv(self):
        data = []
        with open(self.filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if not row or all(cell == '' for cell in row):
                    continue
                data.append([float(cell) if cell else 0 for cell in row])
        
        for x in data:
            x.pop(-1)
            x.pop(10)
        return data

    @log_comment
    def find_min_value_coordinates(self):
        min_value_coordinates = []
        rows = len(self.data)
        cols = len(self.data[0])

        for i in range(rows):
            for j in range(cols):
                value = self.data[i][j]
                if value == min(self.data[i]) and value == min(self.data[row][j] for row in range(rows)):
                    min_value_coordinates.append((i+1, j+1))
        
        return min_value_coordinates

    @log_comment
    def find_min_value_coordinates(self):
        min_value_coordinates = []
        rows = len(self.data)
        cols = len(self.data[0])

        for i in range(rows):
            for j in range(cols):
                value = self.data[i][j]
                if value == min(self.data[i]) or value == min(self.data[row][j] for row in range(rows)):
                    min_value_coordinates.append((i+1, j+1))
        
        return min_value_coordinates
    
    def find_min_value_coordinates_row(self, row):
        min_value_coordinates = []
        rows = len(self.data)
        cols = len(self.data[0])

        for i in range(rows):
            for j in range(cols):
                value = self.data[i][j]
                if value == min(self.data[i]) or value == min(self.data[row][j] for row in range(rows)):
                    min_value_coordinates.append((i+1, j+1))
        
        return min_value_coordinates[row]

    @log_comment
    def calculate_deviations(self):
        deviations = []
        rows = len(self.data)
        cols = len(self.data[0])

        for i in range(rows):
            row_deviation = sum(self.data[i]) / cols
            deviations.append(row_deviation)
        
        for j in range(cols):
            col_data = [self.data[i][j] for i in range(rows)]
            col_deviation = sum(col_data) / rows
            deviations.append(col_deviation)
        
        return deviations

# def setup_logger():
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
