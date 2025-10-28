# Orchestrating Complex HPC and AI/ML Workflows on Kubernetes Using Flux and AWS

**SC25 Tutorial tut158s3**

Welcome to the workshop materials for "Orchestrating Complex HPC and AI/ML Workflows on Kubernetes Using Flux and AWS". This tutorial will teach you how Flux's hierarchical resource management and graph-based scheduling capabilities extend Kubernetes to support diverse workflows.

## 🚀 Getting Started

### Using VS Code for This Workshop

This workshop is designed to be completed using VS Code in your browser. All materials are provided as markdown files that you can view in VS Code's built-in preview mode.

#### How to Navigate These Materials

1. **Opening Files**: Click on any `.md` file in the VS Code file explorer
2. **Preview Mode**: Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) to open markdown preview
3. **Side-by-Side**: Press `Ctrl+K V` to open preview alongside the source
4. **Following Links**: Click any link in the preview to navigate between sections

#### VS Code Tips for This Workshop

- **Integrated Terminal**: Use `Ctrl+`` (backtick) to open the terminal
- **File Explorer**: Use `Ctrl+Shift+E` to focus on the file explorer
- **Quick Open**: Use `Ctrl+P` to quickly open files by name
- **Zoom**: Use `Ctrl++` and `Ctrl+-` to adjust text size

## 📚 Workshop Structure

This workshop progresses from foundational infrastructure concepts to advanced Flux capabilities, culminating in deploying MuMMI (Multiscale Machine-learned Modeling Infrastructure)—a scientific workflow exemplifying emerging complexity through combined large-scale simulations and machine learning.

### Workshop Modules

| Module | Topic | Estimated Time | Status |
|--------|-------|----------------|---------|
| [Workshop Setup](01-workshop-setup/README.md) | VS Code connection and navigation | 5-10 minutes | ✅ Available |
| [Module 1](02-module1-hpc-kubernetes/README.md) | HPC on Kubernetes (Amazon EKS) | 30 min - 1 hour | ✅ Available |
| [Module 2](03-module2-flux-lammps/README.md) | Flux and LAMMPS | TBD | 🚧 Coming Soon |
| [Module 3](04-module3-mummi-workflows/README.md) | MuMMI Workflows | TBD | 🚧 Coming Soon |

### Module 1 Detailed Contents

- Install Tools (eksctl, kubectl, helm)
- Create and validate EKS cluster
- Create persistent volume with FSx for Lustre
- Setup monitoring
- Deploy MPI Operator
- Run GROMACS MPI job
- Cleanup and optional scale-out

## 🏗️ Architecture Overview

![Flux+EKS Architecture](images/aws-eks/eks-hpc-architecture.png)

The workshop demonstrates how to orchestrate complex workflows using:
- **Amazon EKS**: Managed Kubernetes service
- **Flux**: Advanced job scheduling and resource management
- **FSx for Lustre**: High-performance parallel file system
- **GROMACS**: Molecular dynamics simulation software
- **MuMMI**: Multiscale machine learning infrastructure

## 🎯 Learning Objectives

By the end of this workshop, you will:

1. **Understand** how to deploy and manage HPC workloads on Kubernetes
2. **Learn** Flux's hierarchical resource management capabilities
3. **Experience** running real scientific applications (GROMACS, LAMMPS)
4. **Explore** integration of HPC simulations with machine learning workflows
5. **Gain** hands-on experience with AWS services for HPC

## 📋 Prerequisites

- Basic familiarity with containers and Kubernetes concepts
- Understanding of command-line interfaces
- AWS account access (provided during the workshop)
- No prior experience with Flux or HPC required

## 🚦 Getting Started

Ready to begin? Start with the [Workshop Setup](01-workshop-setup/README.md) to connect to your development environment and learn how to navigate these materials.

## 📞 Support

If you encounter issues during the workshop:

1. Check the troubleshooting sections in each module
2. Ask questions in the workshop chat or raise your hand
3. Consult the workshop instructors

## 📄 Additional Resources

- [Flux Documentation](https://flux-framework.readthedocs.io/)
- [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GROMACS Documentation](https://manual.gromacs.org/)

---

**Ready to start?** → [Begin with Workshop Setup](01-workshop-setup/README.md)