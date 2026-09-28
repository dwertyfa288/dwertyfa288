"""Generate self-contained animated SVG assets for the profile README.

Standard library only. Every asset is a single SVG document driven by CSS
animations (no scripts, no external fonts, no foreignObject), so the files keep
working behind GitHub's image proxy and `prefers-reduced-motion` can still
switch the whole motion layer off while every label stays readable.
"""
from pathlib import Path
from html import escape
import base64
import hashlib
import math
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

W = 1100
VIOLET, MINT, PEACH, PINK, SKY = '#a78bfa', '#5eead4', '#f7b48b', '#f0a8d8', '#7dd3fc'

# One motion language for every asset: entrances, light runs, glows, floaters.
STYLE = '''
text{font-family:'Segoe UI',system-ui,-apple-system,Arial,sans-serif}
.mono{font-family:Consolas,'Cascadia Mono','Courier New',monospace}
.pivot{transform-box:view-box;transform-origin:0 0}
.fx{transform-box:fill-box;transform-origin:center}
.fxl{transform-box:fill-box;transform-origin:left center}

@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes breathe{0%,100%{opacity:.4;transform:scale(1)}50%{opacity:1;transform:scale(1.06)}}
@keyframes driftA{0%,100%{transform:translate(0,0)}35%{transform:translate(148px,-44px)}70%{transform:translate(-58px,62px)}}
@keyframes driftB{0%,100%{transform:translate(0,0)}50%{transform:translate(-136px,70px)}}
@keyframes sheen{0%{transform:translateX(0);opacity:0}12%{opacity:.9}58%{opacity:.5}100%{transform:translateX(1780px);opacity:0}}
@keyframes ripple{0%{transform:scale(.5);opacity:0}14%{opacity:.55}100%{transform:scale(1.75);opacity:0}}
@keyframes dash{to{stroke-dashoffset:-1000}}
@keyframes flow{to{stroke-dashoffset:-240}}
@keyframes eq{0%,100%{transform:scaleY(.28);opacity:.55}50%{transform:scaleY(1);opacity:1}}
@keyframes twinkle{0%,100%{opacity:.14;transform:scale(.55)}50%{opacity:1;transform:scale(1.3)}}
@keyframes blink{0%,44%{opacity:1}50%,100%{opacity:0}}
@keyframes glowPulse{0%,100%{opacity:.22}50%{opacity:.9}}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes bar{from{transform:scaleX(0);opacity:0}12%{opacity:1}to{transform:scaleX(1);opacity:1}}
@keyframes load{0%{transform:scaleX(0);opacity:.25}68%{transform:scaleX(1);opacity:1}84%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}
@keyframes badge{0%,100%{stroke:#2c3247}50%{stroke:#6b5f95}}

.rise{animation:rise 1s cubic-bezier(.19,1,.22,1) both}
.spin{animation:spin 26s linear infinite}
.spin-fast{animation:spin 16s linear infinite}
.spin-rev{animation:spin 34s linear infinite reverse}
.breathe{animation:breathe 4.6s ease-in-out infinite}
.drift-a{animation:driftA 19s ease-in-out infinite}
.drift-b{animation:driftB 23s ease-in-out infinite}
.sheen{opacity:0;animation:sheen 11s cubic-bezier(.4,0,.2,1) infinite}
.ripple{animation:ripple 4.4s cubic-bezier(.2,.6,.3,1) infinite}
.dash{stroke-dasharray:150 850;animation:dash 13s linear infinite}
.flow{stroke-dasharray:24 216;animation:flow 3.4s linear infinite}
.eq{animation:eq 1.9s cubic-bezier(.4,0,.2,1) infinite}
.twinkle{animation:twinkle 4.2s ease-in-out infinite}
.blink{animation:blink 1.1s steps(1,end) infinite}
.glow-pulse{animation:glowPulse 4s ease-in-out infinite}
.floaty{animation:floaty 6s ease-in-out infinite}
.bar{animation:bar 1.5s cubic-bezier(.19,1,.22,1) both}
.load{animation:load 4.2s cubic-bezier(.4,0,.2,1) infinite}
.badge{animation:badge 6s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none !important}}
'''


def svg(name, height, body, title, accent=VIOLET, second=MINT, extra_defs='', radius=22):
    """Wrap panel content into one animated, self-contained document."""
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-labelledby="asset-title">
<title id="asset-title">{escape(title)}</title>
<defs>
 <clipPath id="panel-clip"><rect width="{W}" height="{height}" rx="{radius}"/></clipPath>
 <linearGradient id="surface" x1="0" y1="0" x2=".85" y2="1">
  <stop offset="0" stop-color="#161c2e"/><stop offset=".52" stop-color="#0d1220"/><stop offset="1" stop-color="#070a11"/>
 </linearGradient>
 <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{second}"/>
 </linearGradient>
 <linearGradient id="rim" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{accent}"/><stop offset=".5" stop-color="{second}"/><stop offset="1" stop-color="{accent}"/>
 </linearGradient>
 <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset=".5" stop-color="#ffffff" stop-opacity=".12"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
 </linearGradient>
 <linearGradient id="sheen-soft" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
  <stop offset=".5" stop-color="{accent}" stop-opacity=".3"/>
  <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
 </linearGradient>
 <radialGradient id="haloA" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="{accent}" stop-opacity=".55"/>
  <stop offset=".55" stop-color="{accent}" stop-opacity=".15"/>
  <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
 </radialGradient>
 <radialGradient id="haloB" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="{second}" stop-opacity=".45"/>
  <stop offset=".55" stop-color="{second}" stop-opacity=".12"/>
  <stop offset="1" stop-color="{second}" stop-opacity="0"/>
 </radialGradient>
 <radialGradient id="vignette" cx=".5" cy=".42" r=".75">
  <stop offset=".4" stop-color="#03050a" stop-opacity="0"/>
  <stop offset="1" stop-color="#03050a" stop-opacity=".72"/>
 </radialGradient>
 <filter id="glow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="6"/></filter>
 {extra_defs}
