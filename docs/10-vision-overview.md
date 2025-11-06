# 10. 비전 시스템 개요

openpilot의 눈인 AI 비전 시스템을 탐구해봅시다. 어떻게 카메라만으로 도로를 이해하는지 알아봅니다.

## 개요

**openpilot의 비전 철학**:
- **카메라 우선**: 라이다 없이 카메라만 사용
- **딥러닝**: End-to-end 학습
- **실시간**: 20Hz로 추론
- **경량**: 모바일 디바이스에서 실행

## 비전이 하는 일

### 입력

```
카메라 프레임:
- 해상도: 1164 × 874 (wide road camera)
- 프레임 레이트: 20 FPS
- 포맷: YUV
- 시야각: ~120°
```

### 출력

```python
{
    # 1. 차선 라인 (4개)
    'laneLines': [
        left_far,    # 왼쪽 먼 차선
        left,        # 왼쪽 차선
        right,       # 오른쪽 차선  
        right_far    # 오른쪽 먼 차선
    ],
    
    # 2. 주행 경로
    'position': {
        'x': [...],  # 전방 거리 (0~100m)
        'y': [...],  # 좌우 오프셋
        'z': [...],  # 높이
    },
    
    # 3. 선행 차량 (최대 2대)
    'leads': [
        {
            'prob': 0.95,        # 감지 확률
            'x': [50, ...],      # 거리
            'y': [0, ...],       # 좌우 위치
            'v': [5, ...],       # 상대 속도
            'a': [0, ...]        # 상대 가속도
        }
    ],
    
    # 4. 도로 모서리
    'roadEdges': [left_edge, right_edge],
    
    # 5. 메타 정보
    'meta': {
        'desireState': ...,      # 의도 (차선 유지/변경)
        'engaged': ...,          # 시스템 활성
    }
}
```

## supercombo 모델

### 모델 진화

```
2016: dashcam model
  ↓ (단순 차선 감지)
  
2017: model v1
  ↓ (경로 예측 추가)
  
2018: model v2  
  ↓ (선행 차 감지)
  
2020: supercombo
  ↓ (통합 모델)
  
2023: supercombo v2
  ↓ (트랜스포머 기반)
  
2025: current
  (지속적 개선)
```

### 아키텍처

```
입력 이미지 (12채널)
    ↓
┌──────────────────────┐
│  Feature Extractor   │
│  EfficientNet-Lite0  │
│                      │
│  Conv layers         │
│  + MobileNet blocks  │
└──────────┬───────────┘
           │ features
    ┌──────┴──────┐
    │   Temporal  │
    │     GRU     │ ← 과거 프레임 기억
    └──────┬──────┘
           │
    ┌──────┴──────────┐
    │                 │
┌───▼────┐      ┌────▼────┐
│ Lane   │      │  Lead   │
│ Head   │      │  Head   │
└───┬────┘      └────┬────┘
    │                │
    ▼                ▼
차선 좌표      차량 위치/속도
```

### 모델 크기

```
파일: supercombo.dlc
크기: ~30 MB
형식: Qualcomm SNPE (Snapdragon Neural Processing Engine)

레이어 수: ~200
파라미터 수: ~8M
FLOPS: ~500M per frame
```

### 추론 시간

```
Snapdragon 8 Gen 1:
- GPU 추론: ~30ms
- CPU 추론: ~150ms
- NPU 추론: ~25ms (최적)

Snapdragon 845 (comma 3):
- GPU 추론: ~50ms
- NPU 추론: ~40ms
```

## 학습 데이터

### 데이터 수집

```python
# openpilot 주행 데이터 자동 수집

def upload_log_segment(segment_path):
    # 1. 주행 세그먼트
    files = [
        'rlog.bz2',        # 메시지 로그
        'fcamera.hevc',    # 전방 카메라
        'qlog.bz2',        # 쿼리 로그
    ]
    
    # 2. 업로드 (사용자 동의 시)
    if user_opted_in():
        for file in files:
            upload_to_comma_server(file)
    
    # 3. 익명화
    # - GPS 좌표 제거
    # - 개인 정보 필터링
```

