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
        #No conexión, salida anticipada
        return

    try:
        collection = conn.bmsDB[entity]
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontró la colección en la base de datos: %s" %e)
    

    key = str(uuid.uuid1())

    try:
        body.setdefault("key", key)
        collection.insert_one(body)
    except Exception as e:
        print("Error al insertar documento en base de datos: %s" %e)
    
    conn.close() 
    
    response = {
        "key":key,
        "success": "true",
        "configuration": {
            "meta": {
                "status": {
                    "code": "00",
                    "message_ilgn": [{
                        "locale": "es_PE",
                        "value": "Se registró satisfactoriamente."
                    }]
                }
            }
        }
    }
    print("Response payload: ", json.dumps(response))
    return response