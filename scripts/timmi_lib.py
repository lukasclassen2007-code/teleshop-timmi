"""Gemeinsames Design-System für Timmi-Posts und TV-Clips."""
import math, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-{}.ttf"
INK, AMBER, WHITE, GREY = (17, 17, 17), (255, 166, 43), (255, 255, 255), (60, 60, 60)
HOURS = "Mo–Fr 9–17 Uhr"
ADDRESS = "Poststraße 34"

THEMES = {
    "intro":   ((255, 236, 200), (255, 183, 77)),
    "warn":    ((255, 228, 214), (255, 150, 110)),
    "data":    ((222, 236, 255), (140, 184, 255)),
    "signal":  ((233, 226, 255), (166, 148, 255)),
    "weekend": ((255, 234, 241), (255, 168, 196)),
    "cold":    ((234, 247, 255), (160, 212, 245)),
    "wifi":    ((222, 248, 238), (128, 222, 186)),
    "cta":     ((255, 236, 200), (255, 183, 77)),
}


@lru_cache(maxsize=256)
def font(weight, size):
    return ImageFont.truetype(FONT.format(weight), size)


def fit(draw, text, weight, size, maxw, minsize=30):
    while size > minsize:
        f = font(weight, size)
        if draw.textlength(text, font=f) <= maxw:
            return f
        size -= 2
    return font(weight, minsize)


def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=f) <= maxw:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def gradient(w, h, top, bottom):
    g = Image.new("RGB", (1, 256))
    for y in range(256):
        a = y / 255
        g.putpixel((0, y), tuple(int(top[i] * (1 - a) + bottom[i] * a) for i in range(3)))
    return g.resize((w, h), Image.BICUBIC)


def glow(img, cx, cy, r, color, strength=0.55):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (int(255 * strength),))
    lay = lay.filter(ImageFilter.GaussianBlur(r * 0.45))
    img.alpha_composite(lay)


@lru_cache(maxsize=8)
def logo(height):
    lg = Image.open(os.path.join(BASE, "logo.png")).convert("RGBA")
    lg = lg.resize((int(lg.width * height / lg.height), height), Image.LANCZOS)
    mask = Image.new("L", lg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, lg.width - 1, lg.height - 1), radius=height // 4, fill=255)
    lg.putalpha(mask)
    return lg


_cat_cache = {}


def cat(pose, max_w, max_h):
    key = (pose, max_w, max_h)
    if key not in _cat_cache:
        im = Image.open(os.path.join(BASE, "cut", f"timmi_{pose}.png")).convert("RGBA")
        s = min(max_w / im.width, max_h / im.height)
        _cat_cache[key] = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return _cat_cache[key]


def shadow(img, cx, by, w):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((cx - w / 2, by - w * 0.07, cx + w / 2, by + w * 0.07), fill=(0, 0, 0, 70))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18)))


# ---------- Deko-Elemente (gezeichnet in 2x, dadurch weich und ruckelfrei) ----------

def _signal(d, cx, cy, s, col, crossed=False):
    bw = s / 6
    for i in range(4):
        h = s * (0.3 + 0.23 * i)
        x = cx - s / 2 + i * bw * 1.55
        d.rounded_rectangle((x, cy + s / 2 - h, x + bw, cy + s / 2), radius=bw / 3, fill=col)
    if crossed:
        d.line((cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6), fill=(230, 60, 60, 255), width=int(s / 9))


def _wifi(d, cx, cy, s, col):
    w = int(s / 9)
    for r in (s * 0.25, s * 0.5, s * 0.75):
        d.arc((cx - r, cy - r, cx + r, cy + r), 225, 315, fill=col, width=w)
    d.ellipse((cx - w, cy - w, cx + w, cy + w), fill=col)


def _warn(d, cx, cy, s, col):
    p = [(cx, cy - s / 2), (cx + s / 2, cy + s / 2.4), (cx - s / 2, cy + s / 2.4)]
    d.polygon(p, fill=col)
    d.rounded_rectangle((cx - s / 18, cy - s / 5, cx + s / 18, cy + s / 7), radius=s / 30, fill=INK + (255,))
    d.ellipse((cx - s / 14, cy + s / 5, cx + s / 14, cy + s / 5 + s / 7), fill=INK + (255,))


