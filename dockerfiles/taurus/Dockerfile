FROM blazemeter/taurus:latest

MAINTAINER Savva Genchevskiy

# Installing virtual environment
RUN apt-get update
RUN apt-get -y install python3-venv

RUN mkdir /bzt-configs/load_test

ADD ./requirements.txt /bzt-configs/requirements.txt
ADD ./run.sh /bzt-configs/run.sh

RUN pip3 install virtualenv \
    && python3 -m venv /bzt-configs/venv \
    && echo $(pwd) \
    # && echo "locustio\nbzt" >> $(pwd)/load_test/requirements.txt \
    && pip3 install -r /bzt-configs/requirements.txt

# Set script to be executable
RUN chmod 755 run.sh


ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

WORKDIR /bzt-configs

ENTRYPOINT ["./run.sh"]
# ENTRYPOINT ["sh", "-c", "bzt -l /tmp/artifacts/bzt.log \"$@\"", "ignored"]
