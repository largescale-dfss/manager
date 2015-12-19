##################################
# This file tests name node rpc
###############################
import namenode_pb2, datanode_pb2
import json, hashlib, sys
from grpc.beta import implementations

def main():
    if len(sys.argv) == 1:
        print("Please pass port number as parameter")
        exit()

    #Setup rpc channel
    ip = "127.0.0.1"  
    port = sys.argv[1]
    print("Testing namenode read request on port %s" % port)
    
    channel = implementations.insecure_channel(str(ip), int(port))
    stub = namenode_pb2.beta_create_NameNode_stub(channel)
   
    path_to_file = "./test.txt"
    hash_path = hashlib.sha1(path_to_file).hexdigest()
    ts = "123121234"
    with open(path_to_file, 'r') as f:
        file_data = f.read()
        file_size = len(file_data)
    
    #req =namenode_pb2.StoreRequest(file_path=pfn,file_size=file_size,timestamp=ts)
    #response = stub.Store(req,10)
    req = namenode_pb2.ReadRequest(file_path=path_to_file, timestamp=ts)
    response = stub.Read(req, 10)
    datanodes = json.loads(response.datanodes)
    block_size = 15010
    c = datanodes
    split_data = [file_data[i:i+block_size] for i in range(0, len(file_data), block_size)]
    for index, dn in enumerate(datanodes):
        dn_ip = dn[0]
        dn_port = dn[1]
        offset = "{0:#0{1}x}".format(index,6)[2:]
        block_name = hash_path[:36] + offset
        print dn_ip, dn_port, block_name, ts
        dn_channel = implementations.insecure_channel(dn_ip, dn_port)
        dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
        dn_write_req = datanode_pb2.StoreRequest(blockname=block_name, timestamp=ts, data=split_data[index])
        response = dn_stub.Store(dn_write_req, 10)
    dn_channel2 = implementations.insecure_channel(dn_ip, dn_port)
    dn_stub2 = datanode_pb2.beta_create_DataNode_stub(dn_channel2)
    dn_read_req = datanode_pb2.ReadRequest(blockname=block_name, timestamp=ts)
    response = dn_stub2.Read(dn_read_req, 10)
    print response.data
    
    #pathy = hashlib.sha1(pfn).hexdigest()
    #dn_req = datanode_pb2.ReadRequest(blockname=pathy,timestamp=ts)
    #response = dn_stub.Read(dn_req,10)
    #print(response.data)
    
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
    print("Test successful") 

if __name__ == '__main__':
    try:
        main()
        print("Test is successful")
    except Exception as err:
        print(err)
        print("Test failed")
