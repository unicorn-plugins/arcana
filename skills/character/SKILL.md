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

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용 
1. 에이젼트 호출 -> Agent: character-artist