</defs>
<style>{STYLE}</style>
{body}
</svg>'''
    (ASSETS / name).write_text(document, encoding='utf-8')


def backdrop(height, phase=0.0, grid=True, radius=22):
    """Layered background, clipped to the panel: grid, nebulae, dust, sweep."""
    grid_layer = ''
    if grid:
        columns = ''.join(f'<path d="M{x} 0V{height}"/>' for x in range(44, W, 44))
        rows = ''.join(f'<path d="M0 {y}H{W}"/>' for y in range(44, height, 44))
        grid_layer = f'<g fill="none" stroke="#cfd6ff" stroke-opacity=".05">{columns}{rows}</g>'
    dust = ''.join(
        f'<circle class="fx twinkle" style="animation-delay:-{(i * 0.47 + phase) % 4.2:.2f}s" '
        f'cx="{70 + (i * 137) % (W - 140)}" cy="{26 + (i * 89) % (height - 52)}" '
        f'r="{1.1 if i % 3 else 1.8}" fill="#e4ddff" opacity=".25"/>' for i in range(22))
    return f'''
<rect width="{W}" height="{height}" rx="{radius}" fill="url(#surface)"/>
<g clip-path="url(#panel-clip)">
{grid_layer}
<g style="mix-blend-mode:screen">
 <ellipse class="drift-a" style="animation-delay:-{phase:.1f}s" cx="250" cy="{height * .26:.0f}" rx="330" ry="240" fill="url(#haloA)"/>
 <ellipse class="drift-b" style="animation-delay:-{phase * 1.6:.1f}s" cx="880" cy="{height * .76:.0f}" rx="310" ry="230" fill="url(#haloB)"/>
</g>
{dust}
<g transform="skewX(-16)"><g class="sheen" style="animation-delay:-{phase + 2.4:.1f}s">
 <rect x="-300" y="-70" width="300" height="{height + 140}" fill="url(#sheen)"/></g></g>
</g>
<rect width="{W}" height="{height}" rx="{radius}" fill="url(#vignette)"/>'''


def frame(height, accent, second, radius=22, phase=0.0):
    """Static gradient rim, one travelling light segment, soft inner highlight."""
    return f'''
<rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="{radius}" fill="none" stroke="url(#rim)" stroke-opacity=".2" stroke-width="1.4"/>
<rect class="dash" style="animation-delay:-{phase:.1f}s" x="1" y="1" width="{W - 2}" height="{height - 2}" rx="{radius}" pathLength="1000" fill="none" stroke="url(#rim)" stroke-width="1.7" stroke-linecap="round"/>
<rect x="{radius + 26}" y="1.6" width="{W - (radius + 26) * 2}" height="1.3" rx=".65" fill="url(#rim)" opacity=".5"/>'''


def section(filename, number, title, caption, accent, second):
    """Section divider: index badge, heading, a rule drawing itself open."""
    svg(filename, 104, f'''
<g clip-path="url(#panel-clip)">
<ellipse class="drift-a" cx="170" cy="50" rx="290" ry="110" fill="url(#haloA)" opacity=".45"/>
<ellipse class="drift-b" cx="900" cy="72" rx="270" ry="100" fill="url(#haloB)" opacity=".4"/>
<g transform="skewX(-16)"><g class="sheen" style="animation-delay:-3s">
 <rect x="-300" y="-70" width="300" height="244" fill="url(#sheen)"/></g></g>
</g>
<g class="rise" style="animation-delay:-.1s">
 <rect x="40" y="24" width="54" height="54" rx="15" fill="#111726" stroke="url(#accent)" stroke-opacity=".55"/>
 <rect x="42" y="26" width="50" height="1.4" rx=".7" fill="url(#accent)" opacity=".7"/>
 <text x="67" y="60" text-anchor="middle" fill="url(#accent)" font-size="22" font-weight="700" class="mono">{number}</text>
</g>
<text class="rise" style="animation-delay:-.2s" x="114" y="62" fill="#eef0fb" font-size="34" font-weight="600">{title}</text>
<g class="rise" style="animation-delay:-.34s">
 <rect class="fxl bar" x="116" y="76" width="250" height="2.4" rx="1.2" fill="url(#accent)"/>
 <path d="M392 77.2H{W - 40}" stroke="#dfe6ff" stroke-opacity=".1"/>
 <path class="flow" d="M392 77.2H{W - 40}" stroke="url(#accent)" stroke-width="2.4" stroke-linecap="round"/>
</g>
<text class="rise mono" style="animation-delay:-.42s" x="{W - 40}" y="46" text-anchor="end" fill="#7c88a3" font-size="13" letter-spacing="2">{caption}</text>
''', f'{number} — {title}. Раздел: {caption}', accent, second)


# --- icon art: every piece is drawn around its own origin so rotations pivot ---

def art_voice(color):
    bars = ''
    for i in range(15):
        level = 20 + 56 * abs(math.sin(i * 0.85 + 0.4))
        bars += (f'<rect class="fx eq" style="animation-delay:-{i * 0.12:.2f}s" x="{-105 + i * 15}" y="{-level / 2:.0f}" '
                 f'width="7" height="{level:.0f}" rx="3.5" fill="{color}" opacity="{0.4 + (i % 3) * 0.2:.2f}"/>')
    return f'<ellipse rx="135" ry="58" fill="url(#haloA)"/>{bars}'


def art_telegram(color):
    return f'''<ellipse rx="135" ry="58" fill="url(#haloA)"/>
