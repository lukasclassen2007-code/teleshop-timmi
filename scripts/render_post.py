"""Rendert Instagram-Karussells (2 Bilder je Tag, 1080x1350 JPEG) aus einer Wochen-JSON.
Bild 1: Tipp-Szene passend zum Thema · Bild 2: Timmis Fun-Fact
Aufruf: python3 render_post.py woche.json ausgabeordner
"""
import json, sys, os
from PIL import Image, ImageDraw
from timmi_lib import (font, fit, wrap, gradient, glow, logo, cat, shadow, draw_deco, chevron,
                       THEMES, INK, AMBER, WHITE, GREY, HOURS, ADDRESS)

W, H, FOOT = 1080, 1350, 72
STAGE = (0, 330, W, H - FOOT)


def header(img, d, kicker, headline, sub, dark=False):
    img.alpha_composite(logo(54), (48, 40))
    kf = font("Bold", 24)
    kw = d.textlength(kicker, font=kf)
    d.rounded_rectangle((48, 118, 48 + kw + 36, 162), radius=22, fill=AMBER)
    d.text((66, 140), kicker, font=kf, fill=INK, anchor="lm")
    hf = fit(d, headline, "Bold", 76, W - 96)
    d.text((46, 176), headline, font=hf, fill=WHITE if dark else INK)
    if sub:
        sf = fit(d, sub, "Medium", 34, W - 96, minsize=24)
        d.text((48, 176 + hf.size + 16), sub, font=sf, fill=(210, 210, 210) if dark else GREY)


def footer(d):
    d.rectangle((0, H - FOOT, W, H), fill=INK)
    ff = font("Medium", 26)
    d.text((48, H - FOOT / 2), "Teleshop Timmendorfer Strand", font=ff, fill=WHITE, anchor="lm")
    d.text((W - 48, H - FOOT / 2), f"{ADDRESS} · {HOURS}", font=ff, fill=AMBER, anchor="rm")


def slide_tip(p, hint=True):
    img = gradient(W, H, *THEMES[p["theme"]]).convert("RGBA")
    glow(img, W // 2, 860, 420, (255, 255, 255), 0.6)
    draw_deco(img, p["theme"], STAGE)
    c = cat(p["pose"], 860, 840)
    cx, by = W // 2, H - FOOT - 28
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    header(img, d, p["kicker"], p["headline"], p["sub"])
    # Hinweis auf zweites Bild
    if hint:
        draw_hint(d)
    footer(d)
    return img.convert("RGB")


def draw_hint(d, label="FUN-FACT"):
    tf = font("Bold", 22)
    lw = d.textlength(label, font=tf)
    x1 = W - 48
    d.rounded_rectangle((x1 - lw - 70, 44, x1, 90), radius=23, fill=INK)
    d.text((x1 - lw - 46, 67), label, font=tf, fill=AMBER, anchor="lm")
    chevron(d, x1 - 32, 67, 16, AMBER)


def slide_fact(p, pose="03_idee"):
    img = Image.new("RGBA", (W, H), (20, 20, 22, 255))
    glow(img, 800, 1010, 360, AMBER, 0.85)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    kf = font("Bold", 24)
    kt = "TIMMIS FUN-FACT"
    kw = d.textlength(kt, font=kf)
    d.rounded_rectangle((48, 118, 48 + kw + 36, 162), radius=22, fill=AMBER)
    d.text((66, 140), kt, font=kf, fill=INK, anchor="lm")
    d.text((46, 180), "Wusstest du?", font=font("Bold", 64), fill=WHITE)
    bf = fit(d, p["funfact"]["big"], "Bold", 170, W - 96, minsize=90)
    d.text((40, 270), p["funfact"]["big"], font=bf, fill=AMBER)
    tf = font("Medium", 42)
    y = 270 + bf.size + 40
    for line in wrap(d, p["funfact"]["text"], tf, W - 110):
        d.text((48, y), line, font=tf, fill=WHITE)
        y += 58
    by = H - FOOT - 20
    c = cat(pose, 560, min(640, by - y - 20))
    cx = 800
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    footer(d)
    return img.convert("RGB")


if __name__ == "__main__":
    posts = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for p in posts:
        stem = os.path.join(out, p["datum"])
        slide_tip(p).save(stem + "_1_tipp.jpg", "JPEG", quality=92)
        slide_fact(p).save(stem + "_2_funfact.jpg", "JPEG", quality=92)
        print(stem)
