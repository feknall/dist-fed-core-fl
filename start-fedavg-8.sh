#!/bin/bash

echo "Stopping all entities..."
docker compose -f docker-compose-fedavg.yml down
docker compose -f docker-compose-trainer-fedavg-8.yml down

echo "Starting all entities..."
docker compose -f docker-compose-fedavg.yml up leadAggregator -d
docker compose -f docker-compose-trainer-fedavg-8.yml up -d

echo "Waiting 10 seconds..."
sleep 10
docker compose -f docker-compose-fedavg.yml up flAdmin
./extract-report.sh
