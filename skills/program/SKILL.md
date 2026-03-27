---
name: program
description: 게임 로직 구현, 데이터 구조 설계, ScriptableObject 에셋 관리
type: orchestrator
user-invocable: true
---

# Program

[Program 스킬 활성화]

## 목표

전투/천칭/카드/시너지/궁극기/증강 핵심 시스템을 구현하고, 데이터-로직 분리 구조를 확립한다.

## 활성화 조건

- 사용자가 `/arcana:program` 호출 시
- "코드", "구현", "로직", "데이터 구조", "JSON 로더", "FSM", "전투 시스템", "천칭 구현", "시너지 로직", "궁극기", "증강 구현" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| programmer | `arcana:programmer:programmer` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: programmer