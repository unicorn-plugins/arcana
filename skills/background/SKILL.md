---
name: background
description: 배경 컨셉 및 조명/분위기 가이드 오케스트레이션
type: orchestrator
user-invocable: true
---

# Background

[Background 스킬 활성화]

## 목표

아르카나 게임의 4스테이지별 배경 컨셉 가이드와 Unity 2D Lighting/Tilemap/Parallax 기준을 수립하여, 각 스테이지(The Chariot / Justice / The Hermit / The World)의 고유한 세계관 분위기를 구현한다.

## 활성화 조건

- 사용자가 `/arcana:background` 호출 시
- "배경", "환경 아트", "스테이지 배경", "조명/분위기", "배경 컨셉", "월드 아트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| background-artist | `arcana:background-artist:background-artist` |

### 프롬프트 조립 절차

1. `agents/background-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: LOW` → `tier_mapping.default.LOW` → 해당 모델
   - **툴 구체화**: tools.yaml의 `generate_image` → `tool_mapping.generate_image` → MCP 서버
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재 시:
   "당신은 령입니다. 답변 시 별명 '령'를 표시하세요. Immersive World Creator, Environment Specialist, Lighting Master. 게임 내 몰입감을 극대화하는 랜드마크 및 필드 오브젝트 그래픽 제작 5년, 배경 컨셉 아트 전문."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:background-artist:background-artist", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 지역/배경 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 컨셉 가이드 작성 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| Unity 규격 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 지역/배경 분석 → Agent: background-artist
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서 2.3장(주요 지역)과 6.3장(배경 환경 아트 가이드), 내부문서 2종을 분석하여 4스테이지 지역 설정 파악
- **EXPECTED OUTCOME**: 4스테이지 지역 분석 보고서 (각 스테이지 세계관, 분위기, 건축 키워드)
- **MUST DO**: 4개 스테이지 모두 포함, 각 영역 지배 보스와 세계관 연계 분석
- **MUST NOT DO**: 마스터 기획서 지역 설정 임의 변경 금지
- **CONTEXT**: `output/planning/master_planning_v*.md` 2.3장, 6.3장, `resources/초기자료/배경컨셉_V0_이채연.md`

### Phase 2: 4스테이지별 배경 컨셉 가이드 작성 → Agent: background-artist
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 중세 건축 + 판타지 환경 참조를 기반으로 4스테이지 배경 컨셉 가이드와 Unity 2D Lighting 조명 기준 작성
- **EXPECTED OUTCOME**: `output/design/stage-background-concepts.md`, `output/design/lighting-atmosphere-guide.md`
- **MUST DO**: 각 스테이지별 색상 팔레트, 주요 구조물, Unity 조명 설정값(강도, 색상) 포함
- **MUST NOT DO**: AD 비주얼 아이덴티티 가이드의 스테이지별 색상 지정을 벗어난 임의 결정 금지
- **CONTEXT**: `resources/references/external/background-artist/`, Phase 1 분석 결과, `output/design/visual-identity-guide.md`

### Phase 3: Unity 구현 기준 검증 → Agent: background-artist
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: Tilemap/Parallax 레이어 구성 기준 검증 및 최종 가이드 완성
- **EXPECTED OUTCOME**: 검증 완료된 배경 컨셉 가이드 2종, Unity 레이어 구성표 포함
- **MUST DO**: 5-레이어 구성(원경~전경) 및 스크롤 배율 명세 포함
- **MUST NOT DO**: Unity 구현 기준 없이 비주얼 컨셉만 작성 금지
- **CONTEXT**: `resources/references/external/background-artist/unity_tilemap_parallax.md`, `resources/references/external/background-artist/unity_2d_lighting_urp.md`, Phase 2 산출물

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 배경 컨셉은 중세 건축 레퍼런스 및 판타지 환경 가이드 근거 필수 |
| 2 | 4스테이지 모두 포함 (The Chariot / Justice / The Hermit / The World) |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | Unity 2D Lighting(URP) 조명 설정값과 Tilemap 레이어 구성 포함 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | AD 비주얼 아이덴티티 가이드의 스테이지별 색상을 벗어난 임의 결정 |
| 2 | Unity 구현 기준(Tilemap, Lighting) 없이 컨셉 아트만 제시 |
| 3 | 코드 작성 및 실행 (배경 아트 기획 역할만 수행) |

## 완료 조건

- [ ] 4개 스테이지 배경 컨셉 가이드 `output/design/stage-background-concepts.md` 저장 완료
- [ ] 조명/분위기 가이드 `output/design/lighting-atmosphere-guide.md` 저장 완료
- [ ] 각 스테이지별 Unity 조명 설정값(강도, 색상) 포함 확인
- [ ] Tilemap/Parallax 5-레이어 구성표 포함 확인

## 검증 프로토콜

1. 4스테이지 배경 컨셉이 마스터 기획서 2.3장 지역 설정과 일치하는지 확인
2. Unity 2D Lighting 설정값이 스테이지별 분위기와 연계되는지 확인
3. Tilemap 레이어 구성의 스크롤 배율이 근경→원경 순서로 올바르게 설정되었는지 확인
4. AD 비주얼 아이덴티티 가이드의 스테이지별 색상 지정과 배경 컨셉이 일치하는지 확인

## 상태 정리

- 완료 시 임시 분석 메모 정리
- 최종 배경 컨셉 가이드, 조명/분위기 가이드만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 초안은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:background-artist:background-artist`)
- [ ] runtime-mapping.yaml 참조하여 LOW tier 모델 매핑이 올바른가
- [ ] forbidden_actions `["code_execute"]` 구체화가 올바른가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목(TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT)이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/design/`로 명확한가
