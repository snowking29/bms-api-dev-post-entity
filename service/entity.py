import uuid
import json
import bson
import traceback
import pymongo as py
from db_util.get_connection import mongodb_connection
from db_util.get_document import mongodb_document

def register(body,entity):
    conn = mongodb_connection()
    print("Info Base de datos: ", conn.server_info())
    
    if conn is None:
        #No conexi�n, salida anticipada
        return

    try:
        collection = conn.bmsDB[entity]
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontr� la colecci�n en la base de datos: %s" %e)
    
    if "key" in body:
        key = body["key"]
    else:
        key = str(uuid.uuid1())
        
    
    registerFound = mongodb_document(conn,key)
    print("�Se encontr� key?: ", registerFound)
    
    if registerFound:
        try:
            body.pop("key")
            collection.update({'key':key}, {'$push': {entity: body[entity]}}, upsert = True)
            success = "true"
            code = "00"
            value = "Se registr� satisfactoriamente."
        except Exception as e:
            print("Error al insertar documento en base de datos: %s" %e)
    else:
        try:
            body.setdefault("key", key)
            collection.insert_one(body)
            success = "true"
            code = "00"
            value = "Se registr� satisfactoriamente."
        except Exception as e:
            print("Error al insertar documento en base de datos: %s" %e)
    
    conn.close() 
    
    response = {
        "key":key,
        "success": success,
        "configuration": {
            "meta": {
                "status": {
                    "code": code,
                    "message_ilgn": [{
                        "locale": "es_PE",
                        "value": value
                    }]
                }
            }
        }
    }
    print("Response payload: ", json.dumps(response))
    return response