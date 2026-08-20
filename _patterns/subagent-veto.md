---
id: subagent-veto
title: 서브에이전트에게 거부권을 주고 근거를 요구하라
claim: 지시를 그대로 따르는 에이전트보다 근거를 대고 반박하는 에이전트가 사고를 막는다.
origin: ours
universality: conditional
status: tested
last_reviewed: 2026-08-20
applies_when:
  team_size:         [solo, small]
  codebase_maturity: [mature, legacy]
  test_level:        [partial, strong]
  risk_tolerance:    [low, medium]
  typing:            [strong, loose, any]
evidence:
  - kind: own-incident
    ref: soxl#69
    what: >-
      브리프가 "self-test 8줄" 을 요구했는데 그 파일은 수정 금지 대상이었다.
      개발자가 티켓을 따르고 이유를 밝혀 반박했다. 브리프가 틀렸다.
  - kind: own-incident
    ref: soxl#68
    what: >-
      창 게이트를 정규장 안으로 좁히는 안을 승인할 뻔했다. 그러면 고쳐야 할 1시간이
      게이트에서 빠져 "고친 것처럼 보이면서 안 고친" 상태가 된다.
  - kind: own-incident
    ref: soxl#67
    what: >-
      티켓 지시대로 위임 방향을 잡으면 시뮬 현금이 갱신되지 않아 시뮬 전체가 멈춘다.
      개발자가 방향을 반대로 하고 근거를 댔고 그게 옳았다.
  - kind: own-measurement
    ref: soxl#76
    what: >-
      검토가 이득 2.4배 과대계상과 "더 싼 대안이 표에 없음" 을 잡아냈다.
      결과적으로 신규 라이브 주문 경로를 만들지 않았다.
related: [cold-review-loop, independent-harness, count-the-benefit-first]
---

## 적용 조건
**오케스트레이터가 혼자 여러 작업을 지시하는 구조**(solo/small)에서 값이 크다 — 지시자가
세부를 다 확인할 수 없기 때문이다. 큰 팀에서는 사람 리뷰가 이미 그 역할을 한다.

검증 수단(테스트·실측)이 없으면 반박이 **의견 대립**으로 끝나므로 `test_level: none` 에서는
성립하지 않는다. 반박은 데이터로 결판나야 한다.

## 안 쓰면 무엇이 조용히 깨지는가
지시자의 오류가 그대로 코드가 된다. 오류가 사고로 드러날 때까지 아무도 "그 지시가 틀렸다"고
말하지 않는다. 에이전트는 기본적으로 순종적이라 **틀린 지시일수록 조용히 실행된다.**

## 잘못 적용하면
거부권만 주고 근거를 요구하지 않으면 진행이 멈춘다. **"재현 명령 또는 코드 인용"** 을
반박의 형식 요건으로 못박아야 한다. 그리고 반박이 맞았을 때 지시를 고치는 쪽이
오케스트레이터라는 것도 명시해야 한다.

## 비용
중간. 왕복이 늘고 브리프를 길게 써야 한다. 대신 브리프를 길게 쓰는 것 자체가
지시자의 사고를 정리시킨다.
