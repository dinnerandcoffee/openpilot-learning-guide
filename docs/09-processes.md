# 9. 주요 프로세스 깊이 알기

openpilot의 핵심 프로세스들을 하나씩 깊이 있게 분석해봅시다.

## 개요

이 장에서 다룰 프로세스:
1. **controlsd** - 제어 루프
2. **plannerd** - 경로 계획
3. **modeld** - AI 비전
4. **boardd** - 차량 인터페이스

## 1. controlsd - 제어의 심장

### 역할

controlsd는 openpilot의 **메인 제어 루프**입니다.

```
입력:
- carState (차량 상태)
- lateralPlan (조향 계획)
- longitudinalPlan (속도 계획)
- modelV2 (AI 예측)
- driverMonitoringState (운전자 상태)

출력:
- carControl (차량 제어 명령)
- controlsState (제어 상태)

주기: 100 Hz (10ms마다)
```

### 메인 루프

```python
# selfdrive/controls/controlsd.py

def controlsd_thread():
    # 1. 초기화
    sm = SubMaster([
        'carState', 'carParams',
        'lateralPlan', 'longitudinalPlan',
        'modelV2', 'driverMonitoringState'
    ])
    pm = PubMaster(['controlsState', 'carControl'])
    
    # 차량 인터페이스 로드
    CI, CP = get_car(sm['carParams'])
    
    # 제어기 초기화
    state_control = StateControl(CP)
    events = Events()
    
    # 2. 메인 루프 (100Hz)
    rk = Ratekeeper(100, print_delay_threshold=None)
    
    while True:
        # 2.1 메시지 수신
        sm.update()
        
        # 2.2 상태 업데이트
        CS = sm['carState']
        
        # 2.3 이벤트 처리
        events.clear()
        events.add_from_carstate(CS)
        
        # 2.4 상태 머신
        state_control.update(CS, events)
        
        # 2.5 제어 계산
        if state_control.state == State.enabled:
            actuators = compute_actuators(sm)
        else:
            actuators = CarControl.Actuators.new_message()
        
        # 2.6 안전 검사
        actuators = apply_safety_limits(actuators, CS, CP)
        
        # 2.7 메시지 발행
        pm.send('carControl', build_car_control(actuators))
        pm.send('controlsState', build_controls_state(state_control))
        
        # 2.8 100Hz 유지
        rk.keep_time()
```

### 상태 머신

controlsd는 다음 상태들을 관리합니다:

```python
class State:
    disabled = 0      # 비활성
    preEnabled = 1    # 활성화 준비
    enabled = 2       # 활성
    softDisabling = 3 # 부드러운 비활성화
    
class StateControl:
    def update(self, CS, events):
        # disabled → preEnabled
        if self.state == State.disabled:
            if cruise_button_pressed(CS):
                if all_conditions_met(CS, events):
                    self.state = State.preEnabled
        
        # preEnabled → enabled
        elif self.state == State.preEnabled:
            if hands_on_wheel(CS) and no_errors(events):
                self.state = State.enabled
        
        # enabled → softDisabling
        elif self.state == State.enabled:
            if has_critical_event(events):
                self.state = State.softDisabling
        
        # softDisabling → disabled
        elif self.state == State.softDisabling:
            if actuators_at_zero():
                self.state = State.disabled
```

### 횡방향 제어 (조향)

