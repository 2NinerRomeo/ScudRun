#import sys
import dbConnect as db
import pdb
from os import system, name
from time import sleep

CREDFILENAME = 'creds.json'

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def printLabelMenu(labelDict):
    for cat in labelDict:
        print(str(cat) + ". " + labelDict[cat])

def printTransactionInfo(trans):
    print(trans[1])
    print(trans[2])
    print(trans[3])
    print(trans)

def assignTransactions(db):
    theCursor = db.db.cursor()

    #get the list of categories, store in dictionary
    query = "SELECT id,name FROM expCategories;"
    theCursor.execute(query)
    theResults = theCursor.fetchall()
    catDict = {};
    for row in theResults:
        catDict[row[0]]=row[1]
    clear()


    #get the list of unmatched transactions
    query = ("SELECT postDate,description,cardTransactions.amount,"
            "transCat.amount from cardTransactions LEFT JOIN transCat"
            " ON cardTransactions.id = transCat.transId;")
    theCursor.execute(query)
    theResults = theCursor.fetchall()

    #how many reusults
    transCount = len(theResults)
    currentTrans = 1

    #Have user classify single-category transactions
    for row in theResults:
        printLabelMenu(catDict)
        print('\ntransaction ' + str(currentTrans) + '/' + str(transCount))
        printTransactionInfo(row)
        input('Enter Category:')
        ##More here
        # Quit, Skip
        print('500ms')
        sleep(0.5)
        currentTrans = currentTrans + 1 
        clear();
        
        



#_________________________Things get started here ____________________________#

# Don't need an argument for this, just connect to the database
#if len(sys.argv) < 2:
#    print("Please provide the path to the CSV file as an argument.")
#    sys.exit(1)
#file_path = sys.argv[1]

finDb = db.Dbase(CREDFILENAME)
finDb.connect()

assignTransactions(finDb)

#pdb.set_trace()

