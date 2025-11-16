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

---
**Navigation:**
- Back to: [Module 1: HPC on Kubernetes](../01-module1-hpc-kubernetes/README.md)
