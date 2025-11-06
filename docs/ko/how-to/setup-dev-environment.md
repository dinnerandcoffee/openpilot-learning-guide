# openpilot 개발 환경 구축 가이드

openpilot 개발을 시작하기 위한 환경 설정 가이드입니다.

---

## 📋 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [Linux/macOS 환경 설정](#linuxmacos-환경-설정)
3. [Windows (WSL) 환경 설정](#windows-wsl-환경-설정)
4. [저장소 클론 및 설정](#저장소-클론-및-설정)
5. [빌드 및 테스트](#빌드-및-테스트)
6. [도구 설치](#도구-설치)
7. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 하드웨어

- **CPU**: x86_64 또는 ARM64 (Apple Silicon 지원)
- **RAM**: 최소 8GB, 권장 16GB 이상
- **디스크**: 최소 20GB 여유 공간
- **GPU**: (선택) NVIDIA GPU (모델 학습 시)

### 소프트웨어

- **OS**: 
  - Ubuntu 20.04/22.04/24.04 (권장)
  - macOS 11+ (Apple Silicon 또는 Intel)
  - Windows 10/11 (WSL2 사용)
- **Python**: 3.11 이상
- **Git**: 2.x 이상

---

## Linux/macOS 환경 설정

### 1. 기본 도구 설치

#### Ubuntu/Debian

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y \
  build-essential \
  git \
  curl \
  wget \
  python3 \
  python3-pip \
  python3-venv \
  libssl-dev \
  libffi-dev \
  libncurses5-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  llvm \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  liblzma-dev

# Qt 관련 패키지 (UI 개발 시)
sudo apt install -y \
  qt6-base-dev \
  libqt6widgets6 \
  libqt6gui6 \
  libqt6core6
```

#### macOS

```bash
# Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 필수 패키지 설치
brew install \
  python@3.11 \
  git \
  cmake \
  qt@6 \
  capnp \
  coreutils \
  eigen \
  ffmpeg \
  glfw \
  libarchive \
  libusb \
  libtool \
  llvm \
  openssl \
  portaudio \
  protobuf \
  pyenv \
  zeromq
```

### 2. Python 환경 설정

#### pyenv 설치 (권장)

```bash
# pyenv 설치
curl https://pyenv.run | bash

# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 설정 적용
source ~/.bashrc

# Python 3.11 설치
pyenv install 3.11.9
pyenv global 3.11.9

# 확인
python --version  # Python 3.11.9 출력되어야 함
```

---

## Windows (WSL) 환경 설정

### 1. WSL2 설치

```powershell
# PowerShell을 관리자 권한으로 실행

# WSL 활성화
wsl --install

# 시스템 재부팅 후 Ubuntu 설치
wsl --install -d Ubuntu-22.04
```

### 2. Ubuntu 설정

WSL Ubuntu 터미널에서:

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 위의 Ubuntu/Debian 섹션과 동일하게 진행
```

### 3. Windows와 WSL 연동

```bash
# Windows 파일 시스템 접근
cd /mnt/c/Users/YourName/

# VS Code 설치 (Windows에서)
# VS Code에서 WSL 확장 설치: "Remote - WSL"
```

---

## 저장소 클론 및 설정

### 1. openpilot 클론

```bash
# 작업 디렉토리 생성
mkdir -p ~/projects
cd ~/projects

# 원본 저장소 클론
git clone https://github.com/commaai/openpilot.git
cd openpilot

# 또는 자신의 포크 클론
git clone https://github.com/YOUR_USERNAME/openpilot.git
cd openpilot

# upstream 추가 (포크한 경우)
git remote add upstream https://github.com/commaai/openpilot.git
```

### 2. 서브모듈 초기화

```bash
# 서브모듈 업데이트
git submodule update --init --recursive
```

### 3. Python 의존성 설치

openpilot은 `uv`를 사용하여 Python 의존성을 관리합니다.

```bash
# uv 설치 (최신 방법)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 또는 pip로 설치
pip install uv

# 의존성 설치
cd ~/projects/openpilot
uv sync --all-extras

# 가상 환경 활성화
source .venv/bin/activate
```

---

## 빌드 및 테스트

### 1. 프로젝트 빌드

```bash
# openpilot 디렉토리에서
cd ~/projects/openpilot

# scons를 사용하여 빌드
scons -j$(nproc)

# 또는 특정 타겟만 빌드
scons -j$(nproc) selfdrive/
```

### 2. 테스트 실행

```bash
# 모든 테스트 실행
pytest .

# 특정 테스트 실행
pytest selfdrive/test/

# 커버리지와 함께 테스트
pytest --cov=./ --cov-report=html
```

### 3. 시뮬레이터 실행

```bash
# 시뮬레이터 실행 (실제 차량 없이 테스트)
./tools/sim/launch_openpilot.sh

# 별도 터미널에서 시뮬레이션 시작
./tools/sim/start_carla.sh
```

---

## 도구 설치

### 1. 개발 도구

#### VS Code 설정

```bash
# VS Code 설치 (Ubuntu)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# 추천 확장:
# - Python
# - Pylance
# - GitLens
# - C/C++
```

#### PyCharm (대안)

```bash
# JetBrains Toolbox를 통해 설치 권장
# https://www.jetbrains.com/toolbox-app/
```

### 2. CAN 분석 도구

#### cabana 설치

```bash
# openpilot/tools/cabana
cd ~/projects/openpilot/tools/cabana

# 빌드
./build.sh

# 실행
./cabana
```

### 3. Replay 도구

```bash
# 주행 데이터 재생
cd ~/projects/openpilot

# comma connect에서 다운로드한 로그 재생
./tools/replay/replay <log_directory>
```

---

## 문제 해결

### 일반적인 문제

#### 1. Python 버전 문제

```bash
# Python 버전 확인
python --version

# 3.11 이상이 아니면 pyenv로 설치
pyenv install 3.11.9
pyenv local 3.11.9
```

#### 2. 빌드 오류

```bash
# 깨끗한 빌드
scons -c  # 클린
scons -j$(nproc)  # 다시 빌드

# 의존성 문제 시 재설치
rm -rf .venv
uv sync --all-extras
```

#### 3. 서브모듈 문제

```bash
# 서브모듈 초기화 재실행
git submodule deinit -f .
git submodule update --init --recursive
```

#### 4. 권한 문제 (Linux)

```bash
# sudo 없이 docker 사용
sudo usermod -aG docker $USER
newgrp docker
```

### macOS 특정 문제

#### Qt 경로 문제

```bash
# Qt 경로 설정
export Qt6_DIR=$(brew --prefix qt@6)
export PATH="$Qt6_DIR/bin:$PATH"
```

#### Apple Silicon (M1/M2) 문제

```bash
# Rosetta 없이 네이티브 빌드
arch -arm64 brew install ...

# 일부 패키지는 x86_64 필요
arch -x86_64 brew install ...
```

---

## 개발 워크플로우

### 1. 일반적인 개발 사이클

```bash
# 1. 최신 코드 가져오기
git pull upstream master

# 2. 새 브랜치 생성
git checkout -b feature/my-feature

# 3. 코드 수정

# 4. 테스트
pytest selfdrive/test/

# 5. 빌드
scons -j$(nproc)

# 6. 커밋
git add .
git commit -m "Add my feature"

# 7. 푸시
git push origin feature/my-feature

# 8. PR 생성 (GitHub에서)
```

### 2. 코드 스타일 확인

```bash
# pre-commit 설치
pip install pre-commit
pre-commit install

# 수동 실행
pre-commit run --all-files

# 자동으로 커밋 전 실행됨
```

### 3. 디버깅

```bash
# Python 디버거 사용
python -m pdb selfdrive/controls/controlsd.py

# 로그 확인
tail -f /data/log/
```

---

## 다음 단계

환경 구축이 완료되었다면:

1. **[첫 빌드 가이드](./first-build.md)**: 첫 빌드 해보기
2. **[코드 구조 이해](../concepts/architecture.md)**: 아키텍처 파악
3. **[간단한 수정](./simple-modifications.md)**: 파라미터 튜닝
4. **[테스트 작성](./writing-tests.md)**: 테스트 코드 작성

---

## 참고 자료

- [openpilot 공식 문서](https://docs.comma.ai)
- [openpilot Wiki](https://github.com/commaai/openpilot/wiki)
- [comma.ai Discord](https://discord.comma.ai)

---

<div align="center">

**개발 환경 구축 완료를 축하합니다! 🎉**

질문이 있으시면 [Discord](https://discord.comma.ai)에 물어보세요!

</div>
