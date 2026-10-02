"""Render the original profile ASCII as a self-contained animated SVG.

Run: python scripts/generate-night-watch.py
Standard library only. All ASCII glyphs are geometry: no font downloads,
JavaScript, external assets or scheduled jobs are required.
"""
from collections import defaultdict
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
ASCII = (ROOT / 'assets/night-watch.txt').read_text(encoding='utf-8')
X, Y, CW, CH = 128, 78, 16, 22
W, H = 1200, 594


def rect_path(x, y, w, h):
    return f'M{x:g} {y:g}h{w:g}v{h:g}h{-w:g}z'


def glyph(char, col, row):
    x, y = X + col * CW, Y + row * CH
    if char == '▄':
        return rect_path(x, y + CH/2, CW, CH/2)
    if char == '▀':
        return rect_path(x, y, CW, CH/2)
    if char == '▐':
        return rect_path(x + CW/2, y, CW/2, CH)
    if char == '▌':
        return rect_path(x, y, CW/2, CH)
    if char in '░▒▓':
        # Re-create block-shading characters as a regular pixel matrix.
        out = []
        for yy in range(0, CH, 2):
            for xx in range(0, CW, 2):
                n = (xx//2 + yy//2) % 4
                if n < {'░': 1, '▒': 2, '▓': 3}[char]:
                    out.append(rect_path(x+xx, y+yy, 2, 2))
        return ''.join(out)
    if char == '█':
        return rect_path(x, y, CW, CH)
    if char == '.':
        return rect_path(x+7, y+16, 3, 3)
    raise ValueError(f'Unexpected ASCII glyph: {char!r}')


def region(row, col, char):
    if char == '.':
        return 'original-stars'
    if row < 4 and col > 40:
        return 'moon'
    if row >= 17 or (row == 16 and col < 33):
        return 'ground'
    if col >= 47 and row >= 11:
        if col == 53 and row <= 14:
            return 'sword'
        return 'fire' if row < 16 else 'coals'
    if col >= 47:
        return 'sword'
    if col >= 31 and row >= 7:
        return 'knight'
    return 'castle'


paths = defaultdict(list)
for row, line in enumerate(ASCII.splitlines()):
    for col, char in enumerate(line):
        if not char.isspace():
            paths[region(row, col, char)].append(glyph(char, col, row))

style = '''
  .moon-halo { animation: moon-breathe 8s ease-in-out infinite; }
  .star { animation: twinkle var(--d) ease-in-out var(--delay) infinite; }
  .ember { animation: rise var(--d) linear var(--delay) infinite; }
  .fire { animation: firelight 2s ease-in-out infinite; }
  .fire-a { animation: flame-a 1s steps(4,end) infinite; transform-origin: 952px 418px; }
  .fire-b { animation: flame-b 1.6s steps(5,end) infinite; transform-origin: 1016px 418px; }
  .warmth { animation: warmth 4s ease-in-out infinite; }
  .knight { animation: breathe 8s ease-in-out infinite; }
  .mist-a { animation: drift 8s ease-in-out infinite; }
  .mist-b { animation: drift 8s ease-in-out -4s infinite; }
  .meteor { opacity: 0; animation: meteor 8s linear infinite; }
  .blade-light { opacity: 0; animation: blade 8s ease-in-out infinite; }
  .castle-light { animation: castle-light 8s ease-in-out infinite; }
  @keyframes moon-breathe { 0%,100% { opacity:.45; } 50% { opacity:.8; } }
  @keyframes twinkle { 0%,100% { opacity:.15; } 50% { opacity:.85; } }
  @keyframes rise { 0% { transform:translate(0,0); opacity:0; } 12% { opacity:.95; } 85% { opacity:.65; } 100% { transform:translate(var(--dx),var(--dy)); opacity:0; } }
  @keyframes firelight { 0%,100% { opacity:.9; } 25% { opacity:1; } 50% { opacity:.77; } 75% { opacity:.96; } }
  @keyframes flame-a { 0%,100% { transform:translateY(0) scaleY(1); } 33% { transform:translateY(-5px) scaleY(1.12); } 66% { transform:translateY(3px) scaleY(.94); } }
  @keyframes flame-b { 0%,100% { transform:translateY(-2px) scaleY(1.06); } 40% { transform:translateY(4px) scaleY(.9); } 70% { transform:translateY(-7px) scaleY(1.14); } }
  @keyframes warmth { 0%,100% { opacity:.48; } 50% { opacity:.78; } }
  @keyframes breathe { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-1.5px); } }
  @keyframes drift { 0%,100% { transform:translateX(-28px); opacity:.24; } 50% { transform:translateX(36px); opacity:.5; } }
  @keyframes meteor { 0%,70%,100% { opacity:0; transform:translate(0,0); } 72% { opacity:.9; } 79% { opacity:0; transform:translate(210px,100px); } }
  @keyframes blade { 0%,20%,42%,100% { opacity:0; transform:translateY(0); } 24% { opacity:.9; } 38% { opacity:.8; transform:translateY(125px); } }
  @keyframes castle-light { 0%,100% { opacity:.1; } 50% { opacity:.23; } }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation:none !important; }
    .ember { opacity:.45; }
  }
'''

out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">G1LB3T0 · The Night Watch</title>
<desc id="desc">El ASCII original de un castillo, un caballero, una espada en una hoguera y una luna creciente. Fuego ámbar, brasas ascendentes, estrellas, niebla y reflejos de luz animados. Se detiene con la preferencia de movimiento reducido.</desc>
<defs>
  <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#080e1b"/><stop offset=".7" stop-color="#10182a"/><stop offset="1" stop-color="#0a111e"/></linearGradient>
  <radialGradient id="moon-halo"><stop stop-color="#89c6f0" stop-opacity=".22"/><stop offset="1" stop-color="#89c6f0" stop-opacity="0"/></radialGradient>
  <radialGradient id="fire-halo"><stop stop-color="#ff9c43" stop-opacity=".38"/><stop offset=".45" stop-color="#ee6730" stop-opacity=".12"/><stop offset="1" stop-color="#ff823b" stop-opacity="0"/></radialGradient>
  <linearGradient id="stone" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#b0cfeb"/><stop offset=".3" stop-color="#789bbb"/><stop offset=".7" stop-color="#496482"/><stop offset="1" stop-color="#263c56"/></linearGradient>
  <linearGradient id="earth" x2="0" y2="1"><stop stop-color="#5a7790"/><stop offset=".5" stop-color="#334d68"/><stop offset="1" stop-color="#182e46"/></linearGradient>
  <linearGradient id="armor"><stop stop-color="#6a92b4"/><stop offset=".48" stop-color="#c0d9e4"/><stop offset=".73" stop-color="#88a3ad"/><stop offset="1" stop-color="#e7b381"/></linearGradient>
  <linearGradient id="flame" x2="0" y2="1"><stop stop-color="#f7853b"/><stop offset=".42" stop-color="#ffbd64"/><stop offset=".72" stop-color="#ffe1a0"/><stop offset="1" stop-color="#c66a34"/></linearGradient>
  <linearGradient id="steel" x2="0" y2="1"><stop stop-color="#d6e7ee"/><stop offset=".6" stop-color="#b6c7d3"/><stop offset="1" stop-color="#ffd48d"/></linearGradient>
  <linearGradient id="trail"><stop stop-color="#bce5ff" stop-opacity="0"/><stop offset="1" stop-color="#d6edff"/></linearGradient>
  <linearGradient id="mist"><stop stop-color="#a6cadb" stop-opacity="0"/><stop offset=".45" stop-color="#98b7d0" stop-opacity=".19"/><stop offset="1" stop-color="#a6cadb" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="fog"><feGaussianBlur stdDeviation="9"/></filter>
  <clipPath id="frame"><rect width="1200" height="594" rx="18"/></clipPath>
  <clipPath id="blade-mask"><path d="{''.join(paths['sword'])}"/></clipPath>
</defs>
<style>{style}</style>
<g clip-path="url(#frame)">
<rect width="1200" height="594" fill="url(#sky)"/>
<ellipse class="moon-halo" cx="881" cy="124" rx="215" ry="178" fill="url(#moon-halo)"/>
<ellipse class="warmth" cx="961" cy="400" rx="251" ry="178" fill="url(#fire-halo)"/>
<g fill="#aac4db">''']

rng = random.Random(19)
for i in range(54):
    x, y = rng.randrange(60,1145), rng.randrange(62,386)
    # Clear space around the silhouette so the original art stays legible.
    if (x < 490 and y > 140) or (640 < x < 812 and y > 220):
        continue
    d, delay, s = rng.choice([2,4,8]), -rng.randint(1,8), rng.choice([1,1,1.5,2])
    out.append(f'<rect class="star" x="{x}" y="{y}" width="{s}" height="{s}" opacity=".45" style="--d:{d}s;--delay:{delay}s"/>')
out.append('</g><path class="meteor" d="M528 97l92 43" stroke="url(#trail)" stroke-width="2"/>')

fills = {'castle':'url(#stone)', 'ground':'url(#earth)', 'knight':'url(#armor)',
         'moon':'#d4e5ee', 'original-stars':'#b8d2e5', 'fire':'url(#flame)',
         'coals':'#b17c58', 'sword':'url(#steel)'}
for key in ('original-stars','moon','castle','ground','coals','knight','sword','fire'):
    path = ''.join(paths[key])
    if key in ('moon','fire'):
        out.append(f'<path d="{path}" fill="{fills[key]}" filter="url(#glow)" opacity=".28" class="{key}"/>')
    out.append(f'<path id="ascii-{key}" class="{key}" d="{path}" fill="{fills[key]}"/>')

out.append('''
<!-- Light in the two arched windows, behind the original stone silhouette. -->
<g class="castle-light" fill="#b0d3ef" opacity=".15">
<path d="M384 354h8v31h-8zm16-8h4v49h-4zM488 374h7v31h-7z"/>
</g>
<!-- Pixel tongues grow out of the original bonfire. -->
<g fill="#ffc479" class="fire-a" opacity=".8"><path d="M930 390h4v-13h4v-9h4v28h-12zM949 408h5v-30h5v-12h4v42z"/></g>
<g fill="#ffab58" class="fire-b" opacity=".8"><path d="M1009 401h5v-21h5v-13h4v34zM1030 411h4v-17h5v-11h4v28z"/></g>
<g clip-path="url(#blade-mask)"><path class="blade-light" d="M936 252l73-13v12l-73 13z" fill="#fff3d0"/></g>
''')
for i in range(24):
    x,y = rng.randrange(929,1037),rng.randrange(401,444)
    dx,dy = rng.randrange(-85,38),rng.randrange(-192,-75)
    d,delay = rng.choice([4,8]),-rng.uniform(0,8)
    size = rng.choice([2,2,3])
    color = rng.choice(['#ffbd6b','#f79745','#ffe2a3'])
    out.append(f'<rect class="ember" x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" opacity="0" style="--dx:{dx}px;--dy:{dy}px;--d:{d:.2f}s;--delay:{delay:.2f}s"/>')

out.append('''
<g filter="url(#fog)" fill="url(#mist)">
<path class="mist-a" d="M34 467q200-33 421 4t506-9v19q-273 22-510 7T34 486z" opacity=".32"/>
<path class="mist-b" d="M309 507q219-23 378-1t459-10v13q-220 24-459 14t-378 1z" opacity=".25"/>
</g>
<path d="M35 42V26h16M1149 26h16v16M35 552v16h16M1149 568h16v-16" fill="none" stroke="#47607a" stroke-opacity=".6"/>
<g font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">
<text x="59" y="36" fill="#829ab4">G1LB3T0</text>
<text x="1140" y="36" fill="#829ab4" text-anchor="end">THE NIGHT WATCH</text>
<text x="60" y="563" fill="#71849b" font-size="10" letter-spacing="1.5">BUILT FROM CHARACTERS. BROUGHT TO LIFE.</text>
<text x="1140" y="563" fill="#a5b7c8" text-anchor="end" font-size="10" letter-spacing="1.5">&lt; / &gt;</text>
</g>
<rect x=".5" y=".5" width="1199" height="593" rx="18" fill="none" stroke="#2c3b50" stroke-opacity=".65"/>
</g>
</svg>
''')
svg = '\n'.join(out)
(ROOT / 'assets/night-watch.svg').write_text(svg, encoding='utf-8')
# Static alternative honors the same original art and palette.
static = svg.replace(f'<style>{style}</style>', '<style>.ember{opacity:.45}.meteor,.blade-light{opacity:0}</style>')
static = static.replace('Fuego ámbar, brasas ascendentes, estrellas, niebla y reflejos de luz animados. Se detiene con la preferencia de movimiento reducido.', 'Versión estática con fuego ámbar, brasas, estrellas y niebla.')
(ROOT / 'assets/night-watch-static.svg').write_text(static, encoding='utf-8')
print(f'Generated {len(svg.encode()):,} byte SVG from {len(ASCII.splitlines())} original ASCII rows.')
