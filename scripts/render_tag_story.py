"""Animierte Story-Reihe 11.11. (3 × 7 s, 1080x1920, ohne Ton): GTA-Speed, Glasfaser, Haushalts-Check.
Aufruf: python3 render_tag_story.py tag.json ausgabeordner [1 2 3]
"""
import json, math, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, W, H
from timmi_lib import font, fit, wrap, gradient, glow, cat, shadow, INK, AMBER, WHITE

TEAL = (0, 140, 120)


def cta_bottom(img, t, text, t0=3.2, fill=AMBER, col=INK):
    a = ease((t - t0) / 0.5)
    pulse = 1 + 0.035 * math.sin(t * 5)
    layer(img, a, lambda dd: pill(dd, W / 2, 1600, text, round(36 * pulse), fill=fill, col=col))
    a = ease((t - t0 - 0.4) / 0.5)
    layer(img, a, lambda dd: dd.text((W / 2, 1712), "Poststraße 34 · Mo–Fr 9–17 Uhr", font=font("Bold", 36), fill=WHITE if fill == AMBER else INK, anchor="mt"))


# ---------- Story 1: GTA VI – Download lädt auf 100 %, dann "Bereit!" ----------
def make_story1(data):
    g = data["gta"]
    bg = gradient(W, H, (34, 22, 60), (12, 10, 20)).convert("RGBA")
    glow(bg, 820, 1300, 460, (255, 80, 170), 0.45)
    glow(bg, 200, 500, 420, (80, 160, 255), 0.35)
    c = cat(g["pose"], 640, 440)

    def frame(t):
        img = bg.copy()
        if t >= 2.9:
            p = ease((t - 2.9) / 0.8)
            x = W // 2 - c.width // 2 + round((1 - p) * 1200)
            img.alpha_composite(c, (x, 1540 - c.height))
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), g["titel"], font=fit(dd, g["titel"], "Bold", 84, W - 80, 50), fill=WHITE, anchor="mt"))
        a2 = ease((t - 0.6) / 0.5)
        layer(img, a2, lambda dd: dd.text((W / 2, 540), g["frage"], font=fit(dd, g["frage"], "Bold", 64, W - 80, 36), fill=AMBER, anchor="mt"))
        a3 = ease((t - 1.0) / 0.4)
        p = ease((t - 1.2) / 1.5)
        pct = round(100 * p) if t > 1.2 else 0

        def bar(dd):
            y = 700
            dd.rounded_rectangle((70, y, W - 70, y + 200), radius=34, fill=WHITE)
            dd.text((110, y + 34), "Download", font=font("Bold", 44), fill=INK)
            dd.text((W - 110, y + 34), f"{pct} %", font=font("Bold", 44), fill=(190, 0, 140), anchor="ra")
            dd.rounded_rectangle((110, y + 120, W - 110, y + 154), radius=17, fill=(230, 230, 236))
            if p > 0.01:
                dd.rounded_rectangle((110, y + 120, 110 + round((W - 220) * p), y + 154), radius=17, fill=AMBER)
        layer(img, a3, bar)
        q = back((t - 2.8) / 0.45)
        if q > 0:
            pill(ImageDraw.Draw(img), W / 2, 950, "✓ Bereit zum Zocken!".replace("✓ ", ""), max(10, round(44 * q)), fill=AMBER, col=INK)
        cta_bottom(img, t, g["cta"], t0=3.8)
        return img
    return frame


# ---------- Story 2: Glasfaser – Lichtpulse laufen durch die Faser ----------
def make_story2(data):
    g = data["glasfaser"]
    bg = gradient(W, H, (210, 244, 236), (60, 170, 150)).convert("RGBA")
    c = cat(g["pose"], 560, 520)
    # Faser-Kurve (Bezier) von links oben nach rechts unten zur Katze
    pts = []
    for k in range(200):
        s = k / 199
        x = (1 - s) ** 3 * -60 + 3 * (1 - s) ** 2 * s * 700 + 3 * (1 - s) * s ** 2 * 200 + s ** 3 * 820
        y = (1 - s) ** 3 * 900 + 3 * (1 - s) ** 2 * s * 860 + 3 * (1 - s) * s ** 2 * 1300 + s ** 3 * 1250
        pts.append((x, y))

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1300, 430, (255, 255, 255), 0.55)
        lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.line([(x * 2, y * 2) for x, y in pts], fill=(255, 255, 255, 170), width=20, joint="curve")
        for j in range(5):
            s = ((t * 0.45) + j * 0.2) % 1.0
            x, y = pts[int(s * 199)]
            for r, al in ((46, 60), (26, 140), (12, 255)):
                ld.ellipse((x * 2 - r, y * 2 - r, x * 2 + r, y * 2 + r), fill=(255, 220, 120, al))
        img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
        rs.put_cat(img, c, 800, 1560, 0.4, t, "pop")
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Glasfaser kommt?", font=font("Bold", 100), fill=INK, anchor="mt"))
        a2 = ease((t - 0.6) / 0.5)
        layer(img, a2, lambda dd: dd.text((W / 2, 560), "Wir helfen dir!", font=font("Bold", 84), fill=TEAL, anchor="mt"))
        for i, txt in enumerate(g["extras"]):
            p = back((t - 1.2 - i * 0.35) / 0.45)
            if p > 0:
                sz = max(10, round(40 * p))
                pill(ImageDraw.Draw(img), W / 2, 700 + i * 100, txt, sz, fill=WHITE, col=INK)
        cta_bottom(img, t, g["cta"], fill=INK, col=AMBER)
        return img
    return frame


