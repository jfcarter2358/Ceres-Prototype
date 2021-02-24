FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get install -y apt-transport-https gnupg2 curl git
# install python3.8
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install python3.8 -y
RUN apt-get install python3-pip -y

# make directories
RUN mkdir -p /ceres/ceres_home/config

# add contents
ADD src /ceres
ADD requirements.txt /ceres/requirements.txt
ADD ceres_home/config/config.ini /ceres/ceres_home/config/config.ini
ADD ceres_home/config/schema.json /ceres/ceres_home/config/schema.json

# install dependencies
WORKDIR /ceres
RUN pip3 install -r requirements.txt

# run the database
ENTRYPOINT [ "python3", "ceres.py", "run" ]