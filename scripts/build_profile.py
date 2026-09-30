"""Build the entire profile in one SVG with a shared animation clock."""
from pathlib import Path
from html import escape
import base64
import hashlib

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
INK, PAPER, MUTED, LINE, ACCENT = '#101016', '#f4f0ee', '#aaa4b7', '#373240', '#ff947d'
PALETTE = ['#81d6ee', '#baa0ff', '#ff947d', '#f7c783']
PROJECTS = [
('Избранное', [
('TG for Astra', 'Telegram, который можно слушать. И отвечать голосом.', 'TYPESCRIPT / TELEGRAM / ASTRA', 'VOICE', 'https://github.com/dwertyfa288/dwertyfa-astra-tg', 'voice'),
('Astra Interject', 'Продолжение диалога без повторного триггерного слова.', 'TYPESCRIPT / AUDIO / ASTRA', 'AUDIO', 'https://github.com/dwertyfa288/astra-interject', 'voice'),
('dwertyfa / portfolio', 'Интерактивное портфолио с 3D-графикой и анимациями.', 'NEXT.JS / REACT / THREE.JS', 'WEB', 'https://dwertyfa288.github.io/dwertyfa/', 'web'),
]),
('Веб-проекты', [
('Nova Prestige', 'Промо-сайт жилого дома с вниманием к атмосфере и деталям.', 'REAL ESTATE / RESPONSIVE / MOTION', 'SITE', 'https://novaprestige.ru/', 'web'),
('Roxy Boost', 'VPN-продукт: инфраструктура, приложение и сайт.', 'FULL-STACK / VPN / INFRASTRUCTURE', 'VPN', 'https://roxyvpn.ru/', 'network'),
('danek montage', 'Портфолио видеомонтажёра, в котором движение задаёт ритм.', 'REACT / MOTION UI / RESPONSIVE', 'FILM', 'https://fazedanek-hub.github.io/danekmontage/', 'voice'),
('Hey Ksusha', 'Лендинг интенсива: выразительная подача, запись и оплата.', 'LANDING / ART DIRECTION / PAYMENTS', 'SITE', 'https://heyksusha.ru/intensive', 'web'),
]),
('SpherePrime', [
('PrimeProxy', 'Локальный MTProto-прокси для Telegram через WebSocket.', 'PYTHON / MTPROTO / WEBSOCKET', 'NET', 'https://github.com/SpherePrime/PrimeProxy', 'network'),
('PrimeAI', 'AI-провайдер для Astra с маршрутизацией запросов к моделям.', 'TYPESCRIPT / ROUTER API / ASTRA', 'AI', 'https://github.com/SpherePrime/PrimeAi', 'network'),
('Prime CLI', 'AI-ассистент для работы с кодом прямо в терминале.', 'GO / MCP / MULTI-MODEL', 'CLI', 'https://github.com/SpherePrime/CLI', 'web'),
])]
parts = []
def text(x, y, value, size=22, color=PAPER, weight=400, mono=False, extra=''):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" class="{"mono" if mono else "sans"}" {extra}>{escape(value)}</text>')
def rule(y):
    parts.append(f'<path d="M40 {y}H1060" stroke="{LINE}"/>')
def border(y, height, color=ACCENT):
    parts.append(f'<rect x="40" y="{y}" width="1020" height="{height}" rx="9" fill="#17151f" stroke="{LINE}"/>')
    parts.append(f'<rect class="rim" pathLength="1000" x="40" y="{y}" width="1020" height="{height}" rx="9" fill="none" stroke="{color}"/>')
    parts.append(f'<path d="M40 {y+20}v{height-40}" stroke="{color}" stroke-width="3"/>')
