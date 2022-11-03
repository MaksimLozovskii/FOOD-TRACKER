import pymongo , re , os , certifi
from flask import Flask, render_template, request, redirect
from bson.json_util import dumps

date_pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
text_pattern = "^[a-zA-Z ]*$"

DATABASEKEY = os.getenv('DATABASEKEY')
DATABASEPWD = os.getenv("DATABASEPWD")
DATABASEURI = os.getenv("DATABASEURI")

app = Flask(__name__)
mongodb_client = pymongo.MongoClient(DATABASEURI, tlsCAFile=certifi.where())

@app.route('/')
def insert_on_toDb():

    try:
        products = mongodb_client.foodTracker.products.find()
        return render_template("index.html", products=products)
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/handle_data', methods=['POST'])
def handle_data():
    productName = request.form['productName']
    expiryDate = request.form["expiryDate"]
    databaseKey = request.form["databaseKey"]

    if re.match(date_pattern, expiryDate) and re.match(text_pattern, productName) and databaseKey == DATABASEKEY:

        products = mongodb_client.foodTracker.products.find()

        for product in products:
            if(productName == product["productName"]):
                return render_template("error.html")
        
        mongodb_client.foodTracker.products.insert_one({'productName': productName, "expiryDate": expiryDate})
        return redirect("/")

    else:
        return render_template("error.html")