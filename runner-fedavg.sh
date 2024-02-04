#!/bin/bash

PYTHONPATH=${PYTHONPATH}/$(pwd)

for INDEX in {0..3}
do
  PORT=$((6001+${INDEX}))
  nohup python main.py "trainer" "localhost" ${PORT} ${INDEX} "1" &> logs/trainer"${INDEX}".txt &
done

nohup python main.py "leadAggregator" "localhost" 8082 "1" &> logs/leadAggregator.txt &

sleep 10
nohup python main.py "flAdmin" "localhost" 8083 "1" &> logs/flAdmin.txt &

