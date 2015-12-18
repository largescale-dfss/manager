protoc -I . --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` manager_django.proto
echo "Protobuf complied with protoc, starting server..."

python manager.py
