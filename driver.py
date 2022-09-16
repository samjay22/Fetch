import json
import requests

List = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
, { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
, { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
, { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
, { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]

'''
DropTable is a route which drops the data base table to run a new test.
NewTable creates a new table for the new test.
AddTransaction creates a new transaction and stores it using an AWS API gateway to lambda which connects to a MYSQL database.
RedeemPoints invokes AddTransaction's class method apart of the databaselogic.py class def. This route redeems points from data in db.
GetBalance is a route which gets all database info and displays it.

All the code is in this solution, it is a carbon copy of the server minus the driver code in this py script. 
'''

Endpoint = 'https://keic1qsxuc.execute-api.us-east-1.amazonaws.com/'



print(requests.get(Endpoint + 'DropTable'))
print(requests.get(Endpoint + 'NewTable'))


for Request in List:
    print(requests.post(Endpoint + 'AddTransaction',
                        data=json.dumps(Request)).content)

print(requests.post(Endpoint + 'RedeemPoints', data=json.dumps(
        {"points" : 5000})).content)