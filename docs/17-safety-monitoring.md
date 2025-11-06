# 17. 안전 모델과 모니터링

openpilot의 안전 시스템과 모니터링 메커니즘을 살펴봅니다.

## 안전 모델 (Safety Model)

panda 펌웨어에 구현된 안전 검증 로직입니다.

```c
// board/safety/safety_toyota.h

const int TOYOTA_MAX_STEER = 1500;
const int TOYOTA_MAX_RATE = 15;

int toyota_tx_hook(CANPacket_t *to_send) {
  int addr = GET_ADDR(to_send);
  
  if (addr == 0x2E4) {  // STEERING_LTA
    int desired_steer = GET_BYTE(to_send, 0) | (GET_BYTE(to_send, 1) << 8);
    
    // 조향 제한 확인
    if (abs(desired_steer) > TOYOTA_MAX_STEER) {
      return 0;  // 차단
    }
    
    // 변화율 제한
    int delta = abs(desired_steer - toyota_last_steer);
    if (delta > TOYOTA_MAX_RATE) {
      return 0;
    }
    
    toyota_last_steer = desired_steer;
  }
  
  return 1;  // 전송 허용
}
```

## 모니터링 시스템

```python
# selfdrive/controls/lib/alertmanager.py

class AlertManager:
    def __init__(self):
        self.alerts = []
    
    def add_alert(self, alert_type, severity):
        """알림 추가"""
        alert = Alert(alert_type, severity)
        self.alerts.append(alert)
        
        # 심각도에 따른 처리
        if severity == 'critical':
            self.trigger_disengagement()
    
    def process(self, sm):
        # 운전자 모니터링
        if sm['driverMonitoringState'].awarenessStatus < 0.3:
            self.add_alert('driverDistracted', 'warning')
        
        # 차량 상태
        if sm['carState'].standstill and self.engaged:
            self.add_alert('standstillResume', 'info')
```

## 페일세이프

```python
# 이중화된 안전 검사
def check_safety():
    # 차량 측 검사 (panda)
    panda_ok = panda.health()['safety_model_ok']
    
    # openpilot 측 검사
    controls_ok = (
        abs(actuators.steer) < MAX_STEER and
        abs(actuators.accel) < MAX_ACCEL
    )
    
    return panda_ok and controls_ok
```

## 로깅

```python
# 블랙박스 로깅
logger = LogWriter('/data/logs')

logger.write({
    'timestamp': time.time(),
    'controlsState': controls_state,
    'carState': car_state,
    'alerts': alerts
})
```

---

[다음: 18. 컨트리뷰션 가이드 →](./18-contributing.md)
