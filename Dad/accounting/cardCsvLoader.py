import csv
import sys
import dbConnect as db
import csvParser as csv
from enum import Enum
import datetime
import pdb

CREDFILENAME = 'creds.json'

class CardType(Enum):
    CSP = 1
    AMXP = 2

def loadTransactions(db,cardDictLst,card):
    theCursor = db.db.cursor()

    if card == CardType.CSP:
        print("Looks Like a Chase Statement")
        for trans in cardDictLst:
            #print(trans) #Debug
            tDate = datetime.datetime.strptime(trans['Transaction Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            pDate = datetime.datetime.strptime(trans['Post Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            print("Post Date: " + pDate + " Description: " + trans['Description'] + " amount: " + trans['Amount'] )
            query = "INSERT INTO cardTransactions (transDate, postDate, description, autoCat, autoType, amount, memo, account, card_id) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)"
            vals = (tDate,pDate,trans['Description'],trans['Category'],trans['Type'],trans['Amount'],trans['Memo'],"-5920","0")
            theCursor.execute(query,vals)

    elif card == CardType.AMXP:
        print("Looks Like an Amex Statement")
        for trans in cardDictLst:
            #print(trans) #Debug
            pDate = datetime.datetime.strptime(trans['Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            amount = str(float(trans['Amount'])*-1)
            print("Post Date: " + pDate + " Description: " + trans['Description'] + " amount: " + amount )
            query = "INSERT into cardTransactions (postDate, description, amount, memo, account, card_id) VALUES (%s, %s, %s, %s, %s, %s)"
            vals = (pDate,trans['Description'],amount,trans['Card Member'],trans["Account #"],"2")
            theCursor.execute(query,vals)

    else:
        print("Unknown Statement, should not reach here")


    db.db.commit()
    #print(theCursor.rowcount," record inserted."); # only counts the last insert :(


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
cardDictList = cardCsv.to_dict_list()
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
   loadTransactions(finDb,cardDictList,CardType.CSP)
elif(cardCsv.headers == amexList):
   loadTransactions(finDb,cardDictList,CardType.AMXP)
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
