# 13. 횡방향 제어 (조향)

차선을 유지하고 경로를 따라가는 조향 제어를 깊이 있게 다룹니다.

## 제어 목표

**입력**: 
- 목표 경로 (plannerd에서)
- 현재 차량 상태

**출력**:
- 조향 명령 (조향각 또는 토크)

**목표**:
- 경로 정확히 추종
- 부드러운 조향
- 안정성 보장

## 제어 알고리즘

### 1. PID 제어

가장 기본적인 방법입니다.

```python
class PIDController:
    def __init__(self, Kp=0.5, Ki=0.05, Kd=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        self.integral = 0
        self.prev_error = 0
    
    def update(self, error, dt=0.01):
        # P: 비례
        P = self.Kp * error
        
        # I: 적분
        self.integral += error * dt
        I = self.Ki * self.integral
        
        # D: 미분
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative
        
        # 업데이트
        self.prev_error = error
        
        # 출력
        output = P + I + D
        return output

# 사용
pid = PIDController(Kp=0.5, Ki=0.05, Kd=0.1)

while True:
    # 경로 오차
    error = desired_position - current_position
    
    # 제어 계산
    steer_angle = pid.update(error)
    
    # 제한
    steer_angle = np.clip(steer_angle, -MAX_STEER, MAX_STEER)
```

### 2. Pure Pursuit

기하학적 경로 추종 방법입니다.

```python
def pure_pursuit(current_position, current_heading, path, look_ahead_distance):
    """
    Pure Pursuit 알고리즘
    
    Args:
        current_position: (x, y) 현재 위치
        current_heading: 현재 방향각 (rad)
        path: 목표 경로 [(x, y), ...]
        look_ahead_distance: Look-ahead 거리 (m)
    
    Returns:
        steering_angle: 조향각 (rad)
    """
    # 1. Look-ahead 점 찾기
    target_point = None
    for point in path:
        distance = np.linalg.norm(point - current_position)
        if distance >= look_ahead_distance:
            target_point = point
            break
    
    if target_point is None:
        target_point = path[-1]
    
    # 2. 차량 좌표계로 변환
    dx = target_point[0] - current_position[0]
    dy = target_point[1] - current_position[1]
    
    # 회전
    alpha = np.arctan2(dy, dx) - current_heading
    
    # 3. 조향각 계산
    # δ = arctan(2L sin(α) / ld)
    L = 2.7  # 휠베이스 (m)
    steering_angle = np.arctan2(2 * L * np.sin(alpha), look_ahead_distance)
    
    return steering_angle

# 속도에 따른 look-ahead 거리
def adaptive_look_ahead(velocity):
    # 저속: 5m, 고속: 20m
    return 5.0 + velocity * 0.5
```

### 3. Stanley Controller

경로 오차와 헤딩 오차를 모두 고려합니다.

```python
def stanley_control(path, current_pos, current_heading, velocity):
    """
    Stanley 제어기
    
    Returns:
        steering_angle: 조향각
    """
    # 1. 가장 가까운 경로 점 찾기
    distances = [np.linalg.norm(p - current_pos) for p in path]
    nearest_idx = np.argmin(distances)
    nearest_point = path[nearest_idx]
    
    # 2. 경로의 헤딩
    if nearest_idx < len(path) - 1:
        path_heading = np.arctan2(
            path[nearest_idx + 1][1] - nearest_point[1],
            path[nearest_idx + 1][0] - nearest_point[0]
        )
    else:
        path_heading = current_heading
    
    # 3. 헤딩 오차
    heading_error = path_heading - current_heading
    
    # 4. 크로스 트랙 오차 (CTE)
    cte = distances[nearest_idx]
    
    # 경로의 어느 쪽에 있는지 판단
    path_vec = path[nearest_idx + 1] - nearest_point if nearest_idx < len(path) - 1 else [0, 0]
    pos_vec = current_pos - nearest_point
    cross = np.cross(path_vec, pos_vec)
    if cross < 0:
        cte = -cte
    
    # 5. Stanley 공식
    k = 2.5  # 게인
    steering_angle = heading_error + np.arctan2(k * cte, velocity + 0.1)
    
    return steering_angle
```

