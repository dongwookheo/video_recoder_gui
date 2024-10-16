FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y ssh && \
    apt-get install -y gcc && \
    apt-get install -y g++ && \
    apt-get install -y gdb && \
    apt-get install -y clang && \
    apt-get install -y rsync && \
    apt-get install -y tar && \
    apt-get install -y mesa-utils && \
    apt-get install -y git && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-tk && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install X11 related packages
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglu1-mesa-dev && \
    apt-get install -y mesa-common-dev && \
    apt-get install -y x11-utils && \
    apt-get install -y x11-apps && \
    apt-get install -y zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Deep-Live-Cam
RUN cd / && \
    git clone https://github.com/hacksider/Deep-Live-Cam.git && \
    cd Deep-Live-Cam && \
    pip install -r requirements.txt

# Download model
RUN cd /Deep-Live-Cam/models && \
    apt-get install -y wget && \
    wget https://huggingface.co/hacksider/deep-live-cam/resolve/main/GFPGANv1.4.pth -O ./GFPGANv1.4.pth && \
    wget https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx -O ./inswapper_128_fp16.onnx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
