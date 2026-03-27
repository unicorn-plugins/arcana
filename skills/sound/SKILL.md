---
name: sound
description: 사운드 디렉팅 및 BGM/SFX 설계 오케스트레이션
type: orchestrator
user-invocable: true
---

# Sound

[Sound 스킬 활성화]

## 목표

아르카나 게임의 사운드 방향성을 수립하고 BGM/SFX 상세 설계 및 에셋 카탈로그를
산출하여 사운드-이펙트-구현 파이프라인의 기초를 마련함.

## 활성화 조건

- 사용자가 `/arcana:sound` 호출 시
- "BGM", "SFX", "사운드", "음향", "효과음", "배경음악", "FMOD", "AudioMixer" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| sound-director | `arcana:sound-director:sound-director` |

### 프롬프트 조립 절차

1. `agents/sound-director/` 에서 3파일 로드:
   - `AGENT.md` (프롬프트 본문 — WHY + HOW)
   - `agentcard.yaml` (tier 확인 + persona 첨부)
   - `tools.yaml` (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**: tools.yaml의 `sound_catalog` → `tool_mapping.sound_catalog` → `tools/sound-asset-catalog.py` (`manage_catalog`)
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `action_mapping.code_execute` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: agentcard.yaml의 persona 존재하므로:
   "당신은 주디입니다. 답변 시 별명 '주디'를 표시하세요. Visionary Leader, Audio-Visual Specialist. 사운드 전문가 관점에서 게임의 감정적 몰입을 설계합니다. 메이저 게임사 사운드 팀장(6년), 배경음악/효과음 사운드 엔지니어링 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:sound-director:sound-director", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 사운드 기획 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| BGM/SFX 상세화 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 에셋 카탈로그 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 참조 및 사운드 기획 분석 -> Agent: sound-director
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: `resources/references/index.md` Sound Director 섹션 확인 후, 마스터 기획서의 목차를 읽고 사운드 기획 관련 챕터를 분석하여 BGM 6종 상황별 분위기 및 SFX 5종 질감 파악
- **EXPECTED OUTCOME**: BGM 6종 + SFX 5종 현황 요약 및 상세화 방향 도출
- **MUST DO**: 외부문서 3종(unity_audio_system, fmod_unity_guide, interactive_sound_design) 참조하여 기술 연동 방식 병행 검토
- **MUST NOT DO**: 마스터 기획서 사운드 기획 관련 챕터 확인 전 사운드 설계 진행 금지
- **CONTEXT**: `output/planning/master_planning_v*.md` 사운드 기획 관련 챕터, `resources/초기자료/모션이펙트제안서_V0_김주연.md`, `resources/references/external/sound-director/`

### Phase 2: BGM/SFX 상세화 -> Agent: sound-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: BGM 6종 구성 계획 상세화(악기 구성, BPM 범위, 전환 방식) + SFX 5종 질감 상세화(레이어 구성, 길이, 처리 효과)
- **EXPECTED OUTCOME**: BGM 구성 계획서 + SFX 디자인 문서 (각각 상세 테이블 포함)
- **MUST DO**: 카드 드로우/정방향/역방향/천칭기울기/시너지발동 5종 SFX 모두 커버; BGM 6종 전환 방식(FMOD 파라미터 기반) 명시
- **MUST NOT DO**: 기획서에 없는 새로운 사운드 이벤트 임의 추가
- **CONTEXT**: Phase 1 분석 결과, `resources/references/external/sound-director/fmod_unity_guide.md`, `resources/references/external/sound-director/interactive_sound_design.md`

### Phase 3: 에셋 카탈로그 갱신 및 저장 -> Agent: sound-director
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: sound_catalog 도구로 BGM/SFX 에셋 카탈로그 생성/갱신 후 산출물 3종 저장
- **EXPECTED OUTCOME**: `output/design/sound_plan_{YYYYMMDD}.md`, `output/design/sfx_design_{YYYYMMDD}.md`, `output/design/sound_asset_catalog_{YYYYMMDD}.md`
- **MUST DO**: 에셋 카탈로그에 ID, 유형, 파일명, 상태, 담당자 컬럼 모두 포함; 모션이펙트제안서와 사운드-이펙트 싱크 정합성 확인
- **MUST NOT DO**: 미완성 설계를 카탈로그에 "완료" 상태로 등록 금지
- **CONTEXT**: Phase 1~2 결과물, `tools/sound-asset-catalog.py`

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | BGM 6종(메인화면/맵탐색/일반전투/보스전투/사건노드/엔딩) 모두 커버 |
| 2 | SFX 5종(카드드로우/정방향/역방향/천칭기울기/시너지발동) 모두 상세화 |
| 3 | Unity Audio System 및 FMOD 연동 방식 명시 |
| 4 | 모션이펙트제안서(`resources/초기자료/모션이펙트제안서_V0_김주연.md`) 기준 사운드-이펙트 싱크 검증 |
| 5 | 산출물은 `output/design/`에 저장 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 코드 실행 (`Bash` 도구 사용 금지) |
| 2 | 마스터 기획서 사운드 기획 챕터에 없는 새로운 사운드 이벤트 임의 추가 |
| 3 | VFX-SFX 연동 구현 직접 수행 — vfx-artist에 핸드오프 |
| 4 | 사운드 에셋 코드 연동 구현 직접 수행 — programmer에 핸드오프 |
| 5 | 미완성 설계를 카탈로그에 "완료" 상태로 등록 |

## 완료 조건

- [ ] 마스터 기획서 사운드 기획 관련 챕터 분석 완료
- [ ] BGM 6종 구성 계획 상세화 완료
- [ ] SFX 5종 질감 설계 완료
- [ ] 사운드 에셋 카탈로그 생성/갱신 완료
- [ ] 산출물 3종 `output/design/`에 저장 완료

## 검증 프로토콜

1. 에이전트 FQN `arcana:sound-director:sound-director` 정확성 확인
2. BGM 6종 모두 커버되었는지 확인
3. SFX 5종 모두 커버되었는지 확인
4. 에셋 카탈로그 필수 컬럼(ID, 유형, 파일명, 상태, 담당자) 존재 여부 확인
5. 모션이펙트제안서와 사운드-이펙트 싱크 정합성 확인

## 상태 정리

- 완료 시 임시 분석 데이터 정리
- 최종 산출물 3종만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 BGM/SFX 설계 내용은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:sound-director:sound-director`)
- [ ] runtime-mapping.yaml 참조하여 tier(MEDIUM) → 모델(claude-sonnet-4-6) 매핑이 올바른가
- [ ] forbidden_actions(code_execute → Bash 제외) 구체화가 올바른가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(-> Agent:)에 5항목(TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT)이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로(`output/design/`)가 명확한가