def signal(x, y, name, color=ACCENT):
    # Each illustration is centered in the same 96px column.
    parts.append(f'<g transform="translate({x+42} {y-5})" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')
    if name == 'TG for Astra':
        parts.append('<g class="icon-float"><path d="m-42-10 82-27-23 76-24-25-17 13 3-27 42-27-51 20Z"/><path class="trail" d="M-44 37h38"/></g>')
    elif name == 'Astra Interject':
        parts.append('<rect x="-9" y="-33" width="18" height="39" rx="9"/><path d="M-20-9v6a20 20 0 0 0 40 0v-6M0 17v15m-13 0h26"/>')
        for i,h in enumerate((12,27,18)):
            parts.append(f'<path class="icon-wave" style="animation-delay:-{i*.3}s" d="M{29+i*8} {-h/2}v{h}"/>')
    elif name == 'dwertyfa / portfolio':
        parts.append('<rect x="-44" y="-31" width="88" height="63" rx="6"/><path d="M-44-13h88m-73-9h1m8 0h1m8 0h1m4 18-10 9 10 9m24-18 10 9-10 9"/><path class="cursor" d="M-6 21H6"/>')
    elif name == 'Nova Prestige':
        parts.append('<path d="M-39 34v-48l28-20v68m0-38 26-15v53m0-22 25-10v32M-46 34h93"/><path class="windows" d="M-29-8v30m10-38v38m19-19v19m8-24v24m18-8v8"/>')
    elif name == 'Roxy Boost':
        parts.append('<path d="M0-40 34-27V-2c0 17-14 31-34 42-20-11-34-25-34-42v-25Z"/><rect x="-12" y="-6" width="24" height="23" rx="4"/><path d="M-8-6v-9a8 8 0 0 1 16 0v9"/><circle class="lock-pulse" cy="4" r="2"/>')
    elif name == 'danek montage':
        parts.append('<rect x="-43" y="-20" width="86" height="54" rx="5"/><g class="clapper"><path d="M-43-20v-15h86v15Zm13-15-10 15m29-15-10 15m29-15-10 15m29-15-10 15"/></g><path class="play" d="m-7-7 20 14-20 14Z"/>')
    elif name == 'Hey Ksusha':
        parts.append('<path d="M0-26c-12-9-28-12-42-8v63c15-4 29-1 42 8 13-9 27-12 42-8v-63c-14-4-30-1-42 8ZM0-26v63"/><path d="M-32-17h17m-17 12h21m-21 12h21m24-24h17m-17 12h21"/><path class="bookmark" d="M25-34v24l7-4 7 4v-24"/>')
    elif name == 'PrimeProxy':
        parts.append('<rect x="-45" y="-18" width="22" height="36" rx="4"/><rect x="23" y="-18" width="22" height="36" rx="4"/><path d="M-23 0h46"/><path class="packet" d="M-23 0h46"/><circle r="8" fill="#17151f"/><path d="M-38 10h8m38 0h8"/>')
    elif name == 'PrimeAI':
        parts.append('<rect x="-24" y="-24" width="48" height="48" rx="8"/><path d="M-12-24v-12m12 12v-12m12 12v-12m-24 60v12m12-12v12m12-12v12M-24-12h-12m12 12h-12m12 12h-12m60-24h12m-12 12h12m-12 12h12"/><g class="ai-core"><path d="M0-12 12 0 0 12-12 0Z"/><circle r="3"/></g>')
    else:
        parts.append('<rect x="-43" y="-31" width="86" height="63" rx="6"/><path d="M-43-13h86m-72-9h1m8 0h1m8 0h1m-20 23 11 10-11 10"/><path class="cursor" d="M-3 21h18"/>')
    parts.append('</g>')

parts.append('''<defs><linearGradient id="title-colors" x1="0" y1="0" x2="1" y2="1"><stop class="tone-a" stop-color="#ff947d"/><stop offset=".5" class="tone-b" stop-color="#baa0ff"/><stop offset="1" class="tone-c" stop-color="#81d6ee"/></linearGradient><clipPath id="hero-zone"><rect x="25" y="75" width="1050" height="256" rx="12"/></clipPath></defs>''')

text(40,43,'DWERTYFA / DEVELOPER',15,ACCENT,mono=True,extra='letter-spacing="1.5"')
text(1060,43,'PERSONAL INDEX · 2026',14,MUTED,mono=True,extra='text-anchor="end"')
rule(65)
text(34,195,'dwertyfa.',118,'url(#title-colors)',600,extra='letter-spacing="-6"')
text(40,254,'Создаю то, чем удобно пользоваться.',31)
text(40,291,'Веб. Голосовые интерфейсы. Интеграции.',22,MUTED)
avatar = base64.b64encode((ASSETS/'avatar.png').read_bytes()).decode()
parts.append('<defs><clipPath id="portrait"><circle cx="941" cy="186" r="63"/></clipPath><radialGradient id="portrait-halo"><stop stop-color="#baa0ff" stop-opacity=".2"/><stop offset="1" stop-color="#baa0ff" stop-opacity="0"/></radialGradient></defs>')
parts.append('<circle cx="941" cy="186" r="116" fill="url(#portrait-halo)"/>')
for i,(angle,color) in enumerate(((-32,'#81d6ee'),(32,'#baa0ff'),(90,'#ff947d'))):
    parts.append(f'<g transform="translate(941 186) rotate({angle})"><ellipse rx="112" ry="49" fill="none" stroke="{color}" opacity=".25"/><ellipse class="orbital-flow" style="animation-duration:{9+i*3}s" pathLength="1000" rx="112" ry="49" fill="none" stroke="{color}" stroke-width="2.2"/><circle class="satellite" style="animation-duration:{9+i*3}s" r="3.5" fill="{color}" stroke="none"/></g>')
