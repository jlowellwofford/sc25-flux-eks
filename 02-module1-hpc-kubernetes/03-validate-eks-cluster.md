# Validate Amazon EKS Cluster

[Home](../README.md) > [Module 1](README.md) > Validate EKS Cluster

## Overview

In this section, you will validate the newly created Amazon EKS cluster to ensure it's properly configured and ready for HPC workloads.

## 1. Validate Amazon EKS cluster creation

To validate that the cluster was provisioned successfully and is ready for use, you will list the Kubernetes nodes by executing the following command:

```bash
kubectl get nodes -o wide
```

You should see a node listed similar to the one shown below:

```
NAME                             STATUS   ROLES    AGE     VERSION
ip-192-168-86-187.ec2.internal   Ready    <none>   4m54s   v1.21.14-eks-ba74326
```

## Troubleshooting

> **⚠️ Warning:** If you encounter connection issues, follow the troubleshooting steps below.

- If the cluster creation fails with an ExpiredToken error (`ExpiredToken: The security token included in the request is expired`), ensure you have properly configured your AWS credentials in the VS Code terminal environment.

- If your kubectl client is unable to connect to the cluster, you may try to update the connection information by executing the command below, then try validating the cluster again.

Use the command below, only **if you were unable to connect** to the cluster:

```bash
aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
```

---
**Navigation:**
- Previous: [Create Amazon EKS Cluster](02-create-eks-cluster.md)
- Next: [Create Persistent Volume](04-create-persistent-volume.md)
- Up: [Module 1](README.md)