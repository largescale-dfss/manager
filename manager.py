from grpc.beta import implementations
import manager_django_pb2, namenode_pb2, datanode_pb2
import json, hashlib, sys, random, grpc, time, os

TIMEOUT = 10
_TIMEOUT = 10
_ONE_DAY_IN_SECONDS = 24 * 60 *60

class Manager(manager_django_pb2.BetaManagerServicer):

    def __init__(self, ip, port):
        self.namenode_ip = ip
        self.namenode_port = port

    def OpenFile(self, request, context):
        print "Inside OpenFile"

        path_to_file = request.open_path.encode('ascii','ignore')
        timestamp = str(request.timestamp)
        hash_path = hashlib.sha1(path_to_file).hexdigest()
        print path_to_file, timestamp, hash_path
        
        #RPC to Namenode and get datanodes
        read_res = self.readFromNamenode(path_to_file, timestamp)
        datanodes = json.loads(read_res.datanodes)
        #print json.loads(datanodes)[0]
        #RPC to Datanodes and combine data to get full file
        read_data = self.readFromDatanodes(hash_path, timestamp, datanodes)
        #read_data = "hello world"
        #print read_data
        return manager_django_pb2.OpenResponse(open_file=read_data)
    
    def readFromNamenode(self, path_to_file, timestamp):
        channel = implementations.insecure_channel(self.namenode_ip, self.namenode_port)
        stub = namenode_pb2.beta_create_NameNode_stub(channel)
        req = namenode_pb2.ReadRequest(file_path=path_to_file, timestamp=timestamp)
        response = stub.Read(req, 10)
        return response

    def readFromDatanodes(self, hash_path, timestamp, datanodes):
        print "inside", datanodes[0]
        datalist = []
        for index, dn in enumerate(datanodes):
            print "readFromDatanodes", dn
            dn_ip = dn[0].encode('ascii','ignore')
            dn_port = int(dn[1])
            print type(dn_ip), type(dn_port)
            offset = "{0:#0{1}x}".format(index,6)[2:]
            block_name = hash_path[:36] + offset
            dn_channel = implementations.insecure_channel(dn_ip, dn_port)
            dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
            dn_read_req = datanode_pb2.ReadRequest(blockname=block_name, timestamp=timestamp)
            response = dn_stub.Read(dn_read_req, 10)
            datalist.append(response.data)
        return ("").join(datalist)            


    def writeToNamenode(self, path_to_file, timestamp, file_data):
        print "Inside writeToNamenode", self.namenode_ip, self.namenode_port
        file_size = len(file_data)
        channel = implementations.insecure_channel('localhost', 5050)
        stub = namenode_pb2.beta_create_NameNode_stub(channel)
        req = namenode_pb2.StoreRequest(file_path = path_to_file, file_size = file_size, timestamp = timestamp)
        response = stub.Store(req, _TIMEOUT)
        #TODO check response.success
        return response

    def writetoDatanode(self, hash_path, timestamp, datanodes, split_data):
        for index, dn in enumerate(datanodes):
            print type(dn[0]), dn[0], type(dn[1]), dn[1]
            dn_ip = dn[0].encode('ascii','ignore')
            dn_port = dn[1]
            offset = "{0:#0{1}x}".format(index,6)[2:]
            block_name = hash_path[:36] + offset
            dn_channel = implementations.insecure_channel(dn_ip, dn_port)
            dn_stub = datanode_pb2.beta_create_DataNode_stub(dn_channel)
            dn_write_req = datanode_pb2.StoreRequest(blockname=block_name, timestamp=timestamp, data=split_data[index])
            response = dn_stub.Store(dn_write_req, 10)

    def SaveFile(self, request, context):
        print "Saving File..."
        finalMessage = "File has been saved to dfs"

        #SaveFile request has file, filepath, and timestamp
        file_data = request.save_file.encode('ascii','ignore')
        path_to_file = request.save_path.encode('ascii','ignore')
        timestamp = str(request.timestamp)

        #TEAM DFS SHOULD IMPLEMENT RPC CALL NAMENODE CALL HERE
        #Writes to Namenode

        #print type(file_data), type(path_to_file), type(timestamp)
        write_res = self.writeToNamenode(path_to_file, timestamp, file_data)
        
        hash_path = write_res.path
        datanodes = json.loads(write_res.datanodes)
        block_size = write_res.block_size
        
        #Splits the file by block size into a list
        split_data = [file_data[i:i+block_size] for i in range(0, len(file_data), block_size)]

        #Writes to Datanodes
        self.writetoDatanode(hash_path, timestamp, datanodes, split_data)
        #You can return whatever you like on write
        return manager_django_pb2.SaveResponse(transfer_status='%s' % finalMessage)

  

#Host Manager Server
def serve():
    #Reading off of the manager.proto, creating Manager class

    #pass the ip and port from command line then init on Manager
    server = manager_django_pb2.beta_create_Manager_server(Manager('localhost', 5050))
    server.add_insecure_port('[::]:50050')
    server.start()
    try:
      while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
  serve()
