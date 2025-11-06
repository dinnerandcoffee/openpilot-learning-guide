# 14. 종방향 제어 (속도)

차량의 가속과 감속을 제어하는 종방향 제어 시스템을 다룹니다.

## 제어 목표

- 크루즈 속도 유지
- 선행 차량 추종 (ACC)
- 부드러운 가감속
- 안전거리 확보

## ACC (Adaptive Cruise Control)

### 기본 로직

```python
class ACCController:
    def __init__(self):
        self.Kp = 0.5
        self.Ki = 0.1
        self.Kd = 0.05
        
        self.time_headway = 1.8  # 초
        self.min_distance = 5.0  # m
    
    def update(self, v_ego, v_target, lead_distance=None, lead_velocity=None):
        if lead_distance is not None:
            # 추종 모드
            return self.follow_lead(v_ego, lead_distance, lead_velocity)
        else:
            # 크루즈 모드
            return self.cruise_control(v_ego, v_target)
    
    def cruise_control(self, v_ego, v_target):
        """크루즈 제어"""
        error = v_target - v_ego
        accel = self.Kp * error
        return np.clip(accel, -4.0, 2.0)
    
    def follow_lead(self, v_ego, d_lead, v_lead):
        """선행 차량 추종"""
        # 목표 거리
        d_target = self.time_headway * v_ego + self.min_distance
        
        # 거리 오차
        d_error = d_lead - d_target
        
        # 속도 매칭
        v_rel = v_lead - v_ego
        
        # 제어 계산
        accel = 0.3 * d_error + 0.5 * v_rel
        
        return np.clip(accel, -4.0, 2.0)
```

### MPC 기반 제어

```python
# selfdrive/controls/lib/longitudinal_mpc.py

class LongitudinalMPC:
    def __init__(self):
        self.horizon = 50  # 5초 (100ms × 50)
        self.cost_v = 1.0
        self.cost_a = 1.0
        self.cost_j = 10.0  # jerk
    
    def run(self, v_ego, a_ego, v_target, lead_data):
        """MPC 최적화"""
        # 상태 벡터: [v, a] × 50
        # 제어 입력: [jerk] × 50
        
        # 비용 함수
        cost = 0
        for t in range(self.horizon):
            # 속도 오차
            cost += self.cost_v * (v[t] - v_target) ** 2
            
            # 가속도
            cost += self.cost_a * a[t] ** 2
            
            # Jerk (승차감)
            cost += self.cost_j * jerk[t] ** 2
            
            # 충돌 회피
            if lead_data:
                cost += collision_cost(position[t], lead_data)
        
        # 최적화 (scipy)
        result = minimize(cost_function, x0, constraints=constraints)
        
        return result.jerk[0]
```

## 저크 최소화

```python
def smooth_acceleration(a_current, a_target, max_jerk=2.0, dt=0.01):
    """부드러운 가속도 변화"""
    delta_a = a_target - a_current
    max_delta = max_jerk * dt
    
    delta_a = np.clip(delta_a, -max_delta, max_delta)
    
    return a_current + delta_a
```

## 언덕 보상

```python
def compensate_slope(accel, pitch_angle):
    """경사 보상"""
    g = 9.81
    slope_accel = -g * np.sin(pitch_angle)
    return accel - slope_accel
```

## 다음 단계

Part 5 완료! 다음은 Part 6 (차량 인터페이스)입니다.

---

[다음: 15. CAN 버스 이해 →](./15-can-bus.md)
