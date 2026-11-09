"""Shop-Start-Post (Karussell, 3 Bilder 1080x1350) + Story-Reihe (3 Bilder 1080x1920) für den 9.11.2026."""
import os
from PIL import Image, ImageDraw
from timmi_lib import (font, fit, wrap, gradient, glow, logo, cat, shadow, draw_deco,
                       INK, AMBER, WHITE, GREY, HOURS, ADDRESS)
import render_post as rp

OUT = "launch_2026-11-09"
os.makedirs(OUT, exist_ok=True)
W, H, FOOT = 1080, 1350, 72
BLACK = (14, 14, 16)


def pill(d, x, y, text, size=24, fill=AMBER, col=INK, center=False):
    f = font("Bold", size)
    w = d.textlength(text, font=f) + size * 1.5
    h = size * 1.85
    if center:
        x = x - w / 2
    d.rounded_rectangle((x, y, x + w, y + h), radius=h / 2, fill=fill)
    d.text((x + w / 2, y + h / 2), text, font=f, fill=col, anchor="mm")
    return w


def sparkles(img, pts, col=(255, 255, 255)):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x, y, s in pts:
        d.polygon([(x, y - s), (x + s / 4, y - s / 4), (x + s, y), (x + s / 4, y + s / 4),
                   (x, y + s), (x - s / 4, y + s / 4), (x - s, y), (x - s / 4, y - s / 4)], fill=col + (230,))
    img.alpha_composite(lay)


# ---------------- POST ----------------

def post_iphone():
    img = gradient(W, H, (40, 36, 52), (14, 14, 16)).convert("RGBA")
    glow(img, W // 2, 900, 460, AMBER, 0.55)
    sparkles(img, [(150, 560, 26), (930, 520, 20), (880, 860, 30), (190, 980, 18)])
    c = cat("02_handy_neu", 860, 780)
    cx, by = W // 2, H - FOOT - 20
    shadow(img, cx, by, c.width * 0.7)
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, "NEU IM SHOP")
    d.text((46, 176), "Endlich da:", font=font("Bold", 76), fill=WHITE)
    d.text((46, 262), "das neue iPhone 18", font=font("Bold", 76), fill=AMBER)
    x = 48
    for t in ("iPhone 18", "18 Pro", "18 Pro Max"):
        x += pill(d, x, 368, t, 26, fill=(255, 255, 255), col=INK) + 14
    rp.draw_hint(d)
    rp.footer(d)
    return img.convert("RGB")


