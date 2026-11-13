"""Karussell 13.11.: Themen, Fun-Fact Freitag der 13., 5G-Router, Einsatzorte, Wochenend-Tipp.
Aufruf: python3 render_tag4.py tag.json ausgabeordner
"""
import json, os, sys
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, INK, AMBER, WHITE
import render_post as rp
import render_tag as rt
import render_tag2 as r2
import math
from render_tarife import pill, cta, place_cat, W, H, FOOT

BLUE = (20, 110, 210)


def router_icon(d, cx, cy, s, t=0.0, waves=3):
    """Generischer 5G-Router mit Kabel zur Steckdose und WLAN-Wellen."""
    w, h = s, s * 0.62
    x0, y0 = cx - w / 2, cy - h / 2
    # Antennen
    for ax in (x0 + w * 0.18, x0 + w * 0.82):
        d.rounded_rectangle((ax - s * 0.03, y0 - s * 0.32, ax + s * 0.03, y0 + 6), radius=s * 0.03, fill=(235, 238, 245), outline=INK, width=4)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=s * 0.1, fill=WHITE, outline=INK, width=5)
    d.text((cx, y0 + h * 0.42), "5G", font=font("Bold", int(s * 0.26)), fill=BLUE, anchor="mm")
    for k in range(4):
        lx = x0 + w * (0.3 + k * 0.13)
        on = (math.sin(t * 6 + k) > -0.3)
        d.ellipse((lx - 7, y0 + h * 0.8 - 7, lx + 7, y0 + h * 0.8 + 7), fill=(60, 200, 110) if on else (190, 200, 190))
    # WLAN-Wellen
    wx, wy = cx, y0 - s * 0.12
    for k in range(waves):
        r = s * (0.12 + 0.1 * k)
        a = 255 if t == 0 else int(255 * (0.4 + 0.6 * max(0.0, math.sin(t * 4 - k * 0.9))))
        d.arc((wx - r, wy - r, wx + r, wy + r), 225, 315, fill=BLUE + (a,), width=max(6, int(s * 0.045)))
    d.ellipse((wx - s * 0.035, wy - s * 0.035, wx + s * 0.035, wy + s * 0.035), fill=BLUE)
    # Kabel und Steckdose
    sx, sy = x0 - s * 0.32, cy + h * 0.25
    d.line([(x0 + w * 0.1, y0 + h), (x0 + w * 0.1, sy), (sx + s * 0.12, sy)], fill=INK, width=6)
    r = s * 0.16
    d.rounded_rectangle((sx - r, sy - r, sx + r, sy + r), radius=r * 0.35, fill=WHITE, outline=INK, width=4)
    d.ellipse((sx - r * 0.7, sy - r * 0.7, sx + r * 0.7, sy + r * 0.7), outline=(150, 150, 160), width=4)
    for dx in (-0.28, 0.28):
        d.ellipse((sx + r * dx - 6, sy - 6, sx + r * dx + 6, sy + 6), fill=INK)


def slide_router(g):
    img = rt.slide_topic(g).convert("RGBA")
    d = ImageDraw.Draw(img)
    router_icon(d, 340, 1110, 260)
    return img.convert("RGB")


def slide_einsatz(e):
    bg = e.get("bg", [[230, 244, 255], [120, 180, 240]])
    col = tuple(e.get("col", BLUE))
    img = gradient(W, H, tuple(bg[0]), tuple(bg[1])).convert("RGBA")
    glow(img, 540, 1000, 420, (255, 255, 255), 0.5)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, e["kicker"])
    d.text((46, 176), e["headline"], font=fit(d, e["headline"], "Bold", 84, W - 96, 40), fill=INK)
    y = 300
    if e.get("sub"):
        for ln in wrap(d, e["sub"], font("Medium", 34), W - 100):
            d.text((48, y - 10), ln, font=font("Medium", 34), fill=(50, 50, 60))
            y += 46
        y += 20
    for i, (t, txt) in enumerate(e["faelle"]):
        d.rounded_rectangle((48, y, W - 48, y + 205), radius=30, fill=WHITE)
        d.ellipse((78, y + 52, 178, y + 152), fill=col)
        d.text((128, y + 102), str(i + 1), font=font("Bold", 56), fill=WHITE, anchor="mm")
        d.text((210, y + 30), t, font=font("Bold", 44), fill=INK)
        yy = y + 92
        for ln in wrap(d, txt, font("Medium", 30), W - 48 - 210 - 40):
            d.text((210, yy), ln, font=font("Medium", 30), fill=(60, 60, 70))
            yy += 40
        y += 235
    # Drei Schritte
    y += 25
    if not e["schritte"]:
        cta(d, e["cta"], y)
        rp.footer(ImageDraw.Draw(img))
        return img.convert("RGB")
    xs = (48, 48 + 340, 48 + 680)
    for i, s in enumerate(e["schritte"]):
        x = xs[i]
        d.rounded_rectangle((x, y, x + 300, y + 90), radius=45, fill=INK)
        d.text((x + 150, y + 45), s, font=fit(d, s, "Bold", 36, 260, 24), fill=AMBER, anchor="mm")
        if i < 2:
            cx = x + 320
            d.polygon([(cx - 8, y + 30), (cx + 10, y + 45), (cx - 8, y + 60)], fill=INK)
    cta(d, e["cta"], y + 145)
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="05_warnung", kicker="TIMMIS FUN-FACT").save(f"{out}/2_funfact.jpg", quality=92)
    slide_router(data["router"]).save(f"{out}/3_5g_router.jpg", quality=92)
    slide_einsatz(data["esim"]).save(f"{out}/4_esim.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_wochenende.jpg", quality=92)
    print("ok")
