import sys
sys.path.insert(0, "/home/claude/galaxymovers-social/tools")
from reviews import REVIEWS
from render_all import css, theme, FOOT, NAVY, ORANGE
from playwright.sync_api import sync_playwright
from PIL import Image

def build(r, t):
    c = theme(t)
    n = len(r["quote"])
    size = 50 if n < 110 else 44 if n < 150 else 38
    extra = f"""
.q{{margin-top:40px;font-weight:700;font-size:{size}px;line-height:1.3}}
.mark{{font-weight:700;font-size:170px;line-height:.6;color:{ORANGE};margin-top:60px;height:70px}}
.stars{{font-size:46px;color:{ORANGE};letter-spacing:6px}}
.who{{position:absolute;left:80px;bottom:190px}}
.who .nm{{font-weight:700;font-size:34px}} .who .sv{{font-weight:500;font-size:26px;color:{c['muted']};margin-top:4px}}
"""
    body = f"""<div class="brand"><div class="dot"></div>GALAXY MOVERS · CUSTOMER REVIEW</div>
    <div class="mark">&ldquo;</div><div class="stars">★★★★★</div>
    <div class="q">{r['quote']}</div>
    <div class="who"><div class="nm">— {r['name']}</div><div class="sv">{r['service']} · Google review</div></div>"""
    return f"<html><head><style>{css(c)}{extra}</style></head><body><div class='card'>{body}{FOOT}</div></body></html>"

out = "/home/claude/galaxymovers-social/posts/"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1080})
    for i, r in enumerate(REVIEWS):
        pg.set_content(build(r, "cream" if i % 2 == 0 else "navy")); pg.wait_for_timeout(300)
        tmp = f"/home/claude/{r['slug']}.png"; pg.screenshot(path=tmp)
        Image.open(tmp).convert("RGB").quantize(48).save(out + r["slug"] + ".png", optimize=True)
        print("made", r["slug"])
    b.close()
