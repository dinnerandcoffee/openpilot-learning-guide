# 11. 모델 학습

openpilot 비전 모델을 직접 학습하는 방법을 알아봅시다. 데이터 준비부터 배포까지 전 과정을 다룹니다.

## 개요

**학습 과정**:
1. 데이터 준비
2. 모델 설계
3. 학습 실행
4. 검증 및 평가
5. 양자화 및 변환
6. 배포

**필요한 것**:
- GPU (NVIDIA, 16GB+ VRAM 권장)
- PyTorch
- 대용량 저장소 (1TB+)
- 주행 데이터

## 환경 설정

### GPU 환경

```bash
# CUDA 설치 확인
nvidia-smi

# PyTorch 설치 (CUDA 11.8 예시)
pip install torch torchvision \
    --index-url https://download.pytorch.org/whl/cu118

# 확인
python -c "import torch; print(torch.cuda.is_available())"
```

### 의존성 설치

```bash
cd ~/dev/openpilot

# 학습 도구
pip install \
    tensorboard \
    tqdm \
    scipy \
    scikit-learn

# 데이터 처리
pip install \
    h5py \
    opencv-python \
    pillow
```

## 데이터 준비

### 1. 로그 다운로드

```bash
# comma API 키 설정
export COMMA_API_KEY="your_api_key"

# 로그 다운로드 스크립트
cd ~/dev/openpilot/tools

# 특정 route 다운로드
python lib/route.py \
    "a2a0ccea32023010|2023-07-27--13-01-19" \
    --download

# 여러 route 다운로드
python lib/route.py \
    --download-list routes.txt \
    --output-dir ~/data/openpilot_data
```

**routes.txt 예시**:
```
a2a0ccea32023010|2023-07-27--13-01-19
b3b1ddeb43034021|2023-07-28--09-15-32
c4c2eefa54045032|2023-07-29--14-22-41
```

### 2. 데이터 전처리

```python
#!/usr/bin/env python3
# tools/lib/prepare_training_data.py

import numpy as np
from tools.lib.logreader import LogReader
import cv2

def extract_frames_and_labels(route_path):
    """로그에서 학습 데이터 추출"""
    
    # 로그 읽기
    lr = LogReader(f"{route_path}/rlog.bz2")
    
    # 비디오 열기
    cap = cv2.VideoCapture(f"{route_path}/fcamera.hevc")
    
    data = []
    frame_idx = 0
    
    for msg in lr:
        # carState와 동기화
        if msg.which() == 'carState':
            cs = msg.carState
            
            # 프레임 읽기
            ret, frame = cap.read()
            if not ret:
                break
            
            # 라벨 생성
            label = {
                # 실제 조향각
                'steer_angle': cs.steeringAngleDeg,
                
                # 속도
                'speed': cs.vEgo,
                
                # 타임스탬프
                'timestamp': msg.logMonoTime,
            }
            
            # 저장
            data.append({
                'frame': frame,
                'label': label
            })
            
            frame_idx += 1
    
    cap.release()
    return data

# 실행
if __name__ == '__main__':
    import sys
    route = sys.argv[1]
    data = extract_frames_and_labels(route)
    
    # HDF5로 저장
    import h5py
    with h5py.File('training_data.h5', 'w') as f:
        f.create_dataset('frames', data=[d['frame'] for d in data])
        f.create_dataset('labels', data=[d['label'] for d in data])
```

### 3. 데이터 증강

```python
import torch
import torchvision.transforms as T

class DrivingDataAugmentation:
    def __init__(self):
        self.transforms = T.Compose([
            # 1. 밝기 조정
            T.ColorJitter(
                brightness=0.3,
                contrast=0.3,
                saturation=0.3
            ),
            
            # 2. 그림자 시뮬레이션
            RandomShadow(p=0.5),
            
            # 3. 노이즈 추가
            T.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
            
            # 4. 정규화
            T.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def __call__(self, image):
        return self.transforms(image)

class RandomShadow:
    """랜덤 그림자 추가"""
    def __init__(self, p=0.5):
        self.p = p
    
    def __call__(self, img):
        if np.random.rand() > self.p:
            return img
        
        # 그림자 마스크 생성
        h, w = img.shape[:2]
        x1 = np.random.randint(0, w)
        y1 = np.random.randint(0, h)
        x2 = np.random.randint(0, w)
        y2 = np.random.randint(0, h)
        
        mask = np.zeros((h, w), dtype=np.float32)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 1, -1)
        
        # 그림자 적용
        img_shadow = img.copy()
        img_shadow = img_shadow * (1 - 0.5 * mask[..., None])
        
        return img_shadow.astype(np.uint8)
```

## 모델 설계

### PyTorch 모델

