#import sys
import dbConnect as db
import pdb

CREDFILENAME = 'creds.json'

def assignTransactions(db):
    theCursor = db.db.cursor()
    query = "SELECT postDate,description,cardTransactions.amount,transCat.amount from cardTransactions LEFT JOIN transCat ON cardTransactions.id = transCat.transId;"

    theCursor.execute(query)
    theResults = theCursor.fetchall()

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

assignTransactions(finDb)

#pdb.set_trace()

