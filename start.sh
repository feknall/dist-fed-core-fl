#!/bin/bash

nohup docker compose up trainer01 &> logs/trainer01.log &
nohup docker compose up trainer02 &> logs/trainer02.log &
nohup docker compose up aggregatorOrg1 &> logs/aggregatorOrg1.log &
nohup docker compose up aggregatorOrg2 &> logs/aggregatorOrg2.log &
nohup docker compose up leadAggregator &> logs/leadAggregator.log &

echo "Waiting 5 seconds..."
sleep 5
nohup docker compose up flAdmin &> logs/flAdmin.log &