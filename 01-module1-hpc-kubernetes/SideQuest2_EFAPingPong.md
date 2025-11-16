
## Side Quest 2: Build Container Image for Training

### Build and Push Your Image Using the Deploy Script

The simplified DDP example includes a deploy script that handles building, pushing, and deploying your training job. This is the recommended approach.

```bash
# Navigate to the DDP example directory
cd ~/environment/sc25-flux-eks/01-module1-hpc-kubernetes/ddp-example

# Run the deploy script (builds image, pushes to ECR, and deploys to Kubernetes)
bash scripts/deploy.sh
```

The deploy script will:
1. Build the Docker image with a unique timestamp tag
2. Push to Amazon ECR (creates repository if needed)
3. Deploy the Kubernetes Job
4. Show you monitoring commands

Building and pushing typically takes 3-5 minutes total.

### Manual Build (Alternative)

If you prefer to build manually or need to customize the process:

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

# Wait for pod to be ready
kubectl wait --for=condition=Ready pod/efa-test -n ddp-training --timeout=300s

# Check EFA device is mapped into container
kubectl exec -it efa-test -n ddp-training -- ls -l /dev/infiniband/

# Check EFA drivers are installed (see [](https://docs.aws.amazon.com/eks/latest/userguide/node-efa.html) for more)
kubectl exec -it efa-test -n ddp-training -- /opt/amazon/efa/bin/fi_info -p efa || echo "No EFA device found"

# Check RDMA statistics. These counters capture real utilization of the EFA interface. 
kubectl exec -it efa-test -n ddp-training -- rdma statistic show

# Clean up test pod
kubectl delete pod efa-test -n ddp-training
```

#### EFA Bandwidth Test with fi_pingpong (Advanced)

Next we will run a `fi_pingpong` test to confirm EFA transmissions between pods will work. `fi_pingpong` is provided by the EFA installer, so you absolutely need a container image with EFA installer installed. Look closely at `efa-test/k8s/efa-pingpong.yaml` to see how we lean on a pre-built [Deep Learning Container Image from AWS Public ECR](https://aws.amazon.com/ai/machine-learning/containers/). 

Deploy the EFA pingpong test using the provided configuration:

```bash
# Deploy EFA bandwidth test pods
kubectl apply -f ~/environment/sc25-flux-eks/01-module1-hpc-kubernetes/efa-test/k8s/efa-pingpong.yaml

# Monitor the test
kubectl logs -n efa-test -l app=efa-test -f

# After test completes, cleanup
kubectl delete job efa-pingpong-test -n efa-test
kubectl delete service efa-test-svc -n efa-test
kubectl delete namespace efa-test
```

**Expected output:**

The test will show bandwidth measurements from fi_pingpong followed by EFA statistics:

```
[...]
2k      10k     =10k     39m         0.36s    113.21      18.09       0.06
3k      10k     =10k     58m         0.37s    168.27      18.26       0.05
4k      10k     =10k     78m         0.37s    221.55      18.49       0.05
6k      10k     =10k     117m        0.39s    317.43      19.36       0.05
8k      10k     =10k     156m        0.40s    405.88      20.18       0.05

=== Data Transfer Summary (Server) ===
Counter                     Starting    ⚠ (Change)
-------                     --------      ----------
tx_bytes                    26717622      +286897950  ✓
rx_bytes                    19875952      +286680004  ✓
send_bytes                  19875780      +286680004  ✓
recv_bytes                  19875392      +286680004  ✓
```

**Key indicators that EFA is working:**
- ✓ checkmarks show EFA counters increased during the test
- Delta values show ~300MB transferred (matching the bandwidth test)
- High bandwidth (multiple GB/s) in fi_pingpong output
- All four metrics (tx_bytes, rx_bytes, send_bytes, recv_bytes) show activity

**Note:** The test automatically handles counter wraparound (negative values from rdma command are converted to unsigned 32-bit integers).

**If your cluster is not scale properly:**
```
Error from server (BadRequest): container "efa-test" in pod "efa-pingpong-test-1-6bk7d" is waiting to start: ContainerCreating
```
You might see this error when grabbing the app=efa logs. ContainerCreating means the cluster is waiting for worker nodes with the required EFA labels to come up, and to pull the container image. Wait a minute or two and retry the commands. 


**If fi_pingpong is not available in your container image:**
This test will fail with a `Command Not Found` error. Don't worry though, Training can still work using TCP networking instead of EFA RDMA. The real requirement is that you have PyTorch installed training functionality. 


---
**Navigation:**
- Back to: [Module 1: HPC on Kubernetes](../01-module1-hpc-kubernetes/README.md)