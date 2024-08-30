import csv
import sys
import dbConnect as db
import csvParser as csv
from enum import Enum
import pdb

CREDFILENAME = 'creds.json'

class CardType(Enum):
    CSP = 1
    AMXP = 2

def loadTransactions(db,csv,card):
    theCursor = db.db.cursor()

    if card == CardType.CSP:
        print("Looks Like a Chase Statement")
    elif card == CardType.AMXP:
        print("Looks Like an Amex Statement")
    else:
        print("Unknown Statement, should not reach here")

    query = "INSERT into cardTransactions (transDate, postDate, description, autoCat, autoType, amount, memo, account, card_id) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)"
    #vals = ("12/29/2023","12/31/2023","AR MANAGEMENT PHREESIA","Health & Wellness","Sale","-178.05","")
    vals = ('2023-12-09','2023-12-31',"AR MANAGEMENT PHREESIA","Health & Wellness","Sale","-178.05","","-5920","0")
    theCursor.execute(query,vals)
    db.db.commit()
    print(theCursor.rowcount," record inserted.");


#_________________________Things get started here ____________________________#

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

#pdb.set_trace()

if(cardCsv.headers == chaseList):
   loadTransactions(finDb,cardCsv,CardType.CSP)
elif(cardCsv.headers == amexList):
   loadTransactions(finDb,cardCsv,CardType.AMXP)
else:
   print("Unknown Statement")

# A python idiomatic way of checking for all the right
# column headers, but it is not logically the same, since
# there could be extra headers in the incoming file
#if(all(item in cardCsv.headers for item in chaseList)):
#   print("Chase statement alterative")
#else:
#   print("Maybe not chase")

#pdb.set_trace()
