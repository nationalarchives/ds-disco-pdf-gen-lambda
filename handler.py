import PrepareFiles
import json


def prepare_files(event, context):
    if 'body' in event['Records'][0]:
        input_vars = event['Records'][0]['body']
        input_vars = json.loads(input_vars)
        replica = PrepareFiles.get_replica(input_vars['ReplicaId'])
        status = replica.process_files(input_vars['FileExtension'],input_vars['MaxDeliverySize'],input_vars['Reference'],input_vars['Iaid'])

        response = {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "statusCode": 200,
            "body": status
        }
    else:
        response = {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "statusCode": 500,
            "body": "No event body"
        }

    return response
