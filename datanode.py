import os
class Datanode:
    root = "/var/dfs_dn"
    
    def __init__(self, datanode_id):
        self.root = self.root + datanode_id
        if not (os.path.isdir(self.root) and os.path.exists(self.root)):
            try:
                os.makedirs(self.root)
            except OSError as exception:
                print "Run the script as root"

    def get_dir(self, file_hash):
        folder = file_hash[:3]
        folder_path = os.path.join(self.root, folder)
        return folder_path

    def get_filename(self, file_hash, timestamp):
        filename = file_hash[3:] + "@" + str(timestamp)
        return filename

    def read(self, file_hash, timestamp):
        folder_path = self.get_dir(file_hash)
        filename = self.get_filename(file_hash, timestamp)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as f:
            return f.read()

    def write(self, file_hash, timestamp, data):
        folder_path = self.get_dir(file_hash)
        if not (os.path.isdir(folder_path) and os.path.exists(folder_path)):
            os.makedirs(folder_path)

        filename = self.get_filename(file_hash, timestamp)
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'w') as f:
            f.write(data)
