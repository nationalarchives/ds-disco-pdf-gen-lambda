import PrepareFiles

data = '{ "Iaid": "C7351413", "ReplicaId": "769c283b-1676-4eb6-a85b-63c7e6eb5272", "Reference": "WO 95/1105/1", "FileExtension": "pdf", "MaxDeliverySize": 46925 }'

input_vars = PrepareFiles.get_input_variables(data)

replica = PrepareFiles.get_replica(input_vars['ReplicaId'])

replica.process_files(input_vars['FileExtension'],input_vars['MaxDeliverySize'],input_vars['Reference'])

