# openpilot 완벽 가이드

<div align="center">

## 오픈소스 자율주행 시스템을 배우는 가장 쉬운 방법

**openpilot**은 comma.ai에서 개발한 오픈소스 운전자 보조 시스템입니다.  
이 책은 openpilot을 처음 접하는 한국 개발자들을 위한 완벽한 가이드입니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/dinnerandcoffee/openpilot-learning-guide?style=social)](https://github.com/dinnerandcoffee/openpilot-learning-guide)

[📖 온라인에서 읽기](https://wikidocs.net/book/openpilot) | [GitHub](https://github.com/dinnerandcoffee/openpilot-learning-guide) | [원본 저장소](https://github.com/commaai/openpilot)

</div>

---

## 📚 이 책에 대하여

openpilot은 300개 이상의 차량에서 작동하는 오픈소스 레벨2 자율주행 시스템입니다. 하지만 한국어 학습 자료가 부족하여 많은 개발자들이 어려움을 겪고 있습니다.

**이 책은:**
- ✅ 기초부터 고급까지 체계적으로 학습
- ✅ 실습 중심의 단계별 가이드
- ✅ 실제 코드 분석과 예제
- ✅ 한국 개발자를 위한 맞춤 설명

**대상 독자:**
- openpilot에 관심있는 개발자
- 자율주행 기술을 배우고 싶은 분
- Python과 기본적인 프로그래밍 지식이 있는 분

---

---

## 📖 목차

### Part 1: 시작하기 (완료 ✅)
1. [openpilot 소개](./docs/01-intro.md)
2. [openpilot이란 무엇인가](./docs/02-what-is-openpilot.md)

### Part 2: 개발 환경 구축 (완료 ✅)
3. [준비하기](./docs/03-prerequisites.md)
4. [개발 환경 설정](./docs/04-setup-environment.md)
5. [저장소 클론 및 빌드](./docs/05-clone-and-build.md)
6. [첫 실행과 테스트](./docs/06-first-run.md)

### Part 3: 핵심 개념 (완료 ✅)
7. [시스템 아키텍처](./docs/07-architecture.md)
8. [메시지 시스템 (cereal)](./docs/08-cereal.md)
9. [주요 프로세스 상세 분석](./docs/09-processes.md)

### Part 4: 비전 시스템 (완료 ✅)
10. [비전 시스템 개요](./docs/10-vision-overview.md)
11. [모델 학습 절차](./docs/11-model-training.md)
12. [모델 최적화](./docs/12-model-optimization.md)

### Part 5: 제어 시스템 (완료 ✅)
13. [횡방향 제어 (조향)](./docs/13-lateral-control.md)
14. [종방향 제어 (속도)](./docs/14-longitudinal-control.md)

### Part 6: 차량 인터페이스 (완료 ✅)
15. [CAN 버스 이해하기](./docs/15-can-bus.md)
16. [차량 포팅 가이드](./docs/16-car-porting.md)
17. [안전 모델과 모니터링](./docs/17-safety-monitoring.md)
18. [컨트리뷰션 가이드](./docs/18-contributing.md)

### Part 7: 실전 프로젝트 (완료 ✅)
19. [커스텀 모델 만들기](./docs/19-custom-model.md)
20. [시뮬레이터 개발](./docs/20-simulator.md)
21. [프로덕션 배포](./docs/21-deployment.md)

### 부록 (완료 ✅)
- [A. 용어집](./docs/appendix-a-glossary.md)
- [B. FAQ](./docs/appendix-b-faq.md)
- [C. 참고 자료](./docs/appendix-c-resources.md)
- [D. 문제 해결](./docs/appendix-d-troubleshooting.md)

---

## 🎯 학습 경로

### 초급 (1-2개월)
**목표**: openpilot 이해하고 개발 환경 구축

- Part 1: 시작하기 (1주)
- Part 2: 개발 환경 구축 (1주)
- Part 3: 핵심 개념 (2주)

### 중급 (2-3개월)
**목표**: 코드 분석과 이해

- Part 4: 비전 시스템 (2주)
- Part 5: 제어 시스템 (2주)
- Part 6: 차량 인터페이스 (2주)

### 고급 (진행 중)
**목표**: 실전 프로젝트와 기여

- Part 7: 실전 프로젝트
- 오픈소스 기여
- 전문 영역 개발

---

## � 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/dinnerandcoffee/openpilot-learning-guide.git
cd openpilot-learning-guide

# 2. 첫 챕터부터 읽기
cat docs/01-intro.md

# 3. openpilot 저장소 클론
git clone https://github.com/commaai/openpilot.git
```

---

## 💬 커뮤니티

- **Discord**: [comma.ai 공식 Discord](https://discord.comma.ai)
- **GitHub Issues**: [질문과 제안](https://github.com/dinnerandcoffee/openpilot-learning-guide/issues)
- **Discussions**: [토론 참여](https://github.com/dinnerandcoffee/openpilot-learning-guide/discussions)

---

## 🤝 기여하기

이 책은 오픈소스 프로젝트입니다. 기여를 환영합니다!

1. Fork 후 수정
2. Pull Request 제출
3. 오타, 개선사항, 추가 내용 모두 환영

---

## 📄 라이선스

- 이 가이드: MIT License
- openpilot: MIT License

---

## 🙏 감사의 말

- [comma.ai](https://comma.ai) - openpilot 개발
- openpilot 커뮤니티 - 지속적인 기여
- 모든 기여자분들

---

<div align="center">

**openpilot과 함께 자율주행의 세계로! 🚗💨**

Made with ❤️ for Korean developers

[시작하기](./docs/01-intro.md) →

</div>
