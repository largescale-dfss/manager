##################################
# This file tests  data node rpc
###############################
import namenode_pb2
import json
from grpc.beta import implementations
import hashlib
import datanode_pb2
import sys
def main():
    if len(sys.argv) ==1:
        print("Please pass the proper parameters, include port number")
        exit()

    port = sys.argv[1]
    print("Testing datanode...")
    #port = 5000
    ip = "127.0.0.1"
    
    channel = implementations.insecure_channel(str(ip),int(port))
    stub = datanode_pb2.beta_create_DataNode_stub(channel)
    
    pfn = "./test.txt"
    file_size = 1337
    ts = "123121234"
    f = open(pfn, 'r')
    d = f.read()
    f.close()
    print(d)
    req =datanode_pb2.ReadRequest(blockname=pfn,timestamp=ts)
    response = stub.Read(req,10) 
    #req =namenode_pb2.StoreRequest(file_path=pfn,file_size=file_size,timestamp=ts)
    #response = stub.Store(req,10)

if __name__ == '__main__':
    try:
        main()
        print("Test is successful!")
    except Exception as err:
        print(err)
        print("Test failed")
