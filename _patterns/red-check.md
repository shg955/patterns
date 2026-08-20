---
id: red-check
title: 가드를 지우면 red 가 되는 테스트를 심어라
claim: 가드가 실제로 무언가를 막고 있다는 증거는 "제거하면 실패한다"뿐이다.
origin: ours
universality: conditional
status: tested
last_reviewed: 2026-08-20
applies_when:
  team_size:         [solo, small, large]
  codebase_maturity: [mature, legacy]
  test_level:        [partial, strong]
  risk_tolerance:    [low, medium]
  typing:            [strong, loose, any]
evidence:
  - kind: own-measurement
    ref: soxl#67
    what: >-
      부동소수 결합순서만 바꾼 변형에서 red 가 됐다. 잡아낸 차이가 6.2e−17 —
      ULP 수준에서 판별한다는 뜻이다. 그 감시가 없으면 누가 그 줄을 "단순화" 해도 모른다.
  - kind: own-measurement
    ref: soxl#69
    what: >-
      스윕 클램프 1줄을 제거하면 원장에 1.01주, 계좌에서는 1.00주가 나가는 과대기록이
      생기고 단정 3개가 red 가 된다. 그 과대기록은 다음날 정합성 검사에서 슬롯을 멈춘다.
  - kind: own-measurement
    ref: soxl#74
    what: >-
      패치를 모듈수준에 두는 잘못된 처방으로 바꾸면 원복 프로브가 1 failed 로 잡는다.
related: [independent-harness, verify-your-instruments]
---

## 적용 조건
테스트 인프라가 있어야 성립한다(`test_level: none` 제외). 그리고 **코드가 오래 살 것일 때만**
값이 있다 — 일회성 스크립트에는 과하다. 리스크 허용도가 높은 팀에서는 비용이 이득을 넘는다.

## 안 쓰면 무엇이 조용히 깨지는가
가드가 있는데 아무것도 안 막고 있다. 리팩터링에서 조용히 사라지고, 사라진 것을 아무도 모른 채
다음 사고까지 간다. 특히 에이전트가 "정리" 하는 과정에서 사라지기 쉽다 — 그 줄이 왜 있는지
모르니까.

## 잘못 적용하면
**안전방향으로 틀리는 변형은 감시가 안 된다.** red-check 를 심을 때 "이 변형은 통과한다"를
같이 적어야 감시 범위를 오해하지 않는다. 한 개발자가 "클램프를 지우면 1과 3이 red 인데
2는 안전방향이라 통과한다" 를 명시했고 그게 옳은 기록 방식이다.

## 비용
낮음. 케이스당 몇 줄. 단 **"무엇을 제거하면 red 인가"를 생각하는 비용**이 실비용이다.
