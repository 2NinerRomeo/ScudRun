import csv
import sys
import dbConnect as db
import csvParser as csv
import pdb

CREDFILENAME = 'creds.json'

#def allItemsInList(candidateList, standardList):


if len(sys.argv) < 2:
    print("Please provide the path to the CSV file as an argument.")
    sys.exit(1)
file_path = sys.argv[1]
cardCsv = csv.CSVParser(file_path)
cardCsv.read_csv()

finDb = db.Dbase(CREDFILENAME)
finDb.connect()

# Get a specific column
#column_name = 'column_name'  # Replace with the actual column name you want to retrieve
#column_data = cardCsv.get_column(column_name)
#print(f"Data from column '{column_name}':")
#print(column_data)

# Convert to list of dictionaries
dict_list = cardCsv.to_dict_list()
#print("CSV data as list of dictionaries:")
#print(dict_list)

chaseList = ['Transaction Date',
             'Post Date',
             'Description',
             'Category',
             'Type',
             'Amount',
             'Memo']
amexList = ['Date',
            'Description',
            'Card Member',
            'Account #',
            'Amount']

print(cardCsv.headers)
print(type(cardCsv.headers))

if(cardCsv.headers == chaseList):
   print("Looks Like a Chase Statement")
elif(cardCsv.headers == amexList):
   print("Looks Like an Amex Statement")
else:
   print("Looks like an unknown Statement")

# A python idiomatic way of checking for all the right
# column headers, but it is not logically the same, since
# there could be extra headers in the incoming file
#if(all(item in cardCsv.headers for item in chaseList)):
#   print("Chase statement alterative")
#else:
#   print("Maybe not chase")

pdb.set_trace()