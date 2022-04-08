import json
import traceback
from service.entity import register

def handler(event, context):
    print("Evento recibido: ",json.dumps(event))
    path = event["pathParameters"]["entity"]
    try:
        body = json.loads(event['body'])
        response = register(body,path)
        
    except Exception as e:
        traceback.print_exc()
        response = {"exception",str(e)}
    
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }