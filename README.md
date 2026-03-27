# Arcana — 게임 개발 AI 어시스턴트 플러그인

아르카나(Arcana) 2D 로그라이트 턴제 전략 카드 게임 개발의 전 과정을 지원하는 DMAP 플러그인.
13개 역할에 대해 전용 에이전트와 스킬을 제공합니다.

## 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | arcana |
| 버전 | 1.0.0 |
| 게임 엔진 | Unity (URP 2D Renderer) |
| 플랫폼 | PC (Steam) |
| 팀 | Team Light Life (12명, 13개 역할) |

## 설치

```bash
/arcana:setup
```

setup 스킬이 자동으로 MCP 서버(context7)와 커스텀 도구를 설치합니다.

## 업그레이드

최신 버전의 플러그인으로 업그레이드:

```bash
/arcana:setup
```

## 사용법

### 역할별 스킬

| 명령 | 역할 | 담당자 | 설명 |
|------|------|--------|------|
| `/arcana:pd` | PD | 주디 | 프로젝트 총괄, 크로스 역할 조율 |
| `/arcana:sound` | Sound Director | 주디 | BGM/SFX 설계, 사운드 에셋 관리 |
| `/arcana:pm` | PM | 체리 | 일정 관리, 시스템 기획 상세화 |
| `/arcana:balance` | Balance Designer | 보스 | 세계관 검증, 밸런싱 시뮬레이션 |
| `/arcana:ad` | AD | 송이 | 비주얼 컨셉, 아트 스타일 관리 |
| `/arcana:character` | Character Artist | 아트 트리오 | 캐릭터 디자인, 카드 일러스트 |
| `/arcana:background` | Background Artist | 령 | 배경 컨셉, 조명/분위기 가이드 |
| `/arcana:animation` | 2D Animator | 모션 듀오 | 전투 모션 스펙, 컷신 시퀀스 |
| `/arcana:uiux` | UIUX Designer | 밍키 | HUD 설계, UX 플로우 |
| `/arcana:vfx` | VFX Artist | 니니 | 이펙트 스펙, 타격감 연출 |
| `/arcana:td` | TD | 우디 | 기술 아키텍처, 파이프라인 |
| `/arcana:program` | Programmer | 진 | 게임 로직 구현, 데이터 구조 |
| `/arcana:qa` | QA | 보니 | 테스트 케이스, 버그 추적 |

### 기본 스킬

| 명령 | 설명 |
|------|------|
| `/arcana:setup` | 플러그인 초기 설정 |
| `/arcana:help` | 사용법 안내 |
| `/arcana:add-ext-skill` | 외부호출 스킬 추가 |
| `/arcana:remove-ext-skill` | 외부호출 스킬 제거 |

### 자동 라우팅

자연어로 요청하면 core 스킬이 자동으로 적절한 역할 에이전트를 선택합니다:

- "밸런싱 시뮬레이션 해줘" → balance-designer
- "카드 레이아웃 검증" → character-artist
- "전투 모션 스펙 작성" → animator
- "천칭 시스템 코드 구현" → programmer

### 산출물 디렉토리

```
output/
├── planning/    ← 기획 산출물 (PD, PM, Balance Designer)
├── design/      ← 설계 산출물 (AD, Character, Background, Animator, UIUX, VFX, Sound)
├── build/       ← 구현 산출물 (Programmer, TD)
└── deploy/      ← 배포/QA 산출물 (QA Engineer)
```

## 참조 문서

모든 참조 문서는 `resources/references/reference-index.md`에 인덱싱되어 있습니다.

| 유형 | 경로 | 수량 |
|------|------|------|
| 마스터 기획서 | `output/planning/master_planning_v*.md` | 최신 버전 |
| 내부 기획 자료 | `resources/초기자료/` | 23개 |
| 외부 참조 문서 | `resources/references/{역할}/` | 53개 |

## 요구사항

- Claude Code CLI
- Node.js 18+ (context7 MCP 서버)
- Python 3.9+ (커스텀 도구)

## 라이선스

MIT License — Team Light Life
