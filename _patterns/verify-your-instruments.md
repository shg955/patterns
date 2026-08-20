---
id: verify-your-instruments
title: 측정 도구를 먼저 검증하라
claim: 도구가 아무것도 안 하고 있어도 로그는 성공처럼 보인다.
origin: ours
universality: universal
status: tested
last_reviewed: 2026-08-20
applies_when:
  team_size:         [solo, small, large]
  codebase_maturity: [greenfield, mature, legacy]
  test_level:        [none, partial, strong]
  risk_tolerance:    [low, medium, high]
  typing:            [strong, loose, any]
evidence:
  - kind: own-measurement
    ref: soxl#73
    what: >-
      `-p no:randomly` 를 여러 브리프에서 "셔플했다" 의 근거로 요구하고 보고에서 받아들였는데
      `pytest-randomly` 가 설치돼 있지 않았다. 그 플래그는 no-op 이었고 셔플은 없었다.
      순서 변화는 파일 인자 순서로만 만들어진다.
  - kind: own-measurement
    ref: soxl#74
    what: >-
      "라이브 DB 쓰기 0" 을 세 테이블 카운트로만 판정해왔다. 그 셋을 안 건드리는 쓰기는
      전부 통과했고 실제로 다른 테이블에 65행이 들어가 있었다. 기준을 세 번 고쳐야
      맞는 것(전 테이블 행수 diff + 정상 드리프트 귀속)에 도달했다.
  - kind: own-measurement
    ref: soxl/WH-007
    what: >-
      실효 처리량 지표가 "output" 토큰만 세어 서버 자체 계측과 17배 어긋났다(2,424 vs 42,115).
      그 지표를 믿고 원인을 세 번 오진단했다.
  - kind: own-measurement
    ref: soxl#78
    what: >-
      🔴 **같은 결함을 고쳤다고 하고 새로 만들었다.** 위 사건 뒤 만든 래퍼가 도구 호출을
      `'"type":"tool_call"'` 로 셌는데 **그 이벤트는 존재하지 않는다** — 항상 0 을 찍었고,
      나는 그 0 을 무시하고 원시 정규식으로 다시 세어 보고했다. 실측 대조:
      도구 raw 64 vs 실제 16(top-level `tool_execution_start`) · 생성토큰 raw 90,630 vs
      실제 30,210(`turn_end.usage.output`) · 실효 49 tok/s(146 이라고 세 번 보고했다).
      스트리밍 델타와 중간 usage 가 중복 계상된다.
related: [independent-harness, silent-truncation, baseline-purification]
---

## 적용 조건
조건 없이 성립한다. **측정을 하는 순간 이 패턴이 필요하다.**

## 안 쓰면 무엇이 조용히 깨지는가
측정이 무효인데 결론이 나온다. 그리고 그 결론으로 다음 결정을 한다.
**도구가 조용히 아무것도 안 하는 것**이 가장 나쁜 실패 양식이다 — 에러가 나면 오히려 낫다.

## 잘못 적용하면
도구를 검증하려고 또 다른 미검증 도구를 쓴다. 검증은 **독립 경로**여야 한다 —
플러그인 존재 여부는 `importlib.util.find_spec` 으로, 토큰 수는 서버 자체 계측으로,
DB 무접촉은 전 테이블 스냅샷으로.

## 이 패턴이 자기 자신에게 적용된다
이 패턴을 문서화한 직후, 그 교훈으로 만든 새 지표가 **같은 방식으로 틀렸다**(위 `soxl#78` 근거).
원시 문자열을 세는 습관이 원인이었다 — 이벤트 스키마를 확인하지 않고 "그럴 것 같은" 키를 골랐다.
⇒ 처방은 "조심하자" 가 아니라 **구조적인 것**이어야 한다: 지표를 뽑는 코드를 한 곳에 모으고,
**과대계수 방식이 red 가 되는 음성대조 테스트**를 붙인다. 원시 정규식 집계는 금지 목록에 넣는다.

## 비용
낮음. 한 번의 확인. 안 하면 그 뒤 **모든 측정이 무효**가 된다.
단 이 패턴은 **재발한다** — 한 번 고쳤다고 끝나지 않는다.