<path d="M-112 50C-74-16 6-62 92-24" fill="none" stroke="{color}" stroke-opacity=".28" stroke-width="1.4" stroke-dasharray="8 12"/>
<path class="flow" d="M-112 50C-74-16 6-62 92-24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
<g class="floaty">
 <path d="M6 2 74-32 44 32 30 12 6 20Z" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
 <path d="M30 12 74-32" fill="none" stroke="{color}" stroke-opacity=".45" stroke-width="1.4"/>
 <circle class="fx glow-pulse" cx="74" cy="-32" r="5" fill="{color}" filter="url(#glow)"/>
</g>'''


def art_building(color):
    towers, windows, roof = '', '', []
    for index, (x, top) in enumerate([(-104, 56), (-68, 44), (-32, 62), (4, 34), (40, 48)]):
        towers += f'<path d="M{x} 60V{60 - top}l30-16V60" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
        roof.append(f'M{x} {60 - top}l30-16')
        first = 68 - top + 6
        for row in range(4):
            for col in range(2):
                y = first + row * 14
                if y + 7 > 54 or (index + row + col) % 3:
                    continue
                delay = (index * 5 + row * 2 + col) % 11 * 0.33
                windows += (f'<rect class="blink" style="animation-delay:-{delay:.2f}s" x="{x + 8 + col * 14}" y="{y}" '
                            f'width="5" height="7" rx="1" fill="{color}" opacity=".85"/>')
    return f'''<ellipse rx="135" ry="58" fill="url(#haloA)"/>
<g fill="none" stroke="{color}" stroke-linejoin="round">
<path d="M-118 60h150" stroke-width="2"/>
{towers}</g>
<g>{windows}</g>
<path class="flow" d="{' '.join(roof)}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M-118 60h150" stroke="{color}" stroke-opacity=".35" stroke-width="1"/>'''


def art_shield(color):
    return f'''<ellipse rx="130" ry="62" fill="url(#haloA)"/>
<path d="M0-52 48-34v34c0 23-23 42-48 54-25-12-48-31-48-54v-34Z" fill="#120f22" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
<path class="flow" d="M-32-34v34c0 17 17 34 32 43 15-9 32-26 32-43v-34" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
<g class="floaty">
 <rect x="-14" y="8" width="28" height="22" rx="6" fill="{color}" opacity=".92"/>
 <path d="M-8 8V-2a8 8 0 0 1 16 0v10" fill="none" stroke="{color}" stroke-width="2.8"/>
 <circle cy="17" r="2.6" fill="#120f22"/><path d="M0 18v6" stroke="#120f22" stroke-width="2"/>
</g>'''


def art_film(color):
    holes = ''.join(f'<rect x="{-84 + i * 22}" y="-42" width="9" height="7" rx="1.5" fill="{color}" opacity=".35"/>' for i in range(8))
    holes += ''.join(f'<rect x="{-84 + i * 22}" y="35" width="9" height="7" rx="1.5" fill="{color}" opacity=".35"/>' for i in range(8))
    return f'''<ellipse rx="140" ry="56" fill="url(#haloA)"/>
<rect x="-96" y="-48" width="192" height="96" rx="10" fill="#0d1120" stroke="{color}" stroke-width="1.8"/>
<g clip-path="url(#film-clip)">
<path d="M-96-22h192M-96 22h192" stroke="{color}" stroke-opacity=".35"/>
{holes}
<g transform="skewX(-14)"><g class="sheen" style="animation-delay:-3.4s">
<rect x="-140" y="-48" width="90" height="96" fill="url(#sheen-soft)"/></g></g>
</g>
<circle class="fx ripple" r="30" fill="none" stroke="{color}" stroke-width="1.3"/>
<path class="fx glow-pulse" d="M-9-11 15 0-9 11Z" fill="{color}"/>'''


def art_spark(color):
    return f'''<ellipse rx="128" ry="60" fill="url(#haloA)"/>
<g class="pivot spin-fast" opacity=".4">
 <circle r="78" fill="none" stroke="{color}" stroke-dasharray="3 14" stroke-width="1.4"/>
</g>
<g class="pivot spin-rev" opacity=".28">
 <circle r="58" fill="none" stroke="{color}" stroke-dasharray="26 22" stroke-width="1"/>
</g>
<circle class="fx ripple" r="26" fill="none" stroke="{color}" stroke-width="1.4"/>
<circle class="fx ripple" style="animation-delay:-2.2s" r="26" fill="none" stroke="{color}" stroke-width="1"/>
<path class="fx glow-pulse" d="M0-48 13-13 48 0 13 13 0 48-13 13-48 0-13-13Z" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
<path d="M0-28 8-8 28 0 8 8 0 28-8 8-28 0-8-8Z" fill="{color}" opacity=".85"/>'''


def art_web(color):
    return f'''<ellipse rx="140" ry="56" fill="url(#haloA)"/>
<rect x="-100" y="-54" width="200" height="108" rx="12" fill="#111524" stroke="{color}" stroke-width="1.8"/>
<path d="M-100-28h200" stroke="{color}" stroke-opacity=".4"/>
<circle cx="-86" cy="-41" r="3.4" fill="{color}"/><circle cx="-74" cy="-41" r="3.4" fill="{color}" opacity=".6"/><circle cx="-62" cy="-41" r="3.4" fill="{color}" opacity=".3"/>
<rect x="-40" y="-48" width="52" height="15" rx="4" fill="{color}" opacity=".2"/>
<path d="m-70-2-16 14 16 14m60-28 16 14-16 14m-22-32-14 44" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<rect class="blink" x="18" y="8" width="3" height="16" rx="1.5" fill="{color}"/>
<g clip-path="url(#web-clip)"><g transform="skewX(-14)"><g class="sheen" style="animation-delay:-6.8s">
<rect x="-160" y="-54" width="90" height="108" fill="url(#sheen-soft)"/></g></g></g>'''


def art_proxy(color):
    return f'''<ellipse rx="140" ry="54" fill="url(#haloA)"/>
