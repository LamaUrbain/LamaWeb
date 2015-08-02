FROM ubuntu:trusty
MAINTAINER lamaurba.in
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y update && apt-get -qq -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y update && apt-get -qq -y install libpython-dev libffi-dev libssl-dev libmysqlclient-dev python-virtualenv git
RUN groupadd lamaweb && useradd -m lamaweb -g lamaweb
EXPOSE 9999
WORKDIR /home/lamaweb
CMD ./manage.py runserver 0.0.0.0:9999
ADD . /home/lamaweb
RUN chown -R lamaweb:lamaweb /home/lamaweb
RUN /bin/bash -c "cd /home/lamaweb && pip install -r requirements.txt"
