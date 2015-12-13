from grpc.beta import implementations

import sys
import manager_django_pb2
import time

_TIMEOUT_SECONDS = 100

def sendFile(transferFile, filePath, timeStamp):
  channel = implementations.insecure_channel('localhost', 50050)
  stub = manager_django_pb2.beta_create_Manager_stub(channel)

  response = stub.SaveFile(manager_django_pb2.SaveRequest(save_file=transferFile, save_path=filePath, timestamp=timeStamp), _TIMEOUT_SECONDS)

  print response.transfer_status


with open('/Users/darwin/Desktop/test.txt', 'r') as f:
  read_data = f.read()

filePath = "/User01/test.txt"
#time.time is float by default so cutting off decimal points
timestamp = int(time.time())



# print read_data
# print type(read_data)

sendFile(read_data, filePath, timestamp)



f.closed