##################################
# This file tests name node rpc
###############################
import namenode_pb2
import json
from grpc.beta import implementations
import hashlib
import datanode_pb2
import sys
def main():
    
    if len(sys.argv) == 1:
        print("Please pass port number")
        exit()
    
    port = sys.argv[1]
    print("Testing namenode on port "+port)
    ip = "127.0.0.1"
    
    channel = implementations.insecure_channel(str(ip),int(port))
    stub = namenode_pb2.beta_create_NameNode_stub(channel)
    
    pfn = "./test.txt"
    with open(pfn, 'r') as f:
        file_size = len(f.read())
    ts = "123121234"
    
    req =namenode_pb2.StoreRequest(file_path=pfn,file_size=file_size,timestamp=ts)
    response = stub.Store(req,10)
    """
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
    """
    """
    for dn in c:
        ip = dn[0]
        port = int(dn[1])
        
        dn_channel = implementations.insecure_channel(ip,port)
        dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
        pathy = hashlib.sha1(pfn).hexdigest()
        dn_req = datanode_pb2.StoreRequest(blockname=pathy,timestamp=ts, data=d)
        response = dn_stub.Store(dn_req,10)
    """
    """dn_channel = implementations.insecure_channel('localhost',5000)
    dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
    pathy = hashlib.sha1(pfn).hexdigest()
    dn_req=datanode_pb2.ReadRequest(blockname=pathy,timestamp=ts)
    response = stub.Read(dn_req,10)
    print(response.data)
   """ 

if __name__ == '__main__':
    try:
        main()
        print("Test is successful")
    except Exception as err:
        print(err)
        print("Test failed!")
