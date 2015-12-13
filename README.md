# Django - gRPC Manager

This code is based off of the code from Assignment 3 in class.  

###Preparing Code
First compile the protobufs into .py files by running `protoprep.sh`  
`bash protoprep.sh` command on Mac.

###Protofile Description
`manager_django.proto` is in charge of communication between django and manager server.  



###Running Server
manager-server.py is the manager server.
`python manager-server.py` to start the server.  

`python test-client.py` to test that the RPC connections are working.