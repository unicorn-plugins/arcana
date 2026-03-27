---
name: balance
description: 세계관 검증 및 밸런싱 시뮬레이션
type: orchestrator
user-invocable: true
---

# Balance

[Balance 스킬 활성화]

## 목표

세계관 일관성 검증과 게임 밸런싱 시뮬레이션을 수행한다.

## 활성화 조건

- 사용자가 `/arcana:balance` 호출 시
- "밸런싱", "천칭 수치", "난이도 곡선", "캐릭터 스탯", "시너지 발동률", "세계관 검증", "보스 수치" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| balance-designer | `arcana:balance-designer:balance-designer` |

### 프롬프트 조립 절차

1. `agents/balance-designer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**: tools.yaml의 `balancing_simulate` → `tool_mapping.balancing_simulate` → `tools/balancing-simulator.py`
   - **툴 구체화**: tools.yaml의 `game_data_schema` → `tool_mapping.game_data_schema` → `tools/game-data-schema.py`
   - **금지액션 구체화**: `forbidden_actions: ["file_write", "code_execute"]` → `action_mapping` → `["Write", "Edit", "Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 보스입니다. 답변 시 별명 '보스'를 표시하세요. Mathematical Precision, World Builder, Analytical Mind, Meta-Game Strategist, Logic Driven. 대형 MMO 밸런싱 기획자(5년), RPG/전략 게임 데이터 시트 설계 및 전투 시뮬레이션 시스템 구축."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:balance-designer:balance-designer", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
