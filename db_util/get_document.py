import bson
import traceback
import pymongo as py

def mongodb_document(conn,key):
    try:
        db = conn.marketplace
        all_collections = db.list_collection_names()
        registers = []
        
        for collection in all_collections:
            get_register = db[collection].find({"key":key})
            for register in get_register:
                registers.append(register)
        if len(registers) == 0:
            foundkey = False
        else:
            foundkey = True
        
        return foundkey
    except Exception as e:
        traceback.print_exc()
        print("Error al intentar obtener documento: %s" %e)