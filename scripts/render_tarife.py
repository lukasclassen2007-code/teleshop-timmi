"""Tarif-Portfolio als Karussell (1080x1350) – ohne Preise, im Timmi-Stil.
Bilder: Cover, Wenig-/Gelegenheits-/Vielsurfer, Familienspezial, Sicherheits-Tipp, Fun-Fact.
Aufruf: python3 render_tarife.py tarife.json ausgabeordner
"""
import json, os, sys, random
from PIL import Image, ImageDraw, ImageFont
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, shadow, INK, AMBER, WHITE, GREY
import render_post as rp

W, H, FOOT = 1080, 1350, 72
RED = (230, 0, 0)
CHECK = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)


def pill(d, x, y, text, size=24, fill=AMBER, col=INK, center=False):
    f = font("Bold", size)
    w = d.textlength(text, font=f) + size * 1.5
    h = size * 1.85
    if center:
        x -= w / 2
    d.rounded_rectangle((x, y, x + w, y + h), radius=h / 2, fill=fill)
    d.text((x + w / 2, y + h / 2), text, font=f, fill=col, anchor="mm")
    return w


def snow(img, n=40, seed=5):
    random.seed(seed)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H - 200), random.uniform(3, 9)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, random.randint(120, 220)))
    img.alpha_composite(lay)


def card(img, d, x0, y0, x1, top, big, text, top_col=GREY):
    f_text = font("Medium", 30)
    lines = wrap(d, text, f_text, x1 - x0 - 72)
    fb = font("Bold", 96)
    big_lines = [big] if d.textlength(big, font=fb) <= x1 - x0 - 64 else None
    if big_lines is None:
        fb = font("Bold", 62)
        big_lines = wrap(d, big, fb, x1 - x0 - 64)
    big_h = fb.size + 16
    y_text = y0 + 84 + len(big_lines) * big_h + 22
    y1 = y_text + len(lines) * 40 + 30
    d.rounded_rectangle((x0 + 6, y0 + 12, x1 + 6, y1 + 12), radius=36, fill=(0, 0, 0, 40))
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=WHITE)
    d.text((x0 + 36, y0 + 34), top, font=font("Bold", 28), fill=top_col)
    for i, bl in enumerate(big_lines):
        d.text((x0 + 32, y0 + 78 + i * big_h), bl, font=fb, fill=INK)
    y = y_text
    for ln in lines:
        d.text((x0 + 36, y), ln, font=f_text, fill=(70, 70, 70))
        y += 40
    return y1


def checks(d, y, items, col=INK):
    for e in items:
        d.text((52, y), "✓", font=CHECK, fill=col)
        d.text((92, y + 2), e, font=font("Bold", 30), fill=col)
        y += 48
    return y


def cta(d, text, y, fill=INK, col=AMBER):
    pill(d, 48, y, text, 28, fill=fill, col=col)


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
    for g in data["gruppen"] + [{"kicker": "FAMILIE", "kurz": "Unbegrenzt für die Familie"}]:
        d.rounded_rectangle((48, y, 600, y + 98), radius=26, fill=WHITE)
        d.text((76, y + 16), g["kicker"].title(), font=font("Bold", 30), fill=INK)
        d.text((76, y + 58), g["kurz"], font=font("Bold", 22), fill=(200, 110, 0))
        y += 110
    d.text((48, y + 14), "Wisch dich durch und", font=font("Medium", 32), fill=(220, 220, 220))
    d.text((48, y + 56), "finde deinen Tarif!", font=font("Medium", 32), fill=(220, 220, 220))
    rp.draw_hint(d)
    rp.footer(d)
    return img.convert("RGB")


def place_cat(img, pose, text_bottom, cx=810, maxh=560, maxw=470):
    """Katze unter den Text oder rechts daneben – je nachdem, wo sie größer wird."""
    by = H - FOOT - 30
    below = cat(pose, maxw, max(60, min(maxh, by - text_bottom - 24)))
    side = cat(pose, 360, min(640, by - 330))
    if side.height > below.height * 1.15 and cx == 810:
        c, cx = side, 870
    else:
        c = below
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))


