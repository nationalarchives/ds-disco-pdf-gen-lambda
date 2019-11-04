import PrepareFiles

data = '{ "IAID": "C12738155", "RID": "0e50b4e6-e582-43d3-b38f-f8741c770efa", "AvgSize": 5000, "DeliveryType": "PDF", "CatRef": "DEFE 24/2061/1" }'

input_vars = PrepareFiles.get_input_variables(data)

replica = PrepareFiles.get_replica(input_vars['RID'])

replica.process_files(input_vars['DeliveryType'],input_vars['AvgSize'])

