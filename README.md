# openpilot 학습 가이드 (한글)

<div align="center">

## openpilot을 한국어로 배우기

openpilot은 로보틱스를 위한 운영 체제입니다.  
현재 300개 이상의 지원 차량에서 운전자 보조 시스템을 업그레이드합니다.

</div>

---

## 📚 프로젝트 소개

이 저장소는 [comma.ai의 openpilot](https://github.com/commaai/openpilot)을 한국어로 학습하기 위한 가이드입니다.

원본 저장소: https://github.com/commaai/openpilot  
한글 가이드 저장소: https://github.com/dinnerandcoffee/openpilot

---

## 🎯 학습 목표

1. **openpilot 이해하기**: openpilot의 구조와 작동 원리 파악
2. **한글 문서화**: 주요 문서를 한글로 번역하여 학습 자료 제공
3. **실습 가이드**: openpilot 개발 환경 구축 및 실습 가이드 작성
4. **커뮤니티 기여**: 한국 개발자들의 openpilot 접근성 향상

---

## 📖 문서 구조

### 메인 문서
- [한글 README](./docs/ko/README.md) - openpilot 소개 및 시작 가이드
- [지원 차량 목록](./docs/ko/CARS.md) - 지원되는 차량 목록
- [기여 가이드](./docs/ko/CONTRIBUTING.md) - 개발에 참여하는 방법
- [안전성](./docs/ko/SAFETY.md) - 안전 모델 및 테스트

### 개념 및 이론
- [openpilot 개념](./docs/ko/concepts/) - 핵심 개념 설명
- [용어 사전](./docs/ko/GLOSSARY.md) - 주요 용어 정리

### 실습 가이드
- [시작하기](./docs/ko/getting-started/) - 초보자를 위한 가이드
- [개발 환경 구축](./docs/ko/how-to/setup-dev-environment.md) - 개발 환경 설정
- [차량 포팅](./docs/ko/car-porting/) - 새 차량 추가 가이드

---

## 🚀 빠른 시작

### 1. openpilot 사용하기 (차량에서)

차량에서 openpilot을 사용하려면 다음 4가지가 필요합니다:

1. **지원 장치**: comma 3X (구매: [comma.ai/shop](https://comma.ai/shop/comma-3x))
2. **소프트웨어**: 설치 URL `openpilot.comma.ai` 사용
3. **지원 차량**: [275개 이상의 지원 차량](./docs/ko/CARS.md) 중 하나
4. **차량 하네스**: comma 3X를 차량에 연결하기 위한 [하네스](https://comma.ai/shop/car-harness)

### 2. openpilot 개발 시작하기

```bash
# 저장소 클론
git clone https://github.com/dinnerandcoffee/openpilot.git
cd openpilot

# 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/commaai/openpilot.git

# 개발 환경 설정 (자세한 내용은 문서 참조)
```

---

## 🌿 브랜치 설명

| 브랜치 | URL | 설명 |
|--------|-----|------|
| `release3` | openpilot.comma.ai | 공식 릴리스 브랜치 |
| `release3-staging` | openpilot-test.comma.ai | 릴리스 준비 브랜치 (조기 접근 가능) |
| `nightly` | openpilot-nightly.comma.ai | 최신 개발 브랜치 (불안정할 수 있음) |
| `nightly-dev` | installer.comma.ai/commaai/nightly-dev | nightly + 실험적 기능 포함 |

---

## 🛠️ 주요 디렉토리 구조

```
openpilot/
├── openpilot/          # 핵심 파이썬 패키지
├── selfdrive/          # 자율주행 관련 코드
├── cereal/             # 메시지 정의 (Cap'n Proto)
├── opendbc/            # 차량 CAN 데이터베이스
├── panda/              # 차량 인터페이스 펌웨어
├── tools/              # 개발 및 디버깅 도구
├── docs/               # 문서
└── system/             # 시스템 레벨 코드
```

---

## 🤝 기여하기

이 프로젝트는 오픈소스이며 누구나 기여할 수 있습니다!

### 기여 방법
1. 이 저장소를 포크합니다
2. 새 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m '멋진 기능 추가'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

### 기여 아이디어
- 📝 문서 번역 및 개선
- 🐛 버그 리포트 및 수정
- 💡 새로운 학습 자료 추가
- 🔧 코드 예제 및 튜토리얼 작성

---

## 📚 학습 리소스

### 공식 리소스
- [공식 문서](https://docs.comma.ai)
- [로드맵](https://docs.comma.ai/contributing/roadmap/)
- [커뮤니티 Discord](https://discord.comma.ai)
- [comma.ai 블로그](https://blog.comma.ai)

### 한글 가이드 (이 저장소)
- **[📍 학습 로드맵](./docs/ko/ROADMAP.md)** ⭐ 여기서 시작하세요!
- [openpilot 시작하기](./docs/ko/getting-started/README.md)
- [핵심 개념 이해하기](./docs/ko/concepts/README.md)
- [개발 가이드](./docs/ko/how-to/README.md)
- [용어 사전](./docs/ko/GLOSSARY.md)

---

## ⚠️ 안전 및 법적 고지

**이것은 연구 목적의 알파 품질 소프트웨어입니다. 제품이 아닙니다.**

- openpilot은 [ISO26262](https://en.wikipedia.org/wiki/ISO_26262) 가이드라인을 준수합니다
- 사용자는 지역 법률 및 규정을 준수할 책임이 있습니다
- 명시적 또는 묵시적 보증이 없습니다
- 자세한 내용은 [안전성 문서](./docs/ko/SAFETY.md) 참조

---

## 📄 라이선스

openpilot은 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./openpilot/LICENSE) 파일을 참조하세요.

---

## 💬 커뮤니티

- **Discord**: [discord.comma.ai](https://discord.comma.ai)
- **Twitter/X**: [@comma_ai](https://x.com/comma_ai)
- **GitHub Issues**: [문제 보고 및 제안](https://github.com/dinnerandcoffee/openpilot/issues)

---

## 📝 번역 진행 상황

- [x] 메인 README
- [ ] CARS.md (차량 목록)
- [ ] CONTRIBUTING.md (기여 가이드)
- [ ] SAFETY.md (안전성)
- [ ] getting-started/ (시작 가이드)
- [ ] concepts/ (개념)
- [ ] how-to/ (실습 가이드)

---

<div align="center">

**openpilot으로 더 안전한 운전을 경험하세요! 🚗**

Made with ❤️ by the Korean openpilot community

</div>
