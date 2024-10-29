import cv2
import datetime
import os

# 저장할 디렉토리 생성
if not os.path.exists("videos"):
    os.makedirs("videos")
if not os.path.exists("captures"):
    os.makedirs("captures")

cap = cv2.VideoCapture("./videos/checkerboard.mp4")  # 웹캠 연결

# 프레임 크기 설정
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"frame_width: {frame_width}, frame_height: {frame_height}")
fps = 50

# 비디오 저장을 위한 변수
is_recording = False
out = None
cnt = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 키 입력 처리
    key = cv2.waitKey(int(1000 / fps + 0.5)) & 0xFF

    # ESC 키를 누르면 종료
    if key == 27:
        break
    # 's' 키를 누르면 비디오 녹화 시작/정지
    elif key == ord("s"):
        if not is_recording:
            # 현재 시간을 파일명으로 사용
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"videos/video_{timestamp}.mp4"

            # VideoWriter 객체 생성
            out = cv2.VideoWriter(
                video_filename,
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (frame_width, frame_height),
            )
            is_recording = True
            print(f"녹화 시작: {video_filename}")
        else:
            # 녹화 종료
            out.release()
            is_recording = False
            print("녹화 종료")

    # 'c' 키를 누르면 이미지 캡처
    elif key == ord("c"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"captures/{cnt:04d}.jpg"
        cnt += 1
        cv2.imwrite(image_filename, frame)
        print(f"이미지 저장: {image_filename}")

    # 녹화 중이면 프레임 저장
    if is_recording:
        out.write(frame)

    # 현재 녹화 중임을 표시
    if is_recording:
        # 빨간 원을 그려서 녹화 중임을 표시
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)

    # 프레임 표시
    cv2.imshow("Camera", frame)

# 자원 해제
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
