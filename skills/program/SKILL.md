---
name: program
description: 게임 로직 구현, 데이터 구조 설계, ScriptableObject 에셋 관리
type: orchestrator
user-invocable: true
---

# Program

[Program 스킬 활성화]

## 목표

전투/천칭/카드/시너지/궁극기/증강 핵심 시스템을 구현하고, 데이터-로직 분리 구조를 확립한다.

## 활성화 조건

- 사용자가 `/arcana:program` 호출 시
- "코드", "구현", "로직", "데이터 구조", "JSON 로더", "FSM", "전투 시스템", "천칭 구현", "시너지 로직", "궁극기", "증강 구현" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| programmer | `arcana:programmer:programmer` |

### 프롬프트 조립 절차

1. `agents/programmer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**:
     - `doc_search` → `tool_mapping.doc_search` → context7 MCP (query-docs, resolve-library-id)
     - `game_data_schema` → `tool_mapping.game_data_schema` → `tools/game-data-schema.py`
   - **금지액션 구체화**: `forbidden_actions: []` → 제외 도구 없음
   - **최종 도구** = context7 MCP + game-data-schema.py (전체 허용)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 진입니다. 답변 시 별명 '진'를 표시하세요. Clean Coder, Logical Thinker, Debugging Expert, Collaborative Developer, Efficient Scripter. 게임 내 콘텐츠 기능 구현 및 안정적인 데이터 처리 로직 개발, 멀티 플랫폼 이식 지원 전문."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:programmer:programmer", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
