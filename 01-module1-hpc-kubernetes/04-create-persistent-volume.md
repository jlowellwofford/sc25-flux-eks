# Create Persistent Volume

[Home](../README.md) > [Module 1](README.md) > Create Persistent Volume

## Overview

In this section, you will create an FSx for Lustre file system and expose it as a resource in Kubernetes for your application pods. This high-performance parallel file system will be used by GROMACS for reading and writing simulation data.

The process involves three main steps:
1. Deploy the FSx for Lustre Container Storage Interface (CSI) driver
2. Create a Kubernetes `StorageClass` for FSx for Lustre
3. Create a persistent volume claim (PVC) that dynamically provisions an FSx for Lustre persistent volume (PV)

## Deploy FSx CSI Driver

The FSx Container Storage Interface driver provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of FSx for Lustre file systems.

Deploy the driver to your cluster:

```bash
kubectl apply -k "github.com/kubernetes-sigs/aws-fsx-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-0.8"
```

## Retrieve Security Group Information

Create a security group that allows TCP traffic on port 988 for FSx:

```bash
SECURITY_GROUP_ID=`aws eks describe-cluster --name ${EKS_CLUSTER_NAME} --query cluster.resourcesVpcConfig.clusterSecurityGroupId --region ${AWS_REGION}`
echo $SECURITY_GROUP_ID
```

## Retrieve Subnet Information

Get the subnet ID of the node group:

```bash
SUBNET_ID=`aws eks describe-nodegroup --cluster-name ${EKS_CLUSTER_NAME} --nodegroup-name "hpc" --query nodegroup.subnets --region ${AWS_REGION} --output text`
echo $SUBNET_ID
```

## Create Storage Class

Execute the following snippet to generate the storage class manifest (`fsx-storage-class.yaml`) and apply it to the cluster:

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

Apply the storage class:

```bash
kubectl apply -f ~/environment/fsx-storage-class.yaml
```

Verify that the storage class was created successfully:

```bash
kubectl get storageclass
```

You should see output similar to:

```console
NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
fsx-sc          fsx.csi.aws.com         Delete          Immediate              false                  9s
gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  16h
```

## Dynamically Provision FSx Volume

Create a persistent volume claim manifest:

```bash
cat > ~/environment/fsx-pvc.yaml << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fsx-pvc
  namespace: gromacs
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: fsx-sc
  resources:
    requests:
      storage: 1200Gi
EOF
```

Create the namespace and persistent volume claim:

```bash
kubectl create namespace gromacs
kubectl apply -f ~/environment/fsx-pvc.yaml
```

## Monitor FSx Volume Creation

Check the status of the persistent volume claim:

```bash
kubectl -n gromacs get pvc fsx-pvc
```

While the persistent volume is provisioning, you should see output like:

```text
NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
fsx-pvc   Pending                                      fsx-sc         2m39s
```

You can also describe the FSx file systems in your account to see the current status:

```bash
aws fsx describe-file-systems --region ${AWS_REGION}
```

You should see output showing the file system with a **Lifecycle** status of **CREATING**. The provisioning process takes approximately 6-8 minutes.

Example output:

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

> **ℹ️ Info:** To save time, you can proceed with the next sections of the workshop as they do not require the FSx volume to be available. Please return to this step and verify the persistent volume claim is bound before running the GROMACS MPI job.

## Verify Volume is Ready

When the FSx volume becomes available, the status of the persistent volume claim in Kubernetes will change to **Bound**:

```bash
kubectl -n gromacs get pvc fsx-pvc
```

Expected output when ready:

```text
NAME      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
fsx-pvc   Bound    pvc-159049a3-d25d-465f-ad7e-3e0799756fce   1200Gi     RWX            fsx-sc         7m45s
```

The **Bound** status indicates that the persistent volume claim is successfully bound to the persistent FSx for Lustre volume and is ready to be mounted by pods.

---
**Navigation:**
- Previous: [Validate Amazon EKS Cluster](03-validate-eks-cluster.md)
- Next: [Setup Monitoring](05-setup-monitoring.md)
- Up: [Module 1](README.md)