parts.append(f'<circle cx="941" cy="186" r="67" fill="#17151f" stroke="#baa0ff" stroke-width="1.5"/><image x="878" y="123" width="126" height="126" href="data:image/jpeg;base64,{avatar}" clip-path="url(#portrait)" preserveAspectRatio="xMidYMid slice"/>')
text(941,329,'ЧЕЛОВЕК ЗА КОДОМ',12,MUTED,mono=True,extra='text-anchor="middle" letter-spacing="1.5"')

rule(343)
text(40,391,'ОБО МНЕ',14,MUTED,mono=True)
text(40,436,'От выразительного интерфейса —',29)
text(40,474,'до работающего инструмента.',29)
text(650,422,'Сайты с 3D и анимациями.',22)
text(650,460,'Плагины для Astra и Telegram.',22)
text(650,498,'Сервисы, связанные в единый продукт.',22)
border(534,129)
text(62,567,'СТЕК',13,MUTED,mono=True,extra='letter-spacing="1.5"')
text(62,603,'TypeScript / React / Next.js / Go / Rust / Tauri / Python',22,PAPER,mono=True)
text(62,640,'Three.js · Astra Plugin SDK',19,MUTED,mono=True)
y, number = 745, 0
for index,(title,projects) in enumerate(PROJECTS,1):
    section_color = PALETTE[index-1]
    text(40,y,f'0{index}',18,section_color,mono=True)
    text(107,y,title,34,PAPER,500)
    parts.append(f'<path class="section-scan" d="M40 {y+26}h1020" stroke="{section_color}" stroke-width="2"/>')
    if title == 'SpherePrime':
        text(1060,y,'ПРОЕКТЫ ОРГАНИЗАЦИИ',13,MUTED,mono=True,extra='text-anchor="end"')
    rule(y+26)
    y += 55
    for name,description,tags,label,url,kind in projects:
        number += 1
        color = PALETTE[(number-1)%4]
        border(y,143,color)
        text(62,y+38,f'{number:02}',15,MUTED,mono=True)
        text(115,y+43,name,31,PAPER,500)
        text(115,y+80,description,20,MUTED)
        text(115,y+118,tags,13,color,mono=True,extra='letter-spacing=".8"')
        text(1038,y+32,label,12,MUTED,mono=True,extra='text-anchor="end"')
        signal(924,y+88,name,color)
        y += 161
    y += 64
