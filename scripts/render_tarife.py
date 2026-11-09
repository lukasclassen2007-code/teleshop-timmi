"""Tarif-Portfolio als Karussell (1080x1350): Cover, Wenig-/Gelegenheits-/Vielsurfer, Familienspezial, Fun-Fact.
Aufruf: python3 render_tarife.py tarife.json ausgabeordner
"""
import json, os, sys
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, shadow, INK, AMBER, WHITE, GREY
import render_post as rp

W, H, FOOT = 1080, 1350, 72
RED = (230, 0, 0)


def pill(d, x, y, text, size=24, fill=AMBER, col=INK, center=False):
    f = font("Bold", size)
    w = d.textlength(text, font=f) + size * 1.5
    h = size * 1.85
    if center:
        x -= w / 2
    d.rounded_rectangle((x, y, x + w, y + h), radius=h / 2, fill=fill)
    d.text((x + w / 2, y + h / 2), text, font=f, fill=col, anchor="mm")
    return w


def footnote(img, text, y_bottom, dark=False):
    d = ImageDraw.Draw(img)
    f = font("Regular", 17)
    lines = wrap(d, "* " + text, f, W - 96)
    y = y_bottom - len(lines) * 22
    for ln in lines:
        d.text((48, y), ln, font=f, fill=(200, 200, 200) if dark else (70, 70, 70))
        y += 22
    return y_bottom - len(lines) * 22


def snow(img, n=40, seed=5):
    import random
    random.seed(seed)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H - 200), random.uniform(3, 9)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, random.randint(120, 220)))
    img.alpha_composite(lay)


def slide_cover(data):
    img = gradient(W, H, (40, 36, 52), (14, 14, 16)).convert("RGBA")
    glow(img, 760, 980, 420, AMBER, 0.55)
    c = cat("03_idee", 560, 700)
    img.alpha_composite(c, (770 - c.width // 2, H - FOOT - 20 - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, "BLACK WEEK · 10.11.–15.12.")
    d.text((46, 180), "Welcher", font=font("Bold", 110), fill=WHITE)
    d.text((46, 300), "Surfer-Typ", font=font("Bold", 110), fill=AMBER)
    d.text((46, 420), "bist du?", font=font("Bold", 110), fill=WHITE)
    y = 600
    for g in data["gruppen"]:
        d.rounded_rectangle((48, y, 520, y + 96), radius=26, fill=(255, 255, 255, 255))
        d.text((76, y + 14), g["kicker"].title(), font=font("Bold", 30), fill=INK)
        d.text((76, y + 54), f'{g["daten"]} · ab {g["preis_fest"] or g["preis"]}*', font=font("Medium", 24), fill=GREY)
        y += 116
    d.text((48, y + 10), "Wisch dich durch und finde", font=font("Medium", 32), fill=(220, 220, 220))
    d.text((48, y + 52), "deinen Tarif!", font=font("Medium", 32), fill=(220, 220, 220))
    rp.draw_hint(d)
    rp.footer(d)
    footnote(img, "Details und Bedingungen auf den folgenden Bildern.", H - FOOT - 14, dark=True)
    return img.convert("RGB")


def slide_group(g, aktion):
    img = gradient(W, H, tuple(g["bg"][0]), tuple(g["bg"][1])).convert("RGBA")
    glow(img, 790, 900, 380, (255, 255, 255), 0.55)
    # Fußnote zuerst messen, damit Katze und Karte darüber Platz haben
    probe = Image.new("RGBA", (W, H))
    top_note = footnote(probe, g["fuss"], H - FOOT - 14)
    c = cat(g["pose"], 470, top_note - 640)
    cx, by = 800, top_note - 20
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, g["kicker"])
    d.text((46, 176), g["typ"], font=fit(d, g["typ"], "Bold", 52, W - 96, 34), fill=INK)
    # Tarifkarte
    x0, y0, x1 = 48, 280, 600
    y1 = y0 + (560 if g["preis_fest"] else 470)
    d.rounded_rectangle((x0 + 6, y0 + 12, x1 + 6, y1 + 12), radius=36, fill=(0, 0, 0, 40))
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=WHITE)
    d.text((x0 + 36, y0 + 34), g["marke"], font=font("Bold", 28), fill=RED if g["marke"] == "Vodafone" else GREY)
    d.text((x0 + 36, y0 + 70), g["tarif"], font=fit(d, g["tarif"], "Bold", 40, x1 - x0 - 72, 28), fill=INK)
    d.text((x0 + 32, y0 + 130), g["daten"], font=fit(d, g["daten"], "Bold", 110, x1 - x0 - 64, 60), fill=INK)
    if g["daten_alt"]:
        d.text((x0 + 36, y0 + 260), g["daten_alt"], font=font("Medium", 30), fill=GREY)
    d.line((x0 + 36, y0 + 315, x1 - 36, y0 + 315), fill=(225, 225, 225), width=2)
    d.text((x0 + 36, y0 + 335), g["preis"] + "*", font=font("Bold", 72), fill=INK)
    d.text((x0 + 36, y0 + 420), "pro Monat", font=font("Medium", 26), fill=GREY)
    if g["preis_fest"]:
        d.rounded_rectangle((x0 + 24, y0 + 465, x1 - 24, y0 + 540), radius=20, fill=RED)
        d.text(((x0 + x1) / 2, y0 + 486), "Vodafone-Festnetzkunden nur", font=font("Medium", 22), fill=WHITE, anchor="mm")
        d.text(((x0 + x1) / 2, y0 + 518), g["preis_fest"] + "*", font=font("Bold", 34), fill=WHITE, anchor="mm")
    y = y1 + 26
    for e in g["extras"]:
        d.text((52, y), "✓", font=ImageFont_check(), fill=INK)
        d.text((92, y + 2), e, font=font("Bold", 30), fill=INK)
        y += 48
    footnote(img, g["fuss"], H - FOOT - 14)
    rp.footer(d)
    return img.convert("RGB")