**데이터 규모 (2025년 기준)**:
```
총 주행 거리: ~5억 마일 (800M km)
총 주행 시간: ~1000만 시간
카메라 프레임: ~조 단위
학습에 사용: 선별된 수백만 세그먼트
```

### 데이터 라벨링

openpilot은 **자동 라벨링**을 사용합니다.

```python
# 라벨 생성 (간소화)

def generate_labels(driving_log):
    labels = []
    
    for frame in driving_log:
        # 실제 주행 데이터를 라벨로 사용
        label = {
            # 운전자가 실제로 선택한 경로
            'path': frame.actual_path,
            
            # 차선 (카메라 + 후처리)
            'lanes': detect_lanes_with_cv(frame.image),
            
            # 선행 차량 (레이더 + 카메라)
            'lead': merge_radar_and_camera(frame),
        }
        
        labels.append(label)
    
    return labels
```

**라벨 소스**:
1. **인간 운전**: 실제 운전자의 조향/속도
2. **컴퓨터 비전**: 전통적 CV로 차선 감지
3. **레이더**: 선행 차량 거리/속도 (일부 차량)
4. **IMU/GPS**: 차량 움직임

### 학습 파이프라인

```
1. 데이터 수집
   comma 사용자 → 주행 로그 → comma 서버
   
2. 데이터 선별
   품질 필터 → 다양성 확보 → 균형 샘플링
   
3. 전처리
   프레임 추출 → 정규화 → 증강
   
4. 학습
   PyTorch → 모델 학습 → 검증
   
5. 양자화
   FP32 → INT8 → SNPE 변환
   
6. 배포
   테스트 → 릴리스 → OTA 업데이트
```

## 카메라 설정

### 하드웨어

```
comma 3X 카메라:

1. Wide Road Camera (메인)
   센서: Sony IMX390
   해상도: 1928 × 1208
   사용 크롭: 1164 × 874
   시야각: 120°
   프레임: 20 FPS

2. Standard Road Camera (보조)
   센서: OV8865
   해상도: 1632 × 1224
   시야각: 90°
   프레임: 20 FPS

3. Driver Camera
   센서: OV8865  
   해상도: 1152 × 864
   용도: 운전자 모니터링
```

### 카메라 보정

```python
# selfdrive/camerad/cameras/camera_qcom2.cc

# 내부 파라미터 (intrinsics)
INTRINSICS = {
    'focal_length': [910.0, 910.0],  # fx, fy
    'principal_point': [582.0, 437.0],  # cx, cy
    'distortion': [k1, k2, p1, p2, k3]  # 왜곡 계수
}

# 외부 파라미터 (extrinsics)
EXTRINSICS = {
    'height': 1.22,  # 지면에서 높이 (m)
    'pitch': 0.0,    # 피치 각도 (rad)
    'yaw': 0.0,      # 요 각도
    'roll': 0.0      # 롤 각도
}
```

## 전처리 파이프라인

### 이미지 변환

```python
# selfdrive/modeld/models/commonmodel.cc

def preprocess_frame(yuv_frame):
    # 1. YUV → RGB 변환
    rgb = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2RGB_NV12)
    
    # 2. 크롭 (하늘 제거)
    # 원본: 1164 × 874
    # 크롭: 1164 × 874 (이미 최적화됨)
    cropped = rgb[0:874, 0:1164]
    
    # 3. 리사이즈 (모델 입력)
    # 1164 × 874 → 512 × 384
    resized = cv2.resize(
        cropped, 
        (512, 384),
        interpolation=cv2.INTER_LINEAR
    )
    
    # 4. 정규화
    # [0, 255] → [-1, 1]
    normalized = (resized.astype(np.float32) / 127.5) - 1.0
    
    return normalized
```

