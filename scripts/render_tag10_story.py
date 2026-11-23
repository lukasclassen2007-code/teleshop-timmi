"""Story-Reihe 23.11. (3 × 7 s): Fake-Shop erkennen, erster Online-Kauf 1994, sicher bezahlen."""
import math, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

RED, GREEN = (210, 45, 50), (40, 160, 80)


def story1():
    bg = gradient(W, H, (255, 236, 236), (235, 120, 120)).convert("RGBA")
    c = cat("06_detektiv", 280, 280)
    flags = [("Zu billig?", 960), ("Kein Impressum", 1045), ("Nur Vorkasse", 1130)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 430, (255, 255, 255), 0.55)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Fake-Shop?", font=font("Bold", 110), fill=INK, anchor="mt"))
        # Browserfenster
        q = back((t - 0.5) / 0.6) if t > 0.5 else 0
        if q > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            bw, bh = 820 * q, 360 * q
            x0, y0 = W / 2 - bw / 2, 560
            d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=26, fill=WHITE, outline=INK, width=6)
            if q > 0.95:
                d.rounded_rectangle((x0, y0, x0 + bw, y0 + 60), radius=26, fill=(225, 225, 232))
                d.rectangle((x0, y0 + 36, x0 + bw, y0 + 60), fill=(225, 225, 232))
                for k, col in enumerate(((240, 90, 90), (250, 200, 70), (90, 200, 110))):
                    d.ellipse((x0 + 24 + k * 34, y0 + 20, x0 + 46 + k * 34, y0 + 42), fill=col)
                pulse = 1 + 0.06 * math.sin(t * 8)
                d.rounded_rectangle((x0 + 60, y0 + 100, x0 + bw - 60, y0 + 260), radius=20, fill=RED)
                d.text((W / 2, y0 + 180), "SALE -90 %", font=font("Bold", round(84 * pulse)), fill=WHITE, anchor="mm")
                for k in range(3):
                    d.rounded_rectangle((x0 + 60 + k * 240, y0 + 280, x0 + 260 + k * 240, y0 + 330), radius=16, fill=(240, 240, 245))
            img.alpha_composite(lay)
        # Warnzeichen
        for i, (txt, y) in enumerate(flags):
            a = ease((t - 1.8 - i * 0.5) / 0.35)
            def fl(dd, txt=txt, y=y):
                f = font("Bold", 40)
                tw = dd.textlength("! " + txt, font=f)
                bx0 = W / 2 - (tw + 40) / 2
                dd.rounded_rectangle((bx0, y, bx0 + tw + 40, y + 70), radius=35, fill=INK)
                dd.text((bx0 + 20, y + 35), "! " + txt, font=f, fill=AMBER, anchor="lm")
            layer(img, a, fl)
        a = ease((t - 3.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1235), "Lieber zweimal hinschauen!", font=fit(dd, "Lieber zweimal hinschauen!", "Bold", 60, W - 90, 34), fill=INK, anchor="mt"))
        rs.put_cat(img, c, W // 2, 1640, 3.0, t, "pop")
        cta_bottom(img, t, "Unsicher? Frag Timmi im Shop!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("03_idee", 260, 260)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 800, 440, AMBER, 0.5)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Der erste Online-Kauf", font=fit(dd, "Der erste Online-Kauf", "Bold", 80, W - 80, 40), fill=WHITE, anchor="mt"))
        # CD dreht sich
        if t > 0.6:
            q = back((t - 0.6) / 0.6)
            r = 230 * q
            cx, cy = W / 2, 800
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(215, 220, 230), outline=(150, 155, 170), width=6)
            for k in range(6):
                ang = t * 4 + k * 1.047
                d.pieslice((cx - r * 0.95, cy - r * 0.95, cx + r * 0.95, cy + r * 0.95), math.degrees(ang), math.degrees(ang) + 22, fill=(170 + 14 * k, 200, 255 - 12 * k))
            d.ellipse((cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3), fill=(235, 238, 245))
            d.ellipse((cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12), fill=(30, 26, 44))
            img.alpha_composite(lay)
        p = ease((t - 1.6) / 1.0)
        if t > 1.6:
            yr = round(2026 - 32 * p)
            ImageDraw.Draw(img).text((W / 2, 1070), str(yr), font=font("Bold", 190), fill=AMBER, anchor="mt", stroke_width=6, stroke_fill=INK)
        a = ease((t - 2.8) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1290), "Eine Musik-CD – sicher per Internet bezahlt!", font=fit(dd, "Eine Musik-CD – sicher per Internet bezahlt!", "Bold", 48, W - 90, 28), fill=WHITE, anchor="mt"))
        rs.put_cat(img, c, 900, 1680, 3.4, t, "pop")
        cta_bottom(img, t, "Besuch Timmi im Shop!", t0=3.8)
        return img
    return frame


def shield(d, cx, cy, s, col):
    pts = [(cx, cy - s), (cx + s * 0.8, cy - s * 0.65), (cx + s * 0.7, cy + s * 0.3), (cx, cy + s), (cx - s * 0.7, cy + s * 0.3), (cx - s * 0.8, cy - s * 0.65)]
    d.polygon(pts, fill=col, outline=INK)
    d.line([(cx - s * 0.35, cy), (cx - s * 0.08, cy + s * 0.3), (cx + s * 0.4, cy - s * 0.3)], fill=WHITE, width=max(8, int(s * 0.13)), joint="curve")


def story3():
    bg = gradient(W, H, (232, 248, 238), (110, 200, 150)).convert("RGBA")
    c = cat("04_zeigen", 330, 340)
    tips = ["Käuferschutz nutzen", "Keine Überweisung an Unbekannte", "Bewertungen woanders prüfen"]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 760, 420, (255, 255, 255), 0.6)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Sicher bezahlen!", font=fit(dd, "Sicher bezahlen!", "Bold", 100, W - 80, 50), fill=INK, anchor="mt"))
        if t > 0.6:
            q = back((t - 0.6) / 0.6)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            shield(ImageDraw.Draw(lay), W / 2, 720, 150 * q * (1 + 0.04 * math.sin(t * 5)), GREEN)
            img.alpha_composite(lay)
        for i, tp in enumerate(tips):
            a = ease((t - 1.6 - i * 0.45) / 0.4)
            layer(img, a, lambda dd, tp=tp, i=i: pill(dd, W / 2, 930 + i * 95, "✓ " + tp if False else tp, 40, fill=WHITE, col=INK))
        rs.put_cat(img, c, W // 2, 1640, 3.2, t, "pop")
        cta_bottom(img, t, "Lieber persönlich? Komm vorbei!", t0=3.8, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_fake_shop", story1())
    if "2" in todo: rs.write("story_2_erster_kauf", story2())
    if "3" in todo: rs.write("story_3_sicher_bezahlen", story3())