# ---------- Story 3: Haushalts-Check – vier Kacheln ploppen auf ----------
def icon(d, kind, cx, cy, s, col):
    if kind == "strom":
        d.polygon([(cx + 0.1 * s, cy - 0.5 * s), (cx - 0.3 * s, cy + 0.08 * s), (cx - 0.02 * s, cy + 0.08 * s),
                   (cx - 0.12 * s, cy + 0.5 * s), (cx + 0.3 * s, cy - 0.1 * s), (cx + 0.02 * s, cy - 0.1 * s)], fill=col)
    elif kind == "gas":
        d.ellipse((cx - 0.28 * s, cy - 0.1 * s, cx + 0.28 * s, cy + 0.46 * s), fill=col)
        d.polygon([(cx, cy - 0.5 * s), (cx + 0.27 * s, cy + 0.12 * s), (cx - 0.27 * s, cy + 0.12 * s)], fill=col)
        d.ellipse((cx - 0.12 * s, cy + 0.12 * s, cx + 0.12 * s, cy + 0.36 * s), fill=WHITE)
    elif kind == "internet":
        w = max(4, int(s / 9))
        for r in (0.18, 0.34, 0.5):
            d.arc((cx - r * s, cy - r * s + 0.2 * s, cx + r * s, cy + r * s + 0.2 * s), 225, 315, fill=col, width=w)
        d.ellipse((cx - w, cy + 0.2 * s - w, cx + w, cy + 0.2 * s + w), fill=col)
    elif kind == "mobil":
        bw = s / 7
        for i in range(4):
            h = s * (0.25 + 0.2 * i)
            x = cx - s * 0.4 + i * bw * 1.6
            d.rounded_rectangle((x, cy + s * 0.4 - h, x + bw, cy + s * 0.4), radius=bw / 3, fill=col)


def make_story3(data):
    g = data["haushalt"]
    bg = gradient(W, H, (238, 230, 255), (150, 120, 240)).convert("RGBA")
    c = cat(g["pose"], 560, 520)
    tiles = [("strom", "Strom"), ("gas", "Gas"), ("internet", "Internet"), ("mobil", "Mobilfunk")]
    VIO = (110, 70, 220)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1300, round(430 + 25 * math.sin(t * 2.5)), (255, 255, 255), 0.55)
        rs.put_cat(img, c, W // 2, 1560, 0.4, t, "pop")
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Zahlst du zu viel?", font=font("Bold", 92), fill=INK, anchor="mt"))
        a2 = ease((t - 0.6) / 0.5)
        layer(img, a2, lambda dd: dd.text((W / 2, 545), "Timmi checkt deinen Haushalt", font=fit(dd, "Timmi checkt deinen Haushalt", "Bold", 58, W - 80, 36), fill=VIO, anchor="mt"))
        lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for i, (k, lab) in enumerate(tiles):
            p = back((t - 1.1 - i * 0.25) / 0.45)
            if p <= 0:
                continue
            cx = round(W / 2 + (i - 1.5) * 240) * 2
            cy = 760 * 2
            s = 200 * p * 2
            ld.rounded_rectangle((cx - s / 2, cy - s / 2 + 30, cx + s / 2, cy + s / 2 + 30), radius=s / 5, fill=(0, 0, 0, 35))
            ld.rounded_rectangle((cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), radius=s / 5, fill=WHITE)
            icon(ld, k, cx, cy - s * 0.12, s * 0.5, VIO)
            if p > 0.9:
                ld.text((cx, cy + s * 0.3), lab, font=font("Bold", 50), fill=INK, anchor="mm")
        img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 900), "Bring einfach deine Rechnungen mit!", font=fit(dd, "Bring einfach deine Rechnungen mit!", "Medium", 44, W - 100, 30), fill=INK, anchor="mt"))
        cta_bottom(img, t, g["cta"], fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    rs.OUT = sys.argv[2]
    todo = sys.argv[3:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_gta", make_story1(data))
    if "2" in todo: rs.write("story_2_glasfaser", make_story2(data))
    if "3" in todo: rs.write("story_3_haushalt", make_story3(data))
