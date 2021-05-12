FROM ubuntu:20.04
MAINTAINER alvalentini@fbk.eu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y gcc make cmake g++ python3-dev python3-pip openjdk-11-jdk git
RUN pip3 install grpcio grpcio-tools pytest pysmt

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

CMD /bin/bash
