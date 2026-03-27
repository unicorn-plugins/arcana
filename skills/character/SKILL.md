---
name: character
description: 캐릭터 디자인 및 카드 일러스트 검증 오케스트레이션
type: orchestrator
user-invocable: true
---

# Character

[Character 스킬 활성화]

## 목표

아르카나 게임의 플레이어블 캐릭터(7종) 및 보스(5종)의 디자인 참조 시트와 정방향/역방향 포즈 가이드를 작성하고, Unity Sprite 규격에 맞는 카드 일러스트 레이아웃을 검증한다.

## 활성화 조건

- 사용자가 `/arcana:character` 호출 시
- "캐릭터 디자인", "캐릭터 원화", "포즈 가이드", "카드 일러스트", "캐릭터 시트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| character-artist | `arcana:character-artist:character-artist` |

### 프롬프트 조립 절차

1. `agents/character-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → 해당 모델
   - **툴 구체화**: tools.yaml의 `generate_image` → `tool_mapping.generate_image` → MCP 서버
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 아트 트리오입니다. 답변 시 별명 '아트 트리오'를 표시하세요. Creative Character Designer, Anatomy Expert, Style Adaptive. 유명 모바일 게임 캐릭터 원화 및 코스튬 디자인, 매력적인 캐릭터 IP 창출 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:character-artist:character-artist", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 캐릭터 기획 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 디자인 시트 작성 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 레이아웃 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 캐릭터/아트 가이드 분석 → Agent: character-artist
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서 4장(캐릭터 기획)과 6.2장(캐릭터 아트 가이드), 내부문서 4종을 분석하여 캐릭터별 비주얼 설정 파악
- **EXPECTED OUTCOME**: 캐릭터 기획 현황 보고서 (7종 플레이어블 + 5종 보스 비주얼 설정)
- **MUST DO**: 각 캐릭터의 능력/스킬과 비주얼 설정 간 연계 분석 포함
- **MUST NOT DO**: 마스터 기획서 캐릭터 설정 임의 변경 금지
- **CONTEXT**: `output/planning/master_planning_v*.md` 4장, 6.2장, `resources/초기자료/캐릭터비주얼컨셉_V1_이채연.md`

### Phase 2: 캐릭터 디자인 시트 및 포즈 가이드 작성 → Agent: character-artist
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 해부학/포즈 + 중세 의상 + 타로 도상학 참조를 기반으로 12종 캐릭터 디자인 시트와 정방향/역방향 포즈 가이드 작성
- **EXPECTED OUTCOME**: `output/design/character-design-sheets.md`, `output/design/pose-guide.md`
- **MUST DO**: 각 캐릭터 정방향/역방향 2가지 포즈 명세, 상징 소품 포함
- **MUST NOT DO**: AD 가이드(비주얼 아이덴티티)를 벗어난 색상/스타일 임의 결정 금지
- **CONTEXT**: `resources/references/external/character-artist/`, Phase 1 분석 결과, `output/design/visual-identity-guide.md`

### Phase 3: 카드 레이아웃 검증 → Agent: character-artist
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: Unity Sprite 규격 기준으로 카드 일러스트 레이아웃 검증 및 결과 보고
- **EXPECTED OUTCOME**: `output/design/card-layout-validation.md` (모든 체크리스트 항목 통과)
- **MUST DO**: 배경 색상 규칙, 이름표 영역 가림 금지, 정/역 포즈 방향 일치 검증
- **MUST NOT DO**: 미검증 레이아웃을 통과 처리 금지
- **CONTEXT**: `resources/references/external/character-artist/unity_sprite_guide.md`, Phase 2 산출물, `output/design/card-layout-standard.md`

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 캐릭터 디자인은 타로 도상학 및 중세 의상 레퍼런스 근거 필수 |
| 2 | 정방향/역방향 포즈 2종을 반드시 명세 (심리적 대비 명확히) |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | AD 비주얼 아이덴티티 가이드 준수 여부 확인 후 작업 시작 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | AD 가이드(색상 지정, 프레임 규칙)를 벗어난 임의 비주얼 결정 |
| 2 | 이름표 영역(카드 하단)을 캐릭터 신체로 가리는 레이아웃 승인 |
| 3 | 코드 작성 및 실행 (캐릭터 아트 기획 역할만 수행) |

## 완료 조건

- [ ] 플레이어블 캐릭터 7종 디자인 시트 작성 완료
- [ ] 보스 캐릭터 5종 디자인 시트 작성 완료
- [ ] 전 캐릭터 정방향/역방향 포즈 가이드 완료
- [ ] 카드 레이아웃 검증 체크리스트 전 항목 통과
- [ ] `output/design/`에 3종 산출물 저장 완료

## 검증 프로토콜

1. 캐릭터 디자인 시트의 타로 도상학 상징 소품이 원전과 일치하는지 확인
2. 포즈 가이드의 정방향/역방향 심리적 대비가 명확한지 확인
3. 카드 레이아웃 검증에서 Unity Sprite 규격(PPU, Pivot)이 포함되었는지 확인
4. AD 비주얼 아이덴티티 가이드 색상 지정과 캐릭터 디자인 시트가 일치하는지 확인

## 상태 정리

- 완료 시 임시 분석 메모 정리
- 최종 디자인 시트, 포즈 가이드, 검증 결과만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 초안은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:character-artist:character-artist`)
- [ ] runtime-mapping.yaml 참조하여 MEDIUM tier 모델 매핑이 올바른가
- [ ] forbidden_actions `["code_execute"]` 구체화가 올바른가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목(TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT)이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/design/`로 명확한가
