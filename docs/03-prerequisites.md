# 3. 준비하기

openpilot을 배우고 사용하기 위해 필요한 것들을 정리해봅시다. 목적에 따라 필요한 준비물이 다릅니다.

## 두 가지 경로

### 경로 1: 차량에서 실제 사용

**목적**: 내 차에 openpilot을 설치하여 실제로 사용

**필요한 것**:
- ✅ 지원되는 차량
- ✅ comma 3X 장치
- ✅ 차량 하네스
- ✅ 기본적인 차량 지식

**이 책의 범위**: Part 1-2에서 설치 방법 다룸

### 경로 2: 개발 및 학습

**목적**: 코드를 이해하고, 수정하고, 기여하기

**필요한 것**:
- ✅ 개발 환경 (컴퓨터)
- ✅ 프로그래밍 지식
- ✅ 개발 도구

**이 책의 범위**: Part 1-7 전체

## 차량에서 사용하기 위한 준비

### 1. 차량 확인

**지원 여부 확인**

가장 먼저 확인해야 할 것은 내 차가 지원되는지입니다.

```bash
# 방법 1: 온라인에서 확인
https://comma.ai/vehicles

# 방법 2: GitHub에서 확인
https://github.com/commaai/openpilot/blob/master/docs/CARS.md
```

**확인해야 할 사항**:

1. **제조사 및 모델**
   - 예: Hyundai Sonata 2020

2. **지원 수준**
   - ⭐⭐⭐ Full Support: 모든 기능
   - ⭐⭐ Limited: 일부 기능만
   - ⭐ Experimental: 테스트 단계

3. **필요한 기능**
   - LKAS (Lane Keeping Assist System)
   - SCC (Smart Cruise Control) 또는 ACC
   - CAN 게이트웨이 접근 가능

**한국 차량 예시**:

| 제조사 | 인기 모델 | 지원 수준 |
|--------|----------|----------|
| Hyundai | Sonata (2020+) | ⭐⭐⭐ |
| Hyundai | Palisade (2020+) | ⭐⭐⭐ |
| Kia | K5 (2021+) | ⭐⭐⭐ |
| Genesis | G70 (2019+) | ⭐⭐⭐ |

### 2. comma 3X 구매

**공식 스토어**:
- https://comma.ai/shop
- 가격: $1,299 (2025년 기준)

**포함 사항**:
```
comma 3X 패키지
├── comma 3X 본체
├── 마운트 (흡착식)
├── USB 케이블
├── 시가잭 충전기
└── 설명서
```

**별도 구매 필요**:
- 차량 하네스 (차량별로 다름)

### 3. 차량 하네스

**하네스란?**

comma 3X를 차량의 CAN 버스에 연결하는 케이블입니다.

**선택 방법**:
1. comma.ai 웹사이트에서 차량 모델 입력
2. 추천되는 하네스 확인
3. 구매

**가격**: 약 $100-200

**주의사항**:
- 차량 모델/연식별로 다름
- 잘못된 하네스 사용 시 작동 불가
- 일부 차량은 추가 어댑터 필요

### 4. 기본 지식

**필요한 지식**:
- ✅ 기본적인 차량 구조 이해
- ✅ 퓨즈박스 위치 파악 능력
- ✅ 간단한 배선 이해
- ✅ 안전 운전 능력

**권장 지식**:
- CAN 버스 개념
- ADAS 시스템 이해
- 기본 전기 지식

## 개발 및 학습을 위한 준비

### 1. 하드웨어 요구사항

**최소 사양**:
```
CPU: x86_64 또는 ARM64
RAM: 8GB
디스크: 20GB 여유 공간
OS: Ubuntu 20.04+ / macOS 11+ / Windows 10+ (WSL2)
```

**권장 사양**:
```
CPU: 멀티코어 (4코어 이상)
RAM: 16GB 이상
디스크: SSD 50GB 이상
GPU: NVIDIA GPU (모델 학습 시)
인터넷: 안정적인 고속 연결
```

**왜 이런 사양이 필요한가?**:
- openpilot 빌드: 많은 메모리와 CPU 사용
- 시뮬레이션: GPU 가속 필요
- 대용량 주행 데이터 다운로드: 디스크 공간

### 2. 운영 체제

**Linux (가장 권장)**

```bash
# Ubuntu 22.04 LTS 권장
# 이유:
- openpilot 개발 환경과 동일
- 패키지 설치 쉬움
- 문제 해결 자료 많음
```

**macOS**

```bash
# macOS 11 (Big Sur) 이상
# 특징:
- Apple Silicon (M1/M2) 지원
- Unix 기반으로 호환성 좋음
- 일부 패키지 설치 번거로움
```

**Windows + WSL2**

```powershell
# Windows 10/11 + WSL2
# 설정:
wsl --install -d Ubuntu-22.04

# 특징:
- Windows에서 Linux 사용 가능
- 약간의 성능 오버헤드
- GUI 앱 실행은 복잡
```

**권장**: Ubuntu Linux 또는 macOS

### 3. 프로그래밍 지식

**필수 지식**:

**Python** (⭐⭐⭐⭐⭐ 매우 중요)
```python
# openpilot 대부분이 Python으로 작성됨

# 알아야 할 것:
- 기본 문법 (변수, 함수, 클래스)
- 객체지향 프로그래밍
- 리스트, 딕셔너리 등 자료구조
- 모듈과 패키지
- 예외 처리

# 권장 수준:
- Python 책 1권 완독
- 간단한 프로젝트 경험
```

