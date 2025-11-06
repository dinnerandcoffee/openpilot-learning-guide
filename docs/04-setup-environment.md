# 4. 개발 환경 설정

이제 openpilot 개발을 위한 환경을 구축해봅시다. 이 장에서는 운영 체제별 설정 방법을 다룹니다.

## 개요

**목표**: 로컬 컴퓨터에서 openpilot을 빌드하고 실행할 수 있는 환경 만들기

**소요 시간**: 1-2시간 (인터넷 속도에 따라 다름)

**결과물**: 
- Python 3.11+ 설치
- 필수 패키지 설치
- 개발 도구 설정

## 운영 체제 선택

시작하기 전에 어떤 OS를 사용할지 선택하세요.

| OS | 난이도 | 권장도 | 특징 |
|-----|--------|--------|------|
| Ubuntu 22.04 | ⭐ 쉬움 | ⭐⭐⭐⭐⭐ | 가장 권장, 공식 지원 |
| macOS | ⭐⭐ 보통 | ⭐⭐⭐⭐ | Apple Silicon 지원 |
| WSL2 (Windows) | ⭐⭐⭐ 어려움 | ⭐⭐⭐ | Windows 사용자용 |

**초보자 권장**: Ubuntu 22.04 LTS

## Ubuntu 22.04 설정

가장 권장하는 환경입니다. openpilot 개발팀도 Ubuntu를 사용합니다.

### 1. 시스템 업데이트

먼저 시스템을 최신 상태로 업데이트합니다.

```bash
# 패키지 목록 업데이트
sudo apt update

# 설치된 패키지 업그레이드
sudo apt upgrade -y

# 재부팅 (커널 업데이트 시)
sudo reboot  # 필요한 경우만
```

### 2. 필수 패키지 설치

openpilot 빌드에 필요한 기본 도구들을 설치합니다.

```bash
# 빌드 도구
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates

# Python 관련
sudo apt install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip

# 라이브러리
sudo apt install -y \
    libssl-dev \
    libffi-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    zlib1g-dev \
    libxml2-dev \
    libxmlsec1-dev

# 시스템 도구
sudo apt install -y \
    tmux \
    htop \
    tree \
    vim
```

### 3. Python 3.11 확인

```bash
# Python 버전 확인
python3.11 --version
# 출력: Python 3.11.x

# 기본 python3를 3.11로 설정 (선택사항)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

### 4. pip 업그레이드

```bash
# pip 최신 버전으로 업그레이드
python3.11 -m pip install --upgrade pip

# 확인
python3.11 -m pip --version
```

### 5. Git 설정

```bash
# Git 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 에디터 설정 (선택)
git config --global core.editor "vim"

# 확인
git config --list
```

## macOS 설정

macOS 사용자를 위한 설정입니다. Intel과 Apple Silicon 모두 지원합니다.

### 1. Homebrew 설치

macOS의 패키지 관리자인 Homebrew를 설치합니다.

```bash
# Homebrew 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 환경 변수 설정 (Apple Silicon의 경우)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# 확인
brew --version
```

### 2. 필수 도구 설치

```bash
# Python 3.11
brew install python@3.11

# Git
brew install git

# 개발 도구
brew install \
    cmake \
    make \
    gcc

# 유용한 도구
brew install \
    tmux \
    htop \
    tree \
    wget
```

### 3. Xcode Command Line Tools

```bash
# Xcode CLI 도구 설치
xcode-select --install

# 확인
xcode-select -p
```

### 4. Python 경로 설정

```bash
# .zshrc 또는 .bash_profile에 추가
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc

# 적용
source ~/.zshrc

# 확인
python3.11 --version
```

### 5. Git 설정

```bash
# Git 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# macOS Keychain 사용
git config --global credential.helper osxkeychain
```

## Windows + WSL2 설정

Windows에서 Linux 환경을 사용하는 방법입니다.

### 1. WSL2 활성화

PowerShell을 **관리자 권한**으로 실행:

```powershell
# WSL 설치
wsl --install

# 시스템 재부팅
Restart-Computer
```

### 2. Ubuntu 설치

재부팅 후:

```powershell
# Ubuntu 22.04 설치
wsl --install -d Ubuntu-22.04

# 설치 확인
wsl -l -v
```

### 3. Ubuntu 초기 설정

Ubuntu가 실행되면 사용자 이름과 비밀번호를 설정합니다.

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y
```

### 4. WSL2 최적화

**Windows에서** (PowerShell):

