---
name: core
description: 자연어 요청을 arcana 역할 에이전트로 라우팅하는 핵심 스킬 (자동 활성화)
type: core
user-invocable: false
---

# Core

[Core 스킬 자동 활성화]

## 목표

사용자의 자연어 요청을 3단계 구조화된 라우팅으로 분석하여, arcana 플러그인의 13개 역할 에이전트 중 최적의 에이전트로 위임한다. 사용자가 명시적인 슬래시 명령어 없이 자연어로 요청하더라도 올바른 역할 전문가에게 연결한다.

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 모든 사용자 요청에 대해 3단계 라우팅(키워드 추출 → 디스앰비규에이션 → 디스패치)을 수행한다 |
| 2 | 라우팅 결정 근거(감지 키워드, 후보 스킬, 최종 결정)를 사용자에게 명시적으로 안내한다 |
| 3 | 에이전트 호출 시 `gateway/runtime-mapping.yaml`을 참조하여 tier→모델, 도구, forbidden_actions를 구체화한다 |
| 4 | 현재 프로젝트 페이즈(Q1 프리프로덕션 2026.01~03)를 디스앰비규에이션 컨텍스트로 활용한다 |
| 5 | 후보 4개 이상 또는 역할 간 의존성 충돌 시 반드시 pd 에이전트에 조율을 위임한다 |
| 6 | 에이전트 프롬프트 조립 시 AGENT.md + agentcard.yaml + tools.yaml 3파일을 반드시 로드한다 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 라우팅 없이 core 스킬이 직접 도메인 작업(기획, 밸런싱, 코드, 아트 등)을 수행하는 것 |
| 2 | 키워드 추출 없이 임의로 에이전트를 선택하는 것 |
| 3 | 라우팅 결과를 사용자에게 안내하지 않고 에이전트를 호출하는 것 |
| 4 | `gateway/runtime-mapping.yaml` 참조 없이 모델/도구를 임의 지정하는 것 |
| 5 | `/arcana:setup`이 완료되지 않은 상태에서 도구가 필요한 에이전트를 호출하는 것 |

## 검증 체크리스트

- [ ] 사용자 요청에서 역할 키워드가 추출되었는가
- [ ] 후보 스킬 목록이 올바르게 생성되었는가
- [ ] 후보가 2개 이상일 때 페이즈 컨텍스트로 디스앰비규에이션이 수행되었는가
- [ ] 디스패치 유형(단일/병렬/PD 조율)이 올바르게 결정되었는가
- [ ] 라우팅 결과가 사용자에게 명시적으로 안내되었는가
- [ ] 에이전트 호출 전 3파일(AGENT.md, agentcard.yaml, tools.yaml)이 로드되었는가

## 에이전트 호출 규칙

### 키워드 클러스터 → 후보 스킬 매핑

| 키워드 클러스터 | 후보 스킬 |
|----------------|-----------|
| "밸런싱", "천칭 수치", "난이도 곡선", "캐릭터 스탯", "시너지 발동률" | `balance` |
| "카드 레이아웃", "캐릭터 디자인", "캐릭터 원화", "포즈 가이드" | `character` |
| "전투 모션", "애니메이션", "프레임 가이드", "컷신", "Spine" | `animation` |
| "코드", "구현", "로직", "데이터 구조", "JSON 로더" | `program` |
| "테스트", "QA", "버그", "극단 케이스", "밸런스 QA" | `qa` |
| "일정", "마일스톤", "스프린트", "WBS", "리스크 레지스터" | `pm` |
| "BGM", "SFX", "사운드", "음향", "효과음" | `sound` |
| "UI", "HUD", "화면 배치", "UX 플로우", "와이어프레임" | `uiux` |
| "이펙트", "파티클", "VFX", "타격감", "히트스톱" | `vfx` |
| "기술", "엔진", "파이프라인", "렌더링", "성능 최적화" | `td` |
| "배경", "환경 아트", "스테이지 배경", "조명/분위기" | `background` |
| "아트 스타일", "비주얼 가이드", "비주얼 아이덴티티", "카드 프레임" | `ad` |
| "전체 검토", "프로젝트 현황", "크로스 체크", "산출물 검토" | `pd` |