```python
# selfdrive/modeld/models/supercombo.py

import torch
import torch.nn as nn

class SuperCombo(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 1. Feature Extractor (Backbone)
        self.backbone = EfficientNetLite0(pretrained=True)
        
        # 2. Temporal Module (GRU)
        self.gru = nn.GRU(
            input_size=1280,  # EfficientNet output
            hidden_size=512,
            num_layers=2,
            batch_first=True
        )
        
        # 3. Task-specific Heads
        self.lane_head = LaneHead(512)
        self.lead_head = LeadHead(512)
        self.path_head = PathHead(512)
    
    def forward(self, x, hidden=None):
        # x: (batch, seq_len, 3, H, W)
        batch_size, seq_len = x.shape[:2]
        
        # 1. Extract features per frame
        features = []
        for t in range(seq_len):
            feat = self.backbone(x[:, t])
            features.append(feat)
        
        features = torch.stack(features, dim=1)
        # (batch, seq_len, 1280)
        
        # 2. Temporal aggregation
        gru_out, hidden = self.gru(features, hidden)
        # (batch, seq_len, 512)
        
        # 마지막 타임스텝만 사용
        feat_t = gru_out[:, -1]
        
        # 3. Task predictions
        lanes = self.lane_head(feat_t)
        leads = self.lead_head(feat_t)
        path = self.path_head(feat_t)
        
        return {
            'lanes': lanes,
            'leads': leads,
            'path': path,
            'hidden': hidden
        }

class LaneHead(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 4 * 192 * 3)  # 4 lanes × 192 points × 3 coords
        )
    
    def forward(self, x):
        out = self.fc(x)
        # Reshape to (batch, 4, 192, 3)
        return out.view(-1, 4, 192, 3)

class LeadHead(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Linear(256, 2 * (1 + 100 * 4))  # 2 leads × (prob + 100 points × 4 values)
        )
    
    def forward(self, x):
        out = self.fc(x)
        # Reshape and parse
        return out.view(-1, 2, 401)

class PathHead(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Linear(256, 200 * 3)  # 200 points × 3 coords
        )
    
    def forward(self, x):
        out = self.fc(x)
        return out.view(-1, 200, 3)
```

### 손실 함수

```python
class SuperComboLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.L1Loss()
        self.bce = nn.BCEWithLogitsLoss()
    
    def forward(self, predictions, labels):
        losses = {}
        
        # 1. 경로 손실
        path_loss = self.l1(
            predictions['path'],
            labels['path']
        )
        losses['path'] = path_loss
        
        # 2. 차선 손실
        lane_loss = self.l1(
            predictions['lanes'],
            labels['lanes']
        )
        
        # 차선 존재 확률
        lane_prob_loss = self.bce(
            predictions['lane_probs'],
            labels['lane_exists'].float()
        )
        losses['lane'] = lane_loss + 0.1 * lane_prob_loss
        
        # 3. 선행 차량 손실
        # (차량이 있을 때만)
        lead_mask = labels['lead_prob'] > 0.5
        if lead_mask.any():
            lead_loss = self.l1(
                predictions['leads'][lead_mask],
                labels['leads'][lead_mask]
            )
        else:
            lead_loss = torch.tensor(0.0)
        
        losses['lead'] = lead_loss
        
        # 총 손실 (가중 합)
        total_loss = (
            1.0 * losses['path'] +
            0.5 * losses['lane'] +
            2.0 * losses['lead']
        )
        
        return total_loss, losses
```

## 학습 실행

### 학습 루프

```python
#!/usr/bin/env python3
# tools/train/train_supercombo.py

import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

def train():
    # 설정
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_epochs = 100
    batch_size = 32
    learning_rate = 1e-4
    
    # 모델
    model = SuperCombo().to(device)
    
    # 옵티마이저
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate,
        weight_decay=1e-5
    )
    
    # 스케줄러
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=num_epochs
    )
    
    # 데이터
    train_dataset = DrivingDataset('train_data.h5', augment=True)
    val_dataset = DrivingDataset('val_data.h5', augment=False)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4
    )
    
    # 손실 함수
    criterion = SuperComboLoss()
    
    # TensorBoard
    writer = SummaryWriter('runs/supercombo')
    
    # 학습 루프
    for epoch in range(num_epochs):
        # Train
        model.train()
        train_loss = 0
        
        pbar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}')
        for batch_idx, (images, labels) in enumerate(pbar):
            images = images.to(device)
            labels = {k: v.to(device) for k, v in labels.items()}
            
            # Forward
            optimizer.zero_grad()
            predictions = model(images)
            loss, loss_dict = criterion(predictions, labels)
            
            # Backward
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            # 로깅
            train_loss += loss.item()
            pbar.set_postfix({'loss': loss.item()})
            
            # TensorBoard
            global_step = epoch * len(train_loader) + batch_idx
            writer.add_scalar('Loss/train', loss.item(), global_step)
            for k, v in loss_dict.items():
                writer.add_scalar(f'Loss/{k}', v.item(), global_step)
        
        # Validation
        model.eval()
        val_loss = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = {k: v.to(device) for k, v in labels.items()}
                
                predictions = model(images)
                loss, _ = criterion(predictions, labels)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        print(f'Validation Loss: {val_loss:.4f}')
        writer.add_scalar('Loss/val', val_loss, epoch)
        
        # 스케줄러 업데이트
        scheduler.step()
        
        # 체크포인트 저장
        if (epoch + 1) % 10 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': val_loss,
            }, f'checkpoints/supercombo_epoch_{epoch+1}.pth')
    
    writer.close()

if __name__ == '__main__':
    train()
```

