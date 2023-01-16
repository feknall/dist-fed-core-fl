#!/bin/bash

echo "Stopping all entities..."
docker compose -f docker-compose-fl-fedavg.yml down
docker compose down

echo "Starting all entities..."
docker compose -f docker-compose-fl-fedavg.yml up -d

echo "Waiting 10 seconds..."
sleep 10
docker compose up flAdmin
./extract-report.sh
