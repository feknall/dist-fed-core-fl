#!/bin/bash

PYTHONPATH=${PYTHONPATH}/$(pwd)

for INDEX in {0..1}
do
  PORT=$((6001+${INDEX}))
  nohup python main.py "trainer" "localhost" ${PORT} ${INDEX} &> logs/trainer"${INDEX}".txt &
done

nohup python main.py "aggregator" "localhost" 8091 &> logs/aggregator1.txt &
nohup python main.py "aggregator" "localhost" 8092 &> logs/aggregator2.txt &
nohup python main.py "leadAggregator" "localhost" 8082 &> logs/leadAggregator.txt &

sleep 10
nohup python main.py "flAdmin" "localhost" 8083 &> logs/flAdmin.txt &

