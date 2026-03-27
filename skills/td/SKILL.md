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

### 프롬프트 조립 절차

1. `agents/tech-director/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**:
     - `doc_search` → `tool_mapping.doc_search` → context7 MCP (query-docs, resolve-library-id)
     - `art_pipeline` → `tool_mapping.art_pipeline` → `tools/art-pipeline-guide.py`
   - **금지액션 구체화**: `forbidden_actions: []` → 제외 도구 없음
   - **최종 도구** = context7 MCP + art-pipeline-guide.py (전체 허용)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 우디입니다. 답변 시 별명 '우디'를 표시하세요. Problem Solver, Pipeline Architect, Optimization Expert, Bridge-Builder, Technical Specialist. 그래픽 엔진 최적화 및 아트-프로그래밍 간 기술적 가교 역할 수행 8년, 렌더링 파이프라인 설계 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:tech-director:tech-director", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
