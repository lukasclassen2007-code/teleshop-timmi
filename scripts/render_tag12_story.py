"""Story-Reihe 25.11. (3 × 7 s): Schaufenster mit Lichterkette, Tannenbaum & Beratung, Foto-Tipp."""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom
from render_tag12 import garland, tree, BULBS


def flakes(seed, n=90):
    rnd = random.Random(seed)
    return [(rnd.uniform(0, W), rnd.uniform(-H, H), rnd.uniform(4, 10), rnd.uniform(60, 140), rnd.uniform(0, 6.28)) for _ in range(n)]


def draw_snow(img, fl, t):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x, y0, r, v, ph in fl:
        y = (y0 + t * v) % (H + 40) - 20
        xx = x + math.sin(t * 1.5 + ph) * 25
        d.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 255, 255, 200))
    img.alpha_composite(lay)


def story1():
    bg = gradient(W, H, (28, 36, 70), (10, 12, 26)).convert("RGBA")
    c = cat("15_advent", 420, 460)
    fl = flakes(25)

    def frame(t):
        img = bg.copy()
        on = ease((t - 1.4) / 0.4)
        glow(img, W // 2, 1150, 480, AMBER, 0.15 + 0.4 * on)
        draw_snow(img, fl, t)
        if on > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
            garland(tmp, 330, x0=60, x1=W - 60, sag=60, n=14, t=t)
            tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * on)))
            img.alpha_composite(tmp)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 500), "Draußen Schnee …", font=font("Bold", 92), fill=WHITE, anchor="mt"))
        layer(img, ease((t - 1.6) / 0.5), lambda dd: dd.text((W / 2, 615), "… drinnen Lichterkette!", font=fit(dd, "… drinnen Lichterkette!", "Bold", 84, W - 80, 44), fill=AMBER, anchor="mt"))
        if t > 2.2:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            q = ease((t - 2.2) / 0.6)
            tree(lay, 270, 1300, 520 * q, t)
            img.alpha_composite(lay)
        rs.put_cat(img, c, 790, 1600, 2.8, t, "pop")
        cta_bottom(img, t, "Komm rein und wärm dich auf!", t0=3.8)
        return img
    return frame


def story2():
    bg = gradient(W, H, (255, 236, 236), (225, 110, 110)).convert("RGBA")
    c = cat("16_geschenk", 380, 420)
    fl = flakes(8, 50)
    items = [("Beratung", "fürs perfekte Geschenk"), ("Startklar", "wir richten's vorher ein"), ("Tarif dazu", "passend fürs neue Handy")]

    def frame(t):
        img = bg.copy()
        draw_snow(img, fl, t)
        glow(img, W // 2, 850, 430, (255, 255, 255), 0.55)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Geschenk-Zeit", font=font("Bold", 100), fill=INK, anchor="mt"))
        layer(img, ease((t - 0.5) / 0.5), lambda dd: dd.text((W / 2, 540), "bei Timmi!", font=font("Bold", 100), fill=WHITE, anchor="mt", stroke_width=5, stroke_fill=INK))
        for i, (tt, sub) in enumerate(items):
            a = ease((t - 1.0 - i * 0.5) / 0.4)
            y = 700 + i * 170
            def card(dd, tt=tt, sub=sub, y=y, i=i):
                dd.rounded_rectangle((110, y, W - 110, y + 140), radius=34, fill=WHITE)
                dd.ellipse((135, y + 25, 225, y + 115), fill=(200, 40, 50))
                dd.text((180, y + 70), str(i + 1), font=font("Bold", 50), fill=WHITE, anchor="mm")
                dd.text((255, y + 22), tt, font=font("Bold", 48), fill=INK)
                dd.text((255, y + 84), sub, font=font("Medium", 34), fill=(80, 80, 90))
            layer(img, a, card)
        rs.put_cat(img, c, W // 2, 1650, 3.0, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


def story3():
    bg = gradient(W, H, (28, 36, 70), (10, 12, 26)).convert("RGBA")
    c = cat("09_empfang", 380, 440)
    fl = flakes(31, 70)
    tips = ["Blitz aus", "Nachtmodus an", "Handy ruhig halten"]

    def frame(t):
        img = bg.copy()
        draw_snow(img, fl, t)
        garland(img, 300, x0=60, x1=W - 60, sag=50, n=12, t=t)
        glow(img, W // 2, 1300, 460, AMBER, 0.4)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 480), "Lichter-Fotos?", font=font("Bold", 100), fill=WHITE, anchor="mt"))
        layer(img, ease((t - 0.6) / 0.5), lambda dd: dd.text((W / 2, 600), "Timmis 3 Tricks:", font=font("Bold", 60), fill=AMBER, anchor="mt"))
        for i, tp in enumerate(tips):
            a = ease((t - 1.2 - i * 0.5) / 0.4)
            layer(img, a, lambda dd, tp=tp, i=i: pill(dd, W / 2, 740 + i * 110, f"{i + 1}. {tp}", 46, fill=WHITE, col=INK))
        # Blitz-Symbol durchgestrichen
        if t > 2.8:
            q = back((t - 2.8) / 0.5)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            cx, cy, s = 200, 1240, 70 * q
            d.polygon([(cx + s * 0.1, cy - s), (cx - s * 0.5, cy + s * 0.1), (cx - s * 0.05, cy + s * 0.1), (cx - s * 0.2, cy + s), (cx + s * 0.5, cy - s * 0.15), (cx + s * 0.05, cy - s * 0.15)], fill=AMBER)
            d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=(230, 60, 60), width=12)
            img.alpha_composite(lay)
        rs.put_cat(img, c, 760, 1620, 3.2, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.8)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_lichterkette", story1())
    if "2" in todo: rs.write("story_2_geschenkzeit", story2())
    if "3" in todo: rs.write("story_3_foto_tipp", story3())