```python
# selfdrive/controls/controlsd.py

def compute_lateral_actuators(sm, v_ego):
    # 계획 가져오기
    lateral_plan = sm['lateralPlan']
    
    # 제어 알고리즘 선택
    if CP.lateralTuning.which() == 'indi':
        # INDI (Incremental Nonlinear Dynamic Inversion)
        return indi_control(lateral_plan, v_ego)
    
    elif CP.lateralTuning.which() == 'pid':
        # PID
        return pid_control(lateral_plan, v_ego)
    
    elif CP.lateralTuning.which() == 'lqr':
        # LQR (Linear Quadratic Regulator)
        return lqr_control(lateral_plan, v_ego)

# INDI 제어 예시
def indi_control(plan, v_ego):
    # 경로 다항식: d = c0 + c1*x + c2*x² + c3*x³
    c0, c1, c2, c3 = plan.dPoly
    
    # 현재 오프셋과 각도
    d = c0                    # 경로에서 떨어진 거리
    psi = c1                  # 경로 각도
    
    # 목표 조향각 계산
    # (look-ahead 거리를 고려)
    look_ahead = v_ego * 0.5  # 속도 비례
    d_future = c0 + c1*look_ahead + c2*look_ahead**2
    
    # 제어 게인
    K_d = 2.0    # 거리 게인
    K_psi = 5.0  # 각도 게인
    
    # 조향각 계산
    steer_angle = -(K_d * d_future + K_psi * psi)
    
    # 제한
    steer_angle = clip(steer_angle, -MAX_STEER, MAX_STEER)
    
    return steer_angle
```

### 종방향 제어 (속도)

```python
# selfdrive/controls/controlsd.py

def compute_longitudinal_actuators(sm, v_ego):
    # 계획 가져오기
    long_plan = sm['longitudinalPlan']
    
    # 목표 속도와 가속도
    v_target = long_plan.vTarget
    a_target = long_plan.aTarget
    
    # PID 제어
    v_error = v_target - v_ego
    
    # P: 비례
    P = Kp * v_error
    
    # I: 적분 (누적 오차)
    I_error += v_error * DT
    I = Ki * I_error
    
    # D: 미분 (변화율)
    D = Kd * (v_error - prev_error) / DT
    
    # 제어 출력
    accel = P + I + D
    
    # 목표 가속도 고려
    accel += a_target
    
    # 제한
    accel = clip(accel, MIN_ACCEL, MAX_ACCEL)
    
    # Anti-windup (적분 포화 방지)
    if accel == MIN_ACCEL or accel == MAX_ACCEL:
        I_error = prev_I_error
    
    return accel
```

### 이벤트 시스템

```python
# selfdrive/controls/lib/events.py

class Events:
    def __init__(self):
        self.events = []
    
    def add(self, event_name, static=False):
        self.events.append(Alert.get(event_name))
    
    def add_from_carstate(self, CS):
        # 차량 상태 기반 이벤트
        if CS.doorOpen:
            self.add('doorOpen')
        
        if CS.seatbeltUnlatched:
            self.add('seatbeltNotLatched')
        
        if CS.espDisabled:
            self.add('espDisabled')
    
    def has_critical(self):
        return any(e.priority == Priority.CRITICAL 
                   for e in self.events)

# 이벤트 정의
EVENTS = {
    'doorOpen': Alert(
        "Door Open",
        "Check Door",
        Priority.LOW
    ),
    'seatbeltNotLatched': Alert(
        "Seatbelt Unlatched",
        "Fasten Seatbelt",
        Priority.MID
    ),
    'steerUnavailable': Alert(
        "TAKE CONTROL IMMEDIATELY",
        "Steering Unavailable",
        Priority.CRITICAL
    ),
}
```

## 2. plannerd - 경로 계획자

### 역할

plannerd는 AI 예측을 바탕으로 **안전하고 편안한 경로**를 계획합니다.

```
입력:
- modelV2 (AI 예측: 차선, 선행차)
- carState (현재 속도, 가속도)
- controlsState (현재 제어 상태)

출력:
- lateralPlan (조향 계획)
- longitudinalPlan (속도 계획)

주기: 20 Hz (50ms마다)
```

### 횡방향 계획

