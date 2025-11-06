# openpilot 학습 로드맵

openpilot을 체계적으로 학습하기 위한 단계별 로드맵입니다.

---

## 📊 학습 로드맵 개요

```
Phase 1: 기초 (2-3주)
    ↓
Phase 2: 실습 환경 구축 (1주)
    ↓
Phase 3: 코드 이해 (4-6주)
    ↓
Phase 4: 심화 학습 (4-8주)
    ↓
Phase 5: 실전 프로젝트 (진행 중)
```

---

## 🎯 Phase 1: 기초 다지기 (2-3주)

### 목표
- openpilot이 무엇인지 이해
- 자율주행의 기본 개념 파악
- 필요한 배경 지식 습득

### 학습 내용

#### Week 1: openpilot 이해하기

**Day 1-2: 문서 읽기**
- [ ] [메인 README](../README.md) 정독
- [ ] [openpilot 소개](README.md) 읽기
- [ ] [용어 사전](GLOSSARY.md) 숙지
- [ ] openpilot 공식 문서 브라우징 (https://docs.comma.ai)

**Day 3-4: 영상 자료**
- [ ] YouTube에서 openpilot 주행 영상 10개 이상 시청
- [ ] George Hotz의 강의 영상 시청
  - "Programming with comma" 시리즈
  - "How openpilot works" 강의
- [ ] comma.ai 제품 소개 영상

**Day 5-7: 커뮤니티 탐색**
- [ ] Discord 가입 및 채널 둘러보기
- [ ] GitHub Issues/Discussions 읽기
- [ ] comma connect 둘러보기 (https://connect.comma.ai)
- [ ] 블로그 글 읽기 (https://blog.comma.ai)

#### Week 2: 기술 배경 지식

**자율주행 기초**
- [ ] 자율주행 레벨 (Level 0-5) 이해
- [ ] ADAS vs 자율주행 차이점
- [ ] 센서 종류: 카메라, 레이더, 라이다
- [ ] 비전 기반 vs 센서 융합 방식

**컴퓨터 비전 기초**
- [ ] 이미지 처리 기본 개념
- [ ] CNN (Convolutional Neural Network) 기초
- [ ] 객체 탐지 (Object Detection)
- [ ] 차선 탐지 (Lane Detection)

**추천 학습 자료:**
- Coursera: "Self-Driving Cars Specialization" (Univ. of Toronto)
- YouTube: "Two Minute Papers" - 자율주행 관련 영상
- 책: "Programming Computer Vision with Python"

#### Week 3: 자동차 및 제어 기초

**자동차 시스템**
- [ ] CAN 버스란 무엇인가
- [ ] ECU (Electronic Control Unit) 이해
- [ ] 조향, 가속, 제동 시스템
- [ ] OBD-II 프로토콜

**제어 이론 기초**
- [ ] PID 컨트롤러 원리
- [ ] 피드백 제어 (Feedback Control)
- [ ] MPC (Model Predictive Control) 개념
- [ ] 안정성과 응답성

**추천 학습 자료:**
- YouTube: "Brian Douglas" - Control Systems 강의
- 책: "Feedback Control of Dynamic Systems"
- 온라인: MIT OpenCourseWare - Control Systems

### 체크리스트
- [ ] openpilot이 무엇인지 설명할 수 있다
- [ ] 레벨 2 자율주행의 의미를 안다
- [ ] CAN 버스의 역할을 이해한다
- [ ] PID 컨트롤러의 기본 원리를 안다
- [ ] CNN이 무엇인지 대략 이해한다

---

## 🛠️ Phase 2: 실습 환경 구축 (1주)

### 목표
- 로컬에서 openpilot 개발 환경 구축
- 기본적인 빌드 및 실행 경험

### 학습 내용

#### Day 1-2: 환경 설정

**개발 환경 구축**
- [ ] [개발 환경 구축 가이드](how-to/setup-dev-environment.md) 따라하기
- [ ] Python 3.11+ 설치
- [ ] 필수 패키지 설치
- [ ] Git 설정 (username, email)

**저장소 준비**
- [ ] openpilot 저장소 fork
- [ ] 로컬에 clone
- [ ] 서브모듈 초기화
- [ ] 의존성 설치 (`uv sync`)

#### Day 3-4: 첫 빌드

**빌드 실습**
- [ ] scons를 사용한 빌드
- [ ] 빌드 오류 해결
- [ ] 테스트 실행 (`pytest`)
- [ ] 주요 도구 확인

**도구 익히기**
- [ ] Git 기본 명령어 (add, commit, push)
- [ ] VS Code 또는 선호하는 IDE 설정
- [ ] 터미널 기본 명령어

#### Day 5-7: 시뮬레이터 실행

**시뮬레이션 환경**
- [ ] CARLA 시뮬레이터 설치 (선택)
- [ ] replay 도구 사용법 익히기
- [ ] 주행 로그 다운로드 및 재생
- [ ] UI 탐색

**간단한 수정**
- [ ] 파라미터 하나 수정해보기
- [ ] 재빌드 및 테스트
- [ ] 변경사항 커밋

### 체크리스트
- [ ] 로컬에서 openpilot 빌드 성공
- [ ] 테스트가 정상적으로 실행된다
- [ ] replay 도구로 주행 로그를 재생할 수 있다
- [ ] Git으로 코드 수정 및 커밋을 할 수 있다

---

## 📖 Phase 3: 코드 이해하기 (4-6주)

### 목표
- openpilot 아키텍처 완전 이해
- 주요 컴포넌트의 역할 파악
- 코드 읽기 및 디버깅 능력 향상

### Week 1: 아키텍처 이해

**전체 구조 파악**
- [ ] [핵심 개념](concepts/README.md) 정독
- [ ] 디렉토리 구조 탐색
- [ ] 프로세스 간 통신 흐름 이해
- [ ] cereal 메시지 시스템 파악

**실습:**
```bash
# 주요 디렉토리 탐색
ls -la openpilot/selfdrive/
ls -la openpilot/cereal/
ls -la openpilot/opendbc/
ls -la openpilot/panda/

# 실행 중인 프로세스 확인 (실제 장치에서)
tmux attach
```

**학습 목표:**
- [ ] 각 디렉토리의 역할을 설명할 수 있다
- [ ] cereal 메시지가 무엇인지 안다
- [ ] 프로세스 간 데이터 흐름을 그릴 수 있다

### Week 2: 센서 및 인식

**camerad - 카메라 관리**
- [ ] `system/camerad/` 코드 읽기
- [ ] 카메라 초기화 과정 이해
- [ ] 이미지 캡처 및 전송 로직
- [ ] roadCameraState 메시지 구조

**modeld - 비전 모델**
- [ ] `selfdrive/modeld/` 코드 읽기
- [ ] supercombo 모델 입출력 이해
- [ ] 모델 실행 파이프라인
- [ ] modelV2 메시지 구조

**실습:**
```bash
# 메시지 모니터링
cereal log cat roadCameraState
cereal log cat modelV2

# 모델 관련 코드 읽기
cat selfdrive/modeld/runners/run.py
cat selfdrive/modeld/parse_model_outputs.py
```

**학습 목표:**
- [ ] 카메라에서 이미지가 어떻게 처리되는지 안다
- [ ] 딥러닝 모델이 무엇을 출력하는지 안다
- [ ] 차선 탐지가 어떻게 이루어지는지 이해한다

### Week 3: 경로 계획

**plannerd - 경로 계획**
- [ ] `selfdrive/controls/plannerd.py` 분석
- [ ] 횡방향 계획 (lateral planning)
- [ ] 종방향 계획 (longitudinal planning)
- [ ] ACC 로직 이해

**locationd - 위치 추정**
- [ ] `selfdrive/locationd/` 분석
- [ ] Kalman 필터 이해
- [ ] GPS + IMU 융합
- [ ] 위치 추정 정확도

**실습:**
```bash
# 경로 계획 메시지 확인
cereal log cat lateralPlan
cereal log cat longitudinalPlan

# 코드 분석
cat selfdrive/controls/plannerd.py
cat selfdrive/locationd/paramsd.py
```

**학습 목표:**
- [ ] 주행 경로가 어떻게 계획되는지 안다
- [ ] ACC가 어떻게 작동하는지 이해한다
- [ ] Kalman 필터의 역할을 안다

### Week 4: 제어 시스템

**controlsd - 차량 제어**
- [ ] `selfdrive/controls/controlsd.py` 심층 분석
- [ ] PID 컨트롤러 구현 읽기
- [ ] 조향 제어 로직
- [ ] 가감속 제어 로직

**제어 파라미터**
- [ ] 각 파라미터의 의미 이해
- [ ] 튜닝 원리 파악
- [ ] 안전 검사 메커니즘

**실습:**
```bash
# 제어 메시지 확인
cereal log cat carControl
cereal log cat carState

# 제어 코드 분석
cat selfdrive/controls/controlsd.py
cat selfdrive/controls/lib/latcontrol_pid.py
cat selfdrive/controls/lib/longcontrol.py
```

**학습 목표:**
- [ ] PID 컨트롤러가 어떻게 구현되어 있는지 안다
- [ ] 조향 제어의 흐름을 설명할 수 있다
- [ ] 안전 검사가 어디서 이루어지는지 안다

### Week 5: 차량 인터페이스

**panda - 하드웨어 인터페이스**
- [ ] `panda/` 저장소 탐색
- [ ] 안전 모델 코드 읽기 (C)
- [ ] CAN 메시지 송수신 로직
- [ ] 펌웨어 구조 이해

**opendbc - 차량 데이터베이스**
- [ ] `opendbc/` 구조 파악
- [ ] DBC 파일 형식 이해
- [ ] 차량별 CAN 메시지 차이
- [ ] 새 차량 추가 과정

**실습:**
```bash
# DBC 파일 읽기
cat opendbc/honda_civic_touring_2016_can_generated.dbc
cat opendbc/toyota_nodsu_pt_generated.dbc

# panda 안전 모델
cat panda/board/safety/safety_honda.h
cat panda/board/safety/safety_toyota.h
```

**학습 목표:**
- [ ] panda의 역할을 설명할 수 있다
- [ ] DBC 파일을 읽고 이해할 수 있다
- [ ] 안전 모델이 무엇을 검사하는지 안다

### Week 6: 통합 이해

**전체 흐름 추적**
- [ ] 단일 프레임이 처리되는 전 과정 추적
- [ ] 각 프로세스의 실행 주기 이해
- [ ] 지연 시간 (latency) 분석
- [ ] 병목 지점 파악

**디버깅 실습**
- [ ] 로그 분석 (`/data/log/`)
- [ ] Python 디버거 사용 (pdb)
- [ ] 메시지 덤프 분석
- [ ] 성능 프로파일링

**실습 프로젝트:**
- [ ] 간단한 파라미터 튜닝
- [ ] 새로운 로그 메시지 추가
- [ ] 기존 기능 수정
- [ ] 테스트 케이스 작성

### 체크리스트
- [ ] 주요 프로세스의 역할을 모두 설명할 수 있다
- [ ] 코드를 읽고 이해할 수 있다
- [ ] 간단한 수정을 직접 할 수 있다
- [ ] 디버깅 도구를 사용할 수 있다

---

## 🚀 Phase 4: 심화 학습 (4-8주)

### 목표
- 전문 영역 심층 학습
- 실제 기여 준비
- 고급 기능 이해

### Track A: 머신러닝 (4-6주)

**Week 1-2: 모델 이해**
- [ ] supercombo 모델 아키텍처 분석
- [ ] 입력 데이터 전처리 과정
- [ ] 출력 후처리 (post-processing)
- [ ] 모델 성능 평가 방법

**Week 3-4: 데이터 파이프라인**
- [ ] 학습 데이터 수집 방법
- [ ] 데이터 라벨링 과정
- [ ] 데이터 증강 (augmentation)
- [ ] 데이터셋 관리

**Week 5-6: 모델 학습**
- [ ] 학습 환경 구축
- [ ] 학습 스크립트 이해
- [ ] 하이퍼파라미터 튜닝
- [ ] 모델 평가 및 검증

**리소스:**
- openpilot 모델 학습 저장소
- PyTorch 공식 문서
- 논문: comma.ai의 관련 논문들

### Track B: 제어 시스템 (3-4주)

**Week 1-2: 고급 제어**
- [ ] MPC (Model Predictive Control) 심화
- [ ] 최적 제어 이론
- [ ] 차량 동역학 모델링
- [ ] 시뮬레이션 기반 튜닝

**Week 3-4: 실전 튜닝**
- [ ] 실제 차량에서 파라미터 튜닝
- [ ] A/B 테스트 방법론
- [ ] 성능 메트릭 분석
- [ ] 안전성 검증

**리소스:**
- 제어 이론 강의
- MATLAB/Simulink 튜토리얼
- openpilot 튜닝 가이드

### Track C: 차량 포팅 (4-6주)

**Week 1-2: 기초 준비**
- [ ] 차량 포팅 가이드 정독
- [ ] 필요한 장비 준비
- [ ] CAN 메시지 수집 방법
- [ ] cabana 도구 숙달

**Week 3-4: CAN 분석**
- [ ] 대상 차량의 CAN 메시지 수집
- [ ] 메시지 리버스 엔지니어링
- [ ] DBC 파일 작성
- [ ] 핑거프린팅 추가

**Week 5-6: 통합 및 테스트**
- [ ] 차량 인터페이스 구현
- [ ] 안전 모델 작성
- [ ] 실차 테스트
- [ ] PR 준비

**리소스:**
- [차량 포팅 가이드](car-porting/)
- cabana 튜토리얼
- Discord #car-porting 채널

### Track D: 시스템 아키텍처 (3-4주)

**Week 1-2: 시스템 프로그래밍**
- [ ] Linux 시스템 프로그래밍
- [ ] 프로세스 관리
- [ ] IPC (Inter-Process Communication)
- [ ] 실시간 시스템 개념

**Week 3-4: 성능 최적화**
- [ ] 프로파일링 도구 사용
- [ ] 병목 지점 최적화
- [ ] 메모리 관리
- [ ] 멀티스레딩 최적화

**리소스:**
- Linux Programming Interface (책)
- 시스템 프로그래밍 강의
- 성능 최적화 가이드

### 체크리스트
- [ ] 선택한 전문 영역에서 깊이 있는 이해를 갖췄다
- [ ] 실제 기여를 할 수 있는 수준이다
- [ ] 독립적으로 문제를 해결할 수 있다

---

## 💡 Phase 5: 실전 프로젝트 (진행 중)

### 목표
- 실제 기여 시작
- 포트폴리오 구축
- 커뮤니티 참여

### 프로젝트 아이디어

#### 초급 프로젝트

**1. 문서화**
- [ ] 한글 문서 추가 번역
- [ ] 코드 주석 개선
- [ ] 튜토리얼 작성
- [ ] FAQ 작성

**2. 버그 수정**
- [ ] GitHub Issues에서 "good first issue" 찾기
- [ ] 버그 재현 및 분석
- [ ] 수정 및 테스트
- [ ] PR 제출

**3. 도구 개선**
- [ ] 기존 도구 개선
- [ ] 새로운 분석 스크립트
- [ ] 시각화 도구
- [ ] 테스트 자동화

#### 중급 프로젝트

**1. 기능 개선**
- [ ] 기존 기능 향상
- [ ] 새로운 파라미터 추가
- [ ] UI/UX 개선
- [ ] 성능 최적화

**2. 새 차량 포팅**
- [ ] 미지원 차량 포팅
- [ ] CAN 데이터베이스 추가
- [ ] 안전 모델 구현
- [ ] 실차 테스트 및 검증

**3. 분석 도구**
- [ ] 주행 데이터 분석 도구
- [ ] 성능 비교 도구
- [ ] A/B 테스트 프레임워크
- [ ] 자동화된 검증 도구

#### 고급 프로젝트

**1. 모델 개선**
- [ ] 모델 아키텍처 개선
- [ ] 새로운 데이터셋 활용
- [ ] 특정 시나리오 성능 향상
- [ ] 경량화 (optimization)

**2. 새 기능 구현**
- [ ] 차선 변경 개선
- [ ] 고속도로 램프 처리
- [ ] 복잡한 교차로 대응
- [ ] 날씨 대응 개선

**3. 연구 프로젝트**
- [ ] 새로운 알고리즘 적용
- [ ] 논문 구현
- [ ] 벤치마킹
- [ ] 성능 평가 연구

### 기여 가이드라인

**PR 준비**
1. [ ] 이슈 확인 또는 생성
2. [ ] 브랜치 생성
3. [ ] 코드 작성
4. [ ] 테스트 작성/실행
5. [ ] 코드 리뷰 준비
6. [ ] PR 제출

**코드 품질**
- [ ] 스타일 가이드 준수
- [ ] 테스트 커버리지
- [ ] 문서화
- [ ] 성능 영향 고려

**커뮤니티 참여**
- [ ] Discord 활발히 참여
- [ ] 다른 사람 돕기
- [ ] 코드 리뷰 참여
- [ ] 발표/공유

### 체크리스트
- [ ] 최소 1개의 PR이 머지되었다
- [ ] 커뮤니티에서 활발히 활동한다
- [ ] 독립적인 프로젝트를 수행할 수 있다

---

## 📅 학습 일정 예시

### 풀타임 학습 (하루 6-8시간)
- **Phase 1**: 2주
- **Phase 2**: 1주
- **Phase 3**: 4주
- **Phase 4**: 4주
- **Phase 5**: 지속적
- **총 기간**: 약 3개월

### 파트타임 학습 (하루 2-3시간)
- **Phase 1**: 3주
- **Phase 2**: 2주
- **Phase 3**: 6주
- **Phase 4**: 6주
- **Phase 5**: 지속적
- **총 기간**: 약 4-5개월

### 주말 학습 (주 10-15시간)
- **Phase 1**: 4주
- **Phase 2**: 2주
- **Phase 3**: 8주
- **Phase 4**: 8주
- **Phase 5**: 지속적
- **총 기간**: 약 6개월

---

## 🎓 학습 팁

### 효과적인 학습 방법

**1. 실습 위주로 학습**
- 이론만 보지 말고 직접 코드 실행
- 작은 수정부터 시작
- 실패를 두려워하지 말기

**2. 체계적으로 기록**
- 학습 노트 작성
- 코드 주석 달기
- 어려운 부분 표시

**3. 커뮤니티 활용**
- 막히면 Discord에서 질문
- 다른 사람 질문에 답변
- 코드 리뷰 요청

**4. 꾸준히 학습**
- 매일 조금씩이라도 진행
- 학습 진도 체크
- 목표 설정

### 추천 도구

**개발 환경**
- VS Code / PyCharm
- Git / GitHub Desktop
- Terminal / tmux

**학습 도구**
- Notion / Obsidian (노트)
- Draw.io (다이어그램)
- Jupyter Notebook (실험)

**분석 도구**
- cabana (CAN 분석)
- replay (주행 재생)
- plotjuggler (데이터 시각화)

---

## 📚 추가 학습 자료

### 온라인 강의
- Coursera: Self-Driving Cars Specialization
- Udacity: Self-Driving Car Engineer Nanodegree
- MIT OpenCourseWare: Control Systems

### 책
- "Programming Computer Vision with Python"
- "Deep Learning" (Ian Goodfellow)
- "Probabilistic Robotics" (Sebastian Thrun)
- "Vehicle Dynamics and Control" (Rajesh Rajamani)

### 논문
- comma.ai 관련 논문들
- End-to-End Learning 관련 논문
- Vision-based Autonomous Driving

### YouTube 채널
- comma.ai 공식 채널
- George Hotz
- Two Minute Papers
- Lex Fridman (자율주행 인터뷰)

---

## 🎯 마일스톤

### 단기 목표 (1-3개월)
- [ ] openpilot 빌드 및 실행
- [ ] 코드 이해 및 간단한 수정
- [ ] 첫 PR 제출

### 중기 목표 (3-6개월)
- [ ] 전문 영역 선택 및 심화 학습
- [ ] 의미 있는 기여 (버그 수정, 기능 개선)
- [ ] 커뮤니티 활발 참여

### 장기 목표 (6-12개월)
- [ ] 독립적인 프로젝트 수행
- [ ] 새 차량 포팅 또는 새 기능 구현
- [ ] openpilot 전문가로 성장

---

## 💬 학습 중 도움받기

### 질문하기 전에
1. 문서 먼저 확인
2. GitHub Issues 검색
3. Discord 과거 대화 검색

### 좋은 질문 방법
- 구체적으로 질문
- 시도한 내용 공유
- 에러 메시지/로그 첨부
- 환경 정보 제공

### 도움 받을 수 있는 곳
- **Discord**: 실시간 질문/답변
- **GitHub Issues**: 버그 리포트, 기능 제안
- **GitHub Discussions**: 일반적인 토론
- **Reddit**: r/Comma_ai

---

<div align="center">

## 🚀 지금 바로 시작하세요!

**Phase 1, Day 1부터 시작하세요:**
1. [시작 가이드](getting-started/README.md) 읽기
2. YouTube에서 openpilot 영상 찾기
3. Discord 가입하기

**학습은 여정입니다. 즐기면서 배우세요! 🎓**

---

질문이나 피드백: [GitHub Issues](https://github.com/dinnerandcoffee/openpilot-learning-guide/issues)

</div>
