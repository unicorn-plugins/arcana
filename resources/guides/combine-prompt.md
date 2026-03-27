# 프롬프트 조립 가이드

에이전트 호출 시 프롬프트를 조립하는 공통 절차.

## 입력

- **FQN**: SKILL.md의 FQN 테이블에서 확인 (예: `arcana:balance-designer:balance-designer`)
- **사용자 메시지**: 사용자가 입력한 요청

## 조립 절차

### 1단계: 3파일 로드

FQN에서 에이전트 디렉토리를 도출하여 (`arcana:{agent}:{agent}` → `agents/{agent}/`) 다음 3파일을 로드한다:

| 파일 | 용도 |
|------|------|
| `AGENT.md` | 프롬프트 본문 (WHY + HOW) |
| `agentcard.yaml` | tier 확인 + persona 정보 |
| `tools.yaml` | 도구 목록 + 제약 조건 |

### 2단계: runtime-mapping 구체화

`gateway/runtime-mapping.yaml`을 참조하여 추상 값을 구체 값으로 변환한다:

**모델 구체화**
- agentcard.yaml의 `tier` 값을 `tier_mapping.default.{TIER}.model`로 변환
- 예: `tier: MEDIUM` → `claude-sonnet-4-6`

**도구 구체화**
- tools.yaml의 각 추상 도구를 `tool_mapping.{도구명}`으로 변환
- 예: `image_generate` → `tools/generate-image-bridge.py`

**금지액션 구체화**
- agentcard.yaml의 `forbidden_actions` 각 항목을 `action_mapping.{액션}`으로 변환
- 예: `code_execute` → `["Bash"]` 제외

**최종 도구 산출**
```
최종 도구 = (구체화된 도구) - (금지액션에서 도출된 제외 도구)
```

### 3단계: 참조 문서 로드 (캐싱 최적화)

`resources/references/index.md`를 읽어 아래 두 섹션의 문서를 모두 로드한다.

**역할 섹션 찾기**

FQN의 에이전트명으로 `## 3. 역할별 참조` 아래 `### {에이전트명}` 섹션을 직접 찾는다.
- 예: FQN `arcana:balance-designer:balance-designer` → `### balance-designer` 섹션

**로드 대상**
1. **역할별 참조** — `### {에이전트명}` 섹션의 내부/외부 문서 전체
2. **공통 참조** — `## 4. 공통 참조` 섹션의 문서 전체

> 각 문서는 내용 전체를 읽어 다음 단계에서 프롬프트에 포함한다.

### 4단계: 프롬프트 합성

3파일(AGENT.md + agentcard.yaml + tools.yaml)을 하나의 프롬프트로 합친다.

### 5단계: 인격 주입

agentcard.yaml에 `persona` 섹션이 존재하면, 다음 템플릿으로 인격을 주입한다:

```
당신은 {persona.profile.nickname}입니다.
답변 시 별명 '{persona.profile.nickname}'를 표시하세요.
{persona.style}.
{persona.background}.
```

### 6단계: 프롬프트 구성 순서

최종 프롬프트는 다음 순서로 구성한다.
정적 블록을 앞에 배치하여 반복 호출 시 프롬프트 캐싱이 적용되도록 한다.

```
[정적 — 캐싱 대상]
1. 공통 정적       : runtime-mapping에서 도출된 공통 설정
2. 에이전트별 정적  : 3파일(AGENT.md + agentcard.yaml + tools.yaml) 합성 결과 + 인격 주입
3. 공통 참조 문서   : index.md 4절에서 로드한 문서 내용
4. 역할별 참조 문서  : index.md 3절에서 로드한 내부/외부 문서 내용

[동적]
5. 사용자 메시지   : 매 호출마다 달라지는 입력 (항상 마지막)
```

> **참조 문서 포함 형식**
> ```
> [공통 참조 문서]
> ## [참조: {파일명}]
> {문서 전체 내용}
> ...
>
> [역할별 참조 문서]
> ## [참조: {파일명}]
> {문서 전체 내용}
> ...
> ```

### 7단계: 에이전트 호출

```
Task(subagent_type="{FQN}", prompt=조립된 프롬프트)
```

에이전트는 컨텍스트에 이미 참조 문서가 포함되어 있으므로
**파일 읽기 툴 호출 없이** 해당 내용을 직접 참조한다.