### 4. INDI (openpilot 사용)

Incremental Nonlinear Dynamic Inversion - openpilot의 기본 제어기입니다.

```python
# selfdrive/controls/lib/lateral_planner.py

class LateralINDIController:
    def __init__(self, CP):
        self.RC = CP.lateralTuning.indi.timeConstant  # 시간 상수
        self.G = CP.lateralTuning.indi.actuatorEffectiveness  # 효과성
        self.outer_gain = CP.lateralTuning.indi.outerGain
        
        self.sat_flag = False
        self.speed_filter = FirstOrderFilter(0, self.RC, DT_CTRL)
    
    def update(self, steer_rate_desired, steer_rate_actual, v_ego):
        # 1. 속도 필터링
        v_ego_filtered = self.speed_filter.update(v_ego)
        
        # 2. 외부 루프 (경로 오차)
        steer_rate_ref = self.outer_gain * steer_rate_desired
        
        # 3. INDI 제어
        # u = (v_desired - v_actual) / G
        steer_delta = (steer_rate_ref - steer_rate_actual) / self.G
        
        # 4. 속도 보상
        steer_delta *= (v_ego_filtered + 0.5)  # 저속에서도 작동
        
        # 5. 포화 방지
        if abs(steer_delta) > MAX_STEER_RATE:
            self.sat_flag = True
            steer_delta = np.sign(steer_delta) * MAX_STEER_RATE
        else:
            self.sat_flag = False
        
        return steer_delta
```

**INDI의 장점**:
- 모델 불확실성에 강함
- 빠른 응답
- 차량별 튜닝 최소화

## 경로 생성

### 다항식 경로

```python
def fit_polynomial_path(lane_points):
    """
    차선 점들을 3차 다항식으로 피팅
    
    y = c0 + c1*x + c2*x^2 + c3*x^3
    """
    x = np.array([p[0] for p in lane_points])
    y = np.array([p[1] for p in lane_points])
    
    # 3차 다항식 피팅
    coeffs = np.polyfit(x, y, 3)
    
    return coeffs  # [c3, c2, c1, c0]

def evaluate_path(coeffs, x_values):
    """다항식 경로 계산"""
    return np.polyval(coeffs, x_values)

# 경로 오차 계산
def compute_path_error(coeffs, current_x=0):
    """
    현재 위치에서의 경로 오차
    
    c0: 현재 오프셋
    c1: 현재 각도 (tan θ)
    c2, c3: 곡률
    """
    offset = coeffs[3]  # c0
    angle = coeffs[2]   # c1
    
    return offset, angle
```

### Look-ahead 전략

```python
def compute_lookahead_point(path_coeffs, v_ego):
    """
    속도에 따른 look-ahead 거리
    """
    # 기본 시간: 0.5초
    lookahead_time = 0.5
    
    # 고속에서 더 멀리
    if v_ego > 20:  # 20 m/s (72 km/h)
        lookahead_time = 0.7
    
    # 거리 계산
    lookahead_distance = v_ego * lookahead_time
    
    # 경로 상의 점 계산
    x = lookahead_distance
    y = np.polyval(path_coeffs, x)
    
    return x, y

# 목표 조향각
def compute_desired_steer(path_coeffs, v_ego):
    x, y = compute_lookahead_point(path_coeffs, v_ego)
    
    # Ackermann 기하학
    L = 2.7  # 휠베이스
    steer_angle = np.arctan2(2 * L * y, x ** 2)
    
    return steer_angle
```

## 차량 모델

### Bicycle Model

