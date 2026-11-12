"""Karussell 12.11. (neu): Themen-Cover, Erstes Handy, Throwback-Fun-Fact, MagentaTV, Tipp älteres Smartphone.
Aufruf: python3 render_tag3.py tag.json ausgabeordner
"""
import json, os, sys
import render_post as rp
import render_tag as rt
import render_tag2 as r2

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    r2.slide_cover(data["erstes"]).save(f"{out}/2_erstes_handy.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="03_idee", kicker="THROWBACK THURSDAY").save(f"{out}/3_funfact.jpg", quality=92)
    rt.slide_topic(data["magenta"]).save(f"{out}/4_magentatv.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/5_tipp.jpg", quality=92)
    print("ok")