```python
# selfdrive/controls/plannerd.py

def compute_lateral_plan(model, CS):
    # 1. 차선 라인 선택
    # (왼쪽 차선, 오른쪽 차선)
    left_lane = model.laneLines[1]
    right_lane = model.laneLines[2]
    
    # 2. 차선 중앙 계산
    if left_lane.prob > 0.5 and right_lane.prob > 0.5:
        # 양쪽 차선 모두 보임
        path_y = (left_lane.y + right_lane.y) / 2
    elif left_lane.prob > 0.5:
        # 왼쪽만
        path_y = left_lane.y + LANE_WIDTH / 2
    elif right_lane.prob > 0.5:
        # 오른쪽만
        path_y = right_lane.y - LANE_WIDTH / 2
    else:
        # 차선 안 보임 → 모델 경로 사용
        path_y = model.position.y
    
    # 3. 경로를 다항식으로 피팅
    # d = c0 + c1*x + c2*x² + c3*x³
    path_x = np.array(model.position.x)
    coeffs = np.polyfit(path_x, path_y, 3)
    
    # 4. 차선 폭 추정
    if left_lane.prob > 0.5 and right_lane.prob > 0.5:
        lane_width = np.mean(right_lane.y - left_lane.y)
    else:
        lane_width = DEFAULT_LANE_WIDTH
    
    # 5. 곡률 계산
    # κ = d²y/dx² / (1 + (dy/dx)²)^(3/2)
    curvature = (2*coeffs[1]) / (1 + coeffs[2]**2)**1.5
    
    return {
        'dPoly': coeffs,
        'laneWidth': lane_width,
        'curvature': curvature
    }
```

### 종방향 계획

```python
# selfdrive/controls/plannerd.py

def compute_longitudinal_plan(model, CS, controls_state):
    # 1. 선행 차량 확인
    lead = model.leadsV3[0]  # 가장 가까운 차량
    
    if lead.prob > 0.5:
        # 선행 차량 있음 → 추종 모드
        return follow_lead(lead, CS, controls_state)
    else:
        # 선행 차량 없음 → 크루즈 모드
        return cruise_control(CS, controls_state)

def follow_lead(lead, CS, controls_state):
    # 목표 시간 간격 (time headway)
    T_target = 1.8  # 초
    
    # 현재 거리와 속도
    d = lead.x[0]           # 거리 (m)
    v_rel = lead.v[0]       # 상대 속도 (m/s)
    v_ego = CS.vEgo         # 내 속도
    v_lead = v_ego + v_rel  # 선행차 속도
    
    # 목표 거리
    d_target = v_ego * T_target + D_min
    
    # 거리 오차
    d_error = d - d_target
    
    # 목표 속도 계산
    # (거리 오차를 속도로 변환)
    K_d = 0.5
    v_target = v_lead + K_d * d_error
    
    # 목표 가속도
    # (선행차 가속도 + 거리 보정)
    a_lead = lead.a[0]
    a_target = a_lead + 0.3 * d_error
    
    # 제한
    v_target = clip(v_target, 0, controls_state.vCruise)
    a_target = clip(a_target, -4.0, 2.0)
    
    return {
        'vTarget': v_target,
        'aTarget': a_target,
        'distances': [...],  # 궤적
        'speeds': [...],
        'accels': [...]
    }

def cruise_control(CS, controls_state):
    # 단순히 설정 속도 유지
    v_target = controls_state.vCruise
    a_target = 0.0
    
    # 현재 속도와의 차이
    v_error = v_target - CS.vEgo
    
    # 부드러운 가속
    if v_error > 0:
        a_target = min(1.0, v_error * 0.5)
    else:
        a_target = max(-2.0, v_error * 0.5)
    
    return {
        'vTarget': v_target,
        'aTarget': a_target,
        'distances': [...],
        'speeds': [...],
        'accels': [...]
    }
```

### 편안함 최적화

```python
# Jerk (가속도 변화율) 최소화
def smooth_trajectory(v_current, a_current, v_target, a_target):
    # Jerk 제한
    MAX_JERK = 2.0  # m/s³
    
    # 목표 가속도 변화
    da = a_target - a_current
    
    # Jerk 제한 적용
    da = clip(da, -MAX_JERK * DT, MAX_JERK * DT)
    
    # 부드러운 가속도
    a_smooth = a_current + da
    
    return a_smooth
```

## 3. modeld - AI의 눈

### 역할

modeld는 **카메라 이미지를 분석**하여 도로 상황을 이해합니다.

```
입력:
- roadCameraState (카메라 이미지)
- driverCameraState (운전자 카메라)

출력:
- modelV2 (예측: 차선, 차량, 경로)
- driverMonitoringState (운전자 상태)

주기: 20 Hz (카메라와 동기)
```

