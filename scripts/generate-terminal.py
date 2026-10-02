"""Generate the terminal typography SVGs with Python's standard library.

python scripts/generate-terminal.py
Outlined JetBrains Mono glyphs and OFL license are bundled in type-data.
The SVGs have no scripts, external fonts or network dependencies.
"""
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'scripts/type-data/glyphs.json').read_text(encoding='utf-8'))
UNITS = DATA['units']
STAGES = (
    ('BACKEND', 'Python / TypeScript / PostgreSQL', '01', 'Backend'),
    ('APIs', 'REST / JSON-RPC / MCP', '02', 'APIs'),
    ('INTEGRACIONES', 'Odoo / FEL / Meta API', '03', 'Integraciones'),
)
CYCLE = 18


def pct(seconds):
    return f'{seconds/CYCLE*100:.4f}%'


def outline(text, x, y, size, color):
    scale = size/UNITS
    content, cursor = [], 0
    for char in text:
        if char != ' ':
            content.append(f'<use href="#g{ord(char)}" transform="translate({cursor:g} 0)"/>')
        cursor += DATA['glyphs'][char]['advance']
    return f'<g fill="{color}" transform="translate({x:g} {y:g}) scale({scale:g} {-scale:g})">{"".join(content)}</g>'


def render(theme, mobile):
    if theme == 'dark':
        bg, border, ink, muted, quiet, accent, shade = '#0d1117', '#30363d', '#e6edf3', '#9aa7b5', '#586574', '#79d994', '#14261d'
    else:
        bg, border, ink, muted, quiet, accent, shade = '#f6f8fa', '#d0d7de', '#18212a', '#52616f', '#6b7785', '#176f3e', '#e2f1e7'
    w, h = (600, 274) if mobile else (1000, 296)
    margin = 30 if mobile else 46
    size = 58 if mobile else 82
    cw = size*.6
    baseline = 146 if mobile else 162
    top = baseline-size*.76
    tech_y = 186 if mobile else 204
    header_size = 19 if mobile else 16
    footer_y = 242 if mobile else 266
    step_width = (w-2*margin)/3
    section_width = step_width-(17 if mobile else 28)
    styles = [f'''
  .motion {{ display:none; }}
  .stage {{ opacity:0; animation:stage {CYCLE}s linear var(--phase) infinite; }}
  .detail {{ animation:detail {CYCLE}s ease-out var(--phase) infinite; }}
  .decode-cursor {{ animation:scan {CYCLE}s steps(1,end) var(--phase) infinite; }}
  .end-cursor {{ animation:end-cursor {CYCLE}s linear var(--phase) infinite; }}
  .blink {{ animation:blink 1.2s steps(1,end) infinite; }}
  .progress {{ transform:scaleX(0); animation:progress {CYCLE}s linear var(--phase) infinite; }}
  @keyframes stage {{ 0%,{pct(5.55)} {{ opacity:1; }} {pct(5.88)},100% {{ opacity:0; }} }}
  @keyframes detail {{ 0%,{pct(.68)} {{ opacity:0; transform:translateY(5px); }} {pct(1.18)},100% {{ opacity:1; transform:translateY(0); }} }}
  @keyframes end-cursor {{ 0%,{pct(1.26)} {{ opacity:0; }} {pct(1.27)},100% {{ opacity:1; }} }}
  @keyframes blink {{ 0%,49.99% {{ opacity:1; }} 50%,100% {{ opacity:0; }} }}
  @keyframes progress {{ 0% {{ transform:scaleX(0); }} {pct(5.8)},100% {{ transform:scaleX(1); }} }}
  @supports (animation-name:stage) {{
    @media (prefers-reduced-motion:no-preference) {{ .motion {{ display:inline; }} .still {{ display:none; }} }}
  }}
  @media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; }} }}
''']
    for word, *_ in STAGES:
        keys = ['0%{opacity:1;transform:translateX(0)}']
        for i in range(len(word)):
            keys.append(f'{pct(.3+i*.062)}{{opacity:1;transform:translateX({i*cw:g}px)}}')
        keys.append(f'{pct(.52+(len(word)-1)*.062)},100%{{opacity:0;transform:translateX({(len(word)-1)*cw:g}px)}}')
        styles.append(f'@keyframes scan-{len(word)}{{{"".join(keys)}}}')
    for state in range(6):
        start, end = state/6*100, (state+1)/6*100
        styles.append(f'.noise-{state}{{opacity:0;animation:noise-{state} .6s steps(1,end) infinite;}} @keyframes noise-{state}{{0%,100%{{opacity:0;}}{start:.5f}%{{opacity:1;}}{end-.001:.5f}%{{opacity:1;}}{end:.5f}%{{opacity:0;}}}}')
    for i in range(13):
        lock = .3 + i*.062
        styles.append(f'''
  .unresolved-{i} {{ animation:unresolved-{i} {CYCLE}s steps(1,end) var(--phase) infinite; }}
  .resolved-{i} {{ animation:resolved-{i} {CYCLE}s linear var(--phase) infinite; }}
  @keyframes unresolved-{i} {{ 0% {{ opacity:1; }} {pct(lock)},100% {{ opacity:0; }} }}
  @keyframes resolved-{i} {{
    0%,{pct(lock-.001)} {{ opacity:0; transform:translateY(3px); color:{accent}; }}
    {pct(lock)} {{ opacity:1; transform:translateY(3px); color:{accent}; }}
    {pct(lock+.16)} {{ transform:translateY(0); color:{accent}; }}
    {pct(lock+.38)},100% {{ opacity:1; transform:translateY(0); color:{ink}; }}
  }}''')
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">G1LB3T0: Backend, APIs e Integraciones</title>
<desc id="desc">Los caracteres se descifran hasta mostrar cada especialidad y sus tecnologías. El ciclo dura 18 segundos. Con movimiento reducido se muestran las tres especialidades sin animación.</desc>
<defs>''']
    for char, g in DATA['glyphs'].items():
        if g['d']:
            out.append(f'<path id="g{ord(char)}" d="{g["d"]}"/>')
    out.append(f'</defs><style>{"".join(styles)}</style>')
    out += [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{bg}" stroke="{border}"/>',
            f'<path d="M1 52H{w-1}" stroke="{border}"/>',
            outline('>_',margin,34,header_size,accent),
            outline('G1LB3T0',margin+38,34,header_size,ink),
            outline('/ software engineer',margin+38+header_size*.6*9,34,header_size,muted)]
    if not mobile:
        out.append(outline('PROFILE',w-margin-7*9.6,34,16,quiet))
    for i, (_, _, number, label) in enumerate(STAGES):
        x = margin+i*step_width
        out.append(outline(number,x,footer_y,16 if mobile else 14,quiet))
        out.append(outline(label,x+(28 if mobile else 30),footer_y,18 if mobile else 16,muted))
        out.append(f'<path d="M{x:g} {footer_y+12}h{section_width:g}" stroke="{border}" stroke-width="2"/>')
    out.append('<g class="still">')
    out.append(outline('BACKEND / APIs',margin,116 if mobile else 132,42 if mobile else 56,ink))
    out.append(outline('INTEGRACIONES',margin,169 if mobile else 191,42 if mobile else 56,accent))
    out.append('</g><g class="motion">')
    rng = random.Random(127223507)
    for phase, (word, tech, number, label) in enumerate(STAGES):
        delay = (0, -12, -6)[phase]
        length = len(word)
        travel = (length-1)*cw
        out.append(f'<g class="stage" data-word="{word}" style="--phase:{delay}s;--jumps:{length-1};--travel:{travel:g}px">')
        out.append(outline(f'[{number}]',w-margin-4*header_size*.6,87 if mobile else 96,header_size,quiet))
        out.append(outline('FOCUS',margin,85 if mobile else 95,14 if mobile else 12,muted))
        out.append(f'<g transform="translate({margin-4} {top-5:g})"><g class="decode-cursor" style="animation-name:scan-{length}"><rect width="{cw+8:g}" height="{size*.86:g}" rx="2" fill="{shade}"/><path d="M0 10V0H10M{cw-2:g} 0h10v10M0 {size*.86-10:g}v10h10M{cw-2:g} {size*.86:g}h10v-10" stroke="{accent}" stroke-width="1.3" fill="none"/></g></g>')
        for i, char in enumerate(word):
            x = margin+i*cw
            out.append(f'<g class="unresolved-{i}">')
            for state in range(6):
                noise = rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ023456789')
                out.append(f'<g class="noise-{state}">{outline(noise,x,baseline,size,quiet)}</g>')
            out.append('</g>')
            out.append(f'<g class="resolved-{i}">{outline(char,x,baseline,size,"currentColor")}</g>')
        out.append(f'<g class="end-cursor"><rect class="blink" x="{margin+length*cw+9:g}" y="{baseline-7}" width="{cw*.58:g}" height="5" fill="{accent}"/></g>')
        out.append(f'<g class="detail">{outline(tech,margin,tech_y,22 if mobile else 20,muted)}</g>')
        x = margin+phase*step_width
        out.append(outline(number,x,footer_y,16 if mobile else 14,accent))
        out.append(outline(label,x+(28 if mobile else 30),footer_y,18 if mobile else 16,accent))
        out.append(f'<g transform="translate({x:g} {footer_y+12})"><rect class="progress" width="{section_width:g}" height="2" fill="{accent}"/></g></g>')
    out.append('</g></svg>')
    suffix = '-mobile' if mobile else ''
    target = ROOT/'assets'/f'typography-{theme}{suffix}.svg'
    target.write_text('\n'.join(out)+'\n', encoding='utf-8')
    print(f'{target.name}: {target.stat().st_size:,} bytes')


for theme in ('dark','light'):
    for mobile in (False,True):
        render(theme,mobile)
