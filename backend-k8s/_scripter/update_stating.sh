#!/bin/bash
parent_path="$( cd "$(dirname "$0")" ; pwd -P )"
project_path=$parent_path/..
cd $project_path
kubectl apply -f staging/env/configmaps.yaml
kubectl apply -f staging/env/popeye-nginx-conf.yaml
kubectl apply -f staging/env/secrets.yaml
kubectl apply -f staging/ingress.yaml

kubectl apply -f popeye-api.yaml
kubectl apply -f rabbitmq.yaml
kubectl apply -f redis.yaml
kubectl apply -f backend-config.yaml
