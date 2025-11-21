# infra/docker/Dockerfile.ml
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential \
    git wget curl \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN pip install --upgrade pip

# PyTorch CUDA
RUN pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1 \
    --index-url https://download.pytorch.org/whl/cu121

# ML deps
COPY ml/requirements.txt ./ml_requirements.txt
RUN pip install --no-cache-dir -r ml_requirements.txt

# Copy ML code
COPY ml/ ./ml/

# Default command (override this when you run other jobs)
CMD ["python", "-m", "ml.training.train_contrastive"]
