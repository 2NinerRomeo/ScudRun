import sys
from csvParser import CSVParser

def classify_entries(file_path):
    # Initialize the CSV parser and read the CSV file
    csv_parser = CSVParser(file_path)
    csv_parser.read_csv()
    
    # Get the CSV data as a list of dictionaries
    dict_list = csv_parser.to_dict_list()
    
    if not dict_list:
        print("No data found in the CSV file.")
        return
    
    classifications = {}

    print("Classify each entry with an enumerated value.")
    print("Enter 'q' to quit.")

    # Iterate through each dictionary (row) and prompt the user for classification
    for i, entry in enumerate(dict_list):
        print(f"\nEntry {i+1}/{len(dict_list)}: {entry}")
        
        while True:
            classification = input("Enter classification (integer) or 'q' to quit: ")
            
            if classification.lower() == 'q':
                print("Exiting classification process.")
                return classifications
            
            if classification.isdigit():
                classifications[i] = int(classification)
                break
            else:
                print("Invalid input. Please enter an integer value.")

    print("\nClassification complete.")
    return classifications

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the CSV file as an argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    classifications = classify_entries(file_path)
    
    # Optionally, you can save or process the classifications as needed
    print("Classifications:", classifications)
