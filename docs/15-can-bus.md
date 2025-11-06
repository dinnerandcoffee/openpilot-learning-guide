# 15. CAN 버스 이해

차량 통신의 핵심인 CAN 버스를 이해하고 분석하는 방법을 배웁니다.

## CAN 버스란?

**Controller Area Network**:
- 차량 내부 통신 표준
- ECU 간 메시지 교환
- 실시간, 고신뢰성

### 메시지 구조

```
CAN 메시지:
┌─────────┬──────┬──────────┬─────┐
│ ID      │ DLC  │ Data     │ CRC │
│ (11bit) │ (4)  │ (0-8B)   │     │
└─────────┴──────┴──────────┴─────┘

예시:
ID: 0x4F1 (속도)
Data: [0x12, 0x34, 0x00, 0x00, ...]
```

## CAN 메시지 읽기

### panda로 수신

```python
from panda import Panda

# Panda 연결
p = Panda()

# 메시지 읽기
while True:
    msgs = p.can_recv()
    
    for addr, ts, data, bus in msgs:
        print(f"ID: 0x{addr:03X}, Data: {data.hex()}")
```

### 메시지 파싱

```python
# Hyundai 속도 (0x4F1)
def parse_speed(data):
    speed_raw = (data[0] << 8) | data[1]
    speed_mps = speed_raw * 0.01
    speed_kmh = speed_mps * 3.6
    return speed_kmh

# 조향각 (0x2B0)
def parse_steering(data):
    angle_raw = (data[0] << 8) | data[1]
    angle = (angle_raw - 32768) * 0.1
    return angle
```

## DBC 파일

### DBC 형식

```dbc
# hyundai_kia_generic.dbc

BO_ 1265 SPEED: 8 XXX
 SG_ SPEED : 0|16@1+ (0.01,0) [0|655.35] "m/s" XXX
 SG_ CHECKSUM : 56|8@1+ (1,0) [0|255] "" XXX

BO_ 688 STEERING: 8 XXX
 SG_ ANGLE : 0|16@1- (0.1,-3276.8) [-3276.8|3276.7] "deg" XXX
 SG_ RATE : 16|16@1- (0.1,-327.68) [-327.68|327.67] "deg/s" XXX
```

### cantools 사용

```python
import cantools

# DBC 로드
db = cantools.database.load_file('hyundai.dbc')

# 메시지 디코드
msg = db.get_message_by_name('SPEED')
data = bytes([0x12, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAB])
decoded = msg.decode(data)

print(decoded)  # {'SPEED': 46.6, 'CHECKSUM': 171}
```

## CAN 전송

```python
# 조향 명령 생성
def create_steer_command(angle, bus=0):
    addr = 0x340
    
    # 각도를 raw 값으로
    angle_raw = int(angle * 10) & 0xFFFF
    
    # 메시지 구성
    data = [
        (angle_raw >> 8) & 0xFF,
        angle_raw & 0xFF,
        0x00,
        0x00,
        checksum(...)
    ]
    
    p.can_send(addr, data, bus)
```

## 다음 단계

CAN 버스를 이해했습니다! 다음은 차량별 인터페이스입니다.

---

[다음: 16. 차량 포팅 →](./16-car-porting.md)
