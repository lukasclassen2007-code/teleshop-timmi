"""Story-Reihe 18.11. (3 × 7 s): KI Vor-/Nachteile, Black Week, GTA VI morgen."""
import math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

GREEN, RED = (40, 160, 80), (210, 50, 50)


def story1():
    bg = gradient(W, H, (226, 244, 250), (90, 170, 210)).convert("RGBA")
    c = cat("03_idee", 330, 340)
    pro = ["Fotos verbessern", "Texte übersetzen", "Zeit sparen"]
    con = ["Fehler möglich", "Fake-Stimmen", "Daten schützen"]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 440, (255, 255, 255), 0.6)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "KI im Alltag", font=font("Bold", 104), fill=INK, anchor="mt"))
        a = ease((t - 0.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 550), "Praktisch – aber mit Köpfchen nutzen!", font=fit(dd, "Praktisch – aber mit Köpfchen nutzen!", "Bold", 48, W - 90, 28), fill=(20, 80, 120), anchor="mt"))
        # Waage
        tilt = 0.12 * math.sin(t * 1.6) * ease((t - 1.0) / 0.6)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        cx, cy, L = W / 2, 720, 265
        if t > 0.9:
            q = ease((t - 0.9) / 0.4)
            d.polygon([(cx - 40, 1060), (cx + 40, 1060), (cx, cy)], fill=(40, 40, 50, round(255 * q)))
            dx, dy = L * math.cos(tilt), L * math.sin(tilt)
            d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(40, 40, 50, round(255 * q)), width=14)
            d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=AMBER + (round(255 * q),))
        img.alpha_composite(lay)
        for side, items, col, title in ((-1, pro, GREEN, "Vorteile"), (1, con, RED, "Risiken")):
            dx, dy = L * math.cos(tilt), L * math.sin(tilt)
            px, py = cx + side * dx, cy + side * dy + 30
            a = ease((t - 1.3) / 0.4)
            def draw(dd, px=px, py=py, items=items, col=col, title=title):
                dd.rounded_rectangle((px - 150, py, px + 150, py + 70), radius=35, fill=col)
                dd.text((px, py + 35), title, font=font("Bold", 40), fill=WHITE, anchor="mm")
            layer(img, a, draw)
            for i, it in enumerate(items):
                a2 = ease((t - 1.8 - i * 0.35 - (0.15 if side > 0 else 0)) / 0.35)
                layer(img, a2, lambda dd, px=px, py=py, it=it, i=i: pill(dd, px, py + 100 + i * 80, it, 30, fill=WHITE, col=INK))
        rs.put_cat(img, c, W // 2, 1640, 3.4, t, "pop")
        cta_bottom(img, t, "Fragen zu KI? Komm vorbei!", t0=4.0, fill=INK, col=AMBER)
        return img
    return frame


def story2():
    bg = gradient(W, H, (30, 30, 34), (8, 8, 10)).convert("RGBA")
    c = cat("16_geschenk", 380, 420)
    random.seed(21)
    conf = [(random.uniform(0, W), random.uniform(-H, 0), random.uniform(8, 16), random.uniform(220, 380), random.choice([AMBER, WHITE, (255, 200, 120)]), random.uniform(0, 6.28)) for _ in range(70)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 900, 480, AMBER, 0.45)
        if t > 1.2:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            for x, y0, s, v, col, ph in conf:
                y = y0 + (t - 1.2) * v
                if -20 < y < H:
                    xx = x + math.sin(t * 3 + ph) * 20
                    d.rectangle((xx - s / 2, y - s / 4, xx + s / 2, y + s / 4), fill=col + (220,))
            img.alpha_composite(lay)
        head(img, "STORY 2 / 3")
        q = back((t - 0.3) / 0.6) if t > 0.3 else 0
        if q > 0:
            sz = max(1, round(150 * q))
            ImageDraw.Draw(img).text((W / 2, 520), "BLACK", font=font("Bold", sz), fill=WHITE, anchor="mm")
        q2 = back((t - 0.7) / 0.6) if t > 0.7 else 0
        if q2 > 0:
            sz = max(1, round(150 * q2))
            ImageDraw.Draw(img).text((W / 2, 680), "WEEK", font=font("Bold", sz), fill=AMBER, anchor="mm")
        a = ease((t - 1.5) / 0.5)
        layer(img, a, lambda dd: pill(dd, W / 2, 820, "läuft jetzt – bis 15.12.!", 48, fill=AMBER, col=INK))
        a = ease((t - 2.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 960), "Starke Angebote für Mobilfunk & Internet", font=fit(dd, "Starke Angebote für Mobilfunk & Internet", "Bold", 46, W - 90, 28), fill=WHITE, anchor="mt"))
        a = ease((t - 2.8) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1040), "mit persönlicher Beratung", font=font("Medium", 42), fill=(210, 210, 215), anchor="mt"))
        rs.put_cat(img, c, W // 2, 1640, 3.0, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=3.6)
        return img
    return frame


def story3():
    bg = gradient(W, H, (40, 20, 70), (10, 8, 22)).convert("RGBA")
    c = cat("08_speed", 520, 400)

    def frame(t):
        img = bg.copy()
        glow(img, 860, 1300, 420, (255, 80, 170), 0.45)
        glow(img, 200, 600, 380, (80, 160, 255), 0.35)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "GTA VI", font=font("Bold", 140), fill=WHITE, anchor="mt"))
        a = ease((t - 0.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 590), "erscheint morgen!", font=font("Bold", 76), fill=AMBER, anchor="mt"))
        # Kalenderblatt 18 -> 19
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if t > 0.9:
            q = back((t - 0.9) / 0.5)
            cw, ch = 300 * q, 280 * q
            x0, y0 = W / 2 - cw / 2, 720
            d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=26, fill=WHITE, outline=INK, width=6)
            if q > 0.9:
                d.rounded_rectangle((x0, y0, x0 + cw, y0 + 70), radius=26, fill=(190, 0, 140))
                d.rectangle((x0, y0 + 44, x0 + cw, y0 + 70), fill=(190, 0, 140))
                d.text((W / 2, y0 + 36), "NOVEMBER", font=font("Bold", 32), fill=WHITE, anchor="mm")
                day = "19" if t > 2.2 else "18"
                flip = 1 - abs(math.cos(min(1, max(0, (t - 1.9) / 0.6)) * math.pi)) if 1.9 < t < 2.5 else 1
                sz = max(10, round(150 * (flip if 1.9 < t < 2.5 else 1)))
                d.text((W / 2, y0 + 170), day, font=font("Bold", sz), fill=INK, anchor="mm")
        img.alpha_composite(lay)
        # Download-Balken
        p = ease((t - 2.6) / 1.6)
        if t > 2.4:
            a = ease((t - 2.4) / 0.3)
            def bar(dd):
                x0, y0, x1 = 120, 1070, W - 120
                dd.rounded_rectangle((x0, y0, x1, y0 + 56), radius=28, fill=(255, 255, 255))
                dd.rounded_rectangle((x0 + 8, y0 + 8, x0 + 8 + (x1 - x0 - 16) * max(0.03, p), y0 + 48), radius=20, fill=AMBER)
                dd.text((W / 2, y0 + 78), "Bereit zum Zocken? " + f"{round(p * 100)} %", font=font("Bold", 42), fill=WHITE, anchor="mt")
            layer(img, a, bar)
        rs.put_cat(img, c, W // 2, 1640, 3.4, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=4.2)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_ki", story1())
    if "2" in todo: rs.write("story_2_black_week", story2())
    if "3" in todo: rs.write("story_3_gta", story3())
