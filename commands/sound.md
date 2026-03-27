# /arcana:sound

사운드 디렉팅 및 BGM/SFX 설계를 수행한다.

## 사용법

```
/arcana:sound [요청 내용]
```

## 설명

Sound Director 에이전트(주디)를 활성화하여 아르카나 게임의 BGM 구성 계획과
SFX 디자인을 상세화하고, 사운드 에셋 카탈로그를 생성/갱신한다.

## 활성화 시나리오

| 시나리오 | 예시 |
|---------|------|
| BGM 설계 | `/arcana:sound 보스 전투 BGM 구성 계획 상세화해줘` |
| SFX 설계 | `/arcana:sound 천칭 기울기 효과음 질감 설계해줘` |
| 에셋 카탈로그 | `/arcana:sound 사운드 에셋 카탈로그 현황 정리해줘` |
| 사운드 전체 기획 | `/arcana:sound 마스터 기획서 9장 기반으로 전체 사운드 방향 잡아줘` |
| FMOD 연동 설계 | `/arcana:sound 적응형 BGM 전환 FMOD 설계해줘` |

## 에이전트 정보

| 항목 | 내용 |
|------|------|
| 에이전트 ID | `sound-director` |
| FQN | `arcana:sound-director:sound-director` |
| 담당자 | 주디 (김주연) |
| Tier | MEDIUM (claude-sonnet-4-6) |
| 산출물 | `output/design/sound_plan_{YYYYMMDD}.md`, `output/design/sfx_design_{YYYYMMDD}.md`, `output/design/sound_asset_catalog_{YYYYMMDD}.md` |

## 워크플로우 요약

1. 참조 인덱스 확인 → 마스터 기획서 9장 분석
2. Unity Audio System / FMOD for Unity 참조
3. BGM 6종 구성 계획 상세화
   - 메인화면: 오케스트라+합창 / 맵탐색: 앰비언트 / 일반전투: 퍼커시브+현악
   - 보스전투: 풀 오케스트라+코러스 / 사건노드: 피아노 미니멀 / 엔딩: 서정적 오케스트라
4. SFX 5종 질감 설계
   - 카드드로우: 타로카드 질감 / 정방향: 맑고 정돈 / 역방향: 왜곡+리버스
   - 천칭기울기: 기계적 기어 / 시너지발동: 크리스탈 공명
5. 에셋 카탈로그 갱신 → `output/design/` 저장

## 핸드오프

| 조건 | 대상 에이전트 |
|------|-------------|
| 이펙트-사운드 싱크 작업 필요 | `/arcana:vfx` |
| 사운드 에셋 코드 연동 구현 필요 | `/arcana:program` |

## 참조

- 스킬 정의: `skills/sound/SKILL.md`
- 에이전트: `agents/sound-director/AGENT.md`
- 산출물 위치: `output/design/`
- 참조 문서: `resources/references/sound-director/`, `resources/초기자료/모션이펙트제안서_V0_김주연.md`
