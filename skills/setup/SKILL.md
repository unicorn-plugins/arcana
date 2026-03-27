---
name: setup
description: arcana 플러그인 초기 설정 (MCP 서버 설치, 커스텀 도구 등록)
type: setup
command: /arcana:setup
user-invocable: true
---

# Setup

[Setup 스킬 활성화]

## 목표

`gateway/install.yaml`을 읽어 arcana 플러그인 실행에 필요한 MCP 서버와 커스텀 도구를 설치/등록한다. 최초 1회 실행으로 플러그인 전체 기능을 활성화한다.

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | `gateway/install.yaml`을 읽어 설치 항목 목록을 확인한다 |
| 2 | MCP 서버(`mcp_servers`)는 각 항목의 `config` 파일을 Claude Code 설정에 등록한다 |
| 3 | 커스텀 도구(`custom_tools`)는 `source` 경로의 파일 존재 여부를 확인한 후 등록한다 |
| 4 | `required: true` 항목 설치 실패 시 오류를 명시적으로 보고하고 중단한다 |
| 5 | `required: false` 항목 설치 실패 시 경고 메시지를 출력하고 계속 진행한다 |
| 6 | 설치 완료 후 설치 결과 요약(성공/실패/건너뜀)을 사용자에게 보고한다 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | `gateway/install.yaml` 미확인 상태에서 임의의 도구를 설치하는 것 |
| 2 | 이미 설치된 MCP 서버를 중복 등록하는 것 (기존 설정 덮어쓰기 금지) |
| 3 | `source` 파일이 존재하지 않는 커스텀 도구를 강제 등록하는 것 |
| 4 | 설치 결과 보고 없이 설치를 완료한 것으로 처리하는 것 |

## 검증 체크리스트

- [ ] `gateway/install.yaml` 파일을 성공적으로 읽었는가
- [ ] `mcp_servers` 목록의 모든 항목을 처리했는가
- [ ] `custom_tools` 목록의 모든 항목을 처리했는가
- [ ] `required: true` 항목이 모두 성공적으로 설치되었는가
- [ ] 설치 결과 요약이 사용자에게 보고되었는가

## 설치 워크플로우

### Phase 1: 설치 매니페스트 로드

1. `gateway/install.yaml` 파일을 읽는다
2. `mcp_servers` 목록과 `custom_tools` 목록을 파싱한다
3. 설치 항목 수를 사용자에게 미리 안내한다:
   ```
   [Setup] gateway/install.yaml 로드 완료
   - MCP 서버: {N}개
   - 커스텀 도구: {N}개
   설치를 시작합니다...
   ```

### Phase 2: MCP 서버 설치

`mcp_servers` 각 항목에 대해:
1. `config` 경로의 JSON 파일을 확인한다 (예: `gateway/mcp/context7.json`)
2. `scope: user`인 경우 Claude Code 사용자 설정에 등록한다
3. `scope: project`인 경우 프로젝트 설정에 등록한다
4. 등록 결과를 기록한다

**현재 설치 대상 MCP 서버:**

| 이름 | 설명 | 필수 여부 |
|------|------|---------|
| `context7` | 게임 엔진 및 라이브러리 공식 문서 검색 | 필수 |

### Phase 3: 커스텀 도구 등록

`custom_tools` 각 항목에 대해:
1. `source` 경로의 파일 존재 여부를 확인한다
2. 파일이 존재하면 도구로 등록한다
3. 파일이 없으면 `required` 값에 따라 오류/경고를 출력한다

**현재 설치 대상 커스텀 도구:**

| 이름 | 파일 경로 | 필수 여부 |
|------|----------|---------|
| `balancing-simulator` | `tools/balancing-simulator.py` | 필수 |
| `game-data-schema` | `tools/game-data-schema.py` | 필수 |
| `sound-asset-catalog` | `tools/sound-asset-catalog.py` | 선택 |
| `art-pipeline-guide` | `tools/art-pipeline-guide.py` | 선택 |
| `generate-image-bridge` | `tools/generate-image-bridge.py` | 선택 |
| `check-mermaid-bridge` | `tools/check-mermaid-bridge.py` | 선택 |

### Phase 4: 설치 결과 보고

설치 완료 후 다음 형식으로 결과를 보고한다:

```
[Setup] 설치 완료

MCP 서버:
  ✓ context7 - 설치 성공
  (또는) ✗ context7 - 설치 실패 (오류 내용)

커스텀 도구:
  ✓ balancing-simulator - 등록 성공
  ✓ game-data-schema - 등록 성공
  ~ sound-asset-catalog - 파일 없음 (선택 항목, 건너뜀)
  ...

결과 요약: 필수 {N}개 성공 / 선택 {N}개 성공 / {N}개 건너뜀
arcana 플러그인이 준비되었습니다. /arcana:help 로 사용법을 확인하세요.
```
