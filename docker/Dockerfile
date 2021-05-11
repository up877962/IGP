FROM python:3.6

WORKDIR /usr/src/app

COPY . ./

RUN apt update ;\
apt-get update ;\
apt install -y python3-opencv

RUN cd yolov3-tf2 ;\ 
pip install -r requirements.txt ;\
chmod +x run-full run-tiny