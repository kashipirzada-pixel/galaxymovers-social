import sys
sys.path.insert(0, "/home/claude")
from plan import POSTS
from playwright.sync_api import sync_playwright
from PIL import Image

NAVY, ORANGE, CREAM = "#0B1F3A", "#FF8A1F", "#FFF6EC"
FONT = "/usr/share/fonts/truetype/google-fonts/"

def theme(t):
    if t == "navy":
        return dict(bg=NAVY, fg="#FFFFFF", muted="#C9D4E6", chip="rgba(255,255,255,.1)", chipb="rgba(255,255,255,.25)", tile="rgba(255,255,255,.07)", ink=NAVY)
    return dict(bg=CREAM, fg=NAVY, muted="#43536b", chip="#FFFFFF", chipb="rgba(11,31,58,.18)", tile="#FFFFFF", ink=NAVY)

def art(name, c):
    fg = "#FFFFFF" if c["bg"] == NAVY else NAVY
    arts = {
     "truck": f"""<svg viewBox="0 0 320 150"><rect x="10" y="20" width="190" height="95" rx="10" fill="{ORANGE}"/>
       <text x="105" y="62" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="22" fill="{NAVY}">GALAXY</text>
       <text x="105" y="88" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="15" fill="{NAVY}">MOVERS</text>
       <path d="M205 45 h55 l40 38 v32 h-95 z" fill="{fg}"/><path d="M218 55 h38 l28 26 h-66 z" fill="{NAVY}" opacity=".7"/>
       <circle cx="65" cy="120" r="19" fill="#1d2d4a" stroke="{fg}" stroke-width="6"/><circle cx="250" cy="120" r="19" fill="#1d2d4a" stroke="{fg}" stroke-width="6"/></svg>""",
     "boxes": """<svg viewBox="0 0 220 170"><rect x="10" y="70" width="100" height="95" rx="6" fill="#D9A066"/><rect x="10" y="70" width="100" height="18" fill="#C58A4E"/>
       <rect x="52" y="70" width="16" height="95" fill="#F3D2A6"/><rect x="115" y="90" width="95" height="75" rx="6" fill="#D9A066"/>
       <rect x="115" y="90" width="95" height="15" fill="#C58A4E"/><rect x="155" y="90" width="15" height="75" fill="#F3D2A6"/>
       <rect x="40" y="5" width="85" height="68" rx="6" fill="#E3B27A"/><rect x="40" y="5" width="85" height="13" fill="#C58A4E"/><rect x="75" y="5" width="14" height="68" fill="#F3D2A6"/></svg>""",
     "paw": f"""<svg viewBox="0 0 200 200"><ellipse cx="100" cy="130" rx="48" ry="40" fill="{ORANGE}"/>
       <ellipse cx="45" cy="80" rx="20" ry="26" fill="{ORANGE}"/><ellipse cx="80" cy="45" rx="20" ry="27" fill="{ORANGE}"/>
       <ellipse cx="122" cy="45" rx="20" ry="27" fill="{ORANGE}"/><ellipse cx="157" cy="80" rx="20" ry="26" fill="{ORANGE}"/></svg>""",
     "plane": f"""<svg viewBox="0 0 220 200"><circle cx="110" cy="100" r="85" fill="none" stroke="{fg}" stroke-width="6" opacity=".35"/>
       <ellipse cx="110" cy="100" rx="40" ry="85" fill="none" stroke="{fg}" stroke-width="6" opacity=".35"/>
       <line x1="25" y1="100" x2="195" y2="100" stroke="{fg}" stroke-width="6" opacity=".35"/>
       <g transform="translate(110 100) rotate(-35)"><path d="M-70 0 L70 0 M0 0 L-25 -55 M0 0 L-25 55 M-60 0 L-75 -22 M-60 0 L-75 22" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/></g></svg>""",
     "car": f"""<svg viewBox="0 0 300 170"><rect x="5" y="118" width="290" height="14" rx="4" fill="{fg}" opacity=".35"/>
       <path d="M40 105 L60 65 Q68 50 85 50 H190 Q205 50 215 62 L245 95 Q270 98 272 110 V118 H30 V110 Q30 105 40 105 Z" fill="{ORANGE}"/>
       <path d="M78 62 H135 V92 H64 Z M148 62 H192 L222 92 H148 Z" fill="{NAVY}" opacity=".8"/>
       <circle cx="85" cy="120" r="22" fill="#1d2d4a" stroke="{fg}" stroke-width="6"/><circle cx="220" cy="120" r="22" fill="#1d2d4a" stroke="{fg}" stroke-width="6"/></svg>""",
     "warehouse": f"""<svg viewBox="0 0 260 190"><path d="M10 70 L130 10 L250 70 V185 H10 Z" fill="{ORANGE}"/>
       <rect x="55" y="95" width="150" height="90" fill="{NAVY}"/>
       <rect x="70" y="140" width="45" height="45" fill="#D9A066"/><rect x="120" y="140" width="45" height="45" fill="#E3B27A"/><rect x="95" y="100" width="45" height="40" fill="#C58A4E"/></svg>""",
     "office": f"""<svg viewBox="0 0 260 200"><rect x="20" y="20" width="130" height="180" rx="6" fill="{ORANGE}"/>
       {''.join(f'<rect x="{38+c*38}" y="{40+r*36}" width="24" height="22" fill="{NAVY}" opacity=".8"/>' for r in range(4) for c in range(3))}
       <rect x="160" y="110" width="90" height="90" rx="6" fill="#D9A066"/><rect x="160" y="110" width="90" height="16" fill="#C58A4E"/><rect x="197" y="110" width="16" height="90" fill="#F3D2A6"/></svg>""",
     "calendar": f"""<svg viewBox="0 0 220 210"><rect x="10" y="30" width="200" height="170" rx="16" fill="{fg}"/>
       <rect x="10" y="30" width="200" height="48" rx="16" fill="{ORANGE}"/><rect x="10" y="60" width="200" height="18" fill="{ORANGE}"/>
       <rect x="50" y="10" width="14" height="40" rx="7" fill="{NAVY}"/><rect x="156" y="10" width="14" height="40" rx="7" fill="{NAVY}"/>
       {''.join(f'<rect x="{32+c*40}" y="{95+r*34}" width="26" height="22" rx="4" fill="{ORANGE if (r,c)==(1,3) else NAVY}" opacity="{1 if (r,c)==(1,3) else .25}"/>' for r in range(3) for c in range(4))}</svg>""",
    }
    return arts[name]

