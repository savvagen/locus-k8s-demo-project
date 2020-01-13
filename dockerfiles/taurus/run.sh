#!/usr/bin/env bash

TAURUS="bzt"

TAURUS_CONFIG=${TAURUS_CONFIG:-/my_config.yaml}

TAURUS_OPTS="$TAURUS_CONFIG -l /tmp/artifacts/bzt.log $ADD_OPTIONS"

#OLD
#echo "$TAURUS $TAURUS_OPTS"
#$TAURUS $TAURUS_OPTS

if [[ -z ${ADD_COMMAND} ]] ; then
    echo "Running Taurus:"
    echo "$TAURUS $TAURUS_OPTS"
    $TAURUS $TAURUS_OPTS
    if [ "$?" -eq "0" ]
    then
        echo "Test Passed."
        exit 0
    else
        echo "Test Failed"
        exit 1
    fi
else
    echo "Running Taurus with additional command: "
    echo "$TAURUS $TAURUS_OPTS" && $ADD_COMMAND
    # sh -c "$TAURUS $TAURUS_OPTS" && sh -c "$ADD_COMMAND" || sh -c "$ADD_COMMAND"
    $TAURUS $TAURUS_OPTS # && $ADD_COMMAND || $ADD_COMMAND
    if [ "$?" -eq "0" ]
    then
        echo "Test Passed."
        sh -c "$ADD_COMMAND"
        exit 0
    else
        echo "Test Failed"
        sh -c "$ADD_COMMAND"
        exit 1
    fi
fi

# The same Code Snipped:
#
#echo "Running Taurus:"
#echo "$TAURUS $TAURUS_OPTS"
#$TAURUS $TAURUS_OPTS
#if [ "$?" -eq "0" ]; then
#    echo "Test Passed."
#    if [[ -z ${ADD_COMMAND} ]] ; then
#        sh -c "$ADD_COMMAND"
#    fi
#    exit 0
#else
#    echo "Test Failed"
#    if [[ -z ${ADD_COMMAND} ]] ; then
#        sh -c "$ADD_COMMAND"
#    fi
#    exit 1
#fi