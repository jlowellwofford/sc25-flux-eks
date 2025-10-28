# Create Amazon EKS Cluster

[Home](../README.md) > [Module 1](README.md) > Create EKS Cluster

## Overview

In this section, you will create a new Amazon EKS cluster using `eksctl`. The cluster will be configured specifically for HPC workloads with appropriate instance types and networking settings.

## Set Environment Variables

Prior to creating the cluster, ensure your environment variables are set by executing the following commands in your VS Code integrated terminal:

```bash
echo export EKS_CLUSTER_NAME=eks-hpc >> env_vars
source env_vars
echo "EKS_CLUSTER_NAME=${EKS_CLUSTER_NAME}"

export AWS_REGION=${AWS_REGION:-us-east-1}
echo "AWS_REGION=${AWS_REGION}"

# Select two random availability zones for the cluster
export AZ_IDS=(use1-az4 use1-az5 use1-az6)
echo "AZ_IDS=(${AZ_IDS[@]})"
export AZ_COUNT=${#AZ_IDS[@]}
export AZ_IND=($(python3 -S -c "import random; az_ind=random.sample(range(${AZ_COUNT}),2); print(*az_ind)"))
echo "AZ_IND=(${AZ_IND[@]})"
export AZ1_NAME=$(aws ec2 describe-availability-zones --region ${AWS_REGION} --query "AvailabilityZones[?ZoneId == '${AZ_IDS[${AZ_IND[0]}]}'].ZoneName" --output text)
echo "AZ1_NAME=${AZ1_NAME}"
export AZ2_NAME=$(aws ec2 describe-availability-zones --region ${AWS_REGION} --query "AvailabilityZones[?ZoneId == '${AZ_IDS[${AZ_IND[1]}]}'].ZoneName" --output text)
echo "AZ2_NAME=${AZ2_NAME}"

export IMAGE_URI=$(aws ecr --region ${AWS_REGION} describe-repositories --repository-name sc22-container --query "repositories[0].repositoryUri" --output text)
echo "IMAGE_URI=${IMAGE_URI}"
```

> **⚠️ Warning:** The IMAGE_URI is required for later steps. If the value of IMAGE_URI above is blank, you may need to create the container image first or check with the workshop instructors.

## Create the EKS Manifest File

The EKS cluster manifest specifies the Kubernetes version, AWS region, availability zones, instance types, and network settings. For this workshop, you will create an Amazon EKS cluster with one managed node group optimized for HPC workloads.

Create the manifest file by pasting the following commands into your VS Code integrated terminal:

```bash
cat > ~/environment/eks-hpc.yaml << EOF
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: ${EKS_CLUSTER_NAME}
  version: "1.21"
  region: ${AWS_REGION}

availabilityZones:
  - ${AZ1_NAME}
  - ${AZ2_NAME}

iam:
  withOIDC: true

managedNodeGroups:
  - name: hpc
    instanceType: c5.24xlarge
    instancePrefix: hpc
    privateNetworking: true
    availabilityZones: ["${AZ1_NAME}"]
    efaEnabled: false
    minSize: 0
    desiredCapacity: 1
    maxSize: 10
    volumeSize: 30
    iam:
      withAddonPolicies:
        autoScaler: true
        ebs: true
        fsx: true
EOF
```

### Understanding the Configuration

Notice the `efaEnabled` flag in the manifest file. When set to `true`, `eksctl` creates a node group with the correct setup for using the [Elastic Fabric Adapter (EFA)](https://aws.amazon.com/hpc/efa/) network interface to run tightly-coupled workloads with MPI. 

`eksctl` leverages AWS CloudFormation to create:
- A [Placement group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) that puts instances close together
- An [EFA-enabled security group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start.html#efa-start-security)

If EFA is enabled, `instanceType` must be set to one of the [EC2 instance types with EFA support](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html#efa-instance-types), and the managedNodeGroup `availabilityZones` must be constrained to a single AZ. 

In this workshop, we set `efaEnabled` to `false` for simplicity.

## Create the EKS Cluster

Now create the cluster using the manifest file. This process takes approximately 20 minutes total:
- ~10 minutes to create the Kubernetes control plane
- ~10 minutes to create the node group

```bash
eksctl create cluster -f ~/environment/eks-hpc.yaml
```

> **ℹ️ Info:** While the cluster is being created, you can continue reading the next sections to understand what comes next, but don't execute the commands until this cluster creation is complete.

Upon successful completion, you will see a log line similar to this:

```console
2022-09-29 03:34:37 [✔]  EKS cluster "eks-hpc" in "us-east-1" region is ready
```

## Verification

Once the cluster is created, verify it's working correctly:

```bash
kubectl get nodes
```

You should see output showing your cluster nodes in a `Ready` state.

---
**Navigation:**
- Previous: [Install CLIs](01-install-clis.md)
- Next: [Validate Amazon EKS Cluster](03-validate-eks-cluster.md)
- Up: [Module 1](README.md)