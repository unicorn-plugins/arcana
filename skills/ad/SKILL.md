---
name: ad
description: 비주얼 컨셉 및 아트 스타일 관리
type: orchestrator
user-invocable: true
---

# AD

[AD 스킬 활성화]

## 목표

아르카나 게임의 비주얼 아이덴티티를 확립하고, 카드 레이아웃 표준을 수립하며, 아트 산출물 품질을 최종 검수한다.

## 활성화 조건

- 사용자가 `/arcana:ad` 호출 시
- "아트 스타일", "비주얼 가이드", "비주얼 아이덴티티", "카드 프레임", "카드 레이아웃", "아트 기획" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| art-director | `arcana:art-director:art-director` |

### 프롬프트 조립 절차

1. `agents/art-director/` 에서 3파일 로드:
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
   "당신은 송이입니다. 답변 시 별명 '송이'를 표시하세요. Aesthetic Trendsetter, Quality Guard, Visual Storyteller. 프로젝트 전체 비주얼 가이드 수립 및 원화/그래픽 품질 최종 검수 10년."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:art-director:art-director", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
