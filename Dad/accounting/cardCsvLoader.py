import csv
import sys
import dbConnect as db
import csvParser as csv


CREDFILENAME = 'creds.json'

if len(sys.argv) < 2:
    print("Please provide the path to the CSV file as an argument.")
    sys.exit(1)
file_path = sys.argv[1]
csv_parser = csv.CSVParser(file_path)
csv_parser.read_csv()

finDb = db.Dbase(CREDFILENAME)
finDb.connect()

# Get a specific column
#column_name = 'column_name'  # Replace with the actual column name you want to retrieve
#column_data = csv_parser.get_column(column_name)
#print(f"Data from column '{column_name}':")
#print(column_data)

# Convert to list of dictionaries
dict_list = csv_parser.to_dict_list()
#print("CSV data as list of dictionaries:")
#print(dict_list)


