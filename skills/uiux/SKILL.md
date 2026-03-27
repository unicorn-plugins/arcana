---
name: uiux
description: HUD 설계, UX 플로우, 파티/증강 UI, 접근성, 튜토리얼 UX
type: orchestrator
user-invocable: true
---

# UIUX

[UIUX 스킬 활성화]

## 목표

게임의 전체 UX 플로우와 HUD/파티/증강/튜토리얼 UI를 설계한다.

## 활성화 조건

- 사용자가 `/arcana:uiux` 호출 시
- "UI", "HUD", "화면 배치", "UX 플로우", "와이어프레임", "인터페이스", "튜토리얼 UI" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| uiux-designer | `arcana:uiux-designer:uiux-designer` |

### 프롬프트 조립 절차

1. `agents/uiux-designer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**: tools.yaml의 `diagram_validate` → `tool_mapping.diagram_validate` → `tools/check-mermaid-bridge.py`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 밍키입니다. 답변 시 별명 '밍키'를 표시하세요. User-Centric Designer, Information Architect, Intuitive Interaction Maker, Interface Visualizer. 게임 편의성 향상을 위한 최적의 인터페이스 레이아웃 및 UX 플로우 설계, 모바일 UI 시스템 구축 4년."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:uiux-designer:uiux-designer", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
