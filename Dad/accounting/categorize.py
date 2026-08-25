#import sys
import dbConnect as db
import pdb
from os import system, name
from time import sleep

CREDFILENAME = 'creds.json'
PAYMENT_DESCRIPTIONS = {
    'Payment Thank You - Web',
    'Returned Payment',
    'ONLINE PAYMENT - THANK YOU',
}

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
    print("s - skip\nq - quit")

def printTransactionInfo(trans):
    print("Transaction# " + str(trans[0]))
    print("Vendor:      " + trans[2])
    print("Amount:      " + str(trans[3]))
    print("Date:        " + str(trans[1]))
    #print(trans) #Debug

def repeatedTransactions(cursor):
    query = ("SELECT cardTransactions.description, cardTransactions.amount, "
             "transCat.catId, COUNT(*) FROM cardTransactions INNER JOIN transCat "
             "ON cardTransactions.id = transCat.transId "
             "GROUP BY cardTransactions.description, cardTransactions.amount, "
             "transCat.catId HAVING COUNT(*) > 1")
    cursor.execute(query)

    repeated = {}
    ambiguous = set()
    for description, amount, catId, count in cursor.fetchall():
        key = (description, amount)
        if key in repeated and repeated[key] != catId:
            ambiguous.add(key)
        else:
            repeated[key] = catId

    for key in ambiguous:
        del repeated[key]
    return repeated

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
    query = ("SELECT id,postDate,description,cardTransactions.amount,"
            "transCat.amount from cardTransactions LEFT JOIN transCat"
            " ON cardTransactions.id = transCat.transId WHERE "
             "transCat.amount IS NULL")
    theCursor.execute(query)
    theResults = theCursor.fetchall()
    repeated = repeatedTransactions(theCursor)

    #how many reusults
    transCount = len(theResults)
    currentTrans = 1
    lastMsg = "Classifying expenditures"
    
    #Have user classify single-category transactions
    for row in theResults:
        if row[2] in PAYMENT_DESCRIPTIONS:
            currentTrans = currentTrans + 1
            continue
        print(lastMsg)
        printLabelMenu(catDict)
        print('\ntransaction ' + str(currentTrans) + '/' + str(transCount))
        printTransactionInfo(row)
        suggestion = repeated.get((row[2], row[3]))
        if suggestion is not None:
            print('Suggested category: ' + catDict[suggestion] + ' (y)')
        choice = input('Enter Category:')
        if choice == 'q':
            db.db.commit()
            exit()
        elif choice == 's':
            print('skipping')
            continue
        elif choice.lower() == 'y' and suggestion is not None:
            choice = suggestion
        elif choice == '':
            print('try again')
            continue
        else:
            while(not int(choice) in catDict):
                choice = input(choice +' was not one of your choices, try again ')

        lastMsg = ('transaction# ' + str(row[0]) + " " + str(row[3]) +
                   ' categorized as ' + catDict[int(choice)])
        query = ("INSERT INTO transCat (transId, catId, amount) VALUES"
                 " (%s, %s, %s)")
        vals = (row[0],choice,row[3])
        theCursor.execute(query,vals)
        db.db.commit()

        sleep(0.5)
        currentTrans = currentTrans + 1 
        clear();
    db.db.commit()



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

