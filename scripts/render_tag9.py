"""Karussell 20.11.: Themen, Wochenend-Checkliste, Fun-Fact Emoji, Tipp Serienbild."""
import json, os, sys
import render_post as rp
import render_tag as rt
import render_tag2 as r2

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rt.slide_cover(data["cover"]).save(f"{out}/1_themen.jpg", quality=92)
    r2.slide_tip(data["checkliste"]).save(f"{out}/2_wochenende.jpg", quality=92)
    rp.slide_fact({"funfact": data["funfact"]}, pose="01_winken", kicker="TIMMIS FUN-FACT").save(f"{out}/3_funfact.jpg", quality=92)
    r2.slide_tip(data["tipp"]).save(f"{out}/4_tipp.jpg", quality=92)
    print("ok")
