# 7. 시스템 아키텍처

openpilot의 전체 구조를 이해해봅시다. 각 컴포넌트가 어떻게 협력하는지 알면 코드를 읽고 수정하기 훨씬 쉬워집니다.

## 개요

**목표**: openpilot의 전체 시스템 구조 이해

**핵심 개념**:
- 프로세스 기반 아키텍처
- Pub-Sub 메시징 패턴
- 100Hz 제어 루프

## 전체 구조도

### 하드웨어 레이어

```
┌─────────────────────────────────────────────────────┐
│                     comma 3X                        │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │
│  │ Cameras  │  │ GPS/IMU  │  │ Snapdragon SoC  │   │
│  └─────┬────┘  └────┬─────┘  └────────┬────────┘   │
└────────┼────────────┼─────────────────┼────────────┘
         │            │                 │
         └────────────┴─────────────────┘
                      │
┌─────────────────────▼─────────────────────┐
│              panda (CAN gateway)           │
│  - CAN 버스 통신                            │
│  - 차량 인터페이스                          │
└────────────────────┬──────────────────────┘
                     │
┌────────────────────▼──────────────────────┐
│               Car (차량)                   │
│  - Steering                                │
│  - Throttle/Brake                          │
│  - Sensors                                 │
└───────────────────────────────────────────┘
```

### 소프트웨어 레이어

```
┌─────────────────── openpilot ───────────────────┐
│                                                  │
│  ┌──────────────── manager ──────────────────┐  │
│  │  (프로세스 관리자)                          │  │
│  └──┬────────────────────────────────────┬───┘  │
│     │                                    │       │
│  ┌──▼──────────┐                  ┌──────▼───┐  │
│  │  Sensing    │                  │ Control  │  │
│  ├─────────────┤                  ├──────────┤  │
│  │ camerad     │───────┐  ┌───────│ plannerd │  │
│  │ sensord     │       │  │       │controlsd │  │
│  │ ubloxd      │       │  │       │ boardd   │  │
│  └─────────────┘       │  │       └──────────┘  │
│                        │  │                      │
│  ┌─────────────┐    ┌──▼──▼────┐  ┌──────────┐  │
│  │ Perception  │    │ cereal   │  │ UI/UX    │  │
│  ├─────────────┤    │(messaging)  │──────────┤  │
│  │ modeld      │◄───┤          ├──►│ ui       │  │
│  │ dmonitoringd│    │  pub/sub │  │ soundd   │  │
│  └─────────────┘    └──────────┘  └──────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

## 핵심 컴포넌트

### 1. Sensing (센싱)

차량과 환경 데이터를 수집합니다.

#### camerad
```python
# selfdrive/camerad/cameras/camera_common.cc
# 역할: 카메라 입력 처리

def camerad():
    cameras = [
        RoadCamera(),    # 전방 카메라 (1164x874, 20fps)
        DriverCamera(),  # 운전자 카메라
        WideCamera()     # 광각 카메라
    ]
    
    while True:
        for cam in cameras:
            frame = cam.read()
            publish('roadCameraState', frame)  # cereal로 발행
```

**출력 메시지**:
- `roadCameraState`: 전방 카메라 이미지
- `driverCameraState`: 운전자 모니터링 이미지
- `wideRoadCameraState`: 광각 이미지

**주요 파일**:
- `selfdrive/camerad/cameras/camera_qcom2.cc`
- `selfdrive/camerad/main.cc`

#### sensord
```python
# selfdrive/sensord/sensord.py
# 역할: IMU, 자이로, 가속도계 데이터

def sensord():
    imu = IMUSensor()
    
    while True:
        data = imu.read()
        publish('sensorEvents', {
            'acceleration': data.accel,
            'gyro': data.gyro,
            'orientation': data.orientation
        })
```

**출력 데이터**:
- 3축 가속도
- 3축 자이로
- 디바이스 방향

#### ubloxd
```python
# selfdrive/locationd/ubloxd.py
# 역할: GPS 데이터 처리

def ubloxd():
    gps = UbloxGPS()
    
    while True:
        position = gps.read()
        publish('ubloxGnss', {
            'latitude': position.lat,
            'longitude': position.lon,
            'altitude': position.alt,
            'speed': position.speed
        })
