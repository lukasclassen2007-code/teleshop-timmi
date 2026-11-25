"""Karussell 25.11.: Themen, Weihnachtsstimmung im Shop, Weihnachtsberatung, Fun-Fact 1882, Foto-Tipp."""
import json, os, sys, math, random
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, INK, AMBER, WHITE
import render_post as rp
import render_tag as rt
import render_tag2 as r2
from render_tag4 import slide_einsatz
from render_tarife import pill, cta, W, H, FOOT

BULBS = [(255, 80, 80), (255, 200, 60), (90, 200, 120), (90, 160, 255), (255, 140, 220)]


def garland(img, y0, x0=0, x1=W, sag=60, n=14, t=0.0):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    pts = [(x0 + (x1 - x0) * i / 60, y0 + sag * math.sin(math.pi * ((i / 60 * 3) % 1))) for i in range(61)]
    d.line(pts, fill=(40, 60, 40), width=5)
    for k in range(n):
        u = (k + 0.5) / n
        x = x0 + (x1 - x0) * u
        y = y0 + sag * math.sin(math.pi * ((u * 3) % 1)) + 16
        col = BULBS[k % len(BULBS)]
        on = 0.6 + 0.4 * math.sin(t * 4 + k * 1.3)
        glow(img, round(x), round(y), 46, col, 0.35 * on)
        d.ellipse((x - 11, y - 16, x + 11, y + 16), fill=col)
        d.rectangle((x - 6, y - 24, x + 6, y - 14), fill=(60, 60, 60))
    img.alpha_composite(lay)


def tree(img, cx, base, h, t=0.0):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle((cx - h * 0.06, base - h * 0.1, cx + h * 0.06, base), fill=(110, 70, 40))
    for i, (w, top) in enumerate(((0.62, 0.55), (0.5, 0.33), (0.36, 0.1))):
        yb = base - h * 0.08 - i * h * 0.22
        d.polygon([(cx - h * w / 2, yb), (cx + h * w / 2, yb), (cx, base - h + h * top * 0.0 - (0 if i < 2 else 0) + h * (0.45 - i * 0.2) * 0 + (base - h - (base - h)) )], fill=(40, 130, 70))
    # sauberer Baum: drei Dreiecke
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle((cx - h * 0.06, base - h * 0.12, cx + h * 0.06, base), fill=(110, 70, 40))
    tiers = [(base - h * 0.1, base - h * 0.55, 0.62), (base - h * 0.35, base - h * 0.78, 0.48), (base - h * 0.58, base - h * 0.98, 0.34)]
    for yb, yt, w in tiers:
        d.polygon([(cx - h * w / 2, yb), (cx + h * w / 2, yb), (cx, yt)], fill=(40, 130, 70))
    rnd = random.Random(5)
    for k in range(16):
        yy = base - h * rnd.uniform(0.15, 0.85)
        frac = (base - h * 0.1 - yy) / (h * 0.9)
        half = h * 0.3 * (1 - frac) * 0.9
        xx = cx + rnd.uniform(-half, half)
        col = BULBS[k % len(BULBS)]
        on = 0.6 + 0.4 * math.sin(t * 4 + k)
        glow(img, round(xx), round(yy), 26, col, 0.3 * on)
        d.ellipse((xx - 9, yy - 9, xx + 9, yy + 9), fill=col)
    s = h * 0.07
    sy = base - h * 0.98
    pts = []
    for i in range(10):
        r = s if i % 2 == 0 else s * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), sy + r * math.sin(a)))
    d.polygon(pts, fill=AMBER)
    img.alpha_composite(lay)


def snow_static(img, n=70, seed=3):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rnd = random.Random(seed)
    for _ in range(n):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H - FOOT), rnd.uniform(3, 8)
        if x < 980 and 180 < y < 760:
            continue
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 190))
    img.alpha_composite(lay)


def slide_stimmung(s):
    img = gradient(W, H, (28, 36, 70), (10, 12, 26)).convert("RGBA")
    snow_static(img)
    glow(img, 780, 1050, 420, AMBER, 0.45)
    garland(img, 20, sag=70, n=16)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 130))
    pill(d, 48, 205, s["kicker"])
    d.text((46, 265), s["headline"][0], font=font("Bold", 80), fill=WHITE)
    d.text((46, 355), s["headline"][1], font=fit(d, s["headline"][1], "Bold", 80, W - 90, 50), fill=AMBER)
    y = 475
    for ln in wrap(d, s["text"], font("Medium", 34), 600):
        d.text((48, y), ln, font=font("Medium", 34), fill=(225, 225, 235))
        y += 46
    cta(d, s["cta"], y + 26, fill=AMBER, col=INK)
    tree(img, 240, H - FOOT - 30, 430)
    c = cat("15_advent", 440, 620)
    img.alpha_composite(c, (W - 40 - c.width, H - FOOT - 10 - c.height))
    # Schneedecke unten
    d = ImageDraw.Draw(img)
    d.ellipse((-200, H - FOOT - 50, W + 200, H - FOOT + 120), fill=(240, 246, 255))
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    slide_stimmung(data["stimmung"]).save(f"{out}/2_weihnachtsstimmung.jpg", quality=92)
    slide_einsatz(data["beratung"]).save(f"{out}/3_beratung.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="03_idee", kicker="TIMMIS FUN-FACT").save(f"{out}/4_funfact.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    print("ok")
