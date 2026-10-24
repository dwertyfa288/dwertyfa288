from .canvas import text, label, delay, window_keyframes
from .scope import oscilloscope
from .theme import PAPER, GREY, DIM, LINE, SIGNAL, INK

CHAT_CYCLE = 9
LISTEN_CYCLE = 8


def appear(name, start, end, cycle):
    return window_keyframes(name, start, end, fade=4, lift=8) + f'.{name}{{animation:{name} {cycle}s cubic-bezier(.2,.8,.2,1) infinite}}'


def telegram(x, y, w, h):
    left, top = x + 22, y + 22
    bars = ''.join(f'<rect class="fb eq" style="{delay(-(i * .19) % 1.5)};animation-duration:{.9 + (i % 5) * .14:.2f}s" x="{left + 40 + i * 7}" y="{top + 55 - (5 + (i * 5 % 9) * 1.6) / 2:.1f}" width="3" height="{5 + (i * 5 % 9) * 1.6:.1f}" fill="{SIGNAL}"/>'
                   for i in range(17))
    ox, oy = x + w - 84, y + h / 2
    link = f'M{left + 206} {top + 55}H{ox - 70}L{ox - 46} {oy}'
    css = appear('tg1', 4, 93, CHAT_CYCLE) + appear('tg2', 20, 93, CHAT_CYCLE) + appear('tg3', 48, 93, CHAT_CYCLE)
    css += '@keyframes dash{to{stroke-dashoffset:-24}}.dash{stroke-dasharray:4 4;animation:dash 1.6s linear infinite}'
    svg = f'''
<g class="tg1"><rect x="{left}" y="{top}" width="178" height="30" fill="none" stroke="{GREY}"/>
 {text(left + 12, top + 20, 'Андрей: ты скоро?', 13, PAPER)}</g>
<g class="tg2"><rect x="{left}" y="{top + 38}" width="200" height="34" fill="{INK}" stroke="{PAPER}"/>
 <path d="M{left + 14} {top + 47}L{left + 28} {top + 55}L{left + 14} {top + 63}Z" fill="{PAPER}"/>
 {bars}{text(left + 162, top + 59.5, '0:07', 11, DIM, mono=True)}</g>
<g class="tg3"><rect x="{left + 40}" y="{top + 86}" width="190" height="30" fill="{PAPER}"/>
 {text(left + 52, top + 106, 'Буду через 5 минут', 13, INK, 700)}</g>
<path d="{link}" fill="none" stroke="{DIM}" class="dash"/>
<rect x="-3" y="-3" width="6" height="6" fill="{SIGNAL}"><animateMotion dur="2.2s" repeatCount="indefinite" path="{link}"/></rect>
<circle class="fb ripple" cx="{ox}" cy="{oy}" r="44" fill="none" stroke="{GREY}"/>
<circle cx="{ox}" cy="{oy}" r="44" fill="{INK}" stroke="{PAPER}"/>
<clipPath id="orb"><circle cx="{ox}" cy="{oy}" r="43"/></clipPath>
<g clip-path="url(#orb)">{oscilloscope(ox - 40, oy, 80, 18, SIGNAL, duration=3.6, stroke=1.8)}</g>
{label(ox, oy + 66, 'astra', anchor='middle', fill=GREY, size=10)}'''
    return svg, css


def mic(cx, cy, color):
    return (f'<rect x="{cx - 7}" y="{cy - 18}" width="14" height="24" rx="7" fill="none" stroke="{color}" stroke-width="1.8"/>'
            f'<path d="M{cx - 13} {cy - 2}A13 13 0 0 0 {cx + 13} {cy - 2}M{cx} {cy + 11}V{cy + 17}" fill="none" stroke="{color}" stroke-width="1.8"/>')


def interject(x, y, w, h):
    cx, cy, r = x + w - 86, y + h / 2, 56
    css = '@keyframes countdown{from{stroke-dashoffset:0}to{stroke-dashoffset:100}}' + f'.countdown{{stroke-dasharray:100;animation:countdown {LISTEN_CYCLE}s linear infinite}}'
    digits = []
    for second in range(8):
        name = f'cd{second}'
        start = 100 * second / 8
        css += (f'@keyframes {name}{{0%,{start:.2f}%{{opacity:0}}{start + .01:.2f}%,{start + 12.5:.2f}%{{opacity:1}}{start + 12.51:.2f}%,100%{{opacity:0}}}}'
                f'.{name}{{animation:{name} {LISTEN_CYCLE}s steps(1,end) infinite}}')
        digits.append(f'<g class="{name}">{text(cx, cy + 34, f"0{8 - second}s", 11, SIGNAL, 700, anchor="middle", mono=True)}</g>')
    css += appear('ij1', 2, 95, LISTEN_CYCLE) + appear('ij2', 14, 95, LISTEN_CYCLE) + appear('ij3', 42, 95, LISTEN_CYCLE) + appear('ij4', 62, 95, LISTEN_CYCLE)
    ticks = ''.join(f'<path d="M{cx} {cy - r - 8}V{cy - r - (14 if k % 5 == 0 else 11)}" stroke="{PAPER if k % 5 == 0 else DIM}" transform="rotate({k * 6} {cx} {cy})"/>' for k in range(60))
    lx = x + 22
    svg = f'''
<g class="ij1"><rect x="{lx}" y="{y + 20}" width="8" height="8" fill="{SIGNAL}"/>{text(lx + 16, y + 28.5, 'event: tts_completed', 12, GREY, mono=True)}</g>
<g class="ij2">{text(lx, y + 66, 'ASTRA', 11, DIM, 700, mono=True, spacing=1.5)}{text(lx + 62, y + 66, 'Напоминание создано.', 14, PAPER)}</g>
<g class="ij3">{text(lx, y + 98, 'ТЫ', 11, SIGNAL, 700, mono=True, spacing=1.5)}{text(lx + 62, y + 98, 'и перенеси звонок на 15:00', 14, PAPER)}</g>
<g class="ij4"><path d="M{lx} {y + 118}H{lx + 270}" stroke="{LINE}"/>{text(lx, y + 140, 'без «Astra, …» — сразу в диалог', 12, GREY, mono=True)}</g>
{ticks}
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="3"/>
<g transform="rotate(-90 {cx} {cy})"><circle class="countdown" cx="{cx}" cy="{cy}" r="{r}" pathLength="100" fill="none" stroke="{SIGNAL}" stroke-width="3"/></g>
{mic(cx, cy - 4, PAPER)}
{"".join(digits)}'''
    return svg, css
