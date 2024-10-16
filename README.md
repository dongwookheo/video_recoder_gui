```
cd /path/to/Dockerfile
docker build -t deep_live_cam:v1.0 .
```

```
docker run -it --privileged --gpus all --net=host --ipc=host \
-e "DISPLAY=$DISPLAY" \
-e "QT_X11_NO_MITSHM=1" \
-e NVIDIA_DRIVER_CAPABILITIES=all \
-v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
-v "/your/dataset/path:/dataset" \
deep_live_cam:v1.0
```