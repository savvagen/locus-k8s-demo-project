
# Deploying Kubernetes LoadTest Jobs

1. Deploy namespace with secrets: `kubectl apply -f namespace_config.yml`

2. Create configMaps for performance tests code: 
```
kubectl create configmap tests --from-file ./ --namespace=locust
kubectl create configmap locust-scenarios --from-file locust_scenarios --namespace=locust
kubectl create configmap taurus-configs --from-file taurus_configs --namespace locust
kubectl create configmap hooks --from-file listeners --namespace locust
```

