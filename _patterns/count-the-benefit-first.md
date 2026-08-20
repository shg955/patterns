---
id: count-the-benefit-first
title: 만들기 전에 이득을 세라 — 그리고 더 싼 대안을 표에 올려라
claim: 에이전트는 요청받은 것을 잘 만든다. 만들 가치가 있는지는 세지 않는다.
origin: ours
universality: conditional
status: tested
last_reviewed: 2026-08-20
applies_when:
  team_size:         [solo, small]
  codebase_maturity: [mature, legacy]
  test_level:        [none, partial, strong]
  risk_tolerance:    [low, medium]
  typing:            [strong, loose, any]
evidence:
  - kind: own-measurement
    ref: soxl#76
    what: >-
      기대 이득이 월 $2 로 문서화돼 있었는데 실제로는 월 $0.87 = 연 $10 이었다
      (1.40배 과대계상 — 밴드가 일부러 남기는 몫에도 수익률을 매겼다). 같은 날
      config 한 줄로 고친 다른 항목이 연 $7 이었다. 그 비교에서 이 기능은 졌다.
  - kind: own-measurement
    ref: soxl#76
    what: >-
      대안표에 "자동화하지 않고 분기 1회 수동" 행이 없었다. 그 행은 연 $8~10 을
      코드 0줄·lock 0·블로킹 0 으로 잡는다. 그 공백이 의사결정의 가장 큰 결함이었다.
  - kind: own-measurement
    ref: soxl#76
    what: >-
      위험 쪽 전제도 틀렸다. 우려한 "73초 동기 블로킹" 은 신규 위험이 아니라 기존의
      0.12배였다(라이브에 592초 버스트가 이미 3회 있었고 전건 체결). 즉 기각 이유는
      위험이 아니라 **이득이 비용을 못 넘긴 것**이다.
related: [subagent-veto, cold-review-loop]
---

## 적용 조건
**코드 생성이 싸질수록 이 패턴의 값이 커진다.** greenfield 에서는 "일단 만든다" 가 합리적일
수 있지만, 성숙한 시스템에서는 신규 경로가 **영구 운영부담**이 된다 — 동결된 계약, 정적
테스트 lock, 램프 운영. 그 부담은 이득과 달리 자동으로 줄지 않는다.

## 안 쓰면 무엇이 조용히 깨지는가
잘 만들어진, 잘 테스트된, **아무도 필요하지 않은 기능**이 영구 운영부담으로 남는다.
그리고 그 기능을 유지하는 비용이 다른 작업의 속도를 깎는다.

## 잘못 적용하면
이득을 세는 것이 "하지 말자" 의 근거로만 쓰이면 개선이 멈춘다.
**자본·규모에 선형인 이득**은 "지금은 작지만 나중에 커진다" 로 **보류**하는 것이 맞다 —
기각과 보류는 다르고, 보류는 설계 산출물을 보존한다.

## 비용
낮음. 숫자 몇 개. 단 **"더 싼 대안" 을 성실하게 찾는 것**이 실비용이다.
