FROM ubuntu:22.04
#FROM public.ecr.aws/deep-learning-containers/pytorch-training-arm64:2.7.0-gpu-py312-cu128-ubuntu22.04-ec2-v1.37-soci

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# These are pre-installed in the ECR image
# Install Python, dependencies, and rdma tools for EFA monitoring
RUN apt-get update && apt-get install -y \
    iproute2 rdma-core \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU version for ARM64
# These are pre-installed in the ECR image
RUN pip3 install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

WORKDIR /app
COPY train.py /app/
RUN mkdir -p /data

CMD ["python3", "/app/train.py"]
