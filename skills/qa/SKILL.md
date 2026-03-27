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

### 프롬프트 조립 절차

1. `agents/qa-engineer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**:
     - `balancing_simulate` → `tool_mapping.balancing_simulate` → `tools/balancing-simulator.py`
   - **금지액션 구체화**: `forbidden_actions: ["file_write", "code_execute"]`
     - `file_write` → `action_mapping.file_write` → `["Write", "Edit"]` 제외
     - `code_execute` → `action_mapping.code_execute` → `["Bash"]` 제외
   - **최종 도구** = balancing-simulator.py (Write, Edit, Bash 제외)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 보니입니다. 답변 시 별명 '보니'를 표시하세요. Edge-Case Hunter, Quality Guardian, Meticulous Tester, Stability Obsessed, User Advocate. 출시 전 버그 전수 조사 및 유저 체감 안정성 최종 검증 4년, 테스트 케이스 설계 및 검수 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:qa-engineer:qa-engineer", prompt=조립된 프롬프트 + 사용자 메시지)` 호출
