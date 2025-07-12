#import sys
import dbConnect as db
import pdb
import csv
import io
from time import sleep

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
    #Year Selection
    while True:
        year = input('Choose Year: ')
        try:
            yearInt = int(year)
            print(f"Outputing transactions from '{year}'")
            break
        except:
            print(f"'{year}' is not a good year. Try again")
    #Business Selection
    busDict = {1: "BE Air + Hangar", 2: "BE Real"}
    while True:
        print(busDict)
        for business in busDict:
            print(str(business) + ". " + busDict[business])
        selectedBusiness = int(input('Choose Business: '))
        if selectedBusiness in busDict:
            print(f"Outputting transactions for " + busDict[selectedBusiness])
            sleep(0.5)
            break
        else:
            print(f"That was not one of the choices. ")
            sleep(0.5)
            continue

    theCursor = db.db.cursor()
    bname = "none"

    #get the list of unmatched transactions
    if busDict[selectedBusiness] == "BE Air + Hangar":
        query = ("SELECT cardTransactions.id,postDate,description,transCat.amount "
                 "FROM cardTransactions INNER JOIN transCat ON cardTransactions.id "
                 "= transCat.transId INNER JOIN expCategories ON transCat.catId = "
                 "expCategories.id WHERE (expCategories.name = 'BeAirborne' OR "
                 "expCategories.name = 'Hangar') AND YEAR(cardTransactions.transDate) = "
                 + str(yearInt))
        bname = "BeAirAndHangar"
    elif busDict[selectedBusiness] == "BE Real":
        query = ("SELECT cardTransactions.id,postDate,description,transCat.amount "
                 "FROM cardTransactions INNER JOIN transCat ON cardTransactions.id "
                 "= transCat.transId INNER JOIN expCategories ON transCat.catId = "
                 "expCategories.id WHERE (expCategories.name = 'BeRealEstate') "
                 "AND YEAR(cardTransactions.transDate) = "
                 + str(yearInt))
        bname = "BeRealEstate"

    theCursor.execute(query)
    theResults = theCursor.fetchall()

    print(query)

    #how many reusults
    transCount = len(theResults)
    print("Matched Records: " + str(transCount))
    #currentTrans = 1
    #lastMsg = "Classifying expenditures"
    
    #Go through the rows, output results
    ofname = str(yearInt) + "_" + bname + "_toUpload.csv"
    f = open(ofname,"a")
    for row in theResults:
        #pdb.set_trace()
        lrow = list(row)
        lrow[3] = lrow[3]*-1
        print(lrow)
        csvRow = rowToCsv(lrow,',')
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

