"""Rendert den TV-Clip (1080x1920, Hochformat, ohne Ton) aus einer Szenen-JSON.
Ruckelfrei: Die Katze wird in Endgröße einmal skaliert und danach nur pixelgenau gesetzt.
Bewegung entsteht durch Deko (weich gezeichnet), Text-Einblendungen und Schiebe-Übergänge.
Aufruf: python3 render_tv.py szenen.json ausgabe.mp4
"""
import json, math, sys, subprocess
from PIL import Image, ImageDraw
from timmi_lib import (font, fit, wrap, gradient, glow, logo, cat, shadow, draw_deco,
                       THEMES, INK, AMBER, WHITE, GREY, HOURS, ADDRESS)

W, H, FPS = 1080, 1920, 30
SCENE, TRANS = 5.0, 0.5
FOOT = 290
INSTA = "teleshop_timmendorfer_strand"
INSTA_URL = f"https://www.instagram.com/{INSTA}/"
GOOGLE_REVIEW_URL = "https://search.google.com/local/writereview?placeid=ChIJ0xOCWDh1skcRKqzjS1E7uy0"
QR_SCENES = ("insta", "google")
STAGE = (0, 660, W, H - FOOT)
LAYOUT = {"center": (0.5, 980), "left": (0.38, 960), "right": (0.62, 960), "close": (0.5, 1060)}


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def back(x):
    x = max(0.0, min(1.0, x))
    c = 1.4
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def fade_layer(img, alpha, fn):
    if alpha <= 0:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(lay))
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay)


