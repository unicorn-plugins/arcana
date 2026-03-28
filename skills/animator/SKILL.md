---
name: animator
description: 전투 모션 스펙, 프레임 가이드(24fps), 컷신 시퀀스
type: orchestrator
user-invocable: true
---

# Animator

[Animator 스킬 활성화]

## 목표

2D 캐릭터 애니메이션 스펙 기획을 수행하여, 전투 모션의 타이밍/무게감 기준과 컷신 시퀀스를 작성한다.

## 활성화 조건

- 사용자가 `/arcana:animation`, `/animation`, `/animator` 중 하나를 호출 시
- "전투 모션", "애니메이션", "프레임 가이드", "컷신", "Spine", "모션 스펙" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| animator | `arcana:animator:animator` |


### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: animator
