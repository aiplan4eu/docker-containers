FROM ubuntu:20.04
MAINTAINER alvalentini@fbk.eu

# Default user and group ID
ARG UID=1000
ARG GID=1000
ARG BUILDDATETIME=0

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y gcc make cmake g++ tmux python3-dev python3-pip openjdk-17-jdk git unzip wget curl gringo

RUN pip install matplotlib networkx 

RUN pip3 install jupyter notebook jupyter_http_over_ws

# Create user: planner (password: planner) with given UID/GID and sudo power

RUN useradd -ms /bin/bash planner && echo "planner:planner" | chpasswd && adduser planner sudo

RUN usermod -u $UID planner && groupmod -g $GID planner

RUN echo "$BUILDATETIME" > /builddatetime

USER planner

RUN pip install --pre --force-reinstall unified-planning
RUN pip install unified-planning[pyperplan,tamer,enhsp,fast-downward,fmap]

# Configuration

RUN echo "set -g mouse on" > $HOME/.tmux.conf 
RUN touch ~/.sudo_as_admin_successful
RUN jupyter serverextension enable --py jupyter_http_over_ws

COPY init.bash /home/planner/init.bash

# Get other code

RUN mkdir /home/planner/aiplan4eu

RUN cd /home/planner/aiplan4eu && \
    git clone https://github.com/aiplan4eu/planning-test-cases.git


VOLUME /home/planner/playground

WORKDIR /home/planner/playground

CMD [ "jupyter", "notebook", \
        "--NotebookApp.allow_origin='https://colab.research.google.com'", \
        "--port=8888", "--NotebookApp.port_retries=0" ]

#ENTRYPOINT [ "/bin/bash", "/home/planner/init.bash" ]

#CMD /bin/bash


