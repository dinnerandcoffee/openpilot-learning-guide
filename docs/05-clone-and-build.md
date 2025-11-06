# 5. 저장소 클론 및 빌드

이제 실제로 openpilot 코드를 다운로드하고 첫 빌드를 해봅시다.

## 개요

**목표**: openpilot 저장소를 클론하고 성공적으로 빌드하기

**소요 시간**: 30분 - 1시간 (인터넷 속도 및 컴퓨터 성능에 따라)

**필요 공간**: 약 5-10GB

## 작업 디렉토리 준비

먼저 작업할 디렉토리를 만듭니다.

```bash
# 홈 디렉토리로 이동
cd ~

# 개발 디렉토리 생성 (선택사항)
mkdir -p ~/dev
cd ~/dev
```

**추천 디렉토리 구조**:
```
~/dev/
├── openpilot/           # 공식 openpilot
├── openpilot-fork/      # 내 포크 (나중에)
└── openpilot-tools/     # 분석 도구들
```

## Git 클론

### 방법 1: HTTPS 클론 (권장 - 초보자)

```bash
# openpilot 저장소 클론
git clone https://github.com/commaai/openpilot.git

# 디렉토리 이동
cd openpilot

# 확인
ls -la
```

**장점**:
- 간단하고 빠름
- SSH 키 설정 불필요

**단점**:
- Push 시 매번 인증 필요

### 방법 2: SSH 클론 (권장 - 기여자)

```bash
# SSH 클론
git clone git@github.com:commaai/openpilot.git

cd openpilot
```

**장점**:
- Push 시 자동 인증
- 보안성 높음

**단점**:
- SSH 키 설정 필요 (이전 장 참조)

### 클론 확인

```bash
# 저장소 정보 확인
git remote -v
# 출력:
# origin  https://github.com/commaai/openpilot.git (fetch)
# origin  https://github.com/commaai/openpilot.git (push)

# 현재 브랜치 확인
git branch
# 출력: * master

# 최근 커밋 확인
git log --oneline -5
```

## 저장소 구조 이해

클론한 디렉토리 구조를 살펴봅시다.

```bash
# 트리 구조 보기
tree -L 1 -d

# 또는
ls -F
```

**주요 디렉토리**:

```
openpilot/
├── cereal/              # 메시지 정의 (Protocol Buffers)
├── common/              # 공통 유틸리티
├── opendbc/             # DBC 파일 (CAN 메시지 정의)
├── panda/               # Panda 펌웨어 (C/C++)
├── selfdrive/           # 핵심 코드 (주행 로직)
│   ├── car/             # 차량별 인터페이스
│   ├── controls/        # 제어 로직
│   ├── locationd/       # 위치 추정
│   ├── modeld/          # AI 모델 (vision)
│   ├── ui/              # 사용자 인터페이스
│   └── manager/         # 프로세스 관리
├── system/              # 시스템 레벨 코드
├── tools/               # 개발 도구
├── SConstruct           # 빌드 스크립트
├── launch_openpilot.sh  # 실행 스크립트
└── pyproject.toml       # Python 프로젝트 설정
```

**핵심 파일**:
- `SConstruct`: SCons 빌드 시스템 설정
- `pyproject.toml`: Python 의존성 및 프로젝트 메타데이터
- `launch_openpilot.sh`: openpilot 실행 스크립트
- `README.md`: 프로젝트 소개

## 의존성 설치

openpilot 실행에 필요한 Python 패키지들을 설치합니다.

### Python 가상 환경 생성

```bash
# 가상 환경 생성
python3.11 -m venv venv

# 활성화
source venv/bin/activate

# 확인 (프롬프트에 (venv) 표시됨)
which python
# 출력: /home/user/dev/openpilot/venv/bin/python
```

**왜 가상 환경을?**
- 시스템 Python과 격리
- 의존성 충돌 방지
- 프로젝트별 패키지 관리

### 의존성 설치

```bash
# pip 업그레이드
pip install --upgrade pip

# openpilot 의존성 설치
pip install -e .

# 시간이 좀 걸립니다 (5-10분)
# 다음과 같은 패키지들이 설치됩니다:
# - numpy, scipy
# - opencv-python
# - PyQt5
# - cereal (openpilot의 메시징 라이브러리)
# - 등등...
```

**설치 중 발생할 수 있는 경고**:
```
WARNING: Running pip as the 'root' user...
```
→ 무시해도 됨 (가상 환경 사용 중)

### 추가 도구 설치

```bash
# 개발 도구 (선택사항)
pip install \
    pytest \
    pytest-cov \
    ruff \
    mypy
```

## 첫 빌드

이제 openpilot을 빌드해봅시다.

### SCons 빌드

openpilot은 SCons 빌드 시스템을 사용합니다.

```bash
# SCons 설치 확인
scons --version

# 전체 빌드
scons -j$(nproc)

# 설명:
# -j$(nproc): 병렬 빌드 (CPU 코어 수만큼)
```

**빌드 과정**:
```
Compiling selfdrive/boardd/boardd.cc
Compiling selfdrive/locationd/paramsd.cc
Compiling cereal/gen/cpp/log.capnp.c++
...
많은 파일들이 컴파일됩니다
...
Build succeeded.
```

**소요 시간**:
- 첫 빌드: 10-30분 (컴퓨터 성능에 따라)
- 이후 빌드: 1-5분 (변경된 파일만)

### 빌드 확인

```bash
# 빌드 결과물 확인
ls -lh selfdrive/boardd/boardd
ls -lh selfdrive/locationd/paramsd

# 권한 확인
file selfdrive/boardd/boardd
# 출력: selfdrive/boardd/boardd: ELF 64-bit LSB executable...
```

