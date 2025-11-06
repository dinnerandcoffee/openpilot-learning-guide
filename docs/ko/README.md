# openpilot

<div align="center" style="text-align: center;">

<h1>openpilot</h1>

<p>
  <b>openpilot은 로보틱스를 위한 운영 체제입니다.</b>
  <br>
  현재 300개 이상의 지원 차량에서 운전자 보조 시스템을 업그레이드합니다.
</p>

<h3>
  <a href="https://docs.comma.ai">문서</a>
  <span> · </span>
  <a href="https://docs.comma.ai/contributing/roadmap/">로드맵</a>
  <span> · </span>
  <a href="https://github.com/commaai/openpilot/blob/master/docs/CONTRIBUTING.md">기여하기</a>
  <span> · </span>
  <a href="https://discord.comma.ai">커뮤니티</a>
  <span> · </span>
  <a href="https://comma.ai/shop">comma 3X에서 체험하기</a>
</h3>

빠른 시작: `bash <(curl -fsSL openpilot.comma.ai)`

[![openpilot tests](https://github.com/commaai/openpilot/actions/workflows/selfdrive_tests.yaml/badge.svg)](https://github.com/commaai/openpilot/actions/workflows/selfdrive_tests.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![X Follow](https://img.shields.io/twitter/follow/comma_ai)](https://x.com/comma_ai)
[![Discord](https://img.shields.io/discord/469524606043160576)](https://discord.comma.ai)

</div>

---

## 차량에서 openpilot 사용하기

차량에서 openpilot을 사용하려면 다음 네 가지가 필요합니다:

1. **지원 장치**: comma 3X ([comma.ai/shop](https://comma.ai/shop/comma-3x)에서 구매 가능)
2. **소프트웨어**: comma 3X 설정 절차에서 사용자 정의 소프트웨어 URL을 입력할 수 있습니다. 릴리스 버전을 설치하려면 `openpilot.comma.ai` URL을 사용하세요.
3. **지원 차량**: [275개 이상의 지원 차량](CARS.md) 중 하나가 있어야 합니다.
4. **차량 하네스**: comma 3X를 차량에 연결하기 위한 [차량 하네스](https://comma.ai/shop/car-harness)가 필요합니다.

하네스와 장치를 차량에 설치하는 방법에 대한 자세한 지침은 [comma.ai/setup](https://comma.ai/setup)에서 확인할 수 있습니다. [다른 하드웨어](https://blog.comma.ai/self-driving-car-for-free/)에서도 openpilot을 실행할 수 있지만, 플러그 앤 플레이는 아닙니다.

### 브랜치

| 브랜치 | URL | 설명 |
|--------|-----|------|
| `release3` | openpilot.comma.ai | openpilot의 릴리스 브랜치입니다. |
| `release3-staging` | openpilot-test.comma.ai | 릴리스를 위한 스테이징 브랜치입니다. 새로운 릴리스를 조금 더 일찍 받으려면 이것을 사용하세요. |
| `nightly` | openpilot-nightly.comma.ai | 최신 개발 브랜치입니다. 안정적이지 않을 수 있습니다. |
| `nightly-dev` | installer.comma.ai/commaai/nightly-dev | nightly와 동일하지만, 일부 차량에 대한 실험적 개발 기능이 포함되어 있습니다. |

---

## openpilot 개발 시작하기

openpilot은 [comma](https://comma.ai/)와 여러분 같은 사용자들에 의해 개발됩니다. [GitHub](http://github.com/commaai/openpilot)에서 Pull Request와 이슈를 환영합니다.

* [커뮤니티 Discord](https://discord.comma.ai)에 참여하세요
* [기여 문서](CONTRIBUTING.md)를 확인하세요
* [openpilot 도구](../../openpilot/tools/)를 확인하세요
* 코드 문서는 https://docs.comma.ai 에서 확인하세요
* openpilot 실행에 대한 정보는 [커뮤니티 위키](https://github.com/commaai/openpilot/wiki)에 있습니다

openpilot 작업으로 급여를 받고 싶으신가요? [comma는 채용 중](https://comma.ai/jobs#open-positions)이며 외부 기여자를 위한 많은 [바운티](https://comma.ai/bounties)를 제공합니다.

---

## 안전성 및 테스트

* openpilot은 [ISO26262](https://en.wikipedia.org/wiki/ISO_26262) 가이드라인을 준수합니다. 자세한 내용은 [SAFETY.md](SAFETY.md)를 참조하세요.
* openpilot은 모든 커밋마다 실행되는 소프트웨어 인 더 루프(software-in-the-loop) [테스트](https://github.com/commaai/openpilot/blob/master/.github/workflows/selfdrive_tests.yaml)를 갖추고 있습니다.
* 안전 모델을 적용하는 코드는 panda에 있으며 C로 작성되었습니다. 자세한 내용은 [코드 엄격성](https://github.com/commaai/panda#code-rigor)을 참조하세요.
* panda는 소프트웨어 인 더 루프 [안전 테스트](https://github.com/commaai/panda/tree/master/tests/safety)를 갖추고 있습니다.
* 내부적으로 다양한 프로세스를 빌드하고 단위 테스트하는 하드웨어 인 더 루프 Jenkins 테스트 스위트가 있습니다.
* panda는 추가적인 하드웨어 인 더 루프 [테스트](https://github.com/commaai/panda/blob/master/Jenkinsfile)를 갖추고 있습니다.
* 우리는 10개의 comma 장치가 지속적으로 경로를 재생하는 테스트 클로짓에서 최신 openpilot을 실행합니다.

---

## MIT 라이선스

openpilot은 MIT 라이선스 하에 배포됩니다. 소프트웨어의 일부는 명시된 대로 다른 라이선스 하에 배포됩니다.

이 소프트웨어의 모든 사용자는 Comma.ai, Inc. 및 그 이사, 임원, 직원, 대리인, 주주, 계열사, 하청업체 및 고객을 사용자의 이 소프트웨어 사용으로 인해 발생하거나 관련되거나 그로부터 발생하는 모든 주장, 청구, 소송, 소송, 요구, 손해, 책임, 의무, 손실, 합의, 판결, 비용 및 경비(변호사 비용 및 비용 포함)로부터 면책하고 무해하게 합니다.

**이것은 연구 목적을 위한 알파 품질 소프트웨어입니다. 이것은 제품이 아닙니다.
귀하는 현지 법률 및 규정을 준수할 책임이 있습니다.
명시적 또는 묵시적 보증이 없습니다.**

---

## 사용자 데이터 및 comma 계정

기본적으로 openpilot은 운전 데이터를 우리 서버에 업로드합니다. [comma connect](https://connect.comma.ai/)를 통해 데이터에 액세스할 수도 있습니다. 우리는 여러분의 데이터를 사용하여 더 나은 모델을 훈련하고 모두를 위해 openpilot을 개선합니다.

openpilot은 오픈 소스 소프트웨어입니다: 사용자는 원하는 경우 데이터 수집을 비활성화할 수 있습니다.

openpilot은 도로를 향한 카메라, CAN, GPS, IMU, 자력계, 열 센서, 충돌 및 운영 체제 로그를 기록합니다.
운전자를 향한 카메라와 마이크는 설정에서 명시적으로 동의한 경우에만 기록됩니다.

openpilot을 사용함으로써 귀하는 [우리의 개인정보 보호정책](https://comma.ai/privacy)에 동의합니다. 이 소프트웨어 또는 관련 서비스를 사용하면 특정 유형의 사용자 데이터가 생성되며, 이는 comma의 단독 재량에 따라 기록되고 저장될 수 있음을 이해합니다. 본 계약을 수락함으로써 귀하는 이 데이터의 사용에 대해 comma에 취소 불가능하고 영구적이며 전 세계적인 권리를 부여합니다.

---

<div align="center">

**원본 문서**: [openpilot README](https://github.com/commaai/openpilot/blob/master/README.md)

번역일: 2025년 11월 6일

</div>
