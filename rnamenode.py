##################
# Data rpc node 
#################

import time
import namenode_pb2
from grpc.beta import implementations
import sys 
from namenode import Namenode
import hashlib
#global vars
TIMEOUT = 10
DEBUG = True

class NameNode(namenode_pb2.BetaNameNodeServicer):
    
    def Store(self,request,context):
        """
        StoreRequest takes the following parameters:
            1. string file_path
            2. int32 file_size
            3. string timestamp

        StoreReply takes the following parameters:
            1. string hash(path)
            2. string datanodes
            3. int32 block_size
            4. bool success
        """
        if DEBUG:
            print("Requesting NameNode.Store")

        nn = Namenode()
        data_nodes = nn.save(request.file_path, request.file_size, request.timestamp)
        path_hash = hashlib.sha1(request.file_path).hexdigest()
        if DEBUG:
            print("Datanode.save() processed successfully")
            print("StoreReply response should be available")

        return namenode_pb2.StoreReply(path=path_hash,datanodes=str(data_nodes),block_size=nn.blocksize,success=True)

    def Read(self,request,context):
        """
        Reads a file from data node. This should simply call
        dfss.Read() with the proper parameters.

        ReadRequest takes the following parameters:
            1. string file_name
            2. string timestamp

        ReadReply takes the following parameters:
            1. bytes reply_file
            2. bool success
        """
        
        if DEBUG:
            print("Requesting NameNode.Read")

        file_path = request.file_path
        timestamp = request.timestamp
        nn = Namenode()
        data_nodes = nn.get(file_path, timestamp)
        if DEBUG: 
            print("Processing namenode.get() successful.")
            print("Response should be completed")
        return namenode_pb2.ReadReply(datanodes=data_nodes, success=True)
    
    def isAlive(self,request,context):
        """This responds with a message indicating the service is alive.
        """    
        
        #msg = "This service is alive"
        
        return data_pb2.AliveReply(health=True) 

def main():
    """Creates Master Node server and listens onto port according to
    commandline arg"""
    if len(sys.argv)  == 1:
        print("Please pass in a port number to run!")
        exit()
    #set port 
    port = sys.argv[1]

    print("\n\tStarting server on localhost:"+port)
    server = namenode_pb2.beta_create_NameNode_server(NameNode())
    ip = "[::]:"+str(port)
    print("Starting NameNode at %s" % ip)
    server.add_insecure_port(ip)
    server.start()
    try:
        while True:
            time.sleep(TIMEOUT)
    except KeyboardInterrupt:
        print("\n\tKilling the server...\n")
        server.stop(grace=0)
        exit()
    except:
        print("Error has occured, please refer to log")



if __name__ == '__main__':
    main()
