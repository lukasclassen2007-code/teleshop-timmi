"""Setzt eine Beispiel-Betrugs-SMS perspektivisch auf das leere Display von timmi_02_handy."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/truetype/google-fonts/Poppins-{}.ttf"
src = Image.open("raw/timmi_02_handy.jpg").convert("RGB")
SW, SH = 600, 1240  # Displayinhalt in hoher Auflösung

scr = Image.new("RGB", (SW, SH), (22, 22, 24))
d = ImageDraw.Draw(scr)
# Kopfzeile Nachrichten-App
d.rectangle((0, 0, SW, 230), fill=(30, 30, 32))
d.ellipse((SW / 2 - 50, 60, SW / 2 + 50, 160), fill=(110, 114, 124))
d.text((SW / 2, 195), "+49 1521 0473816", font=ImageFont.truetype(F.format("Medium"), 32), fill=(235, 235, 240), anchor="mm")
d.line((0, 230, SW, 230), fill=(60, 60, 64), width=2)
# Nachrichtenblase
bf = ImageFont.truetype(F.format("Medium"), 44)
lines = ["Ihr Paket konnte", "nicht zugestellt", "werden:"]
link = ["paket-info24.cc"]
x0, y0 = 70, 300
h = 64 * (len(lines) + len(link)) + 50
d.rounded_rectangle((x0, y0, SW - 30, y0 + h), radius=36, fill=(58, 58, 62))
y = y0 + 25
for t in lines:
    d.text((x0 + 30, y), t, font=bf, fill=(245, 245, 247)); y += 64
for t in link:
    d.text((x0 + 30, y), t, font=bf, fill=(90, 170, 255)); y += 64
yl = y0 + 25 + 64 * len(lines)
d.line((x0 + 30, yl + 58, x0 + 30 + d.textlength(link[0], font=bf), yl + 58), fill=(90, 170, 255), width=3)
# Warnhinweis unten
d.rounded_rectangle((40, SH - 260, SW - 40, SH - 120), radius=30, fill=(255, 166, 43))
d.text((SW / 2, SH - 190), "⚠ BETRUG", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52), fill=(17, 17, 17), anchor="mm")

# Display-Ecken im Originalbild (1024x1024): oben links, oben rechts, unten rechts, unten links
quad = np.float32([[223, 368], [354, 352], [399, 633], [271, 652]])
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [SW, 0], [SW, SH], [0, SH]]), quad)
warp = cv2.warpPerspective(np.array(scr), M, (1024, 1024), flags=cv2.INTER_AREA)
inside = cv2.warpPerspective(np.full((SH, SW), 255, np.uint8), M, (1024, 1024))

base = np.array(src).astype(np.float32)
lum = base.mean(axis=2)
# nur das dunkle Display ersetzen, Pfoten (hell) bleiben vorne
m = ((inside > 128) & (lum < 125)).astype(np.uint8) * 255
m = cv2.erode(m, np.ones((3, 3), np.uint8))
m = cv2.GaussianBlur(m, (5, 5), 0).astype(np.float32) / 255.0
# Displayhelligkeit leicht reduzieren, damit es wie ein echtes Display wirkt
w = warp.astype(np.float32)
out = base * (1 - m[..., None]) + w * m[..., None]
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save("raw/timmi_02_handy_sms.jpg", quality=95)
print("ok")
