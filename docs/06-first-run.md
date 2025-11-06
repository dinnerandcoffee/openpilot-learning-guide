# 6. 첫 실행 및 테스트

빌드가 완료되었으니 이제 openpilot을 실행해봅시다. 실제 차량 없이도 시뮬레이션으로 테스트할 수 있습니다.

## 개요

**목표**: 
- openpilot 프로세스 이해
- 시뮬레이션 환경에서 실행
- 로그 분석 방법 배우기

**소요 시간**: 30분 - 1시간

## openpilot 실행 방식 이해

### 아키텍처 개요

openpilot은 여러 프로세스가 협력하는 분산 시스템입니다.

```
┌─────────────────────────────────────────────┐
│         manager.py (프로세스 관리자)           │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
┌─────▼─────┐ ┌──▼──────┐ ┌─▼─────────┐
│ camerad   │ │ modeld  │ │ controlsd │
│ (카메라)   │ │ (AI)    │ │ (제어)     │
└─────┬─────┘ └──┬──────┘ └─┬─────────┘
      │          │           │
      └──────────┼───────────┘
                 │
         ┌───────▼────────┐
         │  cereal (통신)  │
         └────────────────┘
```

**주요 프로세스**:

1. **manager.py**: 모든 프로세스 관리
2. **camerad**: 카메라 입력 처리
3. **modeld**: AI 비전 모델 (차선, 차량 감지)
4. **controlsd**: 조향/가속 제어 계산
5. **plannerd**: 경로 계획
6. **radard**: 레이더 처리 (차량에 따라)
7. **boardd**: panda(CAN 인터페이스)와 통신
8. **ui**: 사용자 인터페이스

### 통신 방식: cereal

모든 프로세스는 **cereal**을 통해 메시지를 주고받습니다.

```python
# cereal 메시지 예시
from cereal import messaging

# 구독 (메시지 받기)
sm = messaging.SubMaster(['carState', 'modelV2'])

while True:
    sm.update()
    car_state = sm['carState']
    model_output = sm['modelV2']
    
# 발행 (메시지 보내기)
pm = messaging.PubMaster(['controlsState'])
pm.send('controlsState', msg)
```

## 실행 전 준비

### 1. 환경 변수 설정

openpilot 실행에 필요한 환경 변수를 설정합니다.

```bash
# 가상 환경 활성화
cd ~/dev/openpilot
source venv/bin/activate

# 환경 변수 파일 생성 (선택사항)
cat > ~/.openpilot_env << 'EOF'
export OPENPILOT_ROOT="$HOME/dev/openpilot"
export PYTHONPATH="$OPENPILOT_ROOT:$PYTHONPATH"
EOF

# 적용
source ~/.openpilot_env

# .bashrc에 추가 (영구 적용)
echo 'source ~/.openpilot_env' >> ~/.bashrc
```

### 2. 시뮬레이션 모드 설정

실제 차량 없이 테스트하려면 시뮬레이션 플래그를 사용합니다.

```bash
# 환경 변수 설정
export SIMULATION=1
export SKIP_FW_QUERY=1
export FINGERPRINT="HYUNDAI SONATA 2020"
```

**환경 변수 설명**:
- `SIMULATION=1`: 시뮬레이션 모드
- `SKIP_FW_QUERY=1`: 펌웨어 쿼리 건너뛰기
- `FINGERPRINT`: 시뮬레이션할 차량 모델

## 방법 1: 개별 프로세스 실행

개발 및 디버깅 시 유용한 방법입니다.

### controlsd 단독 실행

```bash
# controlsd 실행
python selfdrive/controls/controlsd.py

# 출력 예시:
# controlsd is waiting for CarParams
# starting control loop
# ...
```

**Ctrl+C**로 종료할 수 있습니다.

### modeld 실행

AI 비전 모델을 실행합니다.

```bash
# GPU 사용 (NVIDIA)
python selfdrive/modeld/modeld.py

# CPU 모드 (느림)
USE_CPU_RUNTIME=1 python selfdrive/modeld/modeld.py
```

### 메시지 확인

다른 터미널에서 cereal 메시지를 확인:

```bash
# 새 터미널
cd ~/dev/openpilot
source venv/bin/activate

# 메시지 확인 도구
python -m cereal.services

# 특정 메시지 구독
python -c "
from cereal import messaging
sm = messaging.SubMaster(['controlsState'])
while True:
    sm.update()
    print(sm['controlsState'])
"
```

