# 12. 모델 최적화

학습한 모델을 실제 comma 장치에서 효율적으로 실행하기 위한 최적화 기법들을 다룹니다.

## 최적화 목표

**목표**:
- 추론 속도 향상 (20+ FPS)
- 메모리 사용량 감소
- 배터리 효율 개선
- 정확도 유지

**제약 조건**:
- Snapdragon 845/8 Gen 1
- 제한된 메모리 (4-8GB)
- 열 관리 필요

## 양자화 (Quantization)

### FP32 → INT8

```python
import torch
from torch.quantization import quantize_dynamic

# 동적 양자화
model_quantized = quantize_dynamic(
    model, 
    {torch.nn.Linear, torch.nn.Conv2d},
    dtype=torch.qint8
)

# 모델 크기 비교
def print_model_size(model):
    torch.save(model.state_dict(), "temp.pth")
    size_mb = os.path.getsize("temp.pth") / 1024 / 1024
    print(f"Model size: {size_mb:.2f} MB")
    os.remove("temp.pth")

print_model_size(model)  # ~30 MB
print_model_size(model_quantized)  # ~8 MB
```

### 양자화 인식 학습 (QAT)

```python
from torch.quantization import prepare_qat, convert

# QAT 설정
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model_prepared = prepare_qat(model)

# 재학습 (fine-tuning)
for epoch in range(10):
    train_one_epoch(model_prepared, train_loader)

# INT8로 변환
model_quantized = convert(model_prepared)
```

## 프루닝 (Pruning)

### 구조적 프루닝

```python
import torch.nn.utils.prune as prune

def prune_model(model, amount=0.3):
    """불필요한 뉴런 제거"""
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.l1_unstructured(module, name='weight', amount=amount)
            prune.remove(module, 'weight')
    
    return model

# 30% 프루닝
model_pruned = prune_model(model, amount=0.3)

# 정확도 복구를 위한 fine-tuning
for epoch in range(5):
    train_one_epoch(model_pruned, train_loader)
```

## 지식 증류 (Knowledge Distillation)

### Teacher-Student

```python
class DistillationLoss(nn.Module):
    def __init__(self, temperature=3.0, alpha=0.7):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.criterion = nn.MSELoss()
    
    def forward(self, student_output, teacher_output, labels):
        # Hard loss (실제 라벨)
        hard_loss = self.criterion(student_output, labels)
        
        # Soft loss (teacher 모방)
        soft_loss = self.criterion(
            student_output / self.temperature,
            teacher_output.detach() / self.temperature
        )
        
        # 결합
        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss

# Teacher (큰 모델)
teacher = SuperCombo()
teacher.load_state_dict(torch.load('best_model.pth'))
teacher.eval()

# Student (작은 모델)  
student = MiniCombo()

# 증류 학습
criterion = DistillationLoss()

for images, labels in train_loader:
    with torch.no_grad():
        teacher_out = teacher(images)
    
    student_out = student(images)
    loss = criterion(student_out, teacher_out, labels)
    
    # backward & update
    ...
```

## 모델 아키텍처 최적화

### Depthwise Separable Convolution

```python
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super().__init__()
        # Depthwise
        self.depthwise = nn.Conv2d(
            in_channels, in_channels,
            kernel_size=kernel_size,
            groups=in_channels,  # 핵심!
            padding=kernel_size//2
        )
        # Pointwise
        self.pointwise = nn.Conv2d(
            in_channels, out_channels,
            kernel_size=1
        )
    
    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x

# 파라미터 수 비교
# 일반 Conv: in_ch * out_ch * k^2
# DepthwiseSep: in_ch * k^2 + in_ch * out_ch
# 약 8-9배 감소!
```

### Mobile-Optimized Blocks

```python
class MobileBlock(nn.Module):
    """MobileNetV3 스타일 블록"""
    def __init__(self, in_ch, out_ch, expand_ratio=6):
        super().__init__()
        hidden_ch = in_ch * expand_ratio
        
        self.conv = nn.Sequential(
            # Expand
            nn.Conv2d(in_ch, hidden_ch, 1),
            nn.BatchNorm2d(hidden_ch),
            nn.Hardswish(),
            
            # Depthwise
            nn.Conv2d(hidden_ch, hidden_ch, 3, groups=hidden_ch, padding=1),
            nn.BatchNorm2d(hidden_ch),
            nn.Hardswish(),
            
            # SE (Squeeze-Excitation)
            SEBlock(hidden_ch),
            
            # Project
            nn.Conv2d(hidden_ch, out_ch, 1),
            nn.BatchNorm2d(out_ch)
        )
        
        self.use_skip = (in_ch == out_ch)
    
    def forward(self, x):
        if self.use_skip:
            return x + self.conv(x)
        return self.conv(x)
```

## 추론 최적화

### TensorRT 변환

