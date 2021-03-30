from flask import Flask, request, Response, jsonify , make_response
from database.db import initialize_db
from database.models import Balance
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/bank-bag'
}

initialize_db(app)

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ab2HmEAghK1-vTIE8FUZD60ArSMk0o1DsZ7aJi_d52k'
service = build('sheets', 'v4', credentials=creds)


def get_balance():
    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if intent_name=='get_balance':
        bal = Balance.objects.get(name="john").to_json()
        bal = json.loads(bal)
        return {
    'fulfillmentMessages': [
        {
            'text': {
                'text': [
                
                bal["balance"]
                
                ]
            }
        }
        ]
    }

def order_book():
    from datetime import datetime, date
    today = date.today()
    date = today.strftime("%b-%d-%Y")
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    ab= [["samiya",date, time]]

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="sales!A1",valueInputOption="USER_ENTERED", body={"values" : ab}).execute()
    values = result.get('values', [])
    if intent_name=='order_book':
        return {
    'fulfillmentMessages': [
        {
            'text': {
                'text': [
                "Ok, your order has been approved. Date for collection of cheque book will be informed soon"
                ]
            }
        }
        ]
    }

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name=='order_book' :
        return make_response(jsonify(order_book()))

    elif intent_name=='get_balance':
        return make_response(jsonify(get_balance()))

# run the app
if __name__ == '__main__':
   app.run()




