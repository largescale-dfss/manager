# manager

Based off of the code from Assignment 3 in class  

To compile protobuf:
`protoc -I . --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` manager_django.proto`  

`manager_django.proto` is in charge of communication between django and manager server.  

manager-server.py is the manager server.