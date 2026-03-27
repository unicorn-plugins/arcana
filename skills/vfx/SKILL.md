---
name: vfx
description: 스킬 이펙트 스펙, 파티클 가이드, 타격감 연출 설계
type: orchestrator
user-invocable: true
---

# VFX

[VFX 스킬 활성화]

## 목표

정방향/역방향 스킬 이펙트 스펙과 천칭 시각효과를 기획하고, 타격감 연출을 설계한다.

## 활성화 조건

- 사용자가 `/arcana:vfx` 호출 시
- "이펙트", "파티클", "VFX", "타격감", "히트스톱", "스킬 연출", "시너지 이펙트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| vfx-artist | `arcana:vfx-artist:vfx-artist` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
ralph 모드로 수행  
1. 에이젼트 호출 -> Agent: vfx-artist
