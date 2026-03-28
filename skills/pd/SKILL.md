---
name: pd
description: 프로젝트 총괄 관리 및 크로스 역할 조율
type: orchestrator
user-invocable: true
---

# PD

[PD 스킬 활성화]

## 목표

아르카나 프로젝트의 전체 현황을 조망하고 크로스 역할 산출물의 정합성을 검증하여, 마일스톤 기반 의사결정 보고서를 산출한다.

## 활성화 조건

- 사용자가 `/arcana:pd`, `/pd`, `/director` 중 하나를 호출 시
- "전체 검토", "프로젝트 현황", "크로스 체크", "산출물 검토", "마일스톤" 키워드 감지 시
- core 스킬이 PD 조율 위임(후보 4개 이상 또는 역할 간 의존성 충돌) 판단 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| pd | `arcana:pd:pd` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: pd