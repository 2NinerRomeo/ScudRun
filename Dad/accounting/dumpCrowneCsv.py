#import sys
import dbConnect as db
import pdb
import csv
import io

CREDFILENAME = 'creds.json'

def rowToCsv(row, delimiter=','):
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    # Write the row to the CSV writer
    csv_writer.writerow(row)
    
    # Retrieve the CSV formatted string
    csv_string = output.getvalue().strip()  # strip to remove extra newlines
    output.close()

    return csv_string    


def dumpTransactions(db):
    theCursor = db.db.cursor()

    #get the list of unmatched transactions
    query = ("SELECT cardTransactions.id,postDate,description,bankAccts.name,"
             "transCat.amount "
             "FROM cardTransactions INNER JOIN transCat ON cardTransactions.id "
             "= transCat.transId INNER JOIN expCategories ON transCat.catId = "
             "expCategories.id INNER JOIN bankAccts ON cardTransactions.card_id "
             "= bankAccts.id "
             "WHERE expCategories.name = 'BeAirborne' OR "
             "expCategories.name = 'Hangar'")
    theCursor.execute(query)
    theResults = theCursor.fetchall()

    #how many reusults
    transCount = len(theResults)
    currentTrans = 1
    lastMsg = "Classifying expenditures"
    
    #Go through the rows, output results
    f = open("examplefile.csv","a")
    f.write('Entry Number;Expense Date;Vendor;Expense Account;Expense Amount\n')
    for row in theResults:
        lrow = list(row)
        lrow[4] = lrow[4]*-1
        print(lrow)
        csvRow = rowToCsv(lrow,';')
        print(csvRow)
        f.write(csvRow + '\n')

    f.close()

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

