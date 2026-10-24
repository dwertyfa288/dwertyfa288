from .canvas import text, label, delay, window_keyframes
from .theme import PAPER, GREY, DIM, LINE, SIGNAL, INK

ROOM_CYCLE = 9
BOOKING_CYCLE = 8
GATE_CYCLE = 6
PRODUCTS = [('Диван, серый букле', '96%'), ('Торшер, латунь', '91%'), ('Ковёр, шерсть', '88%'), ('Стеллаж, дуб', '84%')]


def appear(name, start, end, cycle):
    return window_keyframes(name, start, end, fade=3, lift=6) + f'.{name}{{animation:{name} {cycle}s cubic-bezier(.2,.8,.2,1) infinite}}'


def room(x, y, w, h, stroke, furnished):
    back = (x + w * .22, y + h * .18, w * .56, h * .5)
    bx, by, bw, bh = back
    shell = (f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="none" stroke="{stroke}"/>'
             f'<path d="M{x} {y}L{bx:.1f} {by:.1f}M{x + w} {y}L{bx + bw:.1f} {by:.1f}M{x} {y + h}L{bx:.1f} {by + bh:.1f}M{x + w} {y + h}L{bx + bw:.1f} {by + bh:.1f}" stroke="{stroke}"/>'
             f'<rect x="{bx + bw * .58:.1f}" y="{by + bh * .14:.1f}" width="{bw * .3:.1f}" height="{bh * .42:.1f}" fill="none" stroke="{stroke}"/>'
             f'<path d="M{bx + bw * .73:.1f} {by + bh * .14:.1f}V{by + bh * .56:.1f}" stroke="{stroke}"/>')
    if not furnished:
        return shell + f'<path d="M{bx + 6:.1f} {by + bh * .3:.1f}l12 10M{bx + bw * .3:.1f} {by + bh * .7:.1f}l9 -7" stroke="{stroke}" stroke-dasharray="2 3"/>'
    floor = by + bh
    return shell + f'''
<ellipse cx="{bx + bw * .4:.1f}" cy="{floor + h * .14:.1f}" rx="{bw * .42:.1f}" ry="{h * .07:.1f}" fill="none" stroke="{SIGNAL}"/>
<path d="M{bx + bw * .08:.1f} {floor - 4:.1f}V{floor - bh * .3:.1f}H{bx + bw * .52:.1f}V{floor - 4:.1f}M{bx + bw * .04:.1f} {floor - bh * .2:.1f}H{bx + bw * .56:.1f}V{floor - 2:.1f}H{bx + bw * .04:.1f}Z" fill="none" stroke="{PAPER}"/>
<path d="M{bx + bw * .66:.1f} {floor - 2:.1f}V{floor - bh * .62:.1f}" stroke="{PAPER}"/><path d="M{bx + bw * .6:.1f} {floor - bh * .62:.1f}H{bx + bw * .72:.1f}L{bx + bw * .69:.1f} {floor - bh * .74:.1f}H{bx + bw * .63:.1f}Z" fill="{SIGNAL}"/>
<rect x="{bx + bw * .14:.1f}" y="{by + bh * .16:.1f}" width="{bw * .26:.1f}" height="{bh * .22:.1f}" fill="none" stroke="{PAPER}"/>
<path d="M{bx + bw * .9:.1f} {floor - 2:.1f}V{floor - bh * .2:.1f}M{bx + bw * .9:.1f} {floor - bh * .2:.1f}l-7 -9M{bx + bw * .9:.1f} {floor - bh * .2:.1f}l6 -11M{bx + bw * .9:.1f} {floor - bh * .26:.1f}l1 -12" stroke="{PAPER}"/>'''


