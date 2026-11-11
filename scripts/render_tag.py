"""Themen-Karussell (1080x1350) für einen Tag: Cover, Glasfaser, GTA-Speed, Haushalts-Check, Tipp, Fun-Fact.
Aufruf: python3 render_tag.py tag.json ausgabeordner
"""
import json, os, sys
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, shadow, INK, AMBER, WHITE, GREY
import render_post as rp
from render_tarife import pill, card, checks, cta, place_cat, CHECK, W, H, FOOT

TEAL = (0, 140, 120)


def slide_cover(c):
    img = gradient(W, H, (40, 36, 52), (14, 14, 16)).convert("RGBA")
    glow(img, 790, 980, 420, AMBER, 0.55)
    k = cat("01_winken", 420, 640)
    img.alpha_composite(k, (830 - k.width // 2, H - FOOT - 20 - k.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, c["kicker"])
    cols = (WHITE, AMBER, WHITE)
    for i, t in enumerate(c["titel"]):
        d.text((46, 180 + i * 112), t, font=font("Bold", 104), fill=cols[i])
    y = 640
    for a, b in c["punkte"]:
        d.rounded_rectangle((48, y, 600, y + 90), radius=26, fill=WHITE)
        d.text((76, y + 12), a, font=font("Bold", 30), fill=INK)
        d.text((76, y + 52), b, font=font("Bold", 22), fill=(200, 110, 0))
        y += 102
    rp.draw_hint(d)
    rp.footer(d)
    return img.convert("RGB")


def slide_topic(g):
    img = gradient(W, H, tuple(g["bg"][0]), tuple(g["bg"][1])).convert("RGBA")
    glow(img, 800, 900, 380, (255, 255, 255), 0.55)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, g["kicker"])
    d.text((46, 176), g["typ"], font=fit(d, g["typ"], "Bold", 56, W - 96, 34), fill=INK)
    y1 = card(img, d, 48, 280, 600, g["card_top"], g["card_big"], g["card_text"], TEAL if g["id"] == "glasfaser" else (120, 80, 220))
    y = checks(d, y1 + 30, g["extras"])
    cta(d, g["cta"], y + 20)
    place_cat(img, g["pose"], y + 20 + 52)
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


def slide_gta(g):
    img = gradient(W, H, (34, 22, 60), (12, 10, 20)).convert("RGBA")
    glow(img, 860, 1060, 380, (255, 80, 170), 0.45)
    glow(img, 200, 300, 360, (80, 160, 255), 0.35)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, g["kicker"])
    d.text((46, 176), g["titel"], font=fit(d, g["titel"], "Bold", 76, W - 96, 40), fill=WHITE)
    d.text((48, 270), g["frage"], font=fit(d, g["frage"], "Bold", 52, W - 96, 30), fill=AMBER)
    d.text((48, 370), g["label"], font=font("Medium", 30), fill=(210, 210, 210))
    y = 430
    for speed, zeit, frac in g["zeilen"]:
        d.rounded_rectangle((48, y, 1032, y + 120), radius=28, fill=(255, 255, 255, 255))
        d.text((80, y + 30), speed, font=font("Bold", 36), fill=INK)
        d.text((1000, y + 30), zeit, font=font("Bold", 36), fill=INK, anchor="ra")
        d.rounded_rectangle((80, y + 82, 1000, y + 100), radius=9, fill=(230, 230, 236))
        d.rounded_rectangle((80, y + 82, 80 + round(920 * frac), y + 100), radius=9, fill=AMBER)
        y += 140
    k = cat(g["pose"], 470, H - FOOT - 30 - (y + 120))
    img.alpha_composite(k, (800 - k.width // 2, H - FOOT - 30 - k.height))
    d = ImageDraw.Draw(img)
    pill(d, 48, y + 20, g["cta"], 28)
    yy = y + 100
    for ln in wrap(d, g["hinweis"], font("Regular", 20), 520):
        d.text((48, yy), ln, font=font("Regular", 20), fill=(190, 190, 190))
        yy += 26
    rp.footer(d)
    return img.convert("RGB")


def slide_tip(tp):
    img = gradient(W, H, (226, 240, 255), (130, 180, 255)).convert("RGBA")
    glow(img, 800, 950, 380, (255, 255, 255), 0.55)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, tp["kicker"])
    d.text((46, 176), tp["headline"], font=fit(d, tp["headline"], "Bold", 84, W - 96, 40), fill=INK)
    y = 290
    for ln in wrap(d, tp["sub"], font("Medium", 36), W - 110):
        d.text((48, y), ln, font=font("Medium", 36), fill=(50, 50, 60))
        y += 48
    y += 30
    for p in tp["punkte"]:
        lines = wrap(d, p, font("Bold", 32), 600)
        d.text((52, y), "✓", font=CHECK, fill=INK)
        for ln in lines:
            d.text((92, y + 2), ln, font=font("Bold", 32), fill=INK)
            y += 42
        y += 16
    cta(d, tp["cta"], y + 14)
    place_cat(img, tp["pose"], y + 14 + 52)
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slide_cover(data["cover"]).save(f"{out}/1_cover.jpg", quality=92)
    slide_topic(data["glasfaser"]).save(f"{out}/2_glasfaser.jpg", quality=92)
    slide_gta(data["gta"]).save(f"{out}/3_gta.jpg", quality=92)
    slide_topic(data["haushalt"]).save(f"{out}/4_haushalt.jpg", quality=92)
    slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}).save(f"{out}/6_funfact.jpg", quality=92)
    print("ok")
