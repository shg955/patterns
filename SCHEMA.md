# 패턴 스키마 — md + frontmatter

## 왜 이 구조인가
인용된 설계 원칙: *"대부분의 교훈이 보편적 진리처럼 말해지지만, 실제로는 팀 규모·코드베이스
성숙도·테스트 수준·리스크 허용도에 따라 달라진다. 중요한 건 **언제 이 패턴이 통하는가**를
밝히는 것"*

⇒ `applies_when` 은 산문이 아니라 **frontmatter 필드**다. 그래야 독자가 자기 상황으로 **필터**할 수 있다.
책은 그걸 못 하고 웹사이트는 한다 — 그게 웹을 택하는 실제 이유다.

## 구조 결정
- **DB 없음.** md 파일 1개 = 패턴 1개 = 페이지 1개(`/p/<id>/`).
- **frontmatter = 기계가 읽는 메타.** 필터·정렬·집계에 쓰는 건 전부 여기.
- **본문 = 사람이 읽는 산문.** 자유서술만.
- **Jekyll 컬렉션이 `_patterns/` 폴더를 훑어 화면을 만든다.** 매니페스트를 손으로 동기화하지 않는다.
- 나중에 레포에 grep/검색을 돌리면 그 자체가 DB다(`grep -l "origin: ours" _patterns/`).

## frontmatter
```yaml
---
id:            kebab-case (파일명과 일치)
title:         한 줄 제목
claim:         한 문장 주장 — 카드 앞면에 뜬다
origin:        ours | external | synthesized   # 🔴 우리 실측과 남의 주장을 섞지 않는다
universality:  universal | conditional | narrow
status:        draft | tested | retired | superseded
superseded_by: <id>   # status: superseded 일 때만
last_reviewed: YYYY-MM-DD

applies_when:                                  # 🔴 필터 축. 해당하는 값만 나열
  team_size:         [solo, small, large]
  codebase_maturity: [greenfield, mature, legacy]
  test_level:        [none, partial, strong]
  risk_tolerance:    [low, medium, high]
  typing:            [strong, loose, any]

evidence:                                      # 🔴 비어 있으면 등록 불가
  - kind: own-incident | own-measurement | external-claim | external-measurement
    ref:  soxl#66  또는 URL
    what: 무엇이 관측됐는가 — **숫자를 넣어라**

related: [다른 패턴 id]
---
```

## 본문 섹션 (고정)
```markdown
## 적용 조건
필드로 안 잡히는 뉘앙스. "왜 이 축에서는 성립하지 않는가"를 적는다.

## 안 쓰면 무엇이 조용히 깨지는가
🔴 "조용히" 가 핵심이다. 시끄럽게 깨지는 건 어차피 잡힌다.

## 잘못 적용하면
안티패턴. 이 패턴을 오용하는 가장 자연스러운 방식.

## 비용
사람·시간·인프라. 낮음/중간/높음 + 한 줄 근거.
```

## origin 을 나누는 이유
남이 "보편적 진리"로 말한 것과 우리가 실제로 확인한 것을 섞으면 이 사이트가
또 하나의 격언 모음이 된다. 실측 하루치만 봐도 추론 9건이 데이터로 뒤집혔고,
외부 2차 출처는 HTTP 403 이라 1차 출처를 다시 찾아야 했다.

## 레퍼런스 조사 결과 (2026-08-20) — 두 정본에서 배운 것

**MADR** (ADR 표준 · `adr.github.io/madr`) — 결정 1건 = md 1개, 레포에 번호순 저장, `log4brains` 가
검색 가능한 사이트로 발행. frontmatter: `status`(proposed|rejected|accepted|deprecated|superseded)·
`date`·`decision-makers`·`consulted`·`informed`. 본문: Context and Problem → Decision Drivers →
Considered Options → **Decision Outcome** → Consequences → Confirmation → Pros/Cons.
🔴 **적용 조건을 별도 필드로 형식화하지 않는다** — context·drivers 에서 암묵적으로 드러난다.

**Microsoft Cloud Design Patterns** (`learn.microsoft.com/azure/architecture/patterns/*`) — 본문:
Context and problem → Solution → Problems and considerations → **When to use this pattern** →
Workload design(품질 축 표) → Example → Related resources.
"When to use" 가 **`Use this pattern when:` / `This pattern might not be suitable when:` 두 불릿 묶음**이다.
frontmatter 는 발행 메타(`ms.date`·`ms.topic`·`author`)이고 **의미 메타가 아니다.**
🔴 즉 적용 조건이 **산문 불릿**이고 **필터 가능한 구조가 아니다.**

### 그래서 우리가 다르게 하는 것 (이 사이트의 차별점)
둘 다 "언제 통하는가" 를 **기계가 못 읽는다.** Microsoft 는 산문으로 명시하고 MADR 은 암묵적이다.
인용된 원칙("팀 규모·성숙도·테스트 수준·리스크 허용도에 따라 달라진다")을 실현하려면 그게
**필터 축**이어야 한다 ⇒ `applies_when` 을 frontmatter 필드로 둔다.

### 그들에게서 채택하는 것 2개
1. **`not_suitable_when` 을 1급 섹션으로 승격** (Microsoft 에서 채택).
   `anti_pattern`(오용)과 **다른 것**이다 — 이건 *올바르게 적용했는데 맥락이 틀린* 경우다.
   `applies_when` 이 "어디서 되는가" 라면 이건 "왜 저기서는 안 되는가" 다.
2. **생명주기 필드** (MADR 에서 채택): `status` 에 `superseded` 추가 + `superseded_by`.
   패턴은 폐기된다. 폐기 이력을 지우면 "왜 저 방식을 안 쓰는가" 를 잃는다.

## 공개 사이트 익명화 규칙
공개하되 주 독자는 작성자다. 근거로 **유효한 것**과 **빼는 것**을 구분한다.
- ✅ 넣는다: 손실·비용 규모($64 · 연 $10), 실패 건수(274회 중 265), 시간(592초), 비율(97%)
- ❌ 뺀다: 계좌 잔고·매수여력, `order_id`, API 키, 전략 파라미터 실값, 보유 수량
- 티켓 번호(`soxl#66`)는 넣는다 — 추적성이 근거의 일부이고 그 레포는 비공개다
