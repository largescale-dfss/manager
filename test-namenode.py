##################################
# This file tests name node rpc
###############################
import namenode_pb2
from grpc.beta import implementations

def main():
    print("Testing namenode...")
    port = 50056
    ip = "127.0.0.1"
    
    channel = implementations.insecure_channel(str(ip),int(port))
    stub = namenode_pb2.beta_create_NameNode_stub(channel)
    
    pfn = "./test.txt"
    file_size = 1337
    ts = "123121234"
    req =namenode_pb2.StoreRequest(file_path=pfn,file_size=file_size,timestamp=ts)
    response = stub.Store(req,10)

if __name__ == '__main__':
    main()
