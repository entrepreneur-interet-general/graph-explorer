FROM openjdk:8-jdk

RUN apt-get update && \
    apt-get install -y wget unzip htop && \
    mkdir /workspace && \
    cd /workspace && \
    wget https://artifacts.elastic.co/downloads/logstash/logstash-6.0.1.zip && \
    unzip logstash-6.0.1.zip && \
    rm logstash-6.0.1.zip && \
    ls && \
    mv logstash-* logstash

WORKDIR /workspace/logstash

COPY ./logstash.conf /workspace/logstash 
COPY ./data/transactions.csv /workspace/logstash/data 

CMD ["bin/logstash", "-f", "logstash.conf"]
