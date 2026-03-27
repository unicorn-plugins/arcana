---
name: program
description: 게임 로직 구현, 데이터 구조 설계, ScriptableObject 에셋 관리 오케스트레이션
type: orchestrator
user-invocable: true
---

# Program

[Program 스킬 활성화]

## 목표

전투/천칭/카드/시너지/궁극기/증강 핵심 시스템을 기획서 수치에 정확히 기반하여 구현하고,
ScriptableObject 데이터 에셋과 JSON/CSV 로더를 통해 데이터-로직 분리 구조를 확립함.

## 활성화 조건

- 사용자가 `/arcana:program` 호출 시
- "코드", "구현", "로직", "데이터 구조", "JSON 로더", "FSM", "전투 시스템", "천칭 구현", "시너지 로직", "궁극기", "증강 구현" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| programmer | `arcana:programmer:programmer` |

### 프롬프트 조립 절차

1. `agents/programmer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**:
     - `doc_search` → `tool_mapping.doc_search` → context7 MCP (query-docs, resolve-library-id)
     - `game_data_schema` → `tool_mapping.game_data_schema` → `tools/game-data-schema.py`
   - **금지액션 구체화**: `forbidden_actions: []` → 제외 도구 없음
   - **최종 도구** = context7 MCP + game-data-schema.py (전체 허용)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 진입니다. 답변 시 별명 '진'를 표시하세요. Clean Coder, Logical Thinker, Debugging Expert, Collaborative Developer, Efficient Scripter. 게임 내 콘텐츠 기능 구현 및 안정적인 데이터 처리 로직 개발, 멀티 플랫폼 이식 지원 전문."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:programmer:programmer", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 시스템 기획 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 핵심 시스템 구현 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 구현 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 검증 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 시스템 기획 분석 → Agent: programmer
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: `output/planning/master_planning_v*.md` 3장 전체 + 10.4장 완독 후 구현 요구사항 추출
- **EXPECTED OUTCOME**: 구현 우선순위 목록 + 시스템별 수치 정리 (코스트, 천칭 칸 수치, 드로우 수 등)
- **MUST DO**: 내부문서 전투/천칭/시너지/증강/턴/파티 기획서 교차 참조, 수치 불일치 시 최신 기획서 우선
- **MUST NOT DO**: 기획서 수치 미확인 상태에서 임의 수치 사용 금지
- **CONTEXT**: `output/planning/master_planning_v*.md`, `resources/초기자료/전투컨셉기획서_V4_장보성.md` 등

### Phase 2: 아키텍처 및 전투 시스템 구현 → Agent: programmer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: FSM 기반 전투 시스템 아키텍처 설계 + 턴 구조/코스트/드로우 구현
- **EXPECTED OUTCOME**: `BattleStateMachine.cs` + `TurnManager.cs` + `DeckManager.cs` 구현 코드 및 설명
- **MUST DO**: doc_search로 Unity Scripting API + 게임 프로그래밍 패턴(State Machine) 참조
- **MUST NOT DO**: 하드코딩된 수치 사용 금지 (ScriptableObject 또는 외부 데이터 참조 필수)
- **CONTEXT**: Phase 1 구현 요구사항, 기획서 3.4장

### Phase 3: 천칭 시스템 구현 → Agent: programmer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 천칭 증감치 처리 + 칸 이동 + 효과 즉시 적용 로직 구현
- **EXPECTED OUTCOME**: `LibraSystem.cs` 구현 코드 (역방향 +10/정방향 -10, 칸당 50, 3칸 구조)
- **MUST DO**: Observer 패턴으로 천칭 수치 변화 → UI 이벤트 전파 구현, 경계값(-3/+3) 처리 포함
- **MUST NOT DO**: 경계값 처리 없이 천칭 로직 완성 선언 금지
- **CONTEXT**: 기획서 3.3장, `resources/초기자료/천칭시스템기획서_V1_이채연.md`

### Phase 4: 카드/시너지/궁극기 구현 → Agent: programmer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 3종 시너지 세트 판정 로직 + 궁극기 3회 연속 발동 + 하이라이트 UI 연동 구현
- **EXPECTED OUTCOME**: `SynergyManager.cs` + `UltimateSystem.cs` 구현 코드
- **MUST DO**: 3종 시너지(정방향/역방향/혼합) 전 조합 커버, 특수 카드(Hangedman, Devil) 예외 처리 포함
- **MUST NOT DO**: 시너지 판정 없이 UI 하이라이트만 구현 금지
- **CONTEXT**: `resources/초기자료/시너지시스템_V2_김주연.md`, `resources/초기자료/특수카드시스템_V2_김주연_pptx.md`

### Phase 5: 증강 시스템 + 데이터 구조 구현 → Agent: programmer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 증강 합연산/비율연산 + 슬롯 귀속 + ScriptableObject 에셋 + JSON/CSV 로더 구현
- **EXPECTED OUTCOME**: `AugmentSystem.cs` + 데이터 에셋 클래스 + `JsonLoader.cs` + `CsvLoader.cs` 코드
- **MUST DO**: game_data_schema 도구로 JSON 스키마 생성, 비율연산 상한선 검증 코드 필수 포함
- **MUST NOT DO**: 상한선 검증 없이 비율연산 증강 완성 선언 금지
- **CONTEXT**: `resources/초기자료/증강시스템_V2_김주연.md`, Phase 1 구현 요구사항

### Phase 6: DOTween 애니메이션 + 최종 검증 → Agent: programmer
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 카드 드로우/시너지/천칭 DOTween Tween 구현 + 전체 시스템 통합 검증
- **EXPECTED OUTCOME**: `CardAnimator.cs` 구현 코드 + 최종 구현 문서 (`output/build/` 저장)
- **MUST DO**: doc_search로 DOTween API 참조, 모든 Tween에 풀링 적용 (TD 성능 기준 준수)
- **MUST NOT DO**: 성능 기준(TD 산출물) 미확인 상태에서 애니메이션 구현 금지
- **CONTEXT**: `output/build/td_*` TD 기술 문서, Phase 2~5 구현 코드

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 수치는 기획서에서 확인 후 사용 (코스트 최대 10, 천칭 칸당 50, 드로우 18장 중 6장) |
| 2 | 수치는 하드코딩 금지 — ScriptableObject 또는 외부 데이터 참조 필수 |
| 3 | 증강 비율연산 상한선 검증 코드 반드시 포함 |
| 4 | 산출물은 `output/build/`에 저장 |
| 5 | TD 기술 표준(`output/build/td_*`) 준수 (직렬화 방식, 풀링 기준) |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 기획서 수치 미확인 상태에서 임의 수치 하드코딩 |
| 2 | 경계값 처리 없이 천칭 시스템 완성 선언 |
| 3 | 증강 비율연산 상한선 검증 없이 증강 시스템 완성 선언 |
| 4 | TD 기술 표준 미확인 상태에서 직렬화 방식 임의 결정 |

## 완료 조건

- [ ] 전투 FSM 구현 완료 (PlayerTurn / MonsterTurn / ResolvePhase / BattleEnd)
- [ ] 천칭 시스템 구현 완료 (경계값 -3/+3 처리 포함)
- [ ] 3종 시너지 판정 로직 구현 완료 (전 조합 커버)
- [ ] 궁극기 3회 연속 발동 로직 구현 완료
- [ ] 증강 합연산+비율연산 상한선 검증 포함 구현 완료
- [ ] ScriptableObject 데이터 에셋 클래스 설계 완료
- [ ] JSON/CSV 로더 구현 완료
- [ ] 전 산출물 `output/build/`에 저장 완료

## 검증 프로토콜

1. 기획서 수치(코스트 10, 천칭 칸당 50, 드로우 6장)가 코드에 정확히 반영되었는지 확인
2. 증강 비율연산 상한선 검증 코드가 포함되어 있는지 확인
3. 3종 시너지 전 조합이 커버되는지 매트릭스 검증
4. TD 기술 표준(직렬화 방식, 풀링 기준) 준수 여부 확인

## 상태 정리

- 완료 시 임시 분석 메모 정리
- 구현 코드 및 데이터 스키마만 `output/build/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 Phase 구현 코드는 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 구현 코드 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:programmer:programmer`)
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (MEDIUM → claude-sonnet-4-6)
- [ ] forbidden_actions가 빈 배열로 올바르게 처리되었는가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/build/`로 명확한가
