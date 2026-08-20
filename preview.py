#!/usr/bin/env python3
"""독립 렌더러 — Jekyll 없이 _patterns/*.md 를 정적 HTML 로 굽는다.

존재 이유가 두 가지다:
 1) 로컬에 Ruby·Docker 가 없어도 "잘 보이는지" 를 확인한다.
 2) 🔴 **저장 형식이 Jekyll 에 묶이지 않았음을 증명한다.** 100줄 파이썬이 읽을 수 있으면
    다른 어떤 도구도 읽을 수 있다. 그게 md+frontmatter 를 고른 이유의 절반이다.
GitHub Pages 의 Jekyll 이 정본 렌더러이고 이건 미리보기 + 형식 검증용이다.
"""
import io, os, re, sys, html, json
sys.path.insert(0, "/root/soxl-grid-bot/.venv/lib/python3.12/site-packages")
import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = yaml.safe_load(io.open(os.path.join(BASE, "_config.yml"), encoding="utf-8"))
AXES, LABELS = CFG["axes"], CFG["axis_labels"]
OUT = os.path.join(BASE, "_preview")

def split_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m: raise ValueError("frontmatter 없음")
    return yaml.safe_load(m.group(1)), m.group(2)

def md_lite(s):
    """검증용 최소 마크다운. 정본은 Jekyll 의 kramdown 이다."""
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    out, para = [], []
    for line in s.split("\n"):
        if line.startswith("## "):
            if para: out.append("<p>" + " ".join(para) + "</p>"); para = []
            out.append("<h2>" + line[3:] + "</h2>")
        elif not line.strip():
            if para: out.append("<p>" + " ".join(para) + "</p>"); para = []
        else:
            para.append(line.strip())
    if para: out.append("<p>" + " ".join(para) + "</p>")
    return "\n".join(out)

def load(coll):
    d = os.path.join(BASE, "_" + coll)
    items = []
    if not os.path.isdir(d): return items
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"): continue
        fm, body = split_fm(io.open(os.path.join(d, fn), encoding="utf-8").read())
        fm["_file"], fm["_body"] = fn, body
        fm["_url"] = "p_%s.html" % fm["id"]
        items.append(fm)
    return items

# ── 검증 ────────────────────────────────────────────────────────────────
REQ = ["id","title","claim","origin","universality","status","last_reviewed","applies_when","evidence"]
SECTIONS = ["적용 조건", "조용히 깨지는가", "잘못 적용하면", "비용"]
problems = []
pats = load("patterns")
ids = {p["id"] for p in pats}
for p in pats:
    for k in REQ:
        if k not in p or p[k] in (None, "", []): problems.append("%s: 필수 %s 누락/빈값" % (p["_file"], k))
    if p.get("id") != p["_file"][:-3]: problems.append("%s: id != 파일명" % p["_file"])
    for ax in AXES:
        v = (p.get("applies_when") or {}).get(ax)
        if not v: problems.append("%s: applies_when.%s 없음" % (p["_file"], ax)); continue
        bad = [x for x in v if x not in AXES[ax] and x != "any"]
        if bad: problems.append("%s: applies_when.%s 에 미정의 값 %s" % (p["_file"], ax, bad))
    for e in (p.get("evidence") or []):
        for k in ("kind","ref","what"):
            if not e.get(k): problems.append("%s: evidence 항목에 %s 없음" % (p["_file"], k))
    for s in SECTIONS:
        if s not in p["_body"]: problems.append("%s: 본문에 '%s' 섹션 없음" % (p["_file"], s))
    for r in (p.get("related") or []):
        if r not in ids: problems.append("%s: related '%s' 미작성(경고)" % (p["_file"], r))
    if p.get("status") == "superseded" and not p.get("superseded_by"):
        problems.append("%s: superseded 인데 superseded_by 없음" % p["_file"])

