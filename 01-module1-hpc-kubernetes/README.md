# Module 1: DDP Workloads with EFA on CPU

[Home](../README.md) > Module 1: DDP Workloads with EFA on CPU

## Overview

This module teaches the basics about running distributed training workloads on Kubernetes clusters. Content targets End-User personas, less technical than a Systems Administrators. Amazon EKS [[1]](https://docs.aws.amazon.com/eks/), a managed Kubernetes service, controls Kubernetes configuration and control plane management (i.e., Administrator-level). 

All examples run on AWS Graviton [[20]](https://aws.amazon.com/ec2/graviton/) processors (ARM-based architecture). 

We will deploy DDP (Distributed Data Parallel) training jobs on Amazon EKS [[1]](https://docs.aws.amazon.com/eks/), a managed Kubernetes service. Amazon EKS handles the control plane for you, so you can focus your time on running workloads.

### What You'll Learn

- How to connect to an EKS cluster
- How to check cluster resources and EFA networking
- How to install training operators
- How to set up automatic cluster scaling
- How to run distributed training jobs
- How to monitor and debug workloads
- How to use shared storage for training data

### Why Use Cloud for HPC

Cloud platforms let you get computing resources quickly. Traditional HPC systems can take months to set up. With cloud, you can start in minutes and scale up or down as needed.

**Infrastructure as Code** means you write your infrastructure setup in files. Tools like CloudFormation [[2]](https://docs.aws.amazon.com/cloudformation/) or Terraform [[3]](https://www.terraform.io/) let you save these files and reuse them to quickly deploy or reconfigure infrastructure. For example, the eksctl [[4]](https://eksctl.io/) YAML config, `~/environment/eksctl/config.yaml` provided at the top of this tutorial creates a complete EKS cluster, including: a) all networking prerequisites; b) a control plane; c) a node-group of `workers` to run workloads; d) all necessary permissions policies; and e) it preconfigures the cluster to use Amazon's Elastic Fabric Adapter (EFA) [[5]](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html) for high-performance low-latency networking.

**Auto-scaling** adds more machines when you need them and removes them when you don't. This saves money. Kubernetes add ons like Cluster Autoscaler [[9]](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) and Karpenter [[10]](https://karpenter.sh/) grow/shrink pools of workers in response to real workloads. 

Auto Scaling Groups [[8]](https://docs.aws.amazon.com/autoscaling/ec2/). 

Managed Services 
**Specialized Services** give you access to powerful tools without managing infrastructure. SageMaker [[11]](https://docs.aws.amazon.com/sagemaker/) handles training and inference. Bedrock [[12]](https://docs.aws.amazon.com/bedrock/) provides AI models. Specialized instances like P5 [[13]](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/p5-instances.html) for training and Inferentia [[14]](https://docs.aws.amazon.com/inferentia/) for inference give you optimized performance.

### Why Use Kubernetes for HPC

Kubernetes [[15]](https://kubernetes.io/docs/) creates a unified platform for HPC and AI/ML workloads. It works the same way whether you're on-premises or in the cloud. This makes your work portable.

Kubernetes handles complex distributed training jobs. It can:
- Start all training processes at the same time (gang scheduling)
- Place workloads on the best machines (node affinity)
- Manage CPU and GPU resources efficiently
- Integrate with PyTorch and TensorFlow through Kubeflow [[17]](https://github.com/kubeflow/training-operator)
- Provide fault tolerance and automatic checkpointing
- Support high-speed networking like EFA [[5]](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html), InfiniBand [[18]](https://www.infinibandta.org/), and RDMA [[19]](https://www.openfabrics.org/)

Amazon EKS [[1]](https://docs.aws.amazon.com/eks/) makes Kubernetes easier to use. It manages the control plane across multiple data centers with automatic updates. You get:
- Access to specialized compute instances (P4d/P5 for GPUs, Graviton [[20]](https://aws.amazon.com/ec2/graviton/) for CPU training)
- High-performance storage (EFS [[21]](https://docs.aws.amazon.com/efs/), FSx [[22]](https://docs.aws.amazon.com/fsx/))
- AI services (SageMaker [[11]](https://docs.aws.amazon.com/sagemaker/), Bedrock [[12]](https://docs.aws.amazon.com/bedrock/))
- Built-in security and compliance
- Support for Spot instances [[25]](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) to reduce costs
- Integration with CloudWatch [[24]](https://docs.aws.amazon.com/cloudwatch/) for monitoring

**This module uses c7g.16xlarge instances** (64 vCPUs, 128GB RAM each) with AWS Graviton4 processors and EFA networking for high-performance CPU-based distributed training.

## Prerequisites

- AWS CLI configured with appropriate permissions
- kubectl installed
- eksctl [[4]](https://eksctl.io/) installed
- Docker installed (for container builds)
- EKS cluster created using the provided `config.yaml`

## 1. Connect kubectl to Your Cluster

Let's connect kubectl to your EKS cluster. The AWS CLI will set this up automatically.

```bash
# Update kubeconfig for the cluster
aws eks update-kubeconfig --region us-east-1 --name workshop-cluster

# Verify connection
kubectl cluster-info

# Test basic connectivity
kubectl get nodes
```

You should see your cluster endpoint and at least one c7g.16xlarge node.

## 2. Inspect Your Cluster

### Get Basic Information

Let's check what's in your cluster before we deploy anything.

```bash
# List all namespaces
kubectl get namespaces

# Get all nodes with detailed information
kubectl get nodes -o wide

# Check node labels and taints
kubectl describe nodes

# Get all pods across namespaces
kubectl get pods --all-namespaces
```

### Check EFA Status

EFA (Elastic Fabric Adapter) provides fast networking between nodes. This is important for distributed training. Let's check if EFA is enabled.

```bash
# Check if EFA is enabled on nodes
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{": vpc.amazonaws.com/efa: "}{.status.allocatable.vpc\.amazonaws\.com\/efa}{"\n"}{end}'

# Describe node to see EFA-related information
kubectl describe node $(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')

# Check for EFA device plugin (if installed)
kubectl get pods -n kube-system | grep efa
```

### Check Custom Resource Definitions (CRDs)

CRDs extend Kubernetes with new resource types. We need to check what training operators are already installed. CRDs let you define custom objects like PyTorchJob or TensorFlowJob that Kubernetes can manage just like built-in resources. This makes it easy to run distributed training workloads using familiar kubectl commands.

```bash
# List all CRDs
kubectl get crd

# Look for training-related CRDs (None expected initially)
kubectl get crd | grep -E "(pytorch|training|kubeflow)"
```

### Check Cluster Resources

Let's see what resources are available in your cluster.

```bash
# Get cluster resource usage
kubectl top nodes

# Check available storage classes
kubectl get storageclass
```

## 3. Install Kubeflow Training Operator

The Kubeflow Training Operator helps you run distributed training jobs. It supports PyTorch [[28]](https://pytorch.org/), TensorFlow [[29]](https://www.tensorflow.org/), and MXNet [[30]](https://mxnet.apache.org/). Let's install it.

```bash
# Create kubeflow namespace
kubectl create namespace kubeflow

# Install Kubeflow Training Operator
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.8.0"

# Verify installation
kubectl get pods -n kubeflow
kubectl get crd | grep kubeflow
```

### Create Application Namespace

Namespaces help organize your workloads. Let's create one for training jobs.

```bash
# Create namespace for training workloads
kubectl create namespace ddp-training

# Label namespace for monitoring
kubectl label namespace ddp-training purpose=distributed-training
```

## 4. Set Up Automatic Cluster Scaling

### Check Current State

Let's see what nodes you have before we set up auto-scaling.

```bash
# Check current nodes and their status
kubectl get nodes -o wide

# Check existing node group configuration
eksctl get nodegroup --cluster=workshop-cluster --region=us-east-1

# View current resource utilization
kubectl top nodes
```

### Enable Cluster Autoscaler

Cluster Autoscaler [9] adds or removes nodes automatically based on what your workloads need. Your cluster already has the right permissions. Let's enable it.

```bash
# Update the existing nodegroup to enable autoscaling with higher limits
eksctl scale nodegroup \
  --cluster=workshop-cluster \
  --name=workers \
  --nodes=1 \
  --nodes-min=1 \
  --nodes-max=6 \
  --region=us-east-1

# Deploy Cluster Autoscaler using the official manifest
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Update the deployment to use the correct cluster name and service account
kubectl patch deployment cluster-autoscaler -n kube-system -p '{
  "spec": {
    "template": {
      "metadata": {
        "annotations": {
          "cluster-autoscaler.kubernetes.io/safe-to-evict": "false"
        }
      },
      "spec": {
        "serviceAccount": "cluster-autoscaler",
        "containers": [{
          "name": "cluster-autoscaler",
          "image": "registry.k8s.io/autoscaling/cluster-autoscaler:v1.30.0",
          "command": [
            "./cluster-autoscaler",
            "--v=4",
            "--stderrthreshold=info",
            "--cloud-provider=aws",
            "--skip-nodes-with-local-storage=false",
            "--expander=least-waste",
            "--node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/workshop-cluster",
            "--balance-similar-node-groups",
            "--skip-nodes-with-system-pods=false"
          ]
        }]
      }
    }
  }
}'

# Verify Cluster Autoscaler installation
kubectl get pods -n kube-system -l app=cluster-autoscaler
kubectl logs -n kube-system -l app=cluster-autoscaler --tail=20
```

### Test Auto-Scaling

Let's test that the autoscaler works. We'll create a workload that needs more resources than one node can provide.

```bash
# Create a test workload that triggers node scaling
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scaling-test
  namespace: default
spec:
  replicas: 8
  selector:
    matchLabels:
      app: scaling-test
  template:
    metadata:
      labels:
        app: scaling-test
    spec:
      containers:
      - name: test-container
        image: nginx:latest
        resources:
          requests:
            cpu: "8"
            memory: "16Gi"
          limits:
            cpu: "8"
            memory: "16Gi"
EOF

# List pods and their associated labels
kubectl get pods -n kube-system --show-labels

# Monitor Cluster Autoscaler decisions (when using -f option, you can exit with CTRL-C)
kubectl logs -n kube-system -l app=cluster-autoscaler -f

# Watch nodes being provisioned (run in separate terminal)
kubectl get nodes -w

# Check for pending pods that trigger scaling
kubectl get pods | grep Pending

# Clean up test workload
kubectl delete deployment scaling-test
```

### Monitor Scaling

You can watch the autoscaler make decisions about adding or removing nodes.

```bash

# Check scaling events
kubectl get events --sort-by='.lastTimestamp' | grep -i "TriggeredScaleUp\|ScaledUpGroup\|SuccessfulCreate"

# Monitor current node group status
eksctl get nodegroup --cluster=workshop-cluster --region=us-east-1

# Check Auto Scaling Group current state
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names $NODE_GROUP_ASG \
  --region us-east-1 \
  --query 'AutoScalingGroups[0].{MinSize:MinSize,MaxSize:MaxSize,DesiredCapacity:DesiredCapacity,Instances:length(Instances)}'

# Verify EFA availability on all nodes
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{": vpc.amazonaws.com/efa: "}{.status.allocatable.vpc\.amazonaws\.com\/efa}{"\n"}{end}'
```


## 5. Build Container Image for Training

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


## 6. Run DDP Training Job

### Deploy Your Training Job

The simplified DDP example uses a Kubernetes Job which automatically stops after training completes. Use the deploy script for the easiest experience:

```bash
# Navigate to the DDP example directory
cd ~/environment/sc25-flux-eks/01-module1-hpc-kubernetes/ddp-example

# Deploy (builds, pushes, and deploys in one command)
bash scripts/deploy.sh
```

The deploy script handles everything automatically. If you already built the image in section 5, it will rebuild with a new timestamp tag to ensure your latest code changes are included.

### Verify Deployment

Check that your training pods are starting correctly:

```bash
# Check pod status
kubectl get pods -n ddp-training -o wide

# Expected output (Job creates indexed pods):
#NAME                       READY   STATUS    RESTARTS   AGE   IP               NODE                             NOMINATED NODE   READINESS GATES
#pytorch-training-0-6hhcd   1/1     Running   0          6s    192.168.78.250   ip-192-168-88-115.ec2.internal   <none>           <none>
#pytorch-training-1-4g26t   1/1     Running   0          6s    192.168.88.186   ip-192-168-65-32.ec2.internal    <none>           <none>

# Check pod distribution across nodes
kubectl get pods -n ddp-training -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName

# View initial logs to verify setup (note the app name is distinct from the namespace in which it was run)
kubectl logs -n ddp-training -l app=pytorch-training --tail=50
```

### Monitor Training Progress

The DDP example uses Kubernetes Jobs with indexed pods. All pods participate in training calculations equally (no master/worker distinction), but there can be distinctions like the rank0 (i.e., master) managing data pulls, checkpoints, and other unique tasks. 

To monitor your training job in real-time:
```bash
# [Job level] View logs from all training pods (recommended)
kubectl logs -n ddp-training -l app=pytorch-training -f

# [Job level] View logs from specific rank (Tip: use move cursor to delete `xxxxx` and your shell Tab-complete the pod name)
kubectl logs -n ddp-training pytorch-training-0-xxxxx -f

# [Cluster level] Watch pod status (run in separate terminal, or Ctrl-C / ^-C to interrupt)
kubectl get pods -n ddp-training -w

# [Scheduling level] Check training events
kubectl get events -n ddp-training --sort-by='.lastTimestamp'
```

You should see output showing:
- EFA device detection
- Distributed training initialization
- Training progress with loss values
- Epoch completion messages

### Shell into Pods

You might also want to script access for a specific pod for debugging purposes: 
```bash
# A scripted way to get the rank 0 pod name
POD_NAME=$(kubectl get pods -n ddp-training -l app=pytorch-training -o jsonpath='{.items[?(@.metadata.annotations.batch\.kubernetes\.io/job-completion-index=="0")].metadata.name}')
echo "Rank 0 pod: $POD_NAME"

# Monitor MNIST training data download
kubectl exec -n ddp-training $POD_NAME -- find /data/MNIST
kubectl exec -n ddp-training $POD_NAME -- du -hs /data/MNIST

# Check EFA devices inside pod
kubectl exec -it -n ddp-training $POD_NAME -- ls -l /dev/infiniband/

# Check network interfaces
kubectl exec -it -n ddp-training $POD_NAME -- ip addr show

# Check Python environment
kubectl exec -it -n ddp-training $POD_NAME -- python3 -c "import torch; print(torch.__version__)"

# Finally, exec into the rank0 Pod and take an interactive look around (use the `exit` command to return to IDE shell)
kubectl exec -it -n ddp-training $POD_NAME -- /bin/bash
```

**Troubleshooting:**

1. If you see:
```
error: cannot exec into a container in a completed pod; current phase is Succeeded
```
or 
```
Error from server (BadRequest): pod pytorch-training-0-dlbdk does not have a host assigned
```
then your training has completed. This is expected (eventually), but we can re-execute to continue practice with this command: 
```
# Re-run training
bash scripts/deploy.sh cleanup && bash scripts/deploy.sh
```

### Check Resource Usage

Monitor how much CPU and memory your training job is using:

```bash
# Monitor node resource usage
kubectl top nodes

# Monitor pod resource usage
kubectl top pods -n ddp-training

# Check detailed pod metrics (this is VERY verbose with a full detailed listing on each pod in the job)
kubectl describe pods -n ddp-training
```

### Cleanup After Training

Once training completes, the Job will show as "Completed" but pods remain for log inspection:

```bash
# Check job status
kubectl get jobs -n ddp-training

# Expected output: 
#NAME               STATUS     COMPLETIONS   DURATION   AGE
#pytorch-training   Complete   2/2           2m55s      2m57s

# Clean up completed job and pods
bash scripts/deploy.sh cleanup

# Or manually delete
kubectl delete namespace ddp-training
```

## 7. Debugging Other Issues

### Check the Host Machine (Administrators)

Sometimes you need to check the actual EC2 instance running your pods. This is commonly prohibited for End-user personas, but Administrators may find this useful:

```bash
# Get node name where pod is running
kubectl get pods -n ddp-training -o wide

# Use SSM to access the node (if Session Manager is enabled)
NODE_INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:eks:cluster-name,Values=workshop-cluster" \
            "Name=instance-state-name,Values=running" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)

aws ssm start-session --target $NODE_INSTANCE_ID
```

> **Note:** SSM access requires the EC2 instances to have the SSM agent and appropriate IAM role. If SSM is not configured, you'll need to use alternative access methods.

### Node-level Check for EFA

Verify EFA networking is configured correctly:

```bash
# Check if EFA is allocated to pods
kubectl get pods -n ddp-training -o jsonpath='{range .items[*]}{.metadata.name}{": EFA="}{.spec.containers[0].resources.limits.vpc\.amazonaws\.com\/efa}{"\n"}{end}'

# Verify EFA on nodes
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{": EFA="}{.status.allocatable.vpc\.amazonaws\.com\/efa}{"\n"}{end}'
```

### Common Issues and Solutions

**Pods stuck in Pending:**
```bash
# Check why pod is pending
kubectl describe pod -n ddp-training <pod-name>

# Common causes:
# - Insufficient EFA resources: Check node EFA allocation
# - Node selector mismatch: Verify c7g.16xlarge nodes exist
# - Resource constraints: Check CPU/memory availability
```


**Image pull errors:**
```bash
# Check if ECR repository exists
aws ecr describe-repositories --repository-names ddp-training --region us-east-1

# Verify image exists
aws ecr list-images --repository-name ddp-training --region us-east-1

# Check pod events for detailed error
kubectl describe pod -n ddp-training $POD_NAME | grep -A 10 Events
```

## Side Quest 3: Set Up Shared Storage

It is common for training jobs to output checkpoint files and/or have a shared storage space for input data and other purposes. To add this to our jobs, we must submit a Kubernetes PersistentVolumeClaim (PVC) that is ultimately fulfilled by a Persistent Volume (PV). Here we will consider [FSx for Lustre](https://aws.amazon.com/fsx/lustre/) storage which offers high performance scratch and persistent profiles. 

To begin, you will deploy The FSx for Lustre Container Storage Interface (CSI) driver. It provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of FSx for Lustre file systems.
Then, you will create a Kubernetes `StorageClass` for FSx for Lustre. A Kubernetes `StorageClass` is a Kubernetes storage mechanism that lets you provision persistent volumes (PV) in a Kubernetes cluster and allows pods to dynamically request the specific type of storage they need.
To finish, you will create a persistent volume claim (PVC) using the `StorageClass` created previously, which will dynamically provision an FSx for Lustre persistent volume (PV). A PVC is a claim of storage capacity from a persistent volume and is a resource that can be mounted into pods.

#### 1. Deploy FSx CSI Driver

The following command deploys the FSx Container Storage Interface driver to your cluster:

```bash
kubectl apply -k "github.com/kubernetes-sigs/aws-fsx-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.6"
```

#### 2. Retrieve security group of cluster

Create a security group that allows TCP traffic on port 988 for FSx

```bash
SECURITY_GROUP_ID=`aws eks describe-cluster --name ${EKS_CLUSTER_NAME} --query cluster.resourcesVpcConfig.clusterSecurityGroupId --region ${AWS_REGION}`
echo $SECURITY_GROUP_ID
```

#### 3. Retrieve subnet id of node group

```bash
SUBNET_ID=`aws eks describe-nodegroup --cluster-name ${EKS_CLUSTER_NAME} --nodegroup-name "workers" --query nodegroup.subnets --region ${AWS_REGION} --output text`
echo $SUBNET_ID
```

#### 4. Create storage class

Execute the following snippet to generate the storage class manifest (`fsx-storage-class.yaml`) and then apply it to the cluster

```bash
cat > ~/environment/fsx-storage-class.yaml << EOF
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: fsx-sc
provisioner: fsx.csi.aws.com
parameters:
  subnetId: ${SUBNET_ID}
  securityGroupIds: ${SECURITY_GROUP_ID}
  deploymentType: SCRATCH_2
  storageType: SSD
EOF
```

```bash
kubectl apply -f ~/environment/fsx-storage-class.yaml
```

To verify that the storage class is created successfully, execute:

```bash
kubectl get storageclass
```

You should see a list, similar to the following:

```console
NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
fsx-sc          fsx.csi.aws.com         Delete          Immediate              false                  9s
gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  16h
```

#### 6. Dynamically provision FSx volume

Next we create a persistent volume claim manifest into a file named `fsx-pvc.yaml`:

```bash
cat > ~/environment/fsx-pvc.yaml << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cd fsx-pvc
  namespace: ddp-training
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: fsx-sc
  resources:
    requests:
      storage: 1200Gi
EOF
```

We will add the persistent volume claim, `fsx-pvc`, to the ddp-training namespace, using the `fsx-sc` storage class. This dynamically creates an FSx for Lustre persistent volume (i.e., it launches a new filesystem through the FSx Lustre service). Creation of the volume is expected to take 6-8 minutes.

```bash
# in case the namespace was deleted above
kubectl create namespace ddp-training
kubectl apply -f ~/environment/fsx-pvc.yaml
```

Get the persistent volume claim to check its status

```bash
kubectl -n ddp-training get pvc fsx-pvc
```

While the persistent volume is provisioning, you should see output like the following:

```text
NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
fsx-pvc   Pending                                      fsx-sc         <unset>                 13s
```

Describe the FSx file systems in your account to see the current status

```bash
aws fsx describe-file-systems --region ${AWS_REGION}
```

You should see output like the following:

```json
{
  "FileSystems": [
    {
      "VpcId": "vpc-09e19ec07fd43d433",
      "LustreConfiguration": {
        "CopyTagsToBackups": false,
        "WeeklyMaintenanceStartTime": "7:07:30",
        "DataCompressionType": "NONE",
        "MountName": "fsx",
        "DeploymentType": "SCRATCH_2"
      },
      "Tags": [
        {
          "Value": "pvc-159049a3-d25d-465f-ad7e-3e0799756fce",
          "Key": "CSIVolumeName"
        }
      ],
      "StorageType": "SSD",
      "SubnetIds": ["subnet-07a7858f836ad4bb4"],
      "FileSystemType": "LUSTRE",
      "CreationTime": 1664481419.438,
      "ResourceARN": "arn:aws:fsx:us-east-2:111122223333:file-system/fs-0a983bda1fd46d2f7",
      "StorageCapacity": 1200,
      "NetworkInterfaceIds": ["eni-04b75f9deb999568f", "eni-0c4695b00d3033f2c"],
      "FileSystemId": "fs-0a983bda1fd46d2f7",
      "DNSName": "fs-0a983bda1fd46d2f7.fsx.us-east-2.amazonaws.com",
      "OwnerId": "944270628268",
      "Lifecycle": "CREATING"
    }
  ]
}
```

The **Lifecycle** field indicates the current status. It is expected that the status will be **CREATING** for about 7 minutes. When the provisioning is complete, the status will change to **AVAILABLE**.

When the FSx volume becomes available, the status of the persistent volume claim in Kubernetes will change to **Bound**

```bash
# This command will continue to watch for the status change (exit with CTRL-C / ^-C)
kubectl -n ddp-training get pvc fsx-pvc -w
```

Output:

```text
NAME      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
fsx-pvc   Bound    pvc-159049a3-d25d-465f-ad7e-3e0799756fce   1200Gi     RWX            fsx-sc         7m45s
```

The **Bound** status indicates that the persistent volume claim is successfully bound to the persistent FSx for Lustre volume and is ready to be mounted by pods.

### Attach the storage to your job

To attach the storage to your training job, modify the k8s/training.yaml to add: 
```bash
spec:
  pytorchReplicaSpecs:
    Master:
      template:
        spec:
          containers:
          - name: pytorch
            volumeMounts:
            - name: training-data
              mountPath: /shared-data
          volumes:
          - name: training-data
            persistentVolumeClaim:
              claimName: fsx-pvc
    Worker:
      template:
        spec:
          containers:
          - name: pytorch
            volumeMounts:
            - name: training-data
              mountPath: /shared-data
          volumes:
          - name: training-data
            persistentVolumeClaim:
              claimName: fsx-pvc'
```
### Delete the PVC

When you're ready to delete the storage and PVC, 
```
# Release the PVC and the FSx filesystem will be deleted.
kubectl -n ddp-training get pvc fsx-pvc

# Release the namespace and everything within it (including training jobs)
kubectl delete namespace ddp-training --ignore-not-found=true
```


## References

1. Amazon Web Services. ["Amazon Elastic Kubernetes Service (Amazon EKS)."](https://docs.aws.amazon.com/eks/) AWS Documentation.
2. Amazon Web Services. ["AWS CloudFormation."](https://docs.aws.amazon.com/cloudformation/) AWS Documentation.
3. HashiCorp. ["Terraform."](https://www.terraform.io/)
4. eksctl. ["The official CLI for Amazon EKS."](https://eksctl.io/)
5. Amazon Web Services. ["Amazon EFA (Elastic Fabric Adapter)."](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html) AWS Documentation.
6. Amazon Web Services. ["Amazon EventBridge."](https://docs.aws.amazon.com/eventbridge/) AWS Documentation.
7. Amazon Web Services. ["AWS Lambda."](https://docs.aws.amazon.com/lambda/) AWS Documentation.
8. Amazon Web Services. ["Amazon EC2 Auto Scaling."](https://docs.aws.amazon.com/autoscaling/ec2/) AWS Documentation.
9. Kubernetes. ["Cluster Autoscaler."](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) Kubernetes SIG Autoscaling.
10. Karpenter. ["Karpenter: Just-in-time Nodes for Any Kubernetes Cluster."](https://karpenter.sh/) AWS and Kubernetes Community.
11. Amazon Web Services. ["Amazon SageMaker."](https://docs.aws.amazon.com/sagemaker/) AWS Documentation.
12. Amazon Web Services. ["Amazon Bedrock."](https://docs.aws.amazon.com/bedrock/) AWS Documentation.
13. Amazon Web Services. ["Amazon EC2 P5 Instances."](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/p5-instances.html) AWS Documentation.
14. Amazon Web Services. ["AWS Inferentia."](https://docs.aws.amazon.com/inferentia/) AWS Documentation.
15. Kubernetes. ["Kubernetes Documentation."](https://kubernetes.io/docs/)
16. Converged Computing. ["Converged Computing: A Best of Both Worlds of High-Performance Computing and Cloud"](https://www.computer.org/csdl/magazine/cs/2024/03) IEEE Computer Society, 2024.
17. Kubeflow Community. ["Kubeflow Training Operator."](https://github.com/kubeflow/training-operator) GitHub.
18. InfiniBand Trade Association. ["InfiniBand Architecture Specification."](https://www.infinibandta.org/) InfiniBand Trade Association.
19. OpenFabrics Alliance. ["RDMA (Remote Direct Memory Access)."](https://www.openfabrics.org/) OpenFabrics Alliance.
20. Amazon Web Services. ["AWS Graviton Processors."](https://aws.amazon.com/ec2/graviton/) AWS Documentation.
21. Amazon Web Services. ["Amazon EFS (Elastic File System)."](https://docs.aws.amazon.com/efs/) AWS Documentation.
22. Amazon Web Services. ["Amazon FSx."](https://docs.aws.amazon.com/fsx/) AWS Documentation.
23. Amazon Web Services. ["Amazon VPC."](https://docs.aws.amazon.com/vpc/) AWS Documentation.
24. Amazon Web Services. ["Amazon CloudWatch."](https://docs.aws.amazon.com/cloudwatch/) AWS Documentation.
25. Amazon Web Services. ["Amazon EC2 Spot Instances."](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) AWS Documentation.
26. Amazon Web Services. ["AWS Fargate."](https://docs.aws.amazon.com/fargate/) AWS Documentation.
27. Prometheus Community. ["kube-prometheus-stack Helm Chart."](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) GitHub.
28. PyTorch Foundation. ["PyTorch."](https://pytorch.org/) 
29. TensorFlow. ["TensorFlow."](https://www.tensorflow.org/)
30. Apache Software Foundation. ["Apache MXNet."](https://mxnet.apache.org/)
31. Helm. ["The package manager for Kubernetes."](https://helm.sh/)
32. Amazon Web Services. ["Amazon Elastic Container Registry (ECR)."](https://docs.aws.amazon.com/ecr/) AWS Documentation.
33. Amazon Web Services. ["AWS Systems Manager Session Manager."](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) AWS Documentation.
34. Amazon Web Services. ["Amazon EFS CSI Driver."](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub.
35. NVIDIA. ["NCCL (NVIDIA Collective Communication Library)."](https://developer.nvidia.com/nccl) NVIDIA Developer Documentation.
