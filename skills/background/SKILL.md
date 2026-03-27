---
name: background
description: 배경 컨셉 및 조명/분위기 가이드
type: orchestrator
user-invocable: true
---

# Background

[Background 스킬 활성화]

## 목표

4스테이지별 배경 컨셉 가이드와 Unity 2D Lighting/Tilemap/Parallax 기준을 수립한다.

## 활성화 조건

- 사용자가 `/arcana:background` 호출 시
- "배경", "환경 아트", "스테이지 배경", "조명/분위기", "배경 컨셉", "월드 아트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| background-artist | `arcana:background-artist:background-artist` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
ralph 모드로 수행  
1. 에이젼트 호출 -> Agent: background-artist