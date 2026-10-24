from . import art_voice, art_prime, art_web
from .canvas import document, frame, text, label, delay, tags, arrow
from .theme import FULL_WIDTH, HALF_WIDTH, PAPER, GREY, LINE, SIGNAL, INK

HALF_HEIGHT = 392
WIDE_HEIGHT = 430

ARTS = {
    'telegram': art_voice.telegram,
    'interject': art_voice.interject,
    'cli': art_prime.cli,
    'desktop': art_prime.desktop,
    'router': art_prime.router,
    'proxy': art_prime.proxy,
    'portfolio': art_web.portfolio,
    'nova': art_web.nova,
    'globe': art_web.globe,
    'timeline': art_web.timeline,
    'landing': art_web.landing,
}


def plate(x, y, w, h, project, figure):
    art, css = ARTS[project['art']](x, y, w, h)
    svg = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK}"/>'
           f'<clipPath id="plate"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
           f'<g clip-path="url(#plate)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#grid)"/>{art}</g>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{LINE}"/>'
           + label(x + w, y + h + 18, f'fig. {figure}', GREY, anchor='end', size=10))
    return svg, css


def title_reveal(uid, x, y, size, content, width):
    return (f'<clipPath id="{uid}"><rect x="{x - 4}" y="{y - size}" width="{width}" height="{size * 1.3:.0f}"/></clipPath>'
            f'<g clip-path="url(#{uid})"><g class="reveal" style="{delay(.15)}">{text(x, y, content, size, PAPER, 800, spacing=-size * .03)}</g></g>')


def half(project, number, phase):
    art, css = plate(28, 66, HALF_WIDTH - 56, 170, project, number)
    lines = ''.join(f'<g class="rise" style="{delay(.35 + i * .1)}">{text(28, 316 + i * 22, line, 15, GREY)}</g>' for i, line in enumerate(project['lines']))
    body = (frame(HALF_WIDTH, HALF_HEIGHT, f'{number} — {project["kind"]}', '', phase=phase, grid=False)
            + f'<g transform="translate({HALF_WIDTH - 38} 32)">{arrow(0, 0, 7, PAPER, 1.6)}</g>'
            + art
            + title_reveal('ttl', 28, 288, 32, project['title'], 420)
            + lines
            + f'<path d="M28 {HALF_HEIGHT - 50}H{HALF_WIDTH - 28}" stroke="{LINE}"/>'
            + tags(28, HALF_HEIGHT - 26, project['chips']))
    return document(HALF_WIDTH, HALF_HEIGHT, body, project['alt'], css=css)


def wide(project, number, phase):
    art, css = plate(556, 66, FULL_WIDTH - 584, WIDE_HEIGHT - 110, project, number)
    lines = ''.join(f'<g class="rise" style="{delay(.4 + i * .1)}">{text(28, 214 + i * 26, line, 17, GREY)}</g>' for i, line in enumerate(project['lines']))
    body = (frame(FULL_WIDTH, WIDE_HEIGHT, f'{number} — {project["kind"]}', project['url_label'], phase=phase, grid=False)
            + art
            + title_reveal('ttl', 26, 172, 72, project['title'], 520)
            + lines
            + f'<path d="M28 300H500" stroke="{LINE}"/>'
            + tags(28, 328, project['chips'], size=13)
            + f'<g class="rise" style="{delay(.9)}"><rect x="28" y="{WIDE_HEIGHT - 82}" width="200" height="44" fill="none" stroke="{PAPER}"/>'
            + label(46, WIDE_HEIGHT - 55, project['cta'], PAPER, size=12)
            + f'<g transform="translate(208 {WIDE_HEIGHT - 60})">{arrow(0, 0, 6, SIGNAL, 1.8)}</g></g>')
    return document(FULL_WIDTH, WIDE_HEIGHT, body, project['alt'], css=css)
