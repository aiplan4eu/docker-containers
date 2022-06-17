# Docker images for AIPlan4EU unified planning code

Install `docker` and `docker-coompose`

## Build image from `Dockerfile`

        ./build.bash

## Create a playground folder 

    This folder will be mounted in the container to store persistntt files. 

        mkdir -p $HOME/playground

## Start the docker container

        ./start.bash

## Attach tmux terminal inside the container

        ./run.bash

## Test

    From the container

        cd ~/test
        python3 icaps_demo.py


## Develop your code in playground folder and run it in the container

    Use your fovorite editor to write code, save files in the playground folder
    and run them from the container.


## Detach tmux terminal without closing the session

    From tmux inside the container, use keyboard keys

        CTRL-b d

## Stop the docker container

        ./stop.bash


