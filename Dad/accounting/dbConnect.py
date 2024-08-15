import mysql.connector
import json

creds = json.load(open('creds.json'));
#for i in creds:
#    print(i)

print (creds['host'])
print (creds['user'])
print (creds['pass'])

mydb = mysql.connector.connect(
  host=creds['host'],
  user=creds['user'],
  password=creds['pass']
)

print(mydb) 
