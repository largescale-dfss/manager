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