# ── 렌더 ────────────────────────────────────────────────────────────────
os.makedirs(OUT, exist_ok=True)
CSS = io.open(os.path.join(BASE, "_layouts", "base.html"), encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", CSS, re.S).group(1)
def shell(title, body):
    return ("<!doctype html><html lang=ko><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            "<title>%s</title><style>%s</style></head><body><div class=wrap>%s</div></body></html>"
            % (html.escape(title), CSS, body))

for p in pats:
    rows = ""
    for ax, allv in AXES.items():
        mine = (p["applies_when"] or {}).get(ax) or []
        cells = " · ".join(
            ("<strong>%s</strong>" % v) if (v in mine or "any" in mine)
            else "<span style='color:var(--dim);text-decoration:line-through'>%s</span>" % v
            for v in allv)
        rows += "<tr><th>%s</th><td>%s</td></tr>" % (LABELS[ax], cells)
    ev = "".join("<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>" % (
        html.escape(e["kind"]),
        ("<a href='%s'>링크</a>" % html.escape(e["ref"])) if "://" in str(e["ref"]) else "<code>%s</code>" % html.escape(str(e["ref"])),
        html.escape(str(e["what"]))) for e in p["evidence"])
    body = ("<div style='font-size:.8rem'><a href=index.html>← 목록</a></div>"
            "<h1>%s</h1><p class=lede>%s</p>"
            "<p><span class='tag o-%s'>%s</span> <span class='tag u-%s'>%s</span> "
            "<span class=tag style='color:var(--dim)'>%s</span> "
            "<span style='color:var(--dim);font-size:.8rem'>최종 검토 %s</span></p>"
            "<h2>언제 통하는가</h2><div class=scroll><table><thead><tr><th>축</th><th>적용되는 값</th></tr></thead><tbody>%s</tbody></table></div>"
            "<h2>근거</h2><div class=scroll><table><thead><tr><th>종류</th><th>출처</th><th>무엇이 관측됐나</th></tr></thead><tbody>%s</tbody></table></div>"
            "%s") % (html.escape(p["title"]), html.escape(p["claim"]), p["origin"], p["origin"],
                     p["universality"], p["universality"], p["status"], p["last_reviewed"],
                     rows, ev, md_lite(p["_body"]))
    io.open(os.path.join(OUT, p["_url"]), "w", encoding="utf-8").write(shell(p["title"], body))

cards = ""
for p in sorted(pats, key=lambda x: (x["universality"] != "universal", x["id"])):
    data = " ".join("data-%s='%s'" % (ax, ",".join((p["applies_when"] or {}).get(ax) or [])) for ax in AXES)
    cards += ("<div class=pat %s data-universality='%s' style='border:1px solid var(--line);border-radius:8px;"
              "padding:.9rem 1rem;margin:.7rem 0;background:var(--card)'>"
              "<div><a href='%s' style='font-weight:600;text-decoration:none'>%s</a> "
              "<span class='tag o-%s'>%s</span> <span class='tag u-%s'>%s</span></div>"
              "<div style='color:var(--dim);font-size:.93rem;margin-top:.3rem'>%s</div>"
              "<div style='font-size:.8rem;margin-top:.35rem;color:var(--dim)'>근거 %d건 · %s</div></div>") % (
              data, p["universality"], p["_url"], html.escape(p["title"]), p["origin"], p["origin"],
              p["universality"], p["universality"], html.escape(p["claim"]), len(p["evidence"]), p["last_reviewed"])
sels = "".join("<tr><th style='white-space:nowrap'>%s</th><td><select data-axis=%s><option value=''>— 무관 —</option>%s</select></td></tr>"
               % (LABELS[ax], ax, "".join("<option>%s</option>" % v for v in AXES[ax])) for ax in AXES)
JS = """<script>
const sels=[...document.querySelectorAll('select[data-axis]')],pats=[...document.querySelectorAll('.pat')];
function apply(){let n=0,u=0;for(const el of pats){let ok=true;
for(const s of sels){if(!s.value)continue;const v=(el.dataset[s.dataset.axis]||'').split(',');
if(!(v.includes(s.value)||v.includes('any'))){ok=false;break}}
el.style.display=ok?'':'none';if(ok){n++;if(el.dataset.universality==='universal')u++}}
document.getElementById('count').textContent=`적용 ${n}건${u?` (그중 보편 ${u}건)`:''} / 전체 ${pats.length}건`;
document.getElementById('empty').style.display=n?'none':''}
sels.forEach(s=>s.addEventListener('change',apply));apply();</script>"""
idx = ("<h1>%s</h1><p class=lede>%s</p><h2>내 상황</h2><div class=scroll><table><tbody>%s</tbody></table></div>"
       "<p id=count style='color:var(--dim);font-size:.9rem'></p><h2>패턴</h2>%s"
       "<p id=empty style='display:none;color:var(--warn)'>이 조합에 적용되는 패턴이 없다.</p>%s") % (
       CFG["title"], CFG["description"], sels, cards, JS)
io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(shell(CFG["title"], idx))

print("  렌더: %d 패턴 → _preview/" % len(pats))
print("  검증: %s" % ("문제 %d건" % len(problems) if problems else "통과 ✅"))
for x in problems: print("    🔴 " + x)
