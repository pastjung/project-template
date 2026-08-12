---
branch: git/attributes
description: 줄 끝 정규화와 binary 파일 지정 (.gitattributes)
provides:
  - .gitattributes
  - docs/git-attributes.md
requires: []
works-with:
  - branch: settings/editor-config
    reason: 에디터 저장 시점과 Git 커밋 시점의 줄 끝 정책을 함께 통일
  - branch: backend/spring-boot
    reason: gradlew LF 규칙이 Windows 체크아웃의 컨테이너 빌드를 보호
conflicts: []
placeholders: []
secrets: []
after-import:
  - 기존 파일이 있는 저장소라면 git add --renormalize . 실행 검토
verify:
  - git check-attr text -- README.md
---

# Git Attributes Guide

이 문서는 프로젝트에서 공통으로 사용할 Git attributes 설정과 운영 기준을 정의합니다.

## Purpose

`.gitattributes`는 Git이 파일을 저장소에 넣거나 작업 디렉터리로 꺼낼 때 파일을 어떻게 처리할지 정하는 설정 파일입니다.

주요 목적은 다음과 같습니다.

- 운영체제별 줄 끝 차이로 생기는 불필요한 diff를 줄입니다.
- 저장소 안의 텍스트 파일을 LF 기준으로 관리합니다.
- Windows 전용 command script는 CRLF를 유지합니다.
- 이미지, 압축 파일, 문서 파일 같은 binary 파일을 텍스트로 diff하지 않게 합니다.

## EditorConfig vs Git Attributes

`.editorconfig`와 `.gitattributes`는 서로 다른 역할을 합니다.

| File | Role |
| --- | --- |
| `.editorconfig` | 에디터나 IDE가 파일을 저장할 때 포맷을 맞춥니다. |
| `.gitattributes` | Git이 파일을 commit, checkout, diff할 때 처리 방식을 맞춥니다. |

Windows, macOS, Linux 사용자가 함께 작업한다면 두 파일을 같이 사용하는 것을 권장합니다.

## Text Normalization

기본 설정은 모든 텍스트 파일을 LF 줄 끝 기준으로 정규화합니다.

```gitattributes
* text=auto eol=lf
```

각 항목의 의미는 다음과 같습니다.

| Attribute | Description |
| --- | --- |
| `text=auto` | Git이 텍스트 파일과 binary 파일을 자동으로 판별합니다. |
| `eol=lf` | 텍스트 파일을 작업 디렉터리와 저장소에서 LF 줄 끝으로 맞춥니다. |

이 설정을 두면 Windows 사용자가 작업하더라도 저장소에 들어가는 텍스트 파일의 줄 끝을 LF 기준으로 유지할 수 있습니다.

## Windows Command Scripts

Windows command script는 실행 환경 호환성을 위해 CRLF 줄 끝을 유지합니다.

```gitattributes
*.bat text eol=crlf
*.cmd text eol=crlf
```

PowerShell script(`*.ps1`)는 기본 텍스트 규칙(LF)을 따릅니다. PowerShell 5.1과
7 모두 LF 스크립트를 정상 실행하며, LF를 유지해야 Linux 컨테이너나 CI에서도
같은 파일을 문제없이 사용할 수 있습니다. 단, Authenticode 서명된 스크립트는
줄 끝이 바뀌면 서명이 깨지므로, 서명 스크립트를 쓰는 프로젝트는
`*.ps1 text eol=crlf`로 바꾸고 Windows 전용으로 관리합니다.

Gradle wrapper 스크립트(`gradlew`)는 확장자가 없어 명시적으로 LF를 지정합니다.
Windows에서 checkout한 저장소를 Linux 컨테이너로 빌드할 때 CRLF면 실행이
깨지기 때문입니다.

```gitattributes
gradlew text eol=lf
```

## Binary Files

이미지, 압축 파일, Java archive, Office 문서, Figma 파일은 binary로 처리합니다.

```gitattributes
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.webp binary
*.pdf binary
*.zip binary
*.gz binary
*.tar binary
*.jar binary
*.war binary
*.7z binary
*.doc binary
*.docx binary
*.ppt binary
*.pptx binary
*.xls binary
*.xlsx binary
*.fig binary
```

폰트와 미디어 파일도 binary로 처리합니다.

```gitattributes
*.woff binary
*.woff2 binary
*.ttf binary
*.otf binary
*.eot binary
*.mp3 binary
*.mp4 binary
*.webm binary
*.mov binary
```

binary로 지정한 파일은 Git이 줄 끝 변환을 하지 않고, 일반 텍스트 diff 대상으로도 취급하지 않습니다.

## Renormalization

이미 프로젝트에 파일이 들어간 뒤 `.gitattributes`를 추가했다면 한 번 정규화 커밋이 필요할 수 있습니다.

```bash
git add --renormalize .
git status
git commit -m "chore: normalize line endings"
```

새 프로젝트를 시작할 때 이 브랜치를 먼저 적용하면 별도의 정규화 커밋 없이 시작할 수 있습니다.

## Usage Rules

- 이 설정은 `settings/editor-config`와 함께 적용하는 것을 권장합니다.
- 텍스트 파일은 기본적으로 LF를 사용합니다.
- Windows에서 직접 실행해야 하는 `.bat`, `.cmd` 파일만 CRLF 예외를 둡니다.
- 프로젝트에서 특별한 binary 포맷을 사용한다면 해당 확장자를 추가합니다.
- 줄 끝 변경만 발생한 대량 diff가 생기면 `.gitattributes` 적용 여부를 먼저 확인합니다.

## Recommended Import

이 설정은 `settings/editor-config` 다음에 적용하는 것을 권장합니다.

```bash
git merge --squash origin/git/attributes
git commit -m "init: add git attributes"
```

## Standalone Usage

이 브랜치만 가져와도 커밋 시점의 줄 끝 정규화와 binary 처리가 즉시 적용됩니다.
기존 파일이 있는 저장소에서는 Renormalization 절의 절차를 따릅니다.

## Works With

`settings/editor-config`와 함께 사용하면 에디터 저장 시점의 정책까지
통일됩니다. `backend/spring-boot`처럼 Gradle wrapper를 쓰는 브랜치와 함께
사용하면 `gradlew` LF 규칙이 크로스 플랫폼 빌드를 보호합니다.
