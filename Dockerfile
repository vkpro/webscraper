FROM jenkins/jenkins:lts
MAINTAINER Vladimir Kharitoshkin <haritoshkin@mail.ru>
# if we want to install via apt
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-virtualenv
RUN pip install pytest
# drop back to the regular jenkins user - good practice
USER jenkins