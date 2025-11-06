# openpilot 용어 사전

openpilot을 학습하면서 자주 접하게 되는 주요 용어들을 정리한 사전입니다.

---

## 🚗 차량 및 하드웨어

### comma 3X
- comma.ai에서 제작한 openpilot 실행을 위한 공식 하드웨어 장치
- 전면 및 운전자 감시 카메라, GPS, 프로세서 등이 내장됨
- 이전 모델: comma 2, comma 3

### Panda
- 차량의 CAN 버스와 comma 장치 간의 인터페이스 역할을 하는 하드웨어
- 안전 모델을 구현하여 차량 제어의 안전성을 보장
- USB를 통해 comma 장치와 연결

### Car Harness (차량 하네스)
- comma 장치를 차량에 연결하기 위한 케이블
- 차량 모델마다 다른 하네스가 필요함

### EON / comma two
- openpilot의 이전 세대 하드웨어 장치들

---

## 🧠 핵심 개념

### openpilot
- comma.ai에서 개발한 오픈소스 운전자 보조 시스템 (ADAS)
- Advanced Driver Assistance System의 레벨 2 자율주행 기능 제공
- 차선 유지(Lane Keep Assist), 적응형 크루즈 컨트롤(ACC) 등 제공

### ADAS (Advanced Driver Assistance System)
- 첨단 운전자 보조 시스템
- 센서와 카메라를 사용하여 운전자를 보조하는 시스템

### Lateral Control (횡방향 제어)
- 차량의 좌우 움직임을 제어 (스티어링 제어)
- 차선 중앙 유지를 담당

### Longitudinal Control (종방향 제어)
- 차량의 전후 움직임을 제어 (가속/감속)
- 앞차와의 거리 유지를 담당

---

## 📡 통신 및 데이터

### CAN Bus (Controller Area Network)
- 차량 내부 전자 제어 장치들이 통신하는 네트워크
- openpilot은 CAN 버스를 통해 차량 상태를 읽고 제어 명령을 보냄

### opendbc
- 다양한 차량의 CAN 메시지를 정의하는 데이터베이스
- DBC (Database CAN) 파일 형식 사용

### cereal
- openpilot의 메시징 시스템
- Cap'n Proto를 사용하여 프로세스 간 통신 구현

### Cap'n Proto
- 빠른 데이터 직렬화 프로토콜
- openpilot의 내부 메시지 전달에 사용

---

## 🎮 주행 모드

### Engaged
- openpilot이 활성화되어 차량을 제어하고 있는 상태
- 운전자는 여전히 주의를 기울여야 함

### Disengaged
- openpilot이 비활성화된 상태
- 운전자가 직접 차량을 제어

### Driver Monitoring
- 운전자 감시 시스템
- 운전자가 도로를 주시하고 있는지 확인
- 내부 카메라를 통해 운전자의 주의 집중 상태 모니터링

---

## 🔧 시스템 구성 요소

### selfdrive
- openpilot의 핵심 자율주행 로직이 포함된 디렉토리
- 제어, 인식, 계획 등의 모듈 포함

### controlsd
- 차량 제어를 담당하는 프로세스
- PID 컨트롤러를 사용하여 조향 및 가감속 제어

### plannerd
- 경로 계획을 담당하는 프로세스
- 차선 변경, 속도 계획 등을 수행

### modeld
- 딥러닝 모델을 실행하는 프로세스
- 카메라 이미지로부터 차선, 차량, 도로 상황 인식

### calibrationd
- 카메라 캘리브레이션을 담당하는 프로세스
- 카메라 장착 각도 등을 자동으로 보정

### locationd
- GPS 및 IMU 데이터를 융합하여 위치 추정
- Kalman 필터 사용

---

## 🤖 머신러닝 및 AI

### supercombo
- openpilot의 메인 비전 모델
- 차선, 경로, 다른 차량 등을 인식

### SNPE (Snapdragon Neural Processing Engine)
- Qualcomm의 신경망 가속 엔진
- comma 3X에서 딥러닝 모델 실행에 사용

