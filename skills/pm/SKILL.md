---
name: pm
description: 일정 관리, WBS, 스프린트 계획, 시스템 스펙 관리
type: orchestrator
user-invocable: true
---

# PM

[PM 스킬 활성화]

## 목표

아르카나 프로젝트의 일정 관리와 시스템 기획 상세화를 수행한다.

## 활성화 조건

- 사용자가 `/arcana:pm`, `/pm`, `/manager` 중 하나를 호출 시
- "일정", "마일스톤", "스프린트", "WBS", "리스크 레지스터", "시스템 스펙", "기획 문서" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| pm | `arcana:pm:pm` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: pm
