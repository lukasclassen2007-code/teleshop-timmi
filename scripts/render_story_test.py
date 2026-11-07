"""Story-Bild (1080x1920) für den Test: Moin Timmi + Fun-Fact + Countdown-Termin + Shop-Handle."""
import json
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, shadow, draw_deco, THEMES, INK, AMBER, WHITE, GREY

W, H = 1080, 1920
p = json.load(open("woche_2026-11-09.json", encoding="utf-8"))[0]

img = gradient(W, H, *THEMES["intro"]).convert("RGBA")
glow(img, W // 2, 820, 400, (255, 255, 255), 0.6)
draw_deco(img, "intro", (0, 540, W, 1110))
c = cat("01_winken", 600, 530)
by = 1090
shadow(img, W // 2, by, c.width * 0.7)
img.alpha_composite(c, (W // 2 - c.width // 2, by - c.height))
d = ImageDraw.Draw(img)

lg = logo(72)
img.alpha_composite(lg, ((W - lg.width) // 2, 250))
kf = font("Bold", 32)
kt = "BALD IN TIMMENDORF"
kw = d.textlength(kt, font=kf)
d.rounded_rectangle(((W - kw) / 2 - 28, 350, (W + kw) / 2 + 28, 408), radius=29, fill=AMBER)
d.text((W / 2, 379), kt, font=kf, fill=INK, anchor="mm")
d.text((W / 2, 430), "Moin, ich bin Timmi!", font=fit(d, "Moin, ich bin Timmi!", "Bold", 96, W - 80), fill=INK, anchor="mt")

# Fun-Fact-Karte
x0, y0, x1 = 60, 1120, W - 60
tf = font("Medium", 38)
lines = wrap(d, p["funfact"]["text"], tf, x1 - x0 - 80)
y1 = y0 + 110 + len(lines) * 52 + 30
d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=(20, 20, 22))
d.rounded_rectangle((x0 + 40, y0 + 34, x0 + 40 + d.textlength("TIMMIS FUN-FACT", font=font("Bold", 26)) + 40, y0 + 82), radius=24, fill=AMBER)
d.text((x0 + 60, y0 + 58), "TIMMIS FUN-FACT", font=font("Bold", 26), fill=INK, anchor="lm")
y = y0 + 110
for ln in lines:
    d.text((x0 + 40, y), ln, font=tf, fill=WHITE)
    y += 52

# Öffnungszeiten
y = y1 + 30
d.text((W / 2, y), "ÖFFNUNGSZEITEN · POSTSTRASSE 34", font=font("Bold", 30), fill=INK, anchor="mt")
d.text((W / 2, y + 44), "Mo–Fr 9–17 Uhr", font=font("Bold", 62), fill=INK, anchor="mt")

# Shop-Handle
h = "@teleshop_timmendorfer_strand"
hf = font("Bold", 40)
hw = d.textlength(h, font=hf)
yh = y + 128
d.rounded_rectangle(((W - hw) / 2 - 36, yh, (W + hw) / 2 + 36, yh + 78), radius=39, fill=INK)
d.text((W / 2, yh + 39), h, font=hf, fill=AMBER, anchor="mm")
print("Unterkante Inhalt:", yh + 78)
img.convert("RGB").save("test/timmi_test_story.jpg", "JPEG", quality=92)
