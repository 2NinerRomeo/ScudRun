#import sys
import dbConnect as db
import pdb
from os import system, name
from time import sleep

CREDFILENAME = 'creds.json'

def dumpTransactions(db):
    theCursor = db.db.cursor()

    #get the list of unmatched transactions
    query = ("SELECT cardTransactions.id,postDate,description,transCat.amount "
             "FROM cardTransactions INNER JOIN transCat ON cardTransactions.id "
             "= transCat.transId INNER JOIN expCategories ON transCat.catId = "
             "expCategories.id WHERE expCategories.name = 'BeAirborne' OR "
             "expCategories.name = 'Hangar'")
    theCursor.execute(query)
    theResults = theCursor.fetchall()

    #how many reusults
    transCount = len(theResults)
    currentTrans = 1
    lastMsg = "Classifying expenditures"
    
    #Have user classify single-category transactions
    for row in theResults:
         print(row)

#_________________________Things get started here ____________________________#

# Don't need an argument for this, just connect to the database
#if len(sys.argv) < 2:
#    print("Please provide the path to the CSV file as an argument.")
#    sys.exit(1)
#file_path = sys.argv[1]

finDb = db.Dbase(CREDFILENAME)
finDb.connect()

dumpTransactions(finDb)

#pdb.set_trace()

