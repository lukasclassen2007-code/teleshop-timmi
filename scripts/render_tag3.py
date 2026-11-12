"""Karussell 12.11. (neu): Themen-Cover, Erstes Handy, Throwback-Fun-Fact, MagentaTV, Tipp älteres Smartphone.
Aufruf: python3 render_tag3.py tag.json ausgabeordner
"""
import json, os, sys
import render_post as rp
import render_tag as rt
import render_tag2 as r2
from PIL import ImageDraw
from timmi_lib import font, WHITE
from render_tag3_story import flip_phone, slide_phone, antenna_phone


def erstes_handy(c):
    img = r2.slide_cover(c).convert("RGBA")
    d = ImageDraw.Draw(img)
    S, y = 265, 840
    for i, (cx, lab) in enumerate(((125, "Klapphandy"), (315, "Schiebehandy"), (505, "Klassiker"))):
        x = cx - 0.42 * S / 2
        if i == 0:
            flip_phone(d, x, y, S * 0.78)
        elif i == 1:
            slide_phone(d, x, y, S, 0.0)
        else:
            antenna_phone(d, x, y + 40, S * 0.86)
        d.text((cx, y + S + 16), lab, font=font("Bold", 24), fill=WHITE, anchor="mt")
    return img.convert("RGB")

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    erstes_handy(data["erstes"]).save(f"{out}/2_erstes_handy.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="03_idee", kicker="THROWBACK THURSDAY").save(f"{out}/3_funfact.jpg", quality=92)
    rt.slide_topic(data["magenta"]).save(f"{out}/4_magentatv.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    print("ok")
