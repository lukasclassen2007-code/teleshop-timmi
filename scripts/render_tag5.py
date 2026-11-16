"""Karussell 16.11.: Themen, Fun-Fact 180 Minuten, Herbstputz, Fokus-Modus, Tipp Benachrichtigungen.
Aufruf: python3 render_tag5.py tag.json ausgabeordner
"""
import json, os, sys
import render_post as rp
import render_tag as rt
import render_tag2 as r2
from render_tag4 import slide_einsatz

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="02_handy", kicker="TIMMIS FUN-FACT").save(f"{out}/2_funfact.jpg", quality=92)
    r2.slide_tip(data["putz"]).save(f"{out}/3_herbstputz.jpg", quality=92)
    slide_einsatz(data["fokus"]).save(f"{out}/4_fokus.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    print("ok")
