# 19. 커스텀 모델 만들기

자신만의 AI 비전 모델을 만들고 openpilot에 통합하는 프로젝트입니다.

## 프로젝트 목표

기존 supercombo에 새로운 기능 추가:
- 신호등 감지
- 보행자 감지
- 차선 변경 의도 예측

## 1. 데이터 수집

```python
# 신호등 라벨링
def label_traffic_lights(image):
    # 수동 라벨링 도구 사용
    # labelImg, CVAT 등
    
    lights = [
        {'x': 320, 'y': 100, 'color': 'red'},
        {'x': 640, 'y': 120, 'color': 'green'}
    ]
    
    return lights
```

## 2. 모델 수정

```python
class SuperComboPlus(SuperCombo):
    def __init__(self):
        super().__init__()
        
        # 추가 헤드
        self.traffic_light_head = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 3)  # [red, yellow, green]
        )
    
    def forward(self, x):
        output = super().forward(x)
        
        # 신호등 감지
        feat = self.gru_output
        traffic_light = self.traffic_light_head(feat)
        output['traffic_light'] = torch.softmax(traffic_light, dim=1)
        
        return output
```

## 3. 학습

```python
# 학습 루프에 추가
def train_with_traffic_lights():
    for images, labels in train_loader:
        predictions = model(images)
        
        # 기존 손실
        loss = criterion(predictions, labels)
        
        # 신호등 손실 추가
        if 'traffic_light' in labels:
            tl_loss = nn.CrossEntropyLoss()(
                predictions['traffic_light'],
                labels['traffic_light']
            )
            loss += 0.5 * tl_loss
        
        loss.backward()
        optimizer.step()
```

## 4. 통합

```python
# selfdrive/modeld/modeld.py 수정

# 모델 로드
model = load_model('supercombo_plus.dlc')

# 추론
output = model.run(frame)

# 신호등 정보 발행
pm.send('trafficLight', output['traffic_light'])
```

## 5. 제어 로직 추가

```python
# controlsd에서 사용
sm = SubMaster(['trafficLight'])

if sm['trafficLight'].color == 'red':
    # 정지
    actuators.accel = -2.0
```

## 다음 단계

---

[다음: 20. 시뮬레이터 개발 →](./20-simulator.md)
