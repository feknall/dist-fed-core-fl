#!/bin/bash

DEST="report/exp2-clients-4"
mkdir $DEST
touch $DEST/result.txt
docker compose logs trainer1 2>&1 | grep trainer_time_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt
docker compose logs aggregatorOrg1 2>&1 | grep aggregator_time_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt
docker compose logs aggregatorOrg2 2>&1 | grep aggregator_time_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt
docker compose logs leadAggregator 2>&1 | grep lead_aggregator_time_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt
docker compose logs flAdmin 2>&1 | grep time_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt
docker compose logs flAdmin 2>&1 | grep accuracy_list | cut -f 2 -d '|' | sed "s,\x1B\[[0-9;|\\?]*[a-zA-Z],,g" | xargs >> $DEST/result.txt