### 모델 실행

```python
# selfdrive/modeld/modeld.py

class ModelRunner:
    def __init__(self):
        # SNPE 모델 로드
        self.model = SNPEModel(
            'supercombo.dlc',
            use_gpu=True
        )
        
        # 입력/출력 버퍼
        self.input_buffer = np.zeros((1, 384, 512, 12), dtype=np.float32)
        self.output_buffer = None
    
    def run(self, camera_frame):
        # 1. 전처리
        img = preprocess_frame(camera_frame)
        
        # 2. 모델 실행
        self.model.execute(img, self.output_buffer)
        
        # 3. 후처리
        result = postprocess_output(self.output_buffer)
        
        return result

def preprocess_frame(frame):
    # 1. YUV → RGB 변환
    rgb = yuv_to_rgb(frame)
    
    # 2. 크롭 및 리사이즈
    # (1164, 874) → (384, 512)
    cropped = rgb[200:1074, :]
    resized = cv2.resize(cropped, (512, 384))
    
    # 3. 정규화
    normalized = (resized / 255.0 - 0.5) / 0.5
    
    # 4. 시간 축 추가 (현재 + 과거 프레임)
    # 12 채널 = RGB * 4프레임
    temporal = stack_temporal_frames(normalized)
    
    return temporal
```

### 모델 출력 파싱

```python
# selfdrive/modeld/parse_model_outputs.py

def postprocess_output(raw_output):
    # 출력 텐서 크기: (1, 6400)
    # 각 부분을 파싱
    
    result = {}
    offset = 0
    
    # 1. 차선 라인 (4개 × 192점 × 3좌표)
    lane_lines = []
    for i in range(4):
        x = raw_output[offset:offset+192]
        y = raw_output[offset+192:offset+384]
        z = raw_output[offset+384:offset+576]
        
        lane_lines.append({
            'x': x,
            'y': y,
            'z': z,
            'prob': sigmoid(raw_output[offset+576])
        })
        offset += 577
    
    result['laneLines'] = lane_lines
    
    # 2. 선행 차량 (2개)
    leads = []
    for i in range(2):
        leads.append({
            'prob': sigmoid(raw_output[offset]),
            'x': raw_output[offset+1:offset+101],   # 100점
            'y': raw_output[offset+101:offset+201],
            'v': raw_output[offset+201:offset+301],
            'a': raw_output[offset+301:offset+401]
        })
        offset += 401
    
    result['leadsV3'] = leads
    
    # 3. 경로
    result['position'] = {
        'x': np.arange(0, 100, 0.5),  # 고정
        'y': raw_output[offset:offset+200],
        'z': raw_output[offset+200:offset+400]
    }
    offset += 400
    
    # 4. 차선 확률
    result['laneLineProbs'] = raw_output[offset:offset+4]
    
    return result
```

### 모델 아키텍처

```
입력: (384, 512, 12) RGB 이미지 × 4프레임
       ↓
┌──────────────────┐
│   Backbone        │
│   EfficientNet-B0 │  특징 추출
│   (pretrained)    │
└─────────┬────────┘
          ↓
┌─────────┴────────┐
│   Temporal       │  시간 정보 통합
│   Aggregation    │  (GRU/LSTM)
└─────────┬────────┘
          ↓
    ┌─────┴──────┐
    │            │
┌───▼──┐    ┌───▼──┐
│ Head1│    │ Head2│  다중 출력
│Lanes │    │Leads │
└──────┘    └──────┘
    ↓           ↓
출력: 차선, 차량, 경로
```

## 4. boardd - 차량 인터페이스

### 역할

boardd는 **panda와 통신**하여 차량 CAN 버스를 읽고 씁니다.

```
입력:
- carControl (제어 명령)

출력:
- carState (차량 상태)
- can (raw CAN 메시지)

주기: 100 Hz
```

### CAN 메시지 파싱

