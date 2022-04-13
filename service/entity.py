import uuid
import json
import bson
import datetime
import traceback
import pymongo as py
from dateutil.tz import gettz
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
        print("No se encontró la coleccion en la base de datos: %s" %e)
    

    key = str(uuid.uuid1())
    
    if "creationTime" not in body:
        creationTime = datetime.datetime.now(gettz('America/Lima')).strftime("%Y-%m-%d %H:%M")
        body.setdefault("creationTime",creationTime)
        
    if "modifiedTime" not in body:
        modifiedTime = datetime.datetime.now(gettz('America/Lima')).strftime("%Y-%m-%d %H:%M")
        body.setdefault("modifiedTime",modifiedTime)

    try:
        body.setdefault("key", key)
        collection.insert_one(body)
        success = "true"
        code = "00"
        value = "Se registro satisfactoriamente."
    except Exception as e:
        print("Error al insertar documento en base de datos: %s" %e)
        success = "false"
        code = "01"
        value = "Hubo un inconveniente en al intentar insertar el documento en la base de datos."
    
    conn.close() 
    
    response = {
        "key":key,
        "success": success,
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
    print("Response payload: ", json.dumps(response))
    return response