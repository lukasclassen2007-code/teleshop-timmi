# Teleshop Timmendorfer Strand – Timmi

Social-Media-Projekt mit der Shop-Katze **Timmi**: tägliche Instagram-Posts und ein wöchentlicher Clip für den TV am Eingang.
Ziel: Frequenz im Shop schaffen und in Timmendorfer Strand eine Marke werden.

**Status (7.11.2026): pausiert** bis zur Rücksprache mit dem Chef (Freigabe Shop-Account, Logo, Impressum).

## Eckdaten

| | |
| --- | --- |
| Shop | Teleshop Timmendorfer Strand, Poststraße 34 (Kette: Hansemobile GmbH) |
| Öffnungszeiten | Mo–Fr 9–17 Uhr (Sa/So geschlossen) |
| Instagram Shop | @teleshop_timmendorfer_strand (noch nicht mit Windsor verbunden) |
| Instagram Test | flickson_cs (mit Windsor verbunden, Testpost + Story am 7.11. erfolgreich) |
| Ansprache | Du, locker, ohne Fachchinesisch |
| Posting | täglich, Karussell aus Tipp-Bild + Fun-Fact-Karte, Freigabe vor Veröffentlichung |
| TV | Hochformat 1080×1920, ohne Ton, per USB, montags neu aufspielen |
| Farben | Schwarz #111111 · Weiß · Bernstein #FFA62B |

## Ordner

| Pfad | Inhalt |
| --- | --- |
| `assets/raw/` | Original-Posen von Timmi (Bild-KI), `timmi_02_handy_sms.jpg` = mit eingesetzter Betrugs-SMS |
| `assets/cut/` | Freigestellte Posen (PNG, transparent) |
| `assets/logo.png` | Logo-Schriftzug (Screenshot, niedrige Auflösung – Original besorgen) |
| `scripts/` | Render-Skripte (Python, Pillow) |
| `wochen/2026-11-09/` | Erste Woche: Plan-JSON, 14 Post-Bilder, Texte, TV-Clip |
| `test/` | Bilder des Testposts und der Test-Story |

## Skripte

Im Ordner `scripts/` ausführen (erwartet `raw/`, `cut/` und `logo.png` daneben – vorher `assets/*` dorthin kopieren oder verlinken):

```bash
pip install pillow opencv-python qrcode rembg onnxruntime
python3 render_post.py woche.json ausgabeordner      # 2 Bilder je Tag + Fun-Fact
python3 render_tv.py tv_woche.json clip.mp4          # TV-Clip mit QR-Code zu Instagram
python3 make_sms_pose.py                             # SMS auf Handy-Display setzen
```

- `timmi_lib.py`: Design-System (Themen-Farben, Deko, Logo, Freisteller, Schriften)
- Themen: `intro`, `warn`, `data`, `signal`, `weekend`, `cold`, `wifi`, `cta`
- TV-Clip: Katze wird nur pixelgenau gesetzt (kein Zittern), Bewegung über Deko, Texte, Schiebeblenden
- Fußleiste im TV-Clip: QR-Code auf instagram.com/teleshop_timmendorfer_strand (geprüft, lesbar)

## Bild-URLs für Instagram (Windsor)

Öffentliche Rohlinks: `https://raw.githubusercontent.com/lukasclassen2007-code/teleshop-timmi/main/<pfad>`

## Offene Punkte

1. **QR-Code (wichtig):** im TV-Clip umgesetzt. Zusätzlich QR-Aufsteller/Sticker im Schaufenster und an der Kasse.
2. Shop-Account @teleshop_timmendorfer_strand in Windsor verbinden (nach Rücksprache Chef).
3. Impressum als Link in der Instagram-Bio klären.
4. Logo-Nutzung (inkl. Netzbetreiber-Symbole) mit Hansemobile klären, Logo als SVG/hochauflösend besorgen.
5. Geplante Aufgabe einrichten: sonntags neue Woche zur Freigabe, danach täglicher Post.
6. TV-Clip wöchentlich zusätzlich als Reel posten.
7. Storys mit Umfrage-/Countdown-Sticker gelegentlich von Hand in der App.
8. Neue Posen: Handy nah zur Kamera (lesbare SMS), frierender Timmi mit Handy.
9. Nach 4 Wochen Auswertung über Windsor (Speicherungen, Shares, Reichweite).