rule(y-17)
text(40,y+34,'Есть задача? Давай обсудим.',35,PAPER,500)
text(40,y+77,'t.me/dwertyfa',22,ACCENT,mono=True)
text(1060,y+77,'КОД / ХАРАКТЕР / ПОЛЬЗА',14,MUTED,mono=True,extra='text-anchor="end"')
height = y+117
STYLE = '''
.sans{font-family:'Segoe UI',Arial,sans-serif}.mono{font-family:Consolas,'Courier New',monospace}
.rim{stroke-width:1.4;stroke-dasharray:70 930;animation:rim 10s linear infinite}
@keyframes rim{from{stroke-dashoffset:0}to{stroke-dashoffset:-1000}}
.dial{animation:dial 24s linear infinite}@keyframes dial{to{transform:rotate(360deg)}}
.bar{transform-box:fill-box;transform-origin:center;animation:bar 2.1s ease-in-out infinite}
@keyframes bar{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}
.packet{stroke-width:2;stroke-dasharray:8 76;animation:packet 3s linear infinite}@keyframes packet{to{stroke-dashoffset:-84}}
.cursor{animation:cursor 1.4s steps(1,end) infinite}@keyframes cursor{0%,55%{opacity:1}56%,100%{opacity:0}}
.tone-a{animation:tone-a 12s ease-in-out infinite}.tone-b{animation:tone-b 12s ease-in-out infinite}.tone-c{animation:tone-c 12s ease-in-out infinite}
@keyframes tone-a{0%,100%{stop-color:#ff947d}50%{stop-color:#81d6ee}}
@keyframes tone-b{0%,100%{stop-color:#baa0ff}50%{stop-color:#ff947d}}
@keyframes tone-c{0%,100%{stop-color:#81d6ee}50%{stop-color:#baa0ff}}
.sculpture{animation:sculpture 20s ease-in-out infinite}
@keyframes sculpture{0%,100%{transform:rotate(-18deg) scale(.95)}50%{transform:rotate(32deg) scale(1.12)}}
.orbit-two{animation:dial 16s linear infinite}.orbit-three{animation:dial 29s linear infinite reverse}
.rotor{animation:dial 24s linear infinite}
.radar{animation:radar 4s ease-out infinite}
@keyframes radar{0%{transform:scale(.7);opacity:0}20%{opacity:.65}100%{transform:scale(1.45);opacity:0}}
.lift{animation:lift 4s ease-in-out infinite}@keyframes lift{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.section-scan{stroke-dasharray:100 920;animation:scan 8s linear infinite}@keyframes scan{to{stroke-dashoffset:-1020}}
.icon-float{animation:icon-float 4s ease-in-out infinite}@keyframes icon-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.icon-wave{transform-box:fill-box;transform-origin:center;animation:bar 1.5s ease-in-out infinite}
.windows,.lock-pulse,.play,.bookmark{animation:detail 3.5s ease-in-out infinite}@keyframes detail{0%,100%{opacity:.4}50%{opacity:1}}
.ai-core{animation:dial 18s linear infinite}
.clapper{transform-origin:-43px -20px;animation:clapper 5s ease-in-out infinite}@keyframes clapper{0%,75%,100%{transform:rotate(0)}35%{transform:rotate(-8deg)}}
.trail{stroke-dasharray:10 28;animation:trail 2s linear infinite}@keyframes trail{to{stroke-dashoffset:-38}}
.orbital-flow{stroke-dasharray:120 880;animation:rim 9s linear infinite}
.satellite{offset-path:path('M112 0 A112 49 0 1 1 -112 0 A112 49 0 1 1 112 0');offset-distance:0%;animation:satellite 9s linear infinite}
@keyframes satellite{to{offset-distance:100%}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
'''
doc = f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title"><title id="title">dwertyfa — веб, голосовые интерфейсы и интеграции. Избранные проекты и стек.</title><style>{STYLE}</style><rect width="1100" height="{height}" fill="{INK}"/>{"".join(parts)}</svg>'
data = doc.encode('utf-8')
filename = f'profile-{hashlib.sha256(data).hexdigest()[:12]}.svg'
(ASSETS/'profile.svg').write_bytes(data)
(ASSETS/filename).write_bytes(data)
nav = '<a href="https://t.me/dwertyfa">Telegram ↗</a> &nbsp; · &nbsp; <a href="https://dwertyfa288.github.io/dwertyfa/">Портфолио ↗</a> &nbsp; · &nbsp; <a href="https://github.com/SpherePrime">SpherePrime ↗</a>'
readme = f'<p align="center">{nav}</p>\n\n<img src="./assets/{filename}" width="100%" alt="dwertyfa — сайты, голосовые плагины и интеграции. Стек: TypeScript, React, Next.js, Go, Rust, Tauri, Python, Three.js и Astra Plugin SDK. Проекты и ссылки ниже." />\n\n### Открыть проекты\n\n'
links = ''
for title,projects in PROJECTS:
    readme += f'**{title}**\n\n'+' · '.join(f'[{name} ↗]({url})' for name,description,tags,label,url,kind in projects)+'\n\n'
    links += f'<p><strong>{title}</strong><br/>'+' · '.join(f'<a href="{url}">{escape(name)} ↗</a>' for name,description,tags,label,url,kind in projects)+'</p>'
readme += '> SpherePrime — организация, в которой я состою. Здесь представлены её публичные проекты.\n'
(ROOT/'README.md').write_text(readme,encoding='utf-8')
preview = f'<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>dwertyfa — profile</title><style>body{{margin:0;background:{INK};color:{PAPER};font:16px/1.7 "Segoe UI",sans-serif}}main{{max-width:1000px;margin:24px auto;padding:24px}}img{{width:100%;height:auto}}a{{color:{ACCENT};text-decoration:none}}nav{{text-align:center;margin:12px 0 28px}}section{{padding:20px 36px}}@media(max-width:640px){{main{{margin:0;padding:12px}}section{{padding:16px}}}}</style><main><nav>{nav}</nav><img src="./assets/{filename}" alt="dwertyfa — профиль"/><section><h3>Открыть проекты</h3>{links}</section></main></html>'
(ROOT/'preview.html').write_text(preview,encoding='utf-8')
print(f'Generated {filename}, 1100 x {height}. All 11 outlines share one SVG animation clock.')