```

**GPS 데이터**:
- 위도/경도
- 고도
- 속도
- 정확도

### 2. Perception (인식)

센서 데이터를 해석하여 의미 있는 정보로 변환합니다.

#### modeld
```python
# selfdrive/modeld/modeld.py
# 역할: AI 비전 모델 실행

class ModelRunner:
    def __init__(self):
        self.model = SNPEModel('supercombo.dlc')
        
    def run(self, frame):
        # 전처리
        input_tensor = preprocess(frame)
        
        # AI 추론
        output = self.model.execute(input_tensor)
        
        # 후처리
        return {
            'lane_lines': parse_lanes(output),
            'lead_vehicle': parse_lead(output),
            'path': parse_path(output),
            'pose': parse_pose(output)
        }

def modeld():
    model = ModelRunner()
    sm = SubMaster(['roadCameraState'])
    pm = PubMaster(['modelV2'])
    
    while True:
        frame = sm['roadCameraState']
        predictions = model.run(frame.image)
        pm.send('modelV2', predictions)
```

**모델 출력**:

1. **차선 라인** (4개):
   ```python
   lane_lines = [
       left_left_line,   # 왼쪽 2차선
       left_line,        # 왼쪽 차선
       right_line,       # 오른쪽 차선
       right_right_line  # 오른쪽 2차선
   ]
   # 각 라인: 192개 점 (0~100m, 0.5m 간격)
   ```

2. **선행 차량**:
   ```python
   lead = {
       'prob': 0.95,           # 감지 확률
       'x': [50.0, ...],       # 상대 거리 (m)
       'v': [5.0, ...],        # 상대 속도 (m/s)
       'a': [0.5, ...],        # 상대 가속도 (m/s²)
   }
   ```

3. **주행 경로**:
   ```python
   path = {
       'x': [0, 1, 2, ..., 100],  # 전방 거리
       'y': [0, 0.1, 0.2, ...],   # 좌우 오프셋
       'prob': 0.99                # 신뢰도
   }
   ```

**모델 파일**:
- `supercombo.dlc`: 메인 모델 (Qualcomm SNPE)
- 입력: 1164x874 RGB 이미지
- 출력: 수천 개의 값 (차선, 차량, 경로 등)

#### dmonitoringd
```python
# selfdrive/modeld/dmonitoringd.py
# 역할: 운전자 모니터링

def dmonitoringd():
    model = DriverModel()
    sm = SubMaster(['driverCameraState'])
    pm = PubMaster(['driverMonitoringState'])
    
    while True:
        frame = sm['driverCameraState']
        
        result = model.run(frame.image)
        # - 얼굴 위치
        # - 시선 방향
        # - 눈 감김 여부
        
        pm.send('driverMonitoringState', {
            'faceProb': result.face_prob,
            'facePosition': result.face_pos,
            'isDistracted': result.distracted
        })
```

### 3. Planning (계획)

인식 결과를 바탕으로 주행 계획을 세웁니다.

#### plannerd
```python
# selfdrive/controls/plannerd.py
# 역할: 경로 및 속도 계획

def plannerd():
    sm = SubMaster([
        'modelV2',      # AI 예측
        'carState',     # 차량 상태
        'radarState'    # 레이더 (옵션)
    ])
    pm = PubMaster([
        'lateralPlan',      # 횡방향 계획
        'longitudinalPlan'  # 종방향 계획
    ])
    
    while True:
        sm.update()
        
        # 횡방향 (조향)
        lateral = compute_lateral_plan(
            sm['modelV2'].laneLines,
            sm['modelV2'].path,
            sm['carState']
        )
        
        # 종방향 (속도)
        longitudinal = compute_longitudinal_plan(
            sm['modelV2'].lead,
            sm['carState'].vEgo,
            sm['carState'].aEgo
        )
        
        pm.send('lateralPlan', lateral)
        pm.send('longitudinalPlan', longitudinal)
```

**lateralPlan (횡방향)**:
```python
{
    'dPoly': [c0, c1, c2, c3],  # 경로 다항식 (d = c0 + c1*x + c2*x² + c3*x³)
    'laneWidth': 3.5,            # 차선 폭 (m)
    'curvature': 0.01,           # 곡률 (1/m)
    'desire': Desire.keepLane    # 의도 (차선 유지/변경)
}
```

**longitudinalPlan (종방향)**:
```python
{
    'vTarget': 25.0,        # 목표 속도 (m/s)
    'aTarget': -0.5,        # 목표 가속도 (m/s²)
    'distances': [...],     # 거리 계획
    'speeds': [...],        # 속도 계획
    'accels': [...],        # 가속도 계획
}
```

### 4. Control (제어)

계획을 실제 조향/가속 명령으로 변환합니다.

#### controlsd
```python
# selfdrive/controls/controlsd.py
# 역할: 주 제어 루프 (100Hz)

