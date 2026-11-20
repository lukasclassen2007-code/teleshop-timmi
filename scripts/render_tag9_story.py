"""Story-Reihe 20.11. (3 × 7 s): Wochenende lädt, Emoji-Fun-Fact, Serienbild-Tipp."""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

YEL, TEAR = (255, 205, 60), (90, 180, 255)


def story1():
    bg = gradient(W, H, (255, 236, 190), (255, 160, 70)).convert("RGBA")
    c = cat("12_chillen", 560, 440)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1250, 480, (255, 255, 255), 0.5)
        head(img, "STORY 1 / 3")
        p = ease((t - 0.6) / 2.2)
        done = t > 2.9
        a = ease((t - 0.2) / 0.4) * (1 - ease((t - 2.9) / 0.3))
        layer(img, a, lambda dd: dd.text((W / 2, 440), "Wochenende", font=font("Bold", 100), fill=INK, anchor="mt"))
        layer(img, a, lambda dd: dd.text((W / 2, 560), "wird geladen …", font=font("Bold", 70), fill=WHITE, anchor="mt", stroke_width=4, stroke_fill=INK))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        x0, y0, x1 = 120, 720, W - 120
        d.rounded_rectangle((x0, y0, x1, y0 + 90), radius=45, fill=WHITE, outline=INK, width=7)
        d.rounded_rectangle((x0 + 12, y0 + 12, x0 + 12 + (x1 - x0 - 24) * max(0.04, p), y0 + 78), radius=33, fill=(60, 180, 95) if done else AMBER)
        d.text((W / 2, y0 + 120), f"{round(p * 100)} %", font=font("Bold", 64), fill=INK, anchor="mt")
        img.alpha_composite(lay)
        if done:
            q = back((t - 2.9) / 0.5)
            sz = max(1, round(110 * q))
            ImageDraw.Draw(img).text((W / 2, 520), "Wochenend-", font=font("Bold", sz), fill=INK, anchor="mm")
            ImageDraw.Draw(img).text((W / 2, 640), "Modus: AN!", font=font("Bold", sz), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=INK)
            for k in range(6):
                ang = t * 1.5 + k * 1.05
                star(ImageDraw.Draw(img), W / 2 + math.cos(ang) * 420, 580 + math.sin(ang) * 120, 18, WHITE)
        rs.put_cat(img, c, W // 2, 1600, 3.2, t, "pop")
        cta_bottom(img, t, "Heute bis 17 Uhr für euch da!", t0=3.8)
        return img
    return frame


def emoji(d, cx, cy, r, t):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL, outline=(200, 140, 20), width=8)
    for s in (-1, 1):
        ex = cx + s * r * 0.38
        d.arc((ex - r * 0.2, cy - r * 0.38, ex + r * 0.2, cy - r * 0.02), 200, 340, fill=(80, 50, 20), width=max(6, int(r * 0.07)))
    d.chord((cx - r * 0.55, cy - r * 0.05, cx + r * 0.55, cy + r * 0.7), 0, 180, fill=(110, 40, 30))
    d.chord((cx - r * 0.42, cy + r * 0.3, cx + r * 0.42, cy + r * 0.68), 0, 180, fill=(240, 100, 110))
    d.rectangle((cx - r * 0.5, cy + r * 0.27, cx + r * 0.5, cy + r * 0.35), fill=WHITE)
    for s in (-1, 1):
        k = (t * 1.2) % 1
        tx, ty = cx + s * (r * 0.68 + k * r * 0.25), cy - r * 0.1 + k * r * 0.5
        d.ellipse((tx - r * 0.12, ty - r * 0.16, tx + r * 0.12, ty + r * 0.16), fill=TEAR)


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("01_winken", 300, 320)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 820, 440, AMBER, 0.5)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Wort des Jahres 2015?", font=fit(dd, "Wort des Jahres 2015?", "Bold", 80, W - 80, 40), fill=WHITE, anchor="mt"))
        if t > 0.9:
            q = back((t - 0.9) / 0.6)
            bob = math.sin(t * 6) * 14 if t > 1.6 else 0
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            emoji(ImageDraw.Draw(lay), W / 2, 790 + bob, 230 * q, t)
            img.alpha_composite(lay)
        a = ease((t - 2.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1080), "Gar kein Wort – ein Emoji!", font=fit(dd, "Gar kein Wort – ein Emoji!", "Bold", 66, W - 80, 36), fill=AMBER, anchor="mt"))
        a = ease((t - 2.8) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1180), "So entschied das Oxford-Wörterbuch.", font=fit(dd, "So entschied das Oxford-Wörterbuch.", "Medium", 44, W - 90, 26), fill=(220, 220, 228), anchor="mt"))
        rs.put_cat(img, c, W // 2, 1640, 3.2, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=3.8)
        return img
    return frame


def story3():
    bg = gradient(W, H, (226, 244, 255), (110, 180, 235)).convert("RGBA")
    c = cat("13_strand", 360, 380)
    cols = [(255, 190, 120), (130, 200, 250), (255, 150, 170), (160, 220, 150), (250, 220, 120)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 440, (255, 255, 255), 0.6)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Klick-klick-klick!", font=fit(dd, "Klick-klick-klick!", "Bold", 96, W - 80, 50), fill=INK, anchor="mt"))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, col in enumerate(cols):
            tt = t - 0.8 - i * 0.25
            if tt > 0:
                q = ease(tt / 0.4)
                ang = (i - 2) * 0.14 * q
                cx, cy = W / 2 + (i - 2) * 70 * q, 800
                w, h = 380, 300
                pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
                rot = [(cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)) for x, y in pts]
                d.polygon(rot, fill=WHITE, outline=(200, 200, 210))
                inner = [(cx + x * 0.86 * math.cos(ang) - (y * 0.82 - 10) * math.sin(ang), cy + x * 0.86 * math.sin(ang) + (y * 0.82 - 10) * math.cos(ang)) for x, y in pts]
                d.polygon(inner, fill=col)
                if i == 4 and t > 2.4:
                    star(d, cx + 130, cy - 110, 34, AMBER)
        img.alpha_composite(lay)
        flash = max(0.0, 1 - ((t - 0.8) % 0.25) / 0.12) if 0.8 < t < 2.05 else 0
        if flash > 0:
            fl = Image.new("RGBA", img.size, (255, 255, 255, round(110 * flash)))
            img.alpha_composite(fl)
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1050, "Serienbild = perfekter Moment", 44, fill=INK, col=AMBER))
        a = ease((t - 2.9) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1150), "Das beste Foto behalten, den Rest löschen.", font=fit(dd, "Das beste Foto behalten, den Rest löschen.", "Medium", 42, W - 90, 26), fill=INK, anchor="mt"))
        rs.put_cat(img, c, W // 2, 1640, 3.2, t, "pop")
        cta_bottom(img, t, "Schönes Wochenende!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_wochenende", story1())
    if "2" in todo: rs.write("story_2_emoji", story2())
    if "3" in todo: rs.write("story_3_serienbild", story3())
