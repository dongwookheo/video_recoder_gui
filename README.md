# Video Recorder GUI
비디오 레코더 GUI. [OpenCV](https://opencv.org/) & [PyQt6](https://www.qt.io/qt-for-python)를 곁들인

## Dependencies
- OpenCV4
- PyQt6

## How to use
![image](https://github.com/user-attachments/assets/205252ad-205e-4b32-8241-59496f64279b)
1. `main.py`를 실행한다.
2. IP 카메라를 사용하고 싶다면, 빨간 박스 안에 RTSP 주소를 입력한다.  
   2-a. `Update RTSP` 버튼을 클릭하거나 키보드의 `Enter` 혹은 `Return` 키를 누르면 영상이 전환된다.
3. Grayscale 영상으로 전환하고 싶은 경우, `Enable Grayscale` 버튼을 클릭하거나 키보드의 `G` 키를 누르면 전환된다.
4. 영상을 비디오로 저장하고 싶은 경우, `Record` 버튼을 클릭하거나 키보드의 `Spacebar` 키를 누른다.  
   4-a. 다시 한 번 반복해서 누르면, 영상 저장이 종료된다.  
   4.b. 코덱을 변경하고 싶은 경우, 영상을 저장하기 전에 초록 박스 안에 해당되는 코덱을 입력한다. (기본값은 `XVID`)
5. 영상을 이미지로 저장하고 싶은 경우, `Save to Images` 버튼을 클릭하거나 키보드의 `S` 키를 누른다.
   5-a. 다시 한 번 반복해서 누르면, 이미지 저장이 종료된다.
6. 종료하고 싶은 경우, `Quit` 버튼을 클릭하거나 키보드의 `ESC` 키를 누른다.


## Todo
- Argparse
- Apply deepfakes with [Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam)  

I tested with Bukayo Saka, my favorite football player at Arsenal.  

[Screencast from 10-16-2024 07:04:32 PM.webm](https://github.com/user-attachments/assets/997c78a9-87fa-4268-8a5b-d35756465dd7)
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
