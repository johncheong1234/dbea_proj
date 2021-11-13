import requests, json
from functions import url

def getTransactionTypes(tID):
    serviceName = 'getTransactionTypes'
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

    types = response.json()['Content']['ServiceResponse']['TransactionTypeList']['TransactionType']
    ID_List= []
    Name_List = []
    
    for i in range(len(types)):
        transactionType = types[i]
        ID_List.append(transactionType['TransactionTypeID'])
        Name_List.append(transactionType['TransactionTypeName'])

    if tID in ID_List:
        index = ID_List.index(tID)
        return Name_List[index]
    else:
        return 'Record not found'


                   
                         
        

