FROM python:3.8

ENV DEBIAN_FRONTEND noninteractive

# Install prerequirement libs
RUN apt-get update \
    && cat /etc/os-release \
    && apt-get install -y apt-transport-https curl wget ca-certificates gnupg-agent software-properties-common \
    && apt-get install -y apt-utils net-tools \
    && apt-get install -y sudo \
    && apt-get install -y --reinstall systemd

# Install Docker
RUN apt-get update \
    && apt-get remove docker docker-engine docker.io \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && apt-key fingerprint 0EBFCD88 \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" \
    && apt-get update \
    && apt-cache madison docker-ce \
    # && apt-get install -y docker-ce docker-ce-cli containerd.io
    && apt-get install -y docker-ce=17.03.3~ce-0~ubuntu-xenial

# Install kubectl
RUN apt-get update \
    && curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.10.5/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl

WORKDIR /locust_workspace

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --requirement requirements.txt

ENTRYPOINT ["/usr/bin/env", "bash", "-c"]
