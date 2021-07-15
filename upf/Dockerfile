FROM ubuntu:20.04
MAINTAINER alvalentini@fbk.eu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y gcc make cmake g++ libboost-all-dev python3-dev python3-pip openjdk-16-jdk git unzip wget
RUN pip3 install grpcio grpcio-tools pysmt

CMD /bin/bash
