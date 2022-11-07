#!/bin/bash

docker build -t dist-fed-core-fl . -f Dockerfile
docker tag dist-fed-core-fl hmaid/hyperledger:dist-fed-core-fl
docker push hmaid/hyperledger:dist-fed-core-fl