<g class="pivot spin-slow" opacity=".45"><circle r="98" fill="none" stroke="{color}" stroke-dasharray="2 16"/></g>
<path d="M-64 0H64" stroke="{color}" stroke-opacity=".26" stroke-width="2"/>
<path class="flow" d="M-64 0H64" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>
<g class="fx breathe"><circle r="16" fill="#0f1422" stroke="{color}" stroke-width="1.8"/><circle r="5" fill="{color}"/></g>
<rect x="-112" y="-26" width="44" height="52" rx="9" fill="#141a29" stroke="{color}" stroke-width="1.8"/>
<rect x="68" y="-26" width="44" height="52" rx="9" fill="#141a29" stroke="{color}" stroke-width="1.8"/>
<path d="M-102-8h24m-24 12h24m-24 12h14m120-24h24m-24 12h24m-24 12h14" stroke="{color}" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>'''


def art_ai(color):
    nodes, edges = '', ''
    for index, (x, y) in enumerate([(-64, -42), (64, -42), (-64, 44), (64, 44)]):
        nodes += (f'<circle cx="{x}" cy="{y}" r="7" fill="#111726" stroke="{color}" stroke-width="1.8"/>'
                  f'<circle class="fx twinkle" style="animation-delay:-{index * 0.7:.1f}s" cx="{x}" cy="{y}" r="3" fill="{color}"/>')
    for index, (x, y, nx, ny) in enumerate([(0, 0, -64, -42), (0, 0, 64, -42), (0, 0, -64, 44), (0, 0, 64, 44),
                                            (-64, -42, 64, -42), (-64, 44, 64, 44)]):
        edges += (f'<path class="flow" style="animation-delay:-{index * 0.6:.1f}s" d="M{x} {y}L{nx} {ny}" '
                  f'stroke="{color}" stroke-width="1.6" fill="none" opacity=".85"/>')
    return f'''<ellipse rx="140" ry="58" fill="url(#haloA)"/>
<g opacity=".45" fill="none" stroke="{color}" stroke-width="1"><path d="M-64-42H64M-64 44H64"/></g>
{edges}{nodes}
<circle class="fx breathe" r="22" fill="#0e1320" stroke="{color}" stroke-width="2"/>
<circle class="fx glow-pulse" r="9" fill="{color}"/>'''


def art_cli(color):
    lines = ''.join(f'<path d="M-80{-1 + i * 18}H{20 + (i % 3) * 24}" stroke="{color}" stroke-opacity="{0.65 - i * 0.14:.2f}" stroke-width="3" stroke-linecap="round"/>' for i in range(3))
    return f'''<ellipse rx="140" ry="56" fill="url(#haloA)"/>
<rect x="-100" y="-52" width="200" height="104" rx="11" fill="#0c1018" stroke="{color}" stroke-width="1.8"/>
<path d="M-100-28h200" stroke="{color}" stroke-opacity=".35"/>
<circle cx="-88" cy="-40" r="3.4" fill="{color}" opacity=".8"/><circle cx="-76" cy="-40" r="3.4" fill="{color}" opacity=".45"/>
<text x="-60" y="-35" fill="{color}" font-size="12" class="mono" opacity=".7">~/projects</text>
<path d="m-80-8 10 8-10 8" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
{lines}
<rect class="blink" x="30" y="1" width="3" height="14" rx="1.5" fill="{color}"/>
<rect class="fxl load" x="-80" y="30" width="160" height="5" rx="2.5" fill="url(#accent)"/>'''


ART = {
    'voice': art_voice, 'telegram': art_telegram, 'building': art_building,
    'shield': art_shield, 'film': art_film, 'spark': art_spark, 'web': art_web,
    'proxy': art_proxy, 'ai': art_ai, 'cli': art_cli,
}
CARD_CLIPS = ('<clipPath id="film-clip"><rect x="-96" y="-48" width="192" height="96" rx="10"/></clipPath>'
              '<clipPath id="web-clip"><rect x="-100" y="-54" width="200" height="108" rx="12"/></clipPath>')


def card(filename, number, label, name, description, tags, color, icon, index, total, phase):
    """One project card: copy on the left, animated art on the right."""
    height = 216
    partner = MINT if color != MINT else SKY
    dots = ''.join(
        f'<circle cx="{958 - (total - 1) * 9 + i * 18}" cy="192" r="3.2" fill="{color if i == index else '#39415a'}"'
        + (f' class="fx breathe" style="animation-delay:-{index * 0.4:.1f}s"' if i == index else '')
        + f' opacity="{1 if i == index else 0.7}"/>' for i in range(total))
    svg(filename, height, f'''
{backdrop(height, phase, radius=18)}
<g class="rise" style="animation-delay:-.05s">
 <rect x="1" y="34" width="3.4" height="148" rx="1.7" fill="{color}"/>
 <rect class="load" x="1" y="34" width="3.4" height="148" rx="1.7" fill="{color}" filter="url(#glow)" opacity=".45"/>
</g>
<text class="rise mono" style="animation-delay:-.1s" x="30" y="36" fill="{color}" font-size="12" letter-spacing="1.8">{number} / {label}</text>
<text class="rise" style="animation-delay:-.18s" x="30" y="88" fill="#f2f3fb" font-size="33" font-weight="600">{name}</text>
<text class="rise" style="animation-delay:-.26s" x="30" y="126" fill="#aeb7cb" font-size="19">{description}</text>
<g class="rise" style="animation-delay:-.34s">
 <text x="30" y="176" fill="{color}" font-size="13" class="mono" letter-spacing="1">{tags}</text>
 <path d="M30 190h150" stroke="{color}" stroke-opacity=".3"/>
 <path class="flow" d="M30 190h150" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
