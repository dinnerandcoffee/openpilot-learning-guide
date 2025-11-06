# 18. 컨트리뷰션 가이드

openpilot 오픈소스 프로젝트에 기여하는 방법입니다.

## 개발 워크플로우

```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/openpilot.git
cd openpilot
git remote add upstream https://github.com/commaai/openpilot.git

# 2. 브랜치 생성
git checkout -b feature/add-new-car

# 3. 개발
# ... 코드 작성 ...

# 4. 테스트
pytest selfdrive/car/toyota/tests/
pre-commit run --all-files

# 5. 커밋
git add .
git commit -m "Add support for Toyota Corolla 2024"

# 6. PR 생성
git push origin feature/add-new-car
```

## 코드 스타일

```python
# mypy 타입 체크
def get_car_params(candidate: str) -> CarParams:
    ret = CarParams()
    ret.carName = "toyota"
    return ret

# 린팅
# pre-commit이 자동으로 실행:
# - ruff (linter)
# - mypy (type checker)
# - cppcheck (C++ checker)
```

## 차량 포팅 PR

```markdown
### 2024 Toyota Corolla Support

**Changes**:
- Added fingerprint for Corolla 2024
- Implemented CarInterface/Controller/State
- Tested 500+ miles

**Testing**:
- ✅ Lane keeping works
- ✅ ACC functional
- ✅ Safety checks pass

**Video**: https://youtu.be/...
```

## 리뷰 과정

1. CI 통과 대기 (자동 테스트)
2. comma팀 리뷰
3. 수정 요청 반영
4. Merge!

---

[다음: 19. 커스텀 모델 만들기 →](https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs/19-custom-model.md)
