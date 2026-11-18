"""Karussell 18.11.: Themen, KI Vor-/Nachteile, Tipp KI-Betrug, Fun-Fact KI, Black Week, GTA VI."""
import json, os, sys
from PIL import Image, ImageDraw
from timmi_lib import font, fit, wrap, gradient, glow, logo, cat, INK, AMBER, WHITE
import render_post as rp
import render_tag as rt
import render_tag2 as r2
from render_tarife import pill, W, H, FOOT

GREEN, RED = (40, 160, 80), (210, 50, 50)


def slide_ki(k):
    img = gradient(W, H, (226, 244, 250), (110, 190, 220)).convert("RGBA")
    glow(img, 540, 1050, 420, (255, 255, 255), 0.5)
    d = ImageDraw.Draw(img)
    img.alpha_composite(logo(54), (48, 40))
    pill(d, 48, 118, k["kicker"])
    d.text((46, 176), k["headline"], font=font("Bold", 84), fill=INK)
    y = 290
    for ln in wrap(d, k["sub"], font("Medium", 34), W - 100):
        d.text((48, y), ln, font=font("Medium", 34), fill=(40, 50, 60))
        y += 46
    y += 24
    cw = (W - 48 * 2 - 24) // 2
    tops = []
    for i, (title, items, col, sym) in enumerate((("Vorteile", k["pro"], GREEN, "+"), ("Risiken", k["contra"], RED, "!"))):
        x0 = 48 + i * (cw + 24)
        yy = y + 100
        lines_all = [wrap(d, it, font("Bold", 29), cw - 110) for it in items]
        hgt = 100 + sum(40 * len(l) + 26 for l in lines_all) + 20
        tops.append(hgt)
    hmax = max(tops)
    for i, (title, items, col, sym) in enumerate((("Vorteile", k["pro"], GREEN, "+"), ("Risiken", k["contra"], RED, "!"))):
        x0 = 48 + i * (cw + 24)
        d.rounded_rectangle((x0, y, x0 + cw, y + hmax), radius=30, fill=WHITE)
        d.rounded_rectangle((x0, y, x0 + cw, y + 80), radius=30, fill=col)
        d.rectangle((x0, y + 50, x0 + cw, y + 80), fill=col)
        d.text((x0 + cw / 2, y + 40), title, font=font("Bold", 42), fill=WHITE, anchor="mm")
        yy = y + 108
        for it in items:
            d.ellipse((x0 + 26, yy, x0 + 66, yy + 40), fill=col)
            d.text((x0 + 46, yy + 20), sym, font=font("Bold", 30), fill=WHITE, anchor="mm")
            for ln in wrap(d, it, font("Bold", 29), cw - 110):
                d.text((x0 + 84, yy + 2), ln, font=font("Bold", 29), fill=INK)
                yy += 40
            yy += 26
    y += hmax + 30
    rt_cta = "Fragen zu KI im Handy? Komm vorbei!"
    from render_tarife import cta
    cta(d, rt_cta, y)
    c = cat("03_idee", 380, H - FOOT - 20 - (y - 20))
    img.alpha_composite(c, (W - 60 - c.width, H - FOOT - 10 - c.height))
    rp.footer(ImageDraw.Draw(img))
    return img.convert("RGB")


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    slide_ki(data["ki"]).save(f"{out}/2_ki.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/3_ki_betrug.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="03_idee", kicker="TIMMIS FUN-FACT").save(f"{out}/4_funfact.jpg", quality=92)
    rt.slide_topic(data["bw"]).save(f"{out}/5_black_week.jpg", quality=92)
    rt.slide_topic(data["gta"]).save(f"{out}/6_gta.jpg", quality=92)
    print("ok")