def designer(x, y, w, h):
    px, py, pw, ph = x + 34, y + 16, 178, h - 32
    ix, iy, iw, ih = px + 14, py + 56, pw - 28, 120
    times = '0;.1;.55;.9;1'
    sweep = f'0;0;{iw};{iw};0'
    rows = []
    css = ''
    for index, (name, match) in enumerate(PRODUCTS):
        css += appear(f'pr{index}', 58 + index * 6, 94, ROOM_CYCLE)
        ry = y + 92 + index * 44
        rows.append(f'<g class="pr{index}"><rect x="{x + 252}" y="{ry}" width="34" height="34" fill="none" stroke="{GREY}"/>'
                    f'<path d="M{x + 258} {ry + 26}L{x + 268} {ry + 14}L{x + 274} {ry + 20}L{x + 280} {ry + 10}" fill="none" stroke="{PAPER}"/>'
                    f'{text(x + 298, ry + 15, name, 13, PAPER)}'
                    f'<rect x="{x + 298}" y="{ry + 23}" width="120" height="3" fill="{LINE}"/><rect x="{x + 298}" y="{ry + 23}" width="{120 * int(match[:-1]) / 100:.0f}" height="3" fill="{SIGNAL}"/>'
                    f'{label(x + w - 20, ry + 27, match, SIGNAL, anchor="end", size=10)}</g>')
    css += appear('prhead', 52, 94, ROOM_CYCLE)
    svg = f'''
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="{INK}" stroke="{PAPER}"/>
<rect x="{px + pw / 2 - 22}" y="{py + 8}" width="44" height="6" rx="3" fill="{LINE}"/>
{label(px + 14, py + 38, 'мой дизайнер', PAPER, size=10)}
{label(px + pw - 14, py + 38, 'mini app', DIM, anchor='end', size=9)}
<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="{INK}" stroke="{LINE}"/>
<g>{room(ix + 4, iy + 4, iw - 8, ih - 8, DIM, False)}</g>
<clipPath id="after"><rect x="{ix}" y="{iy}" width="0" height="{ih}"><animate attributeName="width" dur="{ROOM_CYCLE}s" repeatCount="indefinite" values="{sweep}" keyTimes="{times}" calcMode="spline" keySplines="0 0 1 1;.65 0 .35 1;0 0 1 1;.65 0 .35 1"/></rect></clipPath>
<g clip-path="url(#after)"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="{INK}"/>{room(ix + 4, iy + 4, iw - 8, ih - 8, GREY, True)}</g>
<rect x="{ix - 1}" y="{iy - 6}" width="2" height="{ih + 12}" fill="{SIGNAL}"><animate attributeName="x" dur="{ROOM_CYCLE}s" repeatCount="indefinite" values="{';'.join(f'{ix - 1 + float(v):.1f}' for v in sweep.split(';'))}" keyTimes="{times}" calcMode="spline" keySplines="0 0 1 1;.65 0 .35 1;0 0 1 1;.65 0 .35 1"/></rect>
{label(ix, iy + ih + 22, 'стиль', DIM, size=9)}
{"".join(f'<rect x="{ix + k * 50}" y="{iy + ih + 30}" width="46" height="20" fill="{SIGNAL if k == 1 else "none"}" stroke="{SIGNAL if k == 1 else GREY}"/>' + text(ix + k * 50 + 23, iy + ih + 44, s, 10, INK if k == 1 else GREY, 600, anchor="middle", mono=True) for k, s in enumerate(["лофт", "сканди", "бохо"]))}
<rect x="{ix}" y="{py + ph - 42}" width="{iw}" height="28" fill="{PAPER}"/>
{text(ix + iw / 2, py + ph - 23, 'Сгенерировать дизайн', 12, INK, 700, anchor='middle')}
<path d="M{px + pw + 18} {y + 40}H{x + w - 20}" stroke="{LINE}"/>
<g class="prhead">{label(x + 252, y + 66, 'подбор товаров под проект', GREY, size=10)}</g>
{"".join(rows)}'''
    return svg, css


def bunk(x, y, scale, stroke):
    s = scale
    return (f'<rect x="{x}" y="{y}" width="{100 * s}" height="{110 * s}" fill="none" stroke="{stroke}"/>'
            f'<path d="M{x} {y + 46 * s}H{x + 100 * s}M{x} {y + 34 * s}H{x + 100 * s}M{x} {y + 98 * s}H{x + 100 * s}M{x} {y + 86 * s}H{x + 100 * s}" stroke="{stroke}"/>'
            f'<path d="M{x + 80 * s} {y}V{y + 110 * s}M{x + 92 * s} {y}V{y + 110 * s}M{x + 80 * s} {y + 18 * s}H{x + 92 * s}M{x + 80 * s} {y + 60 * s}H{x + 92 * s}" stroke="{stroke}"/>'
            f'<rect x="{x + 8 * s}" y="{y + 24 * s}" width="{20 * s}" height="{9 * s}" fill="{SIGNAL}"/><rect x="{x + 8 * s}" y="{y + 76 * s}" width="{20 * s}" height="{9 * s}" fill="none" stroke="{stroke}"/>')