**Git/GitHub** (⭐⭐⭐⭐ 중요)
```bash
# 필수 명령어들:
git clone
git add / commit / push
git branch / checkout
git pull / merge

# 권장:
- GitHub 계정 생성
- Fork, Pull Request 이해
- .gitignore 이해
```

**Linux 터미널** (⭐⭐⭐ 중요)
```bash
# 기본 명령어:
cd, ls, pwd          # 디렉토리 탐색
cat, less, grep      # 파일 읽기
cp, mv, rm           # 파일 조작
chmod, chown         # 권한 관리

# 권장:
- vim 또는 nano 사용법
- 파이프(|)와 리다이렉션(>)
- 환경 변수
```

**선택적 지식**:

**C/C++** (⭐⭐ 선택)
```c
// panda 펌웨어, 일부 성능 코드
// 고급 개발자용
// 초보자는 나중에 배워도 됨
```

**딥러닝** (⭐⭐ 선택)
```python
# AI 모델 이해/개선 시 필요
# PyTorch, NumPy
# 처음에는 몰라도 됨
```

**자동차 지식** (⭐⭐ 선택)
```
# CAN 버스, ECU 등
# 차량 포팅 시 필요
# 학습하면서 익힐 수 있음
```

### 4. 개발 도구

**필수 도구**:

**1. Python 3.11+**
```bash
# 설치 확인
python3 --version
# Python 3.11.0 이상이어야 함

# 없다면 설치 (Ubuntu)
sudo apt install python3.11 python3.11-venv python3-pip
```

**2. Git**
```bash
# 설치 확인
git --version

# 없다면 설치
# Ubuntu:
sudo apt install git

# macOS:
brew install git
```

**3. 텍스트 에디터/IDE**

**VS Code** (가장 권장)
```bash
# 설치: https://code.visualstudio.com

# 추천 확장:
- Python (Microsoft)
- Pylance (Microsoft)
- GitLens
- Remote - SSH (WSL/원격 개발)
```

**PyCharm** (대안)
```bash
# 설치: https://www.jetbrains.com/pycharm

# 특징:
- 강력한 Python IDE
- 디버깅 도구 우수
- 유료 (Community 무료)
```

**vim/emacs** (고급 사용자)
```bash
# 터미널 기반 에디터
# 학습 곡선 높음
# 익숙하다면 매우 효율적
```

**선택 도구**:

**4. tmux**
```bash
# 터미널 멀티플렉서
sudo apt install tmux

# comma 장치 SSH 접속 시 유용
```

**5. Docker**
```bash
# 컨테이너 환경
# 일부 테스트에 사용

# 설치 (Ubuntu):
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 5. 학습 자료

**공식 자료**:
```
문서: https://docs.comma.ai
저장소: https://github.com/commaai/openpilot
블로그: https://blog.comma.ai
Discord: https://discord.comma.ai
```

**이 책**:
```
순서대로 읽으면서 실습
막히면 부록 FAQ 참조
커뮤니티에 질문
```

**추가 학습 자료**:
```
Python: "점프 투 파이썬" (온라인 무료)
Git: "Pro Git" (온라인 무료)
자율주행: Coursera "Self-Driving Cars"
```

## 비용 정리

### 차량에서 사용

| 항목 | 가격 (USD) | 비고 |
|------|-----------|------|
| comma 3X | $1,299 | 필수 |
| 하네스 | $100-200 | 필수 |
| 배송비 | $50 | 국가별 다름 |
| comma Prime | $99/년 | 선택 (무제한 저장) |
| **합계** | **~$1,550** | 초기 비용 |

### 개발 및 학습

| 항목 | 가격 | 비고 |
|------|------|------|
| 컴퓨터 | 보유 | 최소 사양 충족 필요 |
| 소프트웨어 | 무료 | 모두 오픈소스 |
| 학습 자료 | 무료 | 이 책 포함 |
| **합계** | **무료** | 컴퓨터만 있으면 됨 |

## 시간 투자

**차량 설치**:
```
하네스 설치: 30분 - 1시간
comma 3X 설정: 30분
첫 주행 및 적응: 1-2주
```

**개발 학습**:
```
환경 구축: 1-2일
기초 이해 (Part 1-3): 2-3주
코드 분석 (Part 4-6): 1-2개월
실전 프로젝트 (Part 7): 진행 중
```

## 체크리스트

출발하기 전에 확인하세요!

### 차량 사용자

- [ ] 내 차가 지원되는지 확인
- [ ] comma 3X 주문 (또는 준비)
- [ ] 하네스 주문 (차량 모델 확인)
- [ ] 설치 가이드 읽기 (comma.ai/setup)
- [ ] 안전 수칙 숙지

### 개발자

- [ ] 컴퓨터 사양 확인 (8GB+ RAM)
- [ ] 운영 체제 준비 (Ubuntu/macOS)
- [ ] Python 3.11+ 설치
- [ ] Git 설치 및 GitHub 계정
- [ ] 텍스트 에디터/IDE 설치
- [ ] 터미널 기본 명령어 숙지
- [ ] Python 기초 지식 확인

## 다음 단계

이제 준비가 되었나요?

**차량 사용자**는 Part 2로 이동하여 설치를 시작하세요.

**개발자**는 Part 2의 개발 환경 구축으로 이동하세요.

---

[다음: 4. 개발 환경 설정 →](./04-setup-environment.md)