def css(c):
    return f"""
@font-face {{ font-family:Poppins; src:url(file://{FONT}Poppins-Bold.ttf); font-weight:700; }}
@font-face {{ font-family:Poppins; src:url(file://{FONT}Poppins-Medium.ttf); font-weight:500; }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;font-family:Poppins;overflow:hidden}}
.card{{width:1080px;height:1080px;position:relative;padding:80px 80px 0;background:{c['bg']};color:{c['fg']}}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:700;font-size:28px;letter-spacing:1px}}
.dot{{width:22px;height:22px;border-radius:50%;background:{ORANGE}}}
.kicker{{margin-top:70px;font-weight:700;font-size:30px;color:{ORANGE};letter-spacing:2px;text-transform:uppercase}}
h1{{font-weight:700;font-size:88px;line-height:1.05;margin-top:14px}}
.chips{{margin-top:44px;display:flex;flex-wrap:wrap;gap:16px;max-width:920px}}
.chips span{{background:{c['chip']};border:2px solid {c['chipb']};border-radius:40px;padding:12px 26px;font-weight:700;font-size:28px}}
.sub{{margin-top:32px;font-weight:500;font-size:29px;color:{c['muted']}}}
.art{{position:absolute;right:70px;bottom:180px;width:380px}}
.art svg{{width:100%;height:auto;display:block}}
.tips{{margin-top:44px;display:flex;flex-direction:column;gap:22px}}
.tip{{display:flex;gap:26px;align-items:center;background:{c['tile']};border-radius:22px;padding:22px 28px}}
.n{{flex:none;width:68px;height:68px;border-radius:50%;background:{ORANGE};color:{NAVY};font-weight:700;font-size:36px;display:flex;align-items:center;justify-content:center}}
.t{{font-weight:700;font-size:30px;line-height:1.25}}
.grid{{margin-top:50px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px}}
.grid div{{background:{c['tile']};border-radius:18px;padding:24px 18px;font-weight:700;font-size:28px;text-align:center}}
.footer{{position:absolute;left:0;right:0;bottom:0;height:150px;background:{ORANGE};color:{NAVY};display:flex;align-items:center;justify-content:space-between;padding:0 80px}}
.ph{{font-weight:700;font-size:48px}} .fs{{font-weight:700;font-size:22px}} .web{{font-weight:700;font-size:34px}}
"""

FOOT = '<div class="footer"><div><div class="fs">Call / WhatsApp</div><div class="ph">0300 1110826</div></div><div class="web">galaxymovers.pk</div></div>'

def build(g):
    c = theme(g["theme"])
    L = g["layout"]
    if L == "hero":
        body = f"""<div class="brand"><div class="dot"></div>GALAXY MOVERS</div>
        <div class="kicker">{g['kicker']}</div><h1>{g['h1']}</h1>
        <div class="chips">{''.join(f'<span>{x}</span>' for x in g['chips'])}</div>
        <div class="sub">{g['sub']}</div><div class="art">{art(g['art'], c)}</div>"""
    elif L == "list":
        body = f"""<div class="brand"><div class="dot"></div>{g['brand']}</div><h1 style="margin-top:50px;font-size:78px">{g['h1']}</h1>
        <div class="tips">{''.join(f'<div class="tip"><div class="n">{i+1}</div><div class="t">{x}</div></div>' for i,x in enumerate(g['items']))}</div>"""
    else:
        body = f"""<div class="brand"><div class="dot"></div>GALAXY MOVERS</div>
        <div class="kicker">{g['kicker']}</div><h1>{g['h1']}</h1>
        <div class="grid">{''.join(f'<div>{x}</div>' for x in g['areas'])}</div>"""
    return f"<html><head><style>{css(c)}</style></head><body><div class='card'>{body}{FOOT}</div></body></html>"

out = "/home/claude/galaxymovers-social/posts/"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1080})
    for post in POSTS:
        if post.get("existing"): continue
        pg.set_content(build(post["g"])); pg.wait_for_timeout(300)
        tmp = f"/home/claude/{post['slug']}.png"
        pg.screenshot(path=tmp)
        Image.open(tmp).convert("RGB").quantize(48).save(out + post["slug"] + ".png", optimize=True)
        print("made", post["slug"])
    b.close()
