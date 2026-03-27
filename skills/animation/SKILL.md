---
name: animation
description: 전투 모션 스펙, 프레임 가이드(24fps), 컷신 시퀀스 오케스트레이션
type: orchestrator
user-invocable: true
---

# Animation

[Animation 스킬 활성화]

## 목표

2D 캐릭터 애니메이션 스펙 기획을 오케스트레이션하여,
전투 모션의 타이밍/무게감 기준과 컷신 시퀀스를 작성하고
모션 듀오의 Spine 기반 고퀄리티 액션 연출을 지원함.

## 활성화 조건

- 사용자가 `/arcana:animation` 호출 시
- "전투 모션", "애니메이션", "프레임 가이드", "컷신", "Spine", "모션 스펙" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| animator | `arcana:animator:animator` |

### 프롬프트 조립 절차

1. `agents/animator/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `claude-sonnet-4-6`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 모션 듀오입니다. 답변 시 별명 '모션 듀오'를 표시하세요. Dynamic Movement Expert, Frame-by-Frame Perfectionist, Timing Specialist, Fluid Action Pursuer. 스파인(Spine) 및 프레임 기반 고퀄리티 캐릭터 액션 연출 전문, 24프레임 LD 컷신 애니메이션 제작 숙련."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:animator:animator", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 기획 분석 → Agent: animator
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서의 목차를 읽고 애니메이션/연출 기획 및 캐릭터 스킬 모션 관련 챕터를 분석하여 애니메이션 현황 파악
- **EXPECTED OUTCOME**: 캐릭터별 모션 요구사항 정리 (정방향/역방향/궁극기/기본동작)
- **MUST DO**: 4개 플레이어블 캐릭터(포춘/저스티스/매지션/더풀) 모든 모션 목록 수집
- **MUST NOT DO**: 기획서에 없는 새로운 캐릭터 모션 임의 추가
- **CONTEXT**: `output/planning/master_planning_v*.md` 애니메이션/연출 기획 및 캐릭터 스킬 모션 관련 챕터

### Phase 2: 모션 스펙 작성 → Agent: animator
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 캐릭터별 전투 모션 스펙 문서 작성 (24fps 기준, Spine 트랙 구성 포함)
- **EXPECTED OUTCOME**: 모션 스펙 문서 (캐릭터 x 모션유형 전체 커버), 기본 동작 목록
- **MUST DO**: 24fps 기준 프레임 수 + Anticipation/Action/Follow-through 타이밍 분해 필수
- **MUST NOT DO**: 프레임 수 미명시 모션 스펙 작성 금지
- **CONTEXT**: Phase 1 분석 결과, `resources/references/index.md` Animator 섹션

### Phase 3: 컷신 및 프레임 가이드 → Agent: animator
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 컷신 시퀀스 기획(프롤로그/스테이지전환/엔딩) + 프레임 가이드 작성 + `output/design/` 저장
- **EXPECTED OUTCOME**: 컷신 시퀀스 기획서, 프레임 가이드 문서, 산출물 저장 완료
- **MUST DO**: 모든 컷신은 씬번호/카메라구도/등장캐릭터/동작/재생시간 5항목 포함
- **MUST NOT DO**: 미검증 타이밍 수치를 최종 문서에 포함 금지
- **CONTEXT**: Phase 2 모션 스펙 결과

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 모션 스펙은 24fps 기준 프레임 수 명시 필수 |
| 2 | 정방향/역방향 모션은 시각적 대비를 명확히 기술 |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | Spine 트랙 구성은 Unity Mecanim 상태 머신 호환성 고려 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 기획서에 없는 캐릭터/모션 임의 추가 |
| 2 | 프레임 수 미명시 모션 스펙 작성 |
| 3 | 코드 실행(Bash) 수행 |

## 완료 조건

- [ ] 4개 플레이어블 캐릭터 전투 모션 스펙 완성 (정방향/역방향/궁극기)
- [ ] 기본 동작 모션 목록 완성 (Idle/이동/피격/전투불능)
- [ ] 컷신 시퀀스 기획서 완성
- [ ] 프레임 가이드 문서 완성
- [ ] 산출물 `output/design/`에 저장 완료

## 검증 프로토콜

1. 모든 캐릭터 모션에 24fps 기준 프레임 수가 명시되어 있는지 확인
2. 정방향/역방향 이펙트 연동 포인트(Spine 이벤트)가 VFX 스펙과 일치하는지 확인
3. 컷신 시퀀스가 4스테이지 게임 흐름과 일관성 있는지 확인

## 상태 정리

- 완료 시 임시 분석 노트 정리
- 최종 모션 스펙/프레임 가이드/컷신 기획서만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 작성된 모션 스펙은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (MEDIUM → claude-sonnet-4-6)
- [ ] forbidden_actions 구체화가 올바른가 (code_execute → Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 명확한가 (output/design/)
