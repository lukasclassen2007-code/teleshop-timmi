"""Setzt einen Display-Inhalt perspektivisch auf Timmis Handy (Pose 02_handy) und stellt frei.
Aufruf: python3 make_phone_screen.py  -> raw/ und cut/timmi_02_handy_neu.*
"""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/truetype/google-fonts/Poppins-{}.ttf"
SW, SH = 600, 1240
QUAD = np.float32([[223, 368], [354, 352], [399, 633], [271, 652]])


def screen_new_iphone():
    g = Image.new("RGB", (1, 256))
    for y in range(256):
        a = y / 255
        g.putpixel((0, y), (int(30 + 40 * a), int(30 + 20 * a), int(40 + 10 * a)))
    scr = g.resize((SW, SH))
    gl = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(gl).ellipse((60, 260, 540, 760), fill=140)
    scr = Image.composite(Image.new("RGB", (SW, SH), (255, 166, 43)), scr, gl.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(scr)
    d.text((SW / 2, 380), "NEU", font=ImageFont.truetype(F.format("Bold"), 70), fill=(255, 255, 255), anchor="mm")
    d.text((SW / 2, 530), "iPhone 18", font=ImageFont.truetype(F.format("Bold"), 100), fill=(255, 255, 255), anchor="mm")
    f = ImageFont.truetype(F.format("Bold"), 54)
    for i, t in enumerate(("18", "18 Pro", "18 Pro Max")):
        y = 660 + i * 92
        w = d.textlength(t, font=f) + 60
        d.rounded_rectangle((SW / 2 - w / 2, y, SW / 2 + w / 2, y + 74), radius=37, outline=(255, 255, 255), width=4)
        d.text((SW / 2, y + 37), t, font=f, fill=(255, 255, 255), anchor="mm")
    d.rounded_rectangle((90, 980, SW - 90, 1090), radius=55, fill=(255, 166, 43))
    d.text((SW / 2, 1035), "JETZT DA", font=ImageFont.truetype(F.format("Bold"), 58), fill=(17, 17, 17), anchor="mm")
    return scr


def apply(scr, out_stem):
    src = Image.open("raw/timmi_02_handy.jpg").convert("RGB")
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [SW, 0], [SW, SH], [0, SH]]), QUAD)
    warp = cv2.warpPerspective(np.array(scr), M, (1024, 1024), flags=cv2.INTER_AREA)
    inside = cv2.warpPerspective(np.full((SH, SW), 255, np.uint8), M, (1024, 1024))
    base = np.array(src).astype(np.float32)
    lum = base.mean(axis=2)
    m = ((inside > 128) & (lum < 185)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m, (5, 5), 0).astype(np.float32) / 255
    out = (base * (1 - m[..., None]) + warp.astype(np.float32) * m[..., None]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out).save(f"raw/{out_stem}.jpg", quality=95)
    from rembg import remove, new_session
    o = remove(Image.fromarray(out), session=new_session("isnet-general-use"), post_process_mask=True)
    o.crop(o.getbbox()).save(f"cut/{out_stem}.png")
    Image.fromarray(out).crop((150, 280, 520, 720)).save("chk_screen.png")


if __name__ == "__main__":
    apply(screen_new_iphone(), "timmi_02_handy_neu")
    print("ok")
