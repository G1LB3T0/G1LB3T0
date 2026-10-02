"""Generate the small, self-contained typewriter line used by the profile.

Run from the repository root: python scripts/generate-typography.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = ('Backend', 'APIs', 'Integraciones')

for theme, ink, accent in (
    ('light', '#424a53', '#238636'),
    ('dark', '#adbac7', '#3fb950'),
):
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="40" viewBox="0 0 400 40" role="img" aria-labelledby="title">
<title id="title">Backend · APIs · Integraciones</title>
<style>
  .cycling {{ display:none; }}
  .slot {{ opacity:0; animation:slot 12s linear infinite; }}
  .reveal {{ width:0; animation:reveal 12s infinite; }}
  .cursor-position {{ animation:cursor-position 12s infinite; }}
  .cursor {{ animation:blink 1s steps(1,end) infinite; }}
  @keyframes slot {{ 0%,33.32% {{ opacity:1; }} 33.33%,100% {{ opacity:0; }} }}
  @keyframes reveal {{
    0% {{ width:0; animation-timing-function:steps(var(--letters),end); }}
    9%,26% {{ width:var(--word-width); animation-timing-function:steps(var(--letters),end); }}
    31%,100% {{ width:0; }}
  }}
  @keyframes cursor-position {{
    0% {{ transform:translateX(0); animation-timing-function:steps(var(--letters),end); }}
    9%,26% {{ transform:translateX(var(--word-width)); animation-timing-function:steps(var(--letters),end); }}
    31%,100% {{ transform:translateX(0); }}
  }}
  @keyframes blink {{ 0%,49% {{ opacity:1; }} 50%,100% {{ opacity:0; }} }}
  @supports (animation-name:slot) {{
    @media (prefers-reduced-motion:no-preference) {{
      .static-label {{ display:none; }}
      .cycling {{ display:inline; }}
    }}
  }}
  @media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; }} }}
</style>
<g fill="{ink}" font-family="Consolas,ui-monospace,monospace" font-size="19">
<text class="static-label" x="200" y="26" text-anchor="middle" font-size="16">Backend · APIs · Integraciones</text>
<g class="cycling">''']
    for index, word in enumerate(WORDS):
        width = len(word) * 11.4
        left = (400-width)/2
        delay = (0, -8, -4)[index]
        timing = f'animation-delay:{delay}s'
        svg.append(f'''<g class="slot" style="--letters:{len(word)};--word-width:{width:g}px;{timing}">
<defs><clipPath id="word-{index}"><rect class="reveal" x="{left:g}" y="0" height="40" style="{timing}"/></clipPath></defs>
<text x="{left:g}" y="26" textLength="{width:g}" lengthAdjust="spacingAndGlyphs" clip-path="url(#word-{index})">{word}</text>
<g class="cursor-position" style="{timing}"><rect class="cursor" x="{left+3:g}" y="10" width="1.5" height="20" rx=".5" fill="{accent}"/></g>
</g>''')
    svg.append('</g></g></svg>')
    target = ROOT / 'assets' / f'typography-{theme}.svg'
    target.write_text('\n'.join(svg)+'\n', encoding='utf-8')
    print(f'{target.name}: {target.stat().st_size} bytes')
