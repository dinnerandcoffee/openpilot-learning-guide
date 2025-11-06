# openpilot 시작하기

openpilot을 처음 접하시는 분들을 위한 완벽 가이드입니다.

---

## 📚 목차

1. [openpilot이란?](#openpilot이란)
2. [시작하기 전에](#시작하기-전에)
3. [학습 경로](#학습-경로)
4. [첫 번째 단계](#첫-번째-단계)

---

## openpilot이란?

**openpilot**은 comma.ai에서 개발한 오픈소스 운전자 보조 시스템(ADAS)입니다.

### 주요 특징

- 🚗 **레벨 2 자율주행**: 차선 유지 + 적응형 크루즈 컨트롤
- 🌍 **오픈소스**: 누구나 코드를 보고 수정 가능 (MIT 라이선스)
- 🔧 **275+ 차량 지원**: 다양한 제조사의 차량 지원
- 🤖 **AI 기반**: 딥러닝을 활용한 비전 시스템
- 📊 **데이터 기반 개선**: 사용자 주행 데이터로 지속적 개선

### openpilot이 할 수 있는 것

✅ 차선 중앙 유지 (Lateral Control)  
✅ 앞차와의 거리 유지 (Longitudinal Control)  
✅ 커브길 주행  
✅ 저속 정체 상황 대응  
✅ 부드러운 가감속  

### openpilot이 할 수 없는 것

❌ 완전 자율주행 (항상 운전자 감시 필요)  
❌ 교차로 신호 판단  
❌ 차선 변경 자동 실행 (일부 차량에서만 가능)  
❌ 주차  
❌ 비포장도로 주행  

---

## 시작하기 전에

### 필요한 것

#### 1️⃣ 차량에서 사용하려면

- ✅ [지원되는 차량](../CARS.md) 확인
- ✅ comma 3X 장치 ([구매 링크](https://comma.ai/shop/comma-3x))
- ✅ 차량 하네스 ([구매 링크](https://comma.ai/shop/car-harness))
- ✅ 기본적인 차량 지식

#### 2️⃣ 개발/학습만 하려면

- ✅ Linux/macOS/WSL 환경
- ✅ Python 3.11+ 지식
- ✅ Git 기본 사용법
- ✅ 터미널 사용 경험
- ✅ (선택) C/C++ 지식

### 배경 지식

openpilot을 제대로 이해하려면 다음 분야의 기초 지식이 도움됩니다:

- **Python 프로그래밍**: openpilot의 대부분이 Python으로 작성됨
- **컴퓨터 비전**: 카메라 기반 인식 시스템
- **제어 이론**: PID, MPC 등의 제어 알고리즘
- **머신러닝**: 딥러닝 모델 학습 및 배포
- **자동차 기초**: CAN 버스, ECU, 센서 등

💡 **초보자 팁**: 모든 것을 완벽히 알 필요는 없습니다! 하나씩 학습하면서 진행하세요.

---

## 학습 경로

openpilot을 배우는 추천 경로입니다.

### 🎯 레벨 1: 기초 이해 (1-2주)

**목표**: openpilot이 무엇인지, 어떻게 작동하는지 이해하기

- [ ] README와 공식 문서 읽기
- [ ] [용어 사전](../GLOSSARY.md) 숙지
- [ ] YouTube에서 openpilot 주행 영상 시청
- [ ] comma connect에서 주행 데이터 둘러보기
- [ ] Discord 커뮤니티 가입

**학습 자료**:
- [openpilot 공식 문서](https://docs.comma.ai)
- [comma.ai 블로그](https://blog.comma.ai)
- [George Hotz의 강의](https://comma.ai/lectures)

### 🎯 레벨 2: 환경 구축 (1주)

**목표**: 로컬에서 openpilot 실행 환경 만들기

- [ ] 저장소 클론
- [ ] 개발 환경 설정
- [ ] 빌드 성공
- [ ] 시뮬레이터에서 실행
- [ ] 간단한 코드 수정 및 테스트

**가이드**:
- [개발 환경 구축](../how-to/setup-dev-environment.md)
- [첫 빌드 가이드](./first-build.md)

### 🎯 레벨 3: 코드 분석 (2-4주)

**목표**: openpilot의 구조와 주요 컴포넌트 이해

- [ ] 디렉토리 구조 파악
- [ ] 주요 프로세스(controlsd, plannerd, modeld) 분석
- [ ] CAN 메시지 흐름 이해
- [ ] 제어 로직 분석
- [ ] 간단한 파라미터 튜닝

**학습 포인트**:
- `selfdrive/` 디렉토리 구조
- `cereal/` 메시지 정의
- `opendbc/` 차량 인터페이스
- `panda/` 하드웨어 인터페이스

### 🎯 레벨 4: 고급 개발 (진행 중)

**목표**: 실제 기여 및 커스터마이징

- [ ] 새 기능 구현
- [ ] 버그 수정
- [ ] Pull Request 제출
- [ ] 새 차량 포팅
- [ ] 모델 학습 및 개선

---

## 첫 번째 단계

### 1. 저장소 클론하기

```bash
# 원본 저장소 클론
git clone https://github.com/commaai/openpilot.git
cd openpilot

# 또는 포크한 저장소 클론
git clone https://github.com/your-username/openpilot.git
cd openpilot
```

### 2. 문서 읽기

openpilot을 사용하기 전에 반드시 읽어야 할 문서들:

1. **[README.md](../README.md)**: 프로젝트 개요
2. **[SAFETY.md](../SAFETY.md)**: 안전 정책 ⚠️ 매우 중요!
3. **[LIMITATIONS.md](../LIMITATIONS.md)**: 시스템 한계
4. **[CARS.md](../CARS.md)**: 지원 차량 목록

### 3. 커뮤니티 참여

- **Discord**: [discord.comma.ai](https://discord.comma.ai)
  - 질문하고 답변 받기
  - 다른 사용자들과 경험 공유
  - 최신 업데이트 받기

- **GitHub**:
  - Issues: 버그 리포트, 기능 제안
  - Discussions: 일반적인 토론
  - Pull Requests: 코드 기여

### 4. 실습 시작

#### A. 시뮬레이터로 시작 (추천)

실제 차량 없이 openpilot을 체험:

```bash
# 시뮬레이터 실행 (자세한 가이드는 별도 문서 참조)
./tools/sim/launch_openpilot.sh
```

#### B. 실제 차량에서 사용

1. comma 3X 구매
2. 차량 하네스 준비
3. [설치 가이드](https://comma.ai/setup) 따라하기
4. 안전한 장소에서 테스트

### 5. 코드 탐험

openpilot 코드를 처음 볼 때 시작하기 좋은 파일들:

```python
# 1. 메인 실행 파일
launch_openpilot.sh

# 2. 제어 관련
selfdrive/controls/controlsd.py

# 3. 경로 계획
selfdrive/controls/plannerd.py

# 4. 비전 모델
selfdrive/modeld/

# 5. 차량 인터페이스
selfdrive/car/
```

---

## 📖 다음 단계

학습을 계속하려면:

1. **[핵심 개념](../concepts/)**: openpilot의 아키텍처 이해
2. **[개발 가이드](../how-to/)**: 실습 중심 튜토리얼
3. **[차량 포팅](../car-porting/)**: 새 차량 추가 방법
4. **[기여 가이드](../CONTRIBUTING.md)**: 프로젝트에 기여하기

---

## ❓ 자주 묻는 질문 (FAQ)

### Q: openpilot은 무료인가요?
A: 소프트웨어는 오픈소스(MIT)로 무료입니다. 하지만 comma 3X 하드웨어는 구매해야 합니다.

### Q: 한국에서도 사용할 수 있나요?
A: 네, 지원되는 차량이라면 사용 가능합니다. 하지만 도로교통법을 반드시 준수해야 합니다.

### Q: 프로그래밍을 모르는데 사용할 수 있나요?
A: 사용은 가능하지만, 커스터마이징이나 문제 해결을 위해서는 기본적인 프로그래밍 지식이 필요합니다.

### Q: 안전한가요?
A: openpilot은 보조 시스템입니다. **항상 운전자가 도로를 주시하고 언제든 개입할 준비가 되어 있어야 합니다.**

### Q: 얼마나 자주 업데이트되나요?
A: 거의 매일 코드가 업데이트됩니다. 안정 버전은 2-3주마다 릴리스됩니다.

---

## 🆘 도움 받기

문제가 생겼을 때:

1. **문서 확인**: docs/ 디렉토리의 관련 문서
2. **검색**: GitHub Issues에서 비슷한 문제 검색
3. **Discord**: 커뮤니티에 질문
4. **Issue 생성**: 새로운 버그나 문제 리포트

---

## ⚠️ 중요한 주의사항

1. **항상 주의를 기울이세요**: openpilot은 보조 시스템일 뿐입니다
2. **법규 준수**: 현지 도로교통법을 반드시 준수하세요
3. **안전 우선**: 확신이 없으면 사용하지 마세요
4. **단계적 학습**: 한 번에 모든 것을 이해하려 하지 마세요

---

<div align="center">

**openpilot 학습 여정을 응원합니다! 🚀**

질문이나 피드백은 [Issues](https://github.com/dinnerandcoffee/openpilot/issues)로 부탁드립니다.

</div>
