"""Story-Reihe 23.11. (3 × 7 s): 5 Anbieter 1 Shop, Service, SIM-Karten-Fun-Fact."""
import math, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

MARKEN = ["Vodafone", "Telekom", "o2", "congstar", "otelo"]


def shopfront(d, cx, y0, w, h):
    x0 = cx - w / 2
    d.rectangle((x0, y0 + 90, x0 + w, y0 + h), fill=(245, 240, 232), outline=INK, width=6)
    n = 8
    for k in range(n):
        d.polygon([(x0 + k * w / n, y0), (x0 + (k + 1) * w / n, y0), (x0 + (k + 1) * w / n, y0 + 90), (x0 + (k + 0.5) * w / n, y0 + 120), (x0 + k * w / n, y0 + 90)], fill=AMBER if k % 2 == 0 else INK)
    d.rounded_rectangle((cx - 210, y0 + 140, cx + 210, y0 + 210), radius=16, fill=INK)
    d.text((cx, y0 + 175), "TELESHOP", font=font("Bold", 46), fill=WHITE, anchor="mm")
    d.rectangle((cx - 80, y0 + h - 230, cx + 80, y0 + h), fill=(120, 170, 210), outline=INK, width=6)
    for s in (-1, 1):
        d.rectangle((cx + s * 120 - (90 if s > 0 else -90) * 0 - (0 if s > 0 else 180), y0 + 250, cx + s * 120 + (180 if s > 0 else 0), y0 + 400), fill=(170, 210, 235), outline=INK, width=5)


def story1():
    bg = gradient(W, H, (40, 36, 52), (12, 12, 14)).convert("RGBA")
    c = cat("01_winken", 260, 260)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 460, AMBER, 0.5)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "5 Anbieter,", font=font("Bold", 96), fill=WHITE, anchor="mt"))
        layer(img, ease((t - 0.6) / 0.5), lambda dd: dd.text((W / 2, 540), "1 Shop!", font=font("Bold", 110), fill=AMBER, anchor="mt"))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        q = back((t - 0.8) / 0.6) if t > 0.8 else 0
        if q > 0.05:
            shopfront(d, W / 2, 700 + (1 - q) * 300, 700, 520)
        img.alpha_composite(lay)
        for i, m in enumerate(MARKEN):
            t0 = 1.6 + i * 0.35
            p = ease((t - t0) / 0.6)
            if t > t0:
                row = i % 3
                x = (W / 2 - 320 + (i * 160)) if True else 0
                y = 1260 + (i % 2) * 80
                sx = W / 2 + (-1 if i % 2 else 1) * 600 * (1 - p)
                tx = W / 2 + (i - 2) * 195
                layer(img, min(1, p * 1.5), lambda dd, m=m, x=sx + (tx - W / 2) * p, y=y: pill(dd, x, y, m, 36, fill=WHITE, col=INK))
        rs.put_cat(img, c, W // 2, 1660, 3.6, t, "pop")
        cta_bottom(img, t, "Komm vorbei – Poststraße 34!", t0=3.8)
        return img
    return frame


ICONS = [("Beratung", "Mobilfunk, Internet & TV"), ("Einrichtung", "Daten übertragen, eSIM"), ("Haushalts-Check", "Strom, Gas, Internet, Mobilfunk")]


def story2():
    bg = gradient(W, H, (232, 238, 255), (130, 150, 230)).convert("RGBA")
    c = cat("04_zeigen", 330, 360)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 430, (255, 255, 255), 0.6)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Wobei hilft dir Timmi?", font=fit(dd, "Wobei hilft dir Timmi?", "Bold", 84, W - 80, 40), fill=INK, anchor="mt"))
        for i, (tt, sub) in enumerate(ICONS):
            a = ease((t - 0.8 - i * 0.6) / 0.45)
            y = 590 + i * 200
            def card(dd, tt=tt, sub=sub, y=y, i=i):
                dd.rounded_rectangle((90, y, W - 90, y + 170), radius=34, fill=WHITE)
                dd.ellipse((120, y + 35, 220, y + 135), fill=(70, 90, 200))
                dd.text((170, y + 85), str(i + 1), font=font("Bold", 56), fill=WHITE, anchor="mm")
                dd.text((260, y + 40), tt, font=font("Bold", 52), fill=INK)
                dd.text((260, y + 108), sub, font=fit(dd, sub, "Medium", 34, W - 90 - 280, 24), fill=(70, 70, 80))
            layer(img, a, card)
        rs.put_cat(img, c, W // 2, 1650, 3.0, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6, fill=INK, col=AMBER)
        return img
    return frame


def simcard(d, cx, cy, s):
    w, h = s, s * 0.68
    x0, y0 = cx - w / 2, cy - h / 2
    d.polygon([(x0, y0), (x0 + w - h * 0.25, y0), (x0 + w, y0 + h * 0.25), (x0 + w, y0 + h), (x0, y0 + h)], fill=WHITE, outline=INK)
    d.rounded_rectangle((cx - w * 0.22, cy - h * 0.25, cx + w * 0.22, cy + h * 0.25), radius=12, fill=(235, 190, 80), outline=(170, 120, 30), width=4)
    d.line([(cx, cy - h * 0.25), (cx, cy + h * 0.25)], fill=(170, 120, 30), width=4)
    d.line([(cx - w * 0.22, cy), (cx + w * 0.22, cy)], fill=(170, 120, 30), width=4)


def story3():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("02_handy", 300, 320)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 800, 440, AMBER, 0.5)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Wusstest du?", font=font("Bold", 80), fill=WHITE, anchor="mt"))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for k in range(3):
            q = back((t - 0.5 - k * 0.2) / 0.5) if t > 0.5 + k * 0.2 else 0
            if q > 0.05:
                simcard(d, W / 2 + (k - 1) * 150 + math.sin(t * 2 + k) * 6, 700 + abs(k - 1) * 40, 300 * q)
        img.alpha_composite(lay)
        p = ease((t - 1.4) / 1.6)
        n = round(106 * p) if t > 1.4 else 0
        ImageDraw.Draw(img).text((W / 2, 900), f"{n} Mio.", font=font("Bold", 170), fill=AMBER, anchor="mt", stroke_width=6, stroke_fill=INK)
        a = ease((t - 2.8) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1110), "aktive SIM-Karten in Deutschland", font=fit(dd, "aktive SIM-Karten in Deutschland", "Bold", 54, W - 90, 30), fill=WHITE, anchor="mt"))
        a = ease((t - 3.3) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1220, "rund 1,3 pro Einwohner!", 44, fill=AMBER, col=INK))
        rs.put_cat(img, c, W // 2, 1650, 3.6, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=4.0)
        ImageDraw.Draw(img).text((W - 70, 1800), "Quelle: Bundesnetzagentur, Ende 2025", font=font("Regular", 22), fill=(150, 150, 160), anchor="ra")
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_anbieter", story1())
    if "2" in todo: rs.write("story_2_service", story2())
    if "3" in todo: rs.write("story_3_sim_karten", story3())
