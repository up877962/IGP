#!/bin/bash
docker run --rm -it --device /dev/video0 --net=host --env="DISPLAY" --env QT_X11_NO_MITSHM=1 --volume="$XAUTHORITY:/root/.Xauthority:rw" azzisami/igp-python:latest /bin/bash
