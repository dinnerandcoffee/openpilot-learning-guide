# 8. cereal 메시징 시스템

openpilot의 모든 프로세스가 통신하는 방법인 cereal을 깊이 있게 알아봅시다.

## 개요

**cereal이란?**
- openpilot의 커스텀 메시징 라이브러리
- Cap'n Proto 기반
- 프로세스 간 통신 (IPC)
- Pub-Sub 패턴

**왜 cereal을 만들었나?**
- 고성능 (최소 레이턴시)
- 타입 안전성
- 스키마 진화 지원
- 크로스 플랫폼

## Cap'n Proto란?

### Protocol Buffers와 비교

```
Protocol Buffers (Google):
- 직렬화/역직렬화 필요
- 메모리 복사 발생
- 약간의 오버헤드

Cap'n Proto (Cloudflare):
- Zero-copy 읽기
- 인코딩 = 메모리 레이아웃
- 매우 빠름
```

### 예시 비교

**Protobuf**:
```python
# 인코딩
msg = CarState()
msg.speed = 25.0
msg.steering_angle = 10.5
data = msg.SerializeToString()  # 복사 발생

# 디코딩
msg2 = CarState()
msg2.ParseFromString(data)  # 또 복사
print(msg2.speed)
```

**Cap'n Proto**:
```python
# 인코딩
msg = message_builder.CarState.new_message()
msg.speed = 25.0
msg.steeringAngle = 10.5
data = msg.to_bytes()  # 이미 인코딩된 형태

# 디코딩 (zero-copy)
msg2 = CarState.from_bytes(data, traversal_limit_in_words=2**64-1)
print(msg2.speed)  # 복사 없이 직접 읽기
```

## cereal 메시지 정의

### 스키마 파일

모든 메시지는 `.capnp` 파일에 정의됩니다.

```capnp
# cereal/log.capnp

struct CarState {
  vEgo @0 :Float32;              # 속도 (m/s)
  vEgoRaw @1 :Float32;           # 필터링 안 된 속도
  aEgo @2 :Float32;              # 가속도 (m/s²)
  steeringAngleDeg @3 :Float32;  # 조향각 (도)
  steeringTorque @4 :Float32;    # 조향 토크
  
  # 브레이크/가스
  brakePressed @5 :Bool;
  gasPressed @6 :Bool;
  
  # 기어
  gearShifter @7 :GearShifter;
  
  enum GearShifter {
    unknown @0;
    park @1;
    reverse @2;
    neutral @3;
    drive @4;
    sport @5;
    low @6;
  }
  
  # 더 많은 필드들...
  cruiseState @8 :CruiseState;
  buttonEvents @9 :List(ButtonEvent);
  
  struct CruiseState {
    enabled @0 :Bool;
    speed @1 :Float32;
    available @2 :Bool;
  }
}
```

### Python 코드 생성

Cap'n Proto 컴파일러가 자동으로 Python 코드를 생성합니다.

```bash
# 스키마 컴파일
cd ~/dev/openpilot
capnp compile -o python cereal/log.capnp

# 생성된 파일
# cereal/log_capnp.py
```

## cereal 사용법

### 1. SubMaster (구독자)

메시지를 받는 쪽입니다.

```python
from cereal import messaging

# SubMaster 생성
sm = messaging.SubMaster([
    'carState',      # 구독할 메시지들
    'modelV2',
    'controlsState'
])

while True:
    # 모든 메시지 업데이트
    sm.update()
    
    # 메시지 읽기
    car_state = sm['carState']
    print(f"Speed: {car_state.vEgo:.1f} m/s")
    
    # 업데이트 확인
    if sm.updated['modelV2']:
        print("New model prediction!")
    
    # 메시지 수신 시간
    print(f"Received {sm.rcv_time['carState']:.3f}s ago")
```

**SubMaster 메서드**:

```python
# update(): 새 메시지 확인
sm.update(timeout=100)  # 100ms 대기

# updated: 새 메시지 도착 여부
if sm.updated['carState']:
    process(sm['carState'])

# valid: 메시지가 유효한지
if sm.valid['modelV2']:
    use_model(sm['modelV2'])

# alive: 메시지가 최근에 도착했는지
if sm.alive['carState']:
    print("Still receiving carState")

# freq: 메시지 주파수
print(f"carState: {sm.freq['carState']:.1f} Hz")

# lag: 레이턴시
print(f"Lag: {sm.lag('carState'):.0f} ms")
```

### 2. PubMaster (발행자)

메시지를 보내는 쪽입니다.

```python
from cereal import messaging, log

# PubMaster 생성
pm = messaging.PubMaster([
    'controlsState',
    'carControl'
])

# 메시지 생성
msg = messaging.new_message('controlsState')
cs = msg.controlsState

# 필드 채우기
cs.enabled = True
cs.active = True
cs.vEgo = 25.0
cs.vEgoRaw = 25.1

# 전송
pm.send('controlsState', msg)
```

**빌더 패턴**:

