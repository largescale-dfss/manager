from grpc.beta import implementations

import sys
import manager_django_pb2
import time
import os

_TIMEOUT_SECONDS = 100

def sendFile(transferFile, filePath, timeStamp):
  channel = implementations.insecure_channel('localhost', 50050)
  stub = manager_django_pb2.beta_create_Manager_stub(channel)

  response = stub.SaveFile(manager_django_pb2.SaveRequest(save_file=transferFile, save_path=filePath, timestamp=timeStamp), _TIMEOUT_SECONDS)

  print response.transfer_status





def openFile(filePath, timeStamp):
	print "Reading file from Manager"


	channel = implementations.insecure_channel('localhost', 50050)
	stub = manager_django_pb2.beta_create_Manager_stub(channel)

	response = stub.OpenFile(manager_django_pb2.OpenRequest(open_path=filePath, timestamp=timeStamp), _TIMEOUT_SECONDS)

	fileContent = response.open_file

	#the response should be a file
	
	#This is just test code for saving file
	filename = os.path.basename(filePath)

	with open(filename, 'wb') as f:
		f.write(fileContent)



	return response



with open('/Users/darwin/Desktop/test.txt', 'r') as f:
  read_data = f.read()

filePath = "/User01/test.txt"
#time.time is float by default so cutting off decimal points
timestamp = int(time.time())

# print read_data
# print type(read_data)

# sendFile(read_data, filePath, timestamp)

openFile("/Users/darwin/Desktop/test.txt", 12345)


f.closed