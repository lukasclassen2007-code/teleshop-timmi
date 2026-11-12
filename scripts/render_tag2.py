"""Karussell 12.11.: Throwback-Cover, Fun-Fact, Altes Handy, Winter-Tipp (1080x1350).
Aufruf: python3 render_tag2.py tag.json ausgabeordner
"""
import json, os, sys
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, shadow, INK, AMBER, WHITE
import render_post as rp
from render_tarife import pill, cta, place_cat, CHECK, W, H, FOOT


def retro_phone(d, x, y, s, screen_text=None):
    """Einfaches, generisches Tasten-Handy (kein echtes Modell)."""
    w, h = 0.42 * s, s
    d.rounded_rectangle((x, y, x + w, y + h), radius=w * 0.28, fill=(60, 66, 80), outline=(20, 20, 24), width=max(2, int(s / 60)))
    d.rounded_rectangle((x + w * 0.14, y + h * 0.12, x + w * 0.86, y + h * 0.42), radius=w * 0.06, fill=(170, 200, 150))
    if screen_text:
        d.text((x + w / 2, y + h * 0.27), screen_text, font=font("Bold", int(s * 0.07)), fill=(40, 60, 40), anchor="mm")
    for r in range(4):
        for c in range(3):
            cx = x + w * (0.27 + c * 0.23)
            cy = y + h * (0.55 + r * 0.1)
            d.ellipse((cx - w * 0.07, cy - h * 0.03, cx + w * 0.07, cy + h * 0.03), fill=(200, 205, 215))


def slide_cover(c):
    img = gradient(W, H, (40, 36, 52), (14, 14, 16)).convert("RGBA")
    glow(img, 800, 980, 420, AMBER, 0.55)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for (x, y, sz, txt) in c.get("phones", [(70, 760, 330, "Hallo?"), (300, 860, 260, None)]):
        retro_phone(ld, x, y, sz, txt)
    img.alpha_composite(lay)
    place_cat(img, c["pose"], 560, cx=830, maxh=700, maxw=440)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, c["kicker"])
    cols = (WHITE, AMBER, WHITE)
    for i, t in enumerate(c["titel"]):
        d.text((46, 180 + i * 112), t, font=font("Bold", 104), fill=cols[i])
    y = 565
    for ln in wrap(d, c["text"], font("Medium", 34), 560):
        d.text((48, y), ln, font=font("Medium", 34), fill=(225, 225, 225))
        y += 46
    cta(d, c["cta"], 1170, fill=AMBER, col=INK)
    if c.get("hint", True):
        rp.draw_hint(d, "WISCHEN")
    rp.footer(d)
    return img.convert("RGB")


def slide_tip(tp):
    img = gradient(W, H, tuple(tp["bg"][0]), tuple(tp["bg"][1])).convert("RGBA")
    glow(img, 800, 950, 380, (255, 255, 255), 0.55)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, tp["kicker"])
    d.text((46, 176), tp["headline"], font=fit(d, tp["headline"], "Bold", 84, W - 96, 40), fill=INK)
    y = 290
    for ln in wrap(d, tp["sub"], font("Medium", 34), W - 110):
        d.text((48, y), ln, font=font("Medium", 34), fill=(50, 50, 60))
        y += 46
    y += 30
    for p in tp["punkte"]:
        lines = wrap(d, p, font("Bold", 31), 620)
        d.text((52, y), "✓", font=CHECK, fill=INK)
        for ln in lines:
            d.text((92, y + 2), ln, font=font("Bold", 31), fill=INK)
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
    rp.slide_fact({"funfact": data["funfact"]}).save(f"{out}/2_funfact.jpg", quality=92)
    slide_tip(data["schublade"]).save(f"{out}/3_altes_handy.jpg", quality=92)
    slide_tip(data["kaelte"]).save(f"{out}/4_kaelte.jpg", quality=92)
    print("ok")