```python
import tensorrt as trt

def build_engine(onnx_path, engine_path):
    """ONNX → TensorRT"""
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)
    
    # ONNX 파싱
    with open(onnx_path, 'rb') as f:
        parser.parse(f.read())
    
    # 빌더 설정
    config = builder.create_builder_config()
    config.max_workspace_size = 1 << 30  # 1GB
    config.set_flag(trt.BuilderFlag.FP16)  # FP16 사용
    
    # 엔진 빌드
    engine = builder.build_engine(network, config)
    
    # 저장
    with open(engine_path, 'wb') as f:
        f.write(engine.serialize())
    
    return engine
```

### 배치 처리

```python
class BatchedInference:
    """여러 프레임을 묶어서 처리"""
    def __init__(self, model, batch_size=4):
        self.model = model
        self.batch_size = batch_size
        self.queue = []
    
    def add_frame(self, frame):
        self.queue.append(frame)
        
        if len(self.queue) >= self.batch_size:
            return self.process_batch()
        return None
    
    def process_batch(self):
        batch = torch.stack(self.queue[:self.batch_size])
        self.queue = self.queue[self.batch_size:]
        
        with torch.no_grad():
            outputs = self.model(batch)
        
        return outputs
```

## 벤치마킹

### 속도 측정

```python
import time

def benchmark_model(model, input_shape, num_runs=100):
    model.eval()
    device = next(model.parameters()).device
    
    # Warm-up
    dummy_input = torch.randn(input_shape).to(device)
    for _ in range(10):
        _ = model(dummy_input)
    
    # 측정
    torch.cuda.synchronize() if device.type == 'cuda' else None
    start = time.time()
    
    for _ in range(num_runs):
        _ = model(dummy_input)
    
    torch.cuda.synchronize() if device.type == 'cuda' else None
    end = time.time()
    
    avg_time = (end - start) / num_runs * 1000  # ms
    fps = 1000 / avg_time
    
    print(f"Average time: {avg_time:.2f} ms")
    print(f"FPS: {fps:.1f}")
    
    return avg_time

# 사용
benchmark_model(model, (1, 4, 3, 384, 512))
```

### 메모리 프로파일링

```python
import torch.cuda

def profile_memory(model, input_shape):
    model.eval()
    model.cuda()
    
    torch.cuda.reset_peak_memory_stats()
    
    dummy_input = torch.randn(input_shape).cuda()
    _ = model(dummy_input)
    
    memory_mb = torch.cuda.max_memory_allocated() / 1024 / 1024
    print(f"Peak memory: {memory_mb:.2f} MB")
    
    return memory_mb
```

## SNPE 최적화

### 양자화 데이터 준비

```python
# input_list.txt 생성
def prepare_calibration_data(dataset, num_samples=100):
    with open('input_list.txt', 'w') as f:
        for i in range(num_samples):
            image, _ = dataset[i]
            
            # Raw 데이터로 저장
            filename = f'calibration/input_{i}.raw'
            image.numpy().tofile(filename)
            
            f.write(f'{filename}\n')

prepare_calibration_data(val_dataset, 100)
```

### SNPE 변환 스크립트

```bash
#!/bin/bash
# convert_to_snpe.sh

# ONNX → DLC
snpe-onnx-to-dlc \
    --input_network supercombo.onnx \
    --output_path supercombo.dlc

# INT8 양자화
snpe-dlc-quantize \
    --input_dlc supercombo.dlc \
    --input_list input_list.txt \
    --output_dlc supercombo_int8.dlc \
    --use_enhanced_quantizer

# 벤치마크
adb push supercombo_int8.dlc /data/local/tmp/
adb shell "snpe-net-run \
    --container /data/local/tmp/supercombo_int8.dlc \
    --input_list /data/local/tmp/input_list.txt"
```

## 실전 최적화 체크리스트

**모델 레벨**:
- [ ] 양자화 (FP32 → INT8)
- [ ] 프루닝 (30% sparse)
- [ ] 지식 증류 (teacher → student)
- [ ] 경량 아키텍처 (MobileNet 블록)

**추론 레벨**:
- [ ] TensorRT/SNPE 변환
- [ ] 배치 처리
- [ ] Mixed precision (FP16)
- [ ] 동적 입력 크기 비활성화

**시스템 레벨**:
- [ ] CPU 고정 (핵심 성능 코어)
- [ ] GPU 주파수 고정
- [ ] 열 관리 (throttling 방지)

## 성능 비교

```
Original Model:
- Size: 30 MB
- Inference: 80ms
- Accuracy: 95%

Optimized Model:
- Size: 8 MB (4배 감소)
- Inference: 35ms (2.3배 빠름)
- Accuracy: 94% (1% 감소)

목표 달성! ✓
```

## 다음 단계

Part 4 완료! 비전 시스템을 완전히 이해했습니다.

Part 5에서는 제어 시스템을 다룹니다:
- 횡방향 제어
- 종방향 제어  
- 튜닝 방법

---

[다음: Part 5 - 제어 시스템 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/13-lateral-control.md)
