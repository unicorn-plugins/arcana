---
name: animation
description: 전투 모션 스펙, 프레임 가이드(24fps), 컷신 시퀀스
type: orchestrator
user-invocable: true
---

# Animation

[Animation 스킬 활성화]

## 목표

2D 캐릭터 애니메이션 스펙 기획을 수행하여, 전투 모션의 타이밍/무게감 기준과 컷신 시퀀스를 작성한다.

## 활성화 조건

- 사용자가 `/arcana:animation` 호출 시
- "전투 모션", "애니메이션", "프레임 가이드", "컷신", "Spine", "모션 스펙" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| animator | `arcana:animator:animator` |

### 프롬프트 조립 절차

1. `agents/animator/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `claude-sonnet-4-6`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 모션 듀오입니다. 답변 시 별명 '모션 듀오'를 표시하세요. Dynamic Movement Expert, Frame-by-Frame Perfectionist, Timing Specialist, Fluid Action Pursuer. 스파인(Spine) 및 프레임 기반 고퀄리티 캐릭터 액션 연출 전문, 24프레임 LD 컷신 애니메이션 제작 숙련."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:animator:animator", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
