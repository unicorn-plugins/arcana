---
name: sound
description: 사운드 디렉팅 및 BGM/SFX 설계
type: orchestrator
user-invocable: true
---

# Sound

[Sound 스킬 활성화]

## 목표

아르카나 게임의 사운드 방향성을 수립하고 BGM/SFX 상세 설계 및 에셋 카탈로그를 산출한다.

## 활성화 조건

- 사용자가 `/arcana:sound` 호출 시
- "BGM", "SFX", "사운드", "음향", "효과음", "배경음악", "FMOD", "AudioMixer" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| sound-director | `arcana:sound-director:sound-director` |

### 프롬프트 조립 절차

1. `agents/sound-director/` 에서 3파일 로드:
   - `AGENT.md` (프롬프트 본문 — WHY + HOW)
   - `agentcard.yaml` (tier 확인 + persona 첨부)
   - `tools.yaml` (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**: tools.yaml의 `sound_catalog` → `tool_mapping.sound_catalog` → `tools/sound-asset-catalog.py` (`manage_catalog`)
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping.code_execute` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재하므로:
   "당신은 주디입니다. 답변 시 별명 '주디'를 표시하세요. Visionary Leader, Audio-Visual Specialist. 사운드 전문가 관점에서 게임의 감정적 몰입을 설계합니다. 메이저 게임사 사운드 팀장(6년), 배경음악/효과음 사운드 엔지니어링 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:sound-director:sound-director", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
