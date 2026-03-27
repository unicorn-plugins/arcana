---
name: td
description: 기술 아키텍처, 렌더링 파이프라인 설계, Spine-Unity 연동
type: orchestrator
user-invocable: true
---

# TD

[TD 스킬 활성화]

## 목표

Unity URP 2D + Spine + Addressables 기반 기술 스택을 확정하고, 렌더링 파이프라인·성능 최적화 기준을 문서화한다.

## 활성화 조건

- 사용자가 `/arcana:td` 호출 시
- "기술", "엔진", "파이프라인", "렌더링", "성능 최적화", "Spine 연동", "Addressables", "드로우콜", "GC", "직렬화" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| tech-director | `arcana:tech-director:tech-director` |

### 프롬프트 조립

`resources/guides/combine-prompt.md`를 참조하여 프롬프트 조립

## 워크플로우 
ralph 모드로 수행  
1. 에이젼트 호출 -> Agent: tech-director