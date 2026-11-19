"""Story-Reihe 19.11. (3 × 7 s): Snake, Nokia-Klingelton 1902, Klingelton pro Kontakt."""
import math, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom
from render_tag3_story import antenna_phone

LCD, PIX = (170, 200, 150), (40, 60, 40)


def note(d, x, y, s, col):
    d.ellipse((x - s * 0.5, y - s * 0.35, x + s * 0.3, y + s * 0.35), fill=col)
    d.rectangle((x + s * 0.18, y - s * 1.8, x + s * 0.3, y), fill=col)
    d.polygon([(x + s * 0.3, y - s * 1.8), (x + s * 0.9, y - s * 1.4), (x + s * 0.9, y - s * 1.1), (x + s * 0.3, y - s * 1.5)], fill=col)


def story1():
    bg = gradient(W, H, (52, 46, 70), (14, 12, 20)).convert("RGBA")
    c = cat("09_empfang", 330, 340)
    path = [(i, 4) for i in range(2, 14)] + [(13, j) for j in range(5, 9)] + [(i, 8) for i in range(12, 1, -1)] + [(2, j) for j in range(7, 3, -1)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 440, AMBER, 0.45)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "THROWBACK THURSDAY", font=font("Bold", 52), fill=AMBER, anchor="mt"))
        layer(img, ease((t - 0.5) / 0.5), lambda dd: dd.text((W / 2, 510), "Erinnerst du dich?", font=font("Bold", 88), fill=WHITE, anchor="mt"))
        # großes Display mit Snake
        q = back((t - 0.8) / 0.6) if t > 0.8 else 0
        if q > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            sw, sh = 640 * q, 400 * q
            x0, y0 = W / 2 - sw / 2, 680
            d.rounded_rectangle((x0 - 30, y0 - 30, x0 + sw + 30, y0 + sh + 30), radius=40, fill=(60, 66, 80), outline=(20, 20, 24), width=6)
            d.rounded_rectangle((x0, y0, x0 + sw, y0 + sh), radius=16, fill=LCD)
            if q > 0.95:
                cs = sw / 16
                step = int(max(0, t - 1.4) * 9)
                n = 5 + step // 6
                food = path[(step + 12) % len(path)]
                fx, fy = x0 + food[0] * cs, y0 + food[1] * cs
                d.rectangle((fx + cs * 0.25, fy + cs * 0.25, fx + cs * 0.75, fy + cs * 0.75), fill=PIX)
                for k in range(n):
                    px, py = path[(step - k) % len(path)]
                    d.rectangle((x0 + px * cs + 2, y0 + py * cs + 2, x0 + (px + 1) * cs - 2, y0 + (py + 1) * cs - 2), fill=PIX)
                d.text((x0 + 20, y0 + 14), f"{step // 6 * 10:04d}", font=font("Bold", 36), fill=PIX)
            img.alpha_composite(lay)
        a = ease((t - 2.6) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1170, "Snake · SMS-Tasten · Klingeltöne", 38, fill=WHITE, col=INK))
        rs.put_cat(img, c, W // 2, 1640, 2.8, t, "pop")
        cta_bottom(img, t, "Komm vorbei – Timmi freut sich!", t0=3.8)
        return img
    return frame


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("03_idee", 250, 250)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 440, AMBER, 0.5)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Wusstest du?", font=font("Bold", 80), fill=WHITE, anchor="mt"))
        # klingelndes Handy mit Noten
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        ring = 0.6 < t < 2.6
        sh = math.sin(t * 40) * 10 if ring else 0
        antenna_phone(d, W / 2 - 0.42 * 420 / 2 + sh, 600, 420)
        for k in range(6):
            ph = (t * 0.6 + k / 6) % 1
            if t > 0.6:
                side = -1 if k % 2 else 1
                nx = W / 2 + side * (180 + ph * 160)
                ny = 820 - ph * 260
                a2 = round(255 * (1 - ph) * min(1, (t - 0.6) / 0.3))
                note(d, nx, ny, 34, AMBER + (a2,))
        img.alpha_composite(lay)
        p = ease((t - 2.4) / 0.9)
        if t > 2.4:
            yr = round(2026 - 124 * p)
            ImageDraw.Draw(img).text((W / 2, 1050), str(yr), font=font("Bold", 190), fill=AMBER, anchor="mt", stroke_width=6, stroke_fill=INK)
        a = ease((t - 3.3) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1255), "So alt ist der Nokia-Klingelton!", font=fit(dd, "So alt ist der Nokia-Klingelton!", "Bold", 52, W - 90, 30), fill=WHITE, anchor="mt"))
        layer(img, ease((t - 3.7) / 0.5), lambda dd: dd.text((W / 2, 1325), "Aus „Gran Vals“ von Francisco Tárrega", font=fit(dd, "Aus „Gran Vals“ von Francisco Tárrega", "Medium", 40, W - 300, 24), fill=(215, 215, 220), anchor="mt"))
        rs.put_cat(img, c, 900, 1680, 4.0, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=4.2)
        return img
    return frame


def story3():
    bg = gradient(W, H, (255, 240, 214), (255, 180, 90)).convert("RGBA")
    c = cat("02_handy", 340, 380)
    contacts = [("Mama", (230, 90, 120)), ("Bester Kumpel", (60, 140, 230)), ("Arbeit", (60, 170, 100))]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 430, (255, 255, 255), 0.6)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Wer ruft da an?", font=font("Bold", 96), fill=INK, anchor="mt"))
        layer(img, ease((t - 0.6) / 0.5), lambda dd: dd.text((W / 2, 545), "Eigener Klingelton pro Kontakt!", font=fit(dd, "Eigener Klingelton pro Kontakt!", "Bold", 54, W - 90, 30), fill=(160, 80, 0), anchor="mt"))
        active = int(max(0, t - 1.6) / 1.0) % 3 if t > 1.6 else -1
        for i, (name, col) in enumerate(contacts):
            a = ease((t - 0.9 - i * 0.2) / 0.4)
            y = 680 + i * 150
            def row(dd, y=y, name=name, col=col, i=i):
                on = i == active
                x0, x1 = 110, W - 110
                dd.rounded_rectangle((x0, y, x1, y + 120), radius=34, fill=WHITE, outline=col if on else (230, 230, 230), width=8 if on else 3)
                dd.ellipse((x0 + 24, y + 20, x0 + 104, y + 100), fill=col)
                dd.text((x0 + 64, y + 60), name[0], font=font("Bold", 46), fill=WHITE, anchor="mm")
                dd.text((x0 + 130, y + 60), name, font=font("Bold", 44), fill=INK, anchor="lm")
                note(dd, x1 - 70 + (math.sin(t * 30) * 6 if on else 0), y + 82, 30, col)
            layer(img, a, row)
        a = ease((t - 3.2) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1170, "Erkennen, ohne hinzuschauen", 40, fill=INK, col=AMBER))
        rs.put_cat(img, c, W // 2, 1640, 3.4, t, "pop")
        cta_bottom(img, t, "Hilfe beim Einstellen? Komm vorbei!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_throwback", story1())
    if "2" in todo: rs.write("story_2_klingelton", story2())
    if "3" in todo: rs.write("story_3_kontakte", story3())
