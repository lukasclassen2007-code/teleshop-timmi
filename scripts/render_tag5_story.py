"""Story-Reihe 16.11. (3 × 7 s): Wochenstart, Handy-Herbstputz, Fokus-Modus.
Aufruf: python3 render_tag5_story.py ausgabeordner [1 2 3]
"""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

RED, GREEN = (225, 55, 55), (60, 180, 95)


def alarm_clock(d, cx, cy, r, t, ring):
    sh = math.sin(t * 40) * 8 if ring else 0
    cx += sh
    for s in (-1, 1):
        d.ellipse((cx + s * r * 0.62 - r * 0.32, cy - r * 1.05 - r * 0.32, cx + s * r * 0.62 + r * 0.32, cy - r * 1.05 + r * 0.32), fill=AMBER, outline=INK, width=6)
    for s in (-1, 1):
        d.line([(cx + s * r * 0.55, cy + r * 0.8), (cx + s * r * 0.8, cy + r * 1.15)], fill=INK, width=12)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=INK, width=10)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line([(cx + math.sin(a) * r * 0.78, cy - math.cos(a) * r * 0.78), (cx + math.sin(a) * r * 0.88, cy - math.cos(a) * r * 0.88)], fill=INK, width=5)
    # 9:00 Uhr
    d.line([(cx, cy), (cx, cy - r * 0.6)], fill=INK, width=10)
    d.line([(cx, cy), (cx - r * 0.45, cy)], fill=INK, width=12)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=AMBER)
    if ring:
        for s in (-1, 1):
            for k in range(3):
                rr = r * (1.25 + 0.18 * k)
                d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 200 if s < 0 else -20, 250 if s < 0 else 30, fill=AMBER, width=8)


