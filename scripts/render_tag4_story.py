"""Story-Reihe 13.11. (3 × 7 s): Freitag der 13., WLAN to go (5G-Router), Wochenende.
Aufruf: python3 render_tag4_story.py ausgabeordner [1 2 3]
"""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom
from render_tag4 import router_icon

GREEN = (60, 175, 90)
RED = (215, 45, 45)


def clover(d, x, y, s, col=GREEN):
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        cx, cy = x + dx * s * 0.42, y + dy * s * 0.42
        d.ellipse((cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42), fill=col)
    d.line([(x, y), (x + s * 0.5, y + s * 1.3)], fill=col, width=max(3, int(s * 0.16)))


def story1():
    bg = gradient(W, H, (36, 30, 58), (10, 10, 16)).convert("RGBA")
    c = cat("01_winken", 440, 420)
    random.seed(13)
    cl = [(random.uniform(60, W - 60), random.uniform(0, 1), random.uniform(18, 34), random.uniform(0, 6.28)) for _ in range(16)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1300, 440, AMBER, 0.5)
        if t > 3.0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            a = ease((t - 3.0) / 0.6)
            for x, ph0, s, ph in cl:
                y = H - ((ph0 * H + (t - 3.0) * 140) % H)
                clover(ld, x + math.sin(t * 2 + ph) * 18, y, s, GREEN + (round(150 * a),))
            img.alpha_composite(lay)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "HEUTE IST …", font=font("Bold", 52), fill=AMBER, anchor="mt"))
        # Kalenderblatt klappt auf
        if t > 0.5:
            q = back((t - 0.5) / 0.6)
            cw, ch = 360, 340 * max(0.02, q)
            x0, y0 = W / 2 - cw / 2, 520
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=28, fill=WHITE, outline=INK, width=6)
            if q > 0.85:
                d.rounded_rectangle((x0, y0, x0 + cw, y0 + 80), radius=28, fill=RED)
                d.rectangle((x0, y0 + 50, x0 + cw, y0 + 80), fill=RED)
                d.text((W / 2, y0 + 42), "NOVEMBER", font=font("Bold", 36), fill=WHITE, anchor="mm")
                d.text((W / 2, y0 + 190), "13", font=font("Bold", 170), fill=INK, anchor="mm")
                d.text((W / 2, y0 + 300), "FREITAG", font=font("Bold", 40), fill=RED, anchor="mm")
            img.alpha_composite(lay)
        a = ease((t - 1.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 905), "Schwarze Katze? Keine Sorge –", font=fit(dd, "Schwarze Katze? Keine Sorge –", "Bold", 58, W - 80, 36), fill=WHITE, anchor="mt"))
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 985), "Timmi bringt Glück!", font=font("Bold", 76), fill=AMBER, anchor="mt"))
        a = ease((t - 3.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1085), "2026 schon der dritte Freitag, der 13.!", font=fit(dd, "2026 schon der dritte Freitag, der 13.!", "Medium", 40, W - 100, 26), fill=(215, 215, 225), anchor="mt"))
        rs.put_cat(img, c, W // 2, 1565, 2.6, t, "pop")
        cta_bottom(img, t, "Komm vorbei – Timmi freut sich!", t0=3.8)
        return img
    return frame


def story2():
    bg = gradient(W, H, (226, 242, 255), (100, 160, 235)).convert("RGBA")
    c = cat("04_zeigen", 260, 260)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 430, (255, 255, 255), 0.6)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "WLAN to go!", font=font("Bold", 96), fill=INK, anchor="mt"))
        a = ease((t - 0.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 545), "Internet überall, wo Strom ist.", font=fit(dd, "Internet überall, wo Strom ist.", "Bold", 50, W - 90, 30), fill=(20, 110, 210), anchor="mt"))
        if t > 0.9:
            q = back((t - 0.9) / 0.7)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            router_icon(ImageDraw.Draw(lay), W / 2 + 40, 900 + (1 - q) * 300, 380, t if t > 1.6 else 0.001, waves=3 if t > 1.6 else 0)
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * ease((t - 0.9) / 0.3))))
            img.alpha_composite(lay)
        a = ease((t - 2.0) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1050, "Unbegrenztes Datenvolumen", 40, fill=INK, col=AMBER))
        for i, (cx, txt) in enumerate(((240, "Urlaub"), (540, "Garten"), (840, "Unterwegs"))):
            a = ease((t - 2.6 - i * 0.25) / 0.4)
            layer(img, a, lambda dd, cx=cx, txt=txt: pill(dd, cx, 1160, txt, 36, fill=WHITE, col=INK))
        a = ease((t - 3.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1250), "Einfach mitnehmen!", font=font("Bold", 52), fill=INK, anchor="mt"))
        rs.put_cat(img, c, W // 2, 1580, 3.2, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


def story3():
    bg = gradient(W, H, (255, 224, 170), (140, 200, 240)).convert("RGBA")
    c = cat("13_strand", 520, 500)

    def frame(t):
        img = bg.copy()
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        sy = 1150 - 160 * ease(t / 2.5)
        glow(img, 860, round(sy), 260, (255, 210, 120), 0.7)
        d.ellipse((860 - 110, sy - 110, 860 + 110, sy + 110), fill=(255, 190, 70))
        # Ostsee-Wellen
        for k, (yb, col) in enumerate(((1280, (70, 150, 210)), (1350, (40, 120, 190)), (1430, (25, 95, 165)))):
            pts = [(x, yb + 18 * math.sin(x / 90 + t * (1.6 + 0.3 * k) + k)) for x in range(0, W + 20, 20)]
            d.polygon(pts + [(W, H), (0, H)], fill=col)
        sand = [(x, 1500 - 40 * math.sin(x / W * math.pi)) for x in range(0, W + 20, 20)]
        d.polygon(sand + [(W, H), (0, H)], fill=(240, 215, 160))
        img.alpha_composite(lay)
        head(img, "STORY 3 / 3")
        f = font("Bold", 104)
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Endlich", font=f, fill=INK, anchor="mt"))
        full = "Wochenende!"
        k = min(len(full), max(0, int((t - 0.7) / 0.06)))
        if k:
            ImageDraw.Draw(img).text((W / 2, 545), full[:k], font=fit(ImageDraw.Draw(img), full, "Bold", 104, W - 90, 60), fill=WHITE, anchor="mt", stroke_width=5, stroke_fill=INK)
        a = ease((t - 1.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 690), "Genieß die Ostsee!", font=font("Bold", 52), fill=INK, anchor="mt"))
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 790, "Tipp: Raster an – Horizont gerade!", 38, fill=INK, col=AMBER))
        rs.put_cat(img, c, 330, 1570, 1.2, t, "pop")
        cta_bottom(img, t, "Mo ab 9 Uhr wieder für dich da!", t0=3.6, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_freitag13", story1())
    if "2" in todo: rs.write("story_2_wlan_to_go", story2())
    if "3" in todo: rs.write("story_3_wochenende", story3())