class Controls:
    def __init__(self):
        self.lat_control = LatControl()  # 조향 제어
        self.long_control = LongControl() # 속도 제어
        
    def update(self, sm):
        # 1. 상태 업데이트
        CS = sm['carState']
        
        # 2. 횡방향 제어 (조향)
        lat_plan = sm['lateralPlan']
        steer = self.lat_control.update(lat_plan, CS)
        
        # 3. 종방향 제어 (속도)
        long_plan = sm['longitudinalPlan']
        accel = self.long_control.update(long_plan, CS)
        
        return {
            'steer': steer,
            'accel': accel
        }

def controlsd():
    controls = Controls()
    sm = SubMaster([
        'carState', 'lateralPlan', 'longitudinalPlan',
        'modelV2', 'driverMonitoringState'
    ])
    pm = PubMaster(['controlsState', 'carControl'])
    
    # 100Hz 루프
    while True:
        t_start = time.monotonic()
        
        sm.update()
        actuators = controls.update(sm)
        
        pm.send('carControl', actuators)
        
        # 정확히 10ms 유지
        dt = time.monotonic() - t_start
        time.sleep(max(0, 0.01 - dt))
```

**제어 알고리즘**:

1. **횡방향 (INDI)**:
   ```python
   # Incremental Nonlinear Dynamic Inversion
   def lateral_control(plan, state):
       error = plan.dPoly[0]  # 경로 오프셋
       d_error = plan.dPoly[1]  # 경로 기울기
       
       steer_rate = -K1 * error - K2 * d_error
       steer = steer_prev + steer_rate * dt
       
       return steer
   ```

2. **종방향 (PID)**:
   ```python
   def longitudinal_control(plan, state):
       v_error = plan.vTarget - state.vEgo
       
       # PID
       P = Kp * v_error
       I += Ki * v_error * dt
       D = Kd * (v_error - prev_error) / dt
       
       accel = P + I + D
       return clip(accel, -4.0, 2.0)  # 제한
   ```

#### boardd
```python
# selfdrive/boardd/boardd.cc
# 역할: panda(CAN 인터페이스)와 통신

def boardd():
    panda = Panda()
    sm = SubMaster(['carControl'])
    pm = PubMaster(['carState', 'can'])
    
    while True:
        # 1. 차량에서 CAN 메시지 받기
        can_msgs = panda.can_recv()
        car_state = parse_can(can_msgs)
        pm.send('carState', car_state)
        
        # 2. 제어 명령을 CAN으로 전송
        control = sm['carControl']
        can_cmds = generate_can_commands(control)
        panda.can_send(can_cmds)
```

**panda 인터페이스**:
```
┌──────────────┐
│   boardd     │
└──────┬───────┘
       │ USB
┌──────▼───────┐
│    panda     │  (STM32 마이크로컨트롤러)
└──────┬───────┘
       │ CAN
┌──────▼───────┐
│  Car ECUs    │
└──────────────┘
```

### 5. UI/UX

사용자 인터페이스를 담당합니다.

#### ui
```python
# selfdrive/ui/ui.cc (C++로 작성)
# 역할: 화면 렌더링

def ui_thread():
    sm = SubMaster([
        'modelV2',
        'carState',
        'controlsState',
        'driverMonitoringState'
    ])
    
    while True:
        sm.update()
        
        # 화면 그리기
        draw_lane_lines(sm['modelV2'])
        draw_lead_car(sm['modelV2'])
        draw_speed(sm['carState'])
        draw_alerts(sm['controlsState'])
        
        display.swap_buffers()
```

**UI 요소**:
- 차선 라인 시각화
- 선행 차량 표시
- 현재 속도
- 경고 메시지
- 운전자 모니터링 상태

## 데이터 흐름

### 전체 파이프라인

```
1. 센싱
   카메라 → camerad → roadCameraState
   GPS → ubloxd → ubloxGnss
   IMU → sensord → sensorEvents
   
2. 인식
   roadCameraState → modeld → modelV2
   driverCameraState → dmonitoringd → driverMonitoringState
   
