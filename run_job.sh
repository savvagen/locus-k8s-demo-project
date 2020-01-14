#!/usr/bin/env bash

kubectl apply -f deploy/kubernetes/taurus/locust_taurus_job.yml


pods=$(kubectl get pods --namespace=locust --selector=job-name=locust-taurus-job --output=jsonpath='{.items[*].metadata.name}')

echo Running pod: ${pods}

# kubectl logs -f -p $pods --namespace locust

while sleep 1; do
    status=$(kubectl get pods -n locust $pods -o=custom-columns=STATUS:.status.phase)
    echo $status
    if [[ $status == *"Running"* ]]; then
        echo "Container is running!!!"
        break
        #exit 0
    fi
done

kubectl logs -fn0 $pods -n locust | while read line ; do
    echo "$line"
#    echo "$line" | grep "start sleeping for 10 sec."
#    if [ $? = 0 ]
#        then
#            kubectl cp ${pods}:/bzt-configs ./reports --namespace=locust
#            echo "Copied reports!!"
#            break
#    fi
    if echo "$line" | grep -q "WARNING: Done performing with code: 3"; then
        echo "Test Failed."
        kubectl cp ${pods}:/bzt-configs ./reports --namespace=locust
        echo "Copied reports!!"
        kubectl cp ${pods}:/tmp/artifacts ./artifacts --namespace=locust
        echo "Copied artifacts!!"
        exit 1
        break
    elif echo "$line" | grep -q  "INFO: Done performing with code: 0"; then
        echo "Test Passed."
        kubectl cp ${pods}:/bzt-configs ./reports --namespace=locust
        echo "Copied reports!!"
        kubectl cp ${pods}:/tmp/artifacts ./artifacts --namespace=locust
        echo "Copied artifacts!!"
        exit 0
        break
    fi

done
# exit 0