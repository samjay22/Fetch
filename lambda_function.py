import datetime
import json
import DatabaseLogic
import base64

NewObject = DatabaseLogic.Connection()


def AddTransaction(Data):
    Payer, Points, TimeStamp = Data["payer"], Data["points"], Data["timestamp"]
    NewObject.NewTransaction(Payer, Points, TimeStamp)
    return {
        'statusCode': 200,
        'body': "Transaction Added!"
    }


def RedeemPoints(Data):
    Points = int(Data["points"])
    UsageResults = NewObject.SpendPoints(Points)
    CurrentTime = datetime.datetime.now()
    Today = CurrentTime.strftime("%Y-%d-%mT%H:%M:%SZ")

    for Payer, Points in UsageResults.items():
        NewObject.NewTransaction(Payer, Points, Today)

    return {
        'statusCode': 200,
        'body': json.dumps(UsageResults)
    }


def CheckBal():
    return {
        'statusCode': 200,
        'body': json.dumps(NewObject.VewBalance())
    }


def NewTable():
    NewObject.CreateTable()
    return {
        'body': 'table created'
    }


def DropTable():
    NewObject.DropTable()
    return {
        'body': 'table deleted'
    }


POST = {
    '/RedeemPoints': RedeemPoints,
    '/AddTransaction': AddTransaction,
}  # Make it easy to call methods

GET = {
    '/GetBalance': CheckBal,
    '/DropTable': DropTable,
    '/NewTable': NewTable,
}


def lambda_handler(event="", context=""):
    RawPath = event["rawPath"]

    if RawPath in POST:
        Data = base64.b64decode(event['body'])
        ParsedData = json.loads(Data)
        Method = POST[RawPath]
        return Method(ParsedData)
    elif RawPath in GET:
        Method = GET[RawPath]
        return Method()
    else:
        return {
            'statusCode': 404,
            'body': json.dumps("No path exists under {}!".format(RawPath))
        }
