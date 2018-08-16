#!/bin/env bash

BIN=./bin

$BIN/wait-for-it.sh -s -t 60 elasticsearch:9200 

if [ $? -eq 0 ]; then
    curl -X DELETE "elasticsearch:9200/transactions*"
    $BIN/logstash -f logstash.conf
fi
    echo " timeout exceeded: could not connect to elasticsearch:9200" >&2
    return 1