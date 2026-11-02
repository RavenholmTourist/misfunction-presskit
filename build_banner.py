# Build the presskit top banner: title card centred, gameplay crops mosaiced
# either side. Crop-only - nothing is scaled or distorted.
# Run: python presskit/build_banner.py
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
SHOTS = ROOT / "screenshots"
OUT = ROOT / "screenshots" / "banner.png"

BW, BH = 1920, 520          # banner canvas
VOID = (10, 8, 18)          # --void
SEAM = (70, 55, 110)        # dim purple seam between tiles
STAGGER = 16                # px vertical stagger between alternating tiles

# (file, crop_x, crop_y, tile_width) - crops are tile_width x BH from the source
LEFT = [
    ("strike_lightning", 70, 120, 210),
    ("boss_fight",       40, 140, 190),
    ("rule_gate",        90, 110, 190),
    ("daily_result",     60, 130, 190),
]
RIGHT = [
    ("bonus_cluster",    30, 150, 190),
    ("strike_bullet",    90, 120, 190),
    ("hero_stroop",      70, 110, 190),
    ("home_modes",       60, 140, 190),
]

canvas = Image.new("RGB", (BW, BH), VOID)

def slice_(name, cx, cy, w, y_off):
    im = Image.open(SHOTS / f"{name}.png").convert("RGB")
    tile = im.crop((cx, cy, cx + w, cy + BH))
    return tile, y_off

def paste_column(tiles, x0, flip_stagger=False):
    x = x0
    for i, (name, cx, cy, w) in enumerate(tiles):
        off = -STAGGER if (i % 2 == 0) ^ flip_stagger else STAGGER
        tile, y = slice_(name, cx, cy, w, off)
        canvas.paste(tile, (x, y))
        d = ImageDraw.Draw(canvas)
        d.rectangle([x + w, 0, x + w + 2, BH], fill=SEAM)
        x += w + 2
    return x

# centre title card: crop the card + wordmark region (575x1024 source)
tc = Image.open(SHOTS / "title_card.png").convert("RGB")
centre_w = 560
centre = tc.crop((8, 300, 8 + centre_w, 300 + BH))  # card + cross arms + top beam
cx0 = (BW - centre_w) // 2 - 2

left_x = cx0
for (name, cx, cy, w) in reversed(LEFT):
    left_x -= w + 2
    tile, y = slice_(name, cx, cy, w, 0)
    canvas.paste(tile, (left_x, y))
    ImageDraw.Draw(canvas).rectangle([left_x - 2 + 0, 0, left_x, BH], fill=SEAM)

# re-do left side cleanly with stagger (build left-to-right ending at centre)
canvas.paste(VOID, (0, 0, cx0, BH))
x = cx0 - 2
ImageDraw.Draw(canvas).rectangle([cx0 - 2, 0, cx0, BH], fill=SEAM)
for i, spec in enumerate(reversed(LEFT)):
    name, cx, cy, w = spec
    x -= w
    off = -STAGGER if i % 2 == 0 else STAGGER
    tile, y = slice_(name, cx, cy, w, off)
    canvas.paste(tile, (x, y))
    x -= 2
    ImageDraw.Draw(canvas).rectangle([x, 0, x + 2, BH], fill=SEAM)

# centre panel on top of seams
canvas.paste(centre, (cx0, 0))
ImageDraw.Draw(canvas).rectangle([cx0 - 2, 0, cx0, BH], fill=SEAM)
ImageDraw.Draw(canvas).rectangle([cx0 + centre_w, 0, cx0 + centre_w + 2, BH], fill=SEAM)

# right side
x = cx0 + centre_w + 2
for i, (name, cx, cy, w) in enumerate(RIGHT):
    off = -STAGGER if i % 2 == 1 else STAGGER
    tile, y = slice_(name, cx, cy, w, off)
    canvas.paste(tile, (x, y))
    x += w
    ImageDraw.Draw(canvas).rectangle([x, 0, x + 2, BH], fill=SEAM)
    x += 2

# side fade into void so the banner melts into the page
fade = Image.new("L", (BW, BH), 0)
fd = ImageDraw.Draw(fade)
for xx in range(140):
    a = int(255 * (1 - xx / 140) ** 1.4)
    fd.line([(xx, 0), (xx, BH)], fill=a)
    fd.line([(BW - 1 - xx, 0), (BW - 1 - xx, BH)], fill=a)
black = Image.new("RGB", (BW, BH), VOID)
canvas = Image.composite(black, canvas, fade)

# bottom fade so text can sit under it if needed
bfade = Image.new("L", (BW, BH), 0)
bfd = ImageDraw.Draw(bfade)
for yy in range(90):
    bfd.line([(0, BH - 1 - yy), (BW, BH - 1 - yy)], fill=int(255 * (yy / 90) ** 1.5))
canvas = Image.composite(black, canvas, bfade)

canvas.save(OUT)
print("wrote", OUT, canvas.size)