</g>
<path class="rise" style="animation-delay:-.3s" d="M820 26v164" stroke="#dfe6ff" stroke-opacity=".09"/>
<g class="rise" style="animation-delay:-.38s">
 <g transform="translate(958 108)"><g class="floaty" style="animation-delay:-{phase:.1f}s">{ART[icon](color)}</g></g>
</g>
<g class="rise" style="animation-delay:-.44s">{dots}</g>
<g class="rise" style="animation-delay:-.5s">
 <path d="M1040 32h16v16m-16 0 16-16" fill="none" stroke="#adb5cb" stroke-width="1.8" stroke-linecap="round"/>
 <circle class="fx glow-pulse" cx="1040" cy="48" r="3" fill="{color}"/>
</g>
{frame(height, color, partner, 18, phase)}
''', f'{name}: {description}', color, partner, CARD_CLIPS, 18)


# --- hero --------------------------------------------------------------------

avatar_bytes = (ASSETS / 'avatar.png').read_bytes()
avatar_mime = 'image/png' if avatar_bytes[:8] == b'\x89PNG\r\n\x1a\n' else 'image/jpeg'
avatar_data = base64.b64encode(avatar_bytes).decode('ascii')

stars = ''.join(
    f'<circle class="fx twinkle" style="animation-delay:-{i * 0.31 % 4.2:.2f}s" cx="{90 + (i * 271) % (W - 180)}" '
    f'cy="{100 + (i * 173) % 330}" r="{1.1 if i % 3 else 1.7}" fill="#e6dfff" opacity=".2"/>' for i in range(46))
floor = ''.join(f'<path d="M{x} 458L{866 + (x - 866) * 0.17:.0f} 320"/>' for x in range(624, 1461, 78))
rings = '<g transform="translate(866 254)">'
for index, (angle, speed, direction) in enumerate([(-34, 22, 'spin'), (26, 32, 'spin-rev'), (84, 40, 'spin-fast')]):
    rings += f'''<g class="{direction}" style="animation-duration:{speed}s"><g transform="rotate({angle})">
 <ellipse rx="168" ry="66" fill="none" stroke="#7d6cae" stroke-opacity=".3"/>
 <ellipse class="flow" rx="168" ry="66" fill="none" stroke="url(#accent)" stroke-width="2.2" style="animation-duration:{4.5 + index * 1.6:.1f}s"/>
 <circle cx="168" cy="0" r="4" fill="{MINT}"/>
 <circle class="fx glow-pulse" cx="168" cy="0" r="8" fill="{MINT}" filter="url(#glow)"/>
</g></g>'''
rings += f'''<ellipse rx="205" ry="152" fill="url(#haloA)" opacity=".45"/>
<g class="pivot spin-slow" opacity=".45"><circle r="106" fill="none" stroke="{VIOLET}" stroke-dasharray="2 15"/></g>
<g class="pivot spin-rev" opacity=".3"><circle r="124" fill="none" stroke="{MINT}" stroke-dasharray="40 30"/></g>
<circle class="fx ripple" r="86" fill="none" stroke="{VIOLET}" stroke-width="1"/>
<circle class="fx ripple" style="animation-delay:-1.5s" r="86" fill="none" stroke="{VIOLET}" stroke-width="1"/>
<circle class="fx ripple" style="animation-delay:-3s" r="86" fill="none" stroke="{MINT}" stroke-width="1"/>
</g>'''

svg('hero.svg', 500, f'''
{backdrop(500, grid=False, radius=24)}
<g clip-path="url(#panel-clip)"><g fill="none" stroke="#cfd6ff" stroke-width="1" opacity=".8">{floor}</g>
<path d="M600 458H{W}" stroke="#cfd6ff" stroke-opacity=".07"/></g>
{stars}
<path d="M0 64H{W}" stroke="#dfe6ff" stroke-opacity=".07"/>
<circle cx="43" cy="34" r="5" fill="{PEACH}"/><circle cx="62" cy="34" r="5" fill="#ffd479"/><circle cx="81" cy="34" r="5" fill="{MINT}"/>
<circle class="fx glow-pulse" cx="43" cy="34" r="8" fill="none" stroke="{PEACH}" stroke-width="1.2"/>
<text class="rise mono" style="animation-delay:-.15s" x="104" y="40" fill="#b6c0d6" font-size="14">dwertyfa / personal space</text>
<text class="rise mono" style="animation-delay:-.25s" x="{W - 42}" y="40" text-anchor="end" fill="{MINT}" font-size="13">CODE · CREATE · CONNECT</text>
<text class="rise mono" style="animation-delay:-.3s" x="46" y="106" fill="url(#accent)" font-size="14" letter-spacing="3.6">FULL-STACK · VOICE · INTEGRATIONS</text>
<text class="rise" style="animation-delay:-.42s;filter:drop-shadow(0 8px 34px rgba(167,139,250,.4))" x="40" y="222" fill="#f5f2ff" font-size="100" font-weight="700" letter-spacing="-5">dwertyfa<tspan fill="{MINT}">.</tspan></text>
<text class="rise" style="animation-delay:-.54s" x="46" y="278" fill="#d6dae8" font-size="27">От идеи — до живого продукта.</text>
<text class="rise" style="animation-delay:-.62s" x="47" y="314" fill="#8d97ae" font-size="19">Сайты с характером. Плагины с пользой.</text>
<g class="rise" style="animation-delay:-.74s">
 <rect x="40" y="344" width="566" height="110" rx="14" fill="#080c15" fill-opacity=".84" stroke="#2a3350"/>
 <path d="M40 376h566" stroke="#2a3350"/>
 <circle cx="62" cy="360" r="4" fill="{VIOLET}"/><circle cx="78" cy="360" r="4" fill="{MINT}"/>
 <text class="mono" x="96" y="365" fill="#7e8aa6" font-size="12">~/dwertyfa — zsh</text>
 <text class="mono" x="62" y="404" fill="{MINT}" font-size="14">$</text>
 <text class="mono" x="78" y="404" fill="#dfe4f2" font-size="14">astra listen --telegram</text>
 <text class="mono" x="62" y="428" fill="#6f7c99" font-size="13">голос → текст · текст → голос</text>
 <text class="mono" x="62" y="448" fill="{MINT}" font-size="14">$</text>
 <text class="mono" x="78" y="448" fill="#dfe4f2" font-size="14">go test ./...</text>
 <rect class="blink" x="196" y="437" width="8" height="15" rx="1" fill="{MINT}"/>
 <g clip-path="url(#term-clip)"><g transform="skewX(-14)"><g class="sheen" style="animation-delay:-4.6s">
 <rect x="-160" y="344" width="110" height="110" fill="url(#sheen-soft)"/></g></g></g>
