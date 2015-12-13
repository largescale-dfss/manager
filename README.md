# Django - gRPC Manager

This code is based off of the code from Assignment 3 in class.  

###Protofile Description
`manager_django.proto` is in charge of communication between django and manager server.  

###Running Server
manager-server.py is the manager server.

Running `startManager.sh` will compile the relevant protobuf files and will start the manager server.
`bash startManager.sh` command on Mac.

`python test-client.py` to test that the RPC connections are working.