def slide_group(g):
    img = gradient(W, H, tuple(g["bg"][0]), tuple(g["bg"][1])).convert("RGBA")
    glow(img, 800, 900, 380, (255, 255, 255), 0.55)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, g["kicker"])
    d.text((46, 176), g["typ"], font=fit(d, g["typ"], "Bold", 56, W - 96, 34), fill=INK)
    top_col = RED if "Vodafone" in g["card_top"] else (200, 110, 0)
    y1 = card(img, d, 48, 280, 600, g["card_top"], g["card_big"], g["card_text"], top_col)
    y = checks(d, y1 + 30, g["extras"])
    cta(d, g["cta"], y + 20)
    place_cat(img, g["pose"], y + 20 + 52)
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


def slide_family(f):
    img = gradient(W, H, (150, 20, 30), (60, 8, 14)).convert("RGBA")
    glow(img, 790, 900, 420, (255, 200, 120), 0.5)
    snow(img)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, f["kicker"])
    d.text((46, 176), f["headline"], font=fit(d, f["headline"], "Bold", 62, W - 96, 34), fill=WHITE)
    d.text((46, 252), f["headline2"], font=fit(d, f["headline2"], "Bold", 62, W - 96, 34), fill=AMBER)
    y1 = card(img, d, 48, 360, 600, f["card_top"], f["card_big"], f["card_text"], RED)
    y = checks(d, y1 + 30, f["extras"], WHITE)
    cta(d, f["cta"], y + 20, fill=AMBER, col=INK)
    place_cat(img, f["pose"], 360, cx=905, maxh=700, maxw=310)
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


def slide_tip(tp):
    img = gradient(W, H, (255, 228, 214), (255, 150, 110)).convert("RGBA")
    glow(img, 800, 950, 380, (255, 255, 255), 0.55)
    c = cat(tp["pose"], 340, 440)
    cx, by = 880, H - FOOT - 30
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, tp["kicker"])
    d.text((46, 176), tp["headline"], font=fit(d, tp["headline"], "Bold", 76, W - 96, 40), fill=INK)
    y = 280
    for ln in wrap(d, tp["sub"], font("Medium", 34), W - 110):
        d.text((48, y), ln, font=font("Medium", 34), fill=(60, 60, 60))
        y += 46
    # drei gefälschte App-Icons mit rotem Kreuz
    y += 30
    for i, a in enumerate(tp["apps"]):
        x = 60 + i * 190
        d.rounded_rectangle((x + 4, y + 8, x + 154, y + 158), radius=36, fill=(0, 0, 0, 40))
        d.rounded_rectangle((x, y, x + 150, y + 150), radius=36, fill=WHITE)
        d.text((x + 75, y + 75), a, font=fit(d, a, "Bold", 44, 120, 26), fill=INK, anchor="mm")
        d.ellipse((x + 110, y - 20, x + 170, y + 40), fill=RED)
        d.line((x + 126, y - 4, x + 154, y + 24), fill=WHITE, width=7)
        d.line((x + 154, y - 4, x + 126, y + 24), fill=WHITE, width=7)
    y += 200
    for p in tp["punkte"]:
        lines = wrap(d, p, font("Bold", 30), 560)
        d.text((52, y), "✓", font=CHECK, fill=INK)
        for ln in lines:
            d.text((92, y + 2), ln, font=font("Bold", 30), fill=INK)
            y += 40
        y += 12
    cta(d, tp["cta"], y + 14)
    rp.footer(d)
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".jpg") and not f.startswith("story"):
            os.remove(os.path.join(out, f))
    slide_cover(data).save(f"{out}/1_cover.jpg", quality=92)
    for i, g in enumerate(data["gruppen"]):
        slide_group(g).save(f"{out}/{i + 2}_{g['id']}.jpg", quality=92)
    slide_family(data["familie"]).save(f"{out}/5_familie.jpg", quality=92)
    slide_tip(data["tipp"]).save(f"{out}/6_tipp.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}).save(f"{out}/7_funfact.jpg", quality=92)
    print("ok")