</g>
<g class="rise" style="animation-delay:-.86s">
 <circle cx="52" cy="484" r="4" fill="{MINT}"/>
 <circle class="fx glow-pulse" cx="52" cy="484" r="8" fill="{MINT}" filter="url(#glow)"/>
 <text class="mono" x="68" y="490" fill="#a9b3c8" font-size="15">TYPESCRIPT · REACT · NEXT.JS · GO · RUST · TAURI · PYTHON</text>
</g>
{rings}
<circle cx="866" cy="254" r="62" fill="#111625" stroke="#7a6aa0"/>
<defs><clipPath id="avatar-clip"><circle cx="866" cy="254" r="59"/></clipPath></defs>
<image x="807" y="195" width="118" height="118" href="data:{avatar_mime};base64,{avatar_data}" xlink:href="data:{avatar_mime};base64,{avatar_data}" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
<circle class="fx breathe" cx="866" cy="254" r="63" fill="none" stroke="{VIOLET}" stroke-width="2.4" filter="url(#glow)"/>
<circle cx="866" cy="254" r="61" fill="none" stroke="{VIOLET}" stroke-opacity=".7"/>
<text class="rise mono" style="animation-delay:-.94s" x="866" y="428" text-anchor="middle" fill="#7f88a2" font-size="12" letter-spacing="4">IDEAS IN ORBIT</text>
{frame(500, VIOLET, MINT, 24)}
''', 'dwertyfa — full-stack, голосовые интерфейсы и интеграции. От идеи до живого продукта.', VIOLET, MINT,
    '<clipPath id="term-clip"><rect x="40" y="344" width="566" height="110" rx="14"/></clipPath>', 24)

# --- about -------------------------------------------------------------------

DIRECTIONS = [
    (40, MINT, '◈', 'Веб и интерфейсы', 'Сайты с характером,', '3D и анимации.'),
    (382, VIOLET, '◉', 'Голос и диалог', 'Плагины для Astra', 'и управление Telegram.'),
    (724, PEACH, '◈', 'Интеграции', 'Связываю сервисы', 'в удобные инструменты.'),
]
blocks = ''
for index, (x, color, glyph, title, line1, line2) in enumerate(DIRECTIONS):
    blocks += f'''<g class="rise" style="animation-delay:-{0.34 + index * 0.08:.2f}s">
<rect x="{x}" y="180" width="336" height="152" rx="14" fill="#0f1522" fill-opacity=".8" stroke="#232b3e"/>
<rect x="{x + 1.2}" y="181.2" width="333" height="1.2" rx=".6" fill="{color}" opacity=".4"/>
<g class="floaty" style="animation-delay:-{index * 0.9:.1f}s">
 <circle cx="{x + 32}" cy="212" r="15" fill="none" stroke="{color}" stroke-opacity=".45"/>
 <circle class="fx glow-pulse" cx="{x + 32}" cy="212" r="15" fill="none" stroke="{color}" stroke-width="1.6"/>
 <text x="{x + 32}" y="218" text-anchor="middle" fill="{color}" font-size="15">{glyph}</text></g>
