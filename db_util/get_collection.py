import traceback
import pymongo as py

def mongodb_collection(conn,dbname,collection):
    try:
        return conn.dbname.collection
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontró la colección en la base de datos: %s" %e)