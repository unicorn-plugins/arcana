---
name: uiux
description: HUD 설계, UX 플로우, 파티/증강 UI, 접근성, 튜토리얼 UX 오케스트레이션
type: orchestrator
user-invocable: true
---

# UIUX

[UIUX 스킬 활성화]

## 목표

게임의 전체 UX 플로우와 인터페이스 컴포넌트 스펙을 오케스트레이션하여,
HUD/파티/증강/튜토리얼 UI를 설계하고 밍키의 유저 중심 설계 원칙으로
최적의 게임 인터페이스를 기획함.

## 활성화 조건

- 사용자가 `/arcana:uiux` 호출 시
- "UI", "HUD", "화면 배치", "UX 플로우", "와이어프레임", "인터페이스", "튜토리얼 UI" 키워드 감지 시

## 에이전트 호출 규칙

### FQN 목록

| 에이전트 | FQN |
|----------|-----|
| uiux-designer | `arcana:uiux-designer:uiux-designer` |

### 프롬프트 조립 절차

1. `agents/uiux-designer/` 에서 3파일 로드:
   - AGENT.md (프롬프트 본문)
   - agentcard.yaml (tier 확인 + 프롬프트 첨부)
   - tools.yaml (도구 해석 + 프롬프트 첨부)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: MEDIUM` → `claude-sonnet-4-6`
   - **툴 구체화**: tools.yaml의 `diagram_validate` → `tool_mapping.diagram_validate` → `tools/check-mermaid-bridge.py`
   - **금지액션 구체화**: `forbidden_actions: ["code_execute"]` → `["Bash"]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 3파일을 합쳐 하나의 프롬프트로 조립
4. **인격 구체화**: "당신은 밍키입니다. 답변 시 별명 '밍키'를 표시하세요. User-Centric Designer, Information Architect, Intuitive Interaction Maker, Interface Visualizer. 게임 편의성 향상을 위한 최적의 인터페이스 레이아웃 및 UX 플로우 설계, 모바일 UI 시스템 구축 4년."
5. **프롬프트 구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 사용자 메시지(동적)
6. `Task(subagent_type="arcana:uiux-designer:uiux-designer", model="claude-sonnet-4-6", prompt=조립된 프롬프트 + 사용자 메시지)` 호출

## 워크플로우

> 아래 워크플로우는 에이전트가 Step 0에서 **모드 B**로 판단한 경우에만 실행된다.
> 모드 A(참조 응답)인 경우, 에이전트가 참조 문서를 기반으로 직접 답변한다.

### Phase 1: UI/UX 기획 분석 → Agent: uiux-designer
이 Phase는 `/oh-my-claudecode:analyze`를 활용하여 수행.
- **TASK**: 마스터 기획서 7장(UI/UX 기획) + 3.4장(전투 HUD) + 3.7장(파티 UI) + 3.5.2장(증강 UI) 분석
- **EXPECTED OUTCOME**: UI 요구사항 정리 (HUD 구성 요소, 파티/증강 UI 구조, 튜토리얼 흐름)
- **MUST DO**: 기획서에 명시된 모든 UI 컴포넌트 목록 수집
- **MUST NOT DO**: 기획서에 없는 UI 요소 임의 추가
- **CONTEXT**: `output/planning/master_planning_v*.md` 7장, 3.4장, 3.7장, 3.5.2장

### Phase 2: UX 플로우 및 HUD 설계 → Agent: uiux-designer
이 Phase는 `ulw` 매직 키워드를 활용하여 수행.
- **TASK**: 전체 UX 플로우 다이어그램 작성 + diagram_validate 검증 + HUD/파티/증강 UI 와이어프레임 작성
- **EXPECTED OUTCOME**: 검증된 Mermaid UX 플로우, HUD 레이아웃 스펙, 파티/증강 UI 스펙
- **MUST DO**: diagram_validate로 Mermaid 문법 검증 필수. 천칭 UI(아스트롤라베) 반드시 포함
- **MUST NOT DO**: 미검증 Mermaid 다이어그램을 최종 산출물에 포함 금지
- **CONTEXT**: Phase 1 분석 결과, `resources/references/index.md` UIUX Designer 섹션

### Phase 3: 접근성 및 튜토리얼 → Agent: uiux-designer
이 Phase는 `/oh-my-claudecode:ultraqa`를 활용하여 수행.
- **TASK**: 접근성 가이드 기반 색각이상/폰트 가독성 검증 + 튜토리얼 UX 설계 + `output/design/` 저장
- **EXPECTED OUTCOME**: 접근성 검증 체크리스트, 튜토리얼 UX 흐름 문서, 산출물 저장 완료
- **MUST DO**: Hangedman 캐릭터를 튜토리얼 안내 역할로 명시적으로 활용
- **MUST NOT DO**: 접근성 검증 없이 최종 UI 스펙 확정 금지
- **CONTEXT**: Phase 2 설계 결과

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | UX 플로우는 diagram_validate로 반드시 검증 |
| 2 | HUD에 천칭 UI(아스트롤라베) 상단 중앙 배치 필수 |
| 3 | 산출물은 `output/design/`에 저장 |
| 4 | 접근성 가이드 준수 (색각이상/폰트 가독성) |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 미검증 Mermaid 다이어그램 최종 산출물 포함 |
| 2 | 기획서에 없는 UI 요소 임의 추가 |
| 3 | 코드 실행(Bash) 수행 |

## 완료 조건

- [ ] 전체 UX 플로우 다이어그램 작성 및 diagram_validate 검증 완료
- [ ] HUD 와이어프레임 (전투 인터페이스) 완성
- [ ] 파티 설정 UI 스펙 완성
- [ ] 증강 선택 UI 스펙 완성
- [ ] 접근성 검증 체크리스트 완성
- [ ] 튜토리얼 UX 설계 완성
- [ ] 산출물 `output/design/`에 저장 완료

## 검증 프로토콜

1. diagram_validate 결과 오류 없음 확인
2. HUD의 모든 구성 요소(카드 6장/아군HP/적HP/천칭/턴/코스트)가 포함되었는지 확인
3. UX 플로우가 게임 전체 흐름(4스테이지 x 4노드, 윤회/토템 시스템)을 커버하는지 확인
4. 접근성 가이드 체크리스트 통과 여부 확인

## 상태 정리

- 완료 시 임시 분석 노트 정리
- 최종 UX 플로우/HUD 와이어프레임/UI 스펙만 `output/design/`에 보존

## 취소

- `cancelomc` 키워드로 즉시 중단
- 진행 중 작성된 다이어그램/와이어프레임은 임시 저장

## 재개

- 마지막 완료 Phase부터 재개
- 이전 Phase 결과물 참조하여 연속성 유지

## 검증 체크리스트

- [ ] 에이전트 FQN이 정확한가
- [ ] runtime-mapping.yaml 참조하여 tier→모델 매핑이 올바른가 (MEDIUM → claude-sonnet-4-6)
- [ ] diagram_validate 도구 구체화가 올바른가 (tools/check-mermaid-bridge.py)
- [ ] forbidden_actions 구체화가 올바른가 (code_execute → Bash 제외)
- [ ] 모든 Phase에 오케스트레이션 스킬이 명시되어 있는가
- [ ] 위임 마커(→ Agent:)에 5항목이 빠짐없이 포함되어 있는가
- [ ] 산출물 저장 경로가 명확한가 (output/design/)
