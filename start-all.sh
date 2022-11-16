#!/bin/bash

echo "Starting all entities..."
docker compose -f docker-compose-fl-trainer.yml up -d
docker compose up aggregatorOrg1 -d
docker compose up aggregatorOrg2 -d
docker compose up leadAggregator -d

echo "Waiting 10 seconds..."
sleep 10
docker compose up flAdmin -d