```python
# 리스트 초기화
msg = messaging.new_message('modelV2')
model = msg.modelV2

# 차선 라인 (4개)
model.laneLines = [
    {'x': [...], 'y': [...], 'z': [...]},
    {'x': [...], 'y': [...], 'z': [...]},
    {'x': [...], 'y': [...], 'z': [...]},
    {'x': [...], 'y': [...], 'z': [...]}
]

# 리스트 빌더
leads = model.init('leadsV3', 2)  # 2개 초기화
leads[0].prob = 0.9
leads[0].x = [50.0, 51.0, 52.0]
leads[1].prob = 0.7
leads[1].x = [100.0, 101.0, 102.0]

pm.send('modelV2', msg)
```

### 3. 주요 메시지 타입

#### carState

차량의 현재 상태입니다.

```python
car_state = sm['carState']

# 속도
print(f"vEgo: {car_state.vEgo} m/s")
print(f"vEgoCluster: {car_state.vEgoCluster} m/s")

# 조향
print(f"Steering angle: {car_state.steeringAngleDeg}°")
print(f"Steering rate: {car_state.steeringRateDeg}/s")

# 페달
print(f"Brake: {car_state.brakePressed}")
print(f"Gas: {car_state.gasPressed}")

# 크루즈
cruise = car_state.cruiseState
print(f"Cruise enabled: {cruise.enabled}")
print(f"Set speed: {cruise.speed} m/s")

# 버튼 이벤트
for event in car_state.buttonEvents:
    print(f"Button {event.type}: {event.pressed}")
```

#### modelV2

AI 모델의 예측 결과입니다.

```python
model = sm['modelV2']

# 차선 라인
for i, lane in enumerate(model.laneLines):
    print(f"Lane {i}:")
    print(f"  x: {lane.x[:10]}")  # 처음 10개 점
    print(f"  y: {lane.y[:10]}")
    print(f"  prob: {lane.prob}")

# 선행 차량
for i, lead in enumerate(model.leadsV3):
    if lead.prob > 0.5:
        print(f"Lead {i}:")
        print(f"  Distance: {lead.x[0]:.1f}m")
        print(f"  Speed: {lead.v[0]:.1f}m/s")
        print(f"  Accel: {lead.a[0]:.2f}m/s²")

# 경로
path = model.position
print(f"Path (next 5s):")
for i in range(0, 50, 10):  # 1초 간격
    print(f"  {i/10}s: x={path.x[i]:.1f}m, y={path.y[i]:.2f}m")

# 차선 폭
print(f"Lane width: {model.laneLineProbs[1]:.2f}m")
```

#### controlsState

제어 시스템의 상태입니다.

```python
controls = sm['controlsState']

# 활성화 상태
print(f"Enabled: {controls.enabled}")
print(f"Active: {controls.active}")

# 속도
print(f"vEgo: {controls.vEgo:.1f} m/s")
print(f"vCruise: {controls.vCruise:.1f} km/h")

# 횡방향 제어
lat = controls.lateralControlState
if lat.which() == 'indiState':
    indi = lat.indiState
    print(f"Steer angle: {indi.steeringAngleDeg:.1f}°")
    print(f"Steer rate: {indi.steeringRateDeg:.1f}°/s")

# 종방향 제어
long = controls.longitudinalControlState
if long.which() == 'pidState':
    pid = long.pidState
    print(f"Target speed: {pid.targetSpeed:.1f} m/s")
    print(f"Error: {pid.error:.2f}")

# 경고
for alert in controls.alertText1:
    print(f"Alert: {alert}")
```

#### carControl

차량에 보내는 제어 명령입니다.

```python
msg = messaging.new_message('carControl')
cc = msg.carControl

# 횡방향 (조향)
actuators = cc.actuators
actuators.steer = 0.1           # -1 ~ 1
actuators.steeringAngleDeg = 5.0

# 종방향 (속도)
actuators.accel = 1.5           # m/s²
actuators.longControlState = log.CarControl.Actuators.LongControlState.pid

# 크루즈
cc.cruiseControl.override = True
cc.cruiseControl.cancel = False

pm.send('carControl', msg)
```

## 메시징 패턴

### 1. 단순 Pub-Sub

```python
# Publisher
pm = PubMaster(['myTopic'])
while True:
    msg = create_message()
    pm.send('myTopic', msg)
    time.sleep(0.1)

# Subscriber
sm = SubMaster(['myTopic'])
while True:
    sm.update()
    process(sm['myTopic'])
```

### 2. 다중 구독

```python
sm = SubMaster([
    'carState',
    'modelV2',
    'controlsState'
])

while True:
    sm.update()
    
    # 모두 업데이트될 때까지 대기
    if sm.all_alive_and_valid():
        process_all(sm)
```

### 3. 타임아웃 처리

```python
sm = SubMaster(['carState'])

while True:
    # 100ms 타임아웃
    updated = sm.update(timeout=100)
    
    if not updated:
        print("Timeout! No message received")
        handle_timeout()
    else:
        process(sm['carState'])
```

### 4. 빈도 조절

