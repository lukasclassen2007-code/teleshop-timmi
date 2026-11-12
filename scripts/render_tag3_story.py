"""Story-Reihe 12.11. (neu, 3 × 7 s): Erstes Handy, Throwback-Fun-Fact, MagentaTV.
Aufruf: python3 render_tag3_story.py ausgabeordner [1 2 3]
"""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, wrap, gradient, glow, cat, INK, AMBER, WHITE
from render_tag2 import retro_phone
from render_tag_story import cta_bottom

MAG = (226, 0, 116)


BODY, EDGE, SCR, KEY = (60, 66, 80), (20, 20, 24), (170, 200, 150), (200, 205, 215)


def keys(d, x, y, w, h, rows=4):
    for r in range(rows):
        for c in range(3):
            cx = x + w * (0.25 + c * 0.25)
            cy = y + h * (0.15 + r * (0.75 / (rows - 1)))
            d.ellipse((cx - w * 0.08, cy - h * 0.045, cx + w * 0.08, cy + h * 0.045), fill=KEY)


def flip_phone(d, x, y, s):
    """Aufgeklapptes Klapphandy: Display oben, Scharnier, Tasten unten."""
    w = 0.42 * s
    hh = s * 0.48
    d.rounded_rectangle((x, y, x + w, y + hh), radius=w * 0.2, fill=(150, 60, 160), outline=EDGE, width=4)
    d.rounded_rectangle((x + w * 0.12, y + hh * 0.14, x + w * 0.88, y + hh * 0.8), radius=w * 0.06, fill=SCR)
    d.rounded_rectangle((x + w * 0.1, y + hh - 8, x + w * 0.9, y + hh + 24), radius=12, fill=(125, 50, 135), outline=EDGE, width=3)
    y2 = y + hh + 16
    d.rounded_rectangle((x, y2, x + w, y2 + hh), radius=w * 0.2, fill=(150, 60, 160), outline=EDGE, width=4)
    keys(d, x, y2 + hh * 0.08, w, hh * 0.82)


def slide_phone(d, x, y, s, t):
    """Schiebehandy: Displayteil gleitet über dem Tastenteil hoch und runter."""
    w = 0.42 * s
    hh = s * 0.6
    ky = y + s - hh
    d.rounded_rectangle((x + 6, ky, x + w - 6, y + s), radius=w * 0.18, fill=(40, 44, 54), outline=EDGE, width=4)
    keys(d, x + 6, ky + hh * 0.42, w - 12, hh * 0.5)
    o = 0.65 + 0.35 * math.sin(t * 2.2)
    sy = ky - o * hh * 0.62
    d.rounded_rectangle((x, sy, x + w, sy + hh), radius=w * 0.2, fill=(30, 110, 200), outline=EDGE, width=4)
    d.rounded_rectangle((x + w * 0.12, sy + hh * 0.1, x + w * 0.88, sy + hh * 0.72), radius=w * 0.06, fill=SCR)


def antenna_phone(d, x, y, s):
    """Klassiker mit kleiner Antenne."""
    w = 0.42 * s
    d.rounded_rectangle((x + w * 0.66, y - s * 0.16, x + w * 0.84, y + 10), radius=w * 0.08, fill=EDGE)
    d.rounded_rectangle((x, y, x + w, y + s), radius=w * 0.28, fill=BODY, outline=EDGE, width=4)
    d.rounded_rectangle((x + w * 0.14, y + s * 0.12, x + w * 0.86, y + s * 0.42), radius=w * 0.06, fill=SCR)
    d.text((x + w / 2, y + s * 0.27), "Hallo?", font=font("Bold", int(s * 0.07)), fill=(40, 60, 40), anchor="mm")
    keys(d, x, y + s * 0.5, w, s * 0.45)


