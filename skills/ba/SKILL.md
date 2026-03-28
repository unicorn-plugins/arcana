---
name: ba
description: 배경 컨셉 및 조명/분위기 가이드
type: orchestrator
user-invocable: true
---

# BA

[BA 스킬 활성화]

## 목표

4스테이지별 배경 컨셉 가이드와 Unity 2D Lighting/Tilemap/Parallax 기준을 수립한다.

## 활성화 조건

- 사용자가 `/arcana:background`, `/background`, `/bg` 중 하나를 호출 시
- "배경", "환경 아트", "스테이지 배경", "조명/분위기", "배경 컨셉", "월드 아트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| ba | `arcana:ba:ba` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: ba