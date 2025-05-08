import os, sys
from PIL import Image, ImageDraw, ImageFont

FIG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'paper', 'figs')
FIG_DIR = os.path.abspath(FIG_DIR)

W, H = 800, 450
BG = (255, 255, 255)
FG = (0, 0, 0)

font = None
try:
    font = ImageFont.truetype('DejaVuSans.ttf', 32)
except Exception:
    font = ImageFont.load_default()

for fname in os.listdir(FIG_DIR):
    if fname.endswith('.png'):
        path = os.path.join(FIG_DIR, fname)
        # create placeholder with text
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        text = os.path.splitext(fname)[0].replace('_', '\n')
        w, h = d.multiline_textsize(text, font=font, spacing=4)
        d.multiline_text(((W - w) / 2, (H - h) / 2), text, fill=FG, font=font, align='center', spacing=4)
        img.save(path)
        print('placeholder written', path) 