def post_blackweek():
    img = Image.new("RGBA", (W, H), BLACK + (255,))
    glow(img, 760, 1000, 420, AMBER, 0.75)
    d = ImageDraw.Draw(img)
    # Streifen-Muster im Hintergrund
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for k in range(-10, 20):
        x = k * 120
        ld.polygon([(x, 0), (x + 40, 0), (x + 40 - 700, H), (x - 700, H)], fill=(255, 255, 255, 10))
    img.alpha_composite(lay)
    c = cat("06_detektiv", 520, 640)
    cx, by = 820, H - FOOT - 20
    img.alpha_composite(c, (cx - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, "BALD GEHT'S LOS")
    d.text((40, 170), "BLACK", font=font("Bold", 170), fill=WHITE)
    d.text((40, 340), "WEEK", font=font("Bold", 170), fill=AMBER)
    tf = font("Medium", 38)
    y = 560
    for ln in ["Timmi ist schon auf", "Spurensuche nach den", "besten Angeboten."]:
        d.text((48, y), ln, font=tf, fill=WHITE)
        y += 52
    y += 24
    d.text((48, y), "Komm vorbei –", font=font("Bold", 40), fill=AMBER)
    d.text((48, y + 52), "wir halten dich", font=font("Bold", 40), fill=AMBER)
    d.text((48, y + 104), "auf dem Laufenden!", font=font("Bold", 40), fill=AMBER)
    rp.footer(d)
    return img.convert("RGB")


def post_funfact():
    p = {"funfact": {"big": "9.11.2007",
                     "text": "Heute vor genau 19 Jahren kam das erste iPhone nach Deutschland – damals exklusiv bei T-Mobile."}}
    return rp.slide_fact(p)


# ---------------- STORYS ----------------
SW, SH = 1080, 1920


def story_base(top, bottom):
    img = gradient(SW, SH, top, bottom).convert("RGBA")
    return img


def story_footer(d, text="Poststraße 34 · Mo–Fr 9–17 Uhr"):
    # unterhalb der Story-Antwortleiste frei lassen: Inhalt endet bei ~1650
    f = font("Bold", 36)
    w = d.textlength(text, font=f)
    d.rounded_rectangle(((SW - w) / 2 - 36, 1560, (SW + w) / 2 + 36, 1636), radius=38, fill=INK)
    d.text((SW / 2, 1598), text, font=f, fill=AMBER, anchor="mm")


def story_1():
    img = story_base((30, 28, 40), (14, 14, 16))
    glow(img, SW // 2, 1050, 480, AMBER, 0.5)
    sparkles(img, [(160, 760, 30), (930, 820, 24), (880, 1280, 34)])
    c = cat("06_detektiv", 820, 780)
    by = 1470
    shadow(img, SW // 2, by, c.width * 0.6)
    img.alpha_composite(c, (SW // 2 - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    lg = logo(72)
    img.alpha_composite(lg, ((SW - lg.width) // 2, 230))
    pill(d, SW / 2, 340, "STORY 1 / 3", 30, center=True)
    d.text((SW / 2, 430), "Psst …", font=font("Bold", 120), fill=WHITE, anchor="mt")
    d.text((SW / 2, 580), "Timmi hat heute früh", font=font("Medium", 50), fill=(220, 220, 220), anchor="mt")
    d.text((SW / 2, 645), "etwas entdeckt …", font=font("Medium", 50), fill=(220, 220, 220), anchor="mt")
    d.text((SW / 2, 1520), "Tippe weiter", font=font("Bold", 44), fill=AMBER, anchor="mt")
    from timmi_lib import chevron
    chevron(d, SW / 2 + 160, 1550, 30, AMBER)
    return img.convert("RGB")


def story_2():
    img = story_base((40, 36, 52), (14, 14, 16))
    glow(img, SW // 2, 1050, 520, AMBER, 0.6)
    sparkles(img, [(140, 820, 34), (950, 760, 26), (920, 1300, 30), (150, 1250, 22)])
    c = cat("02_handy_neu", 960, 800)
    by = 1520
    shadow(img, SW // 2, by, c.width * 0.6)
    img.alpha_composite(c, (SW // 2 - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    lg = logo(72)
    img.alpha_composite(lg, ((SW - lg.width) // 2, 230))
    pill(d, SW / 2, 340, "STORY 2 / 3", 30, center=True)
    d.text((SW / 2, 430), "Endlich da!", font=font("Bold", 110), fill=WHITE, anchor="mt")
    d.text((SW / 2, 560), "iPhone 18 Pro", font=font("Bold", 92), fill=AMBER, anchor="mt")
    story_footer(d, "Jetzt im Shop ansehen & testen")
    return img.convert("RGB")


def story_3():
    img = Image.new("RGBA", (SW, SH), BLACK + (255,))
    glow(img, SW // 2, 1150, 500, AMBER, 0.7)
    c = cat("01_winken", 700, 700)
    by = 1500
    shadow(img, SW // 2, by, c.width * 0.6)
    img.alpha_composite(c, (SW // 2 - c.width // 2, by - c.height))
    d = ImageDraw.Draw(img)
    lg = logo(72)
    img.alpha_composite(lg, ((SW - lg.width) // 2, 230))
    pill(d, SW / 2, 340, "STORY 3 / 3", 30, center=True)
    d.text((SW / 2, 420), "Und die", font=font("Bold", 70), fill=WHITE, anchor="mt")
    d.text((SW / 2, 500), "BLACK WEEK", font=font("Bold", 130), fill=AMBER, anchor="mt")
    d.text((SW / 2, 650), "kommt auch bald!", font=font("Bold", 70), fill=WHITE, anchor="mt")
    d.text((SW / 2, 760), "Komm vorbei – Timmi wartet!", font=font("Medium", 46), fill=(220, 220, 220), anchor="mt")
    story_footer(d)
    return img.convert("RGB")


if __name__ == "__main__":
    post_iphone().save(f"{OUT}/post_1_iphone18.jpg", quality=92)
    post_blackweek().save(f"{OUT}/post_2_blackweek.jpg", quality=92)
    post_funfact().save(f"{OUT}/post_3_funfact.jpg", quality=92)
    story_1().save(f"{OUT}/story_1_psst.jpg", quality=92)
    story_2().save(f"{OUT}/story_2_iphone18pro.jpg", quality=92)
    story_3().save(f"{OUT}/story_3_blackweek.jpg", quality=92)
    print("ok")