def _bubble(d, cx, cy, s, col, text=None, f=None):
    w, h = s * 1.4, s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h / 3, fill=col)
    d.polygon([(cx - w / 4, cy + h / 2 - 2), (cx - w / 2.6, cy + h * 0.85), (cx - w / 10, cy + h / 2 - 2)], fill=col)
    if text:
        d.text((cx, cy), text, font=f, fill=INK + (255,), anchor="mm")


def _battery(d, cx, cy, s, level, col):
    w, h = s * 0.55, s
    d.rounded_rectangle((cx - w / 2, cy - h / 2 + s / 10, cx + w / 2, cy + h / 2), radius=s / 10, outline=INK + (255,), width=int(s / 14))
    d.rounded_rectangle((cx - w / 6, cy - h / 2, cx + w / 6, cy - h / 2 + s / 10), radius=s / 30, fill=INK + (255,))
    inner = (h - s / 10) - s / 5
    top = cy + h / 2 - s / 10 - inner * level
    d.rounded_rectangle((cx - w / 2 + s / 10, top, cx + w / 2 - s / 10, cy + h / 2 - s / 10), radius=s / 30, fill=col)


def _snow(d, cx, cy, s, col):
    for a in range(0, 180, 60):
        r = math.radians(a)
        dx, dy = math.cos(r) * s / 2, math.sin(r) * s / 2
        d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=col, width=max(2, int(s / 10)))
    d.ellipse((cx - s / 10, cy - s / 10, cx + s / 10, cy + s / 10), fill=col)


def _heart(d, cx, cy, s, col):
    r = s / 4
    d.ellipse((cx - 2 * r, cy - 1.5 * r, cx, cy + 0.5 * r), fill=col)
    d.ellipse((cx, cy - 1.5 * r, cx + 2 * r, cy + 0.5 * r), fill=col)
    d.polygon([(cx - 1.95 * r, cy - 0.2 * r), (cx + 1.95 * r, cy - 0.2 * r), (cx, cy + 2 * r)], fill=col)


def _sparkle(d, cx, cy, s, col):
    d.polygon([(cx, cy - s / 2), (cx + s / 8, cy - s / 8), (cx + s / 2, cy), (cx + s / 8, cy + s / 8),
               (cx, cy + s / 2), (cx - s / 8, cy + s / 8), (cx - s / 2, cy), (cx - s / 8, cy - s / 8)], fill=col)


def _pill(d, cx, cy, s, col, text, f):
    w = d.textlength(text, font=f) + s
    d.rounded_rectangle((cx - w / 2, cy - s / 2, cx + w / 2, cy + s / 2), radius=s / 2, fill=col)
    d.text((cx, cy), text, font=f, fill=INK + (255,), anchor="mm")


def _waves(d, x0, x1, y, s, col, ybottom):
    for k, a in enumerate((0, 1)):
        pts = []
        for x in range(int(x0), int(x1) + 20, 20):
            pts.append((x, y + k * s * 0.9 + math.sin((x / (s * 2.2)) + k) * s * 0.25))
        pts += [(x1, ybottom), (x0, ybottom)]
        c = col[:3] + (int(col[3] * (0.6 + 0.4 * k)),)
        d.polygon(pts, fill=c)


def _bricks(d, x0, y0, x1, y1, s, col):
    row = 0
    y = y0
    while y < y1:
        off = (s / 2) if row % 2 else 0
        x = x0 - off
        while x < x1:
            d.rounded_rectangle((x + 3, y + 3, x + s - 3, y + s / 2 - 3), radius=4, fill=col)
            x += s
        y += s / 2
        row += 1


