import pymysql
import json

EndPoint = 'ecomdb.cslidjicrb2x.us-east-1.rds.amazonaws.com'
Username = 'admin'
Password = 'password!'
DatabaseName = 'ecomdb'


class Connection(object):

    def __init__(self):
        self.Connection = pymysql.connect(host=EndPoint, user=Username, password=Password, database=DatabaseName)
        self.CreateTable()

    def Show(self):
        Cursor = self.Connection.cursor()
        Cursor.execute('''SELECT * FROM transactions ORDER BY timestamp DESC''')
        return {
            'statusCode': 200,
            'body': json.dumps(Cursor.fetchall())
        }

    def NewTransaction(self, Payer, Points, TimeStamp):
        Cursor = self.Connection.cursor()
        RecordSet = (str(Payer), int(Points), str(TimeStamp))
        Cursor.execute('''INSERT INTO transactions (payer, points, timestamp) VALUES (%s, %s, %s)''', RecordSet)
        self.Connection.commit()
        return {
            'statusCode': 200,
            'body': json.dumps(RecordSet)
        }

    def CreateTable(self):
        self.Connection.cursor().execute('''CREATE TABLE IF NOT EXISTS transactions
                        (payer text, points integer, timestamp text)''')

    def DropTable(self):
        self.Connection.cursor().execute('''DROP TABLE transactions''')

    def SpendPoints(self, PointsOwed):

        Cursor = self.Connection.cursor()
        PointsOwed = int(PointsOwed)
        CreditsHistory = {}

        Cursor.execute('''SELECT payer, points FROM transactions ORDER BY timestamp ASC''')
        Results = Cursor.fetchone()
        Index = 0

        while (Results != None) and (PointsOwed > 0):
            Payer, Owned = Results

            if Payer not in CreditsHistory:
                CreditsHistory[Payer] = 0  # Save in logs

            if PointsOwed > Owned:
                PointsOwed -= Owned
                CreditsHistory[Payer] -= Owned
            else:
                CreditsHistory[Payer] -= PointsOwed
                PointsOwed = 0

            Results = Cursor.fetchone()

        return CreditsHistory

    def VewBalance(self):
        Cursor = self.Connection.cursor()

        Bal = {}

        Cursor.execute('''SELECT payer, points FROM transactions ORDER BY timestamp ASC''')

        Results = Cursor.fetchone()

        while Results:
            Payer, Owned = Results

            if Payer not in Bal:
                Bal[Payer] = 0

            Bal[Payer] += Owned
            Results = Cursor.fetchone()

        return Bal

    def CloseDB(self):
        self.Connection.close()

