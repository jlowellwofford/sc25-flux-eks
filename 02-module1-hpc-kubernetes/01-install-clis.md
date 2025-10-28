# Install CLIs

[Home](../README.md) > [Module 1](README.md) > Install CLIs

## Overview

In this section, you will install `eksctl`, `kubectl`, and `helm` - the essential command-line tools needed for working with Amazon EKS and Kubernetes.

## Install eksctl

`eksctl` is a simple CLI tool for creating and managing Amazon EKS clusters. It is written in [Go](https://go.dev/), uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/), and was created by [Weaveworks](https://www.weave.works/). Learn more by visiting [https://eksctl.io](https://eksctl.io).

In your VS Code integrated terminal, paste the following commands to install `eksctl`:

```bash
cd ~/environment
curl --location "https://github.com/weaveworks/eksctl/releases/download/v0.112.0/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

## Install kubectl

`kubectl` is a command line utility for interacting with the Kubernetes API. It allows you to run commands against Kubernetes clusters, deploy applications, inspect and manage cluster resources, and view logs. For more information see the [reference documentation](https://kubernetes.io/docs/reference/kubectl/).

In your VS Code integrated terminal, paste the following commands to install `kubectl`:

```bash
curl -Lo kubectl https://dl.k8s.io/release/v1.21.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
kubectl version --client --short
```

## Install helm

`helm` is a package manager for Kubernetes. It allows easy deployment of software from a helm repository to your cluster. Learn more at [helm](https://helm.sh).

To install helm, in your VS Code integrated terminal execute the following command:

```bash
curl -L https://git.io/get_helm.sh | bash -s -- --version v3.8.2
```

## Verification

You now have the tools needed to complete the HPC on Kubernetes module. You can verify the installations by running:

```bash
eksctl version
kubectl version --client --short
helm version --short
```

All three commands should return version information without errors.

---
**Navigation:**
- Previous: [Module 1 Overview](README.md)
- Next: [Create Amazon EKS Cluster](02-create-eks-cluster.md)
- Up: [Module 1](README.md)