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

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: sound-director
