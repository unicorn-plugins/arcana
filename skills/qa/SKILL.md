---
name: qa
description: 테스트 케이스 설계, 극단 케이스 검증, 버그 추적, QA 보고서
type: orchestrator
user-invocable: true
---

# QA

[QA 스킬 활성화]

## 목표

5대 테스트 영역의 테스트 케이스를 설계하고, 극단 케이스를 검증하여 QA 보고서를 산출한다.

## 활성화 조건

- 사용자가 `/arcana:qa` 호출 시
- "테스트", "QA", "버그", "극단 케이스", "밸런스 QA", "빌드 체크", "테스트 케이스 설계", "품질" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| qa-engineer | `arcana:qa-engineer:qa-engineer` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: qa-engineer