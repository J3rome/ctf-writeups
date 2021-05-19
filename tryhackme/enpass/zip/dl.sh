#!/bin/bash

for i in $(seq 0 100); do 
    wget "http://10.10.236.111:8001/zip/a$i.zip" 
done

