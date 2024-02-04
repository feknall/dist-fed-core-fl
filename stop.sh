#!/bin/bash

docker compose -f docker-compose-fedshare.yml down
docker compose -f docker-compose-fl-fedshare.yml down

docker compose -f docker-compose-fedavg.yml down
docker compose -f docker-compose-trainer-fedavg-4.yml down
docker compose -f docker-compose-trainer-fedavg-8.yml down
docker compose -f docker-compose-trainer-fedavg-16.yml down
