---
name: background
description: 배경 컨셉 및 조명/분위기 가이드
type: orchestrator
user-invocable: true
---

# Background

[Background 스킬 활성화]

## 목표

4스테이지별 배경 컨셉 가이드와 Unity 2D Lighting/Tilemap/Parallax 기준을 수립한다.

## 활성화 조건

- 사용자가 `/arcana:background` 호출 시
- "배경", "환경 아트", "스테이지 배경", "조명/분위기", "배경 컨셉", "월드 아트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| background-artist | `arcana:background-artist:background-artist` |

### 프롬프트 조립 절차

1. `agents/background-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: LOW` → `tier_mapping.default.LOW` → 해당 모델
   - **툴 구체화**: tools.yaml의 `generate_image` → `tool_mapping.generate_image` → MCP 서버
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 령입니다. 답변 시 별명 '령'를 표시하세요. Immersive World Creator, Environment Specialist, Lighting Master. 게임 내 몰입감을 극대화하는 랜드마크 및 필드 오브젝트 그래픽 제작 5년, 배경 컨셉 아트 전문."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:background-artist:background-artist", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
