#!/bin/bash
read -p "Please enter port number for datanode: " port
./venv/bin/python ./rdatanode.py $port


