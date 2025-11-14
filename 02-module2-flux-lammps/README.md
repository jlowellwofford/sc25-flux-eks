# Module 2: Flux and LAMMPS

[Home](../README.md) > Module 2: Flux and LAMMPS

## Overview

This module will cover running [LAMMPS](https://www.lammps.org) (Large-scale Atomic/Molecular Massively Parallel Simulator) using Flux for advanced job scheduling and resource management.

## Contents

- [Flux setup and configuration](#setup)
- [LAMMPS MiniCluster as a Job](#lammps-minicluster-as-a-job)
- [Interactive MiniCluster operations](#interactive-minicluster)
- [Helm-based installations](#helm-install)
- [Advanced scheduling scenarios](#advanced-scheduling-scenarios)

## Prerequisites

- Completion of Module 1
- Understanding of HPC job scheduling concepts

## Estimated Time

- 45 minutes

## Tutorial

### Setup

Your eksctl cluster that we used in Module 1 is already created. We need to install the cluster autoscaler to allow for scaling to 2 nodes. 

```bash
kubectl apply -f ./configs/cluster-autoscaler.yaml
```

When the cluster is created, install the Flux Operator. Note that this is an ARM build since we are running on an AWS Graviton (ARM) processor.

```bash
kubectl apply -f https://raw.githubusercontent.com/flux-framework/flux-operator/refs/heads/main/examples/dist/flux-operator-arm.yaml
```

It is easier to have auto-completion for kubectl. If you haven't done this yet:

```bash
source <(kubectl completion bash)
```

## LAMMPS MiniCluster as a Job

A Flux Framework MiniCluster is akin to running an entire Flux Cluster across some number of physical nodes in Kubernetes. 
We create it with a custom resource definition (CRD).

```bash
kubectl apply -f ./configs/minicluster-job.yaml
```

If you have not scaled the nodes of your cluster up yet, here is how to ensure that the cluster is autoscaling.

<details>

<summary>Checking the autoscaler</summary>

See that one is Init/Running, and one is Pending

```bash
kubectl get pods
```

Describe pods to see the events for pending. 

```bash
kubectl describe pods
```

Look at the cluster autoscaler log (press tab to autocomplete to the full pod name)

```bash
kubectl get pods -n kube-system cluster-autoscaler-[TAB]
```

Finally, when you see the scaling event is triggered, watch for the node to be ready.

```bash
kubectl get nodes
```

</details>

You can watch the progress, either as a one of check or with watch for persistence. 
This LAMMPS image takes approximately one minute to pull.
Here is how to view pods, and watch for changes:

```bash
kubectl get pods
kubectl get pods --watch
```

The `Init:0/1` is running initialization containers to prepare the Flux View using [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/). When you see `PodsInitializing` this usually is primarily containers pulling for our main application. The `Running` state indicates our cluster is ready to interact with or the job is running. Since this is running a one-off command, it means the MiniCluster is acting like a Job with state. It will be Running, and then Complete. When it is Running you can monitor it via the lead broker (index 0 of the [Indexed Job](https://kubernetes.io/blog/2021/04/19/introducing-indexed-jobs/) set, which is launching the job). Note that we can add the `-f` to ensure it keeps running.

```bash
kubectl logs lammps-job-0-dl4dm -f
```

<details>

<summary> LAMMPS output </summary>

```console
LAMMPS (17 Apr 2024 - Development - a8687b5372)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Reading data file ...
  triclinic box = (0 0 0) to (22.326 11.1412 13.778966) with tilt (0 -5.02603 0)
  8 by 4 by 4 MPI processor grid
  reading atoms ...
  304 atoms
  reading velocities ...
  304 velocities
  read_data CPU = 0.075 seconds
Replication is creating a 8x8x8 = 512 times larger system...
  triclinic box = (0 0 0) to (178.608 89.1296 110.23173) with tilt (0 -40.20824 0)
  8 by 4 by 4 MPI processor grid
  bounding box image = (0 -1 -1) to (0 1 1)
  bounding box extra memory = 0.03 MB
  average # of replicas added to proc = 18.46 out of 512 (3.61%)
  155648 atoms
  replicate CPU = 0.010 seconds
Neighbor list info ...
  update: every = 20 steps, delay = 0 steps, check = no
  max neighbors/atom: 2000, page size: 100000
  master list distance cutoff = 11
  ghost atom cutoff = 11
  binsize = 5.5, bins = 40 17 21
  2 neighbor lists, perpetual/occasional/extra = 2 0 0
  (1) pair reaxff, perpetual
      attributes: half, newton off, ghost
      pair build: half/bin/ghost/newtoff
      stencil: full/ghost/bin/3d
      bin: standard
  (2) fix qeq/reax, perpetual, copy from (1)
      attributes: half, newton off
      pair build: copy
      stencil: none
      bin: none
Setting up Verlet run ...
  Unit style    : real
  Current step  : 0
  Time step     : 0.1
Per MPI rank memory allocation (min/avg/max) = 143.9 | 143.9 | 143.9 Mbytes
   Step          Temp          PotEng         Press          E_vdwl         E_coul         Volume    
         0   300           -113.27833      438.99595     -111.57687     -1.7014647      1754807.5    
        10   300.88261     -113.2808       1018.2986     -111.5794      -1.7014015      1754807.5    
        20   302.3388      -113.28501      1897.0286     -111.58375     -1.7012621      1754807.5    
        30   302.11018     -113.28419      4220.8936     -111.58318     -1.7010124      1754807.5    
        40   299.82789     -113.27728      6263.6197     -111.57661     -1.7006693      1754807.5    
        50   296.69384     -113.2679       6399.8054     -111.56761     -1.7002908      1754807.5    
        60   294.39704     -113.26102      6164.4726     -111.56111     -1.6999131      1754807.5    
        70   294.64264     -113.26172      6839.9294     -111.56219     -1.699534       1754807.5    
        80   297.83962     -113.27122      8089.2834     -111.57207     -1.6991567      1754807.5    
        90   301.61126     -113.28247      9266.8765     -111.58365     -1.6988216      1754807.5    
       100   302.44604     -113.2849       10317.601     -111.58632     -1.6985828      1754807.5    
Loop time of 16.9415 on 128 procs for 100 steps with 155648 atoms

Performance: 0.051 ns/day, 470.598 hours/ns, 5.903 timesteps/s, 918.737 katom-step/s
99.3% CPU use with 128 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 8.2037     | 9.3305     | 10.232     |  13.5 | 55.08
Neigh   | 0.17003    | 0.17238    | 0.1991     |   0.8 |  1.02
Comm    | 0.74964    | 1.6075     | 2.6846     |  32.1 |  9.49
Output  | 0.0052343  | 0.025479   | 0.068773   |  11.0 |  0.15
Modify  | 5.7377     | 5.8048     | 5.8892     |   1.9 | 34.26
Other   |            | 0.0007941  |            |       |  0.00

Nlocal:           1216 ave        1223 max        1211 min
Histogram: 14 9 15 18 19 32 10 5 4 2
Nghost:        7592.34 ave        7607 max        7578 min
Histogram: 2 5 14 20 25 23 22 10 3 4
Neighs:         432973 ave      435336 max      431057 min
Histogram: 4 13 18 18 22 23 15 7 6 2

Total # of neighbors = 55420529
Ave neighs/atom = 356.06323
Neighbor list builds = 5
Dangerous builds not checked
Total wall time: 0:00:17
broker.info[0]: rc2.0: flux submit -N 2 -n128 -o cpu-affinity=per-task --quiet --watch lmp -v x 8 -v y 8 -v z 8 -in in.reaxff.hns -nocite Exited (rc=0) 20.0s
broker.info[0]: rc2-success: run->cleanup 20.0505s
broker.info[0]: cleanup.0: flux queue stop --quiet --all --nocheckpoint Exited (rc=0) 0.1s
broker.info[0]: cleanup.1: flux resource acquire-mute Exited (rc=0) 0.1s
broker.info[0]: cleanup.2: flux cancel --user=all --quiet --states RUN Exited (rc=0) 0.1s
broker.info[0]: cleanup.3: flux queue idle --quiet Exited (rc=0) 0.1s
broker.info[0]: cleanup-success: cleanup->shutdown 0.414033s
broker.info[0]: children-complete: shutdown->finalize 48.0758ms
broker.info[0]: rc3.0: running /etc/flux/rc3.d/01-sched-fluxion
broker.info[0]: rc3.0: /etc/flux/rc3 Exited (rc=0) 0.1s
broker.info[0]: rc3-success: finalize->goodbye 89.8051ms
broker.info[0]: goodbye: goodbye->exit 0.033698ms
```

</details>

The pods will reach status Complete. This is a feature of a Kubernetes Job. The pod is no longer consuming cluster resources, but is left for inspection.  

```bash
kubectl get pods
NAME                  READY   STATUS      RESTARTS   AGE
lammps-job-0-dl4dm   0/1     Completed   0          5m19s
lammps-job-1-447xz   0/1     Completed   0          5m19s
```

When you are done, clean up. This will remove the pods from the listing, and is good practice.

```bash
kubectl delete -f ./configs/minicluster-job.yaml
```

### Interactive MiniCluster

What if you want to run an HPC workload, but shell into the cluster to interact with it? 
You may want to test the submission, inspect data outputs, or otherwise interact. 
The Flux Operator has an interactive mode that turns your Job into an interactive environment. 
We can make one small change to the MiniCluster custom resource definition to make it interactive:

```diff
+ interactive: true
```

Let's create our interactive LAMMPS Job.

```bash
kubectl apply -f ./configs/minicluster-interactive.yaml
```

When the pods are Running, shell in to the lead broker pod:

```bash
kubectl exec -it lammps-interactive-xxxxx -- bash
```
Source some environment variables to easily expose the Flux socket and update paths, etc.

```bash
. /mnt/flux/flux-view.sh
```

We now are going to connect to our running Flux instance. The Flux instance was started when we brought up the cluster. The pod you are working on is the lead broker, the top of a tree that the worker nodes are connecting to with ZeroMQ. The way we will connect is via a filesystem socket. We use the command `flux proxy` to do that, and the path to the socket is automatically derived for us. Here is how to connect to your Flux instance:

```bash
flux proxy $fluxsocket bash
```

You'll then have a full cluster (the resources will match what you are given). We can use `flux resource list` to see our resources.

```bash
# flux resource list
     STATE NNODES   NCORES    NGPUS NODELIST
      free      2      128        0 lammps-interactive-[0-1]
 allocated      0        0        0 
      down      0        0        0 
```

Then run LAMMPS, this time using flux directly.

```bash
flux run -N2 -n 128 -o cpu-affinity=per-task lmp -v x 8 -v y 8 -v z 8 -in in.reaxff.hns -nocite
```

You can also `flux submit` the same for a non-blocking interaction. When you are done, exit from the interface and:

```bash
kubectl delete -f ./configs/minicluster-interactive.yaml
```

<!--0### Side Quests

- See if you can figure out what the standard LAMMPS Figure of Merit (FOM) is in the output.
- Test running the job with affinity (as we did) and then removing the flag for setting CPU affinity (`-o cpu-affinity=per-task` or setting to `none`. What differences do you see? What do you think is happening?
-->

### Helm Install

We can also install everything via the helm package manager. This is the same LAMMPS, but with the addition of running 3 iterations, and asking for additional log output from Flux.

```bash
helm install \
  --set minicluster.efa=1 \
  --set minicluster.size=2 \
  --set experiment.nodes=2 \
  --set experiment.tasks=128 \
  --set experiment.iterations=3 \
  --set lammps.x=8 \
  --set lammps.y=8 \
  --set lammps.z=8 \
  --set minicluster.save_logs=true \
  --set minicluster.image=ghcr.io/converged-computing/lammps-reax-efa:ubuntu2404-efa \
  --set flux.image=ghcr.io/converged-computing/flux-view-rocky:arm-9 \
lammps oci://ghcr.io/converged-computing/flux-apps-helm-lammps-reax/chart --version 0.1.0
```

Helm is like a package manager for Kubernetes. We have developed several HPC applications there, and you can see them in this [GitHub repository](https://github.com/converged-computing/flux-apps-helm). To see output, we will do the same command. The helm charts provide an ability to run experiments with more structured output and additional metadata from Flux.

```bash
kubectl logs lammps-0-g2ggm -f
```

When you are done:

```bash
helm uninstall lammps
```

### Advanced Scheduling Scenarios

TBA

- Can we do something with fluxbind (topology) if it's ready? Or do the side quests go here?

You are done with this module. If you would like to use or modify the LAMMPS container, we have provided the Docker build assets in [docker](docker). Use the navigation below to move to the next module.

---
**Navigation:**
- Previous: [Module 1](../02-module1-hpc-kubernetes/README.md)
- Next: [Module 3](../04-module3-mummi-workflows/README.md)
- Up: [Workshop Home](../README.md)
