#!/bin/bash

# Define versions
CILIUM_VERSION="v1.16.1"
TETRAGON_VERSION="v1.1.2"
OTEL_VERSION="0.88.0"

# Create Kind cluster
kind create cluster --config=./config/kind.yaml

# Add Cilium repo to helm
if helm repo list | grep -q cilium; then
    echo "Helm repository cilium is already added."
else
    helm repo add cilium https://helm.cilium.io/
fi

if helm repo list | grep -q open-telemetry; then
    echo "Helm repository signalfx is already added."
else
    helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
fi

helm repo update

# Deploy Cilium
helm upgrade --install cilium cilium/cilium --version $CILIUM_VERSION \
    --namespace kube-system \
    -f ./config/cilium-standard.yaml

# Wait until cluster with Cilium is ready
cilium status --wait

# Create images for backend and client
docker build -t backend:latest -f ./apps/backend/Dockerfile .
docker build  -t client:latest -f ./apps/client/Dockerfile .

kind load docker-image backend:latest
kind load docker-image client:latest

kubectl create ns test
kubectl apply -f ./deployments/backend.yaml
kubectl apply -f ./deployments/client.yaml
kubectl apply -f ./deployments/unrelated-service.yaml

# Deploy OTEL collector
helm upgrade --install opentelemetry-collector open-telemetry/opentelemetry-collector --version $OTEL_VERSION \
    --namespace kube-system \
    -f ./config/otel.yaml

# Tests for runtime enforcement

helm upgrade --install tetragon cilium/tetragon --version $TETRAGON_VERSION \
    --namespace kube-system \
    -f ./config/tetragon.yaml

# kubectl apply -f policies/tetragon/enforcecat.yaml

# Tests for encryption

# kubectl -n kube-system exec -ti ds/cilium -- bash -c "apt-get update && apt-get -y install tcpdump"

# kubectl -n kube-system exec ds/cilium -- bash -c "timeout 5 tcpdump -n -i eth0 -w -" | tee ./results/capture.pcap
# tcpdump -r ./results/capture.pcap -nn -A > ./results/unencrypted-eth0.txt
# rm ./results/capture.pcap

# Manually tested outpound traffic in the docker container of worker-node2

# helm uninstall cilium -n kube-system

# helm upgrade --install cilium cilium/cilium --version $CILIUM_VERSION \
#     --namespace kube-system \
#     -f ./config/cilium-encryption.yaml

# cilium status --wait

# Manually tested outpound traffic in the docker container of worker-node2