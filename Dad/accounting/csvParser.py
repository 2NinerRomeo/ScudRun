import csv
import sys

class CSVParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.headers = []

    def read_csv(self):
        """Reads the CSV file and stores the data in the data attribute."""
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                self.headers = next(csv_reader)
                self.data = [row for row in csv_reader]
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_column(self, column_name):
        """Returns a list of values from a specific column."""
        if not self.headers:
            print("CSV file not read yet. Please call read_csv() first.")
            return []

        if column_name not in self.headers:
            print(f"Column '{column_name}' not found in CSV file.")
            return []

        index = self.headers.index(column_name)
        return [row[index] for row in self.data]

    def to_dict_list(self):
        """Converts the CSV data to a list of dictionaries."""
        if not self.headers:
            print("CSV file not read yet. Please call read_csv() first.")
            return []

        return [dict(zip(self.headers, row)) for row in self.data]

# Usage example
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the CSV file as an argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    csv_parser = CSVParser(file_path)
    csv_parser.read_csv()
    
    # Get a specific column
    column_name = 'column_name'  # Replace with the actual column name you want to retrieve
    column_data = csv_parser.get_column(column_name)
    print(f"Data from column '{column_name}':")
    print(column_data)
    
    # Convert to list of dictionaries
    dict_list = csv_parser.to_dict_list()
    print("CSV data as list of dictionaries:")
    print(dict_list)
