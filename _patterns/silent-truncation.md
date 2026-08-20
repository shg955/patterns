---
id: silent-truncation
title: 절단은 조용하다 — stopReason 을 지표에 박아라
claim: LLM 응답이 예산에서 잘리면 실패가 아니라 짧은 성공처럼 보인다.
origin: ours
universality: conditional
status: tested
last_reviewed: 2026-08-20
applies_when:
  team_size:         [solo, small, large]
  codebase_maturity: [greenfield, mature, legacy]
  test_level:        [none, partial, strong]
  risk_tolerance:    [low, medium, high]
evidence:
  - kind: own-incident
    ref: soxl/WH-007
    what: >-
      로컬 에이전트가 큰 과제에서 산출물 0 으로 끝났다. 원인을 prefill 병목 → 과추론 →
      타임아웃으로 **세 번 오진단**했다. 실제로는 provider 설정의 `maxTokens=4096` 하나였고
      서버가 reasoning-budget 12288 로 돌아 thinking 만으로 예산이 소진됐다.
      `stopReason: "length"` 한 줄만 봤으면 첫 번에 알 수 있었다.
  - kind: own-measurement
    ref: soxl#78
    what: >-
      봇의 LLM 호출 전수에서 같은 함정을 찾았다. 한 스킬은 274회 중 265회 실패(97%)하고,
      다른 스킬은 완료토큰이 상한과 정확히 같은데 오류 없이 기록됐다 — 스키마가 없어
      절단이 성공으로 남았다. 그 파이프라인은 폴백 경로로만 돌고 있었다.
detect: >-
  예산·상한을 걸어둔 값과 실제로 요청된 값을 나란히 로그로 찍어라. 두 수가 다른데
  에러가 없으면 지금 조용히 잘리고 있다. 상한이 min() 으로 적용되는 코드를 grep 하고
  각 지점에 경고 로그가 있는지 확인해라.
related: [verify-your-instruments, independent-harness]
---

## 적용 조건
LLM 을 파이프라인에 쓰는 모든 경우. 특히 **thinking/reasoning 이 켜진 모델**에서 치명적이다 —
thinking 토큰이 출력 예산을 먹으므로, 예전 모델 기준으로 잡은 `max_tokens` 가 그대로 남아
있으면 **답을 쓸 예산이 0** 이 된다. 모델을 교체했는데 토큰 예산을 안 만졌다면 이미 이 상태다.

## 안 쓰면 무엇이 조용히 깨지는가
파이프라인이 열화된 상태로 계속 돈다. 산출물이 나오므로 아무도 의심하지 않는다.
"3~5 sources" 같은 빈약한 결과가 정상처럼 축적된다.

## 어떻게 적용하나
1. **상한이 적용되는 지점을 전부 찾는다.** `min(요청, 상한)` · `[:N]` · `truncate` ·
   `max_tokens` · `timeout`. 각각이 발동했을 때 **경고를 남기는지** 본다.
2. **발동을 값으로 기록한다.** 로그 한 줄이 아니라 산출물의 메타데이터에 남겨라
   (`stop_reason` · `truncated: true` · `requested vs applied`). 로그는 유실되고 아무도 안 본다.
3. **잘린 산출물을 성공으로 저장하지 마라.** 최소한 배너 한 줄과 `partial: true` 를 붙인다.
4. **상한을 설정으로 올릴 수 있게 해라.** 코드에 박힌 상한은 다음 사람이 못 찾는다.

```
# 실제로 걸렸던 형태 (2026-08-20)
파이프라인 선언   time_budget_s: 1500
설정 상한        timeout_s: 1200          ← 조용히 여기로 잘렸다
결과            경고 로그 1줄만 남고 300초가 사라졌다.
                티켓 2건이 1500 을 전제로 설계돼 있었는데 아무도 몰랐다
```

## 적용됐는지 확인하는 방법
**상한을 일부러 아주 작게 만들어 돌려봐라.** 산출물에 절단 표시가 나타나지 않으면
그 절단은 지금도 조용히 일어나고 있다. `max_tokens` 를 10 으로 두고 돌렸을 때
"짧지만 성공" 처럼 보이면 그게 이 패턴이 말하는 실패다.

## 잘못 적용하면
`max_tokens` 를 무작정 올리면 비용·지연이 늘고 모델이 장황해진다.
**올리는 게 아니라 관측이 먼저다** — `stopReason` 을 기록하면 어디를 올려야 하는지 나온다.

## 비용
매우 낮음. 지표 한 줄 추가.
