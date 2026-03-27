---
name: pd
description: 프로젝트 총괄 관리 및 크로스 역할 조율
type: orchestrator
user-invocable: true
---

# PD

[PD 스킬 활성화]

## 목표

아르카나 프로젝트의 전체 현황을 조망하고 크로스 역할 산출물의 정합성을 검증하여, 마일스톤 기반 의사결정 보고서를 산출한다.

## 활성화 조건

- 사용자가 `/arcana:pd` 호출 시
- "전체 검토", "프로젝트 현황", "크로스 체크", "산출물 검토", "마일스톤" 키워드 감지 시
- core 스킬이 PD 조율 위임(후보 4개 이상 또는 역할 간 의존성 충돌) 판단 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| pd | `arcana:pd:pd` |

### 프롬프트 조립 절차

1. `agents/pd/` 에서 3파일 로드:
   - `AGENT.md` (프롬프트 본문 — WHY + HOW)
   - `agentcard.yaml` (tier 확인 + persona 첨부)
   - `tools.yaml` (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**: tools.yaml의 `diagram_validate` → `tool_mapping.diagram_validate` → `tools/check-mermaid-bridge.py` (`validate_mermaid`)
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping.code_execute` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재하므로:
   "당신은 주디입니다. 답변 시 별명 '주디'를 표시하세요. Visionary Leader, Audio-Visual Specialist, Creative Director, Holistic Orchestrator, Detail Oriented. 메이저 게임사 사운드 팀장(6년), 다수의 인디 게임 총괄 디렉팅 및 배경음악/효과음 사운드 엔지니어링 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:pd:pd", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
