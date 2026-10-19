"""Create listing graphics from the app's existing code-rendered preview."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
out = root / 'publishing' / 'images'
out.mkdir(parents=True, exist_ok=True)
preview = Image.open(root / 'output' / 'satisfy-fr45-preview-208.png').convert('RGB')
font_bold = 'C:/Windows/Fonts/arialbd.ttf'
font_regular = 'C:/Windows/Fonts/arial.ttf'

def face(canvas, xy, size):
    # Mask off the rectangular surroundings of the circular watch-face preview.
    mask = Image.new('L', (208, 208), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 207, 207), fill=255)
    canvas.paste(preview.resize((size, size), Image.Resampling.NEAREST), xy,
                 mask.resize((size, size), Image.Resampling.NEAREST))

cover = Image.new('RGB', (500, 500), '#141717')
d = ImageDraw.Draw(cover)
d.text((250, 32), 'SATISFY', font=ImageFont.truetype(font_bold, 30), anchor='mt', fill='white')
face(cover, (78, 81), 344)
d.text((250, 446), 'FORERUNNER 45', font=ImageFont.truetype(font_regular, 19), anchor='mt', fill='#c6ccca')
cover.save(out / 'cover-500.png', optimize=True)

screen = Image.new('RGB', (480, 530), '#141717')
face(screen, (32, 30), 416)
sd = ImageDraw.Draw(screen)
sd.text((240, 465), 'SATISFY / FR45', font=ImageFont.truetype(font_bold, 23), anchor='mt', fill='white')
sd.text((240, 500), 'Design preview - example values', font=ImageFont.truetype(font_regular, 16), anchor='mt', fill='#c6ccca')
screen.save(out / 'screen-preview.png', optimize=True)

hero = Image.new('RGB', (1440, 720), '#141717')
hd = ImageDraw.Draw(hero)
hd.text((110, 200), 'SATISFY', font=ImageFont.truetype(font_bold, 90), fill='white')
hd.text((115, 326), 'FORERUNNER 45', font=ImageFont.truetype(font_regular, 32), fill='#c6ccca')
hd.text((115, 393), 'Large time. Clear daily stats.', font=ImageFont.truetype(font_regular, 28), fill='#c6ccca')
face(hero, (795, 90), 540)
hd.text((1065, 658), 'Design preview - example values', font=ImageFont.truetype(font_regular, 18), anchor='mt', fill='#9ca7a2')
hero.save(out / 'hero-1440x720.png', optimize=True)

for name, dimensions, maximum in [('cover-500.png', (500, 500), 300_000),
                                   ('screen-preview.png', (480, 530), 150_000),
                                   ('hero-1440x720.png', (1440, 720), 2_048_000)]:
    path = out / name
    assert Image.open(path).size == dimensions
    assert path.stat().st_size < maximum
    print(name, dimensions, path.stat().st_size, 'bytes: OK')
