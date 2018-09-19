FROM openjdk:8-jdk

ARG version=0.2.0
ARG hadoop=hadoop2

RUN apt-get update && \
    apt-get install -y wget unzip htop && \
    mkdir /workspace && \
    cd /workspace && \
    wget https://github.com/JanusGraph/janusgraph/releases/download/v$version/janusgraph-$version-$hadoop.zip && \
    unzip janusgraph-$version-$hadoop.zip && \
    rm janusgraph-$version-$hadoop.zip && \
    ls && \
    mv janusgraph-* janusgraph

WORKDIR /workspace/janusgraph
RUN bin/gremlin-server.sh -i org.apache.tinkerpop gremlin-python 3.2.6

COPY ./gremlin-server.yaml ./conf/gremlin-server/gremlin-server.yaml
COPY ./janusgraph.properties ./janusgraph.properties
COPY ./janusgraph.groovy ./scripts/janusgraph.groovy
COPY ./create_schema.groovy ./scripts/create_schema.groovy
COPY ./load_data.groovy ./scripts/load_data.groovy
COPY ./clean.groovy ./scripts/clean.groovy

COPY ./data data

CMD [ "bin/gremlin-server.sh" ]