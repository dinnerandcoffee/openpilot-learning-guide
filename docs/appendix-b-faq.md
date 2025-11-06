# 부록 B: FAQ

자주 묻는 질문 모음

## 일반

**Q: openpilot은 완전 자율주행인가요?**
A: 아닙니다. Level 2 운전자 보조 시스템이며, 운전자의 지속적인 주의가 필요합니다.

**Q: 어떤 차량을 지원하나요?**
A: 250개 이상의 차량을 지원합니다. [comma.ai/vehicles](https://comma.ai/vehicles)에서 확인하세요.

**Q: 한국에서 사용 가능한가요?**
A: 기술적으로 가능하지만, 법적 규제를 확인해야 합니다.

## 개발

**Q: 빌드가 실패합니다.**
```bash
# 종속성 재설치
cd openpilot
./tools/ubuntu_setup.sh

# 클린 빌드
scons -c
scons -j$(nproc)
```

**Q: Python 버전 문제**
```bash
# pyenv로 3.11 설치
pyenv install 3.11.4
pyenv local 3.11.4
```

**Q: 모델이 로드되지 않습니다.**
```bash
# 모델 파일 확인
ls -lh models/supercombo.dlc

# 재다운로드
git lfs pull
```

## 하드웨어

**Q: comma three 없이 테스트 가능한가요?**
A: 네, replay를 사용하면 PC에서 테스트할 수 있습니다.

**Q: panda 대신 다른 CAN 인터페이스를 쓸 수 있나요?**
A: 가능하지만 panda의 안전 모델이 없으면 위험합니다.

## 차량 포팅

**Q: 지원되지 않는 차량을 추가하려면?**
A: [16장 차량 포팅 가이드](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/16-car-porting.md)를 참고하세요.

**Q: CAN 메시지를 어떻게 분석하나요?**
```bash
# cabana 사용
./tools/cabana/cabana "route_url"
```

## 모델 개발

**Q: 자체 AI 모델 학습이 가능한가요?**
A: 가능합니다. [11장 모델 학습](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/11-model-training.md)을 참고하세요.

**Q: 학습 데이터는 어디서 구하나요?**
A: comma.ai에서 공개 데이터셋을 제공합니다.

## 기여

**Q: 어떻게 기여할 수 있나요?**
A: [18장 컨트리뷰션 가이드](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/18-contributing.md)를 참고하세요.

**Q: PR이 merge되는 데 얼마나 걸리나요?**
A: 보통 1-2주이지만, 변경 사항의 크기에 따라 다릅니다.

---

[다음: 부록 C - 참고 자료 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/appendix-c-resources.md)
