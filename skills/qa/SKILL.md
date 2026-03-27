---
name: qa
description: 테스트 케이스 설계, 극단 케이스 검증, 버그 추적, QA 보고서 오케스트레이션
type: orchestrator
user-invocable: true
---

# QA

[QA 스킬 활성화]

## 목표

5대 테스트 영역(전투/천칭/증강/윤회/시너지)의 테스트 케이스를 설계하고,
극단 케이스를 자동 검증하여 출시 품질을 보장하는 QA 보고서를 산출함.

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
6. `Task(subagent_type="arcana:qa-engineer:qa-engineer", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| QA 운영 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 테스트 케이스 설계 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 극단 케이스 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 검증 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: QA 운영 분석 → Agent: qa-engineer
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: `output/planning/master_planning_v*.md` 목차를 읽고 QA 운영, 게임 시스템, 밸런싱 관련 챕터를 분석 후 테스트 범위 파악
- **EXPECTED OUTCOME**: 테스트 범위 정의서 (5대 영역별 테스트 대상, 기준 수치 목록)
- **MUST DO**: 기획서 수치(천칭 경계값, 증강 상한선, 보스 페이즈 수) 확인하여 테스트 기준 수립
- **MUST NOT DO**: 기획서 수치 미확인 상태에서 테스트 케이스 설계 시작 금지
- **CONTEXT**: `output/planning/master_planning_v*.md`, `resources/초기자료/전투컨셉기획서_V4_장보성.md`

### Phase 2: 5대 테스트 영역 케이스 설계 → Agent: qa-engineer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 전투/천칭/증강/윤회/시너지 5개 영역 테스트 케이스 전체 설계
- **EXPECTED OUTCOME**: 테스트 케이스 문서 (영역별 케이스 ID, 전제 조건, 테스트 절차, 예상 결과)
- **MUST DO**: 각 영역별 경계값 케이스 반드시 포함, 천칭 -3/+3 경계 케이스 명시 필수
- **MUST NOT DO**: 정상 케이스만 설계하고 극단 케이스 생략 금지
- **CONTEXT**: Phase 1 테스트 범위 정의서, `resources/초기자료/시너지시스템_V2_김주연.md`

### Phase 3: Unity Test Framework 자동화 설계 → Agent: qa-engineer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: EditMode/PlayMode 자동화 테스트 케이스 설계
- **EXPECTED OUTCOME**: 자동화 테스트 설계서 (테스트 클래스 구조, Assert 기준, 커버리지 목표)
- **MUST DO**: EditMode(수치 계산 단위 테스트) + PlayMode(FSM 전환, 시너지 판정) 분리 설계
- **MUST NOT DO**: 파일 직접 수정 또는 코드 실행 금지 (설계 문서만 작성)
- **CONTEXT**: Phase 2 테스트 케이스 문서, `output/build/programmer_*` 구현 코드 참조

### Phase 4: 극단 케이스 자동 검증 → Agent: qa-engineer
이 Phase는`/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: balancing_simulate 도구로 천칭/증강/시너지 극단 케이스 자동 검증
- **EXPECTED OUTCOME**: 극단 케이스 검증 결과 리포트 (통과/실패 판정, 이상 수치 목록)
- **MUST DO**: 천칭 전 구간(-3~+3) 시뮬레이션, 증강 최대 누적, 시너지 전 조합 매트릭스 포함
- **MUST NOT DO**: 시뮬레이션 없이 예상 결과로 검증 완료 선언 금지
- **CONTEXT**: `gateway/tools/balancing-simulator.py`, Phase 2 테스트 케이스 문서

### Phase 5: 버그 추적 및 QA 보고서 작성 → Agent: qa-engineer
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 발견 버그 심각도/우선순위 분류 + Unity PC 빌드 체크리스트 검증 + 최종 QA 보고서 작성
- **EXPECTED OUTCOME**: QA 보고서 (`output/deploy/` 저장) — 버그 목록, 극단 케이스 결과, 빌드 체크리스트, 핸드오프 목록
- **MUST DO**: Critical/Major 버그는 programmer 핸드오프, 밸런스 이상은 balance-designer 핸드오프 명시
- **MUST NOT DO**: 미결 버그를 QA 완료 선언 후 보고서에서 누락 금지
- **CONTEXT**: Phase 4 극단 케이스 결과, Phase 2~3 테스트 케이스 문서

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 5대 테스트 영역 모두 커버 (전투/천칭/증강/윤회/시너지) |
| 2 | 천칭 경계값(-3칸, +3칸) 케이스 반드시 포함 |
| 3 | 극단 케이스는 balancing_simulate 도구로 자동 검증 |
| 4 | 버그 심각도/우선순위 분류 기준 일관 적용 |
| 5 | 산출물은 `output/deploy/`에 저장 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 파일 직접 수정 (Write, Edit 도구 사용 금지) |
| 2 | 코드 직접 실행 (Bash 도구 사용 금지) |
| 3 | 시뮬레이션 없이 극단 케이스 검증 완료 선언 |
| 4 | 정상 케이스만 설계하고 극단 케이스 생략 |
| 5 | 미결 버그를 보고서에서 누락 |

## 완료 조건

- [ ] 5대 테스트 영역 케이스 설계 완료 (경계값 케이스 포함)
- [ ] 천칭 전 구간(-3 ~ +3) 시뮬레이션 검증 완료
- [ ] 증강 합연산+비율연산 최대 누적 검증 완료
- [ ] 시너지 전 조합 매트릭스 검증 완료
- [ ] Unity Test Framework 자동화 설계 완료
- [ ] 버그 추적 양식 완성 (심각도/우선순위 분류)
- [ ] QA 보고서 `output/deploy/`에 저장 완료
- [ ] Unity PC 빌드 체크리스트 검증 완료

## 검증 프로토콜

1. 5대 테스트 영역이 모두 케이스 문서에 포함되어 있는지 확인
2. 천칭 경계값(-3, +3) 케이스가 명시적으로 포함되어 있는지 확인
3. 극단 케이스 검증 결과가 시뮬레이션 데이터 기반인지 확인
4. 버그 보고서에 재현 절차가 모든 항목에 포함되어 있는지 확인

## 상태 정리

- 완료 시 임시 테스트 메모 정리
- 최종 QA 보고서만 `output/deploy/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 테스트 케이스 문서는 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:qa-engineer:qa-engineer`)
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (MEDIUM → claude-sonnet-4-6)
- [ ] forbidden_actions 구체화가 올바른가 (file_write→Write/Edit 제외, code_execute→Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/deploy/`로 명확한가