## 테스트 실행

빌드가 성공했는지 테스트로 확인합니다.

### 단위 테스트

```bash
# pytest 실행
pytest selfdrive/test/

# 특정 테스트만
pytest selfdrive/test/test_fingerprints.py

# 커버리지 포함
pytest --cov=selfdrive selfdrive/test/
```

**성공 예시**:
```
===== test session starts =====
platform linux -- Python 3.11.9
collected 157 items

selfdrive/test/test_fingerprints.py ........ [ 5%]
selfdrive/test/test_models.py ............ [12%]
...
===== 157 passed in 45.23s =====
```

### 간단한 실행 테스트

```bash
# 도움말 확인
python selfdrive/manager/manager.py --help

# 또는 간단한 모듈 임포트 테스트
python -c "import cereal; print('cereal imported successfully')"
python -c "from selfdrive.car import fingerprints; print('OK')"
```

## 특정 브랜치 체크아웃

개발 중인 특정 버전을 사용하고 싶다면:

```bash
# 모든 브랜치 보기
git branch -a

# 태그 목록
git tag -l

# 특정 버전 체크아웃
git checkout v0.9.7

# 또는 최신 릴리스
git checkout $(git describe --tags --abbrev=0)

# master로 돌아가기
git checkout master
```

## 업데이트 받기

나중에 최신 코드로 업데이트:

```bash
# 변경사항 확인
git status

# 최신 코드 가져오기
git pull origin master

# 의존성 업데이트
pip install -e . --upgrade

# 리빌드
scons -j$(nproc)
```

## 포크 만들기 (기여하려면)

나중에 코드를 수정하고 기여하려면 포크를 만드세요.

### GitHub에서 포크

1. https://github.com/commaai/openpilot 방문
2. 우측 상단 "Fork" 버튼 클릭
3. 내 계정으로 포크 생성

### 로컬에서 원격 저장소 추가

```bash
# 내 포크를 원격 저장소로 추가
git remote add fork git@github.com:YOUR_USERNAME/openpilot.git

# 확인
git remote -v
# 출력:
# origin  https://github.com/commaai/openpilot.git (fetch)
# origin  https://github.com/commaai/openpilot.git (push)
# fork    git@github.com:YOUR_USERNAME/openpilot.git (fetch)
# fork    git@github.com:YOUR_USERNAME/openpilot.git (push)

# 브랜치 생성 및 작업
git checkout -b my-feature

# 변경 후 내 포크에 푸시
git push fork my-feature
```

## 개발 워크플로우

일반적인 개발 흐름:

```bash
# 1. 최신 코드 받기
git checkout master
git pull origin master

# 2. 새 브랜치 생성
git checkout -b feature/my-improvement

# 3. 코드 수정
vim selfdrive/controls/controlsd.py

# 4. 빌드 및 테스트
scons -j$(nproc)
pytest selfdrive/test/

# 5. 커밋
git add selfdrive/controls/controlsd.py
git commit -m "Improve lateral control tuning"

# 6. 포크에 푸시
git push fork feature/my-improvement

# 7. GitHub에서 Pull Request 생성
```

## 빌드 최적화

### 특정 타겟만 빌드

```bash
# 전체 빌드 대신 특정 타겟만
scons selfdrive/boardd/boardd
scons selfdrive/controls/
```

### 병렬 빌드 조절

```bash
# CPU 코어 수 확인
nproc

# 4코어로 제한 (과열 방지)
scons -j4
```

### ccache 사용 (빌드 캐싱)

```bash
# ccache 설치
sudo apt install ccache  # Ubuntu
brew install ccache      # macOS

# 환경 변수 설정
echo 'export CC="ccache gcc"' >> ~/.bashrc
echo 'export CXX="ccache g++"' >> ~/.bashrc
source ~/.bashrc

# 이후 빌드는 더 빠름
```

## 트러블슈팅

### 빌드 실패: 의존성 문제

**문제**: `ModuleNotFoundError: No module named 'numpy'`

**해결**:
```bash
# 가상 환경 활성화 확인
source venv/bin/activate

# 의존성 재설치
pip install -e .
```

### 빌드 실패: 컴파일 오류

**문제**: `fatal error: 'capnp/serialize.h' file not found`

**해결**:
```bash
# Ubuntu: 시스템 패키지 설치
sudo apt install \
    capnproto \
    libcapnp-dev

# macOS
brew install capnp

# 다시 빌드
scons -c  # 클린
scons -j$(nproc)
```

### 메모리 부족

**문제**: 빌드 중 시스템이 느려지거나 멈춤

**해결**:
```bash
# 병렬 작업 수 줄이기
scons -j2  # 2개만

# 또는 스왑 메모리 늘리기 (Ubuntu)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Git LFS 문제

**문제**: AI 모델 파일이 제대로 다운로드 안 됨

**해결**:
```bash
# Git LFS 설치
sudo apt install git-lfs  # Ubuntu
brew install git-lfs      # macOS

# Git LFS 초기화
git lfs install

# 파일 다운로드
git lfs pull
```

## 검증 체크리스트

빌드가 제대로 되었는지 확인:

- [ ] `git clone` 성공
- [ ] 가상 환경 생성 및 활성화
- [ ] `pip install -e .` 성공
- [ ] `scons -j$(nproc)` 빌드 성공
- [ ] `pytest` 테스트 통과
- [ ] 바이너리 파일 생성 확인
- [ ] Python 모듈 임포트 가능

## 다음 단계

빌드가 성공했습니다! 

다음 장에서는 실제로 openpilot을 실행하고 테스트해봅시다.

---

[다음: 6. 첫 실행 및 테스트 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/06-first-run.md)
