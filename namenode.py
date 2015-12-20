import os, json, hashlib
from math import pow, ceil
from collections import OrderedDict
class Namenode:
    root = "/var/dfs_nm"
    blocksize = 15 * int(pow(2, 10)) #15 KB
    datanodes ={('localhost',5000):5, ('localhost',6000):0, ('localhost',7000):1, ('localhost',8000):3}

    #Initializes the namenode and creates nm directory if not exist
    def __init__(self):
        if not (os.path.isdir(self.root) and os.path.exists(self.root)):
            try:
                os.makedirs(self.root)
            except OSError as exception:
                print "Run the script as root"

    #choose the datanodes with least number of blocks
    def getNewDN(self, numBlocks):
        dnodes = []
        od = OrderedDict(sorted(self.datanodes.items()), key=lambda t: t[1])
        keys = od.keys()
        if (numBlocks > len(self.datanodes)):
            dnodes = keys + keys[:numBlocks-len(keys)]
        else:
            dnodes = keys[:numBlocks]
        self.updateDN(dnodes)
        return dnodes

    #updates the datanodes with numbers of blocks
    def updateDN(self, dnodes):
        for node in dnodes:
            self.datanodes[node] += 1

    #filename => array of blocks
    def get(self, file_path, timestamp):
        pathHash = hashlib.sha1(file_path).hexdigest()
        filename = pathHash + "@" + str(timestamp)
        dirPath = os.path.join(self.root, os.path.dirname(file_path))
        if not (os.path.isdir(dirPath) and os.path.exists(dirPath)):
            raise Exception('{} doesnt exist'.format(dirPath))
        absPath = os.path.join(dirPath, filename)
        arr = None
        with open(absPath, 'r') as f:
            list_datanodes = f.read()
            print json.loads(list_datanodes)
            return list_datanodes
    
    #filename, filesize => 
    def save(self, file_path, file_size, timestamp):
        numBlocks = int(ceil(float(file_size)/self.blocksize))
        pathHash = hashlib.sha1(file_path).hexdigest()
        filename = pathHash + "@" + str(timestamp)
        dirPath = os.path.join(self.root, os.path.dirname(file_path))
        if not (os.path.isdir(dirPath) and os.path.exists(dirPath)):
            os.makedirs(dirPath)
        absPath = os.path.join(dirPath, filename)
        with open(absPath, 'w') as f:
            list_ports = json.dumps(self.getNewDN(numBlocks))
            f.write(list_ports)
            return list_ports

