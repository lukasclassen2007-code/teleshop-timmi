"""Karussell 23.11.: Themen, 5 Anbieter 1 Shop, Service, Fun-Fact SIM-Karten, Tipp Vertragsende."""
import json, os, sys
from PIL import ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, INK, AMBER, WHITE
import render_post as rp
import render_tag as rt
import render_tag2 as r2
from render_tag4 import slide_einsatz
from render_tarife import pill, cta, W, H, FOOT


def slide_anbieter(a):
    img = gradient(W, H, (40, 36, 52), (14, 14, 16)).convert("RGBA")
    glow(img, 800, 1000, 440, AMBER, 0.5)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, a["kicker"])
    d.text((46, 176), a["headline"], font=font("Bold", 96), fill=WHITE)
    d.text((48, 300), a["sub"], font=font("Medium", 36), fill=(225, 225, 230))
    y = 380
    f = font("Bold", 46)
    for i, m in enumerate(a["marken"]):
        tw = d.textlength(m, font=f)
        d.rounded_rectangle((48, y, 48 + tw + 80, y + 86), radius=43, fill=WHITE)
        d.ellipse((66, y + 30, 92, y + 56), fill=AMBER)
        d.text((108, y + 43), m, font=f, fill=INK, anchor="lm")
        y += 104
    y += 16
    for ln in wrap(d, a["text"], font("Medium", 34), 600):
        d.text((48, y), ln, font=font("Medium", 34), fill=(225, 225, 230))
        y += 46
    cta(d, a["cta"], y + 24, fill=AMBER, col=INK)
    c = cat("01_winken", 420, 760)
    img.alpha_composite(c, (W - 40 - c.width, H - FOOT - 10 - c.height))
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    slide_anbieter(data["anbieter"]).save(f"{out}/2_anbieter.jpg", quality=92)
    slide_einsatz(data["service"]).save(f"{out}/3_service.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="02_handy", kicker="TIMMIS FUN-FACT").save(f"{out}/4_funfact.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    print("ok")
