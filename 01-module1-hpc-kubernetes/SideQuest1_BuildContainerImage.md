## Side Quest 1: Build Container Image for Training

If you wnat to build container images manually or need to customize the process:

```bash
# Set environment variables
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export AWS_REGION=us-east-1

# Create ECR repository
aws ecr create-repository \
  --repository-name ddp-training \
  --region ${AWS_REGION} \
  --image-scanning-configuration scanOnPush=true || true

# Navigate to docker directory
cd ~/environment/sc25-flux-eks/01-module1-hpc-kubernetes/ddp-example/docker

# Build the image
docker build --no-cache -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/ddp-training:latest .

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Push image
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/ddp-training:latest
```

### Test EFA in Container (Optional)

You can verify EFA networking works inside containers before running training. We'll test basic EFA device presence and, if available, run bandwidth tests.

### Create Application Namespace

Let's first create a namespace to organize our workspace.

```bash
# Create namespace for training workloads
kubectl create namespace ddp-training

# Label namespace for monitoring
kubectl label namespace ddp-training purpose=distributed-training
```

#### Basic EFA Device Test

Note that we are calling a pre-built [Deep Learning Container Image from AWS Public ECR](https://aws.amazon.com/ai/machine-learning/containers/). This has all EFA prerequisites installed. You can practice changing to `image: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/ddp-training:latest` (no EFA-installer) and see the difference [EFA-installer](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start.html#efa-start-enable) can make. We will also run the test in the `ddp-training` namespace, which will make the commands reusable when you get to real training. 


```bash
# Create test pod with EFA
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: efa-test
  namespace: ddp-training
spec:
  nodeSelector:
    node.kubernetes.io/instance-type: c7g.16xlarge
  containers:
  - name: efa-test
    image: public.ecr.aws/deep-learning-containers/pytorch-training-arm64:2.7.0-gpu-py312-cu128-ubuntu22.04-ec2-v1.37-soci
    command: ["/bin/bash", "-c", "sleep 3600"]
    resources:
      limits:
        vpc.amazonaws.com/efa: 1
      requests:
        vpc.amazonaws.com/efa: 1
EOF

# Wait for pod to be ready, this can take 5-6 minutes
kubectl wait --for=condition=Ready pod/efa-test -n ddp-training --timeout=360s

# Check EFA device is mapped into container
kubectl exec -it efa-test -n ddp-training -- ls -l /dev/infiniband/

# Check EFA drivers are installed (see [](https://docs.aws.amazon.com/eks/latest/userguide/node-efa.html) for more)
kubectl exec -it efa-test -n ddp-training -- /opt/amazon/efa/bin/fi_info -p efa || echo "No EFA device found"

# Check RDMA statistics. These counters capture real utilization of the EFA interface. 
kubectl exec -it efa-test -n ddp-training -- rdma statistic show

# Clean up test pod
kubectl delete pod efa-test -n ddp-training
```


---
**Navigation:**
- Back to: [Module 1: HPC on Kubernetes](../01-module1-hpc-kubernetes/README.md)