```python
class BicycleModel:
    """
    단순화된 차량 모델
    """
    def __init__(self, L=2.7):
        self.L = L  # 휠베이스
        
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.v = 0
    
    def update(self, steer_angle, accel, dt):
        """
        상태 업데이트
        
        x' = v cos(ψ)
        y' = v sin(ψ)
        ψ' = v tan(δ) / L
        v' = a
        """
        # 속도 업데이트
        self.v += accel * dt
        
        # 헤딩 변화율
        yaw_rate = self.v * np.tan(steer_angle) / self.L
        
        # 위치 업데이트
        self.x += self.v * np.cos(self.yaw) * dt
        self.y += self.v * np.sin(self.yaw) * dt
        self.yaw += yaw_rate * dt
        
        return self.x, self.y, self.yaw

# 시뮬레이션
vehicle = BicycleModel()

for t in np.arange(0, 10, 0.01):
    steer = compute_steer(...)
    accel = 0.5
    
    x, y, yaw = vehicle.update(steer, accel, 0.01)
```

## 제어 튜닝

### 게인 조정

```python
# selfdrive/car/hyundai/interface.py

ret.lateralTuning.init('indi')
ret.lateralTuning.indi.innerLoopGainV = [3.5, 3.5]
ret.lateralTuning.indi.outerLoopGainV = [2.0, 2.0]
ret.lateralTuning.indi.timeConstantV = [1.0, 1.0]
ret.lateralTuning.indi.actuatorEffectivenessV = [1.5, 1.5]
```

**튜닝 가이드**:

1. **innerLoopGain** ↑
   - 빠른 응답
   - 진동 가능성 ↑

2. **outerLoopGain** ↑
   - 경로 추종 ↑
   - 과도한 조향

3. **timeConstant** ↑
   - 부드러운 제어
   - 응답 느림

### 시뮬레이션 기반 튜닝

```python
def simulate_control(controller, path, initial_state):
    """제어기 시뮬레이션"""
    vehicle = BicycleModel()
    vehicle.x, vehicle.y, vehicle.yaw = initial_state
    
    trajectory = []
    errors = []
    
    for t in np.arange(0, 10, 0.01):
        # 현재 오차
        error = compute_error(vehicle, path)
        errors.append(error)
        
        # 제어 계산
        steer = controller.update(error)
        
        # 차량 업데이트
        vehicle.update(steer, 0, 0.01)
        trajectory.append((vehicle.x, vehicle.y))
    
    # 성능 지표
    mae = np.mean(np.abs(errors))
    max_error = np.max(np.abs(errors))
    
    return trajectory, mae, max_error

# 여러 게인 시도
gains = [0.1, 0.3, 0.5, 0.7, 1.0]
best_gain = None
best_mae = float('inf')

for gain in gains:
    controller = PIDController(Kp=gain)
    _, mae, _ = simulate_control(controller, path, (0, 0, 0))
    
    if mae < best_mae:
        best_mae = mae
        best_gain = gain

print(f"Best Kp: {best_gain}, MAE: {best_mae:.3f}m")
```

## 안전 제한

### 조향 속도 제한

```python
class SteerRateLimiter:
    def __init__(self, max_rate=3.0):
        self.max_rate = max_rate  # deg/s
        self.prev_steer = 0
    
    def limit(self, desired_steer, dt=0.01):
        # 최대 변화량
        max_delta = self.max_rate * dt
        
        # 변화량 계산
        delta = desired_steer - self.prev_steer
        
        # 제한
        if abs(delta) > max_delta:
            delta = np.sign(delta) * max_delta
        
        # 적용
        limited_steer = self.prev_steer + delta
        self.prev_steer = limited_steer
        
        return limited_steer
```

### 조향 범위 제한

```python
def apply_steer_limits(steer_angle, v_ego, CP):
    """
    속도와 차량에 따른 조향 제한
    """
    # 속도 비례 제한
    if v_ego < 10:  # 저속
        max_steer = CP.steerMaxV[0]
    else:  # 고속
        max_steer = interp(v_ego, CP.steerMaxBP, CP.steerMaxV)
    
    # 제한 적용
    return np.clip(steer_angle, -max_steer, max_steer)
```

## 다음 단계

횡방향 제어를 마스터했습니다! 다음은 종방향 제어(속도)입니다.

---

[다음: 14. 종방향 제어 →](./14-longitudinal-control.md)
