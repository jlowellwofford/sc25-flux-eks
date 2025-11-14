#!/usr/bin/env python3
"""
Simple PyTorch DDP Training on MNIST
Designed for c7g.16xlarge (ARM64/Graviton4) with EFA
"""
import argparse
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import datasets, transforms

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # Convolutional layers for more complex feature extraction
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        
        # Fully connected layers
        self.fc1 = nn.Linear(128 * 3 * 3, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)
    
    def forward(self, x):
        # Input: 28x28
        x = F.relu(self.conv1(x))  # 28x28x32
        x = self.pool(x)            # 14x14x32
        x = self.dropout1(x)
        
        x = F.relu(self.conv2(x))  # 14x14x64
        x = self.pool(x)            # 7x7x64
        x = self.dropout1(x)
        
        x = F.relu(self.conv3(x))  # 7x7x128
        x = self.pool(x)            # 3x3x128
        x = self.dropout1(x)
        
        x = x.view(-1, 128 * 3 * 3)
        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = F.relu(self.fc2(x))
        x = self.dropout2(x)
        return self.fc3(x)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='PyTorch DDP MNIST Training')
    parser.add_argument('--monitor-efa', action='store_true',
                        help='Enable EFA usage monitoring (default: disabled)')
    args = parser.parse_args()
    
    # Get distributed training parameters from environment
    rank = int(os.environ.get('RANK', 0))
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    
    print(f"[Rank {rank}] Starting training (world_size={world_size})")
    # Get baseline EFA statistics if monitoring is enabled
    efa_stats_before = {}
    if args.monitor_efa:
        print(f"[Rank {rank}] FI_PROVIDER: {os.environ.get('FI_PROVIDER', 'not set')}")
        print(f"[Rank {rank}] FI_EFA_USE_DEVICE_RDMA: {os.environ.get('FI_EFA_USE_DEVICE_RDMA', 'not set')}")
        
        # Check for EFA device
        import subprocess
        try:
            result = subprocess.run(['ls', '/dev/infiniband/'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[Rank {rank}] EFA devices found: {result.stdout.strip()}")
            else:
                print(f"[Rank {rank}] No EFA devices found")
        except:
            print(f"[Rank {rank}] Could not check for EFA devices")
        
        try:
            result = subprocess.run(['rdma', 'statistic', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                # Parse output - format is "link device metric1 value1 metric2 value2 ..." all on one line
                parts = result.stdout.split()
                for i in range(len(parts) - 1):
                    if parts[i] in ['tx_bytes', 'rx_bytes', 'send_bytes', 'recv_bytes']:
                        try:
                            efa_stats_before[parts[i]] = int(parts[i + 1])
                        except (ValueError, IndexError):
                            continue
                
                if efa_stats_before:
                    print(f"[Rank {rank}] EFA stats before training:")
                    for key, val in efa_stats_before.items():
                        print(f"[Rank {rank}]   {key}: {val}")
        except Exception as e:
            print(f"[Rank {rank}] Could not read EFA stats: {e}")
    
    # Initialize process group with Gloo (CPU backend)
    print(f"[Rank {rank}] Initializing process group with Gloo backend...")
    dist.init_process_group(backend='gloo')
    print(f"[Rank {rank}] Process group initialized")
    
    # Set device
    device = torch.device("cpu")
    
    # Create model and wrap with DDP
    model = Net().to(device)
    ddp_model = DDP(model)
    
    # Setup data
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = datasets.MNIST('/data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('/data', train=False, download=True, transform=transform)
    
    train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=rank)
    train_loader = DataLoader(train_dataset, batch_size=32, sampler=train_sampler, num_workers=0)  # Smaller batch = more iterations
    
    # Test loader (only rank 0 will use this)
    test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False, num_workers=0)
    
    # Training setup
    optimizer = torch.optim.Adam(ddp_model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    # Train for more epochs with complex model
    num_epochs = 10
    for epoch in range(1, num_epochs + 1):
        ddp_model.train()
        train_sampler.set_epoch(epoch)  # Ensure different shuffling each epoch
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = ddp_model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            if batch_idx % 100 == 0 and rank == 0:
                print(f"Epoch {epoch}/{num_epochs}, Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}")
        
        # Test after each epoch (only rank 0)
        if rank == 0:
            ddp_model.eval()
            test_loss = 0
            correct = 0
            with torch.no_grad():
                for data, target in test_loader:
                    data, target = data.to(device), target.to(device)
                    output = ddp_model(data)
                    test_loss += criterion(output, target).item()
                    pred = output.argmax(dim=1, keepdim=True)
                    correct += pred.eq(target.view_as(pred)).sum().item()
            
            test_loss /= len(test_loader)
            accuracy = 100. * correct / len(test_dataset)
            print(f"Epoch {epoch}/{num_epochs} - Test Loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_dataset)} ({accuracy:.2f}%)")
    
    if rank == 0:
        print("Training completed successfully!")
    
    # Get EFA statistics after training if monitoring is enabled
    if args.monitor_efa and efa_stats_before:
        print(f"[Rank {rank}] Checking EFA usage after training...")
        try:
            result = subprocess.run(['rdma', 'statistic', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                efa_stats_after = {}
                parts = result.stdout.split()
                for i in range(len(parts) - 1):
                    if parts[i] in ['tx_bytes', 'rx_bytes', 'send_bytes', 'recv_bytes']:
                        try:
                            efa_stats_after[parts[i]] = int(parts[i + 1])
                        except (ValueError, IndexError):
                            continue
                
                print(f"[Rank {rank}] EFA stats after training:")
                efa_used = False
                for key in efa_stats_before.keys():
                    if key in efa_stats_after:
                        delta = efa_stats_after[key] - efa_stats_before[key]
                        print(f"[Rank {rank}]   {key}: {efa_stats_after[key]} (Δ +{delta})")
                        if delta > 0:
                            efa_used = True
                
                if efa_used:
                    print(f"[Rank {rank}] ✓✓✓ EFA WAS USED FOR COMMUNICATION! ✓✓✓")
                else:
                    print(f"[Rank {rank}] ⚠ No EFA traffic detected (Gloo uses TCP)")
        except Exception as e:
            print(f"[Rank {rank}] Exception reading EFA stats: {e}")
    
    dist.destroy_process_group()

if __name__ == "__main__":
    main()
