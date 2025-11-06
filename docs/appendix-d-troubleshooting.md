# 부록 D: 문제 해결

openpilot 개발 중 흔히 발생하는 문제와 해결 방법

## 빌드 문제

### 1. SCons 빌드 실패

**증상**:
```
Error: ... not found
```

**해결**:
```bash
# 종속성 재설치
./tools/ubuntu_setup.sh

# 캐시 정리
scons -c
rm -rf .sconsign.dblite .scons_cache

# 재빌드
scons -j$(nproc)
```

### 2. Python 패키지 오류

**증상**:
```
ModuleNotFoundError: No module named 'cereal'
```

**해결**:
```bash
# cereal 재빌드
cd cereal
scons -j$(nproc)

# 또는
pip install -e .
```

## 실행 문제

### 1. 프로세스가 시작되지 않음

**증상**:
```
Process modeld failed to start
```

**해결**:
```bash
# 로그 확인
cat /tmp/modeld.log

# 수동 실행으로 디버깅
cd selfdrive/modeld
./modeld
```

### 2. 모델 로드 실패

**증상**:
```
Failed to load supercombo.dlc
```

**해결**:
```bash
# Git LFS 설치
sudo apt install git-lfs
git lfs install

# 모델 다운로드
git lfs pull

# 파일 확인
ls -lh models/supercombo.dlc  # 30MB 이상이어야 함
```

## CAN 버스 문제

### 1. panda 연결 안 됨

**증상**:
```
PandaConnectionError
```

**해결**:
```bash
# USB 권한 확인
sudo usermod -a -G dialout $USER

# panda 재설정
python -c "from panda import Panda; Panda().reset()"

# lsusb로 확인
lsusb | grep panda
```

### 2. CAN 메시지 수신 안 됨

**해결**:
```python
from panda import Panda

p = Panda()
# 버스 확인
for i in range(3):
    msgs = p.can_recv()
    print(f"Bus {i}: {len([m for m in msgs if m[3] == i])} messages")
```

## 성능 문제

### 1. modeld 너무 느림

**해결**:
```bash
# SNPE 최적화 확인
ll models/*.dlc

# CPU 주파수 확인
cat /proc/cpuinfo | grep MHz
```

### 2. 메모리 부족

**해결**:
```bash
# 메모리 사용량 확인
free -h

# 불필요한 프로세스 종료
pkill -f ui
```

## 모델 학습 문제

### 1. OOM (Out of Memory)

**해결**:
```python
# 배치 크기 줄이기
BATCH_SIZE = 4  # 32에서 줄임

# Gradient Accumulation
for i, (images, labels) in enumerate(train_loader):
    loss = model(images, labels)
    loss = loss / ACCUMULATION_STEPS
    loss.backward()
    
    if (i + 1) % ACCUMULATION_STEPS == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 2. 학습이 수렴하지 않음

**해결**:
```python
# Learning rate 조정
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=5
)

# Gradient clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

## 차량 포팅 문제

### 1. Fingerprint 실패

**해결**:
```bash
# CAN 메시지 로깅
./tools/lib/logreader.py "route" | grep "can"

# cabana로 분석
./tools/cabana/cabana "route_url"
```

### 2. 조향이 작동하지 않음

**체크리스트**:
- [ ] Safety model 확인
- [ ] CAN 주소 확인
- [ ] Checksum 계산 확인
- [ ] 조향 제한 확인

## 디버깅 팁

### 로그 레벨 설정

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Detailed info")
logger.info("General info")
logger.warning("Warning")
logger.error("Error occurred")
```

### GDB 사용

```bash
# C++ 프로세스 디버깅
gdb --args ./modeld
(gdb) break modeld.cc:123
(gdb) run
```

### Valgrind로 메모리 누수 확인

```bash
valgrind --leak-check=full ./modeld
```

## 도움 받기

문제가 해결되지 않으면:
1. [Discord](https://discord.comma.ai)에서 질문
2. [GitHub Issues](https://github.com/commaai/openpilot/issues) 검색
3. 자세한 로그와 함께 이슈 생성

---

**학습 가이드 완료를 축하합니다! 🎉**

[처음으로 돌아가기 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/01-intro.md)