## 방법 2: manager 사용 (전체 실행)

manager가 모든 프로세스를 관리하게 합니다.

### manager 실행

```bash
# manager 실행
./launch_openpilot.sh

# 또는 직접
python selfdrive/manager/manager.py
```

**실행 과정**:
```
Starting openpilot v0.9.7
preparing to start 15 processes
starting process boardd
starting process camerad
starting process modeld
starting process controlsd
...
all processes started
```

### 로그 확인

```bash
# 로그 위치
ls -la /data/media/0/realdata/

# 실시간 로그 보기
tail -f /tmp/openpilot.log

# 또는
journalctl -u openpilot -f  # systemd 사용 시
```

## 방법 3: Replay (로그 재생)

실제 주행 로그를 재생하며 테스트합니다.

### 로그 다운로드

comma에서 제공하는 공개 주행 로그를 사용합니다.

```bash
# tools 디렉토리로 이동
cd ~/dev/openpilot/tools

# 로그 다운로드 (예시)
python lib/route.py "a2a0ccea32023010|2023-07-27--13-01-19"

# 로그 위치 확인
ls -lh ~/.comma/media/0/realdata/
```

### Replay 실행

```bash
# replay 도구 실행
cd ~/dev/openpilot

# 특정 route 재생
./tools/replay/replay "a2a0ccea32023010|2023-07-27--13-01-19"

# 옵션:
# --demo: UI 표시
# --dcam: 운전자 카메라 포함
```

**Replay 장점**:
- 실제 주행 데이터로 테스트
- 재현 가능한 환경
- 디버깅에 이상적

### UI와 함께 재생

```bash
# UI 실행 (다른 터미널)
cd ~/dev/openpilot
./selfdrive/ui/ui

# Replay 실행 (원래 터미널)
./tools/replay/replay --demo "a2a0ccea32023010|2023-07-27--13-01-19"
```

## 방법 4: 시뮬레이터 사용

CARLA 또는 커스텀 시뮬레이터와 연동합니다.

### openpilot-tools 설치

```bash
# tools 저장소 클론
cd ~/dev
git clone https://github.com/commaai/openpilot-tools.git

cd openpilot-tools
pip install -e .
```

### 시뮬레이터 브릿지

```bash
# 시뮬레이터 브릿지 실행
cd ~/dev/openpilot
python tools/sim/bridge.py

# 별도 터미널에서 openpilot 실행
./launch_openpilot.sh
```

## 주요 프로세스 상세

### controlsd (제어)

가장 중요한 프로세스 중 하나입니다.

```python
# selfdrive/controls/controlsd.py 주요 루프

def controlsd_thread():
    # 초기화
    CI, CP = get_car(...)  # 차량 인터페이스
    state = State.disabled  # 초기 상태
    
    # 메인 루프 (100Hz)
    while True:
        # 1. 입력 받기
        CS = sm['carState']         # 차량 상태
        model = sm['modelV2']       # AI 예측
        
        # 2. 제어 계산
        actuators = control(CS, model)
        
        # 3. 출력 전송
        pm.send('controlsState', actuators)
        
        # 4. 100Hz 유지
        time.sleep(0.01)
```

**주요 변수**:
- `CS.vEgo`: 현재 속도
- `CS.steeringAngleDeg`: 조향각
- `model.position`: AI 예측 경로
- `actuators.steer`: 계산된 조향 명령

### modeld (AI 비전)

카메라 이미지를 분석합니다.

```python
# selfdrive/modeld/modeld.py

def modeld_thread():
    # 모델 로드
    model = ModelRunner()
    
    while True:
        # 1. 카메라 이미지 받기
        img = sm['roadCameraState']
        
        # 2. AI 추론
        predictions = model.run(img)
        
        # 3. 결과 발행
        # - 차선 위치
        # - 선행 차량 거리
        # - 주행 경로
        pm.send('modelV2', predictions)
```

**출력 데이터**:
- 차선 라인 위치
- 선행 차량 상대 속도/거리
- 권장 경로

### plannerd (경로 계획)

안전하고 편안한 경로를 계획합니다.

```python
# selfdrive/controls/plannerd.py

def plannerd_thread():
    while True:
        # 입력
        model = sm['modelV2']
        car_state = sm['carState']
        
        # 경로 계획
        # - 차선 유지
        # - 차량 추종
        # - 속도 계획
        path, speed = plan(model, car_state)
        
        pm.send('lateralPlan', path)
        pm.send('longitudinalPlan', speed)
```

