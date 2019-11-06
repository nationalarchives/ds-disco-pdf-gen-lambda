import PrepareFiles
import json


def prepare_files(event, context):
    if 'body' in event:
        input_vars = PrepareFiles.get_input_variables(event['body'])
        replica = PrepareFiles.get_replica(input_vars['ReplicaId'])
        status = replica.process_files(input_vars['FileExtension'],input_vars['MaxDeliverySize'],input_vars['Reference'])

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
