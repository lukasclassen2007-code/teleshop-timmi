"""Animierte Story-Reihe zum Tarif-Portfolio (3 × 7 s, 1080x1920, ohne Ton).
Aufruf: python3 render_tarife_story.py tarife.json ausgabeordner [1 2 3]
"""
import json, math, random, sys
from PIL import Image, ImageDraw
import render_story_anim as rs
from render_story_anim import ease, back, layer, pill, star, head, W, H
from timmi_lib import font, fit, wrap, gradient, glow, cat, shadow, INK, AMBER, WHITE

RED = (230, 0, 0)
NOTE = "*24 Monate Mindestlaufzeit, Anschlusspreis 0 €. Aktion 10.11.–15.12.2026. Alle Bedingungen im Shop."


def note(img, text=NOTE, dark=True):
    d = ImageDraw.Draw(img)
    f = font("Regular", 22)
    lines = wrap(d, text, f, W - 120)
    y = 1700
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(190, 190, 190) if dark else (70, 70, 70), anchor="mt")
        y += 28


# ---------- Story 1: Welcher Surfer-Typ bist du? ----------
def make_story1(data):
    bg = gradient(W, H, (40, 36, 52), (12, 12, 14)).convert("RGBA")
    c = cat("03_idee", 520, 470)
    rows = [(g["kicker"].title(), g["kurz"]) for g in data["gruppen"]] + [("Familie", "Unbegrenzt zu zweit")]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1250, round(430 + 30 * math.sin(t * 2.5)), AMBER, 0.55)
        rs.put_cat(img, c, W // 2, 1590, 0.3, t, "pop")
        head(img, "STORY 1 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430 + round(20 * (1 - a))), "Welcher Surfer-Typ", font=font("Bold", 92), fill=WHITE, anchor="mt"))
        a2 = ease((t - 0.5) / 0.5)
        layer(img, a2, lambda dd: dd.text((W / 2, 540 + round(20 * (1 - a2))), "bist du?", font=font("Bold", 92), fill=AMBER, anchor="mt"))
        # drei Karten fliegen nacheinander von rechts ein
        for i, (k, v) in enumerate(rows):
            p = ease((t - 1.2 - i * 0.45) / 0.55)
            if p <= 0:
                continue
            x = 140 + round((1 - p) * 1000)
            y = 680 + i * 112

            def card(dd, x=x, y=y, k=k, v=v):
                dd.rounded_rectangle((x, y, x + 800, y + 96), radius=30, fill=WHITE)
                dd.text((x + 36, y + 48), k, font=font("Bold", 38), fill=INK, anchor="lm")
                dd.text((x + 770, y + 48), v, font=font("Bold", 32), fill=(200, 110, 0), anchor="rm")
            layer(img, 1.0, card)
        a = ease((t - 3.4) / 0.5) * (0.7 + 0.3 * math.sin(t * 5) ** 2)
        layer(img, a, lambda dd: pill(dd, W / 2, 1600, "Timmi findet deinen Tarif – im Shop!", 36))
        return img
    return frame


# ---------- Story 2: 3× Daten, Zahl zählt hoch ----------
def make_story2(data):
    g = data["gruppen"][1]
    bg = gradient(W, H, (255, 236, 205), (255, 160, 60)).convert("RGBA")
    rays = rs.rays_image((255, 255, 255, 50))
    c = cat("08_speed", 740, 520)

    def frame(t):
        img = bg.copy()
        r = rays.rotate(t * 10, resample=Image.BICUBIC).crop((1200 - W // 2, 1200 - 1150, 1200 + W // 2, 1200 - 1150 + H))
        img.alpha_composite(r)
        glow(img, W // 2, 1150, 450, (255, 255, 255), 0.5)
        # Timmi fliegt auf der Rakete von rechts herein (Nase zeigt nach links)
        if t >= 0.2:
            p = ease((t - 0.2) / 0.9)
            x = W // 2 - c.width // 2 + round((1 - p) * 1200)
            img.alpha_composite(c, (x, 1560 - c.height))
        head(img, "STORY 2 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "BLACK WEEK", font=font("Bold", 64), fill=INK, anchor="mt"))
        layer(img, a, lambda dd: dd.text((W / 2, 505), "Datenvolumen hoch 3", font=font("Bold", 64), fill=INK, anchor="mt"))
        # Zähler 50 -> 150 GB
        p = ease((t - 0.9) / 1.4)
        val = 50 + round(100 * p) if t > 0.9 else 50
        sz = 210 + round(18 * max(0.0, 1 - abs(t - 2.35) / 0.25))  # kurzer "Pop" beim Erreichen
        d = ImageDraw.Draw(img)
        d.text((W / 2, 600), f"{val} GB", font=font("Bold", sz), fill=WHITE, anchor="mt", stroke_width=6, stroke_fill=INK)
        a = ease((t - 2.4) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 850), "statt 50 GB", font=font("Bold", 46), fill=INK, anchor="mt"))
        a = ease((t - 2.9) / 0.5)

        def price(dd):
            pill(dd, W / 2, 935, "Zum gleichen Preis wie sonst!", 36, fill=INK, col=AMBER)
        layer(img, a, price)
        a = ease((t - 3.4) / 0.5)
        pulse = 1 + 0.035 * math.sin(t * 5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1610, "Komm vorbei – Timmi zeigt's dir!", round(36 * pulse)))
        return img
    return frame


# ---------- Story 3: Familienspezial, weihnachtlich ----------
def make_story3(data):
    f = data["familie"]
    bg = gradient(W, H, (150, 20, 30), (55, 6, 12)).convert("RGBA")
    c = cat(f["pose"], 560, 560)
    random.seed(11)
    flakes = [(random.uniform(0, W), random.uniform(-H, H), random.uniform(3, 10), random.uniform(60, 160), random.uniform(0, 6.28)) for _ in range(90)]

    def frame(t):
        img = bg.copy()
        glow(img, W // 2, 1250, round(440 + 30 * math.sin(t * 2)), (255, 200, 120), 0.5)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for x, y0, r, v, ph in flakes:
            y = (y0 + t * v) % (H + 40) - 20
            xx = x + math.sin(t * 1.5 + ph) * 25
            ld.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 255, 255, 200))
        img.alpha_composite(lay)
        rs.put_cat(img, c, W // 2, 1580, 0.6, t, "pop")
        head(img, "STORY 3 / 3")
        a = ease((t - 0.2) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 430), "Unbegrenzt surfen", font=font("Bold", 84), fill=WHITE, anchor="mt"))
        a2 = ease((t - 0.6) / 0.5)
        layer(img, a2, lambda dd: dd.text((W / 2, 540), "für dich & deine Liebsten?", font=fit(dd, "für dich & deine Liebsten?", "Bold", 70, W - 80, 40), fill=AMBER, anchor="mt"))
        a = ease((t - 1.9) / 0.5)

        def card(dd):
            x0, y0 = W / 2 - 330, 670 + round(30 * (1 - a))
            dd.rounded_rectangle((x0, y0, x0 + 660, y0 + 250), radius=36, fill=WHITE)
            dd.text((W / 2, y0 + 36), "Vodafone 5G-Netz", font=font("Bold", 34), fill=RED, anchor="mt")
            dd.text((W / 2, y0 + 84), "Unbegrenzt zu zweit", font=fit(dd, "Unbegrenzt zu zweit", "Bold", 92, 600, 50), fill=INK, anchor="mt")
        layer(img, a, card)
        a = ease((t - 3.2) / 0.5)
        pulse = 1 + 0.035 * math.sin(t * 5)
        layer(img, a, lambda dd: pill(dd, W / 2, 1600, "Den Preis flüstert dir Timmi im Shop!", round(34 * pulse)))
        a = ease((t - 3.6) / 0.5)
        layer(img, a, lambda dd: dd.text((W / 2, 1700), "Poststraße 34 · Mo–Fr 9–17 Uhr", font=font("Bold", 36), fill=WHITE, anchor="mt"))
        return img
    return frame


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    rs.OUT = sys.argv[2]
    todo = sys.argv[3:] or ["1", "2", "3"]
    if "1" in todo: rs.write("story_1_surfertyp", make_story1(data))
    if "2" in todo: rs.write("story_2_3xdaten", make_story2(data))
    if "3" in todo: rs.write("story_3_familie", make_story3(data))
