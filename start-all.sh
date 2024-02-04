#!/bin/bash

echo "Stopping all entities..."
docker compose -f docker-compose-fl-fedshare.yml down
docker compose down

echo "Starting all entities..."
docker compose -f docker-compose-fl-fedshare.yml up -d
docker compose -f docker-compose-fedshare.yml up aggregatorOrg1 -d
docker compose -f docker-compose-fedshare.yml up aggregatorOrg2 -d

echo "Waiting 10 seconds..."
sleep 10
docker compose -f docker-compose-fedshare.yml up flAdmin
#./extract-report.sh
