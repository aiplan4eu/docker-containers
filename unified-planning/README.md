# Docker images for AIPlan4EU unified planning code

# Install

* Install [docker](http://www.docker.com) (tested on v. 19.03, 20.10) 

    See also 
    [Post-installation steps for Linux](https://docs.docker.com/install/linux/linux-postinstall/).
    In particular, add your user to the `docker` group and log out and in again, before proceeding.


* Install [docker-compose](https://docs.docker.com/compose/install/) (tested on v. 1.28.2)


## Build the UP docker image

    ./build.bash

## Create a playground folder 

This folder will be mounted in the container to store persistntt files. 

    mkdir -p $HOME/playground

## Start the UP docker container

    ./start.bash

    

## Test

* Using Colab

    Open a notebook in a browser

        [UP Basics notebook](https://colab.research.google.com/github/aiplan4eu/unified-planning/blob/master/notebooks/Unified_Planning_Basics.ipynb)

    Connect to local runtime using the jupiter notebook link printed when starting the container
    (or print it again with `docker logs unifiedplanning`)


* Using CLI

    Access the container

        docker exec -it unifiedplanning tmux

    Run code in the container

        cd ~/test
        python3 basic.py
        python3 icaps_demo.py


## Develop your code in playground folder and run it in the container

Use your fovorite editor to write code, save files in the playground folder
and run them from the container.


## Detach tmux terminal without closing the session

From tmux inside the container, use keyboard keys

    CTRL-b d

## Stop the docker container

    ./stop.bash