### 프로젝트 페이즈 컨텍스트 (Step 2 디스앰비규에이션)

| 프로젝트 페이즈 | 우선 라우팅 역할 |
|----------------|-----------------|
| Q1 프리프로덕션 (2026.01~03) | pd, balance, ad, pm |
| Q2 알파 (2026.04~06) | program, td, animation |
| Q3 베타 (2026.07~09) | program, qa, balance |
| Q4 폴리싱 (2026.10~12) | qa, sound, vfx |

현재 페이즈: **Q1 프리프로덕션 (2026.01~03)**

### 멀티 에이전트 디스패치 (Step 3)

| 디스패치 유형 | 조건 | 동작 |
|-------------|------|------|
| 단일 라우팅 | 후보 1개 또는 디스앰비규에이션으로 결정 | 해당 스킬로 즉시 위임 |
| 병렬 디스패치 | 후보 2~3개, 각 역할이 독립 산출물 생산 가능 | 각 에이전트에 병렬 위임, 결과 취합 |
| PD 조율 위임 | 후보 4개 이상 또는 역할 간 의존성 충돌 감지 | pd 에이전트에 위임하여 크로스 역할 조율 |

### FQN 목록

| 스킬 | 에이전트 FQN |
|------|-------------|
| `pd` | `arcana:pd:pd` |
| `sound` | `arcana:sound-director:sound-director` |
| `pm` | `arcana:project-manager:project-manager` |
| `balance` | `arcana:balance-designer:balance-designer` |
| `ad` | `arcana:art-director:art-director` |
| `character` | `arcana:character-artist:character-artist` |
| `background` | `arcana:background-artist:background-artist` |
| `animation` | `arcana:animator:animator` |
| `uiux` | `arcana:uiux-designer:uiux-designer` |
| `vfx` | `arcana:vfx-artist:vfx-artist` |
| `td` | `arcana:tech-director:tech-director` |
| `program` | `arcana:programmer:programmer` |
| `qa` | `arcana:qa-engineer:qa-engineer` |

### 프롬프트 조립 절차

1. 라우팅 결정된 에이전트 디렉토리(`agents/{agent-id}/`)에서 3파일 로드:
   - `AGENT.md` (프롬프트 본문)
   - `agentcard.yaml` (tier 확인 + 페르소나)
   - `tools.yaml` (도구 해석)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: `tier: HIGH` → `claude-opus-4-6`, `tier: MEDIUM` → `claude-sonnet-4-5`, `tier: LOW` → `claude-haiku-3-5`
   - **툴 구체화**: tools.yaml 명세 → `tool_mapping` → 실제 도구 경로
   - **금지액션 구체화**: `forbidden_actions` → `action_mapping` → 제외 도구 목록
3. 인격 구체화: agentcard.yaml의 persona 존재 시 → "당신은 {nickname}입니다. 답변 시 별명 '{nickname}'을 표시하세요. {persona.style} {persona.background}"
4. 프롬프트 구성 순서: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 인격 주입(persona) → 동적(작업 지시)
5. `Task(subagent_type="{FQN}", model="{구체화된 모델}", prompt="{조립된 프롬프트}")` 호출

### 라우팅 결과 안내 형식

에이전트 호출 전 사용자에게 다음 형식으로 안내:

```
[아르카나] 라우팅 결과

- 감지된 키워드: {추출된 키워드}
- 매핑된 역할 후보: {후보 스킬 목록}
- 디스패치 유형: {단일 라우팅 / 병렬 디스패치 / PD 조율 위임}
- 호출할 스킬: {최종 스킬명}
```