### 모니터링

```bash
# TensorBoard 실행
tensorboard --logdir runs/

# 브라우저에서 확인
# http://localhost:6006
```

## 모델 검증

### 정량적 평가

```python
def evaluate_model(model, test_loader, device):
    model.eval()
    
    metrics = {
        'path_error': [],
        'lane_error': [],
        'lead_error': []
    }
    
    with torch.no_grad():
        for images, labels in tqdm(test_loader):
            images = images.to(device)
            labels = {k: v.to(device) for k, v in labels.items()}
            
            predictions = model(images)
            
            # 경로 오차
            path_error = torch.abs(
                predictions['path'] - labels['path']
            ).mean().item()
            metrics['path_error'].append(path_error)
            
            # 차선 오차
            lane_error = torch.abs(
                predictions['lanes'] - labels['lanes']
            ).mean().item()
            metrics['lane_error'].append(lane_error)
            
            # 선행 차량 오차
            lead_mask = labels['lead_prob'] > 0.5
            if lead_mask.any():
                lead_error = torch.abs(
                    predictions['leads'][lead_mask] - 
                    labels['leads'][lead_mask]
                ).mean().item()
                metrics['lead_error'].append(lead_error)
    
    # 평균 계산
    for k in metrics:
        metrics[k] = np.mean(metrics[k])
    
    print("Evaluation Metrics:")
    print(f"  Path Error: {metrics['path_error']:.3f} m")
    print(f"  Lane Error: {metrics['lane_error']:.3f} m")
    print(f"  Lead Error: {metrics['lead_error']:.3f} m")
    
    return metrics
```

### 정성적 평가

```python
import matplotlib.pyplot as plt

def visualize_predictions(model, image, device):
    model.eval()
    
    with torch.no_grad():
        image_tensor = torch.from_numpy(image).unsqueeze(0).to(device)
        predictions = model(image_tensor)
    
    # 시각화
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(image)
    
    # 차선 그리기
    lanes = predictions['lanes'][0].cpu().numpy()
    for i, lane in enumerate(lanes):
        x, y = lane[:, 0], lane[:, 1]
        ax.plot(x, y, label=f'Lane {i}')
    
    # 경로 그리기
    path = predictions['path'][0].cpu().numpy()
    ax.plot(path[:, 0], path[:, 1], 'r-', linewidth=3, label='Path')
    
    # 선행 차량
    leads = predictions['leads'][0].cpu().numpy()
    for i, lead in enumerate(leads):
        if lead[0] > 0.5:  # 확률 > 0.5
            x, y = lead[1], lead[2]
            ax.plot(x, y, 'ro', markersize=10, label=f'Lead {i}')
    
    ax.legend()
    plt.show()
```

## 모델 변환 및 배포

### PyTorch → ONNX

```python
def export_to_onnx(model, output_path):
    model.eval()
    
    # 더미 입력
    dummy_input = torch.randn(1, 4, 3, 384, 512)
    
    # ONNX 변환
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=13,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['lanes', 'leads', 'path'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'lanes': {0: 'batch_size'},
            'leads': {0: 'batch_size'},
            'path': {0: 'batch_size'}
        }
    )

# 사용
export_to_onnx(model, 'supercombo.onnx')
```

### ONNX → SNPE (Qualcomm)

```bash
# SNPE 도구 사용
snpe-onnx-to-dlc \
    --input_network supercombo.onnx \
    --output_path supercombo.dlc

# 양자화 (INT8)
snpe-dlc-quantize \
    --input_dlc supercombo.dlc \
    --input_list input_list.txt \
    --output_dlc supercombo_quantized.dlc
```

### 성능 테스트

```bash
# comma 장치에서 실행
cd /data/openpilot

# 모델 교체
cp supercombo_quantized.dlc models/supercombo.dlc

# 벤치마크
python selfdrive/modeld/test/benchmark.py

# 출력:
# Inference time: 35.2ms (avg)
# Throughput: 28.4 FPS
```

## 다음 단계

모델 학습을 완료했습니다! 다음 장에서는 모델을 더욱 최적화하는 방법을 알아봅니다.

---

[다음: 12. 모델 최적화 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/12-model-optimization.md)