```python
# selfdrive/boardd/boardd.cc (간소화)

def boardd_thread():
    # Panda 연결
    panda = Panda()
    
    # 차량 인터페이스
    from selfdrive.car import CarInterface
    CI = CarInterface(...)
    
    sm = SubMaster(['carControl'])
    pm = PubMaster(['carState', 'can'])
    
    while True:
        # 1. CAN 메시지 읽기
        can_msgs = panda.can_recv()
        
        # 2. 파싱
        CS = CI.update(can_msgs)
        
        # 3. 발행
        pm.send('carState', CS)
        pm.send('can', can_msgs)
        
        # 4. 제어 명령 전송
        if sm.updated['carControl']:
            CC = sm['carControl']
            can_sends = CI.apply(CC, CS)
            panda.can_send_many(can_sends)
        
        time.sleep(0.01)  # 100Hz
```

### CAN 메시지 예시 (Hyundai)

```python
# selfdrive/car/hyundai/carstate.py

def update(self, can_msgs):
    CS = CarState()
    
    for msg in can_msgs:
        # 속도 (0x4F1)
        if msg.address == 0x4F1:
            CS.vEgo = (msg.data[0] << 8 | msg.data[1]) * 0.01
        
        # 조향각 (0x2B0)
        elif msg.address == 0x2B0:
            angle_raw = msg.data[0] << 8 | msg.data[1]
            CS.steeringAngleDeg = (angle_raw - 32768) * 0.1
        
        # 브레이크 (0x50)
        elif msg.address == 0x50:
            CS.brakePressed = bool(msg.data[6] & 0x80)
        
        # 가스 (0x37)
        elif msg.address == 0x37:
            CS.gas = msg.data[0] / 255.0
    
    return CS
```

### 제어 명령 생성

```python
# selfdrive/car/hyundai/carcontroller.py

def apply(self, CC, CS):
    can_sends = []
    
    # 1. 조향 명령
    steer_cmd = make_can_msg(
        address=0x340,
        data=[
            int(CC.actuators.steer * 100) & 0xFF,
            (int(CC.actuators.steer * 100) >> 8) & 0xFF,
            0x00,
            0x00,
            checksum(...)
        ]
    )
    can_sends.append(steer_cmd)
    
    # 2. 속도 명령 (ACC)
    if CC.cruiseControl.cancel:
        accel_cmd = make_can_msg(
            address=0x4A0,
            data=[0x00, 0x00, 0x00, 0x00, 0x00]
        )
    else:
        target_accel = int(CC.actuators.accel * 100)
        accel_cmd = make_can_msg(
            address=0x4A0,
            data=[
                target_accel & 0xFF,
                (target_accel >> 8) & 0xFF,
                0x00,
                checksum(...)
            ]
        )
    can_sends.append(accel_cmd)
    
    return can_sends
```

## 프로세스 간 협력

### 전체 흐름 재확인

```
1. 카메라 프레임 캡처
   camerad → roadCameraState (20Hz)

2. AI 추론
   modeld + roadCameraState → modelV2 (20Hz)

3. 경로 계획
   plannerd + modelV2 + carState → lateralPlan, longitudinalPlan (20Hz)

4. 제어 계산
   controlsd + lateralPlan + longitudinalPlan → carControl (100Hz)

5. 차량 제어
   boardd + carControl → CAN → Car (100Hz)

6. 상태 피드백
   boardd → carState → controlsd (100Hz)
```

### 타이밍 다이어그램

```
Time(ms)   0    10   20   30   40   50   60   70   80   90  100
           |----|----|----|----|----|----|----|----|----|----|
camerad    ●----●----●----●----●----●    (20Hz)
modeld     ●----●----●----●----●----●    (20Hz, AI 추론 30ms)
plannerd   --●----●----●----●----●--    (20Hz)
controlsd  ●●●●●●●●●●●●●●●●●●●●●●    (100Hz)
boardd     ●●●●●●●●●●●●●●●●●●●●●●    (100Hz)
```

## 다음 단계

Part 3 완료! 이제 openpilot의 핵심 개념과 프로세스를 이해했습니다.

Part 4에서는 AI 비전 시스템을 더 깊이 다룹니다:
- 모델 학습
- 데이터셋
- 모델 최적화

---

[다음: Part 4 - 비전 시스템 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/10-vision-overview.md)