<text x="{x + 62}" y="220" fill="{color}" font-size="22" font-weight="600">{title}</text>
<text x="{x + 24}" y="266" fill="#b6bfd2" font-size="21">{line1}</text>
<text x="{x + 24}" y="296" fill="#b6bfd2" font-size="21">{line2}</text>
<path d="M{x + 24} 314h70" stroke="{color}" stroke-opacity=".3"/>
<path class="flow" d="M{x + 24} 314h70" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
</g>'''

chips, x = '', 40
for index, label in enumerate(['TypeScript', 'React', 'Next.js', 'Go', 'Rust', 'Tauri', 'Python']):
    width = int(34 + len(label) * 13.6)
    chips += (f'<g class="rise" style="animation-delay:-{0.58 + index * 0.06:.2f}s">'
              f'<rect class="badge" x="{x}" y="388" width="{width}" height="44" rx="11" fill="#151a2b" stroke="#37344f"/>'
              f'<rect x="{x + 6}" y="389.2" width="{width - 12}" height="1.2" rx=".6" fill="{VIOLET}" opacity=".35"/>'
              f'<text x="{x + width / 2}" y="417" text-anchor="middle" fill="#e2dbf8" font-size="21" class="mono">{label}</text></g>')
    x += width + 14

wave = ''.join(
    f'<rect class="fx eq" style="animation-delay:-{i * 0.11:.2f}s" x="{792 + i * 11}" y="{490 - (10 + 30 * abs(math.sin(i * 0.62))) / 2:.0f}" '
    f'width="4.5" height="{10 + 30 * abs(math.sin(i * 0.62)):.0f}" rx="2.2" fill="{VIOLET}" opacity="{0.35 + (i % 4) * 0.15:.2f}"/>' for i in range(22))

svg('about.svg', 540, f'''
{backdrop(540, phase=0.8, radius=22)}
<text class="rise mono" style="animation-delay:-.05s" x="40" y="46" fill="{VIOLET}" font-size="13" letter-spacing="3">ABOUT / BEHIND THE CODE</text>
<text class="rise mono" style="animation-delay:-.12s" x="{W - 40}" y="46" text-anchor="end" fill="#4b5670" font-size="13" letter-spacing="2">dwertyfa</text>
<text class="rise" style="animation-delay:-.18s" x="40" y="110" fill="#f4f1ff" font-size="46" font-weight="600">Привет, я dwertyfa<tspan fill="{MINT}">.</tspan></text>
<text class="rise" style="animation-delay:-.26s" x="40" y="152" fill="#b7c0d3" font-size="23">Создаю сайты, плагины и интеграции, которыми удобно пользоваться.</text>
<rect class="fxl bar" x="40" y="166" width="210" height="2.4" rx="1.2" fill="url(#accent)"/>
{blocks}
<text class="rise mono" style="animation-delay:-.52s" x="40" y="370" fill="#8f9ab3" font-size="14" letter-spacing="2">МОЙ СТЕК</text>
{chips}
<g class="rise" style="animation-delay:-1s">
 <rect x="40" y="452" width="486" height="76" rx="14" fill="#0f1522" fill-opacity=".82" stroke="#232b3e"/>
 <g transform="translate(88 490)">
  <g class="pivot spin-slow">
   <path d="M0-22 19 11-19 11Z" fill="none" stroke="{MINT}" stroke-width="2" stroke-linejoin="round"/>
   <path class="flow" d="M0-22 19 11-19 11Z" stroke-width="2.4" fill="none"/>
  </g>
 </g>
 <text x="126" y="486" fill="#9aa5bd" font-size="19">Графика</text>
 <text x="126" y="514" fill="{MINT}" font-size="21" font-weight="600">Three.js</text>
 <path d="M300 470v42" stroke="#dfe6ff" stroke-opacity=".08"/>
 <text x="330" y="486" fill="#9aa5bd" font-size="19">Стек</text>
 <text x="330" y="514" fill="#dfe4f2" font-size="21" font-weight="600" class="mono">14+ проектов</text>
</g>
<g class="rise" style="animation-delay:-1.08s">
 <rect x="556" y="452" width="504" height="76" rx="14" fill="#0f1522" fill-opacity=".82" stroke="#232b3e"/>
 <text x="578" y="486" fill="#9aa5bd" font-size="19">Голосовые плагины</text>
 <text x="578" y="510" fill="{VIOLET}" font-size="19" font-weight="600" class="mono">Astra Plugin SDK</text>
 <path d="M770 468v44" stroke="#dfe6ff" stroke-opacity=".07"/>
 {wave}
</g>
{frame(540, VIOLET, MINT, 22, 0.8)}
''', 'Привет, я dwertyfa. Создаю сайты, плагины и интеграции. Веб: 3D и анимации. Голос: Astra и Telegram. '
    'Стек: TypeScript, React, Next.js, Go, Rust, Tauri, Python. Также Three.js и Astra Plugin SDK.', VIOLET, MINT, '', 22)

# --- footer ------------------------------------------------------------------

svg('footer.svg', 176, f'''
{backdrop(176, phase=1.6, radius=20)}
<text class="rise" style="animation-delay:-.05s" x="40" y="64" fill="#f1f2fa" font-size="31" font-weight="600">Есть идея? Дадим ей форму.</text>
<text class="rise" style="animation-delay:-.14s" x="40" y="98" fill="#98a3ba" font-size="19">Обсудим задачу, придумаем решение и соберём рабочий продукт.</text>
<text class="rise mono" style="animation-delay:-.22s" x="40" y="138" fill="{MINT}" font-size="15">t.me/dwertyfa</text>
<g class="rise" style="animation-delay:-.3s">
 <rect x="762" y="42" width="298" height="62" rx="31" fill="#101728" stroke="url(#accent)" stroke-width="1.6"/>
 <rect class="fx breathe" x="762" y="42" width="298" height="62" rx="31" fill="none" stroke="{MINT}" stroke-width="1.4" filter="url(#glow)"/>
 <g clip-path="url(#pill-clip)"><g transform="skewX(-14)"><g class="sheen" style="animation-delay:-7.2s">
 <rect x="700" y="42" width="110" height="62" fill="url(#sheen-soft)"/></g></g></g>
 <circle class="fx glow-pulse" cx="800" cy="73" r="6" fill="{MINT}"/>
 <text x="822" y="81" fill="#e7f7f1" font-size="20" font-weight="600">Написать в Telegram</text>