def ImageFont_check():
    from PIL import ImageFont
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)


def slide_family(f):
    img = gradient(W, H, (150, 20, 30), (60, 8, 14)).convert("RGBA")
    glow(img, 780, 900, 420, (255, 200, 120), 0.5)
    snow(img)
    probe = Image.new("RGBA", (W, H))
    top_note = footnote(probe, f["fuss"], H - FOOT - 14, dark=True)
    c = cat(f["pose"], 480, top_note - 600)
    cx, by = 800, top_note - 20
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, f["kicker"])
    d.text((46, 180), f["headline"], font=font("Bold", 64), fill=WHITE)
    d.text((44, 252), f["headline2"], font=font("Bold", 120), fill=AMBER)
    d.text((48, 392), f["sub"], font=font("Medium", 40), fill=WHITE)
    x0, y0, x1, y1 = 48, 480, 600, 850
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=WHITE)
    d.text((x0 + 36, y0 + 30), "Vodafone", font=font("Bold", 28), fill=RED)
    d.text((x0 + 36, y0 + 66), "2 Karten · Unlimited", font=font("Bold", 38), fill=INK)
    d.text((x0 + 36, y0 + 124), "nur", font=font("Medium", 32), fill=GREY)
    d.text((x0 + 32, y0 + 160), f["preis"] + "*", font=font("Bold", 92), fill=INK)
    d.text((x0 + 36, y0 + 272), f["preis_info"] + ",", font=font("Medium", 24), fill=GREY)
    d.text((x0 + 36, y0 + 304), f["hinweis"], font=fit(d, f["hinweis"], "Medium", 24, x1 - x0 - 72, 18), fill=GREY)
    y = y1 + 26
    for e in f["extras"]:
        d.text((52, y), "✓", font=ImageFont_check(), fill=WHITE)
        d.text((92, y + 2), e, font=font("Bold", 30), fill=WHITE)
        y += 48
    footnote(img, f["fuss"], H - FOOT - 14, dark=True)
    rp.footer(d)
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slide_cover(data).save(f"{out}/1_cover.jpg", quality=92)
    for i, g in enumerate(data["gruppen"]):
        slide_group(g, data["aktion"]).save(f"{out}/{i + 2}_{g['id']}.jpg", quality=92)
    slide_family(data["familie"]).save(f"{out}/5_familie.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}).save(f"{out}/6_funfact.jpg", quality=92)
    print("ok")
