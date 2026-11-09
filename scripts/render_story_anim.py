"""Animierte Story-Reihe (3 Clips, 1080x1920, je 7 s, ohne Ton) für den 9.11.2026.
Timmi steht nach dem Auftritt pixelgenau still (kein Zittern); Leben kommt von Licht, Partikeln, Text und Bewegung.
Aufruf: python3 render_story_anim.py
"""
import math, random, subprocess, os
from PIL import Image, ImageDraw, ImageFilter
from timmi_lib import font, fit, gradient, glow, logo, cat, shadow, chevron, INK, AMBER, WHITE

W, H, FPS, DUR = 1080, 1920, 30, 7.0
OUT = "launch_2026-11-09"
GREY_L = (225, 225, 225)


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def back(x):
    x = max(0.0, min(1.0, x)); c = 1.6
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def layer(img, alpha, fn):
    if alpha <= 0:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(lay))
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay)


def put_cat(img, c, cx, by, t0, t, mode="pop", dx=0):
    """Auftritt der Katze; danach pixelgenau an fester Position."""
    if t < t0:
        return
    if mode == "pop":
        p = back((t - t0) / 0.6)
        if p < 0.999:
            s = 0.6 + 0.4 * p
            cc = c.resize((max(1, round(c.width * s)), max(1, round(c.height * s))), Image.BICUBIC)
            a = ease((t - t0) / 0.25)
            cc.putalpha(cc.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(cc, (cx - cc.width // 2, by - cc.height))
            return
    elif mode == "slide":
        p = ease((t - t0) / 0.8)
        off = round((1 - p) * dx)
        img.alpha_composite(c, (cx - c.width // 2 + off, by - c.height))
        return
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))


def pill(d, cx, y, text, size, fill=AMBER, col=INK):
    f = font("Bold", size)
    w = d.textlength(text, font=f) + size * 1.6
    h = size * 1.9
    d.rounded_rectangle((cx - w / 2, y, cx + w / 2, y + h), radius=h / 2, fill=fill)
    d.text((cx, y + h / 2), text, font=f, fill=col, anchor="mm")


def star(d, x, y, s, col):
    d.polygon([(x, y - s), (x + s / 4, y - s / 4), (x + s, y), (x + s / 4, y + s / 4),
               (x, y + s), (x - s / 4, y + s / 4), (x - s, y), (x - s / 4, y - s / 4)], fill=col)


def head(img, label):
    lg = logo(72)
    img.alpha_composite(lg, ((W - lg.width) // 2, 230))
    d = ImageDraw.Draw(img)
    pill(d, W / 2, 330, label, 30)


def rays_image(color, n=14):
    big = Image.new("RGBA", (2400, 2400), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = a0 + math.pi / n * 0.8
        d.polygon([(1200, 1200), (1200 + 1700 * math.cos(a0), 1200 + 1700 * math.sin(a0)),
                   (1200 + 1700 * math.cos(a1), 1200 + 1700 * math.sin(a1))], fill=color)
    return big.filter(ImageFilter.GaussianBlur(6))


def write(name, frame_fn):
    path = f"{OUT}/{name}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for f in range(n):
        ff.stdin.write(frame_fn(f / FPS).convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    # Standbild für Vorschau / Fallback
    frame_fn(DUR - 0.5).convert("RGB").save(f"{OUT}/{name}_standbild.jpg", quality=92)
    print(path)


# ---------------- Story 1: Psst … ----------------
S1_BG = gradient(W, H, (34, 30, 48), (12, 12, 14)).convert("RGBA")
S1_CAT = cat("06_detektiv", 820, 760)
S1_Q = [(170, 820, 70, 0.0), (900, 760, 90, 0.7), (880, 1240, 60, 1.4), (190, 1250, 80, 2.0)]


def story1(t):
    img = S1_BG.copy()
    # Suchscheinwerfer: wandert über die Szene und bleibt auf Timmi stehen
    p = ease(t / 2.2)
    sx = round(150 + (W / 2 - 150) * p + math.sin(t * 2.2) * 120 * (1 - p))
    sy = round(1500 - 420 * p)
    glow(img, sx, sy, 420, (255, 196, 110), 0.55)
    put_cat(img, S1_CAT, W // 2, 1480, 0.5, t, "slide", dx=-700)
    d = ImageDraw.Draw(img)
    # schwebende Fragezeichen
    for x, y, s, t0 in S1_Q:
        a = ease((t - 1.2 - t0) / 0.4)
        bob = round(math.sin(t * 2.4 + t0 * 3) * 14)
        layer(img, a, lambda dd, x=x, y=y, s=s, bob=bob: dd.text((x, y + bob), "?", font=font("Bold", s), fill=AMBER, anchor="mm"))
    head(img, "STORY 1 / 3")
    # "Psst …" erscheint Buchstabe für Buchstabe
    full = "Psst …"
    k = min(len(full), max(0, int((t - 0.3) / 0.12)))
    d = ImageDraw.Draw(img)
    if k:
        d.text((W / 2, 430), full[:k], font=font("Bold", 130), fill=WHITE, anchor="mt")
    a = ease((t - 1.3) / 0.6)
    layer(img, a, lambda dd: (dd.text((W / 2, 600), "Timmi hat heute früh", font=font("Medium", 52), fill=GREY_L, anchor="mt"),
                              dd.text((W / 2, 668), "etwas entdeckt …", font=font("Medium", 52), fill=GREY_L, anchor="mt")))
    # pulsierender Hinweis
    a = ease((t - 3.0) / 0.5) * (0.65 + 0.35 * math.sin(t * 5) ** 2)
    def tip(dd):
        dd.text((W / 2 - 20, 1525), "Tippe weiter", font=font("Bold", 46), fill=AMBER, anchor="mt")
        chevron(dd, W / 2 + 150, 1555, 30, AMBER)
    layer(img, a, tip)
    return img


# ---------------- Story 2: iPhone 18 ist da ----------------
S2_BG = gradient(W, H, (44, 38, 56), (12, 12, 14)).convert("RGBA")
S2_RAYS = rays_image((255, 190, 90, 34))
S2_CAT = cat("02_handy_neu", 900, 700)
random.seed(7)
S2_CONF = [(random.uniform(0, W), random.uniform(-H, 0), random.uniform(120, 260), random.uniform(10, 22),
            random.choice([AMBER, WHITE, (255, 120, 120), (120, 190, 255)]), random.uniform(0, 6.28)) for _ in range(70)]


def story2(t):
    img = S2_BG.copy()
    # rotierende Lichtstrahlen hinter Timmi
    a = ease((t - 0.2) / 0.6)
    if a > 0:
        r = S2_RAYS.rotate(t * 12, resample=Image.BICUBIC)
        r = r.crop((1200 - W // 2, 1200 - 1100, 1200 + W // 2, 1200 - 1100 + H))
        if a < 1:
            r.putalpha(r.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(r)
    glow(img, W // 2, 1100, 460, AMBER, 0.55)
    # Blitz beim Auftritt
    flash = max(0.0, 1 - abs(t - 0.45) / 0.25)
    if flash > 0:
        layer(img, flash * 0.8, lambda dd: dd.rectangle((0, 0, W, H), fill=WHITE))
    put_cat(img, S2_CAT, W // 2, 1500, 0.4, t, "pop")
    # Konfetti
    if t > 0.5:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for x, y0, v, s, col, ph in S2_CONF:
            y = y0 + (t - 0.5) * v * 3.2
            if 0 < y < H:
                xx = x + math.sin(t * 2 + ph) * 30
                w = s * abs(math.cos(t * 4 + ph))
                ld.rectangle((xx - w / 2, y - s / 3, xx + w / 2, y + s / 3), fill=col + (230,))
        img.alpha_composite(lay)
    head(img, "STORY 2 / 3")
    # Überschrift "schlägt ein"
    p = ease((t - 0.6) / 0.35)
    if p > 0:
        sz = round(150 - 40 * p)
        layer(img, p, lambda dd: dd.text((W / 2, 440), "Endlich da!", font=font("Bold", sz), fill=WHITE, anchor="mt"))
    a = ease((t - 1.1) / 0.5)
    layer(img, a, lambda dd: dd.text((W / 2, 575 + round(20 * (1 - a))), "das neue iPhone 18", font=font("Bold", 76), fill=AMBER, anchor="mt"))
    # drei Modelle nacheinander
    d = ImageDraw.Draw(img)
    for i, (txt, x) in enumerate((("iPhone 18", 230), ("18 Pro", 540), ("18 Pro Max", 850))):
        p = back((t - 1.7 - i * 0.3) / 0.45)
        if p > 0:
            sz = max(10, round(34 * p))
            pill(d, x, 690, txt, sz, fill=WHITE, col=INK)
    # Aufforderung unten, sanft pulsierend
    a = ease((t - 3.0) / 0.5)
    pulse = 1 + 0.04 * math.sin(t * 5)
    layer(img, a, lambda dd: pill(dd, W / 2, 1545, "Jetzt im Shop testen", round(40 * pulse)))
    return img


# ---------------- Story 3: Black Week + Besuch ----------------
S3_CAT = cat("01_winken", 640, 570)
random.seed(3)
S3_SPARK = [(random.uniform(80, W - 80), random.uniform(820, 1450), random.uniform(10, 26), random.uniform(0, 6.28)) for _ in range(14)]


def story3(t):
    img = Image.new("RGBA", (W, H), (12, 12, 14, 255))
    # laufende Diagonalstreifen
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    off = (t * 90) % 160
    for k in range(-14, 22):
        x = k * 160 + off
        ld.polygon([(x, 0), (x + 55, 0), (x + 55 - 1000, H), (x - 1000, H)], fill=(255, 255, 255, 12))
    img.alpha_composite(lay)
    glow(img, W // 2, 1150, round(470 + 40 * math.sin(t * 3)), AMBER, 0.7)
    # Timmi kommt von unten ins Bild
    if t >= 1.2:
        p = ease((t - 1.2) / 0.7)
        oy = round((1 - p) * 700)
        img.alpha_composite(S3_CAT, (W // 2 - S3_CAT.width // 2, 1490 - S3_CAT.height + oy))
    # Funkeln
    spk = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d0 = ImageDraw.Draw(spk)
    for x, y, s, ph in S3_SPARK:
        v = max(0.0, math.sin(t * 3 + ph))
        if v > 0.05 and t > 1.5:
            star(d0, x, y, s * v, (255, 255, 255, int(220 * v)))
    img.alpha_composite(spk)
    head(img, "STORY 3 / 3")
    a = ease((t - 0.2) / 0.5)
    layer(img, a, lambda dd: dd.text((W / 2, 430), "Und die", font=font("Bold", 72), fill=WHITE, anchor="mt"))
    # BLACK von links, WEEK von rechts
    p = ease((t - 0.4) / 0.6)
    d = ImageDraw.Draw(img)
    if p > 0:
        f = font("Bold", 150)
        d.text((W / 2 - round((1 - p) * 1100), 515), "BLACK", font=f, fill=WHITE, anchor="mt")
    p2 = ease((t - 0.6) / 0.6)
    if p2 > 0:
        f = font("Bold", 150)
        d.text((W / 2 + round((1 - p2) * 1100), 665), "WEEK", font=f, fill=AMBER, anchor="mt")
    a = ease((t - 1.4) / 0.5)
    layer(img, a, lambda dd: dd.text((W / 2, 830), "kommt bald!", font=font("Bold", 64), fill=WHITE, anchor="mt"))
    a = ease((t - 2.4) / 0.5)
    pulse = 1 + 0.035 * math.sin(t * 5)

    def cta(dd):
        pill(dd, W / 2, 1515, "Komm vorbei – Timmi wartet!", round(40 * pulse))
        dd.text((W / 2, 1625), "Poststraße 34 · Mo–Fr 9–17 Uhr", font=font("Bold", 38), fill=WHITE, anchor="mt")
    layer(img, a, cta)
    return img


if __name__ == "__main__":
    import sys
    os.makedirs(OUT, exist_ok=True)
    todo = sys.argv[1:] or ["1", "2", "3"]
    if "1" in todo: write("story_1_psst", story1)
    if "2" in todo: write("story_2_iphone18", story2)
    if "3" in todo: write("story_3_blackweek", story3)
