#!/bin/bash

protoc -I . --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` namenode.proto
protoc -I . --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` datanode.proto
