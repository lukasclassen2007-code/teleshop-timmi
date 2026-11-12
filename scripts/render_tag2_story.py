"""Story-Reihe 12.11. (3 × 7 s, 1080x1920): Erstes Handy, Althandy-Schublade, Kälte & Akku.
Aufruf: python3 render_tag2_story.py ausgabeordner [1 2 3]
"""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag2 import retro_phone
from render_tag_story import cta_bottom


def story1():
    bg = gradient(W, H, (40, 36, 52), (12, 12, 14)).convert("RGBA")
    c = cat("09_empfang", 560, 560)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1250, round(430 + 30 * math.sin(t * 2.5)), AMBER, 0.55)
        # zwei Retro-Handys fahren von unten ins Bild und wippen leicht
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for i, (x, s, t0) in enumerate(((90, 380, 0.3), (720, 330, 0.5))):
            p = ease((t - t0) / 0.8)
            if p > 0:
                y = round(1080 + (1 - p) * 900 + math.sin(t * 2 + i) * 10)
                retro_phone(ld, x, y, s, "Hallo?" if i == 0 else None)
        img.alpha_composite(lay)
        rs.put_cat(img, c, W // 2, 1560, 1.0, t, "pop")
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "THROWBACK THURSDAY", font=font("Bold", 52), fill=AMBER, anchor="mt"))
        full = "Was war dein erstes Handy?"
        k = min(len(full), max(0, int((t - 0.6) / 0.06)))
        if k:
            f = fit(ImageDraw.Draw(img), full, "Bold", 84, W - 80, 50)
            ImageDraw.Draw(img).text((W / 2, 520), full[:k], font=f, fill=WHITE, anchor="mt")
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 650), "Klapphandy? Schiebehandy?", font=font("Medium", 48), fill=(220, 220, 220), anchor="mt"))
        cta_bottom(img, t, "Schreib's uns per DM!", t0=3.2)
        return img
    return frame


def story2():
    bg = gradient(W, H, (236, 244, 228), (120, 190, 95)).convert("RGBA")
    c = cat("02_handy", 400, 470)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1150, 420, (255, 255, 255), 0.55)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Wusstest du?", font=font("Bold", 72), fill=INK, anchor="mt"))
        # Zähler 0 -> 167 Millionen
        p = ease((t - 0.6) / 1.6)
        n = round(167 * p) if t > 0.6 else 0
        sz = 220 + round(16 * max(0.0, 1 - abs(t - 2.25) / 0.25))
        ImageDraw.Draw(img).text((W / 2, 530), str(n), font=font("Bold", sz), fill=WHITE, anchor="mt", stroke_width=7, stroke_fill=INK)
        a = ease((t - 1.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 790), "Millionen alte Handys", font=font("Bold", 64), fill=INK, anchor="mt"))
        layer(img, a, lambda dd: dd.text((W / 2, 870), "liegen in deutschen Schubladen.", font=fit(dd, "liegen in deutschen Schubladen.", "Medium", 50, W - 100, 32), fill=INK, anchor="mt"))
        # Schublade fährt auf, Handys darin
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        q = ease((t - 2.4) / 0.7)
        x0, y0, x1 = 120, 1120, 640
        ld.rounded_rectangle((x0, y0, x1, y0 + 360), radius=20, fill=(140, 95, 60))
        open_h = round(170 * q)
        ld.rounded_rectangle((x0 - 20, y0 + 140 - open_h, x1 + 20, y0 + 380), radius=22, fill=(170, 120, 78))
        ld.rounded_rectangle((x0 + 200, y0 + 240, x1 - 200, y0 + 270), radius=12, fill=(110, 75, 45))
        if q > 0.05:
            for i, (dx, s) in enumerate(((40, 150), (170, 170), (300, 140), (420, 160))):
                retro_phone(ld, x0 + dx, y0 + 150 - open_h - round(s * 0.55 * q), s)
            ld.rounded_rectangle((x0 - 20, y0 + 140 - open_h + 40, x1 + 20, y0 + 380), radius=22, fill=(170, 120, 78))
            ld.rounded_rectangle((x0 + 200, y0 + 240, x1 - 200, y0 + 270), radius=12, fill=(110, 75, 45))
        img.alpha_composite(lay)
        rs.put_cat(img, c, 860, 1540, 2.8, t, "pop")
        a = ease((t - 3.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 975), "Daten sichern · zurücksetzen · richtig entsorgen", font=fit(dd, "Daten sichern · zurücksetzen · richtig entsorgen", "Bold", 38, W - 80, 26), fill=INK, anchor="mt"))
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6, fill=INK, col=AMBER)
        ImageDraw.Draw(img).text((W - 70, 1800), "Quelle: Bitkom, 2026", font=font("Regular", 22), fill=(60, 80, 50), anchor="ra")
        return img
    return frame


def story3():
    bg = gradient(W, H, (220, 238, 255), (110, 165, 225)).convert("RGBA")
    c = cat("14_herbst", 600, 440)
    random.seed(4)
    flakes = [(random.uniform(0, W), random.uniform(-H, H), random.uniform(4, 11), random.uniform(60, 150), random.uniform(0, 6.28)) for _ in range(90)]
    RED = (230, 50, 50)

    def frame(t):
        img = bg.copy()
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for x, y0, r, v, ph in flakes:
            y = (y0 + t * v) % (H + 40) - 20
            xx = x + math.sin(t * 1.5 + ph) * 25
            ld.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 255, 255, 220))
        img.alpha_composite(lay)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Brrr … Kälte", font=font("Bold", 96), fill=INK, anchor="mt"))
        layer(img, a, lambda dd: dd.text((W / 2, 550), "frisst Akku!", font=font("Bold", 96), fill=WHITE, anchor="mt", stroke_width=5, stroke_fill=INK))
        # Akku entleert sich von 100 % auf 20 %
        p = ease((t - 0.8) / 1.6)
        lvl = 1.0 - 0.8 * p if t > 0.8 else 1.0
        col = RED if lvl < 0.35 else (60, 190, 90)

        def bat(dd):
            x0, y0, w, h = W / 2 - 200, 720, 400, 190
            dd.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=30, fill=WHITE, outline=INK, width=10)
            dd.rounded_rectangle((x0 + w, y0 + 60, x0 + w + 30, y0 + h - 60), radius=8, fill=INK)
            dd.rounded_rectangle((x0 + 22, y0 + 22, x0 + 22 + (w - 44) * lvl, y0 + h - 22), radius=16, fill=col)
            dd.text((x0 + w / 2, y0 + h / 2), f"{round(lvl * 100)} %", font=font("Bold", 64), fill=INK, anchor="mm")
        layer(img, ease((t - 0.5) / 0.4), bat)
        a = ease((t - 2.6) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 960, "Tipp: Handy in die Innentasche!", 40, fill=INK, col=AMBER))
        rs.put_cat(img, c, W // 2, 1560, 2.2, t, "pop")
        cta_bottom(img, t, "Akku schwächelt? Komm vorbei!", t0=3.6, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_erstes_handy", story1())
    if "2" in todo: rs.write("story_2_altes_handy", story2())
    if "3" in todo: rs.write("story_3_kaelte", story3())
