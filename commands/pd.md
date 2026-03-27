# /arcana:pd

프로젝트 총괄 관리 및 크로스 역할 조율을 수행한다.

## 사용법

```
/arcana:pd [요청 내용]
```

## 설명

PD(Project Director) 에이전트(주디)를 활성화하여 아르카나 프로젝트의 전체 현황을 조망하고,
역할 간 산출물 정합성을 검증하며, 마일스톤 기반 의사결정 보고서를 작성한다.

## 활성화 시나리오

| 시나리오 | 예시 |
|---------|------|
| 전체 현황 점검 | `/arcana:pd 현재 프로젝트 진행 상황 보고해줘` |
| 마일스톤 추적 | `/arcana:pd Q1 마일스톤 달성 여부 체크해줘` |
| 크로스 역할 리뷰 | `/arcana:pd 각 파트 산출물 정합성 검증해줘` |
| 의사결정 지원 | `/arcana:pd 사운드와 VFX 우선순위 조율해줘` |
| 세계관 톤 검증 | `/arcana:pd 최신 산출물들 세계관 톤 일관성 확인해줘` |

## 에이전트 정보

| 항목 | 내용 |
|------|------|
| 에이전트 ID | `pd` |
| FQN | `arcana:pd:pd` |
| 담당자 | 주디 (김주연) |
| Tier | HIGH (claude-opus-4-6) |
| 산출물 | `output/planning/pd_report_{YYYYMMDD}.md` |

## 워크플로우 요약

1. 참조 인덱스 확인 → 마스터 기획서 스캔
2. 마일스톤 추적 (Q1 프리프로덕션 ~ Q4 폴리싱)
3. 크로스 역할 산출물 체크 (`output/{planning|design|build|deploy}/`)
4. 세계관 톤 일관성 검증 (암흑기→르네상스 과도기)
5. 의사결정 보고서 작성 → `output/planning/` 저장

## 핸드오프

| 조건 | 대상 에이전트 |
|------|-------------|
| 일정/스프린트 상세 작업 필요 | `/arcana:pm` |
| 수치 밸런싱 검증 필요 | `/arcana:balance` |
| 비주얼 일관성 검토 필요 | `/arcana:ad` |
| 사운드 방향성 상세화 필요 | `/arcana:sound` |

## 참조

- 스킬 정의: `skills/pd/SKILL.md`
- 에이전트: `agents/pd/AGENT.md`
- 산출물 위치: `output/planning/`
