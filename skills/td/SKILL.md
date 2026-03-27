---
name: td
description: 기술 아키텍처, 렌더링 파이프라인 설계, Spine-Unity 연동 오케스트레이션
type: orchestrator
user-invocable: true
---

# TD

[TD 스킬 활성화]

## 목표

Unity URP 2D + Spine + Addressables 기반 기술 스택을 확정하고,
렌더링 파이프라인·아트-프로그래밍 파이프라인·성능 최적화 기준을 산출물로 문서화하여
전체 개발팀이 기술 표준 위에서 효율적으로 협업할 수 있도록 함.

## 활성화 조건

- 사용자가 `/arcana:td` 호출 시
- "기술", "엔진", "파이프라인", "렌더링", "성능 최적화", "Spine 연동", "Addressables", "드로우콜", "GC", "직렬화" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| tech-director | `arcana:tech-director:tech-director` |

### 프롬프트 조립 절차

1. `agents/tech-director/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `tier_mapping.default.HIGH` → `claude-opus-4-6`
   - **툴 구체화**:
     - `doc_search` → `tool_mapping.doc_search` → context7 MCP (query-docs, resolve-library-id)
     - `art_pipeline` → `tool_mapping.art_pipeline` → `tools/art-pipeline-guide.py`
   - **금지액션 구체화**: `forbidden_actions: []` → 제외 도구 없음
   - **최종 도구** = context7 MCP + art-pipeline-guide.py (전체 허용)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 우디입니다. 답변 시 별명 '우디'를 표시하세요. Problem Solver, Pipeline Architect, Optimization Expert, Bridge-Builder, Technical Specialist. 그래픽 엔진 최적화 및 아트-프로그래밍 간 기술적 가교 역할 수행 8년, 렌더링 파이프라인 설계 전문가."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:tech-director:tech-director", model="claude-opus-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 단계 | 활용 스킬 | 효과 |
|----------------|----------|------|
| 기술 스택 분석 | `/oh-my-claudecode:analyze` | 체계적 기술 분석 절차 |
| 파이프라인 설계 | `ulw` 매직 키워드 | 병렬 실행 + 완료 보장 |
| 산출물 검증 | `/oh-my-claudecode:ultraqa` | QA 순환 검증 |

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: 기술 기획 분석 → Agent: tech-director
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: `output/planning/master_planning_v*.md` 목차를 읽고 기술 기획 관련 챕터를 완독 후 기술 요구사항 추출
- **EXPECTED OUTCOME**: 기술 요구사항 목록 (렌더링 품질, 성능 목표, 플랫폼 타겟)
- **MUST DO**: 게임 시스템, 렌더링, Spine 연동 관련 챕터 교차 참조
- **MUST NOT DO**: 기획서 분석 전 기술 결정 금지
- **CONTEXT**: `output/planning/master_planning_v*.md`

### Phase 2: 기술 스택 확정 → Agent: tech-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: Unity URP 2D + Spine + Addressables 기술 스택 상세 확정 및 문서화
- **EXPECTED OUTCOME**: 기술 스택 문서 (버전, 패키지, 설정 기준 포함)
- **MUST DO**: doc_search로 Unity 2D + URP 2D Renderer 공식 문서 참조, 버전 호환성 확인
- **MUST NOT DO**: 공식 문서 미확인 상태에서 버전 임의 지정 금지
- **CONTEXT**: Phase 1 기술 요구사항, `resources/references/external/tech-director/`

### Phase 3: 렌더링 파이프라인 설계 → Agent: tech-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 배경/캐릭터/UI/이펙트 4개 레이어 렌더링 파이프라인 상세 설계
- **EXPECTED OUTCOME**: 렌더링 파이프라인 설계서 (레이어 구성, 정렬 기준, URP 2D Light 설정)
- **MUST DO**: art_pipeline 도구로 레이어 가이드 생성, 아트 팀 납품 규격 포함
- **MUST NOT DO**: 아트 팀이 이해할 수 없는 기술 용어만으로 문서 작성 금지
- **CONTEXT**: Phase 2 기술 스택 문서

### Phase 4: Spine-Unity 통합 → Agent: tech-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: Spine ↔ Unity 연동 파이프라인 표준 문서화
- **EXPECTED OUTCOME**: Spine 익스포트 설정 기준 + SkeletonAnimation 설정 기준 + 트랙/이벤트 활용 가이드
- **MUST DO**: doc_search로 Spine-Unity 런타임 공식 문서 참조, art_pipeline 도구 활용
- **MUST NOT DO**: 애니메이터 팀과 협의 없이 Spine 파일 포맷 임의 결정 금지
- **CONTEXT**: Phase 3 렌더링 파이프라인, `resources/초기자료/연출컨셉문서_V1_이채연.md`

### Phase 5: Addressables 에셋 관리 설계 → Agent: tech-director
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: Addressables 에셋 그룹 구조, 로딩 전략, 메모리 해제 규칙 설계
- **EXPECTED OUTCOME**: Addressables 에셋 관리 가이드 (그룹 구조, 로딩/해제 시점, DLC 대비 구조)
- **MUST DO**: doc_search로 Unity Addressables 공식 문서 참조
- **MUST NOT DO**: 메모리 해제 규칙 없이 로딩 전략만 설계 금지
- **CONTEXT**: Phase 2 기술 스택 문서

### Phase 6: 성능 최적화 및 데이터 구조 설계 → Agent: tech-director
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 성능 최적화 기준(드로우콜 목표, 풀링 대상, GC 최소화) + JSON 직렬화 결정 + 데이터 구조 스키마 작성
- **EXPECTED OUTCOME**: 성능 최적화 기준서 + 데이터 구조 스키마 + 최종 기술 문서 (`output/build/` 저장)
- **MUST DO**: 드로우콜 목표 수치 명시, JSON/CSV 포맷 예시 포함
- **MUST NOT DO**: 수치 없이 "최적화 필요" 수준의 추상적 기준만 작성 금지
- **CONTEXT**: Phase 1~5 전체 산출물

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 기술 결정은 공식 문서(doc_search) 근거 필수 |
| 2 | 렌더링 파이프라인은 아트 팀이 이해할 수 있는 형태로 문서화 |
| 3 | 성능 목표는 반드시 수치로 명시 (드로우콜, 프레임레이트, 메모리) |
| 4 | 산출물은 `output/build/`에 저장 |
| 5 | Spine 파이프라인 가이드는 animator 팀과 공유 가능한 수준으로 작성 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 공식 문서 미확인 상태에서 버전 및 설정값 임의 지정 |
| 2 | 기획서 요구사항 분석 전 기술 스택 결정 |
| 3 | 아트 팀이 이해할 수 없는 기술 용어만으로 파이프라인 문서 작성 |
| 4 | 수치 없는 추상적 성능 최적화 기준 작성 |

## 완료 조건

- [ ] 기술 스택 확정 문서 작성 완료 (버전, 패키지, 설정 기준 포함)
- [ ] 렌더링 파이프라인 설계서 완료 (4개 레이어 상세 설명)
- [ ] Spine-Unity 통합 가이드 완료 (익스포트 기준 + 컴포넌트 설정 + 트랙/이벤트)
- [ ] Addressables 에셋 관리 가이드 완료
- [ ] 성능 최적화 기준서 완료 (수치 포함)
- [ ] 데이터 구조 스키마 완료 (JSON 예시 포함)
- [ ] 전 산출물 `output/build/`에 저장 완료

## 검증 프로토콜

1. 기술 스택 버전이 상호 호환성을 갖추는지 확인 (Unity ↔ Spine-Unity ↔ Addressables)
2. 렌더링 파이프라인이 4개 레이어를 모두 포함하는지 확인
3. 성능 목표 수치가 명시되어 있는지 확인
4. 데이터 스키마가 기획서 수치 필드를 빠짐없이 포함하는지 확인

## 상태 정리

- 완료 시 중간 분석 메모 정리
- 최종 기술 문서만 `output/build/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 Phase 산출물은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 산출물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가 (`arcana:tech-director:tech-director`)
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (HIGH → claude-opus-4-6)
- [ ] forbidden_actions가 빈 배열로 올바르게 처리되었는가
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 `output/build/`로 명확한가