3. 계획
   modelV2 + carState → plannerd → lateralPlan + longitudinalPlan
   
4. 제어
   lateralPlan + longitudinalPlan + carState → controlsd → carControl
   
5. 실행
   carControl → boardd → panda → CAN → Car
```

### 메시지 주파수

| 메시지 | 주파수 | 생성자 | 소비자 |
|--------|--------|--------|--------|
| roadCameraState | 20 Hz | camerad | modeld, ui |
| modelV2 | 20 Hz | modeld | plannerd, ui |
| carState | 100 Hz | boardd | 모든 프로세스 |
| controlsState | 100 Hz | controlsd | ui, logging |
| lateralPlan | 20 Hz | plannerd | controlsd |
| longitudinalPlan | 20 Hz | plannerd | controlsd |
| carControl | 100 Hz | controlsd | boardd |

### 레이턴시 예시

```
전체 레이턴시 (카메라 → 제어 출력):

카메라 캡처          : T + 0ms
camerad 처리         : T + 10ms
modeld AI 추론       : T + 60ms
plannerd 계획        : T + 65ms
controlsd 제어       : T + 70ms
boardd CAN 전송      : T + 75ms
───────────────────────────────
총 레이턴시          : ~75ms
```

## 프로세스 관리

### manager.py

```python
# selfdrive/manager/manager.py

managed_processes = {
    'camerad': ('selfdrive.camerad.main', True),
    'modeld': ('selfdrive.modeld.modeld', True),
    'controlsd': ('selfdrive.controls.controlsd', True),
    'plannerd': ('selfdrive.controls.plannerd', True),
    'boardd': ('selfdrive.boardd.boardd', True),
    'ui': ('selfdrive.ui.ui', True),
    # ... 더 많은 프로세스
}

def manager_thread():
    # 1. 프로세스 시작
    for name, (module, enabled) in managed_processes.items():
        if enabled:
            start_process(name, module)
    
    # 2. 프로세스 감시
    while True:
        for name in managed_processes:
            if not is_alive(name):
                restart_process(name)
        
        time.sleep(1)
```

### 프로세스 간 의존성

```
manager
├── camerad (독립)
├── sensord (독립)
├── ubloxd (독립)
├── boardd (독립)
├── modeld (depends: camerad)
├── dmonitoringd (depends: camerad)
├── plannerd (depends: modeld, boardd)
├── controlsd (depends: plannerd, boardd, modeld)
└── ui (depends: 모든 프로세스)
```

## 안전 메커니즘

### 1. Watchdog

```python
# selfdrive/controls/controlsd.py

def controlsd():
    watchdog_timer = 0
    
    while True:
        # 메시지 수신 확인
        if sm.updated['carState']:
            watchdog_timer = 0
        else:
            watchdog_timer += dt
        
        # 타임아웃 시 비활성화
        if watchdog_timer > 0.5:  # 500ms
            print("WATCHDOG: carState timeout!")
            disable_controls()
```

### 2. Safety Model (panda)

panda 펌웨어에는 하드웨어 레벨의 안전 검사가 있습니다.

```c
// panda/board/safety/safety_hyundai.h

bool hyundai_tx_hook(CANPacket_t *to_send) {
    // 조향 제한 검사
    int desired_steer = GET_BYTE(to_send, 0);
    
    if (abs(desired_steer - actual_steer) > MAX_STEER_DELTA) {
        return false;  // 거부
    }
    
    if (abs(desired_steer) > MAX_STEER) {
        return false;  // 거부
    }
    
    return true;  // 허용
}
```

### 3. Alerts

```python
# selfdrive/controls/lib/alerts.py

class Alert:
    def __init__(self, text, priority):
        self.text = text
        self.priority = priority  # LOW, MID, HIGH, CRITICAL

alerts = {
    'steerUnavailable': Alert(
        "TAKE CONTROL IMMEDIATELY: Steering Unavailable",
        Priority.CRITICAL
    ),
    'driverDistracted': Alert(
        "PAY ATTENTION: Driver Distracted",
        Priority.HIGH
    ),
}
```

## 다음 단계

시스템 아키텍처를 이해했으니, 다음 장에서는 cereal 메시징 시스템을 깊이 있게 알아봅시다.

---

[다음: 8. cereal 메시징 시스템 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/08-cereal.md)
