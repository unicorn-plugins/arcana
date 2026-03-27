---
name: ad
description: 비주얼 컨셉 및 아트 스타일 관리
type: orchestrator
user-invocable: true
---

# AD

[AD 스킬 활성화]

## 목표

아르카나 게임의 비주얼 아이덴티티를 확립하고, 카드 레이아웃 표준을 수립하며, 아트 산출물 품질을 최종 검수한다.

## 활성화 조건

- 사용자가 `/arcana:ad` 호출 시
- "아트 스타일", "비주얼 가이드", "비주얼 아이덴티티", "카드 프레임", "카드 레이아웃", "아트 기획" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| art-director | `arcana:art-director:art-director` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우  
완료 보장이 필요하면 `/oh-my-claudecode:ralph`와 함께 사용
1. 에이젼트 호출 -> Agent: art-director
