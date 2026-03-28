# Arcana — 게임 개발 AI 어시스턴트 플러그인

아르카나(Arcana) 2D 로그라이트 턴제 전략 카드 게임 개발의 전 과정을 지원하는 DMAP 플러그인.
13개 역할에 대해 전용 에이전트와 스킬을 제공합니다.

## 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | arcana |
| 게임 엔진 | Unity (URP 2D Renderer) |
| 플랫폼 | PC (Steam) |
| 팀 | Team Light Life (12명, 13개 역할) |

[마스터 제안서 ](output/planning/master-planning-infographic.html)

## 팀원 역량
[팀원역량](resources/guides/capabilities.md)
  
## 사용법

### 팀원 호출
| 스킬 | 호출명령 |
|------|---------|
| 프로젝트 디렉터 | `@주디`, `@주연`, `@pd` |
| 프로젝트 매니저 | `@체리`, `@채연`, `@pm` |
| 밸런싱 기획 | `@보스`, `@보성`, `@bd` |
| 캐릭터 아트 | `@아트트리오`, `@유빈`, `@ca` |
| 아트 디렉터 | `@송이`, `@송희`, `@ad` |
| 배경 아트 | `@령`, `@예령`, `@ba` |
| 애니메이션 | `@모션듀오`, `@가현`, `@animator` |
| UI/UX | `@밍키`, `@민경`, `@ux` |
| VFX | `@니니`, `@현희`, `@va` |
| 사운드 | `@주디`, `@주연`, `@sd` |
| 프로그래밍 | `@진`, `@윤진`, `@programmer` |
| 테크 디렉터 | `@우디`, `@윤우`, `@td` |
| QA | `@보니`, `@보현`, `@qa` |
| 도움말 | `@help` |

### 산출물 디렉토리

```
output/
├── planning/    ← 기획 산출물 (PD, PM, Balance Designer)
├── design/      ← 설계 산출물 (AD, Character, Background, Animator, UIUX, VFX, Sound)
├── build/       ← 구현 산출물 (Programmer, TD)
└── deploy/      ← 배포/QA 산출물 (QA Engineer)
```

## 참조 문서

모든 참조 문서는 `resources/references/index.md`에 인덱싱되어 있습니다.

| 유형 | 경로 |
|------|------|
| 마스터 기획서 | `output/planning/master_planning_v*.md` |
| 내부 기획 자료 | `resources/references/internal/` |
| 외부 참조 문서 | `resources/references/external/` |

## 요구사항

- Claude CoWork

## 라이선스

MIT License — Team Light Life
