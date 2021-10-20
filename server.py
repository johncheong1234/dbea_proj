from flask import Flask
import requests, json
from functions import url

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)