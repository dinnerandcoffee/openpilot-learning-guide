# 16. 차량 포팅

새로운 차량을 openpilot에 추가하는 포팅 과정을 다룹니다.

## 포팅 단계

1. CAN 메시지 분석
2. Fingerprint 추가
3. CarInterface 구현
4. CarController 구현
5. CarState 파싱
6. 테스트

## 1. CAN 분석

### 메시지 수집

```python
# CAN 로그 수집
python tools/cabana/cabana.py --stream

# 주요 메시지 찾기:
# - 속도
# - 조향각
# - 브레이크/가스
# - 기어
# - 버튼
```

## 2. Fingerprint

```python
# selfdrive/car/hyundai/values.py

class CAR:
    SONATA_2020 = "HYUNDAI SONATA 2020"

FINGERPRINTS = {
    CAR.SONATA_2020: [{
        66: 8, 67: 8, 68: 8, 127: 8, 128: 8, 129: 8,
        273: 8, 274: 8, 275: 8, 339: 8, 356: 4,
        399: 8, 447: 8, 512: 6, 544: 8, 593: 8,
        608: 8, 688: 5, 809: 8, 832: 8, 854: 8,
        870: 7, 871: 8, 897: 8, 902: 8, 903: 8,
        905: 8, 909: 8, 916: 8, 1040: 8, 1056: 8,
        1057: 8, 1078: 4, 1107: 5, 1136: 8, 1151: 6,
        1168: 7, 1170: 8, 1186: 2, 1191: 2, 1227: 8,
        1265: 4, 1280: 1, 1287: 4, 1290: 8, 1292: 8,
        1294: 8, 1312: 8, 1314: 8, 1322: 8, 1342: 6,
        1345: 8, 1348: 8, 1363: 8, 1366: 8, 1367: 8,
        1369: 8, 1407: 8, 1414: 3, 1419: 8, 1425: 2,
        1427: 6, 1440: 8, 1456: 4, 1470: 8, 1472: 8,
        1486: 8, 1487: 8, 1491: 8, 1530: 8, 1532: 5,
        1592: 8, 1594: 8, 1596: 8, 1912: 8, 1976: 8,
        2000: 8, 2004: 8, 2008: 8, 2012: 8,
    }],
}
```

## 3. CarInterface

```python
# selfdrive/car/hyundai/interface.py

class CarInterface(CarInterfaceBase):
    @staticmethod
    def _get_params(ret, candidate, fingerprint):
        ret.carName = "hyundai"
        ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.hyundai)]
        
        # 제어 파라미터
        ret.steerRatio = 14.5
        ret.steerActuatorDelay = 0.1
        
        # 횡방향 제어
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGainV = [3.5]
        ret.lateralTuning.indi.outerLoopGainV = [2.0]
        
        # 종방향 제어
        ret.longitudinalTuning.kpV = [0.5]
        ret.longitudinalTuning.kiV = [0.1]
        
        return ret
```

## 4. CarController

```python
# selfdrive/car/hyundai/carcontroller.py

class CarController:
    def update(self, CC, CS):
        can_sends = []
        
        # 조향 제어
        steer_cmd = hyundaicanfd.create_steering_command(
            CC.actuators.steer,
            CC.enabled
        )
        can_sends.append(steer_cmd)
        
        # ACC 제어
        accel_cmd = hyundaicanfd.create_acc_command(
            CC.cruiseControl.override,
            CC.actuators.accel
        )
        can_sends.append(accel_cmd)
        
        return can_sends
```

## 5. CarState

```python
# selfdrive/car/hyundai/carstate.py

class CarState(CarStateBase):
    def update(self, can_msgs):
        for msg in can_msgs:
            if msg.address == 1265:  # SPEED
                self.vEgo = (msg.data[0] << 8 | msg.data[1]) * 0.01
            
            elif msg.address == 688:  # STEERING
                angle_raw = msg.data[0] << 8 | msg.data[1]
                self.steeringAngleDeg = (angle_raw - 32768) * 0.1
            
            elif msg.address == 593:  # BRAKE
                self.brakePressed = bool(msg.data[6] & 0x80)
```

## 6. 테스트

```bash
# 시뮬레이션
FINGERPRINT="HYUNDAI SONATA 2020" \
python selfdrive/test/test_car_model.py

# 실차 테스트
# - 조향 확인
# - 속도 확인
# - 버튼 확인
```

## 다음 단계

Part 6 완료! 마지막 Part 7 (실전 프로젝트)입니다.

---

[다음: Part 7 - 실전 프로젝트 →](./19-custom-model.md)
