#!/bin/env bash

bin/gremlin.sh -e scripts/create_schema.groovy
bin/gremlin-server.sh

