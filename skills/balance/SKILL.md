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

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: balance-designer