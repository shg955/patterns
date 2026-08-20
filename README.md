# Agentic Engineering Patterns

언제 이 패턴이 통하는가 — **적용 조건을 명시한** 에이전트 엔지니어링 패턴 모음.

## 구조 (DB 없음)
```
_patterns/<id>.md    패턴 1개 = 페이지 1개 (/p/<id>/). frontmatter = 기계가 읽는 메타
_layouts/            base(껍데기) · pattern(패턴 렌더)
index.html           _patterns/ 폴더를 훑어 필터 UI 를 구성
_config.yml          컬렉션 정의 + 필터 축(axes) 정의
SCHEMA.md            frontmatter 계약 · 본문 섹션 · 익명화 규칙
```
GitHub Pages 의 Jekyll 이 `_patterns/` 를 컬렉션으로 읽는다. **빌드 스크립트도, 동기화할
JSON 도 없다.** 축을 늘리려면 `_config.yml` 의 `axes` 부터 고친다.

## 레포를 DB 처럼 쓰기
```bash
grep -l "origin: ours" _patterns/*.md              # 우리 실측 근거 패턴만
grep -l "universality: universal" _patterns/*.md   # 조건 없이 성립한 것
grep -A3 "kind: own-measurement" _patterns/*.md    # 측정 근거를 가진 항목
```

## 원칙
- **근거 없는 패턴은 등록하지 않는다.** `evidence` 가 비면 draft 로도 안 올린다.
- **`origin` 을 섞지 않는다** — 남이 보편적 진리로 말한 것(`external`)과 우리가 확인한 것(`ours`)은 다르다.
- **"조용히 깨지는 것"** 을 본문에 적는다. 시끄럽게 깨지는 건 어차피 잡힌다.
- 적용 안 되는 축은 **취소선**으로 보여준다 — 숨기지 않는다. 범위를 아는 것이 패턴의 절반이다.

## 로컬 미리보기
```bash
bundle exec jekyll serve   # 또는 docker run --rm -v "$PWD":/srv/jekyll -p 4000:4000 jekyll/jekyll jekyll serve
```