### 시간적 스태킹

모델은 **4개의 프레임**을 동시에 봅니다.

```python
def create_temporal_input(frames):
    # 현재 + 과거 3개 프레임
    # (t, t-1, t-2, t-3)
    
    temporal_stack = np.concatenate([
        frames[0],   # 현재 (t)
        frames[1],   # 50ms 전 (t-1)
        frames[2],   # 100ms 전 (t-2)
        frames[3],   # 150ms 전 (t-3)
    ], axis=2)  # 채널 축으로 연결
    
    # 출력: (384, 512, 12)
    # 12 = RGB × 4 프레임
    return temporal_stack
```

**왜 시간적 스태킹?**
- 움직임 정보 캡처
- 가려진 물체 복원
- 더 안정적인 예측

## 후처리

### 좌표 변환

모델 출력은 **이미지 좌표**이고, 이를 **차량 좌표**로 변환해야 합니다.

```python
def image_to_vehicle_coords(x_img, y_img):
    # 카메라 내부 파라미터
    fx, fy = 910.0, 910.0
    cx, cy = 582.0, 437.0
    
    # 카메라 높이와 피치
    h = 1.22  # m
    pitch = 0.0  # rad
    
    # 이미지 → 카메라 좌표
    x_cam = (x_img - cx) / fx
    y_cam = (y_img - cy) / fy
    
    # 지면 투영
    # z_ground = h / (y_cam * cos(pitch) - sin(pitch))
    z = h / (y_cam * np.cos(pitch) - np.sin(pitch))
    x = x_cam * z
    
    return x, z  # 차량 기준 (좌우, 전방)
```

### 시간적 필터링

노이즈를 줄이기 위한 필터링:

```python
class TemporalFilter:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.prev = None
    
    def update(self, current):
        if self.prev is None:
            self.prev = current
            return current
        
        # Exponential Moving Average
        filtered = (
            self.alpha * current + 
            (1 - self.alpha) * self.prev
        )
        
        self.prev = filtered
        return filtered

# 사용
lane_filter = TemporalFilter(alpha=0.3)

while True:
    raw_lanes = model.predict(frame)
    smooth_lanes = lane_filter.update(raw_lanes)
```

## 모델 평가

### 메트릭

```python
# 학습 중 사용하는 손실 함수

def compute_loss(predictions, labels):
    losses = {}
    
    # 1. 경로 손실 (L1)
    path_loss = torch.mean(torch.abs(
        predictions['path'] - labels['path']
    ))
    losses['path'] = path_loss
    
    # 2. 차선 손실 (L1 + 확률)
    lane_loss = torch.mean(torch.abs(
        predictions['lanes'] - labels['lanes']
    ))
    lane_prob_loss = torch.nn.BCELoss()(
        predictions['lane_probs'],
        labels['lane_exists']
    )
    losses['lane'] = lane_loss + lane_prob_loss
    
    # 3. 선행 차량 손실
    lead_loss = torch.mean(torch.abs(
        predictions['lead_x'] - labels['lead_x']
    )) * labels['lead_prob']  # 있을 때만
    losses['lead'] = lead_loss
    
    # 총 손실 (가중 합)
    total_loss = (
        1.0 * losses['path'] +
        0.5 * losses['lane'] +
        2.0 * losses['lead']
    )
    
    return total_loss, losses
```

### 실전 테스트

```bash
# 테스트 로그로 평가
cd ~/dev/openpilot
python tools/lib/test_model.py \
    --model supercombo.dlc \
    --route "route_name"

# 출력:
# Path error: 0.15m (mean)
# Lane error: 0.08m (mean)
# Lead distance error: 2.3m (mean)
```

## 다음 단계

비전 시스템의 개요를 이해했습니다. 다음 장에서는 모델을 직접 학습하는 방법을 알아봅니다.

---

[다음: 11. 모델 학습 →](./11-model-training.md)
