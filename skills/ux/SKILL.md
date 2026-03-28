---
name: ux
description: HUD 설계, UX 플로우, 파티/증강 UI, 접근성, 튜토리얼 UX
type: orchestrator
user-invocable: true
---

# UX

[UX 스킬 활성화]

## 목표

게임의 전체 UX 플로우와 HUD/파티/증강/튜토리얼 UI를 설계한다.

## 활성화 조건

- 사용자가 `/arcana:uiux`, `/uiux`, `/ui` 중 하나를 호출 시
- "UI", "HUD", "화면 배치", "UX 플로우", "와이어프레임", "인터페이스", "튜토리얼 UI" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| ux | `arcana:ux:ux` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: ux
