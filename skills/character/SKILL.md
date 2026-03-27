---
name: character
description: 캐릭터 디자인 및 카드 일러스트 검증
type: orchestrator
user-invocable: true
---

# Character

[Character 스킬 활성화]

## 목표

플레이어블 캐릭터(7종) 및 보스(5종)의 디자인 시트와 정/역방향 포즈 가이드를 작성하고, 카드 일러스트 레이아웃을 검증한다.

## 활성화 조건

- 사용자가 `/arcana:character` 호출 시
- "캐릭터 디자인", "캐릭터 원화", "포즈 가이드", "카드 일러스트", "캐릭터 시트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| character-artist | `arcana:character-artist:character-artist` |

### 프롬프트 조립 절차

1. `agents/character-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → 해당 모델
   - **툴 구체화**: tools.yaml의 `generate_image` → `tool_mapping.generate_image` → MCP 서버
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 아트 트리오입니다. 답변 시 별명 '아트 트리오'를 표시하세요. Creative Character Designer, Anatomy Expert, Style Adaptive. 유명 모바일 게임 캐릭터 원화 및 코스튬 디자인, 매력적인 캐릭터 IP 창출 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:character-artist:character-artist", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