```powershell
# .wslconfig 파일 생성
notepad $env:USERPROFILE\.wslconfig
```

다음 내용 추가:

```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### 5. WSL에서 Ubuntu 설정

이후 과정은 "Ubuntu 22.04 설정"과 동일합니다.

**팁**: Windows와 WSL 간 파일 접근
```bash
# Windows 파일 접근
cd /mnt/c/Users/YourName/

# WSL 파일을 Windows에서 접근
# 파일 탐색기에서: \\wsl$\Ubuntu-22.04\home\
```

## VS Code 설정

모든 OS에서 사용 가능한 VS Code 설정입니다.

### 1. VS Code 설치

**Ubuntu**:
```bash
# Microsoft GPG 키 추가
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/

# 저장소 추가
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'

# 설치
sudo apt update
sudo apt install code
```

**macOS**:
```bash
brew install --cask visual-studio-code
```

**Windows**:
- https://code.visualstudio.com 에서 다운로드

### 2. 필수 확장 설치

VS Code에서 다음 확장을 설치하세요:

1. **Python** (Microsoft)
   - Python 언어 지원
   - 디버깅, 린팅

2. **Pylance** (Microsoft)
   - 빠른 타입 체킹
   - IntelliSense 향상

3. **GitLens** (GitKraken)
   - Git 히스토리
   - Blame 주석

4. **Remote - SSH** (Microsoft)
   - 원격 개발 (WSL 포함)

5. **Python Indent** (Kevin Rose)
   - 자동 들여쓰기

### 3. VS Code 설정

`settings.json` 열기: `Cmd/Ctrl + Shift + P` → "Preferences: Open Settings (JSON)"

```json
{
    "python.defaultInterpreterPath": "/usr/bin/python3.11",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "git.autofetch": true
}
```

## pyenv 설치 (선택사항)

여러 Python 버전을 관리하려면 pyenv를 사용하세요.

### Ubuntu/macOS:

```bash
# pyenv 설치
curl https://pyenv.run | bash

# 환경 변수 설정 (~/.bashrc 또는 ~/.zshrc에 추가)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 적용
source ~/.bashrc

# Python 3.11 설치
pyenv install 3.11.9
pyenv global 3.11.9

# 확인
python --version
```

## Docker 설치 (선택사항)

일부 테스트나 격리된 환경이 필요할 때 유용합니다.

### Ubuntu:

```bash
# Docker 설치 스크립트
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 로그아웃 후 다시 로그인하거나:
newgrp docker

# 확인
docker run hello-world
```

### macOS:

```bash
# Docker Desktop 설치
brew install --cask docker

# Docker 앱 실행
open -a Docker
```

## SSH 키 생성 (GitHub용)

GitHub에 코드를 푸시하려면 SSH 키가 필요합니다.

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@example.com"

# 기본 경로 사용 (Enter)
# 비밀번호 설정 (선택사항)

# 공개 키 확인
cat ~/.ssh/id_ed25519.pub

# 이 키를 GitHub에 등록:
# GitHub.com → Settings → SSH and GPG keys → New SSH key
```

## 환경 확인

모든 설정이 완료되었는지 확인합니다.

```bash
# Python 버전
python3.11 --version
# 출력: Python 3.11.x

# pip 버전
python3.11 -m pip --version
# 출력: pip 24.x.x

# Git 버전
git --version
# 출력: git version 2.x.x

# 디스크 공간 확인
df -h
# 최소 20GB 여유 공간 필요

# RAM 확인
free -h  # Ubuntu
# 또는
sysctl hw.memsize  # macOS
```

## 트러블슈팅

### Python 버전 문제

**문제**: `python3.11: command not found`

**해결**:
```bash
# Ubuntu: Python 3.11 설치 확인
sudo apt install python3.11

# macOS: Homebrew로 재설치
brew reinstall python@3.11
```

### 권한 문제

**문제**: `Permission denied`

**해결**:
```bash
# sudo 없이 Docker 사용
sudo usermod -aG docker $USER
newgrp docker

# pip 설치 시 권한 오류
python3.11 -m pip install --user <package>
```

### WSL 네트워크 문제

**문제**: WSL에서 인터넷 안 됨

**해결**:
```bash
# DNS 재설정
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo chattr +i /etc/resolv.conf
```

## 다음 단계

환경 설정이 완료되었습니다! 

다음 장에서는 실제로 openpilot 저장소를 클론하고 첫 빌드를 해봅시다.

---

[다음: 5. 저장소 클론 및 빌드 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/05-clone-and-build.md)
