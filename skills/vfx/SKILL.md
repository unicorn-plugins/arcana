---
name: vfx
description: 스킬 이펙트 스펙, 파티클 가이드, 타격감 연출 설계 오케스트레이션
type: orchestrator
user-invocable: true
---

# VFX

[VFX 스킬 활성화]

## 목표

Unity Particle System과 VFX Graph 기반 시각 특수효과 스펙을 오케스트레이션하여,
정방향/역방향 스킬 이펙트 대비와 천칭 시각효과를 기획하고
니니의 타격감 극대화 전문성으로 게임 피드백을 설계함.

## 활성화 조건

- 사용자가 `/arcana:vfx` 호출 시
- "이펙트", "파티클", "VFX", "타격감", "히트스톱", "스킬 연출", "시너지 이펙트" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| vfx-artist | `arcana:vfx-artist:vfx-artist` |

### 프롬프트 조립 절차

1. `agents/vfx-artist/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: LOW` → `claude-haiku-4-5`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 니니입니다. 답변 시 별명 '니니'를 표시하세요. Impactful Visualizer, Particle Master, Technical Artist(VFX), Combat Feel Enhancer. 타격감 극대화를 위한 이펙트 파티클 및 스킬 연출 전문, 엔진 기반 특수효과 최적화 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:vfx-artist:vfx-artist", model="claude-haiku-4-5", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: VFX/SFX 분석 → Agent: vfx-artist
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서의 목차를 읽고 VFX 연출 가이드 및 SFX 연동 관련 챕터를 분석하여 이펙트 요구사항 파악
- **EXPECTED OUTCOME**: 스킬 이펙트 목록, 정방향/역방향 시각 특성 기준, SFX 연동 요구사항
- **MUST DO**: VFX 연출 관련 챕터의 모든 이펙트 유형 수집 + SFX 연동 관련 챕터 타이밍 요구사항 포함
- **MUST NOT DO**: 기획서에 없는 새로운 이펙트 시스템 임의 추가
- **CONTEXT**: `output/planning/master_planning_v*.md` VFX 연출 및 SFX 연동 관련 챕터

### Phase 2: 이펙트 스펙 작성 → Agent: vfx-artist
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 정방향/역방향 스킬 이펙트 스펙 + 시너지(크리스탈 공명) + 천칭 시각효과 + 환경 이펙트 작성
- **EXPECTED OUTCOME**: 이펙트 스펙 문서 (모든 이펙트 유형 커버), 파티클 파라미터 가이드
- **MUST DO**: 각 이펙트에 파티클 모듈 구성/색상/지속시간/최대파티클수 4항목 명시
- **MUST NOT DO**: 성능 검토 없이 무제한 파티클 수 설정 금지
- **CONTEXT**: Phase 1 분석 결과, `resources/references/index.md` VFX Artist 섹션

### Phase 3: 타격감 연출 설계 → Agent: vfx-artist
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: Game Feel 기법 기반 타격감 연출(히트스톱/화면흔들림/번쩍임) + URP Post-Processing 기준 설정 + `output/design/` 저장
- **EXPECTED OUTCOME**: 타격감 연출 설계서, URP Post-Processing 설정 기준, 산출물 저장 완료
- **MUST DO**: 히트스톱 프레임 수를 적/아군/보스 구분하여 명시
- **MUST NOT DO**: SFX 연동 타이밍 미검토 상태로 타격감 스펙 확정 금지
- **CONTEXT**: Phase 2 이펙트 스펙 결과

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 정방향/역방향 이펙트의 시각적 대비를 명확히 기술 (색조/형태/움직임) |
| 2 | 각 이펙트에 최대 파티클 수 및 성능 고려사항 포함 |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | 타격감 연출은 히트스톱/화면흔들림/번쩍임 3요소 모두 포함 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 기획서에 없는 이펙트 시스템 임의 추가 |
| 2 | 성능 검토 없이 무제한 파티클 수 설정 |
| 3 | 코드 실행(Bash) 수행 |

## 완료 조건

- [ ] 정방향/역방향 스킬 이펙트 스펙 완성
- [ ] 시너지 발동 이펙트(크리스탈 공명) 스펙 완성
- [ ] 천칭 기울기 상태별 시각효과 스펙 완성
- [ ] 4개 스테이지 환경 이펙트 스펙 완성
- [ ] 타격감 연출 설계서 완성 (히트스톱/화면흔들림/번쩍임)
- [ ] URP Post-Processing 기준 설정 완성
- [ ] 산출물 `output/design/`에 저장 완료

## 검증 프로토콜

1. 정방향/역방향 이펙트 시각적 대비가 명확히 기술되었는지 확인
2. 천칭 상태 3단계(순응/저항/중립)가 이펙트와 1:1 매핑되는지 확인
3. 타격감 스펙의 SFX 연동 타이밍이 사운드 디렉터 가이드와 정합성 있는지 확인
4. 모든 이펙트에 성능 고려사항(최대 파티클 수)이 포함되었는지 확인

## 상태 정리

- 완료 시 임시 분석 노트 정리
- 최종 이펙트 스펙/파티클 가이드/타격감 연출 설계서만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 작성된 이펙트 스펙은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (LOW → claude-haiku-4-5)
- [ ] forbidden_actions 구체화가 올바른가 (code_execute → Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 명확한가 (output/design/)
