---
name: pd
description: 프로젝트 총괄 관리 및 크로스 역할 조율 오케스트레이션
type: orchestrator
user-invocable: true
---

# PD

[PD 스킬 활성화]

## 목표

아르카나 프로젝트의 전체 현황을 조망하고 크로스 역할 산출물의 정합성을 검증하여,
마일스톤 기반 의사결정 보고서를 산출함.

## 활성화 조건

- 사용자가 `/arcana:pd` 호출 시
- "전체 검토", "프로젝트 현황", "크로스 체크", "산출물 검토", "마일스톤" 키워드 감지 시
- core 스킬이 PD 조율 위임(후보 4개 이상 또는 역할 간 의존성 충돌) 판단 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| pd | `arcana:pd:pd` |

### 프롬프트 조립 절차

1. `agents/pd/` 에서 3파일 로드:
   - `AGENT.md` (프롬프트 본문 — WHY + HOW)
   - `agentcard.yaml` (tier 확인 + persona 첨부)
   - `tools.yaml` (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**: tools.yaml의 `diagram_validate` → `tool_mapping.diagram_validate` → `tools/check-mermaid-bridge.py` (`validate_mermaid`)
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping.code_execute` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재하므로:
   "당신은 주디입니다. 답변 시 별명 '주디'를 표시하세요. Visionary Leader, Audio-Visual Specialist, Creative Director, Holistic Orchestrator, Detail Oriented. 메이저 게임사 사운드 팀장(6년), 다수의 인디 게임 총괄 디렉팅 및 배경음악/효과음 사운드 엔지니어링 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:pd:pd", model="claude-opus-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 현황 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 크로스 체크 실행 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 보고서 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 현황 분석 -> Agent: pd
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: `resources/references/index.md` PD 섹션 확인 후, 마스터 기획서의 목차를 읽고 프로젝트 개요 관련 챕터 + 전 챕터 헤더 스캔으로 프로젝트 전체 현황 파악
- **EXPECTED OUTCOME**: 현재 마일스톤 단계, 진행률, 주요 이슈 목록이 담긴 현황 요약
- **MUST DO**: 마스터 기획서 최신 버전(`master_planning_v*.md` 중 최고 버전 번호) 참조
- **MUST NOT DO**: 현황 파악 없이 의사결정 진행 금지
- **CONTEXT**: `output/planning/master_planning_v*.md`, `resources/references/index.md`

### Phase 2: 크로스 역할 체크 -> Agent: pd
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 각 역할 산출물 디렉토리(`output/planning/`, `output/design/`, `output/build/`, `output/deploy/`) 확인, 파트 간 정합성 검증 및 병목 식별
- **EXPECTED OUTCOME**: 역할별 산출물 상태표 + 정합성 이슈 목록 + 병목 지점
- **MUST DO**: 세계관 톤(암흑기→르네상스 과도기, 고어/유치함 금지) 및 용어 통일(단어집 기준) 위반 여부 반드시 확인
- **MUST NOT DO**: 산출물이 없는 역할을 "정상"으로 판단 금지
- **CONTEXT**: Phase 1 현황 요약, `output/{planning|design|build|deploy}/`

### Phase 3: 의사결정 보고서 작성 -> Agent: pd
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: Phase 1~2 결과를 종합하여 스코프 조정, 우선순위 판단, 역할 간 충돌 해소 의사결정 기록 작성
- **EXPECTED OUTCOME**: 검증 완료된 PD 보고서 `output/planning/pd_report_{YYYYMMDD}.md`에 저장
- **MUST DO**: 모든 의사결정은 근거와 영향 역할을 명시
- **MUST NOT DO**: 미검증 판단을 최종 보고서에 포함 금지
- **CONTEXT**: Phase 1~2 결과물

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 마스터 기획서는 항상 최신 버전(`master_planning_v*.md` 중 최고 버전 번호)을 참조 |
| 2 | 크로스 역할 체크 시 전 역할 산출물 디렉토리를 빠짐없이 확인 |
| 3 | 세계관 톤(암흑기→르네상스 과도기) 및 용어 통일(단어집 기준) 위반 사항 반드시 명시 |
| 4 | 모든 의사결정은 근거와 영향 역할을 병기 |
| 5 | 산출물은 `output/planning/`에 저장 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 코드 실행 (`Bash` 도구 사용 금지) |
| 2 | 개별 역할의 전문 영역(수치 밸런싱, 아트 스타일 등) 직접 결정 — 해당 역할 에이전트에 핸드오프 |
| 3 | 근거 없는 스코프 확장 또는 기획서에 없는 시스템 추가 |
| 4 | 산출물이 없는 역할을 검토 완료로 처리 |

## 완료 조건

- [ ] 마스터 기획서 최신 버전 기반 현황 파악 완료
- [ ] 전 역할 산출물 디렉토리 크로스 체크 완료
- [ ] 세계관 톤 일관성 검증 완료
- [ ] 의사결정 보고서 `output/planning/`에 저장 완료

## 검증 프로토콜

1. 에이전트 FQN `arcana:pd:pd` 정확성 확인
2. 마스터 기획서가 최신 버전인지 확인
3. 크로스 체크 대상 디렉토리 4개(`planning`, `design`, `build`, `deploy`) 모두 포함 여부 확인
4. 의사결정 보고서에 근거 및 영향 역할이 모두 명시되었는지 확인

## 상태 정리

- 완료 시 임시 분석 메모 정리
- 최종 보고서만 `output/planning/pd_report_{YYYYMMDD}.md`로 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 분석 결과는 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:pd:pd`)
- [ ] runtime-mapping.yaml 참조하여 tier(HIGH) → 모델(claude-opus-4-6) 매핑이 올바른가
- [ ] forbidden_actions(code_execute → Bash 제외) 구체화가 올바른가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(-> Agent:)에 5항목(TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT)이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로(`output/planning/`)가 명확한가
