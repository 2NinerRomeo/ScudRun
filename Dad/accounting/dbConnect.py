import mysql.connector
import json

class Dbase:
    def __init__(self,credFileName):
        self.credFileName = credFileName
    def connect(self):
        creds = json.load(open('creds.json'))
        #for i in creds:
        #    print(i)

        print (creds['host'])
        print (creds['user'])
        print (creds['pass'])

        self.db = mysql.connector.connect(
          host=creds['host'],
          user=creds['user'],
          password=creds['pass'])
        print(self.db)

if __name__ == "__main__":
    db = Dbase('creds.json')
    db.connect();
    
    