def hostel(x, y, w, h):
    cx, cy = x + 196, y + 34
    cell, gap = 34, 4
    days = ''
    for row in range(4):
        for col in range(7):
            day = row * 7 + col + 1
            dx, dy = cx + col * (cell + gap), cy + row * (20 + gap)
            days += f'<rect x="{dx}" y="{dy}" width="{cell}" height="20" fill="none" stroke="{LINE}"/>' + text(dx + 5, dy + 14, f'{day:02d}', 9.5, GREY, mono=True)
    start_x, start_y = cx + 3 * (cell + gap), cy + 24
    span = 4 * (cell + gap) - gap
    svg = f'''
{bunk(x + 26, y + 34, 1.0, PAPER)}
{label(x + 26, y + 168, 'номер 210 · отдельный', GREY, size=9.5)}
{label(cx, y + 22, 'заезд — выезд', DIM, size=9.5)}
{days}
<rect x="{start_x}" y="{start_y}" width="{cell}" height="20" fill="{SIGNAL}" fill-opacity=".85">
 <animate attributeName="width" dur="{BOOKING_CYCLE}s" repeatCount="indefinite" values="{cell};{cell};{span};{span};{cell}" keyTimes="0;.15;.45;.9;1" calcMode="spline" keySplines="0 0 1 1;.65 0 .35 1;0 0 1 1;.65 0 .35 1"/></rect>
<rect x="{cx}" y="{cy + 4 * 24 + 6}" width="{7 * (cell + gap) - gap}" height="26" fill="none" stroke="{PAPER}"/>
{text(cx + 12, cy + 4 * 24 + 23, 'Забронировать', 12, PAPER, 700)}
{label(cx + 7 * (cell + gap) - gap - 12, cy + 4 * 24 + 23, 'travelline', SIGNAL, anchor='end', size=9.5)}'''
    return svg, ''


def lotus(cx, cy, size, stroke):
    petals = ''.join(f'<path d="M{cx} {cy}C{cx - size * .5} {cy - size * .4} {cx - size * .3} {cy - size} {cx} {cy - size}C{cx + size * .3} {cy - size} {cx + size * .5} {cy - size * .4} {cx} {cy}Z" fill="none" stroke="{stroke}" transform="rotate({a} {cx} {cy})"/>' for a in (-56, -28, 0, 28, 56))
    return petals + f'<path d="M{cx - size} {cy}H{cx + size}" stroke="{stroke}"/>'


def lotos(x, y, w, h):
    panel_w, panel_h = 170, 100
    lx, rx, py = x + 40, x + w - 40 - panel_w, y + 42
    css = (f'@keyframes gate{{0%,40%{{transform:translateX(0)}}50%,90%{{transform:translateX({rx - lx}px)}}100%{{transform:translateX(0)}}}}'
           f'.gate{{animation:gate {GATE_CYCLE}s cubic-bezier(.77,0,.18,1) infinite}}'
           '@keyframes snip{0%,100%{transform:rotate(0)}50%{transform:rotate(-14deg)}}.snip{animation:snip 1.2s ease-in-out infinite}'
           '@keyframes snip2{0%,100%{transform:rotate(0)}50%{transform:rotate(14deg)}}.snip2{animation:snip2 1.2s ease-in-out infinite}')
    sx, sy = lx + panel_w / 2, py + 44
    beams = ''.join(f'<path class="pulse" style="{delay(-k * .3)};animation-duration:1.4s" d="M{rx + 50 + k * 14} {py + 18}V{py + 70}" stroke="{SIGNAL if k == 2 else PAPER}" stroke-width="{2 if k == 2 else 1}"/>' for k in range(6))
    svg = f'''
{lotus(x + w / 2, y + 34, 18, PAPER)}
{label(x + w / 2, y + 162, 'лотос · полевской', GREY, anchor='middle', size=9.5)}
<path d="M{x + w / 2} {y + 40}V{py + panel_h / 2}M{lx + panel_w} {py + panel_h / 2}H{rx}" stroke="{LINE}"/>
<rect x="{lx}" y="{py}" width="{panel_w}" height="{panel_h}" fill="{INK}" stroke="{GREY}"/>
<rect x="{rx}" y="{py}" width="{panel_w}" height="{panel_h}" fill="{INK}" stroke="{GREY}"/>
<g transform="translate({sx} {sy})">
 <g class="pivot snip"><path d="M0 0L-34 -10" stroke="{PAPER}" stroke-width="1.6"/><circle cx="18" cy="8" r="7" fill="none" stroke="{PAPER}" stroke-width="1.4"/><path d="M0 0L13 5" stroke="{PAPER}" stroke-width="1.4"/></g>
 <g class="pivot snip2"><path d="M0 0L-34 10" stroke="{PAPER}" stroke-width="1.6"/><circle cx="18" cy="-8" r="7" fill="none" stroke="{PAPER}" stroke-width="1.4"/><path d="M0 0L13 -5" stroke="{PAPER}" stroke-width="1.4"/></g>
 <circle r="2.4" fill="{SIGNAL}"/>
</g>
{beams}
{label(lx + 12, py + panel_h - 12, '/barber', PAPER, size=10)}
{label(rx + 12, py + panel_h - 12, '/laser', PAPER, size=10)}
<g class="gate"><rect x="{lx - 6}" y="{py - 6}" width="{panel_w + 12}" height="{panel_h + 12}" fill="none" stroke="{SIGNAL}" stroke-width="1.6"/>
<path d="M{lx - 6} {py + 6}V{py - 6}H{lx + 6}M{lx + panel_w - 6} {py + panel_h + 6}H{lx + panel_w + 6}V{py + panel_h - 6}" stroke="{SIGNAL}" stroke-width="3" fill="none"/></g>'''
    return svg, css
