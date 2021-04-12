FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y x11-apps
CMD ["/usr/bin/xeyes"]