</g>
<path d="M40 154H1060" stroke="#dfe6ff" stroke-opacity=".06"/>
<path d="M40 154H430l24-22 28 38 30-62 32 76 28-46 20 16h458" fill="none" stroke="#3a3f5c" stroke-width="1.4"/>
<path class="flow" d="M40 154H430l24-22 28 38 30-62 32 76 28-46 20 16h458" fill="none" stroke="url(#accent)" stroke-width="2" stroke-linecap="round"/>
<circle cx="1060" cy="154" r="4" fill="{MINT}" filter="url(#glow)"/>
<circle class="fx breathe" cx="1060" cy="154" r="8" fill="none" stroke="{MINT}" stroke-width="1.4"/>
{frame(176, MINT, VIOLET, 20, 1.6)}
''', 'Есть идея? Дадим ей форму. Написать dwertyfa в Telegram: t.me/dwertyfa', MINT, VIOLET,
    '<clipPath id="pill-clip"><rect x="762" y="42" width="298" height="62" rx="31"/></clipPath>', 20)

section('sec-featured.svg', '01', 'Избранное', 'SELECTED WORK', VIOLET, MINT)
section('sec-web.svg', '02', 'Веб-проекты', 'CASE STUDIES', MINT, SKY)
section('sec-org.svg', '03', 'SpherePrime', 'ORGANIZATION', SKY, PINK)

card('telegram.svg', '01', 'VOICE × MESSAGING', 'TG for Astra', 'Telegram, который можно слушать. И отвечать голосом.', 'TYPESCRIPT   /   TELEGRAM   /   ASTRA', MINT, 'telegram', 0, 3, 0.0)
card('interject.svg', '02', 'NATURAL CONVERSATION', 'Astra Interject', 'Продолжение диалога без повторного триггерного слова.', 'TYPESCRIPT   /   AUDIO   /   ASTRA', VIOLET, 'voice', 1, 3, 1.4)
card('portfolio.svg', '03', 'WEB × MOTION', 'dwertyfa / portfolio', 'Интерактивное портфолио с 3D-графикой и анимациями.', 'NEXT.JS   /   REACT   /   THREE.JS', PEACH, 'web', 2, 3, 2.8)

card('nova.svg', '01', 'WEB / ARCHITECTURE', 'Nova Prestige', 'Промо-сайт жилого дома с атмосферой и вниманием к деталям.', 'REAL ESTATE   /   RESPONSIVE   /   MOTION', MINT, 'building', 0, 4, 0.6)
card('roxy.svg', '02', 'WEB / DIGITAL PRODUCT', 'Roxy Boost', 'VPN-продукт: от инфраструктуры до приложения и сайта.', 'FULL-STACK   /   VPN   /   INFRASTRUCTURE', VIOLET, 'shield', 1, 4, 2.0)
card('danek.svg', '03', 'WEB / CREATIVE PORTFOLIO', 'danek montage', 'Портфолио видеомонтажёра, в котором движение задаёт ритм.', 'REACT   /   MOTION UI   /   RESPONSIVE', PEACH, 'film', 2, 4, 3.4)
card('ksusha.svg', '04', 'WEB / EDUCATION', 'Hey Ksusha', 'Лендинг интенсива: выразительная подача, запись и оплата.', 'LANDING PAGE   /   ART DIRECTION   /   PAYMENTS', PINK, 'spark', 3, 4, 4.8)

card('primeproxy.svg', '01', 'SPHEREPRIME / NETWORK', 'PrimeProxy', 'Локальный MTProto-прокси для Telegram через WebSocket.', 'PYTHON   /   MTPROTO   /   WEBSOCKET', MINT, 'proxy', 0, 3, 0.9)
card('primeai.svg', '02', 'SPHEREPRIME / INTELLIGENCE', 'PrimeAI', 'AI-провайдер для Astra с маршрутизацией запросов к моделям.', 'TYPESCRIPT   /   ROUTER API   /   ASTRA', SKY, 'ai', 1, 3, 2.3)
card('primecli.svg', '03', 'SPHEREPRIME / DEVELOPER TOOLS', 'Prime CLI', 'AI-ассистент для кода — прямо в терминале.', 'GO   /   MCP   /   MULTI-MODEL', PEACH, 'cli', 2, 3, 3.7)

print('Generated 16 SVG assets.')


# --- keep the README and the local preview in sync ---------------------------

def version_asset(match):
    """Point every image at a content-hashed copy so GitHub cannot cache it."""
    path = re.sub(r'-[0-9a-f]{12}(?=\.svg$)', '', match.group(1))
    data = (ROOT / path).read_bytes()
    versioned = path.removesuffix('.svg') + f'-{hashlib.sha256(data).hexdigest()[:12]}.svg'
    (ROOT / versioned).write_bytes(data)
    return f'src="{versioned}"'


readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
readme = re.sub(r'src="(\./assets/[^"?]+\.svg)(?:\?[^\"]*)?"', version_asset, readme)
readme_path.write_text(readme, encoding='utf-8')

keep = set(re.findall(r'\./assets/([\w.-]+\.svg)', readme))
for stale in sorted(ASSETS.glob('*.svg')):
    # Canonical files stay as the editable source; only superseded copies go.
    if stale.name not in keep and not re.fullmatch(r'[a-z0-9-]+(?<!-[0-9a-f]{12})\.svg', stale.name):
        stale.unlink()

PREVIEW = '''<!doctype html>
<html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>dwertyfa — GitHub profile preview</title>
<style>
:root{color-scheme:dark}
body{margin:0;background:#0b0e16;color:#e6edf3;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
body::before{content:"";position:fixed;inset:0;background:radial-gradient(900px 520px at 12% -12%,rgba(167,139,250,.2),transparent 62%),radial-gradient(780px 460px at 92% 112%,rgba(94,234,212,.14),transparent 62%);pointer-events:none}
main{position:relative;max-width:1000px;margin:34px auto;padding:32px 28px 44px;border:1px solid #232a3a;border-radius:20px;background:rgba(13,17,28,.74);box-shadow:0 30px 80px rgba(0,0,0,.45)}
img{max-width:100%;height:auto;border-radius:12px}
a{color:#a78bfa;text-decoration:none}a:hover{text-decoration:underline}
h3{font-size:13px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#7f8aa3;margin:46px 0 18px;display:flex;align-items:center;gap:14px}
h3::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,#2a3145,transparent)}
p{margin:16px 0}
@media(max-width:640px){main{margin:0;padding:16px;border:0;border-radius:0}h3{font-size:12px}}
</style>
<main>@@BODY@@</main></html>'''
body = re.sub(r'^###\s*(.+)$', r'<h3>\1</h3>', readme.strip(), flags=re.M)
(ROOT / 'preview.html').write_text(PREVIEW.replace('@@BODY@@', body), encoding='utf-8')

print('README image URLs re-hashed, stale copies removed, preview.html rebuilt.')
