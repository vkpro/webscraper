FROM selenium/standalone-firefox:3.6.0-copper
MAINTAINER Vladimir Kharitoshkin <haritoshkin@mail.ru>

USER root

RUN apt-get update && apt-get install -y python3-pip git
RUN pip3 install --upgrade pip && \
    pip3 install virtualenv
RUN virtualenv /venv && \
    . /venv/bin/activate && \
	  pip3 install pip --upgrade && \
	  pip3 install pytest

RUN mkdir /webscraper
COPY ./* /webscraper