class Scene:
    def __init__(self, sc):
        self.sc = sc
        self.dur = sc.get("dur", SCENE)
        if sc["type"] == "funfact":
            self.bg = Image.new("RGBA", (W, H), (20, 20, 22, 255))
            glow(self.bg, 760, 1450, 470, tuple(sc.get("glow", AMBER)), 0.85)
            self.cx, self.by = 760, H - FOOT - 30
            # Katze nur so groß, dass sie den Text nicht verdeckt
            dd = ImageDraw.Draw(Image.new("RGB", (10, 10)))
            bf = fit(dd, sc["big"], "Bold", 260, W - 120, minsize=120)
            n_lines = len(wrap(dd, sc["text"], font("Medium", 58), W - 130))
            text_bottom = 470 + bf.size + 50 + n_lines * 76
            self.cat = cat(sc["pose"], 640, min(760, self.by - text_bottom - 20))
        elif sc["type"] in QR_SCENES:
            top, bottom = ((250, 222, 255), (255, 176, 150)) if sc["type"] == "insta" else ((255, 244, 214), (255, 196, 92))
            self.bg = gradient(W, H, top, bottom).convert("RGBA")
            glow(self.bg, 300, 1300, 380, (255, 255, 255), 0.55)
            glow(self.bg, 770, 1000, 380, (255, 255, 255), 0.45)
            self.cat = cat(sc["pose"], 470, 760)
            self.cx, self.by = 270, H - FOOT - 40
            shadow(self.bg, self.cx, self.by, self.cat.width * 0.75)
            self.qr = qr_image(INSTA_URL if sc["type"] == "insta" else GOOGLE_REVIEW_URL, 470)
        else:
            self.bg = gradient(W, H, *THEMES[sc["theme"]]).convert("RGBA")
            fx, mh = LAYOUT[sc.get("layout", "center")]
            glow(self.bg, int(W * fx), 1250, 520, (255, 255, 255), 0.6)
            self.cat = cat(sc["pose"], 1000, mh)
            self.cx, self.by = int(W * fx), H - FOOT - (10 if sc.get("layout") == "close" else 40)
            shadow(self.bg, self.cx, self.by, self.cat.width * 0.7)

    def frame(self, t):
        sc, img = self.sc, self.bg.copy()
        if sc["type"] == "scene":
            draw_deco(img, sc["theme"], STAGE, t, animate=True)
        if sc["type"] in QR_SCENES:
            self.qr_card(img, t)
        # Katze: kurzes Hineinfedern, danach pixelgenau und scharf
        p = back((t - 0.15) / 0.55)
        if p >= 0.999:
            c = self.cat
        else:
            s = 0.75 + 0.25 * p
            c = self.cat.resize((max(1, round(self.cat.width * s)), max(1, round(self.cat.height * s))), Image.BICUBIC)
            a = ease((t - 0.15) / 0.25)
            c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
        if t > 0.15:
            img.alpha_composite(c, (self.cx - c.width // 2, self.by - c.height))
        d = ImageDraw.Draw(img)
        if sc["type"] == "funfact":
            self.fact_text(img, d, t)
        else:
            self.head_text(img, d, t)
        if sc["type"] in QR_SCENES:
            self.qr_extras(img, t)
        return img

    # ---------- QR-Szenen ----------
    CARD = (540, 690, 1040, 1350)  # x0, y0, x1, y1

    def qr_card(self, img, t):
        x0, y0, x1, y1 = self.CARD
        a = ease((t - 0.3) / 0.6)
        dy = round(60 * (1 - a))

        def card(dd):
            dd.rounded_rectangle((x0 + 6, y0 + 14 + dy, x1 + 6, y1 + 14 + dy), radius=44, fill=(0, 0, 0, 40))
            dd.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=44, fill=WHITE)
        fade_layer(img, a, card)
        if a >= 0.999:
            # QR erst einsetzen, wenn die Karte steht: dann pixelgenau und gut scannbar
            img.alpha_composite(self.qr, ((x0 + x1) // 2 - self.qr.width // 2, y0 + 40))
        elif a > 0:
            q = self.qr.copy()
            q.putalpha(q.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(q, ((x0 + x1) // 2 - q.width // 2, y0 + 40 + dy))
        d = ImageDraw.Draw(img)
        label = "@" + INSTA if self.sc["type"] == "insta" else "Bewertung abgeben"
        lf = fit(d, label, "Bold", 38, x1 - x0 - 50, 24)
        fade_layer(img, a, lambda dd: dd.text(((x0 + x1) / 2, y0 + 40 + self.qr.height + 52 + dy), label, font=lf, fill=INK, anchor="mm"))
        sub = "Tipps & Fun-Facts jeden Tag" if self.sc["type"] == "insta" else "auf Google · dauert 1 Minute"
        sf = fit(d, sub, "Medium", 30, x1 - x0 - 50, 20)
        fade_layer(img, a, lambda dd: dd.text(((x0 + x1) / 2, y0 + 40 + self.qr.height + 100 + dy), sub, font=sf, fill=GREY, anchor="mm"))

    def qr_extras(self, img, t):
        x0, y0, x1, y1 = self.CARD
        if self.sc["type"] == "google":
            # fünf Sterne, nacheinander aufploppend
            lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
            dd = ImageDraw.Draw(lay)
            for k in range(5):
                p = back((t - 1.0 - k * 0.15) / 0.4)
                if p <= 0:
                    continue
                r = 46 * p * 2
                cx, cy = (x0 + 50 + k * 100) * 2, (y0 - 70) * 2
                pts = []
                for j in range(10):
                    ang = -math.pi / 2 + j * math.pi / 5
                    rr = r if j % 2 == 0 else r * 0.45
                    pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
                dd.polygon(pts, fill=AMBER + (255,), outline=INK + (255,), width=4)
            img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
        # "Scan mich!"-Pille, sanft wippend
        a = ease((t - 1.2) / 0.5)
        bob = round(math.sin(t * 3.0) * 8)
        pf = font("Bold", 40)
        txt = "Scan mich!"
        tw = ImageDraw.Draw(img).textlength(txt, font=pf)
        px, py = (x0 + x1) / 2, y1 + 70 + bob

        def pill(dd):
            dd.rounded_rectangle((px - tw / 2 - 40, py - 38, px + tw / 2 + 40, py + 38), radius=38, fill=INK)
            dd.polygon([(px - 18, py - 36), (px + 18, py - 36), (px, py - 62)], fill=INK)
            dd.text((px, py), txt, font=pf, fill=AMBER, anchor="mm")
        fade_layer(img, a, pill)

    def head_text(self, img, d, t):
        sc = self.sc
        a = ease((t - 0.1) / 0.5)
        kf = font("Bold", 36)
        kw = d.textlength(sc["kicker"], font=kf)
        ky = 250 + round(24 * (1 - a))

        def kick(dd):
            x0 = (W - kw - 56) / 2
            dd.rounded_rectangle((x0, ky, x0 + kw + 56, ky + 66), radius=33, fill=AMBER)
            dd.text((W / 2, ky + 33), sc["kicker"], font=kf, fill=INK, anchor="mm")
        fade_layer(img, a, kick)

        hf = font("Bold", 104)
        lines = wrap(d, sc["headline"], hf, W - 90)
        if len(lines) > 1:
            hf = fit(d, sc["headline"], "Bold", 104, W - 90, minsize=80)
            lines = wrap(d, sc["headline"], hf, W - 90)
        a = ease((t - 0.35) / 0.55)
        hy = 360 + round(36 * (1 - a))

        def head(dd):
            for i, ln in enumerate(lines):
                dd.text((W / 2, hy + i * (hf.size + 8)), ln, font=hf, fill=INK, anchor="mt")
        fade_layer(img, a, head)

        a = ease((t - 0.75) / 0.55)
        sf = fit(d, sc["sub"], "Medium", 52, W - 90, minsize=36)
        sy = 360 + len(lines) * (hf.size + 8) + 28 + round(24 * (1 - a))
        fade_layer(img, a, lambda dd: dd.text((W / 2, sy), sc["sub"], font=sf, fill=GREY, anchor="mt"))

    def fact_text(self, img, d, t):
        sc = self.sc
        a = ease((t - 0.1) / 0.5)

        def kick(dd):
            kf = font("Bold", 36)
            kw = dd.textlength("TIMMIS FUN-FACT", font=kf)
            dd.rounded_rectangle((60, 250, 60 + kw + 56, 316), radius=33, fill=AMBER)
            dd.text((88, 283), "TIMMIS FUN-FACT", font=kf, fill=INK, anchor="lm")
            dd.text((58, 350), "Wusstest du?", font=font("Bold", 88), fill=WHITE)
        fade_layer(img, a, kick)
        a = ease((t - 0.4) / 0.5)
        bf = fit(d, sc["big"], "Bold", 260, W - 120, minsize=120)
        by = 470 + round(30 * (1 - a))
        fade_layer(img, a, lambda dd: dd.text((50, by), sc["big"], font=bf, fill=AMBER))
        tf = font("Medium", 58)
        y0 = 470 + bf.size + 50
        for i, ln in enumerate(wrap(d, sc["text"], tf, W - 130)):
            a = ease((t - 0.9 - i * 0.2) / 0.45)
            yy = y0 + i * 76 + round(16 * (1 - a))
            fade_layer(img, a, lambda dd, ln=ln, yy=yy: dd.text((60, yy), ln, font=tf, fill=WHITE))


_qr = {}


def qr_image(url, size):
    """QR-Code mit ganzzahliger Modulgröße (scharf, gut scannbar)."""
    key = (url, size)
    if key not in _qr:
        import qrcode
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=2, box_size=1)
        q.add_data(url)
        q.make(fit=True)
        n = q.modules_count + 4
        q.box_size = max(1, size // n)
        _qr[key] = q.make_image(fill_color="black", back_color="white").convert("RGBA")
    return _qr[key]


def chrome(img, qr_alpha=1.0):
    """Feste Elemente über allem: Logo und Fußleiste mit QR-Code zu Instagram (in QR-Szenen ausgeblendet)."""
    lg = logo(88)
    img.alpha_composite(lg, ((W - lg.width) // 2, 90))
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - FOOT, W, H), fill=INK)
    q = qr_image(INSTA_URL, 240)
    qs = q.width
    qx, qy = W - 50 - qs, H - FOOT + (FOOT - qs) // 2
    if qr_alpha > 0:
        def small(dd):
            dd.rounded_rectangle((qx - 10, qy - 10, qx + qs + 10, qy + qs + 10), radius=18, fill=WHITE)
        fade_layer(img, qr_alpha, small)
        if qr_alpha >= 0.999:
            img.alpha_composite(q, (qx, qy))
        else:
            qq = q.copy()
            qq.putalpha(qq.getchannel("A").point(lambda v: int(v * qr_alpha)))
            img.alpha_composite(qq, (qx, qy))
        d = ImageDraw.Draw(img)
    x = 56
    d.text((x, H - FOOT + 46), "Folge Timmi auf Instagram", font=font("Bold", 34), fill=AMBER)
    d.text((x, H - FOOT + 92), "@" + INSTA, font=fit(d, "@" + INSTA, "Medium", 30, qx - x - 30, 22), fill=WHITE)
    d.line((x, H - FOOT + 150, qx - 40, H - FOOT + 150), fill=(60, 60, 60), width=2)
    d.text((x, H - FOOT + 168), f"{ADDRESS} · Timmendorfer Strand", font=fit(d, f"{ADDRESS} · Timmendorfer Strand", "Bold", 30, qx - x - 30, 22), fill=WHITE)
    d.text((x, H - FOOT + 212), HOURS, font=font("Bold", 34), fill=AMBER)


def main(spec, out):
    scenes = [Scene(s) for s in json.load(open(spec, encoding="utf-8"))]
    n_sc = len(scenes)
    starts = [0.0]
    for sc in scenes:
        starts.append(starts[-1] + sc.dur)
    total = starts[-1]
    n = int(round(total * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    small_qr = lambda k: 0.0 if scenes[k % n_sc].sc["type"] in QR_SCENES else 1.0
    for f in range(n):
        T = f / FPS
        i = max(k for k in range(n_sc) if starts[k] <= T)
        t = T - starts[i]
        dur = scenes[i].dur
        cur = scenes[i].frame(t)
        qa = small_qr(i)
        if t > dur - TRANS:
            # Schiebe-Übergang: nächste Szene schiebt die aktuelle nach links raus (letzte -> erste = Loop)
            nxt = scenes[(i + 1) % n_sc].frame(0.0)
            p = ease((t - (dur - TRANS)) / TRANS)
            x = round(W * p)
            canvas = Image.new("RGBA", (W, H))
            canvas.alpha_composite(cur, (-x, 0))
            canvas.alpha_composite(nxt, (W - x, 0))
            cur = canvas
            qa = qa * (1 - p) + small_qr(i + 1) * p
        chrome(cur, qa)
        ff.stdin.write(cur.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
