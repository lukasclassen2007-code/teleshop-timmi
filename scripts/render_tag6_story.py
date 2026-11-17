"""Story-Reihe 17.11. (3 × 7 s): Countdown, erste SMS, Geschenk."""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom
from render_tag2 import retro_phone

RED = (200, 40, 50)


def snowflakes(seed, n=80):
    random.seed(seed)
    return [(random.uniform(0, W), random.uniform(-H, H), random.uniform(4, 10), random.uniform(60, 140), random.uniform(0, 6.28)) for _ in range(n)]


def draw_snow(img, flakes, t):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for x, y0, r, v, ph in flakes:
        y = (y0 + t * v) % (H + 40) - 20
        xx = x + math.sin(t * 1.5 + ph) * 25
        ld.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 255, 255, 200))
    img.alpha_composite(lay)


def story1():
    bg = gradient(W, H, (150, 30, 40), (60, 10, 20)).convert("RGBA")
    c = cat("15_advent", 460, 480)
    fl = snowflakes(17)

    def frame(t):
        img = bg.copy()
        draw_snow(img, fl, t)
        glow(img, W // 2, 1300, 460, AMBER, 0.45)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Nur noch", font=font("Bold", 72), fill=WHITE, anchor="mt"))
        p = ease((t - 0.6) / 1.6)
        n = round(99 - 62 * p) if t > 0.6 else 99
        sz = 300 + round(20 * max(0.0, 1 - abs(t - 2.3) / 0.25))
        ImageDraw.Draw(img).text((W / 2, 520), str(n), font=font("Bold", sz), fill=AMBER, anchor="mt", stroke_width=8, stroke_fill=INK)
        a = ease((t - 2.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 870), "Tage bis Weihnachten!", font=fit(dd, "Tage bis Weihnachten!", "Bold", 80, W - 80, 40), fill=WHITE, anchor="mt"))
        a = ease((t - 2.9) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1000, "Geschenk-Ideen bei Timmi", 42, fill=WHITE, col=INK))
        rs.put_cat(img, c, W // 2, 1600, 2.6, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6)
        return img
    return frame


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("03_idee", 300, 300)
    fl = snowflakes(5, 50)

    def frame(t):
        img = bg.copy()
        draw_snow(img, fl, t)
        glow(img, W // 2, 900, 420, AMBER, 0.45)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Die erste SMS der Welt", font=fit(dd, "Die erste SMS der Welt", "Bold", 74, W - 80, 40), fill=WHITE, anchor="mt"))
        a = ease((t - 0.5) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 530), "3. Dezember 1992", font=font("Bold", 50), fill=AMBER, anchor="mt"))
        # Altes Handy mit getipptem Text
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        q = back((t - 0.6) / 0.6) if t > 0.6 else 0
        if q > 0:
            s = 620 * q
            x, y = W / 2 - 0.42 * s / 2, 620 + (1 - q) * 200
            retro_phone(ld, x, y, s)
            img.alpha_composite(lay)
            full = "Merry Christmas"
            k = min(len(full), max(0, int((t - 1.4) / 0.09)))
            if q > 0.95:
                d = ImageDraw.Draw(img)
                w = 0.42 * s
                cx, cy = x + w / 2, y + s * 0.27
                txt = full[:k]
                f = fit(d, "Christmas", "Bold", 44, w * 0.66, 18)
                if k > 6:
                    d.text((cx, cy - 20), full[:min(k, 5)], font=f, fill=(40, 60, 40), anchor="mm")
                    d.text((cx, cy + 20), full[6:k] + ("|" if int(t * 3) % 2 and k < len(full) else ""), font=f, fill=(40, 60, 40), anchor="mm")
                else:
                    d.text((cx, cy - 20), txt + ("|" if int(t * 3) % 2 else ""), font=f, fill=(40, 60, 40), anchor="mm")
        a = ease((t - 3.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1270), "Damals noch vom Computer aufs Handy!", font=fit(dd, "Damals noch vom Computer aufs Handy!", "Medium", 44, W - 90, 28), fill=(225, 225, 230), anchor="mt"))
        rs.put_cat(img, c, 860, 1650, 3.2, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=3.8)
        return img
    return frame


def gift(d, cx, cy, s, lid, lx=0):
    d.rounded_rectangle((cx - s / 2, cy - s * 0.35, cx + s / 2, cy + s * 0.5), radius=16, fill=RED, outline=INK, width=6)
    d.rectangle((cx - s * 0.07, cy - s * 0.35, cx + s * 0.07, cy + s * 0.5), fill=AMBER)
    ly = cy - s * 0.35 - lid
    cx = cx + lx
    d.rounded_rectangle((cx - s * 0.56, ly - s * 0.16, cx + s * 0.56, ly), radius=14, fill=(225, 55, 65), outline=INK, width=6)
    d.rectangle((cx - s * 0.07, ly - s * 0.16, cx + s * 0.07, ly), fill=AMBER)
    for sgn in (-1, 1):
        d.ellipse((cx + sgn * s * 0.18 - s * 0.14, ly - s * 0.3, cx + sgn * s * 0.18 + s * 0.14, ly - s * 0.12), outline=AMBER, width=14)


def story3():
    bg = gradient(W, H, (255, 236, 236), (235, 120, 120)).convert("RGBA")
    c = cat("16_geschenk", 320, 330)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 820, 420, (255, 255, 255), 0.6)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Auspacken &", font=font("Bold", 90), fill=INK, anchor="mt"))
        layer(img, a, lambda dd: dd.text((W / 2, 530), "loslegen!", font=font("Bold", 110), fill=WHITE, anchor="mt", stroke_width=5, stroke_fill=INK))
        lid = 120 * ease((t - 1.4) / 0.6) if t > 1.4 else 0
        shake = math.sin(t * 30) * 6 if 0.6 < t < 1.4 else 0
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if t > 1.6:
            pr = ease((t - 1.6) / 0.6)
            px, py, pw, ph = W / 2 - 75, 960 - 210 * pr, 150, 290
            d.rounded_rectangle((px, py, px + pw, py + ph), radius=26, fill=INK)
            d.rounded_rectangle((px + 10, py + 14, px + pw - 10, py + ph - 14), radius=18, fill=(255, 210, 140))
            if pr > 0.9:
                for k in range(4):
                    ang = t * 1.8 + k * 1.57
                    star(d, W / 2 + math.cos(ang) * 150, py + 140 + math.sin(ang) * 150, 16, AMBER)
        gift(d, W / 2 + shake, 1060, 300, lid, lx=2.2 * lid)
        img.alpha_composite(lay)
        a = ease((t - 2.6) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1250, "Wir richten's dir ein!", 44, fill=INK, col=AMBER))
        rs.put_cat(img, c, 860, 1650, 3.0, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_countdown", story1())
    if "2" in todo: rs.write("story_2_erste_sms", story2())
    if "3" in todo: rs.write("story_3_geschenk", story3())