# Deko-Definition je Thema: (art, x-Anteil, y-Anteil, Größe-Anteil, Parameter)
# x/y-Anteile beziehen sich auf die Bühne (Bereich zwischen Text und Fußleiste)
DECO = {
    "intro":   [("waves", 0, 0.86, 0.05, {}), ("bubble", 0.78, 0.18, 0.13, {"text": "Moin!"}),
                ("sparkle", 0.12, 0.3, 0.05, {}), ("sparkle", 0.88, 0.48, 0.035, {})],
    "warn":    [("warn", 0.13, 0.25, 0.11, {}), ("bubble", 0.85, 0.2, 0.11, {"text": "!"}),
                ("warn", 0.88, 0.58, 0.07, {}), ("bubble", 0.1, 0.6, 0.08, {"text": "?"})],
    "data":    [("pill", 0.17, 0.2, 0.06, {"text": "Updates"}), ("pill", 0.14, 0.42, 0.06, {"text": "Backups"}),
                ("pill", 0.17, 0.64, 0.06, {"text": "Autoplay"}), ("wifi", 0.9, 0.16, 0.1, {})],
    "signal":  [("bricks", 0, 0.42, 0.12, {}), ("signal", 0.13, 0.17, 0.1, {"crossed": True}),
                ("wifi", 0.87, 0.22, 0.13, {}), ("pill", 0.83, 0.42, 0.06, {"text": "WLAN-Call"})],
    "weekend": [("heart", 0.13, 0.22, 0.08, {}), ("heart", 0.86, 0.32, 0.06, {}), ("sparkle", 0.82, 0.12, 0.05, {}),
                ("sparkle", 0.17, 0.52, 0.04, {}), ("heart", 0.9, 0.62, 0.045, {})],
    "cold":    [("snow", 0.12, 0.14, 0.07, {}), ("snow", 0.86, 0.1, 0.05, {}), ("snow", 0.93, 0.55, 0.06, {}),
                ("snow", 0.07, 0.48, 0.045, {}), ("battery", 0.84, 0.3, 0.13, {"level": 0.15})],
    "cta":     [("waves", 0, 0.86, 0.05, {}), ("pill", 0.76, 0.2, 0.065, {"text": "Handy & Tarif"}),
                ("pill", 0.8, 0.38, 0.065, {"text": "Internet"}), ("pill", 0.76, 0.56, 0.065, {"text": "Alle Netze"}),
                ("sparkle", 0.93, 0.08, 0.04, {})],
    "wifi":    [("wifi", 0.2, 0.2, 0.2, {}), ("wifi", 0.86, 0.3, 0.1, {}), ("sparkle", 0.9, 0.1, 0.04, {}),
                ("pill", 0.82, 0.55, 0.06, {"text": "frei stellen"})],
}


def draw_deco(img, theme, stage, t=0.0, animate=False):
    """Zeichnet die Deko eines Themas auf img (RGBA). stage=(x0,y0,x1,y1). t in Sekunden."""
    x0, y0, x1, y1 = stage
    sw, sh = x1 - x0, y1 - y0
    SS = 2
    lay = Image.new("RGBA", (img.width * SS, img.height * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    white = (255, 255, 255, 235)
    for n, (kind, fx, fy, fs, p) in enumerate(DECO.get(theme, [])):
        bob = math.sin(t * 1.6 + n * 1.3) * sh * 0.012 if animate else 0
        cx, cy, s = (x0 + fx * sw) * SS, (y0 + fy * sh + bob) * SS, fs * sw * SS
        if kind == "waves":
            _waves(d, x0 * SS, x1 * SS, cy, s, (255, 255, 255, 120), y1 * SS)
        elif kind == "bricks":
            _bricks(d, x0 * SS, cy, x1 * SS, y1 * SS, s, (255, 255, 255, 60))
        elif kind == "signal":
            _signal(d, cx, cy, s, white, p.get("crossed", False))
        elif kind == "wifi":
            _wifi(d, cx, cy, s, white)
        elif kind == "warn":
            _warn(d, cx, cy, s, AMBER + (255,))
        elif kind == "bubble":
            _bubble(d, cx, cy, s, white, p.get("text"), font("Bold", int(s * 0.42)))
        elif kind == "battery":
            _battery(d, cx, cy, s, p.get("level", 0.5), (230, 60, 60, 255))
        elif kind == "snow":
            _snow(d, cx, cy, s, white)
        elif kind == "heart":
            _heart(d, cx, cy, s, (255, 255, 255, 220))
        elif kind == "sparkle":
            _sparkle(d, cx, cy, s, white)
        elif kind == "pill":
            _pill(d, cx, cy, s, white, p["text"], font("Bold", int(s * 0.42)))
    img.alpha_composite(lay.resize(img.size, Image.LANCZOS))


def chevron(d, x, y, s, col):
    d.line((x, y - s / 2, x + s / 2, y, x, y + s / 2), fill=col, width=max(3, int(s / 5)), joint="curve")
