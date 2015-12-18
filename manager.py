import manager_django_pb2
import random
from grpc.beta import implementations
import grpc
import time
import os

_ONE_DAY_IN_SECONDS = 24 * 60 *60

class Manager(manager_django_pb2.BetaManagerServicer):
    def OpenFile(self, request, context):
        print "inside OpenFile"

        filePath = request.open_path
        timeStamp = request.timestamp

        #THIS IS TEST NAIVE CODE
        with open(filePath, 'r') as f:
          read_data = f.read()

        #NEED RPC CALLS TO THE NAME NODE HERE

        #NEED RPC CALLS TOT THE DATA NODES HERE


        #please return the file as = open_file
        return manager_django_pb2.OpenResponse(open_file=read_data)


    def SaveFile(self, request, context):
        finalMessage = "Inside SaveFile()!"

        #SaveFile request has file, filepath, and timestamp
        saveFile = request.save_file
        path = request.save_path
        timestamp = request.timestamp


        #TEAM DFS SHOULD IMPLEMENT RPC CALL NAMENODE CALL HERE






        #Sha1 of Path (160 bits) & JSON(List of datanodes) [(ip, port), (ip, port)], Blocksize
        # path = SHA1.Path
        # JSON = [(12.12.12.12, 1234), (12.12.12.12, 1345)]
        # Blocksize 123

        # Now talk to the DataNodes









        #This is just test code for saving file
        filename = os.path.basename(path)

        with open(filename, 'wb') as f:
            f.write(saveFile)

        #You can return whatever you like on write
        return manager_django_pb2.SaveResponse(transfer_status='%s' % finalMessage)

  

#Host Manager Server
def serve():
    #Reading off of the manager.proto, creating Manager class
    server = manager_django_pb2.beta_create_Manager_server(Manager())
    server.add_insecure_port('[::]:50050')
    server.start()
    try:
      while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
  serve()