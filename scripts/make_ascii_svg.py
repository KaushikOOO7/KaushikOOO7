from PIL import Image, ImageOps
from html import escape


# ============================================================
# SETTINGS
# ============================================================

INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"

# More characters = more detail
COLS = 80
ROWS = 80

# Terminal-style character size
CELL_WIDTH = 9
CELL_HEIGHT = 10

FONT_SIZE = 9

BACKGROUND = "#0d1117"
TEXT_COLOR = "#c9d1d9"

# Bright → dark
RAMP = " .`:-=+*cs#%@"

# Animation
ROW_DELAY = 0.025
ROW_DURATION = 0.35


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(INPUT_IMAGE).convert("L")

# ------------------------------------------------------------
# IMPORTANT:
# Your source image is square.
# We resize it to the COMPLETE ASCII grid instead of using
# ImageOps.contain(), which was making it tiny.
# ------------------------------------------------------------

image = image.resize(
    (COLS, ROWS),
    Image.Resampling.LANCZOS
)

pixels = image.load()


# ============================================================
# CONVERT IMAGE TO ASCII
# ============================================================

ascii_rows = []

for y in range(ROWS):

    row = ""

    for x in range(COLS):

        brightness = pixels[x, y]

        # White = space
        # Black = dense character

        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        index = max(
            0,
            min(index, len(RAMP) - 1)
        )

        row += RAMP[index]

    ascii_rows.append(row)


# ============================================================
# SVG SIZE
# ============================================================

WIDTH = COLS * CELL_WIDTH
HEIGHT = ROWS * CELL_HEIGHT


# ============================================================
# START SVG
# ============================================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
role="img"
aria-label="Animated ASCII portrait">

<rect
width="100%"
height="100%"
rx="8"
fill="{BACKGROUND}"/>

<style>

.ascii {{
    font-family:
        "Cascadia Mono",
        "Consolas",
        "Liberation Mono",
        monospace;

    font-size: {FONT_SIZE}px;
    font-weight: 500;
    fill: {TEXT_COLOR};
}}

.row {{
    opacity: 0;
    animation:
        appear 0.35s ease-out forwards;
}}

@keyframes appear {{

    0% {{
        opacity: 0;
        transform: translateX(-18px);
    }}

    100% {{
        opacity: 1;
        transform: translateX(0);
    }}

}}

</style>
'''


# ============================================================
# ADD ASCII ROWS
# ============================================================

for row_index, row in enumerate(ascii_rows):

    y = (row_index + 1) * CELL_HEIGHT - 2

    delay = row_index * ROW_DELAY

    svg += f'''
<text
class="ascii row"
x="10"
y="{y}"
xml:space="preserve"
style="animation-delay:{delay:.3f}s">
{escape(row)}
</text>
'''


# ============================================================
# END SVG
# ============================================================

svg += "</svg>"


# ============================================================
# SAVE
# ============================================================

with open(
    OUTPUT_SVG,
    "w",
    encoding="utf-8"
) as f:

    f.write(svg)


print(
    f"Created {OUTPUT_SVG}"
)

print(
    f"Size: {WIDTH} x {HEIGHT}"
)