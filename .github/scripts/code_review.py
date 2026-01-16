#!/usr/bin/env python3
"""
AI Code Review Bot using Claude API
"""

import os
import json
import yaml
import anthropic
from github import Github
from pathlib import Path


def load_config() -> dict:
    """리뷰 설정 파일 로드"""
    config_path = Path(".review-config.yaml")
    default_config = {
        "language": "ko",
        "review_style": "friendly",
        "focus_areas": ["logic", "security", "performance", "naming", "duplication"],
        "ignore_patterns": ["*.lock", "*.min.js", "*.min.css", "package-lock.json"],
        "max_files": 20,
        "custom_instructions": ""
    }

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            return {**default_config, **user_config}

    return default_config


def read_diff() -> str:
    """PR diff 파일 읽기"""
    diff_path = Path("pr_diff.txt")
    if diff_path.exists():
        content = diff_path.read_text(encoding="utf-8")
        # diff가 너무 크면 잘라내기 (토큰 제한 고려)
        if len(content) > 50000:
            content = content[:50000] + "\n\n... (diff truncated due to size)"
        return content
    return ""


def get_pr_info(github_token: str, repo_name: str, pr_number: int) -> dict:
    """PR 정보 가져오기"""
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    return {
        "title": pr.title,
        "body": pr.body or "",
        "author": pr.user.login,
        "files_changed": [f.filename for f in pr.get_files()],
        "additions": pr.additions,
        "deletions": pr.deletions
    }


def build_system_prompt(config: dict) -> str:
    """시스템 프롬프트 생성"""
    lang = "한국어로" if config.get("language") == "ko" else "in English"

    return f"""당신은 시니어 개발자 수준의 코드 리뷰어입니다. {lang} 리뷰해주세요.

## 리뷰 원칙
- 건설적인 피드백 제공 (문제점과 개선 방안 중심)
- 구체적인 파일명:라인번호 형식으로 위치 명시
- 로직/보안/성능 이슈에 집중
- 칭찬이나 잘한 점은 언급하지 않음

## 응답 형식 (마크다운)
반드시 아래 형식을 따라주세요:

## 🤖 AI 코드 리뷰

### 📝 PR 요약
(변경사항 2-3줄 요약)

### 📋 이슈 요구사항 체크
(연결된 이슈가 있으면 요구사항 충족 여부 체크)
- ✅ 완료된 요구사항
- ⚠️ 미완료 또는 부분 구현
- ❌ 누락된 요구사항

### 🔍 코드 로직
(버그 가능성, 에러 처리, 엣지케이스 등)
**`파일명:라인번호`**
- 구체적인 문제점과 수정 제안

### 💡 개선 제안
(성능, 구조, 네이밍 등 개선할 수 있는 부분)

---
🤖 이 리뷰는 AI가 생성했습니다.

{config.get('custom_instructions', '')}
"""


def build_user_prompt(pr_info: dict, diff: str, issue_content: str) -> str:
    """유저 프롬프트 생성"""
    prompt = f"""## PR 정보
- 제목: {pr_info['title']}
- 작성자: {pr_info['author']}
- 변경 파일: {', '.join(pr_info['files_changed'][:10])}
- 추가/삭제: +{pr_info['additions']} / -{pr_info['deletions']}

## PR 설명
{pr_info['body']}

"""

    if issue_content:
        prompt += f"""## 연결된 이슈
{issue_content}

"""

    prompt += f"""## 코드 변경사항 (diff)
```diff
{diff}
```

위 PR에 대해 코드 리뷰를 진행해주세요.
"""

    return prompt


def run_review(config: dict, pr_info: dict, diff: str, issue_content: str) -> str:
    """Claude API로 코드 리뷰 실행"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    system_prompt = build_system_prompt(config)
    user_prompt = build_user_prompt(pr_info, diff, issue_content)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content[0].text


def main():
    # 환경변수 로드
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("REPO_NAME")
    pr_number = int(os.environ.get("PR_NUMBER", 0))
    issue_content = os.environ.get("ISSUE_CONTENT", "")

    if not all([github_token, repo_name, pr_number]):
        print("필수 환경변수가 설정되지 않았습니다.")
        return

    # 설정 로드
    config = load_config()

    # PR 정보 가져오기
    pr_info = get_pr_info(github_token, repo_name, pr_number)

    # diff 읽기
    diff = read_diff()

    if not diff:
        print("diff가 비어있습니다.")
        return

    # 코드 리뷰 실행
    print("🔍 AI 코드 리뷰 시작...")
    review_result = run_review(config, pr_info, diff, issue_content)

    # 결과 저장
    with open("review_result.md", "w", encoding="utf-8") as f:
        f.write(review_result)

    print("✅ 코드 리뷰 완료!")


if __name__ == "__main__":
    main()