```python
pm = PubMaster(['slowTopic'])

rate = 1.0  # 1 Hz
last_send = 0

while True:
    now = time.monotonic()
    
    if now - last_send >= 1.0 / rate:
        msg = create_message()
        pm.send('slowTopic', msg)
        last_send = now
    
    time.sleep(0.01)
```

## ZMQ 기반 구현

cereal은 내부적으로 ZeroMQ를 사용합니다.

### ZMQ 소켓

```python
# cereal/messaging/__init__.py

import zmq

class PubMaster:
    def __init__(self, services):
        self.context = zmq.Context()
        self.sockets = {}
        
        for service in services:
            sock = self.context.socket(zmq.PUB)
            sock.bind(f"ipc:///tmp/{service}")
            self.sockets[service] = sock
    
    def send(self, service, msg):
        data = msg.to_bytes()
        self.sockets[service].send(data)

class SubMaster:
    def __init__(self, services):
        self.context = zmq.Context()
        self.poller = zmq.Poller()
        self.sockets = {}
        
        for service in services:
            sock = self.context.socket(zmq.SUB)
            sock.connect(f"ipc:///tmp/{service}")
            sock.setsockopt(zmq.SUBSCRIBE, b'')
            self.sockets[service] = sock
            self.poller.register(sock, zmq.POLLIN)
    
    def update(self, timeout=100):
        events = dict(self.poller.poll(timeout))
        
        for service, sock in self.sockets.items():
            if sock in events:
                data = sock.recv()
                self.data[service] = parse_message(data)
```

### 소켓 위치

```bash
# IPC 소켓 확인
ls -la /tmp/ | grep -E 'carState|modelV2'

# 예시:
# srwxrwxrwx  1 comma comma  0 Jan 15 10:30 carState
# srwxrwxrwx  1 comma comma  0 Jan 15 10:30 modelV2
```

## 성능 최적화

### 1. Conflation (메시지 병합)

여러 메시지가 쌓이면 가장 최신 것만 사용:

```python
sm = SubMaster(['carState'], conflate=True)

# 오래된 메시지는 무시하고 최신 것만
sm.update()
```

### 2. 메시지 필터링

필요한 필드만 읽기:

```python
# 전체 읽기 (느림)
car_state = sm['carState']
speed = car_state.vEgo

# 필드만 읽기 (빠름)
speed = sm['carState'].vEgo
```

### 3. 지연 로딩

```python
# 메시지가 업데이트될 때만 처리
if sm.updated['modelV2']:
    expensive_processing(sm['modelV2'])
```

## 로깅과 재생

### 1. 메시지 로깅

```python
from cereal import log
from tools.lib.logreader import LogWriter

# 로거 생성
lr = LogWriter("output.rlog")

sm = SubMaster(['carState', 'modelV2'])

while True:
    sm.update()
    
    # 메시지 기록
    for service in sm.updated:
        if sm.updated[service]:
            lr.write(service, sm[service])
```

### 2. 로그 재생

```python
from tools.lib.logreader import LogReader

# 로그 읽기
lr = LogReader("output.rlog")

for msg in lr:
    service = msg.which()
    print(f"{service}: {msg}")
    
    # 특정 메시지만
    if service == 'carState':
        print(f"Speed: {msg.carState.vEgo}")
```

## 실전 예제

### 속도 모니터

```python
#!/usr/bin/env python3
from cereal import messaging

def speed_monitor():
    sm = messaging.SubMaster(['carState'])
    
    max_speed = 0
    
    while True:
        sm.update()
        
        if sm.updated['carState']:
            cs = sm['carState']
            speed_kmh = cs.vEgo * 3.6
            
            max_speed = max(max_speed, speed_kmh)
            
            print(f"Current: {speed_kmh:.1f} km/h | "
                  f"Max: {max_speed:.1f} km/h")
        
        time.sleep(0.1)

if __name__ == '__main__':
    speed_monitor()
```

### 차선 감지 로거

```python
#!/usr/bin/env python3
from cereal import messaging
import numpy as np

def lane_logger():
    sm = messaging.SubMaster(['modelV2'])
    
    while True:
        sm.update()
        
        if sm.updated['modelV2']:
            model = sm['modelV2']
            
            # 왼쪽 차선
            left_lane = model.laneLines[1]
            if left_lane.prob > 0.5:
                y_values = np.array(left_lane.y)
                mean_offset = np.mean(y_values[:20])  # 처음 10m
                print(f"Left lane offset: {mean_offset:.2f}m")
            
            # 오른쪽 차선
            right_lane = model.laneLines[2]
            if right_lane.prob > 0.5:
                y_values = np.array(right_lane.y)
                mean_offset = np.mean(y_values[:20])
                print(f"Right lane offset: {mean_offset:.2f}m")

if __name__ == '__main__':
    lane_logger()
```

## 다음 단계

cereal 메시징을 이해했으니, 다음 장에서는 주요 프로세스들의 동작 원리를 자세히 알아봅시다.

---

[다음: 9. 주요 프로세스 깊이 알기 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/09-processes.md)