def story1():
    bg = gradient(W, H, (40, 36, 52), (12, 12, 14)).convert("RGBA")
    c = cat("09_empfang", 360, 360)
    S = 360
    slots = ((200, "Klapphandy", 0.9), (W // 2, "Schiebehandy", 1.2), (W - 200, "Klassiker", 1.5))

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1300, round(430 + 30 * math.sin(t * 2.5)), AMBER, 0.55)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for i, (cx, lab, t0) in enumerate(slots):
            p = ease((t - t0) / 0.7)
            if p <= 0:
                continue
            y = round(790 + (1 - p) * 1200 + math.sin(t * 2 + i) * 8)
            x = cx - 0.42 * S / 2
            if i == 0:
                flip_phone(ld, x, y, S * 0.78)
            elif i == 1:
                slide_phone(ld, x, y, S, t)
            else:
                antenna_phone(ld, x, y + 50, S * 0.86)
            ld.text((cx, y + S + 30), lab, font=font("Bold", 36), fill=(255, 255, 255, round(255 * p)), anchor="mt")
        img.alpha_composite(lay)
        rs.put_cat(img, c, W // 2, 1585, 2.0, t, "pop")
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "ERINNERST DU DICH?", font=font("Bold", 52), fill=AMBER, anchor="mt"))
        full = "Dein erstes Handy –"
        k = min(len(full), max(0, int((t - 0.5) / 0.04)))
        f = font("Bold", 84)
        if k:
            ImageDraw.Draw(img).text((W / 2, 520), full[:k], font=f, fill=WHITE, anchor="mt")
        a = ease((t - 1.3) / 0.4)
        layer(img, a, lambda dd: dd.text((W / 2, 625), "welches war's?", font=f, fill=AMBER, anchor="mt"))
        cta_bottom(img, t, "Schreib's unter unseren Beitrag!", t0=3.2)
        return img
    return frame


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("03_idee", 380, 400)
    random.seed(7)
    notes = [(random.uniform(60, W - 60), random.uniform(0, 1), random.uniform(40, 70), random.uniform(0, 6.28)) for _ in range(14)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1300, 460, AMBER, 0.5)
        # Musiknoten steigen auf
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for x, ph0, sp, ph in notes:
            y = H - ((ph0 * H + t * sp * 6) % H)
            xx = x + math.sin(t * 2 + ph) * 20
            col = (255, 255, 255, 70)
            ld.ellipse((xx - 18, y - 12, xx + 10, y + 12), fill=col)
            ld.rectangle((xx + 4, y - 62, xx + 10, y), fill=col)
            ld.polygon([(xx + 10, y - 62), (xx + 34, y - 44), (xx + 34, y - 30), (xx + 10, y - 46)], fill=col)
        img.alpha_composite(lay)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "THROWBACK THURSDAY", font=font("Bold", 52), fill=AMBER, anchor="mt"))
        # Jahreszahl spult von 2026 zurück auf 2005
        p = ease((t - 0.5) / 1.4)
        yr = round(2026 - 21 * p) if t > 0.5 else 2026
        sz = 230 + round(18 * max(0.0, 1 - abs(t - 2.05) / 0.25))
        ImageDraw.Draw(img).text((W / 2, 510), str(yr), font=font("Bold", sz), fill=WHITE, anchor="mt", stroke_width=6, stroke_fill=INK)
        a = ease((t - 1.0) / 0.4)
        layer(img, a, lambda dd: dd.text((W / 2, 470 + 290), "zurückspulen …" if t < 2.0 else "Wusstest du?", font=font("Bold", 46), fill=(200, 200, 210), anchor="mt"))
        a = ease((t - 2.2) / 0.5)
        lines = ["Ein Klingelton-Frosch", "stürmte die Charts!"]
        for i, ln in enumerate(lines):
            layer(img, a, lambda dd, ln=ln, i=i: dd.text((W / 2, 860 + i * 78), ln, font=font("Bold", 66), fill=WHITE if i == 0 else AMBER, anchor="mt"))
        a = ease((t - 2.9) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1035), "Crazy Frog mit „Axel F“ – Platz 1 in UK, vor Coldplay.", font=fit(dd, "Crazy Frog mit „Axel F“ – Platz 1 in UK, vor Coldplay.", "Medium", 40, W - 90, 26), fill=(220, 220, 220), anchor="mt"))
        # Platz-1-Badge hüpft rein
        if t > 3.2:
            q = back((t - 3.2) / 0.6)
            r = round(95 * q)
            d = ImageDraw.Draw(img)
            cx, cy = 230, 1330
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=AMBER, outline=INK, width=6)
            if q > 0.6:
                d.text((cx, cy), "#1", font=font("Bold", round(84 * min(1, q))), fill=INK, anchor="mm")
            for k in range(3):
                ang = t * 1.5 + k * 2.1
                star(d, cx + math.cos(ang) * 140, cy + math.sin(ang) * 140, 14, WHITE)
        rs.put_cat(img, c, 760, 1540, 1.6, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=3.8)
        ImageDraw.Draw(img).text((W - 70, 1800), "Quelle: Official Charts, 2005", font=font("Regular", 22), fill=(150, 150, 160), anchor="ra")
        return img
    return frame


