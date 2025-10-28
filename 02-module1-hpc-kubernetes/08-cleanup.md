# Cleanup and Conclusion

[Home](../README.md) > [Module 1](README.md) > Cleanup

## Overview

In this section, you will delete the FSx for Lustre file system and the EKS cluster that you created for this lab.

## 1. Delete resources belonging to the namespace

Execute the following command to remove all Kubernetes resources that were created in the gromacs namespace:

```bash
kubectl delete namespace gromacs
```

When the persistent volume claim is deleted, the FSx for Lustre volume will automatically be deleted as well.

## 2. Delete EKS cluster

To delete the cluster, execute:

```bash
eksctl delete cluster -f ~/environment/eks-hpc.yaml
```

This command will delete the EKS cluster through AWS CloudFormation. The process will take several minutes to complete.

## Conclusion

Congratulations!

You have provisioned a Kubernetes cluster and ran an HPC application on it, using Kubeflow MPI Operator.

The experience obtained through this lab can be used when running your own HPC jobs on Kubernetes!

Read the [next section](09-scale-out-optional.md) to learn about scaling out this architecture with EFA-enabled nodes on a multi-node cluster in your own AWS account.

---
**Navigation:**
- Previous: [Run GROMACS MPI Job](07-run-gromacs-mpi.md)
- Next: [Scale Out (Optional)](09-scale-out-optional.md)
- Up: [Module 1](README.md)