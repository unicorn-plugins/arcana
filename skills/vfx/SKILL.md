---
name: vfx
description: 스킬 이펙트 스펙, 파티클 가이드, 타격감 연출 설계
type: orchestrator
user-invocable: true
---

# VFX

[VFX 스킬 활성화]

## 목표

정방향/역방향 스킬 이펙트 스펙과 천칭 시각효과를 기획하고, 타격감 연출을 설계한다.

## 활성화 조건

- 사용자가 `/arcana:vfx` 호출 시
- "이펙트", "파티클", "VFX", "타격감", "히트스톱", "스킬 연출", "시너지 이펙트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| vfx-artist | `arcana:vfx-artist:vfx-artist` |

### 프롬프트 조립 절차

1. `agents/vfx-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: LOW` → `claude-haiku-4-5`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 니니입니다. 답변 시 별명 '니니'를 표시하세요. Impactful Visualizer, Particle Master, Technical Artist(VFX), Combat Feel Enhancer. 타격감 극대화를 위한 이펙트 파티클 및 스킬 연출 전문, 엔진 기반 특수효과 최적화 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:vfx-artist:vfx-artist", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
