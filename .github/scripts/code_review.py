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

    return f"""시니어 개발자로서 코드 리뷰를 진행합니다. {lang} 작성하세요.

## 리뷰 원칙
- 이모지 사용 금지
- 감정적 표현, 칭찬, 격려 금지
- 문제가 있는 부분만 지적
- 문제가 없으면 해당 섹션 생략
- 팀 컨벤션 위반, 버그, 보안 취약점, 성능 이슈에 집중

## 응답 형식
반드시 아래 형식만 사용. 각 이슈/제안은 파일:라인을 굵게 표시하고, 코드 예시가 필요하면 코드 블록 사용:

## Code Review

### Summary
(이 PR이 무엇을 하는지 1-2줄로 간결하게 서술)

### Issues
(버그, 로직 오류, 보안 취약점, 컨벤션 위반 등. 없으면 섹션 생략)

**`파일명:라인번호`**
- 문제 설명
```typescript
// 수정 예시 코드 (필요한 경우만)
```

### Suggestions
(잠재적 문제, 개선 가능한 부분. 없으면 섹션 생략)

**`파일명:라인번호`**
- 제안 내용
```typescript
// 개선 예시 코드 (필요한 경우만)
```

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
