#!/usr/bin/env python3
"""make.fun entry: news-image-20261125 — the world news of 25 November 2026.

Draws one 1024x1024 PNG summarising six stories from Wednesday 25 November
2026, using only Pillow primitives: no downloads, no network, no randomness,
no input files. Every run writes byte-identical output.

Stories (all reported on 25 November 2026):
  1. Zelenskiy confirms Ukraine hit a Russian cargo ship in the Gulf of Finland.
  2. Medvedev warns Russia could carry out a "preventive nuclear attack".
  3. NATO to deploy AWACS early-warning aircraft to Poland.
  4. Houthis strike Riyadh's tallest tower; 11 wounded.
  5. Huawei convicted in a US criminal trial over its Iran business.
  6. The CIA and ODNI suffer a cybersecurity breach.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (12, 27, 46)
PANEL = (24, 46, 72)
INK = (238, 242, 247)
MUTED = (168, 184, 202)
GOLD = (232, 184, 66)
DARK = (16, 34, 56)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=8):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_ship(d, x, y, s, color):
    """Cargo ship under a small drone: hull, containers, bridge, waves."""
    # Drone above the ship.
    d.rectangle([x + s * 0.62, y + s * 0.04, x + s * 0.86, y + s * 0.12], fill=(255, 255, 255))
    d.line([x + s * 0.62, y + s * 0.08, x + s * 0.56, y + s * 0.02], fill=(255, 255, 255), width=3)
    d.line([x + s * 0.86, y + s * 0.08, x + s * 0.92, y + s * 0.02], fill=(255, 255, 255), width=3)
    d.ellipse([x + s * 0.50, y, x + s * 0.62, y + s * 0.06], fill=(255, 255, 255))
    d.ellipse([x + s * 0.86, y, x + s * 0.98, y + s * 0.06], fill=(255, 255, 255))
    # Hull and containers.
    d.polygon([(x + s * 0.04, y + s * 0.58), (x + s * 0.96, y + s * 0.58),
               (x + s * 0.82, y + s * 0.84), (x + s * 0.18, y + s * 0.84)], fill=color)
    d.rectangle([x + s * 0.16, y + s * 0.40, x + s * 0.34, y + s * 0.58], fill=(255, 255, 255))
    d.rectangle([x + s * 0.38, y + s * 0.40, x + s * 0.56, y + s * 0.58], fill=color)
    d.rectangle([x + s * 0.60, y + s * 0.40, x + s * 0.72, y + s * 0.58], fill=(255, 255, 255))
    # Bridge tower and mast.
    d.rectangle([x + s * 0.76, y + s * 0.30, x + s * 0.90, y + s * 0.58], fill=color)
    d.line([x + s * 0.83, y + s * 0.12, x + s * 0.83, y + s * 0.30], fill=(255, 255, 255), width=4)
    d.polygon([(x + s * 0.83, y + s * 0.12), (x + s * 0.97, y + s * 0.22),
               (x + s * 0.83, y + s * 0.22)], fill=(255, 255, 255))
    # Waves.
    d.arc([x + s * 0.06, y + s * 0.88, x + s * 0.34, y + s * 1.04], 180, 360, fill=(255, 255, 255), width=4)
    d.arc([x + s * 0.66, y + s * 0.88, x + s * 0.94, y + s * 1.04], 180, 360, fill=(255, 255, 255), width=4)


def draw_radiation(d, x, y, s, color):
    """Radiation trefoil: three blades around a centre disc."""
    cx, cy = x + s * 0.50, y + s * 0.50
    d.ellipse([x + s * 0.04, y + s * 0.04, x + s * 0.96, y + s * 0.96], fill=color)
    for start in (60, 180, 300):
        d.pieslice([x + s * 0.12, y + s * 0.12, x + s * 0.88, y + s * 0.88],
                   start, start + 60, fill=BG)
    d.ellipse([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60], fill=color)
    d.ellipse([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56], fill=BG)


def draw_awacs(d, x, y, s, color):
    """AWACS plane in profile: fuselage, radar dome, wings, tail."""
    # Radar dome on a stalk above the fuselage.
    d.rectangle([x + s * 0.44, y + s * 0.24, x + s * 0.52, y + s * 0.36], fill=color)
    d.ellipse([x + s * 0.30, y + s * 0.08, x + s * 0.66, y + s * 0.30], fill=color)
    d.ellipse([x + s * 0.34, y + s * 0.12, x + s * 0.62, y + s * 0.26], fill=(255, 255, 255))
    # Fuselage with nose and tail fin.
    d.rounded_rectangle([x + s * 0.06, y + s * 0.42, x + s * 0.94, y + s * 0.62], radius=10, fill=color)
    d.polygon([(x + s * 0.80, y + s * 0.42), (x + s * 0.94, y + s * 0.42),
               (x + s * 0.88, y + s * 0.22)], fill=color)
    # Wing and tailplane.
    d.polygon([(x + s * 0.36, y + s * 0.60), (x + s * 0.56, y + s * 0.60),
               (x + s * 0.66, y + s * 0.88), (x + s * 0.46, y + s * 0.88)], fill=color)
    d.polygon([(x + s * 0.10, y + s * 0.58), (x + s * 0.24, y + s * 0.58),
               (x + s * 0.16, y + s * 0.76), (x + s * 0.06, y + s * 0.76)], fill=color)
    # Windows.
    for i in range(4):
        wx = x + s * (0.22 + i * 0.13)
        d.rectangle([wx, y + s * 0.48, wx + s * 0.07, y + s * 0.55], fill=(255, 255, 255))


def draw_tower(d, x, y, s, color):
    """Skyscraper with a blast star at its crown."""
    d.polygon(star_points(x + s * 0.50, y + s * 0.16, s * 0.20, s * 0.08, n=8), fill=GOLD)
    d.polygon([(x + s * 0.32, y + s * 0.30), (x + s * 0.68, y + s * 0.30),
               (x + s * 0.74, y + s * 0.98), (x + s * 0.26, y + s * 0.98)], fill=color)
    for row in range(4):
        for col in range(3):
            wx = x + s * (0.38 + col * 0.10)
            wy = y + s * (0.38 + row * 0.15)
            d.rectangle([wx, wy, wx + s * 0.06, wy + s * 0.07], fill=(255, 255, 255))
    d.rectangle([x + s * 0.20, y + s * 0.96, x + s * 0.80, y + s * 1.00], fill=(255, 255, 255))


def draw_court(d, x, y, s, color):
    """Courthouse: pediment, three columns, steps."""
    d.polygon([(x + s * 0.04, y + s * 0.34), (x + s * 0.96, y + s * 0.34),
               (x + s * 0.50, y + s * 0.08)], fill=color)
    d.ellipse([x + s * 0.44, y + s * 0.20, x + s * 0.56, y + s * 0.30], fill=(255, 255, 255))
    for cx in (0.22, 0.50, 0.78):
        d.rectangle([x + s * (cx - 0.06), y + s * 0.40, x + s * (cx + 0.06), y + s * 0.82],
                    fill=color)
    d.rectangle([x + s * 0.08, y + s * 0.84, x + s * 0.92, y + s * 0.90], fill=color)
    d.rectangle([x + s * 0.04, y + s * 0.92, x + s * 0.96, y + s * 0.98], fill=color)


def draw_lock(d, x, y, s, color):
    """Padlock split by a lightning crack: a breached system."""
    d.arc([x + s * 0.28, y + s * 0.06, x + s * 0.72, y + s * 0.48], 180, 360, fill=color, width=10)
    d.rounded_rectangle([x + s * 0.14, y + s * 0.42, x + s * 0.86, y + s * 0.96], radius=10, fill=color)
    d.ellipse([x + s * 0.43, y + s * 0.54, x + s * 0.57, y + s * 0.68], fill=(255, 255, 255))
    d.rectangle([x + s * 0.47, y + s * 0.66, x + s * 0.53, y + s * 0.82], fill=(255, 255, 255))
    bolt = [(x + s * 0.60, y + s * 0.02), (x + s * 0.44, y + s * 0.44),
            (x + s * 0.56, y + s * 0.44), (x + s * 0.42, y + s * 0.92),
            (x + s * 0.66, y + s * 0.40), (x + s * 0.54, y + s * 0.40)]
    d.polygon(bolt, fill=GOLD)


PANELS = [
    ("UKRAINE CLAIMS SHIP STRIKE", (46, 111, 219), draw_ship,
     "Zelenskiy confirms Kyiv's drones hit a Russian cargo ship in the Gulf of Finland; Norway urges caution.",
     "REUTERS · 25 NOV"),
    ("MEDVEDEV'S NUCLEAR WARNING", (192, 57, 43), draw_radiation,
     "Medvedev says Ukraine and NATO have crossed lines that could trigger a \u201cpreventive nuclear attack\u201d.",
     "TASS VIA NY POST · 25 NOV"),
    ("NATO SENDS AWACS TO POLAND", (39, 174, 96), draw_awacs,
     "Early-warning aircraft to patrol Poland after Russian Kh-101 cruise missiles fell there last week.",
     "25 NOV"),
    ("HOUTHIS HIT RIYADH TOWER", (230, 126, 34), draw_tower,
     "Drone strike on the capital's tallest tower wounds 11 \u2014 the second such hit in under a week.",
     "REUTERS · 25 NOV"),
    ("HUAWEI GUILTY IN US TRIAL", (123, 75, 214), draw_court,
     "New York jury finds the Chinese firm guilty over its Iran business and stolen trade secrets.",
     "REUTERS · 25 NOV"),
    ("CIA AND ODNI HIT BY BREACH", (201, 162, 39), draw_lock,
     "US intelligence agencies suffer a cybersecurity breach involving some unclassified information.",
     "REUTERS · 25 NOV"),
]

TICKER = (
    "ALSO TODAY  \u00b7  Trump awards Giuliani the Medal of Freedom  \u00b7  "
    "2 killed in Odesa strikes; Kyiv hit again  \u00b7  "
    "EU unveils 22nd Russia sanctions package  \u00b7  "
    "Putin vows retaliation over oil-plant strikes  \u00b7  "
    "WHO urges US to lift Cuba fuel blockade  \u00b7  "
    "25 hostages held in Cartagena supermarket"
)


def build_image():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(FONT_BOLD, 44)
    f_sub = font(FONT_REG, 22)
    f_head = font(FONT_BOLD, 29)
    f_fact = font(FONT_REG, 21)
    f_src = font(FONT_REG, 15)
    f_tick = font(FONT_REG, 18)

    # Masthead.
    d.rectangle([0, 0, W, 118], fill=(8, 18, 32))
    d.rectangle([0, 118, W, 124], fill=GOLD)
    d.text((28, 26), "THE WORLD IN ONE IMAGE", font=f_title, fill=INK)
    d.text((28, 78), "WEDNESDAY \u00b7 25 NOVEMBER 2026", font=f_sub, fill=MUTED)
    d.text((W - 28, 30), "make.fun \u00b7 $100", font=font(FONT_BOLD, 24), fill=GOLD, anchor="ra")
    d.text((W - 28, 66), "SIX STORIES \u00b7 ONE PICTURE", font=font(FONT_REG, 18), fill=MUTED, anchor="ra")

    # Six panels: 2 columns x 3 rows.
    margin, gap = 16, 14
    pw = (W - 2 * margin - gap) // 2
    ph = 252
    top = 140
    for i, (title, accent, icon, caption, src) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = margin + col * (pw + gap)
        py = top + row * (ph + gap)
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=PANEL)
        d.rounded_rectangle([px, py, px + pw, py + 10], radius=5, fill=accent)
        d.rectangle([px, py + 5, px + pw, py + 10], fill=accent)
        d.rounded_rectangle([px + 16, py + 26, px + 132, py + 142], radius=10, fill=DARK)
        icon(d, px + 24, py + 34, 100, accent)
        head_lines = wrap(title, f_head, pw - 166, d)[:2]
        hy = py + 32
        for line in head_lines:
            d.text((px + 146, hy), line, font=f_head, fill=INK)
            hy += 36
        fact_lines = wrap(caption, f_fact, pw - 36, d)[:3]
        fy = py + 146
        for line in fact_lines:
            d.text((px + 18, fy), line, font=f_fact, fill=MUTED)
            fy += 26
        d.text((px + 18, py + ph - 24), src, font=f_src, fill=(120, 140, 164))
        d.text((px + pw - 52, py + ph - 24), "%d / 6" % (i + 1), font=f_src, fill=(120, 140, 164))

    # Ticker.
    d.rectangle([0, 930, W, H], fill=(10, 20, 34))
    d.rectangle([0, 930, W, 934], fill=GOLD)
    tick_lines = wrap(TICKER, f_tick, W - 56, d)
    ty = 940
    for line in tick_lines:
        d.text((28, ty), line, font=f_tick, fill=(200, 212, 226))
        ty += 26
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build_image()
    target = os.path.join(out_dir, "entry.png")
    img.save(target, format="PNG")
    print("wrote {} ({} bytes)".format(target, os.path.getsize(target)))


if __name__ == "__main__":
    main()
