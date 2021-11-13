from flask import Flask, request
import requests, json
from functions import url,getRecord
from getTransactionTypes import getTransactionTypes

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/product_types")
def getAllProductTypes():
    serviceName = 'getProductTypes'
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': '',
                        'PIN': '',
                        'OTP': ''
                        }
                        }
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)

    product = response.json()['Content']['ServiceResponse']['ProductList']['Product']
    ID_List= []
    Name_List = []
    
    for i in range(len(product)):
        ProductType = product[i]
        ID_List.append(ProductType['ProductID'])
        Name_List.append(ProductType['ProductName'])
    
    print(product)

    return {'Name_list':Name_List, 'ID_list':ID_List}

@app.route("/deposit_account", methods = ['GET','POST'])
def getDepositAccountDetails():
    #Header
    data = json.loads(request.data)
    userID = data['userID']
    PIN = data['PIN']
    accountID = data['accountID']
    serviceName = 'getDepositAccountDetails'
    OTP = '999999'
    #Content
    
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': userID,
                        'PIN': PIN,
                        'OTP': OTP
                        }
                        }
    contentObj = {
                        'Content': {
                        'accountID': accountID
                        }
                        }
    final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    if errorCode == '010000':
        depositAccount = response.json()['Content']['ServiceResponse']['DepositAccount']
        return depositAccount
    elif errorCode == '010041':
        return "OTP has expired.\nYou will receiving a SMS"
    else:
        return serviceRespHeader['ErrorText']

@app.route("/transaction_history", methods = ['GET','POST'])
def getTransactionHistory():
    #Header
    serviceName = 'getTransactionHistory'
    userID = 'S9800980I'
    PIN = '123456'
    OTP = '999999'
    #Content
    accountID = '7681'
    startDate = '2021-09-10 00:00:00'
    endDate = '2021-10-20 00:00:00'
    numRecordsPerPage = '1000'
    pageNum = '1'
    
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': userID,
                        'PIN': PIN,
                        'OTP': OTP
                        }
                        }
    contentObj = {
                         'Content': {
                         'accountID': accountID,
                         'startDate': startDate,
                         'endDate': endDate,
                         'numRecordsPerPage':numRecordsPerPage,
                         'pageNum':pageNum
                         }
                         }
    final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
    response = requests.post(final_url)
    
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    if errorCode == '010000':
        history = response.json()['Content']['ServiceResponse']['CDMTransactionDetail']
        if history == {} and  serviceRespHeader['GlobalErrorID']=='010000':
            return 'No record found'
        else:
            transaction_history = history['transaction_Detail']
            # recordCount = getRecord(transaction_history)   
            return {'transaction_history':transaction_history}
            
    elif errorCode == '010041':
        return "OTP has expired.\nYou will receiving a SMS"
    else:
        return serviceRespHeader['ErrorText']

  

    
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)