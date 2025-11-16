# Module 1: DDP Workloads with EFA on CPU

[Home](../README.md) > Module 1: DDP Workloads with EFA on CPU

## Overview

This module teaches the basics about running distributed training workloads on [Kubernetes](https://kubernetes.io/docs/) clusters. Content targets End-User personas, less technical than a Systems Administrators. 

All examples run on [AWS Graviton](https://aws.amazon.com/ec2/graviton/) processors (ARM-based architecture). [Amazon EKS](https://docs.aws.amazon.com/eks/), a managed Kubernetes service, takes on the task of hosting your Kubernetes configuration (i.e., it performs the Administrator-level management tasks for you). 

Your task will be to deploy Distributed Data Parallel (DDP) training jobs for ML to an existing EKS cluster. You will work through various exercises to familiarize yourself with Kubernetes, ML training, and debugging. 

### What You'll Learn

- How to connect to an EKS cluster
- How to check cluster resources and EFA networking
- How to install training operators
- How to set up automatic cluster scaling
- How to run distributed training jobs
- How to monitor and debug workloads
- How to use shared storage for training data

### Why Use Cloud for HPC

**Flexibility and Agility** are two major reasons to use Cloud for HPC. Cloud and on-premesis HPC are built on similar compute, networking, and storage capabilities, but Traditional HPC systems tend to take months or longer to plan, acquire, and deploy a fixed-size footprint of hardware. Cloud Agility lets us to start in minutes and scale up or down as needed. Cloud flexibility lets us pivot from infrastructure decisions like CPU microarchitecture, accelerator type, or storage technology, and reshape our HPC to better fit application needs.

#### Other differentiators for Cloud: 

**Infrastructure as Code (IaC)** means documenting your infrastructure configuration/setup to be reproducible. Tools like [CloudFormation](https://docs.aws.amazon.com/cloudformation/) or [Terraform](https://www.terraform.io/) let you rebuild/reconfigure an entire HPC environment in minutes. As part of this workshop, an [eksctl](https://eksctl.io/) YAML config is provided in `~/environment/eksctl/config.yaml`. Note that 34 lines of human-readable text represents your complete EKS cluster, including: 
 * all networking prerequisites like IP allotments, subnet configuration, network routes, and security groups; 
 * the Kubernetes control plane; 
 * a group of node `workers` to run workloads; 
 * all necessary permissions policies; and 
 * preconfigured network device for Amazon's [Elastic Fabric Adapter (EFA)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html)--high-performance, low-latency networking. 

In later sections you will also apply [Kubectl](https://kubernetes.io/docs/reference/kubectl/) YAML config files and [Helm Charts](https://helm.sh/) to reconfigure EKS--these are also IaC. 

**Elastic-scaling** adds more compute hosts when you need and removes them when you don't. This saves money and accelerates time to science. Kubernetes add-ons like [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) (used here) or [Karpenter](https://karpenter.sh/) grow/shrink pools of worker nodes on your cluster in response to real workloads. 

**Specialized and Managed Services** give you access to powerful tools without managing infrastructure. EKS is one example of a Managed infrastructure. For those who get deeper into machine learning, [Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/) is a fully-managed ML service on AWS to build, train, and deploy models. [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) is a fully-managed service to build and scale generative AI applications with foundation models. These services handle the complexity and undifferentiated heavy lifting in tasks allowing you to focus on what matters most: your research / business. 

### Why Use Kubernetes for HPC

Kubernetes creates a unified platform for HPC and AI/ML workloads. It works the same way whether you're on-premises or in the cloud. This makes your work portable.

Kubernetes handles complex distributed training jobs. In brief, it can:
- Start all training processes at the same time (gang scheduling)
- Place workloads on the best machines (node affinity)
- Manage CPU and GPU resources efficiently
- Integrate with PyTorch and TensorFlow through projects like [Kubeflow](https://github.com/kubeflow/training-operator)
- Provide fault tolerance and automatic checkpointing
- Integrate most HPC components including high-speed networking, parallel filesystems, schedulers, etc. 

> **Note:** This module uses `workshop-cluster`, an Amazon EKS cluster with [c7g.16xlarge](https://aws.amazon.com/ec2/instance-types/c7g/) instances (64 cores, 128GB RAM each, Graviton3 ARM64 processor, 30 Gbps EFA) for high-performance CPU-based distributed training.

## Prerequisites

- AWS CLI configured with appropriate permissions
- kubectl installed
- eksctl installed
- Docker installed (for container builds)
- EKS cluster created using the provided `config.yaml`

## 1. Connect kubectl to Your Cluster

`kubectl` is the primary tool used by both End-users and Administrators to interact with a running Kubernetes cluster. 

Let's configure kubectl to use your EKS cluster. The AWS CLI interacts with the EKS service API to set this up for you.

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
# List all namespaces. Namespaces help us logically partition a Kubernetes cluster into virtual sub-spaces. They organize and help prevent naming conflicts 
kubectl get namespaces

# Get all nodes with detailed information
kubectl get nodes -o wide

# Check node labels and taints
kubectl describe nodes

# Get all pods across namespaces
kubectl get pods --all-namespaces
```

### Check EFA Status

[EFA (Elastic Fabric Adapter)](https://doi.org/10.1109/HOTI.2019.00023) is Amazon technology providing low-latency, high-bandwidth networking between instances. This is important for scaling distributed training, especially when running on fleets of GPU instances. Let's check if EFA is enabled on worker nodes.

```bash
# Check if EFA is enabled on nodes
# the key "vpc.amazonaws.com/efa" indicates that EFA resource is registered, and the value indicates the number of EFA interfaces in the node. 
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{": vpc.amazonaws.com/efa: "}{.status.allocatable.vpc\.amazonaws\.com\/efa}{"\n"}{end}'


# When you create a node group with efaEnabled: true, EKS deploys the EFA Kubernetes device plugin for you as a DaemonSet (i.e., as nodes come online)
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

# Look at pod resource usage
kubectl top pods --all-namespaces

# Check available storage classes
kubectl get storageclass
```

## 3. Install Kubeflow Training Operator

The [Kubeflow Training Operator](https://github.com/kubeflow/training-operator) helps you run distributed training jobs. It supports [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/), and [MXNet](https://mxnet.apache.org/). Let's install it.

```bash
# Create kubeflow namespace
kubectl create namespace kubeflow

# Install Kubeflow Training Operator
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.8.0"

# Verify installation
kubectl get pods -n kubeflow
kubectl get crd | grep kubeflow
```

### Check Current Cluster scale
Let's see what nodes you have before we set up auto-scaling.

```bash
# Check current nodes and their status
kubectl get nodes -o wide

# Check existing node group configuration
eksctl get nodegroup --cluster=workshop-cluster --region=us-east-1

# View current resource utilization
kubectl top nodes
```

## 4. Set Up Automatic Cluster Scaling

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

--- 

### Time-permitting, go on a Side Quest!
- Click here to go to: [SideQuest #1: Build a Container Image (Optional)](SideQuest1_BuildContainerImage.md)

---


## 5. Run DDP Training Job

The simple DDP example, provided in `~/01-module1-hpc-kubernetes/ddp-example`, includes a deploy script that handles building, pushing, and deploying a training job. 

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

Study the deploy.sh and understand the flow of commands. If you want to run it manually, the command is:

```bash
# Deploy
kubectl apply -f k8s/training.yaml

# Delete
kubectl delete -f k8s/training.yaml
```

### Verify Deployment

Check that your training pods are starting correctly. You may see some pods waiting on workers to come online. Remember that pods also require nodes have the EFA daemonset:

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

The DDP example uses Kubernetes Job with indexed pods. All pods participate in training calculations equally (no master/worker distinction), but there can be distinctions in command logic. For example our DDP distinguishes rank 0 in both `docker/train.py` and `k8s/training.yaml` for data pulls, checkpoints, and other unique tasks. 

An alternative to Kubernetes Job type is to use PyTorchJob from the Kubeflow CRD. The Kubeflow PyTorchJob provided in `k8s/pytorchjob-comparison.yaml` calls out some benefits to the CRD approach like distinguished pod roles (Master/Worker) and managed aspects of training for retries/replicas, scaling, etc. Time-permitting, try launching this job type and monitor it. 

To monitor your training job in real-time:
```bash
# [Job level] View logs from all training pods (recommended)
kubectl logs -n ddp-training -l app=pytorch-training -f

# [Job level] View logs from specific rank (Tip: you can use Tab-complete on kubectl to resolve xxxxx in the pod name)
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

You might need access to a specific pod for debugging purposes: 
```bash
# A scripted way to get the rank 0 pod name
POD_NAME=$(kubectl get pods -n ddp-training -l app=pytorch-training -o jsonpath='{.items[?(@.metadata.annotations.batch\.kubernetes\.io/job-completion-index=="0")].metadata.name}')
echo "Rank 0 pod: $POD_NAME"

# Monitor training data download
kubectl exec -n ddp-training $POD_NAME -- find /data/MNIST

# Check network interfaces
kubectl exec -it -n ddp-training $POD_NAME -- ip addr show

# Check Python environment
kubectl exec -it -n ddp-training $POD_NAME -- python3 -c "import torch; print(torch.__version__)"

# Exec into the rank0 Pod and take an interactive look around (use the `exit` command to return to IDE shell)
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

# Or delete the entire namespace and it will nuke whats attached
kubectl delete namespace ddp-training
```

## 5. Debugging Other Issues

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
---

### Time-permitting, go on a Side Quest!

- Click here to go to: [SideQuest #1: Build a Container Image (Optional)](SideQuest1_BuildContainerImage.md)

- Click Here to go to: [SideQuest #2: EFA Bandwidth Test with fi_pingpong (Optional)](SideQuest1_EFAPingPong.md)

- Click Here to go to: [SideQuest #3: Set Up Shared Storage (Optional)](SideQuest3_StoragePVC.md)

---

> End of Module 1

---
**Navigation:**
- Previous: [VS Code Connection Guide](01-vscode-connection.md)
- Next: [Module 1: HPC on Kubernetes](../01-module1-hpc-kubernetes/README.md)
- Up: [Workshop Setup](README.md)
