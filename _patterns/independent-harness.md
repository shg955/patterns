---
id: independent-harness
title: 에이전트가 스스로 채점하게 하지 마라
claim: 검증은 에이전트가 만들지 않은 독립 소스 오브 트루스에서 나와야 한다.
origin: synthesized
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
  - kind: own-incident
    ref: soxl#66
    what: >-
      에이전트가 만든 로깅이 실패 사유를 스스로 파괴했다. HTTP 422 본문이 gzip 인데
      코드가 `decode("utf-8","replace")` 로 읽어 원본 바이트를 복구 불가로 만들었다.
      9일간 61건의 주문이 거부되는데 로그에 사유가 한 글자도 안 남았고 −$64.
  - kind: own-measurement
    ref: soxl#71
    what: >-
      "원래 실패하는 37건" 중 6건이 허상이었다. 그 6건이 전부 주문 경로 스위트라,
      라이브 코드를 고칠 때 회귀 판정에 쓰는 바로 그 스위트가 눈이 가려진 상태였다.
  - kind: external-claim
    ref: https://news.hada.io/topic?id=27206
    what: >-
      원문 저자가 "일부 패턴은 보편적임 — 독립적인 소스 오브 트루스(harness)를 두는 건
      어디서나 유효함" 이라고 명시. showboat·rodney 를 그 도구로 언급.
related: [baseline-purification, red-check, verify-your-instruments]
---

## 적용 조건
지금까지 **조건 없이 성립한 유일한 패턴**이다. 테스트가 없는 코드베이스에서도 성립하는데,
그때 harness 는 "테스트" 가 아니라 **실측 스냅샷 비교** 형태를 띤다 — 작업 전후로 상태를
떠서 diff 하는 것으로 시작하면 된다.

## 안 쓰면 무엇이 조용히 깨지는가
에이전트가 자기 산출물을 자기 기준으로 통과시킨다. 실패가 성공으로 기록되므로 대시보드·로그·
테스트 결과가 전부 green 인데 실제로는 안 돌고 있다. **깨진 것이 시끄럽게 알려주지 않는다**는
게 이 실패의 성질이다.

## 잘못 적용하면
harness 를 에이전트에게 "고쳐도 되는 파일" 로 주면 즉시 무력화된다. 숫자가 안 맞을 때
코드를 고치는 대신 기준을 고치게 된다. 실제로 DoD 숫자가 틀렸을 때 개발자가 코드를 맞추도록
"숫자를 고치지 마라, 틀렸다고 판단되면 물어라" 를 명시해야 했다.

## 비용
낮음~중간. 기준선을 한 번 측정해 고정하는 비용.
