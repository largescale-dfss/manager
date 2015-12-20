# Django - gRPC Manager

This code is based off of the code from Assignment 3 in class.  

###Protofile Description
`manager_django.proto` is in charge of communication between django and
manager server.  Run `./run_codegen.sh` to compile all the protocol
buffers required for this project.

###Running Server
manager-server.py is the manager server.

Running `startManager.sh` will compile the relevant protobuf files and will start the manager server.
`bash startManager.sh` command on Mac.

`python test-client.py` to test that the RPC connections are working.
Note, separate tests have now been created to test Read and write
requests on the servers. Run `python test-nn_read.py` to test the read
request on the name node, and run `python test-nn_write.py` to test the
write request on the name node. 

The datanodes and namenode servers must be passed a port number, for the
desired port you wish to run the service on. So please invoke the
following for either rdatanode.py or rnamenode.py `python rdatanode.py
port_number`

###Running DFS
Start Namenode: `sudo ./run_namenode.sh`
Set the port to 5050 or match the port in the manager.py

Start a new Datanode: `sudo ./run_datanode.sh`
Available Ports: [5000, 6000, 7000, 8000]


###Project description
The project is split into several different files. The first group of
files are bash scripts that allow you to run the RPC servers. These
include: `run_datanode.sh` , `run_namenode.sh` , and `startManager.sh`

The project also contains our class definition for our file system
calls. `datanode.py` contains a class definition for simple I/O
operations on which the datanodes should perform, such as read and
write. `namenode.py` also contains a class definition for the operations
which should be supported by the namenode.

The second set of files in this project is the proto files, which
contain the protocol buffers for our various RPCs. We have three
protocol buffers: `manager.proto` , `datanode.proto` , and finally
`namenode.proto`

The next set of files are the actual RPCs. These include `manager.py` ,
`rnamenode.py` and finally `rdatanode.py` . These files could be
executed by running the bash scripts talked about in the first portion.

Finally we created test files that test various aspects of our project.
Each test file contains a prefix of the string `test` to denote the test
file, followed by a description of what the file is trying to test.



