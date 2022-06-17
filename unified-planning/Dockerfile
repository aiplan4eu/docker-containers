FROM ubuntu:20.04
MAINTAINER alvalentini@fbk.eu

# Default user and group ID
ARG UID=1000
ARG GID=1000

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y gcc make cmake g++ tmux python3-dev python3-pip openjdk-17-jdk git unzip wget curl gringo

RUN pip install unified-planning[pyperplan,tamer,enhsp,fast-downward]

RUN pip install matplotlib networkx 

# Create user: planner (password: planner) with given UID/GID and sudo power

RUN useradd -ms /bin/bash planner && echo "planner:planner" | chpasswd && adduser planner sudo

RUN usermod -u $UID planner && groupmod -g $GID planner

USER planner

COPY init.bash /home/planner/init.bash

RUN mkdir /home/planner/aiplan4eu

RUN cd /home/planner/aiplan4eu && \
    git clone https://github.com/aiplan4eu/planning-test-cases.git


VOLUME /home/planner/playground

WORKDIR /home/planner/playground

ENTRYPOINT [ "/bin/bash", "/home/planner/init.bash" ]

#CMD /bin/bash


