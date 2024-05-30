import csv

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
    csv_parser = CSVParser('path_to_your_file.csv')
    csv_parser.read_csv()
    
    # Get a specific column
    column_data = csv_parser.get_column('column_name')
    print(column_data)
    
    # Convert to list of dictionaries
    dict_list = csv_parser.to_dict_list()
    print(dict_list)
