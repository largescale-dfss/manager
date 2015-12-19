#####
#RPC Datanode
####
import sys 
import time
import datanode_pb2
from datanode import Datanode
from grpc.beta import implementations

#global variables
DEBUG = True

class DataNode(datanode_pb2.BetaDataNodeServicer):
    def Store(self,request,context):
        if DEBUG:
            print("Requesting DataNode.Store")

        dn = Datanode()
        dn.write(request.blockname,request.timestamp,request.data)
        if DEBUG:
            print("\tDataNode.Store completed successfully!") 
        return datanode_pb2.StoreReply(success=True)

    def Read(self,request,context):
        if DEBUG:
            print("Requesting Datanode.Read")
        dn = Datanode()
        data = dn.read(request.blockname,request.timestamp)
        if DEBUG:
            print("\t Datanode.Read completed successfully! ")
        return datanode_pb2.ReadReply(data=data,success=True)


def main():
    print("Running datanode...")
    if(len(sys.argv) == 1):
        print("Please enter the proper parameters!")
        print("python rdatanode.py <port>")
        exit()
     
    server = datanode_pb2.beta_create_DataNode_server(DataNode())
    #ip = "[::]:5000"
    port = sys.argv[1]
    ip = "[::]:"+port
    print("Running server... %s" % ip)
    server.add_insecure_port(ip)
    server.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("oH NO DON'T KILL ME")
        server.stop(grace=0)
        exit()
    except:
        print("Error occured in datanode server")


if __name__ == '__main__':
    main()
