#!/bin/bash
set -e

export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export AWS_REGION=us-east-1

# Check for cleanup flag
if [[ "$1" == "cleanup" || "$1" == "--cleanup" || "$1" == "-c" ]]; then
    echo "Cleaning up resources..."
    kubectl delete job pytorch-training -n ddp-training --ignore-not-found=true
    kubectl delete service  pytorch-training -n ddp-training --ignore-not-found=true

    echo "Cleanup complete!"
    exit 0
fi

echo "Building and pushing container..."
cd docker

# Generate unique tag based on timestamp
IMAGE_TAG=$(date +%Y%m%d-%H%M%S)
export IMAGE_TAG

aws ecr create-repository --repository-name pytorch-training --region $AWS_REGION 2>/dev/null || true
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build with no cache to ensure changes are picked up
#docker build --no-cache -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:$IMAGE_TAG .
docker build -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:$IMAGE_TAG .
docker tag $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:$IMAGE_TAG \
           $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pytorch-training:latest

echo "Built and pushed image with tag: $IMAGE_TAG"
cd ..

echo "Deploying to Kubernetes..."
# Delete existing job to force new image pull
kubectl delete job pytorch-training -n ddp-training --ignore-not-found=true
sleep 2

envsubst '${AWS_ACCOUNT_ID} ${AWS_REGION}' < k8s/training.yaml | kubectl apply -f -

echo "Deployment complete!"
echo "Image tag: $IMAGE_TAG"
echo ""
echo "Wait for pods to start, then monitor with:"
echo "  kubectl get pods -n ddp-training -w"
echo "  kubectl logs -n ddp-training -l app=pytorch-training -f"
echo ""
echo "To cleanup: bash scripts/deploy.sh cleanup"
