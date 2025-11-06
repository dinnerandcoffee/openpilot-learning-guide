#!/usr/bin/env python3
"""
모든 .md 파일의 상대 경로 링크를 GitHub 절대 경로로 변환
"""

import re
from pathlib import Path

# GitHub 저장소 기본 URL
BASE_URL = "https://github.com/dinnerandcoffee/openpilot-learning-guide/blob/main/docs"

# 파일명 → URL 매핑
FILE_MAP = {
    "01-intro.md": f"{BASE_URL}/01-intro.md",
    "02-what-is-openpilot.md": f"{BASE_URL}/02-what-is-openpilot.md",
    "03-prerequisites.md": f"{BASE_URL}/03-prerequisites.md",
    "04-setup-environment.md": f"{BASE_URL}/04-setup-environment.md",
    "05-clone-and-build.md": f"{BASE_URL}/05-clone-and-build.md",
    "06-first-run.md": f"{BASE_URL}/06-first-run.md",
    "07-architecture.md": f"{BASE_URL}/07-architecture.md",
    "08-cereal.md": f"{BASE_URL}/08-cereal.md",
    "09-processes.md": f"{BASE_URL}/09-processes.md",
    "10-vision-overview.md": f"{BASE_URL}/10-vision-overview.md",
    "11-model-training.md": f"{BASE_URL}/11-model-training.md",
    "12-model-optimization.md": f"{BASE_URL}/12-model-optimization.md",
    "13-lateral-control.md": f"{BASE_URL}/13-lateral-control.md",
    "14-longitudinal-control.md": f"{BASE_URL}/14-longitudinal-control.md",
    "15-can-bus.md": f"{BASE_URL}/15-can-bus.md",
    "16-car-porting.md": f"{BASE_URL}/16-car-porting.md",
    "17-safety-monitoring.md": f"{BASE_URL}/17-safety-monitoring.md",
    "18-contributing.md": f"{BASE_URL}/18-contributing.md",
    "19-custom-model.md": f"{BASE_URL}/19-custom-model.md",
    "20-simulator.md": f"{BASE_URL}/20-simulator.md",
    "21-deployment.md": f"{BASE_URL}/21-deployment.md",
    "appendix-a-glossary.md": f"{BASE_URL}/appendix-a-glossary.md",
    "appendix-b-faq.md": f"{BASE_URL}/appendix-b-faq.md",
    "appendix-c-resources.md": f"{BASE_URL}/appendix-c-resources.md",
    "appendix-d-troubleshooting.md": f"{BASE_URL}/appendix-d-troubleshooting.md",
}

def fix_links_in_file(filepath):
    """파일 내의 모든 상대 경로 링크를 절대 경로로 변환"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # ./파일명.md 패턴 찾기
    pattern = r'\]\(\./([\w-]+\.md)\)'
    
    def replace_link(match):
        filename = match.group(1)
        if filename in FILE_MAP:
            return f']({FILE_MAP[filename]})'
        else:
            # 매핑에 없는 파일은 그대로 유지
            return match.group(0)
    
    content = re.sub(pattern, replace_link, content)
    
    # 변경사항이 있을 때만 저장
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filepath}")
        return True
    else:
        print(f"  {filepath} (no changes)")
        return False

def main():
    docs_dir = Path("docs")
    changed_count = 0
    
    for md_file in sorted(docs_dir.glob("*.md")):
        if fix_links_in_file(md_file):
            changed_count += 1
    
    print(f"\n총 {changed_count}개 파일 수정됨")

if __name__ == "__main__":
    main()