### Training Data
- 사용자들이 업로드한 주행 데이터
- 모델 학습에 사용됨

---

## 🌐 서비스 및 플랫폼

### comma connect
- 사용자의 주행 데이터를 확인할 수 있는 웹 플랫폼
- 주행 영상, 경로, 통계 등을 확인 가능
- URL: https://connect.comma.ai

### comma prime
- comma.ai의 프리미엄 구독 서비스
- 무제한 데이터 저장, LTE 연결 등 제공

### cabana
- CAN 메시지 분석 도구
- 차량 포팅 작업 시 사용

---

## 🔒 안전 관련

### Safety Model
- panda에 구현된 안전 장치
- 비정상적인 제어 명령을 차단
- 차량별로 다른 안전 모델 적용

### Fingerprinting
- 차량 모델을 자동으로 식별하는 과정
- CAN 메시지 패턴을 분석하여 차량 종류 파악

### ISO26262
- 자동차 기능 안전 국제 표준
- openpilot은 이 표준의 가이드라인을 따름

---

## 📊 성능 지표

### Disengagement (해제)
- 시스템이 자동으로 비활성화되거나 운전자가 수동으로 개입하는 경우
- 중요한 안전 및 성능 지표

### MPC (Model Predictive Control)
- 모델 예측 제어
- 차량의 미래 동작을 예측하여 최적의 제어 입력 계산

### Lag (지연)
- 카메라 입력부터 제어 출력까지의 시간 지연
- 낮을수록 좋음 (일반적으로 100ms 이하 목표)

---

## 🛠️ 개발 도구

### scons
- openpilot 빌드 시스템
- Python 기반의 빌드 도구

### pytest
- Python 테스트 프레임워크
- openpilot의 단위 테스트에 사용

### replay
- 기록된 주행 데이터를 재생하는 도구
- 디버깅 및 개발에 유용

### ui (User Interface)
- comma 장치에 표시되는 화면
- Qt로 구현됨

---

## 🌿 개발 관련

### Fork (포크)
- 원본 저장소의 복사본을 자신의 계정에 생성
- 독립적으로 수정 가능

### Pull Request (PR)
- 자신이 수정한 코드를 원본 저장소에 병합 요청
- 코드 리뷰 과정을 거침

### CI (Continuous Integration)
- 지속적 통합
- 코드 변경 시 자동으로 테스트 실행

---

## 🚀 브랜치

### master / release3
- 안정적인 릴리스 버전
- 일반 사용자가 사용하기에 적합

### nightly
- 최신 개발 버전
- 불안정할 수 있음

### staging
- 릴리스 전 테스트 단계

---

## 📱 앱 및 인터페이스

### SSH
- comma 장치에 원격 접속하는 방법
- 고급 설정 및 디버깅에 사용

### tmux
- 터미널 멀티플렉서
- comma 장치에서 여러 프로세스 모니터링

---

## 기타 약어

- **ACC**: Adaptive Cruise Control (적응형 크루즈 컨트롤)
- **LKAS**: Lane Keeping Assist System (차선 유지 보조 시스템)
- **LTA**: Lane Tracing Assist (차선 추적 보조)
- **TSS**: Toyota Safety Sense (도요타 안전 시스템)
- **HSS**: Honda Sensing (혼다 센싱)
- **FW**: Firmware (펌웨어)
- **ECU**: Electronic Control Unit (전자 제어 장치)
- **OBD**: On-Board Diagnostics (차량 자체 진단)
- **IMU**: Inertial Measurement Unit (관성 측정 장치)
- **GPS**: Global Positioning System (위성 위치 확인 시스템)

---

## 📚 더 알아보기

- [openpilot 공식 문서](https://docs.comma.ai)
- [openpilot Wiki](https://github.com/commaai/openpilot/wiki)
- [comma.ai Discord](https://discord.comma.ai)

---

<div align="center">

**이 용어 사전은 계속 업데이트됩니다.**

용어 추가 제안이나 수정 사항은 Issue를 통해 알려주세요!

</div>
