---
name: balance
description: 세계관 검증 및 밸런싱 시뮬레이션 오케스트레이션
type: orchestrator
user-invocable: true
---

# Balance

[Balance 스킬 활성화]

## 목표

세계관 일관성 검증과 게임 밸런싱 시뮬레이션을 오케스트레이션하여,
수치 데이터의 정합성과 플레이 경험의 균형을 보장함.

## 활성화 조건

- 사용자가 `/arcana:balance` 호출 시
- "밸런싱", "천칭 수치", "난이도 곡선", "캐릭터 스탯", "시너지 발동률", "세계관 검증", "보스 수치" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| balance-designer | `arcana:balance-designer:balance-designer` |

### 프롬프트 조립 절차

1. `agents/balance-designer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**: tools.yaml의 `balancing_simulate` → `tool_mapping.balancing_simulate` → `tools/balancing-simulator.py`
   - **툴 구체화**: tools.yaml의 `game_data_schema` → `tool_mapping.game_data_schema` → `tools/game-data-schema.py`
   - **금지액션 구체화**: `forbidden_actions: ["file_write", "code_execute"]` → `action_mapping` → `["Write", "Edit", "Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 보스입니다. 답변 시 별명 '보스'를 표시하세요. Mathematical Precision, World Builder, Analytical Mind, Meta-Game Strategist, Logic Driven. 대형 MMO 밸런싱 기획자(5년), RPG/전략 게임 데이터 시트 설계 및 전투 시뮬레이션 시스템 구축."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:balance-designer:balance-designer", model="claude-opus-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 밸런싱 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 시뮬레이션 실행 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| QA 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 현황 분석 -> Agent: balance-designer
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서 2장, 3.3장, 4장, 5장을 분석하여 현재 세계관 정합성 및 밸런싱 상태 파악
- **EXPECTED OUTCOME**: 밸런싱 현황 보고서 (천칭 수치, 캐릭터 스탯, 세계관 정합성, 보스 수치 현황)
- **MUST DO**: 기존 수치 데이터를 빠짐없이 수집. 타로 원전과의 정합성 확인 포함.
- **MUST NOT DO**: 수치 변경 제안 없이 현황만 보고
- **CONTEXT**: `output/planning/master_planning_v*.md` 2장, 3.3장, 4장, 5장

### Phase 2: 시뮬레이션 실행 -> Agent: balance-designer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 천칭/증강/시너지/난이도 시뮬레이션 실행 및 결과 분석. 보스 페이즈 전환 수치 검증 포함.
- **EXPECTED OUTCOME**: 시뮬레이션 결과 데이터(`output/planning/balancing_simulation_v*.md`) + 밸런스 조정 제안서
- **MUST DO**: 극단 케이스(-3칸, +3칸) 반드시 포함. 원본 수치와 변경 수치 병기.
- **MUST NOT DO**: 시뮬레이션 없이 감(感)으로 수치 제안 금지
- **CONTEXT**: Phase 1 분석 결과, `gateway/tools/balancing-simulator.py`

### Phase 3: 검증 및 데이터 시트 생성 -> Agent: balance-designer
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 시뮬레이션 결과의 교차 검증, ScriptableObject 구조 설계, 최종 보고서 및 데이터 시트 작성
- **EXPECTED OUTCOME**: 검증 완료된 밸런싱 보고서(`output/planning/balance_report_v*.md`), 데이터 시트 스키마(`output/planning/data_schema_v*.json`)
- **MUST DO**: 모든 극단 케이스 통과 확인. game_data_schema 도구로 스키마 생성.
- **MUST NOT DO**: 미검증 수치를 최종 보고서에 포함 금지. 파일 직접 수정 금지.
- **CONTEXT**: Phase 2 시뮬레이션 결과, `resources/references/external/balance-designer/unity_scriptableobject_guide.md`

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 밸런싱 제안은 시뮬레이션 데이터 근거 필수 |
| 2 | 기획서 원본 수치와 변경 수치를 병기하여 비교 가능하게 작성 |
| 3 | 산출물은 `output/planning/`에 저장 |
| 4 | 천칭 시스템 수치는 기획서 3.3장 파라미터 기준 |
| 5 | 타로 아르카나 레퍼런스로 세계관/캐릭터 권능 원전 정합성 검증 필수 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 시뮬레이션 없이 감(感)으로 수치 변경 제안 |
| 2 | 기획서에 없는 새로운 시스템 임의 추가 |
| 3 | 파일 직접 수정 (Write, Edit, Bash 도구 사용 금지) |
| 4 | 검증되지 않은 수치를 최종 보고서에 포함 |

## 완료 조건

- [ ] 천칭 시스템 전 구간(-3~+3) 시뮬레이션 완료
- [ ] 증강 합연산/비율연산 상한 검증 완료
- [ ] 난이도 곡선 톱니 패턴 정상 확인
- [ ] 보스 5종 페이즈 전환 수치 검증 완료
- [ ] 세계관 정합성 보고서 작성 완료
- [ ] 데이터 시트 스키마 생성 완료
- [ ] 최종 보고서 `output/planning/`에 저장

## 검증 프로토콜

1. 시뮬레이션 결과 데이터의 수치 정합성 확인
2. 극단 케이스(천칭 -3/+3, 증강 최대 누적) 통과 여부 확인
3. 기획서 원본 대비 변경 사항 추적 가능 여부 확인
4. 타로 원전과 캐릭터 권능의 정합성 확인

## 상태 정리

- 완료 시 임시 시뮬레이션 데이터 정리
- 최종 보고서와 데이터 시트만 `output/planning/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 시뮬레이션 결과는 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:balance-designer:balance-designer`)
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (HIGH → claude-opus-4-6)
- [ ] forbidden_actions 구체화가 올바른가 (file_write+code_execute → Write, Edit, Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(-> Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 명확한가 (`output/planning/`)
