---
name: pm
description: 일정 관리, WBS, 스프린트 계획, 시스템 스펙 관리 오케스트레이션
type: orchestrator
user-invocable: true
---

# PM

[PM 스킬 활성화]

## 목표

아르카나 프로젝트의 일정 관리와 시스템 기획 상세화를 오케스트레이션하여,
마일스톤 준수와 시스템 스펙의 완결성을 보장함.

## 활성화 조건

- 사용자가 `/arcana:pm` 호출 시
- "일정", "마일스톤", "스프린트", "WBS", "리스크 레지스터", "시스템 스펙", "기획 문서" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| project-manager | `arcana:project-manager:project-manager` |

### 프롬프트 조립 절차

1. `agents/project-manager/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**: tools.yaml의 `diagram_validate` → `tool_mapping.diagram_validate` → `tools/check-mermaid-bridge.py`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 체리입니다. 답변 시 별명 '체리'를 표시하세요. Goal-Oriented, Structural Thinker, Efficiency Optimizer, Risk Manager, Agile Practitioner. IT 스타트업 PM(4년), 애자일 방법론 기반 스케줄링 및 게임 코어 시스템 아키텍처 설계 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:project-manager:project-manager", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 현황 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| WBS/스프린트 계획 작성 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 스펙 문서 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 현황 분석 -> Agent: project-manager
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서의 목차를 읽고 마일스톤 및 게임 시스템 기획 관련 챕터를 분석하여 현재 일정 및 시스템 스펙 현황 파악
- **EXPECTED OUTCOME**: 현황 분석 보고서 (마일스톤 진행률, 미결 시스템 스펙, 리스크 목록)
- **MUST DO**: 각 마일스톤의 완료 기준(Definition of Done)을 명확히 파악
- **MUST NOT DO**: 현황 파악 없이 새 계획 작성 금지
- **CONTEXT**: `output/planning/master_planning_v*.md` 마일스톤 및 게임 시스템 관련 챕터

### Phase 2: WBS 및 스프린트 계획 수립 -> Agent: project-manager
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 마일스톤별 WBS 분해 및 2주 단위 스프린트 계획 작성
- **EXPECTED OUTCOME**: WBS 문서(`output/planning/wbs_v*.md`), 스프린트 계획서(`output/planning/sprint_plan_sprN.md`)
- **MUST DO**: 역할별 담당자 매핑 및 의존성 명시 필수. 애자일 게임 개발 가이드 준수.
- **MUST NOT DO**: 의존성 미검토 상태로 병렬 작업 배치 금지
- **CONTEXT**: Phase 1 분석 결과, `resources/references/external/project-manager/agile_game_development.md`, `resources/references/external/project-manager/unity_milestone_template.md`

### Phase 3: 시스템 스펙 문서화 및 검증 -> Agent: project-manager
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 시스템별 상세 스펙 문서 작성/갱신 및 다이어그램 검증
- **EXPECTED OUTCOME**: 시스템 상세 스펙(`output/planning/system_spec_{시스템명}.md`), 검증된 Mermaid 다이어그램
- **MUST DO**: diagram_validate 도구로 모든 Mermaid 다이어그램 검증. GDD 작성 가이드 양식 준수.
- **MUST NOT DO**: 미검증 다이어그램을 최종 산출물에 포함 금지
- **CONTEXT**: Phase 2 결과, `resources/references/external/project-manager/gdd_writing_guide.md`

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 일정 계획은 마스터 기획서 마일스톤 기준에 부합해야 함 |
| 2 | WBS는 에픽→스토리→태스크 3단계로 분해하여 역할별 담당자를 명시 |
| 3 | 스프린트 계획은 2주 단위로, 목표·백로그·담당자를 포함 |
| 4 | 산출물은 반드시 `output/planning/`에 저장 |
| 5 | diagram_validate 도구로 모든 Mermaid 다이어그램 검증 후 제출 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 코드 실행 또는 파일 직접 수정 (Bash 도구 사용 금지) |
| 2 | 마스터 기획서 마일스톤과 충돌하는 독자적 일정 수립 |
| 3 | 스코프 변경 의사결정을 PM 독단으로 처리 (PD 핸드오프 필요) |
| 4 | 검증되지 않은 시스템 스펙을 확정 문서로 제출 |

## 완료 조건

- [ ] 현재 마일스톤 대비 진행률 분석 완료
- [ ] WBS 전체 항목 역할별 담당자 매핑 완료
- [ ] 스프린트 계획서 (백로그 포함) 작성 완료
- [ ] 시스템 스펙 문서 갱신 완료 (전투/천칭/증강/파티/노드)
- [ ] 리스크 레지스터 갱신 완료
- [ ] 모든 Mermaid 다이어그램 검증 통과
- [ ] 산출물 `output/planning/`에 저장 완료

## 검증 프로토콜

1. WBS 항목이 마일스톤 완료 기준을 충족하는지 확인
2. 스프린트 계획이 팀 전체 역할 리소스를 초과하지 않는지 확인
3. 시스템 스펙 문서에 미결 사항(Open Issue)이 모두 기록되었는지 확인
4. diagram_validate 결과 오류 0건 확인

## 상태 정리

- 완료 시 작업 중 임시 분석 메모 정리
- 확정된 산출물만 `output/planning/`에 보존
- 미완료 항목은 다음 스프린트 백로그로 이관

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 작업 내용은 임시 파일로 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:project-manager:project-manager`)
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (MEDIUM → claude-sonnet-4-6)
- [ ] forbidden_actions 구체화가 올바른가 (code_execute → Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(-> Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 명확한가 (`output/planning/`)
