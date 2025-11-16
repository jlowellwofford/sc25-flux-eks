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

| Time | Topic | Content |
|------|-------|---------|
| 1:30 PM - 1:35 PM | Welcome & Introduction | Slides and [Workshop Setup](00-workshop-setup/README.md) |
| 1:35 PM - 2:00 PM | Introduction to Amazon EKS | Slides and [Module 1](01-module1-hpc-kubernetes/README.md) |
| 2:00 PM - 3:00 PM | Introduction to Flux Framework | Slides and [Module 2](02-module2-flux-lammps/README.md) |
| 3:00 PM - 3:30 PM | Break | |
| 3:30 PM - 4:45 PM | Workflows with Flux on EKS (MuMMI Workflows) | Slides and [Module 3](03-module3-mummi-workflows/README.md) |
| 4:45 PM - 5:00 PM | Closing and Q&A | | 


## 🏗️ Workshop Overview

The workshop demonstrates how to orchestrate complex workflows using:
- **Amazon EKS**: Managed Kubernetes service
- **Flux**: Advanced job scheduling and resource management
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

- Basic familiarity with containers and Kubernetes concepts (Don't worry! Module 1 will also bootstrap your knowledge)
- Understanding of command-line interfaces
- AWS account access (provided during the workshop)
- No prior experience with Flux or HPC required

## 🚦 Getting Started

Ready to begin? Start with the [Workshop Setup](01-workshop-setup/README.md) to connect to your development environment and learn how to navigate these materials.

## 📞 Support

If you encounter issues during the workshop:

1. Check the troubleshooting sections in each module
2. Ask questions in the workshop chat or raise your hand (remember to ask questions on mic for livestream)
3. Consult the workshop instructors

## 📄 Additional Resources

- [Flux Documentation](https://flux-framework.readthedocs.io/)
- [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GROMACS Documentation](https://manual.gromacs.org/)

---

**Ready to start?** → [Begin with Workshop Setup](00-workshop-setup/README.md)
