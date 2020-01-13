## Run json-server load test in Docker

### Run Locust tests
Run locust framework /scenarios/load_test.py file using command:

``` 
Execute command from project root dir:

docker run -it --rm -p=8089:8089 \
    -v $PWD:/locust-tasks \
    -v $PWD/reports:/locust-tasks/reports \
    -e "TARGET_HOST=http://localhost:3000" \
    -e "ADD_OPTIONS=-c 10 -r 5 --no-web -t10s --loglevel=INFO --print-stats --csv=reports/locust-report" \
    -e "LOCUSTFILE_PATH=locust_scenarios/load_tests.py" \
    -e "LOCUST_TEST=JsonServerScenario" \
    -e "MAX_LATENCY=11000" \
    -e "LOCUST_MODE=standalone" \
    -e "ADD_COMMAND=echo sleeping for 10 sec. && sleep 10 " \
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
     -e "ADD_COMMAND=echo sleeping for 10 sec. && sleep 10 " \
     --name "taurus" savvagench/taurus:latest
     
```

## Run json-server load tests with docker-compose

Run locust tests using command:

``` 
    docker-compose -f deploy/docker/locust/docker-compose.yml up
```

Run Taurus tests using command:

```     
    docker-compose -f deploy/docker/taurus/docker-compose.yml up
```