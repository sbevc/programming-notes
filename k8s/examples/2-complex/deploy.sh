docker build -t sebasbeco/multi-client:latest -t sebasbeco/multi-client:$COMMIT_SHA -f ./client/Dockerfile ./client
docker build -t sebasbeco/multi-server:latest -t sebasbeco/multi-server:$COMMIT_SHA -f ./server/Dockerfile ./server
docker build -t sebasbeco/multi-worker:latest -t sebasbeco/multi-worker:$COMMIT_SHA -f ./worker/Dockerfile ./worker

# We don't have to login to docker to push because we already did in .travis.yml file
docker push sebasbeco/multi-client:latest
docker push sebasbeco/multi-server:latest
docker push sebasbeco/multi-worker:latest
docker push sebasbeco/multi-client:$COMMIT_SHA
docker push sebasbeco/multi-server:$COMMIT_SHA
docker push sebasbeco/multi-worker:$COMMIT_SHA

kubectl apply -f k8s

# Imperatively set latest images on each deployment
kubectl set image deployments/client-deployment client=sebasbeco/multi-client:$COMMIT_SHA
kubectl set image deployments/server-deployment server=sebasbeco/multi-server:$COMMIT_SHA
kubectl set image deployments/worker-deployment worker=sebasbeco/multi-worker:$COMMIT_SHA