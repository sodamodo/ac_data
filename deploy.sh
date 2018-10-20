# gcloud auth login
# gcloud config set project ac-transit-46ac1
# gcloud config set compute/zone us-central1-a
# sudo gcloud container clusters create collector-clust --num-nodes=3
# docker build --tag gcr.io/ac-transit-46ac1/collector:v7 .
# docker tag gcr.io/ac-transit-46ac1/collector:v7 gcr.io/ac-transit-46ac1/collector:latest
# docker push gcr.io/ac-transit-46ac1/collector:latest
kubectl run collector --image=gcr.io/ac-transit-46ac1/collector:latest