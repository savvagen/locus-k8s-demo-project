# Locust and Taurus example project
## Description:
#### This project shows the examples how to build scenarios using Locust and Taurus and how to run this load generator tools on Kubernetes
#
##  Building images

### Locust

Build Locust Docker image with command:

```
cd dockerfiles/locust_docker

docker build -t savvagench/locust:latest -f Dockerfile .

```

### Taurus


Build the Docker image wrapper under the blazemeter/taurus image with command:


```
cd dockerfiles/taurus_docker

docker build -t savvagench/taurus:latest -f Dockerfile .

```


## Run json-server load test in Docker

### Run Locust tests
Run locust framework /locust_scenarios/load_test.py file using command:

``` 
Execute command from project root dir:

docker run -it --rm -p=8089:8089 \
    -v $PWD:/locust-tasks \
    -v $PWD/reports:/locust-tasks/reports \
    -e "TARGET_HOST=http://localhost:3000" \
    -e "ADD_OPTIONS=-c 10 -r 5 --no-web -t30s --loglevel=INFO --print-stats --csv=reports/locust-report" \
    -e "LOCUSTFILE_PATH=locust_scenarios/load_test.py" \
    -e "LOCUST_TEST=JsonServerScenario" \
    -e "MAX_LATENCY=11000" \
    -e "LOCUST_MODE=standalone" \
    --name "locust" savvagench/locust:latest
```
### Run Taurus tests
Run Taurus scenarios in Docker with command:

```
Execute command from project root dir:

docker run --rm \
     -v $PWD:/bzt-configs \
     -v $PWD/bzt_artifacts:/tmp/artifacts \
     -e "MAX_LATENCY=11000" \
     -e "TAURUS_CONFIG=taurus_configs/load_test.yml" \
     -e "ADD_OPTIONS=-report" \
     --name "taurus" savvagench/taurus:latest
```


