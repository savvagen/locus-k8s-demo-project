#!/usr/bin/env bash

LOCUST="/usr/local/bin/locust"

LOCUSTFILE_PATH=${LOCUSTFILE_PATH:-/locustfile.py}

LOCUST_OPTS="-f $LOCUSTFILE_PATH $LOCUST_TEST --host=$TARGET_HOST $ADD_OPTIONS"

LOCUST_MODE=${LOCUST_MODE:-standalone}

if [ "$LOCUST_MODE" = "master" ]; then

    if [ -z ${EXPECT_SLAVES} ] ; then
        echo "No expected slaves. Set EXPECT_SLAVES number to set custom slave number waiting condition."
        LOCUST_OPTS="$LOCUST_OPTS --master"
    else
        LOCUST_OPTS="$LOCUST_OPTS --master --expect-slaves $EXPECT_SLAVES"
    fi
    # LOCUST_OPTS="$LOCUST_OPTS --master"

elif [ "$LOCUST_MODE" = "worker" ]; then
    LOCUST_OPTS="$LOCUST_OPTS --slave --master-host=$LOCUST_MASTER"
fi


#OLD
# echo "$LOCUST $LOCUST_OPTS"
# $LOCUST $LOCUST_OPTS

if [[ -z ${ADD_COMMAND} ]] ; then
    echo "Running Locust:"
    echo "$LOCUST $LOCUST_OPTS"
    $LOCUST $LOCUST_OPTS
    if [ "$?" -eq "0" ]
    then
        echo "Test Passed."
        exit 0
    else
        echo "Test Failed."
        exit 1
    fi
else
    echo "Running locust with additional command: "
    echo "$LOCUST $LOCUST_OPTS" #&& $ADD_COMMAND
    # sh -c "$LOCUST $LOCUST_OPTS" && sh -c "$ADD_COMMAND" || sh -c "$ADD_COMMAND"
    # $LOCUST $LOCUST_OPTS && $ADD_COMMAND || $ADD_COMMAND
    $LOCUST $LOCUST_OPTS
    if [ "$?" -eq "0" ]
    then
        echo "Test Passed."
        sh -c "$ADD_COMMAND"
        exit 0
    else
        echo "Test Failed."
        sh -c "$ADD_COMMAND"
        exit 1
    fi
fi

