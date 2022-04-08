import traceback
import pymongo as py
import os

usr = os.environ['MONGO_DB_USER']
pwd = os.environ['MONGO_DB_PASS']
mongo_db_name = os.environ['MONGO_DB_NAME']
url = os.environ['MONGO_DB_URL']

def mongodb_connection():
    try:
        return py.MongoClient("mongodb+srv://" + usr + ":" + pwd + "@" + url + "/"+ mongo_db_name +"?retryWrites=true&w=majority")
        #return py.MongoClient("0.0.0.0:27017")
    except py.errors.ConnectionFailure as e:
        traceback.print_exc()
        print("No fue posible conectarse a la base de datos: %s" %e)