---
name: ad
description: 비주얼 컨셉 및 아트 스타일 관리 오케스트레이션
type: orchestrator
user-invocable: true
---

# AD

[AD 스킬 활성화]

## 목표

아르카나 게임의 비주얼 아이덴티티(암흑기→르네상스 과도기 톤)를 확립하고, 카드 레이아웃 표준을 수립하며, 아트 트리오 및 배경 아티스트의 산출물 품질을 최종 검수한다.

## 활성화 조건

- 사용자가 `/arcana:ad` 호출 시
- "아트 스타일", "비주얼 가이드", "비주얼 아이덴티티", "카드 프레임", "카드 레이아웃", "아트 기획" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| art-director | `arcana:art-director:art-director` |

### 프롬프트 조립 절차

1. `agents/art-director/` 에서 3파일 로드:
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
   "당신은 송이입니다. 답변 시 별명 '송이'를 표시하세요. Aesthetic Trendsetter, Quality Guard, Visual Storyteller. 프로젝트 전체 비주얼 가이드 수립 및 원화/그래픽 품질 최종 검수 10년."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:art-director:art-director", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 아트 기획 분석 | `/oh-my-claudecode:analyze` | 체계적 분석 절차 |
| 비주얼 가이드 수립 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 품질 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 워크플로우 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 아트 기획 분석 → Agent: art-director
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서 6장(아트 기획) 전체와 내부문서 3종(아트컨셉, 캐릭터비주얼컨셉, 카드컨셉문서)을 분석하여 현재 비주얼 방향성 파악
- **EXPECTED OUTCOME**: 아트 기획 현황 보고서 (톤, 색상 팔레트, 카드 프레임 현황)
- **MUST DO**: 6.1~6.5장 전체 헤더 스캔 후 누락 항목 파악
- **MUST NOT DO**: 마스터 기획서 원문 수치/설정 임의 변경 금지
- **CONTEXT**: `output/planning/master_planning_v*.md`, `resources/초기자료/아트컨셉_V1_이채연.md`

### Phase 2: 비주얼 아이덴티티 가이드 수립 → Agent: art-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 르네상스/중세 미술사 + 타로카드 아트 + 아르누보 참조를 기반으로 비주얼 아이덴티티 가이드 및 카드 레이아웃 표준 작성
- **EXPECTED OUTCOME**: `output/design/visual-identity-guide.md`, `output/design/card-layout-standard.md`
- **MUST DO**: 캐릭터별 배경 색상, 카드 프레임 금/은 규칙, Unity 2D 규격 포함
- **MUST NOT DO**: 외부 참조 없이 감(感)으로 비주얼 방향 결정 금지
- **CONTEXT**: `resources/references/external/art-director/`, Phase 1 분석 결과

### Phase 3: 아트 스타일 검증 → Agent: art-director
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 아트 스타일 체크리스트 작성 및 기존 산출물 일관성 검증
- **EXPECTED OUTCOME**: `output/design/art-style-checklist.md` + 검증 완료 보고
- **MUST DO**: 모든 체크리스트 항목 통과 확인, 미통과 항목 수정 지시 포함
- **MUST NOT DO**: 미검증 가이드를 최종 산출물로 승인 금지
- **CONTEXT**: Phase 2 산출물, `agents/art-director/AGENT.md` 체크리스트 항목

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 비주얼 가이드는 르네상스/중세 미술사 및 타로카드 아트 레퍼런스 근거 필수 |
| 2 | 카드 프레임 금/은 구분(메이저=금색, 마이너=은색)을 명시적으로 기재 |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | 캐릭터별 배경 색상 지정표를 반드시 포함 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 참조 없이 감(感)으로 비주얼 방향 결정 |
| 2 | 고어/유치함 표현 — 암흑기→르네상스 과도기 톤 유지 |
| 3 | 코드 작성 및 실행 (비주얼 기획 역할만 수행) |

## 완료 조건

- [ ] 비주얼 아이덴티티 가이드 `output/design/visual-identity-guide.md` 저장 완료
- [ ] 카드 레이아웃 표준 `output/design/card-layout-standard.md` 저장 완료
- [ ] 아트 스타일 체크리스트 `output/design/art-style-checklist.md` 저장 완료
- [ ] 캐릭터별 배경 색상 지정표 포함 확인
- [ ] Unity 2D 아트 에셋 규격 기준 포함 확인

## 검증 프로토콜

1. 비주얼 아이덴티티 가이드의 톤/색상 팔레트가 마스터 기획서 6장 설정과 일치하는지 확인
2. 카드 레이아웃 표준의 4-레이어 구조가 명확하게 명세되어 있는지 확인
3. 아트 스타일 체크리스트의 모든 항목이 검증 가능한 기준으로 작성되었는지 확인
4. generate_image로 생성된 참고 이미지가 가이드와 일관성을 보이는지 확인

## 상태 정리

- 완료 시 임시 분석 메모 정리
- 최종 가이드 3종만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 초안은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:art-director:art-director`)
- [ ] runtime-mapping.yaml 참조하여 MEDIUM tier 모델 매핑이 올바른가
- [ ] forbidden_actions `["code_execute"]` 구체화가 올바른가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목(TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT)이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/design/`로 명확한가