## 로그 분석

### 로그 구조

openpilot은 주행 데이터를 세그먼트 단위로 저장합니다.

```
/data/media/0/realdata/
└── 2024-01-15--10-30-00/  # Route
    ├── 0/                  # Segment 0
    │   ├── rlog.bz2        # 메시지 로그
    │   ├── qlog.bz2        # 쿼리 로그
    │   ├── fcamera.hevc    # 전방 카메라
    │   └── dcamera.hevc    # 운전자 카메라
    ├── 1/                  # Segment 1
    └── ...
```

### cabana (로그 뷰어)

```bash
# cabana 실행
cd ~/dev/openpilot/tools/cabana
python cabana.py

# 로그 파일 열기
# File → Open → rlog.bz2 선택
```

**cabana 기능**:
- 메시지 타임라인
- 그래프 시각화
- 메시지 검색
- DBC 파일 편집

### Python으로 로그 읽기

```python
#!/usr/bin/env python3
from tools.lib.logreader import LogReader

# 로그 읽기
lr = LogReader("rlog.bz2")

# 메시지 순회
for msg in lr:
    if msg.which() == 'carState':
        cs = msg.carState
        print(f"Speed: {cs.vEgo:.1f} m/s")
        print(f"Steering: {cs.steeringAngleDeg:.1f}°")
    
    elif msg.which() == 'controlsState':
        ctrl = msg.controlsState
        print(f"Enabled: {ctrl.enabled}")
        print(f"Desired steer: {ctrl.lateralControlState.steerAngle:.1f}°")
```

### plotjuggler (시각화)

```bash
# plotjuggler 설치
sudo apt install plotjuggler

# openpilot 로그를 CSV로 변환
cd ~/dev/openpilot/tools
python lib/route.py --export-csv "route_name"

# plotjuggler로 열기
plotjuggler data.csv
```

## 디버깅 팁

### 1. 특정 프로세스만 실행

```bash
# manager 수정해서 특정 프로세스만 실행
# selfdrive/manager/manager.py

# 또는 환경 변수로
BLOCK=ui,camerad python selfdrive/manager/manager.py
```

### 2. 로그 레벨 조정

```python
# 코드에 추가
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3. 메시지 모니터링

```bash
# 실시간 메시지 보기
python -m cereal.messaging.bridge

# 메시지 통계
python -m cereal.services
```

### 4. pdb 디버거

```python
# 코드에 브레이크포인트 추가
import pdb; pdb.set_trace()

# 실행 시 중단되어 대화형 디버깅 가능
```

## 성능 모니터링

### 프로세스 상태 확인

```bash
# CPU/메모리 사용량
htop

# openpilot 프로세스만
ps aux | grep python | grep selfdrive
```

### 메시지 레이턴시 확인

```python
from cereal import messaging

sm = messaging.SubMaster(['modelV2'])

while True:
    sm.update()
    lag = sm.lag('modelV2')  # 레이턴시 (ms)
    freq = sm.freq('modelV2')  # 주파수 (Hz)
    print(f"Lag: {lag:.1f}ms, Freq: {freq:.1f}Hz")
```

## 트러블슈팅

### 프로세스가 시작 안 됨

**문제**: `Failed to start camerad`

**해결**:
```bash
# 카메라 권한 확인
ls -la /dev/video*

# 사용자를 video 그룹에 추가
sudo usermod -aG video $USER

# 재로그인
```

### 메시지가 안 보임

**문제**: `SubMaster timeout`

**해결**:
```bash
# 발행자 프로세스 확인
ps aux | grep modeld

# 메시지 서비스 확인
python -m cereal.services
```

### GPU 오류 (modeld)

**문제**: `Failed to initialize GPU`

**해결**:
```bash
# CPU 모드로 전환
export USE_CPU_RUNTIME=1

# 또는 GPU 드라이버 설치
sudo apt install nvidia-driver-535
```

## 다음 단계

첫 실행을 성공적으로 마쳤습니다!

다음 Part에서는 openpilot의 핵심 개념들을 깊이 있게 다룹니다:
- 시스템 아키텍처
- cereal 메시징 시스템
- 주요 프로세스 동작 원리

---

[다음: Part 3 - 핵심 개념 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/07-architecture.md)
