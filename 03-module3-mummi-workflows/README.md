# Module 3: MuMMI Workflows

[Home](../README.md) > Module 3: MuMMI Workflows

## Overview

This module focuses on deploying MuMMI (Multiscale Machine-learned Modeling Infrastructure), a scientific workflow that combines large-scale simulations with machine learning to exemplify emerging complexity in HPC and AI/ML workflows.

## Contents

### 1. MuMMI Components

- [The MLRunner component](#the-mlrunner-component)
- [Simulation steps](#simulation-steps)
- [MuMMI with MPI](#mummi-with-mpi)

### 2. MuMMI Advanced

- [MuMMI as a State Machine](#mummi-as-a-state-machine)

## Prerequisites

- Completion of Modules 1 and 2
- Understanding of machine learning workflows
- Familiarity with scientific computing pipelines

## Estimated Time

45 minutes

## Tutorial

You should start from a 2 node cluster that already has the Flux Operator installed. For this example, MuMMI is made up of 3 components.

1. The machine learning simulation "mlrunner" that samples from a latent space.
2. The setup step "createsims" that sets up a simulation
3. The simulation step "cganalysis"

The final step, cganalysis, can be run with or without MPI.

### The MLRunner Component

Let's create a single MLRunner component. Apply the mlrunner custom resource definition (CRD) to create and run a single step.

```bash
kubectl apply -f ./configs/01-mlrunner-minicluster.yaml
```

Once the container transitions from Init to PodInitiailizing to Running, you can inspect logs. The pull will take about 3 minutes, and the full run to a Completed state is 1.5 minutes.

```bash
kubectl logs mlrunner-0-xxxx -f
```

You'll see the step run, and on completions print timings and show the output directory.

<details>

<summary>mlrunner output</summary>

```console
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/.DS_Store
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/CG_pos_data_summary_pos_dis_C1_v1.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/CG_pos_data_summary_pos_dis_mini_mummi_prerun.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/100_worst_patches.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/actual_positions1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/avg_error_per_bead_large_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/avg_error_per_bead_medium_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/avg_error_per_bead_small_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/difference_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/distribution_rmsd_val_cg.pdf
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/distribution_rmsd_val_ras.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/model_history_mean.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/pca_validation.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/pca_validationxy.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/pca_validationxz.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/pca_validationyz.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_0_large_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_0_medium_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_0_small_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_1_large_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_1_medium_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/positions_1_small_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/predicted_positions1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot0_large_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot0_medium_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot0_small_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot1_large_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot1_medium_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-03-40-41/residual_plot1_small_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/100_worst_patches.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/actual_positions1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/avg_error_per_bead_large_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/avg_error_per_bead_medium_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/avg_error_per_bead_small_cg.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/difference_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/distribution_rmsd_val_cg.pdf
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/distribution_rmsd_val_ras.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/model_history_mean.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/pca_validation.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/pca_validationxy.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/pca_validationxz.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/pca_validationyz.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_0_large_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_0_medium_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_0_small_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_1_large_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_1_medium_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/positions_1_small_cg.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_distance_matrix1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions0_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions0_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions0_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions1_large_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions1_medium_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/predicted_positions1_small_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot0_large_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot0_medium_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot0_small_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot1_large_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot1_medium_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/residual_plot1_small_pos_cg.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/analysis-2024-10-02-11-31-08/tsne_validation.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/checkpoints/
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/config.yaml
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/model.pth
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/model_summary.txt
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r0.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r0.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r1.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r1.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r2.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r2.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r3.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r3.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r4.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r4.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r5.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r5.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r6.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r6.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r7.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/model_history_r7.png
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/training_files.csv
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_all.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_all_plus_pred.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r0.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r1.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r2.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r3.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r4.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r5.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r6.npz
model-protein_latent_space-mini_mummi_ls-c2289_z32-t2024-10-01-23-33-17_h443704/training/validation_data_r7.npz
/workdir
Running with 64 cpu
> Initialized MuMMI
	> MuMMI_ROOT: (/opt/clones/mummi-ras)
	> MuMMI_Resources: (/opt/clones/mummi_resources)
	> MuMMI_Specs: (/opt/clones/mummi-ras/specs)

> Creating MuMMI root hierarchy at (/opt/clones/mummi-ras)

mummi-ml start --jobid structure_000001 --workspace=/opt/clones/mummi-ras/mlserver --outdir=/workdir/tmp --tag mlrunner --plain-http --encoder-model /opt/clones/mummi_resources/ml/chonky-model/CG_pos_data_summary_pos_dis_C1_v1.npz --ml-outdir=/opt/clones/mummi-ras/mlserver --resources martini3-validator --complex=ras-rbdcrd-ref-CG.gro
/pixi-env/.pixi/envs/default/lib/python3.11/site-packages/Bio/Application/__init__.py:39: BiopythonDeprecationWarning: The Bio.Application modules and modules relying on it have been deprecated.

Due to the on going maintenance burden of keeping command line application
wrappers up to date, we have decided to deprecate and eventually remove these
modules.

We instead now recommend building your command line and invoking it directly
with the subprocess module.
  warnings.warn(
INFO:mummi_operator.ml.runner:ML Server launched on host: mlrunner-0
INFO:mummi_operator.ml.runner:> Initializing MuMMI ML Runner
INFO:mummi_operator.ml.runner:  > Mini-Mummi                 True
INFO:mummi_operator.ml.runner:  > Sampler
INFO:mummi_operator.ml.runner:    > Interpolator             ot_feedback
INFO:mummi_operator.ml.runner:    > Run with feedback        False
INFO:mummi_operator.ml.runner:    > Createsims Feedback DB   /opt/clones/mummi-ras/mlserver/feedback/db-feedback-sampling.npz
INFO:mummi_operator.ml.runner:    > CG frames Feedback DB    /opt/clones/mummi-ras/mlserver/feedback/db-feedback-frames.npz
INFO:mummi_operator.ml.runner:  > Generator
INFO:mummi_operator.ml.runner:    > Encoder                  /opt/clones/mummi_resources/ml/chonky-model
INFO:mummi_operator.ml.runner:  > Validator                   CGValidator
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder: > Using torch v2.0.1 (/pixi-env/.pixi/envs/default/lib/python3.11/site-packages/torch/__init__.py)
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:> Initialization of generator with:
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:  > encoder      = /opt/clones/mummi_resources/ml/chonky-model
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:  > dimensions   = ((2289,), (32,))
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:  > #beads       = 763
INFO:mummi_ras.ml.autoencoders.mini.model.model_torch:Initializing (model-protein_latent_space-mini_mummi_ls-c2289_z32-0)
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder: > Device used : cpu
INFO:mummi_ras.ml.autoencoders.mini.model.model_torch:loading model (/opt/clones/mummi_resources/ml/chonky-model/model.pth)
INFO:mummi_ras.ml.autoencoders.mini.model.model_torch:loading model standardization file (/opt/clones/mummi_resources/ml/chonky-model/CG_pos_data_summary_pos_dis_C1_v1.npz)
INFO:mummi_operator.ml.validator:> Initialization of validator with
INFO:mummi_operator.ml.validator:  > iteration_path        = /workdir/tmp
INFO:mummi_operator.ml.validator:  > resource_path         = /opt/clones/mummi_resources/martini3-validator-resources
INFO:mummi_operator.ml.validator:  > complex_name          = ras-rbdcrd-ref-CG.gro
INFO:mummi_operator.ml.validator:  > maximum force         = [-1000000.0, 1000000.0]
INFO:mummi_operator.ml.validator:  > potential energy      = [-10000000.0, 10000000.0]
INFO:mummi_operator.ml.validator:  > cleanup               = True
INFO:mummi_operator.ml.validator:  > healing               = True
INFO:mummi_operator.ml.validator:  > logical cores         = 64
INFO:mummi_operator.ml.validator:  > available cores       = 62
INFO:mummi_operator.ml.runner:All feedback is deactivated for this run.
INFO:mummi_operator.ml.runner:Training data /opt/clones/mummi_resources/ml/chonky-model/training => 1 files
WARNING:mummi_operator.ml.runner:Could not load pre-computed interpolator. Computing interpolator
INFO:mummi_ras.ml.samplers.interpolators.feedback_interpolator:creating all states
DEBUG:mummi_ras.ml.samplers.interpolators.feedback_interpolator:Doing assert
INFO:mummi_ras.ml.samplers.interpolators.feedback_interpolator:compute_optimal_transport_pairwise with source=(222, 32) / target=(222, 32)
INFO:mummi_ras.ml.samplers.interpolators.feedback_interpolator:ot.emd with a=(222,) / b=(222,) and M=(222, 222)
INFO:mummi_operator.ml.runner:Interpolator ot_feedback created in 2.295 seconds for 444 LS points
INFO:mummi_operator.ml.runner:Sampled 1 in 4.291534423828125e-06 seconds
INFO:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:De-standardizing (1, 763, 3) predicted_positions
DEBUG:mummi_ras.ml.autoencoders.mini.full_dense_autoencoder:new_positions= (1, 763, 3) from ls_coords = (1, 32)
INFO:mummi_operator.ml.runner:Write patches in /opt/clones/mummi-ras/mlserver/structure_000001
INFO:mummi_operator.ml.runner:Writing /opt/clones/mummi-ras/mlserver/structure_000001/structure_000001_000000000000.npz
DEBUG:mummi_operator.ml.runner:generated structures done. new_positions = (1, 763, 3)
DEBUG:mummi_operator.ml.validator:Switched dir to fullPathDir /workdir/tmp/structure_000001_000000000000 (/workdir/tmp/structure_000001_000000000000)
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomnames object at 0xfffeeba047d0> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomids object at 0xfffeec0f8f10> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resids object at 0xfffeeb4eb9d0> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resnums object at 0xfffeef9a2910> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resnames object at 0xfffeece31d50> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Segids object at 0xfffeeb4eba50> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomindices object at 0xfffeece43e90> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resindices object at 0xfffeeb4ebb90> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Segindices object at 0xfffeeb4ebbd0> to topology
DEBUG:MDAnalysis.core.universe:Universe.load_new(): loading /opt/clones/mummi_resources/martini3-validator-resources/ras-rbdcrd-ref-CG.gro...
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomtypes object at 0xfffeece31890> to topology
INFO:MDAnalysis.core.universe:attribute types has been guessed successfully.
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Masses object at 0xfffeec51f350> to topology
INFO:MDAnalysis.core.universe:attribute masses has been guessed successfully.
INFO:mummi_operator.ml.validator:Run GROMACS minimization in dir /workdir/tmp/structure_000001_000000000000/structure_000001_000000000000
DEBUG:mummi_operator.ml.validator:minimization results for structure_000001_000000000000: potential energy of -4492.6133 and maximum force of 3711.5876
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomnames object at 0xfffeec4a34d0> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomids object at 0xfffeec4a3590> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resids object at 0xfffeeb3ade90> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resnums object at 0xfffeeb3aded0> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resnames object at 0xfffeeb3adf10> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Segids object at 0xfffeeb3adf50> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomindices object at 0xfffeeb3ae090> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Resindices object at 0xfffeeb3ae0d0> to topology
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Segindices object at 0xfffeeb3ae110> to topology
DEBUG:MDAnalysis.core.universe:Universe.load_new(): loading structure_000001_000000000000-em_whole.gro...
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Atomtypes object at 0xfffeeb4e8d90> to topology
INFO:MDAnalysis.core.universe:attribute types has been guessed successfully.
DEBUG:MDAnalysis.core.universe:_process_attr: Adding <MDAnalysis.core.topologyattrs.Masses object at 0xfffeec111890> to topology
INFO:MDAnalysis.core.universe:attribute masses has been guessed successfully.
INFO:mummi_operator.ml.validator:Structure structure_000001_000000000000 VALID (potential energy of -4492.6133, maximum force of 3711.5876) in 1.335 seconds
INFO:mummi_operator.ml.validator:Validator returned with 1 elements and took: 1.3349963410000214 sec (0.7490637175440755 sample/sec)
INFO:mummi_operator.ml.validator:Found 1 valid patches out of 1 patches
DEBUG:mummi_operator.ml.runner:mlrunner structure_000001 => valid structures=['/workdir/tmp/structure_000001_000000000000.gro']

> Initializing MuMMI (/opt/clones/mummi-core/mummi_core)
> Initialized MuMMI
	> MuMMI_ROOT: (/opt/clones/mummi-ras)
	> MuMMI_Resources: (/opt/clones/mummi_resources)
	> MuMMI_Specs: (/opt/clones/mummi-ras/specs)

> Creating MuMMI root hierarchy at (/opt/clones/mummi-ras)

(1, 763, 3)
=== times
{"created_interpolator_seconds": 2.295388698577881, "sampled_structure_000001": 4.291534423828125e-06}
===
=== timestamps
{"create_sets_start": 1753724498.4369469, "create_sets_complete": 1753724499.3585706, "generator_decode_structure_000001_start": 1753724500.8189955, "generator_decode_structure_000001_complete": 1753724500.8797946, "validate_structure_000001_start": 1753724500.8807309, "validate_structure_000001_complete": 1753724502.216927}
===
mlrunner output:
/workdir/tmp/
├── master_iter1.npz
├── structure_000001_000000000000.gro
└── table_all_predictions.npz
```

</details>

When you are done, cleanup.

```bash
kubectl delete -f ./configs/01-mlrunner-minicluster.yaml
```

### Simulation Steps

The next two steps, `createsims` and `cganalysis`, take longer (you can run them if you are interested). Create these *both* at the same time:

```bash
kubectl apply -f ./configs/02-createsims-minicluster.yaml 
kubectl apply -f ./configs/03-cganalysis-minicluster.yaml
```

Once both are running, you can look at output and shell into the container to look around.  We have included both outputs here for inspection.

<details>

<summary>createsims output</summary>

```console
Defaulted container "createsims" out of: createsims, flux-view (init)
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -153.000000
; Total charge: -147.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            47
POPE            35
DLPE           103
SSM             68
PAPS           101
SAP6            13
CHOL           155
W            38456
NA             573
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158511.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

GROMACS reminds you: "I'm a strong believer that ignorance is important in science. If you know too much, you start seeing reasons why things won't work. That's why its important to change your field to collect more ignorance." (Sydney Brenner)

Setting the LD random seed to 1993203583

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40747      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54805 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54067 elements
Group    12 (          Other) has 54066 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   588 elements
Group    21 (           DLPE) has  1704 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3447 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1313 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38456 elements
Group    28 (            ION) has   998 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54805 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.1#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "I'm a strong believer that ignorance is important in science. If you know too much, you start seeing reasons why things won't work. That's why its important to change your field to collect more ignorance." (Sydney Brenner)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -157.000000
; Total charge: -151.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            47
POPE            34
DLPE           103
SSM             68
PAPS           101
SAP6            14
CHOL           155
W            38469
NA             577
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158577.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.1#

GROMACS reminds you: "It Doesn't Have to Be Tip Top" (Pulp Fiction)

Setting the LD random seed to -4849922

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40764      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54828 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54090 elements
Group    12 (          Other) has 54089 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1704 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3447 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1313 elements
Group    26 (           SAP6) has   252 elements
Group    27 (              W) has 38469 elements
Group    28 (            ION) has  1002 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54828 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.3#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "error: too many template-parameter-lists" (g++)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -154.000000
; Total charge: -148.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            47
POPE            35
DLPE           101
SSM             68
PAPS           102
SAP6            13
CHOL           156
W            38468
NA             574
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158529.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.2#

GROMACS reminds you: "Inventions have long since reached their limit, and I see no hope for further development." (Julius Sextus Frontinus, 1st century A.D.)

Setting the LD random seed to -134252941

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40760      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54816 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54078 elements
Group    12 (          Other) has 54077 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   588 elements
Group    21 (           DLPE) has  1680 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3456 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1326 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38468 elements
Group    28 (            ION) has   999 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54816 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.5#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "gmx fellowship-writing -g grant_name -s protein_structure_involved -o output -m method_used -p list_of_pi" (Tanadet Pipatpolkai, while discussing new features for GROMACS)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -155.000000
; Total charge: -149.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            47
POPE            34
DLPE           104
SSM             68
PAPS           103
SAP6            13
CHOL           153
W            38476
NA             575
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158631.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.3#

GROMACS reminds you: "Here's Another Useful Quote" (S. Boot)

Setting the LD random seed to -3361845

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40769      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54835 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54097 elements
Group    12 (          Other) has 54096 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1716 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3429 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1339 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38476 elements
Group    28 (            ION) has  1000 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54835 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.7#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "But I always say, one's company, two's a crowd, and three's a party." (Andy Warhol)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -153.000000
; Total charge: -147.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            89
PAPC            47
POPE            34
DLPE           103
SSM             68
PAPS           101
SAP6            13
CHOL           155
W            38478
NA             573
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158577.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.4#

GROMACS reminds you: "It's Against the Rules" (Pulp Fiction)

Setting the LD random seed to -677777673

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40769      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54827 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54089 elements
Group    12 (          Other) has 54088 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1704 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3447 elements
Group    24 (           POPC) has  1068 elements
Group    25 (           PAPS) has  1313 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38478 elements
Group    28 (            ION) has   998 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54827 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.9#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "This work contains many things which are new and interesting. Unfortunately, everything that is new is not interesting, and everything which is interesting, is not new." (Lev Landau)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -155.000000
; Total charge: -149.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            48
POPE            34
DLPE           102
SSM             69
PAPS           103
SAP6            13
CHOL           153
W            38477
NA             575
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158637.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.5#

GROMACS reminds you: "This May Come As a Shock" (F. Black)

Setting the LD random seed to 2146285412

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40770      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54837 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54099 elements
Group    12 (          Other) has 54098 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1651 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1692 elements
Group    22 (            SSM) has  2712 elements
Group    23 (           CHOL) has  3429 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1339 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38477 elements
Group    28 (            ION) has  1000 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54837 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.11#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "Should we force science down the throats of those that have no taste for it? Is it our duty to drag them kicking and screaming into the twenty-first century? I am afraid that it is." (George Porter)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -154.000000
; Total charge: -148.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            47
POPE            34
DLPE           102
SSM             69
PAPS           102
SAP6            13
CHOL           155
W            38473
NA             574
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158568.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.6#

GROMACS reminds you: "The road to openness is paved with git commits" (Vedran Miletic)

Setting the LD random seed to -788832268

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40765      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54824 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54086 elements
Group    12 (          Other) has 54085 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1638 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1692 elements
Group    22 (            SSM) has  2712 elements
Group    23 (           CHOL) has  3447 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1326 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38473 elements
Group    28 (            ION) has   999 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54824 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.13#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "Energy is a very subtle concept. It is very, very difficult to get right." (Richard Feynman)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -154.000000
; Total charge: -148.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            89
PAPC            49
POPE            34
DLPE           101
SSM             68
PAPS           102
SAP6            13
CHOL           154
W            38472
NA             574
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158595.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.7#

GROMACS reminds you: "Beware of bugs in the above code; I have only proved it correct, not tried it." (Donald Knuth)

Setting the LD random seed to 1676207981

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40764      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54828 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54090 elements
Group    12 (          Other) has 54089 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1664 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1680 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3438 elements
Group    24 (           POPC) has  1068 elements
Group    25 (           PAPS) has  1326 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38472 elements
Group    28 (            ION) has   999 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54828 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.15#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "Computers are like humans - they do everything except think." (John von Neumann)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -153.000000
; Total charge: -147.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            49
POPE            34
DLPE           102
SSM             69
PAPS           101
SAP6            13
CHOL           154
W            38472
NA             573
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158589.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.8#

GROMACS reminds you: "If You See Me Getting High, Knock Me Down" (Red Hot Chili Peppers)

Setting the LD random seed to 2144881143

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40763      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54826 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54088 elements
Group    12 (          Other) has 54087 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1664 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1692 elements
Group    22 (            SSM) has  2712 elements
Group    23 (           CHOL) has  3438 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1313 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38472 elements
Group    28 (            ION) has   998 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54826 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.17#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "If Life Seems Jolly Rotten, There's Something You've Forgotten !" (Monty Python)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
; X: 20.000 (26 lipids) Y: 20.000 (26 lipids)
; 676 lipids in upper leaflet, 675 lipids in lower leaflet
; Charge of protein: 6.000000
; Charge of membrane: -153.000000
; Total charge: -147.000000
Protein          1
POPX           159
PAPC            79
POPE            14
DLPE            39
SSM            157
CHOL           228
POPC            88
PAPC            48
POPE            34
DLPE           103
SSM             68
PAPS           101
SAP6            13
CHOL           155
W            38476
NA             573
CL             425
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water.gro -r lipids-water.gro -f martini_v2.x_new-rf-em.mdp -p system.top -o topol.tpr -maxwarn 5

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-em.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0

Number of degrees of freedom in T-Coupling group rest is 158574.00
The integrator does not provide a ensemble temperature, there is no system ensemble temperature

NOTE 2 [file martini_v2.x_new-rf-em.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.9#

GROMACS reminds you: ""What are the biological implications of your research?" - "Well, I simulate water." " (Petter Johansson)

Setting the LD random seed to -1163526

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites
Analysing residue names:
There are:   311    Protein residues
There are: 40767      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

This run will generate roughly 5 Mb of data
               :-) GROMACS - gmx trjconv, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx trjconv -f lipids-water-em.gro -o lipids-water-em.gro -pbc mol -s topol.tpr

Will write gro: Coordinate file in Gromos-87 format
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Reading file topol.tpr, VERSION 2024.5-conda_forge (single precision)
Group     0 (         System) has 54826 elements
Group     1 (        Protein) has   738 elements
Group     2 (      Protein-H) has   738 elements
Group     3 (        C-alpha) has     0 elements
Group     4 (       Backbone) has     0 elements
Group     5 (      MainChain) has     0 elements
Group     6 (   MainChain+Cb) has     0 elements
Group     7 (    MainChain+H) has     0 elements
Group     8 (      SideChain) has   738 elements
Group     9 (    SideChain-H) has   738 elements
Group    10 (    Prot-Masses) has   738 elements
Group    11 (    non-Protein) has 54088 elements
Group    12 (          Other) has 54087 elements
Group    13 (            CYF) has     8 elements
Group    14 (            GTP) has    11 elements
Group    15 (             MG) has     1 elements
Group    16 (            CGW) has     3 elements
Group    17 (            ZN2) has     2 elements
Group    18 (           POPX) has  1908 elements
Group    19 (           PAPC) has  1651 elements
Group    20 (           POPE) has   576 elements
Group    21 (           DLPE) has  1704 elements
Group    22 (            SSM) has  2700 elements
Group    23 (           CHOL) has  3447 elements
Group    24 (           POPC) has  1056 elements
Group    25 (           PAPS) has  1313 elements
Group    26 (           SAP6) has   234 elements
Group    27 (              W) has 38476 elements
Group    28 (            ION) has   998 elements
Group    29 (            Ion) has     1 elements
Select a group: Reading frames from gro file 'lipids-sim', 54826 atoms.
Reading frame       0 time    0.000   
Precision of lipids-water-em.gro is 0.001 (nm)

Back Off! I just backed up lipids-water-em.gro to ./#lipids-water-em.gro.19#
Last frame          0 time    0.000   
 ->  frame      0 time    0.000      
Last written: frame      0 time    0.000


GROMACS reminds you: "History has expired" (PubMed Central)

Note that major changes are planned in future for trjconv, to improve usability and utility.
Select group for output
Selected 0: 'System'
               :-) GROMACS - gmx make_ndx, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx make_ndx -f lipids-water-em.gro -o index.ndx


Reading structure file
Going to read 0 old index file(s)
Analysing residue names:
There are:   311    Protein residues
There are: 40767      Other residues
There are:     1        Ion residues
Analysing Protein...
Analysing residues not classified as Protein/DNA/RNA/Water and splitting into groups...

  0 System              : 54826 atoms
  1 Protein             :   738 atoms
  2 Protein-H           :   738 atoms
  3 C-alpha             :     0 atoms
  4 Backbone            :     0 atoms
  5 MainChain           :     0 atoms
  6 MainChain+Cb        :     0 atoms
  7 MainChain+H         :     0 atoms
  8 SideChain           :   738 atoms
  9 SideChain-H         :   738 atoms
 10 Prot-Masses         :   738 atoms
 11 non-Protein         : 54088 atoms
 12 Other               : 54087 atoms
 13 CYF                 :     8 atoms
 14 GTP                 :    11 atoms
 15 MG                  :     1 atoms
 16 CGW                 :     3 atoms
 17 ZN2                 :     2 atoms
 18 POPX                :  1908 atoms
 19 PAPC                :  1651 atoms
 20 POPE                :   576 atoms
 21 DLPE                :  1704 atoms
 22 SSM                 :  2700 atoms
 23 CHOL                :  3447 atoms
 24 POPC                :  1056 atoms
 25 PAPS                :  1313 atoms
 26 SAP6                :   234 atoms
 27 W                   : 38476 atoms
 28 ION                 :   998 atoms
 29 Ion                 :     1 atoms

 nr : group      '!': not  'name' nr name   'splitch' nr    Enter: list groups
 'a': atom       '&': and  'del' nr         'splitres' nr   'l': list residues
 't': atom type  '|': or   'keep' nr        'splitat' nr    'h': help
 'r': residue              'res' nr         'chain' char
 "name": group             'case': case sensitive           'q': save and quit
 'ri': residue index

> 
Removed group 1 'Protein'
Removed group 2 'Protein-H'
Removed group 3 'C-alpha'
Removed group 4 'Backbone'
Removed group 5 'MainChain'
Removed group 6 'MainChain+Cb'
Removed group 7 'MainChain+H'
Removed group 8 'SideChain'
Removed group 9 'SideChain-H'
Removed group 10 'Prot-Masses'
Removed group 11 'non-Protein'
Removed group 12 'Other'
Removed group 13 'CYF'
Removed group 14 'GTP'
Removed group 15 'MG'
Removed group 16 'CGW'
Removed group 17 'ZN2'
Removed group 18 'POPX'
Removed group 19 'PAPC'
Removed group 20 'POPE'
Removed group 21 'DLPE'
Removed group 22 'SSM'
Removed group 23 'CHOL'
Removed group 24 'POPC'
Removed group 25 'PAPS'
Removed group 26 'SAP6'
Removed group 27 'W'
Removed group 28 'ION'
Removed group 29 'Ion'
Group 30 does not exist
Group 31 does not exist
Group 32 does not exist
Group 33 does not exist
Group 34 does not exist
Group 35 does not exist
Group 36 does not exist
Group 37 does not exist
Group 38 does not exist
Group 39 does not exist
Group 40 does not exist
Group 41 does not exist
Group 42 does not exist
Group 43 does not exist
Group 44 does not exist
Group 45 does not exist
Group 46 does not exist
Group 47 does not exist
Group 48 does not exist
Group 49 does not exist
Group 50 does not exist
Group 51 does not exist
Group 52 does not exist
Group 53 does not exist
Group 54 does not exist
Group 55 does not exist
Group 56 does not exist
Group 57 does not exist
Group 58 does not exist
Group 59 does not exist
Group 60 does not exist
Group 61 does not exist
Group 62 does not exist
Group 63 does not exist
Group 64 does not exist
Group 65 does not exist
Group 66 does not exist
Group 67 does not exist
Group 68 does not exist
Group 69 does not exist
Group 70 does not exist
Group 71 does not exist
Group 72 does not exist
Group 73 does not exist
Group 74 does not exist
Group 75 does not exist
Group 76 does not exist
Group 77 does not exist
Group 78 does not exist
Group 79 does not exist
Group 80 does not exist
Group 81 does not exist
Group 82 does not exist
Group 83 does not exist
Group 84 does not exist
Group 85 does not exist
Group 86 does not exist
Group 87 does not exist
Group 88 does not exist
Group 89 does not exist
Group 90 does not exist
Group 91 does not exist
Group 92 does not exist
Group 93 does not exist

GROMACS reminds you: "History has expired" (PubMed Central)

Group 94 does not exist
Group 95 does not exist
Group 96 does not exist
Group 97 does not exist
Group 98 does not exist
Group 99 does not exist
Group 100 does not exist
Group 101 does not exist
Group 102 does not exist
Group 103 does not exist
Group 104 does not exist
Group 105 does not exist
Group 106 does not exist
Group 107 does not exist
Group 108 does not exist
Group 109 does not exist
Group 110 does not exist
Group 111 does not exist
Group 112 does not exist
Group 113 does not exist
Group 114 does not exist
Group 115 does not exist
Group 116 does not exist
Group 117 does not exist
Group 118 does not exist
Group 119 does not exist
Group 120 does not exist
Group 121 does not exist
Group 122 does not exist
Group 123 does not exist
Group 124 does not exist
Group 125 does not exist
Group 126 does not exist
Group 127 does not exist
Group 128 does not exist
Group 129 does not exist
Group 130 does not exist
Group 131 does not exist
Group 132 does not exist
Group 133 does not exist
Group 134 does not exist
Group 135 does not exist
Group 136 does not exist
Group 137 does not exist
Group 138 does not exist
Group 139 does not exist
Group 140 does not exist
Group 141 does not exist
Group 142 does not exist
Group 143 does not exist
Group 144 does not exist
Group 145 does not exist
Group 146 does not exist
Group 147 does not exist
Group 148 does not exist
Group 149 does not exist
Group 150 does not exist
Group 151 does not exist
Group 152 does not exist
Group 153 does not exist
Group 154 does not exist
Group 155 does not exist
Group 156 does not exist
Group 157 does not exist
Group 158 does not exist
Group 159 does not exist
Group 160 does not exist
Group 161 does not exist
Group 162 does not exist
Group 163 does not exist
Group 164 does not exist
Group 165 does not exist
Group 166 does not exist
Group 167 does not exist
Group 168 does not exist
Group 169 does not exist
Group 170 does not exist
Group 171 does not exist
Group 172 does not exist
Group 173 does not exist
Group 174 does not exist
Group 175 does not exist
Group 176 does not exist
Group 177 does not exist
Group 178 does not exist
Group 179 does not exist
Group 180 does not exist
Group 181 does not exist
Group 182 does not exist
Group 183 does not exist
Group 184 does not exist
Group 185 does not exist
Group 186 does not exist
Group 187 does not exist
Group 188 does not exist
Group 189 does not exist
Group 190 does not exist
Group 191 does not exist
Group 192 does not exist
Group 193 does not exist
Group 194 does not exist
Group 195 does not exist
Group 196 does not exist
Group 197 does not exist
Group 198 does not exist
Group 199 does not exist
Group 200 does not exist

> 
Found 38476 atoms with residue name W
Found 0 atoms with residue name NA
Found 0 atoms with residue name CL

> 

> 
Copied index group 1 'Solvent'
Complemented group: 16350 atoms

> 

> 
Found 312 atoms with name BB

> 

> 
Found 8 atoms with residue name CYF
Found 397 atoms with name C1
Merged two groups with AND: 8 397 -> 1

> 

> 
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-em.gro -f martini_v2.x_new-rf-eq1.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-em.gro

Ignoring obsolete mdp entry 'title'
Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq1.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


WARNING 1 [file martini_v2.x_new-rf-eq1.mdp]:
  The Berendsen thermostat does not generate the correct kinetic energy
  distribution, and should not be used for new production simulations (in
  our opinion). We would recommend the V-rescale thermostat.


WARNING 2 [file martini_v2.x_new-rf-eq1.mdp]:
  The Berendsen barostat does not generate any strictly correct ensemble,
  and should not be used for new production simulations (in our opinion).
  We recommend using the C-rescale barostat instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 43146.00

NOTE 2 [file martini_v2.x_new-rf-eq1.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

There were 2 WARNINGs

Back Off! I just backed up topol.tpr to ./#topol.tpr.10#

GROMACS reminds you: "Blessed is He Who In the Name Of Charity and Good Will Shepherds the Weak Through the Valley Of Darkness, For He is Truly His Brother's Keeper and the Finder Of Lost Children." (Pulp Fiction)

Setting the LD random seed to -1074266149

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Setting gen_seed to -1476919591

Velocities were taken from a Maxwell distribution at 310 K

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 5 Mb of data
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq1.gro -f martini_v2.x_new-rf-eq2.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-em.gro

Ignoring obsolete mdp entry 'title'
Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq2.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


WARNING 1 [file martini_v2.x_new-rf-eq2.mdp]:
  The Berendsen thermostat does not generate the correct kinetic energy
  distribution, and should not be used for new production simulations (in
  our opinion). We would recommend the V-rescale thermostat.


WARNING 2 [file martini_v2.x_new-rf-eq2.mdp]:
  The Berendsen barostat does not generate any strictly correct ensemble,
  and should not be used for new production simulations (in our opinion).
  We recommend using the C-rescale barostat instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

NOTE 2 [file martini_v2.x_new-rf-eq2.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 2 NOTEs

There were 2 WARNINGs

Back Off! I just backed up topol.tpr to ./#topol.tpr.11#

GROMACS reminds you: "You still have to climb to the shoulders of the giants" (Vedran Miletic)

Setting the LD random seed to 2147483647

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 6 Mb of data
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq2.gro -f martini_v2.x_new-rf-eq3-PULL.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-em.gro

Ignoring obsolete mdp entry 'title'
Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq3-PULL.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


WARNING 1 [file martini_v2.x_new-rf-eq3-PULL.mdp]:
  The Berendsen thermostat does not generate the correct kinetic energy
  distribution, and should not be used for new production simulations (in
  our opinion). We would recommend the V-rescale thermostat.


WARNING 2 [file martini_v2.x_new-rf-eq3-PULL.mdp]:
  The Berendsen barostat does not generate any strictly correct ensemble,
  and should not be used for new production simulations (in our opinion).
  We recommend using the C-rescale barostat instead.

Pull group 1 'PULL1' has 312 atoms
Pull group 2 'PULL2' has 1 atoms
Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

NOTE 2 [file martini_v2.x_new-rf-eq3-PULL.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.

Pull group  natoms  pbc atom  distance at start  reference at t=0
       1       312       431
       2         1         0       5.405 nm          5.505 nm

There were 2 NOTEs

There were 2 WARNINGs

Back Off! I just backed up topol.tpr to ./#topol.tpr.12#

GROMACS reminds you: "In the processing of models we must be especially cautious of the human weakness to think that models can be verified or validated. Especially one's own." (Roald Hoffmann)

Setting the LD random seed to -212079292

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 9 Mb of data
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq3.gro -f martini_v2.x_new-rf-eq4.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-eq3.gro

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq4.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


NOTE 2 [file system.top, line 45]:
  You are combining position restraints with Parrinello-Rahman pressure
  coupling, which can lead to instabilities. If you really want to combine
  position restraints with pressure coupling, we suggest to use C-rescale
  pressure coupling instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

NOTE 3 [file martini_v2.x_new-rf-eq4.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 3 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.13#

GROMACS reminds you: "Njuta men inte frossa, springa men inte fly" (Paganus)

Setting the LD random seed to -1075073037

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 4 Mb of data
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq4.gro -f martini_v2.x_new-rf-eq5.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-eq4.gro

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq5.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


NOTE 2 [file system.top, line 45]:
  You are combining position restraints with Parrinello-Rahman pressure
  coupling, which can lead to instabilities. If you really want to combine
  position restraints with pressure coupling, we suggest to use C-rescale
  pressure coupling instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

NOTE 3 [file martini_v2.x_new-rf-eq5.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 3 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.14#

GROMACS reminds you: "It Doesn't Seem Right, No Computers in Sight" (Faun Fables)

Setting the LD random seed to 1264582556

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 4 Mb of data
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq5.gro -f martini_v2.x_new-rf-eq6.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx -r lipids-water-eq5.gro

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-eq6.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


NOTE 2 [file system.top, line 45]:
  You are combining position restraints with Parrinello-Rahman pressure
  coupling, which can lead to instabilities. If you really want to combine
  position restraints with pressure coupling, we suggest to use C-rescale
  pressure coupling instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

NOTE 3 [file martini_v2.x_new-rf-eq6.mdp]:
  Removing center of mass motion in the presence of position restraints
  might cause artifacts. When you are using position restraints to
  equilibrate a macro-molecule, the artifacts are usually negligible.


There were 3 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.15#

GROMACS reminds you: "Discovery: A couple of months in the laboratory can frequently save a couple of hours in the library." (Anonymous)

Setting the LD random seed to 1677556667

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

This run will generate roughly 6 Mb of data
rm: cannot remove 'step*.pdb': No such file or directory
rm: cannot remove 'index-old.ndx': No such file or directory
rm: cannot remove 'temp-index-end.txt': No such file or directory
psimSubPatch_lower.pat
psimSubPatch_upper.pat
tar: protein-*-rotate.gro: Cannot stat: No such file or directory
tar: protein-ALL.gro: Cannot stat: No such file or directory
index-selection.txt
lipids-water-em.gro
lipids-water-eq1.gro
lipids-water-eq2.gro
lipids-water-eq3.gro
lipids-water.gro
martini_v2.x_new-rf-eq3-PULL.mdp
mdrun-em.log
mdrun-eq1.log
mdrun-eq2.log
mdrun-eq3.log
mdrun-eq4.log
pullf.xvg
pullx.xvg
tar: lipid_counts.npz: Cannot stat: No such file or directory
mdrun-eq5.log
lipids-water-eq5.gro
mdrun-eq6.log
lipids-water-eq4.gro
tar: macro_sim_dir/snapshot.*: Cannot stat: No such file or directory
tar: macro_sim_dir/macro_createsims.out: Cannot stat: No such file or directory
struct_createsim.gro
tar: Exiting with failure status due to previous errors
rm: cannot remove 'protein-*-rotate.gro': No such file or directory
rm: cannot remove 'protein-ALL.gro': No such file or directory
rm: cannot remove 'traj_comp.step*.xtc': No such file or directory
rm: cannot remove 'lipid_counts.npz': No such file or directory
rm: cannot remove 'macro_sim_dir': No such file or directory
               :-) GROMACS - gmx editconf, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx editconf -f lipids-water-eq6.gro -o lipids-water-eq6.gro -translate 0 0 -0.5


Back Off! I just backed up lipids-water-eq6.gro to ./#lipids-water-eq6.gro.1#

GROMACS reminds you: "Ich war schwanger, mir gings zum kotzen" (Nina Hagen)

Note that major changes are planned in future for editconf, to improve usability and utility.
Read 54826 atoms
Volume: 6024.32 nm^3, corresponds to roughly 2710900 electrons
Velocities found
Translating 54826 atoms (out of 54826) by 0 0 -0.5 nm
                :-) GROMACS - gmx grompp, 2024.5-conda_forge (-:

Executable:   /miniconda3/bin.ARM_NEON_ASIMD/gmx
Data prefix:  /miniconda3
Working dir:  /tmp/workdir
Command line:
  gmx grompp -c lipids-water-eq6.gro -r lipids-water-eq6.gro -f martini_v2.x_new-rf-prod.mdp -p system.top -o topol.tpr -maxwarn 5 -n index.ndx

Ignoring obsolete mdp entry 'ns_type'

NOTE 1 [file martini_v2.x_new-rf-prod.mdp]:
  verlet-buffer-pressure-tolerance is ignored when verlet-buffer-tolerance
  < 0


NOTE 2 [file system.top, line 45]:
  You are combining position restraints with Parrinello-Rahman pressure
  coupling, which can lead to instabilities. If you really want to combine
  position restraints with pressure coupling, we suggest to use C-rescale
  pressure coupling instead.

Number of degrees of freedom in T-Coupling group Solvent is 115425.00
Number of degrees of freedom in T-Coupling group Rest is 41747.00

There were 2 NOTEs

Back Off! I just backed up topol.tpr to ./#topol.tpr.1#

GROMACS reminds you: "Screw a Lightbulb in your Head" (Gogol Bordello)

Setting the LD random seed to -84213841

Generated 844 of the 356590 non-bonded parameter combinations

Excluding 1 bonded neighbours molecule type 'RAS_RAF'

Excluding 1 bonded neighbours molecule type 'POPX'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'POPC'

Excluding 1 bonded neighbours molecule type 'PAPC'

Excluding 1 bonded neighbours molecule type 'POPE'

Excluding 1 bonded neighbours molecule type 'DLPE'

Excluding 1 bonded neighbours molecule type 'SSM'

Excluding 1 bonded neighbours molecule type 'PAPS'

Excluding 1 bonded neighbours molecule type 'SAP6'

Excluding 1 bonded neighbours molecule type 'CHOL'

Excluding 1 bonded neighbours molecule type 'W'

Excluding 1 bonded neighbours molecule type 'NA'

Excluding 1 bonded neighbours molecule type 'CL'

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

Cleaning up constraints and constant bonded interactions with virtual sites

The center of mass of the position restraint coord's is 14.797  5.260 15.281

The center of mass of the position restraint coord's is 14.797  5.260 15.281

This run will generate roughly 4 Mb of data
rm: cannot remove 'fancy-slurm-syrah.she': No such file or directory
rm: cannot remove 'fancy.she': No such file or directory
rm: cannot remove 'lipids-water-eq4-fix.pdbe': No such file or directory
rm: cannot remove 'system.tope': No such file or directory
rm: cannot remove 'molecule_1.data': No such file or directory
rm: cannot remove 'molecule_2.data': No such file or directory
rm: cannot remove 'molecule_3.data': No such file or directory

> Initializing MuMMI (/opt/clones/mummi-core/mummi_core)
> Initialized MuMMI
	> MuMMI_ROOT: (/opt/clones/mummi-ras)
	> MuMMI_Resources: (/opt/clones/mummi_resources)
	> MuMMI_Specs: (/opt/clones/mummi-ras/specs)

> Creating MuMMI root hierarchy at (/opt/clones/mummi-ras)

> Initialized MuMMI
	> MuMMI_ROOT: (/opt/clones/mummi-ras)
	> MuMMI_Resources: (/opt/clones/mummi_resources)
	> MuMMI_Specs: (/opt/clones/mummi-ras/specs)

Launching Createsim from /tmp/workdir: Namespace(fstype='simple', outpath='/tmp/out', outlocal='/tmp/workdir', inpath='/tmp/workdir', loglevel=2, logpath='/tmp/workdir', logstdout=False, logfile='createsims', patch='structure_099868581', gromacs='gmx', mpi='gmx mdrun', mdrunopt=' -ntmpi 1 -ntomp 64 -pin off', simnum='', mini=True)
> Creating MuMMI root hierarchy at (/opt/clones/mummi-ras)

> Initializing logger:  level = (2), stdout = (False), file = (/tmp/workdir/createsims.log), history = (False),  memusage = (False)
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
=== times
{"times": {"createsim_runtime": 597.6543316841125}, "timestamps": {"createsims_create_cg_patch_start": 1753725089.1920626, "createsims_create_cg_patch_complete": 1753725089.1929665, "createsims_setup_cg_sim_start": 1753725089.198383, "createsims_gromacs_energy_minimization_0_start": 1753725089.5718114, "createsims_gromacs_energy_minimization_0_complete": 1753725090.4123578, "createsims_mdrun_lipids_water_0_start": 1753725090.41236, "createsims_mdrun_lipids_water_0_complete": 1753725090.5458217, "createsims_trjconv_lipids_water_0_start": 1753725090.5458314, "createsims_trjconv_lipids_water_0_complete": 1753725090.7104163, "createsims_gromacs_energy_minimization_1_start": 1753725091.091397, "createsims_gromacs_energy_minimization_1_complete": 1753725091.9380894, "createsims_mdrun_lipids_water_1_start": 1753725091.9380922, "createsims_mdrun_lipids_water_1_complete": 1753725093.5570226, "createsims_trjconv_lipids_water_1_start": 1753725093.5570242, "createsims_trjconv_lipids_water_1_complete": 1753725093.7223284, "createsims_gromacs_energy_minimization_2_start": 1753725094.0787253, "createsims_gromacs_energy_minimization_2_complete": 1753725094.9172826, "createsims_mdrun_lipids_water_2_start": 1753725094.917284, "createsims_mdrun_lipids_water_2_complete": 1753725097.0674114, "createsims_trjconv_lipids_water_2_start": 1753725097.0674133, "createsims_trjconv_lipids_water_2_complete": 1753725097.2332273, "createsims_gromacs_energy_minimization_3_start": 1753725097.6076853, "createsims_gromacs_energy_minimization_3_complete": 1753725098.446606, "createsims_mdrun_lipids_water_3_start": 1753725098.4466076, "createsims_mdrun_lipids_water_3_complete": 1753725100.2662787, "createsims_trjconv_lipids_water_3_start": 1753725100.2662802, "createsims_trjconv_lipids_water_3_complete": 1753725100.4321213, "createsims_gromacs_energy_minimization_4_start": 1753725100.8147283, "createsims_gromacs_energy_minimization_4_complete": 1753725101.6529448, "createsims_mdrun_lipids_water_4_start": 1753725101.6529467, "createsims_mdrun_lipids_water_4_complete": 1753725103.6370804, "createsims_trjconv_lipids_water_4_start": 1753725103.637082, "createsims_trjconv_lipids_water_4_complete": 1753725103.8028774, "createsims_gromacs_energy_minimization_5_start": 1753725104.1804912, "createsims_gromacs_energy_minimization_5_complete": 1753725105.018023, "createsims_mdrun_lipids_water_5_start": 1753725105.0180242, "createsims_mdrun_lipids_water_5_complete": 1753725107.1735244, "createsims_trjconv_lipids_water_5_start": 1753725107.1735263, "createsims_trjconv_lipids_water_5_complete": 1753725107.3392963, "createsims_gromacs_energy_minimization_6_start": 1753725107.7121866, "createsims_gromacs_energy_minimization_6_complete": 1753725108.549245, "createsims_mdrun_lipids_water_6_start": 1753725108.5492468, "createsims_mdrun_lipids_water_6_complete": 1753725110.8813105, "createsims_trjconv_lipids_water_6_start": 1753725110.8813136, "createsims_trjconv_lipids_water_6_complete": 1753725111.0474803, "createsims_gromacs_energy_minimization_7_start": 1753725111.4244092, "createsims_gromacs_energy_minimization_7_complete": 1753725112.2636719, "createsims_mdrun_lipids_water_7_start": 1753725112.2636733, "createsims_mdrun_lipids_water_7_complete": 1753725115.3879468, "createsims_trjconv_lipids_water_7_start": 1753725115.3879485, "createsims_trjconv_lipids_water_7_complete": 1753725115.5545108, "createsims_gromacs_energy_minimization_8_start": 1753725115.923677, "createsims_gromacs_energy_minimization_8_complete": 1753725116.7650797, "createsims_mdrun_lipids_water_8_start": 1753725116.7650816, "createsims_mdrun_lipids_water_8_complete": 1753725119.6157968, "createsims_trjconv_lipids_water_8_start": 1753725119.6157982, "createsims_trjconv_lipids_water_8_complete": 1753725119.7827156, "createsims_gromacs_energy_minimization_9_start": 1753725120.141632, "createsims_gromacs_energy_minimization_9_complete": 1753725120.9806569, "createsims_mdrun_lipids_water_9_start": 1753725120.9806585, "createsims_mdrun_lipids_water_9_complete": 1753725123.3611975, "createsims_trjconv_lipids_water_9_start": 1753725123.3611999, "createsims_trjconv_lipids_water_9_complete": 1753725123.527169, "createsims_gromacs_make_ndx_9_start": 1753725123.5274794, "createsims_gromacs_make_ndx_9_complete": 1753725123.9934108, "createsims_generate_velocities_0_start": 1753725123.993481, "createsims_generate_velocities_0_complete": 1753725162.6997712, "createsims_short_equilibration_0_start": 1753725162.6997728, "createsims_short_equilibration_0_complete": 1753725247.0595243, "createsims_pull_molecules_0_start": 1753725247.0595262, "createsims_pull_molecules_0_complete": 1753725575.173523, "createsims_relax_protein_start": 1753725575.1735253, "createsims_relax_protein_complete": 1753725603.0432758, "createsims_short_equilibration_20fs_start": 1753725603.0432773, "createsims_short_equilibration_20fs_complete": 1753725683.820651, "createsims_setup_cg_sim_complete": 1753725685.741987, "createsims_prime_cg_sim_start": 1753725685.742032, "createsims_prime_cg_sim_complete": 1753725686.835294}}
===
/tmp/out
├── 099868581
│   └── structure_099868581.gro
├── createsims-times.json
├── createsims.log
├── createsims.tar.gz
├── createsims_success
├── index.ndx
├── lipids-water-eq6.gro
├── martini_v2.x_new-rf-prod.mdp
├── psim.npz
├── system.top
└── topol.tpr

1 directory, 11 files
```

</details>
<details>

<summary>cganalysis output</summary>

```console
099868581
createsims-times.json
createsims.log
createsims.tar.gz
createsims_success
index.ndx
lipids-water-eq6.gro
martini_v2.x_new-rf-prod.mdp
psim.npz
system.top
topol.tpr
 Resnames ['ALA' 'ARG' 'ASN' 'ASP' 'CGW' 'CYF' 'CYM' 'CYS' 'GLN' 'GLU' 'GLY' 'GTP'
 'HSE' 'ILE' 'ION' 'LEU' 'LYS' 'MET' 'MG' 'PHE' 'PRO' 'SER' 'THR' 'TRP'
 'TYR' 'VAL' 'W' 'ZN2'] either not lipids or not supported!
Found leaflets of size 448 353
/miniconda3/lib/python3.11/site-packages/MDAnalysis/coordinates/XDR.py:253: UserWarning: Reload offsets from trajectory
 ctime or size or n_atoms did not match
  warnings.warn(

Copy cleanup local only works for ddcMD files
Copy cleanup local only works for ddcMD files
> Initialized MuMMI
	> MuMMI_ROOT: (/opt/clones/mummi-ras)
	> MuMMI_Resources: (/opt/clones/mummi_resources)
	> MuMMI_Specs: (/opt/clones/mummi-ras/specs)

> Creating MuMMI root hierarchy at (/opt/clones/mummi-ras)

=== times
{"times": {}, "timestamps": {"cganalysis_run_start": 1753726159.3067226, "cganalysis_load_mdanalysis_start": 1753726159.3704524, "cganalysis_load_mdanalysis_complete": 1753726160.0225558, "cganalysis_run_simulation_start": 1753726160.0243845, "cganalysis_simrun_start": 1753726160.0244572, "cganalysis_simrun_complete": 1753726165.0305023, "cganalysis_run_simulation_complete": 1753726165.0305154, "cganalysis_main_analysis_start": 1753726165.0305185, "cganalysis_main_analysis_complete": 1753726518.4014115, "cganalysis_run_complete": 1753726518.401484}}
===
0
cganalysis output:
/workdir/out
├── analysis.tar
├── analysis.tar.pylst
├── analysis.tar.pytree
├── cg_analysis.log
├── cg_analysis.out
├── cganalysis-times.json
├── createsims.log
├── md.log
└── mdrun.log

0 directories, 9 files
```

When you are done, cleanup.

```bash
kubectl delete -f ./configs/02-createsims-minicluster.yaml 
kubectl delete -f ./configs/03-cganalysis-minicluster.yaml 
```

</details>

Createsims runs for approximately 10 minutes, however it depends on the simulation data you get from the mlrunner. Cganalysis for experiments we ran, we capped to 30 minutes, and the build here is capped to approximately 6 minutes. You can use `kubectl logs <pod>` to equivalently see the output, which will include timings.

### MuMMI with MPI

How can the Flux Operator (and Flux, generally) improve running a MuMMI component? We can run gromacs (the underlying unit of cganalysis and createsims) on two nodes to improve performance. Let's test that next. First, let's run gromacs on one node.

```bash
kubectl apply -f configs/05-gromacs-mpi-1-node-minicluster.yaml
kubectl logs gromacs-mpi-0-wc4mz -f
```

This will run for about 3 minutes. To make it longer (6 minutes) you can change the command as follows:

```diff
- gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.05 -ntomp 1 -ddcheck
+ gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.1 -ntomp 1 -ddcheck
```

The Figure of Merit is the simulation ns/day. For one node with MPI, we get `731.930 ns/day`:

```console
                      :-) GROMACS - gmx mdrun, 2024.2 (-:

Executable:   /usr/bin/gmx_mpi
Data prefix:  /usr
Working dir:  /opt/gromacs/structure_iter00_000000000353_YYNN-0
Command line:
  gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.05 -ntomp 1 -ddcheck

Reading file topol.tpr, VERSION 2024.1-spack (single precision)
Can not increase nstlist because verlet-buffer-tolerance is not set or used
Update groups can not be used for this system because an incompatible virtual site type is used

Using 64 MPI processes
Using 1 OpenMP thread per MPI process

starting mdrun 'lipids-sim'
-1 steps, infinite ps.

Step 75520: Run time exceeded 0.050 hours, will terminate the run within 40 steps


Dynamic load balancing report:
 DLB got disabled because it was unsuitable to use.
 Average load imbalance: 3.5%.
 The balanceable part of the MD step is 61%, load imbalance is computed from this.
 Part of the total run time spent waiting due to load imbalance: 2.1%.


NOTE: 18 % of the run time was spent in domain decomposition,
      5 % of the run time was spent in pair search,
      you might want to increase nstlist (this has no effect on accuracy)

               Core t (s)   Wall t (s)        (%)
       Time:    11413.965      178.343     6400.0
                 (ns/day)    (hour/ns)
Performance:      731.930        0.033

GROMACS reminds you: "You should call it 'entropy'. No one knows what entropy really is, so in a debate you will always have the advantage." (John von Neumann to Claude Shannon, on why he should borrow the term for information theory)
```

When you are done:

```bash
kubectl delete -f configs/05-gromacs-mpi-1-node-minicluster.yaml
```

Now let's increase to 2 nodes and see the benefit of scaling out.

```bash
kubectl apply -f configs/05-gromacs-mpi-2-node-minicluster.yaml
kubectl logs gromacs-mpi-0-wc4mz -f
```

This will also run for about 3 minutes. To make it longer (6 minutes) change the command as follows:

```diff
- gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.05 -ntomp 1 -ddcheck
+ gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.1 -ntomp 1 -ddcheck
```

The Figure of Merit is the simulation ns/day. For two nodes with MPI, we get the following:

```console
                      :-) GROMACS - gmx mdrun, 2024.2 (-:

Executable:   /usr/bin/gmx_mpi
Data prefix:  /usr
Working dir:  /opt/gromacs/structure_iter00_000000000353_YYNN-0
Command line:
  gmx_mpi mdrun -rcon 0.4 -cpi -pin off -maxh 0.05 -ntomp 1 -ddcheck

Reading file topol.tpr, VERSION 2024.1-spack (single precision)
Can not increase nstlist because verlet-buffer-tolerance is not set or used
Update groups can not be used for this system because an incompatible virtual site type is used

Using 128 MPI processes
Using 1 OpenMP thread per MPI process

starting mdrun 'lipids-sim'
-1 steps, infinite ps.

Step 107920: Run time exceeded 0.050 hours, will terminate the run within 40 steps


Dynamic load balancing report:
 DLB got disabled because it was unsuitable to use.
 Average load imbalance: 7.0%.
 The balanceable part of the MD step is 51%, load imbalance is computed from this.
 Part of the total run time spent waiting due to load imbalance: 3.6%.


NOTE: 16 % of the run time was spent in domain decomposition,
      4 % of the run time was spent in pair search,
      you might want to increase nstlist (this has no effect on accuracy)

               Core t (s)   Wall t (s)        (%)
       Time:    22827.047      178.337    12800.0
                 (ns/day)    (hour/ns)
Performance:     1045.899        0.023

GROMACS reminds you: "The three principal virtues of a programmer are Laziness, Impatience, and Hubris" (Larry Wall)
```
Note that the ns/day improves by approximately 1.43x.

### An example state machine

Let's install the state machine operator. The operator will orchestrate components as steps in a state machine, with transitions guided by job completions. First, install the operator.

```bash
kubectl apply -f ./configs/state-machine-operator-arm.yaml
```

Here is how to ensure that the operator is running.

```bash
manager=$(kubectl get pods -l control-plane=controller-manager -n state-machine-operator-system -o json | jq -r .items[0].metadata.name)
echo "Manager pod is $manager"
kubectl logs -n state-machine-operator-system ${manager}
```

Next, create a state machine based on a toy workflow. MuMMI steps generate scientific data and can take a while to run, so let's start with a quick, simple example. The example uses LAMMPS as the HPC application in the workflow, and runs a small REAXFF problem. 

We will ask for two completions, so you will see two jobs run in parallel. If we launched more jobs, they would be submit as space opened up after workflow completions.

```bash
kubectl apply -f ./configs/state-machine.yaml
```

The state machine manager will be creating, and a local [OCI Registry as Storage](https://oras.land) (ORAS) registry created to easily share assets between steps.

```bash
 kubectl get pods
NAME                                     READY   STATUS              RESTARTS   AGE
registry-0                               1/1     Running             0          5s
state-machine-manager-765fb94769-bdlls   0/1     ContainerCreating   0          5s
```

You can look at the logs of the manager to see the state machines starting! 

```bash
kubectl logs mummi-manager-7c74786dfc-gm5vb -f
```
```bash
kubectl logs state-machine-manager-d95d6b564-78jpz 
state-machine-manager start /opt/jobs/state-machine-workflow.yaml --config-dir=/opt/jobs --quiet --scheduler kubernetes --registry registry-0.state-machine.default.svc.cluster.local:5000 --plain-http
INFO:state_machine_operator.manager.manager: Job Prefix: [job_]
INFO:state_machine_operator.manager.manager:  Scheduler: [kubernetes]
INFO:state_machine_operator.manager.manager:   Registry: [registry-0.state-machine.default.svc.cluster.local:5000]
INFO:state_machine_operator.manager.manager:Manager running with 0 job sequence completions.
INFO:state_machine_operator.manager.manager:Job job_034270112 is active and not completed
INFO:state_machine_operator.manager.manager:Job job_076011541 is active and not completed
INFO:state_machine_operator.manager.manager:Job job_076011541 is successful
```

And the matching jobs. First is a faux setup job `job-a`. You will also notice we have two state machines running in parallel. If you look at the custom resource definition that created it, we allow a maximum cluster size of 2 (the number of nodes we have) and ask for 4 completions to indicate success.

```bash
$ kubectl get pods
job-a-job-060932910-tfjjn               0/1     Completed   0          8s
job-a-job-088170049-96h9m               0/1     Completed   0          8s
job-c-job-074261618-h9s6p               0/1     Completed   0          12s
job-c-job-098019854-c6vmh               0/1     Completed   0          12s
lammps-job-060932910-0-s9msw            0/1     Init:0/1    0          5s
lammps-job-060932910-1-48wsq            0/1     Init:0/1    0          5s
lammps-job-074261618-0-xm822            0/1     Completed   0          112s
lammps-job-074261618-1-7gp6z            0/1     Completed   0          112s
lammps-job-088170049-0-4mjxq            0/1     Init:0/1    0          5s
lammps-job-088170049-1-j8vp4            0/1     Init:0/1    0          5s
lammps-job-098019854-0-2x5wg            0/1     Completed   0          112s
lammps-job-098019854-1-c8xvf            0/1     Completed   0          112s
registry-0                              1/1     Running     0          114s
state-machine-manager-d95d6b564-5bhpl   1/1     Running     0          114s
```

You can watch LAMMPS jobs appear, each of which generates 2 pods (a Flux Operator minicluster) and then the final step (job-c) to constitute one completion. If we ran MuMMI, the jobs could go up to 12 hours on HPC, and for small experiments, about 2.5 hours. When everything completes:

```bash
$ kubectl get pods
job-a-job-060932910-tfjjn               0/1     Completed   0          105s
job-a-job-088170049-96h9m               0/1     Completed   0          105s
job-c-job-060932910-z9mdw               0/1     Completed   0          7s
job-c-job-074261618-h9s6p               0/1     Completed   0          109s
job-c-job-088170049-67hjt               0/1     Completed   0          9s
job-c-job-098019854-c6vmh               0/1     Completed   0          109s
lammps-job-060932910-0-s9msw            0/1     Completed   0          102s
lammps-job-060932910-1-48wsq            0/1     Completed   0          102s
lammps-job-074261618-0-xm822            0/1     Completed   0          3m29s
lammps-job-074261618-1-7gp6z            0/1     Completed   0          3m29s
lammps-job-088170049-0-4mjxq            0/1     Completed   0          102s
lammps-job-088170049-1-j8vp4            0/1     Completed   0          102s
lammps-job-098019854-0-2x5wg            0/1     Completed   0          3m29s
lammps-job-098019854-1-c8xvf            0/1     Completed   0          3m29s
registry-0                              1/1     Running     0          3m31s
state-machine-manager-d95d6b564-5bhpl   1/1     Running     0          3m31s
```

How would we get the output? All of the artifacts are stored in a registry in the cluster. We would install [oras](https://oras.land), and pull from the local registry. When you are done:

```bash
kubectl delete -f ./configs/state-machine.yaml
kubectl delete miniclusters.flux-framework.org --all
kubectl delete jobs --all
kubectl delete pods --all
```

Importantly, make sure all Pod objects (the registry, the manager, and job steps) are cleaned up before you proceed.

### MuMMI as a State Machine

Finally, we will run the MuMMI state machine. It is the same conceptually as the simple example above, but we have MuMMI components (e.g., `createsims` and `cganalysis` which use GROMACS) that run longer and generate scientifically meaningful output.

```bash
kubectl apply -f configs/mummi-state-machine.yaml
```

---
**Navigation:**
- Previous: [Module 2](../02-module2-flux-lammps/README.md)
- Up: [Workshop Home](../README.md)
