##################################
# This file tests name node rpc
###############################
import namenode_pb2
import json
from grpc.beta import implementations
import hashlib
import datanode_pb2
def main():
    print("Testing namenode...")
    port = 5000
    ip = "127.0.0.1"
    
    channel = implementations.insecure_channel(str(ip),int(port))
    stub = namenode_pb2.beta_create_NameNode_stub(channel)
    
    #parameters required for request
    pfn = "./test.txt"
    file_size = 1337
    ts = "123121234"
    
    f = open(pfn, 'r')
    d = f.read()
    f.close()
    
    #req =namenode_pb2.StoreRequest(file_path=pfn,file_size=file_size,timestamp=ts)
    #response = stub.Store(req,10)
    req = namenode_pb2.ReadRequest(file_path=pfn,timestamp=ts)
    response = stub.Read(req,10)
    datanodes = json.loads(response.datanodes)
    c = (datanodes)
    dn_channel = implementations.insecure_channel('localhost',5000)
    dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
    pathy = hashlib.sha1(pfn).hexdigest()
    dn_req = datanode_pb2.ReadRequest(blockname=pathy,timestamp=ts)
    response = dn_stub.Read(dn_req,10)
    print(response.data)
    

if __name__ == '__main__':

    try:
        main()
        print("Test is successful")
    except Exception as err:
        print("Test has failed!")
        print(err)

