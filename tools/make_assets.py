"""Generate the exact monochrome bitmap fonts and a clearly labelled mockup.

No static health numbers are embedded in the app. Preview numbers are examples.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / 'resources' / 'fonts'
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)

def create_font(name, font_path, size, height, characters, scale=1.0):
    font = ImageFont.truetype(font_path, size)
    top = font.getbbox('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')[1]
    atlas = Image.new('RGBA', (256, 128), (0, 0, 0, 0))
    x = y = 0
    entries = []
    glyphs = {}
    for character in characters:
        advance = max(3, round(font.getlength(character) * scale))
        image = Image.new('L', (max(1, round(font.getlength(character)) + 3), height), 0)
        ImageDraw.Draw(image).text((0, -top), character, font=font, fill=255)
        image = image.resize((advance + 1, height), Image.Resampling.LANCZOS)
        image = image.point(lambda v: 255 if v >= 120 else 0)
        if x + image.width >= 256:
            x = 0
            y += height + 1
        glyph = Image.new('RGBA', image.size, (255, 255, 255, 0))
        glyph.putalpha(image)
        atlas.paste(glyph, (x, y))
        entries.append(f'char id={ord(character)} x={x} y={y} width={image.width} height={height} xoffset=0 yoffset=0 xadvance={advance} page=0 chnl=15')
        glyphs[character] = (image, advance)
        x += image.width + 1
    atlas.save(FONTS / f'{name}.png')
    lines = [f'info face="Satisfy {name}" size={height} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=1,1 outline=0',
             f'common lineHeight={height} base={height} scaleW=256 scaleH=128 pages=1 packed=0',
             f'page id=0 file="{name}.png"', f'chars count={len(entries)}', *entries]
    (FONTS / f'{name}.fnt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return glyphs

glyph_sets = {
    'time': create_font('time', 'C:/Windows/Fonts/ARIALNB.TTF', 59, 43, '0123456789:', 0.92),
    'small': create_font('small', 'C:/Windows/Fonts/arial.ttf', 15, 12, ' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ:.-%/', 0.82),
    'name': create_font('name', 'C:/Windows/Fonts/ARIALNB.TTF', 15, 12, 'SATIFY', 1.0),
}

face = Image.new('RGB', (208, 208), 'white')
draw = ImageDraw.Draw(face)

def text(x, y, value, style='small', center=False):
    glyphs = glyph_sets[style]
    width = sum(glyphs[c][1] for c in value)
    if center:
        x -= width // 2
    for char in value:
        mask, advance = glyphs[char]
        face.paste('black', (int(x), y), mask)
        x += advance
    return width

points = [(x, int(104 - math.sqrt(99**2 - (x - 104)**2))) for x in range(35, 174)]
draw.line(points, fill='black')
draw.rectangle((80, 18, 92, 24), outline='black')
draw.rectangle((93, 20, 94, 22), fill='black')
draw.rectangle((82, 20, 87, 22), fill='black')
text(100, 15, '66%')
text(30, 33, 'FRI 18.09')
text(17, 49, '01:34', 'time')
text(149, 82, 'SATISFY', 'name')
for y, label, value in [(97, 'DIST', '5.3 KM'), (110, 'STEPS', '7421'), (123, 'HEART RATE', '68 BPM'), (136, 'RECOVERY', '-- H'), (149, 'KCAL', '1190')]:
    text(24, y, label)
    width = sum(glyph_sets['small'][c][1] for c in value)
    text(140 if width > 49 else 149, y, value)
points = []
for x in range(24, 185):
    y = int(178 - 15 * math.sin((x - 24) * math.pi / 160)**2)
    points.append((x, y))
    if x % 3 == 0 and x <= 24 + int(160 * .74):
        for yy in range(y + 4, 206, 3):
            if (x - 104)**2 + (yy - 104)**2 < 102**2:
                draw.point((x, yy), fill='black')
draw.line(points, fill='black')
width = sum(glyph_sets['small'][c][1] for c in '74% GOAL')
draw.rectangle((104 - width // 2 - 3, 183, 104 + width // 2 + 3, 196), fill='white')
text(104, 184, '74% GOAL', center=True)
mask = Image.new('L', (208, 208), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 207, 207), fill=255)
rounded = Image.new('RGB', (208, 208), '#202020')
rounded.paste(face, mask=mask)
rounded.save(OUT / 'satisfy-fr45-preview-208.png')

canvas = Image.new('RGB', (720, 820), '#151718')
cd = ImageDraw.Draw(canvas)
heading = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 30)
body = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
cd.text((48, 38), 'SATISFY / FORERUNNER 45', fill='white', font=heading)
cd.text((48, 85), '208 x 208 px  |  Pratinjau desain', fill='#a5aca9', font=body)
cd.ellipse((32, 136, 688, 792), fill='#090909', outline='#353b3b', width=4)
large = rounded.resize((624, 624), Image.Resampling.NEAREST)
canvas.paste(large, (48, 152))
cd.text((48, 790), 'Angka contoh; RECOVERY tidak tersedia di FR45.', fill='#b9bdbb', font=body)
canvas.save(OUT / 'satisfy-fr45-preview.png')

icon = Image.new('RGBA', (65, 65), 'white')
idraw = ImageDraw.Draw(icon)
idraw.ellipse((2, 2, 62, 62), outline='black', width=3)
idraw.text((19, 9), 'S', font=ImageFont.truetype('C:/Windows/Fonts/ARIALNB.TTF', 44), fill='black')
icon.save(ROOT / 'resources' / 'drawables' / 'launcher.png')
print('Generated three bitmap fonts, launcher icon and design preview.')
