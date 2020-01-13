#FROM python:2.7.13
FROM python:3

MAINTAINER Savva Genchevskiy

# Add the external tasks directory into /load_test
WORKDIR /locust-tasks

ADD requirements.txt requirements.txt
ADD run.sh run.sh

# Install the required dependencies via pip
RUN pip install -r requirements.txt

# Set script to be executable
RUN chmod 755 run.sh

# Expose the required Locust ports
EXPOSE 5557 5558 8089

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["./run.sh"]

#CMD /usr/local/bin/locust -f scenarios/random_scenarios.py $LOCUST_TEST --host=$TARGET_HOST -c $NUM_CLIENTS -r $HATCH_RATE --no-web


