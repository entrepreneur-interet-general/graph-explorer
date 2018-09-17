# Graph Explorer
Explore and find suspicious patterns in a graph of money transactions 
![screenshot](https://github.com/entrepreneur-interet-general/graph-explorer/raw/master/docs/img/home.png)

## Demo 
[https://graph-explorer.fr](https://graph-explorer.fr)

## Prerequisites 

* Docker 
* docker-compose 

## Installation 
 

```
# Clone the repository
> git clone  git@github.com:entrepreneur-interet-general/graph-explorer.git
> cd graph-explorer

# Download and build Docker images
> docker-compose build 

# Start Elasticsearch
> docker-compose up -d elasticsearch 

# Wait for Elasticsearch to be available on port 9200 
> curl localhost:9200/_cat/health 
docker-cluster yellow 1 1 6 6 0 0 6 0 - 50.0%

# Start ScyllaDB
> docker-compose up d scylladb

# Wait for ScyllaDB to be available
> docker-compose exec scylladb nodetool status
--  Address     Load       Tokens       Owns    Host ID                               Rack
UN  172.22.0.3  1.07 MB    256          ?       c961595a-ee52-4f94-baf3-74cdc5058af6  rack1

# Start JanusGraph 
> docker-compose up -d janus 

# Wait for JanusGraph to be available on port 8182
> curl -XPOST -d '{"gremlin" : "1+1" }' localhost:8182 
{"result":{"data":[2],"meta":{}}}

# Create schema and load data into JanusGraph 
# WARNING: do it once the first time or after 
# deleting the data directory  
> docker-compose exec janus bin/gremlin.sh -e scripts/create_schema.groovy
> docker-compose exec janus bin/gremlin.sh -e scripts/load_data.groovy 

# Checks that nodes and edges have been loaded
> curl -XPOST -d '{"gremlin" : "g.V().count()" }' localhost:8182 
{"result":{"data":[1606],"meta":{}}}

> curl -XPOST -d '{"gremlin" : "g.E().count()" }' localhost:8182
{"result":{"data":[2156],"meta":{}}}

# Load raw transactions into Elasticsearch 
> docker-compose up -d logstash 

# Check that transactions has been loaded in the transactions index
> curl localhost:9200/transactions/doc/_count 
{"count":2156,"_shards":{"total":5,"successful":5,"skipped":0,"failed":0}}

# Start the app in the foreground 
docker-compose up app 
```

Visit [http://localhost:5000](http://127.0.0.1:50000)