def story1():
    bg = gradient(W, H, (255, 236, 200), (255, 170, 80)).convert("RGBA")
    c = cat("01_winken", 400, 420)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1250, 460, (255, 255, 255), 0.5)
        head(img, "STORY 1 / 3")
        if t > 0.3:
            q = back((t - 0.3) / 0.6)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            alarm_clock(ImageDraw.Draw(lay), W / 2, 700, 190 * q, t, ring=0.9 < t < 2.4)
            img.alpha_composite(lay)
        a = ease((t - 1.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 975), "Moin, neue Woche!", font=fit(dd, "Moin, neue Woche!", "Bold", 100, W - 80, 50), fill=INK, anchor="mt"))
        a = ease((t - 1.9) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1100), "Timmi ist startklar – du auch?", font=fit(dd, "Timmi ist startklar – du auch?", "Bold", 52, W - 90, 30), fill=WHITE, anchor="mt", stroke_width=4, stroke_fill=INK))
        rs.put_cat(img, c, W // 2, 1640, 2.4, t, "pop")
        cta_bottom(img, t, "Komm vorbei – Timmi freut sich!", t0=3.4)
        return img
    return frame


def story2():
    bg = gradient(W, H, (230, 248, 238), (110, 200, 150)).convert("RGBA")
    c = cat("07_daten", 380, 420)
    random.seed(16)
    apps = [(random.uniform(-1, 1), random.uniform(0.6, 1.4), random.choice([(240, 120, 120), (120, 170, 240), (250, 200, 90), (160, 120, 230), (120, 200, 170)])) for _ in range(9)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 800, 420, (255, 255, 255), 0.6)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Handy voll?", font=font("Bold", 100), fill=INK, anchor="mt"))
        # Speicherbalken: 96 % -> 58 %
        p = ease((t - 1.6) / 1.8)
        lvl = 0.96 - 0.38 * p if t > 1.6 else 0.96
        col = RED if lvl > 0.85 else (AMBER if lvl > 0.7 else GREEN)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        x0, y0, x1, y1 = 120, 640, W - 120, 740
        d.rounded_rectangle((x0, y0, x1, y1), radius=50, fill=WHITE, outline=INK, width=8)
        d.rounded_rectangle((x0 + 14, y0 + 14, x0 + 14 + (x1 - x0 - 28) * lvl, y1 - 14), radius=38, fill=col)
        d.text((W / 2, y1 + 30), f"Speicher: {round(lvl * 100)} % belegt", font=font("Bold", 48), fill=INK, anchor="mt")
        img.alpha_composite(lay)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        # Apps fliegen raus (eigene Ebene)
        for i, (dx, sp, ac) in enumerate(apps):
            tt = t - 1.6 - i * 0.12
            if tt > 0:
                u = ease(tt / 1.0)
                ax = W / 2 + dx * 420 * u
                ay = 690 - 520 * u * sp + 400 * u * u
                al = round(255 * max(0, 1 - u))
                if al <= 0:
                    continue
                s = 70
                d.rounded_rectangle((ax - s / 2, ay - s / 2, ax + s / 2, ay + s / 2), radius=18, fill=ac + (al,))
        img.alpha_composite(lay)
        a = ease((t - 3.2) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 920, "Zeit für den Herbstputz!", 48, fill=INK, col=AMBER))
        rs.put_cat(img, c, W // 2, 1560, 2.8, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


def story3():
    bg = gradient(W, H, (40, 48, 96), (14, 16, 34)).convert("RGBA")
    c = cat("12_chillen", 500, 360)
    random.seed(3)
    stars = [(random.uniform(40, W - 40), random.uniform(200, 1000), random.uniform(2, 5), random.uniform(0, 6)) for _ in range(60)]
    notes = [(200, 680), (760, 660), (300, 860), (780, 870), (540, 770)]

    def frame(t):
        on = ease((t - 2.0) / 0.4)
        img = bg.copy()
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for x, y, r, ph in stars:
            a = round(255 * on * (0.5 + 0.5 * math.sin(t * 3 + ph)))
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))
        img.alpha_composite(lay)
        glow(img, W // 2, 1300, 440, AMBER, 0.35 + 0.2 * on)
        head(img, "STORY 3 / 3")
        # Benachrichtigungen ploppen auf und verschwinden
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, (x, y) in enumerate(notes):
            appear = ease((t - 0.3 - i * 0.2) / 0.3)
            vanish = ease((t - 2.0 - i * 0.05) / 0.35)
            a = appear * (1 - vanish)
            if a > 0.01:
                ww, hh = 300, 90
                d.rounded_rectangle((x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2), radius=26, fill=(255, 255, 255, round(235 * a)))
                d.ellipse((x - ww / 2 + 20, y - 25, x - ww / 2 + 70, y + 25), fill=(RED[0], RED[1], RED[2], round(255 * a)))
                d.text((x - ww / 2 + 45, y), "!", font=font("Bold", 34), fill=(255, 255, 255, round(255 * a)), anchor="mm")
                for k in range(2):
                    d.rounded_rectangle((x - ww / 2 + 90, y - 22 + k * 28, x + ww / 2 - 30 - k * 60, y - 8 + k * 28), radius=7, fill=(190, 195, 210, round(255 * a)))
        img.alpha_composite(lay)
        a = ease((t - 0.2) / 0.4) * (1 - on)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Ping! Ping! Ping!", font=font("Bold", 92), fill=WHITE, anchor="mt"))
        # Schalter
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        sx, sy, sw, sh = W / 2 - 150, 980, 300, 150
        if t > 1.2:
            q = ease((t - 1.2) / 0.4)
            colr = tuple(round(a1 + (b1 - a1) * on) for a1, b1 in zip((120, 125, 140), GREEN))
            d.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=75, fill=colr + (round(255 * q),), outline=(255, 255, 255, round(255 * q)), width=6)
            kx = sx + 75 + (sw - 150) * on
            d.ellipse((kx - 60, sy + 15, kx + 60, sy + sh - 15), fill=(255, 255, 255, round(255 * q)))
        img.alpha_composite(lay)
        layer(img, on, lambda dd: dd.text((W / 2, 425), "Fokus-Modus an –", font=font("Bold", 86), fill=WHITE, anchor="mt"))
        layer(img, on, lambda dd: dd.text((W / 2, 535), "Ruhe an!", font=font("Bold", 110), fill=AMBER, anchor="mt"))
        a = ease((t - 2.8) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1170), "Nur Wichtiges kommt durch.", font=fit(dd, "Nur Wichtiges kommt durch.", "Bold", 54, W - 90, 30), fill=WHITE, anchor="mt"))
        rs.put_cat(img, c, W // 2, 1620, 3.0, t, "pop")
        cta_bottom(img, t, "Hilfe beim Einrichten? Komm vorbei!", t0=3.6)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_wochenstart", story1())
    if "2" in todo: rs.write("story_2_herbstputz", story2())
    if "3" in todo: rs.write("story_3_fokus", story3())
