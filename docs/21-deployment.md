# 21. 프로덕션 배포

개발한 openpilot을 실제 차량에 배포하는 방법입니다.

## OTA 업데이트

```python
# release/update.py

def create_ota_package():
    """OTA 패키지 생성"""
    files = [
        'selfdrive/',
        'models/supercombo.dlc',
        'launch_openpilot.sh'
    ]
    
    # 압축
    with tarfile.open('ota_v0.9.8.tar.gz', 'w:gz') as tar:
        for f in files:
            tar.add(f)
    
    # 서명
    sign_package('ota_v0.9.8.tar.gz')

def apply_update(package_path):
    """업데이트 적용"""
    # 백업
    backup_current_version()
    
    # 압축 해제
    extract(package_path, '/data/openpilot')
    
    # 재시작
    os.system('sudo reboot')
```

## A/B 업데이트

```python
def ab_update():
    """A/B 파티션 업데이트"""
    current = get_current_slot()  # 'a' or 'b'
    target = 'b' if current == 'a' else 'a'
    
    # target 슬롯에 업데이트
    install_to_slot(target)
    
    # 부팅 슬롯 변경
    set_boot_slot(target)
```

## CI/CD 파이프라인

```yaml
# .github/workflows/release.yml

name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build
        run: scons -j$(nproc)
      
      - name: Test
        run: pytest selfdrive/test
      
      - name: Package
        run: python release/create_ota.py
      
      - name: Upload
        run: aws s3 cp ota_package.tar.gz s3://comma-releases/
```

## 모니터링

```python
# 텔레메트리
def send_telemetry():
    data = {
        'version': VERSION,
        'uptime': get_uptime(),
        'errors': get_error_count(),
        'distance': get_distance_driven()
    }
    
    requests.post('https://api.comma.ai/telemetry', json=data)
```

## 마무리

축하합니다! openpilot 학습 가이드를 완료했습니다.

**다음 단계**:
- 실제 프로젝트 시작
- comma Discord 커뮤니티 참여
- 오픈소스 기여

**부록**:
- [부록 A: 용어집](./appendix-a-glossary.md)
- [부록 B: FAQ](./appendix-b-faq.md)
- [부록 C: 참고 자료](./appendix-c-resources.md)
- [부록 D: 문제 해결](./appendix-d-troubleshooting.md)

Happy driving! 🚗
