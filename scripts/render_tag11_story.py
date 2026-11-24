"""Story-Reihe 24.11. (3 × 7 s): Fragen & Antworten, Nummer mitnehmen, Checkliste."""
import math, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, head, star, W, H
from timmi_lib import font, fit, gradient, glow, cat, INK, AMBER, WHITE
from render_tag_story import cta_bottom

BLUE, GREEN = (70, 90, 200), (40, 160, 80)
QA = [("Nummer mitnehmen?", "Ja, klar!"), ("Daten aufs neue Handy?", "Wir helfen!"), ("Vertrag verlängern?", "Wir schauen gemeinsam!")]


def story1():
    bg = gradient(W, H, (232, 238, 255), (130, 150, 230)).convert("RGBA")
    c = cat("03_idee", 380, 420)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 850, 440, (255, 255, 255), 0.6)
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Frag Timmi!", font=font("Bold", 110), fill=INK, anchor="mt"))
        for i, (q, ans) in enumerate(QA):
            a = ease((t - 0.7 - i * 0.4) / 0.4)
            y = 600 + i * 190
            solved = t > 2.3 + i * 0.5
            def card(dd, q=q, ans=ans, y=y, solved=solved):
                dd.rounded_rectangle((90, y, W - 90, y + 160), radius=34, fill=WHITE)
                dd.ellipse((115, y + 35, 205, y + 125), fill=GREEN if solved else BLUE)
                if solved:
                    dd.line([(135, y + 82), (155, y + 102), (188, y + 60)], fill=WHITE, width=12, joint="curve")
                else:
                    dd.text((160, y + 80), "?", font=font("Bold", 58), fill=WHITE, anchor="mm")
                dd.text((235, y + 30), q, font=fit(dd, q, "Bold", 46, W - 90 - 260, 28), fill=INK)
                if solved:
                    dd.text((235, y + 96), ans, font=font("Bold", 38), fill=GREEN)
            layer(img, a, card)
        rs.put_cat(img, c, W // 2, 1650, 3.4, t, "pop")
        cta_bottom(img, t, "Noch Fragen? Komm vorbei!", t0=4.0, fill=INK, col=AMBER)
        return img
    return frame


def phone(d, cx, cy, s, col):
    d.rounded_rectangle((cx - s * 0.25, cy - s * 0.5, cx + s * 0.25, cy + s * 0.5), radius=s * 0.08, fill=INK)
    d.rounded_rectangle((cx - s * 0.21, cy - s * 0.44, cx + s * 0.21, cy + s * 0.44), radius=s * 0.05, fill=col)


def story2():
    bg = gradient(W, H, (30, 26, 44), (10, 10, 14)).convert("RGBA")
    c = cat("02_handy", 380, 420)

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 820, 440, AMBER, 0.5)
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Neuer Anbieter?", font=font("Bold", 92), fill=WHITE, anchor="mt"))
        layer(img, ease((t - 0.6) / 0.5), lambda dd: dd.text((W / 2, 545), "Deine Nummer kommt mit!", font=fit(dd, "Deine Nummer kommt mit!", "Bold", 62, W - 90, 34), fill=AMBER, anchor="mt"))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        q = ease((t - 0.8) / 0.5)
        if q > 0:
            phone(d, 250, 830, 340 * q, (90, 100, 120))
            phone(d, W - 250, 830, 340 * q, (255, 200, 120))
            d.text((250, 1030), "alt", font=font("Bold", 38), fill=(200, 200, 210), anchor="mt")
            d.text((W - 250, 1030), "neu", font=font("Bold", 38), fill=AMBER, anchor="mt")
        img.alpha_composite(lay)
        p = ease((t - 1.6) / 1.2)
        if t > 1.4:
            x = 250 + (W - 500) * p
            y = 830 - 140 * math.sin(math.pi * p)
            layer(img, 1, lambda dd: pill(dd, x, y - 30, "Deine Nummer", 40, fill=WHITE, col=INK))
        a = ease((t - 3.0) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1120), "Möglich seit 2002 – seit 2021 kostenlos.", font=fit(dd, "Möglich seit 2002 – seit 2021 kostenlos.", "Bold", 48, W - 90, 28), fill=WHITE, anchor="mt"))
        rs.put_cat(img, c, W // 2, 1650, 3.4, t, "pop")
        cta_bottom(img, t, "Wir kümmern uns darum!", t0=4.0)
        return img
    return frame


def story3():
    bg = gradient(W, H, (255, 240, 214), (255, 180, 90)).convert("RGBA")
    c = cat("04_zeigen", 380, 420)
    items = ["Personalausweis", "Bankkarte / IBAN", "Altes Handy + Codes"]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 820, 430, (255, 255, 255), 0.6)
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 425), "Das bringst du mit!", font=fit(dd, "Das bringst du mit!", "Bold", 92, W - 80, 50), fill=INK, anchor="mt"))
        # Klemmbrett
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        q = back((t - 0.5) / 0.6) if t > 0.5 else 0
        if q > 0.05:
            bw, bh = 760 * q, 640 * q
            x0, y0 = W / 2 - bw / 2, 580
            d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=30, fill=(170, 120, 70))
            d.rounded_rectangle((x0 + 24, y0 + 40, x0 + bw - 24, y0 + bh - 24), radius=18, fill=WHITE)
            d.rounded_rectangle((W / 2 - 110 * q, y0 - 20, W / 2 + 110 * q, y0 + 50), radius=16, fill=(90, 90, 100))
        img.alpha_composite(lay)
        if q > 0.95:
            for i, it in enumerate(items):
                y = 700 + i * 160
                done = t > 1.6 + i * 0.6
                def row(dd, it=it, y=y, done=done):
                    dd.rounded_rectangle((200, y, 270, y + 70), radius=14, outline=INK, width=6, fill=WHITE)
                    if done:
                        dd.line([(212, y + 36), (232, y + 56), (262, y + 14)], fill=GREEN, width=12, joint="curve")
                    dd.text((300, y + 35), it, font=fit(dd, it, "Bold", 48, 560, 30), fill=INK, anchor="lm")
                layer(img, ease((t - 1.2 - i * 0.2) / 0.3), row)
        rs.put_cat(img, c, W // 2, 1650, 3.4, t, "pop")
        cta_bottom(img, t, "Weitere Infos bei uns im Shop!", t0=4.0, fill=INK, col=AMBER)
        return img
    return frame


if __name__ == "__main__":
    rs.OUT = sys.argv[1]
    todo = sys.argv[2:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_fragen", story1())
    if "2" in todo: rs.write("story_2_nummer", story2())
    if "3" in todo: rs.write("story_3_checkliste", story3())