def tv(d, cx, cy, w, h, t, ch):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=30, fill=INK)
    sx0, sy0, sx1, sy1 = cx - w / 2 + 24, cy - h / 2 + 24, cx + w / 2 - 24, cy + h / 2 - 24
    d.rounded_rectangle((sx0, sy0, sx1, sy1), radius=14, fill=(60, 20, 70))
    # Bewegte Farbbänder als "Programm"
    for k in range(5):
        y = sy0 + (sy1 - sy0) * (k + 0.5) / 5
        off = math.sin(t * 2 + k) * 40
        d.rounded_rectangle((sx0 + 40 + off, y - 10, sx1 - 40 + off * 0.3, y + 10), radius=10, fill=(120 + 25 * k, 40, 140 - 10 * k))
    tri = 46
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=WHITE)
    d.polygon([(cx - tri * 0.45, cy - tri * 0.7), (cx - tri * 0.45, cy + tri * 0.7), (cx + tri * 0.75, cy)], fill=MAG)
    d.text((sx1 - 20, sy0 + 16), ch, font=font("Bold", 34), fill=WHITE, anchor="ra")
    d.rectangle((cx - 20, cy + h / 2, cx + 20, cy + h / 2 + 40), fill=INK)
    d.rounded_rectangle((cx - 130, cy + h / 2 + 36, cx + 130, cy + h / 2 + 54), radius=9, fill=INK)


def story3():
    bg = gradient(W, H, (255, 232, 244), (235, 110, 180)).convert("RGBA")
    c = cat("18_danke", 330, 350)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 460, (255, 255, 255), 0.5)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Gemütliche Winterabende?", font=fit(dd, "Gemütliche Winterabende?", "Bold", 76, W - 80, 40), fill=INK, anchor="mt"))
        # Fernseher springt an, Kanäle zählen hoch
        if t > 0.6:
            q = back((t - 0.6) / 0.6)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ch = min(210, round(210 * ease((t - 1.0) / 1.4))) if t > 1.0 else 1
            tv(ImageDraw.Draw(lay), W / 2, 730, 700 * q, 390 * q, t, f"{ch}{'+' if ch >= 210 else ''} Sender" if q > 0.9 else "")
            img.alpha_composite(lay)
        a = ease((t - 2.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1000), "MagentaTV", font=font("Bold", 96), fill=MAG, anchor="mt", stroke_width=4, stroke_fill=WHITE))
        a = ease((t - 2.5) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1115), "Sender & Streaming in einer Oberfläche", font=fit(dd, "Sender & Streaming in einer Oberfläche", "Bold", 44, W - 90, 28), fill=INK, anchor="mt"))
        for i, txt in enumerate(("TV", "Handy", "Tablet")):
            a = ease((t - 2.9 - i * 0.2) / 0.4)
            layer(img, a, lambda dd, txt=txt, i=i: pill(dd, 190 + i * 175, 1195, txt, 32, fill=WHITE, col=INK))
        rs.put_cat(img, c, 880, 1560, 3.0, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_erstes_handy", story1())
    if "2" in todo: rs.write("story_2_throwback", story2())
    if "3" in todo: rs.write("story_3_magentatv", story3())
