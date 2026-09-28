"""Generate self-contained, animated SVG assets. Python standard library only."""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def svg(name, height, content, title):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs>
 <linearGradient id="accent"><stop stop-color="#bba7ff"/><stop offset="1" stop-color="#88f3cf"/></linearGradient>
 <radialGradient id="halo"><stop stop-color="#7359c4" stop-opacity=".35"/><stop offset="1" stop-color="#0c1018" stop-opacity="0"/></radialGradient>
 <linearGradient id="panel" x2="1" y2="1"><stop stop-color="#141925"/><stop offset="1" stop-color="#0b1018"/></linearGradient>
 <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<style>
text {{font-family: 'Segoe UI', Arial, sans-serif;}}
.mono {{font-family: Consolas, 'Courier New', monospace;}}
.orbit {{stroke-dasharray:90 640; animation: orbit 14s linear infinite;}}
.reverse {{animation-direction:reverse; animation-duration:21s;}}
.pulse {{animation:pulse 5s ease-in-out infinite;}}
.flow {{stroke-dasharray:28 190; animation:flow 9s linear infinite;}}
@keyframes orbit {{to {{stroke-dashoffset:-730;}}}}
@keyframes flow {{to {{stroke-dashoffset:-436;}}}}
@keyframes pulse {{0%,100% {{opacity:.35;}} 50% {{opacity:1;}}}}
@media (prefers-reduced-motion:reduce) {{.orbit,.pulse,.flow {{animation:none;}}}}
</style>
{content}
</svg>'''
    (ASSETS / name).write_text(document, encoding='utf-8')

stars = ''.join(f'<circle cx="{620+(i*137)%450}" cy="{30+(i*83)%355}" r="{1 if i%3 else 1.7}" fill="#cbbcff" opacity="{.12+(i%4)*.1}"/>' for i in range(32))
rings = ''
for angle in (-32, 32, 90):
    rings += f'''<g transform="translate(854 208) rotate({angle})">
    <ellipse rx="156" ry="64" fill="none" stroke="#665984" stroke-opacity=".45"/>
    <ellipse class="orbit {'reverse' if angle==32 else ''}" rx="156" ry="64" fill="none" stroke="url(#accent)" stroke-width="2.2"/>
    </g>'''

svg('hero.svg', 440, f'''
<rect x=".5" y=".5" width="1099" height="439" rx="22" fill="#0b1018" stroke="#2b3041"/>
<ellipse cx="840" cy="220" rx="290" ry="270" fill="url(#halo)"/>
{stars}
<path d="M40 64H1060" stroke="#282c3c"/>
<circle cx="43" cy="34" r="4" fill="#b9a3ff"/><circle cx="59" cy="34" r="4" fill="#88f3cf"/><circle cx="75" cy="34" r="4" fill="#586075"/>
<text x="98" y="40" fill="#a9b2c6" font-size="14" class="mono">dwertyfa / personal space</text>
<text x="1060" y="40" fill="#88f3cf" font-size="13" class="mono" text-anchor="end">CODE · CREATE · CONNECT</text>
<text x="46" y="119" fill="#bba7ff" font-size="14" letter-spacing="3" class="mono">FULL-STACK / VOICE / INTEGRATIONS</text>
<text x="40" y="223" fill="#f3f0ff" font-size="104" font-weight="700" letter-spacing="-5">dwertyfa<tspan fill="#88f3cf">.</tspan></text>
<text x="46" y="269" fill="#d4d8e6" font-size="26">От идеи — до живого продукта.</text>
<text x="47" y="305" fill="#929cb2" font-size="19">Сайты с характером. Плагины с пользой.</text>
{rings}
<circle cx="854" cy="208" r="59" fill="#111625" stroke="#71628e"/>
<circle class="pulse" cx="854" cy="208" r="61" fill="none" stroke="#bba7ff" stroke-width="3" filter="url(#glow)"/>
<text x="854" y="227" text-anchor="middle" fill="#e3d9ff" font-size="62" font-weight="600">d<tspan fill="#88f3cf">.</tspan></text>
<text x="854" y="382" text-anchor="middle" fill="#828aa2" font-size="12" class="mono" letter-spacing="2">IDEAS IN ORBIT</text>
<path d="M46 361H650" stroke="#292e40"/>
<circle cx="51" cy="385" r="4" fill="#88f3cf"/>
<text x="66" y="390" fill="#b0b9cc" font-size="15" class="mono">TYPESCRIPT / REACT / NEXT.JS</text>
<text x="66" y="416" fill="#bba7ff" font-size="15" class="mono">GO / RUST / TAURI / PYTHON</text>
''', 'dwertyfa — full-stack, голосовые интерфейсы и интеграции. От идеи до живого продукта.')

def card(filename, number, label, name, description, tags, color, icon):
    bars = ''.join(f'<rect x="{886+i*13}" y="{99-(i%4)*8}" width="5" height="{16+(i%4)*16}" rx="2" fill="{color}" opacity="{.25+i*.06}"/>' for i in range(9))
    if icon == 'voice':
        art = f'<g class="pulse">{bars}</g>'
    elif icon == 'telegram':
        art = f'<path d="m880 97 117-40-31 104-34-31-23 17 3-35 65-39-77 31Z" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/><path class="flow" d="M838 179h181" stroke="{color}" stroke-width="2"/>'
    elif icon == 'building':
        art = f'<g fill="none" stroke="{color}"><path d="M873 161V79l42-24v106m0-62 39-23v85m0-44 49-20v64M860 162h156" stroke-width="2"/><path d="M886 92v53m15-63v63m29-29v29m13-37v37m27-17v17m17-22v22" opacity=".4"/><path class="flow" d="M873 161V79l42-24v106h88V97l-49 20" stroke-width="3"/></g>'
    elif icon == 'shield':
        art = f'<path d="m941 48 65 24v37c0 26-34 47-65 60-31-13-65-34-65-60V72Z" fill="none" stroke="{color}" stroke-width="2"/><path class="pulse" d="m919 88 38 0-19 26h24l-44 38 14-30h-21Z" fill="{color}"/><ellipse class="orbit" cx="941" cy="108" rx="88" ry="31" fill="none" stroke="{color}" opacity=".5"/>'
    elif icon == 'film':
        art = f'<rect x="866" y="61" width="151" height="92" rx="8" fill="none" stroke="{color}"/><path d="M866 81h151m-151 52h151m-132-72v20m25-20v20m25-20v20m25-20v20m25-20v20m-100 52v20m25-20v20m25-20v20m25-20v20m25-20v20" stroke="{color}" opacity=".5"/><path class="pulse" d="m932 93 24 15-24 15Z" fill="{color}"/>'
    elif icon == 'spark':
        art = f'<g transform="translate(942 107)" fill="none" stroke="{color}"><circle r="61" opacity=".2"/><path class="pulse" d="M0-51 12-13 51 0 12 13 0 51-12 13-51 0-12-13Z" stroke-width="2"/><circle class="orbit reverse" r="74" stroke-width="2"/><circle r="5" fill="{color}"/></g>'
    elif icon == 'proxy':
        art = f'<path d="M874 106h135" stroke="{color}" opacity=".3"/><path class="flow" d="M874 106h135" stroke="{color}" stroke-width="3"/><rect x="861" y="82" width="35" height="48" rx="7" fill="#141925" stroke="{color}"/><rect x="990" y="82" width="35" height="48" rx="7" fill="#141925" stroke="{color}"/><circle class="pulse" cx="943" cy="106" r="15" fill="#141925" stroke="{color}"/><path d="M871 117h15m114 0h15" stroke="{color}"/>'
    elif icon == 'ai':
        art = f'<g fill="none" stroke="{color}"><path d="M877 62 942 106 1007 62M877 150l65-44 65 44M877 106h130" opacity=".45"/><circle class="pulse" cx="942" cy="106" r="24"/><circle cx="942" cy="106" r="10"/><circle cx="877" cy="62" r="6"/><circle cx="1007" cy="62" r="6"/><circle cx="877" cy="150" r="6"/><circle cx="1007" cy="150" r="6"/><path class="flow" d="M877 62 942 106 1007 150" stroke-width="2"/></g>'
    elif icon == 'cli':
        art = f'<rect x="866" y="58" width="154" height="99" rx="9" fill="none" stroke="{color}"/><path d="M866 80h154m-137-12h3m8 0h3m8 0h3" stroke="{color}" opacity=".5"/><path d="m887 101 13 11-13 11" fill="none" stroke="{color}" stroke-width="2"/><path class="pulse" d="M913 124h25" stroke="{color}" stroke-width="3"/>'
    else:
        art = f'<g transform="translate(942 105) rotate(-24)"><ellipse rx="71" ry="31" fill="none" stroke="{color}" opacity=".4"/><ellipse class="orbit" rx="71" ry="31" fill="none" stroke="{color}" stroke-width="2"/><circle r="34" fill="none" stroke="{color}"/><path d="M-34 0h68M0-34v68" stroke="{color}" opacity=".5"/></g>'
    svg(filename, 208, f'''
<rect x=".5" y=".5" width="1099" height="207" rx="17" fill="url(#panel)" stroke="#2b3041"/>
<rect x="1" y="39" width="3" height="130" rx="1.5" fill="{color}"/>
<text x="30" y="35" fill="{color}" font-size="12" letter-spacing="1.8" class="mono">{number} / {label}</text>
<text x="30" y="85" fill="#f1f2fa" font-size="33" font-weight="600">{name}</text>
<text x="30" y="123" fill="#aeb7cb" font-size="19">{description}</text>
<text x="30" y="174" fill="{color}" font-size="13" class="mono" letter-spacing="1">{tags}</text>
<path d="M813 30V178" stroke="#2b3041"/>
{art}
<path d="M1042 35h16v16m-16 0 16-16" fill="none" stroke="#adb5cb" stroke-width="1.8"/>
''', f'{name}: {description}')

card('telegram.svg', '01', 'VOICE × MESSAGING', 'TG for Astra', 'Telegram, который можно слушать. И отвечать голосом.', 'TYPESCRIPT   /   TELEGRAM   /   ASTRA', '#88f3cf', 'telegram')
card('interject.svg', '02', 'NATURAL CONVERSATION', 'Astra Interject', 'Продолжение диалога без повторного триггерного слова.', 'TYPESCRIPT   /   AUDIO   /   ASTRA', '#bba7ff', 'voice')
card('portfolio.svg', '03', 'WEB × MOTION', 'dwertyfa / portfolio', 'Интерактивное портфолио с 3D-графикой и анимациями.', 'NEXT.JS   /   REACT   /   THREE.JS', '#f2b99b', 'web')
card('nova.svg', '01', 'WEB / ARCHITECTURE', 'Nova Prestige', 'Промо-сайт жилого дома с атмосферой и вниманием к деталям.', 'REAL ESTATE   /   RESPONSIVE   /   MOTION', '#88f3cf', 'building')
card('roxy.svg', '02', 'WEB / DIGITAL PRODUCT', 'Roxy Boost', 'VPN-продукт: от инфраструктуры до приложения и сайта.', 'FULL-STACK   /   VPN   /   INFRASTRUCTURE', '#bba7ff', 'shield')
card('danek.svg', '03', 'WEB / CREATIVE PORTFOLIO', 'danek montage', 'Портфолио видеомонтажёра, в котором движение задаёт ритм.', 'REACT   /   MOTION UI   /   RESPONSIVE', '#f2b99b', 'film')
card('ksusha.svg', '04', 'WEB / EDUCATION', 'Hey Ksusha', 'Лендинг интенсива: выразительная подача, запись и оплата.', 'LANDING PAGE   /   ART DIRECTION   /   PAYMENTS', '#edbddd', 'spark')
card('primeproxy.svg', '01', 'SPHEREPRIME / NETWORK', 'PrimeProxy', 'Локальный MTProto-прокси для Telegram через WebSocket.', 'PYTHON   /   MTPROTO   /   WEBSOCKET', '#88f3cf', 'proxy')
card('primeai.svg', '02', 'SPHEREPRIME / INTELLIGENCE', 'PrimeAI', 'AI-провайдер для Astra с маршрутизацией запросов к моделям.', 'TYPESCRIPT   /   ROUTER API   /   ASTRA', '#bba7ff', 'ai')
card('primecli.svg', '03', 'SPHEREPRIME / DEVELOPER TOOLS', 'Prime CLI', 'AI-ассистент для кода — прямо в терминале.', 'GO   /   MCP   /   MULTI-MODEL', '#f2b99b', 'cli')

svg('footer.svg', 138, '''
<rect x=".5" y=".5" width="1099" height="137" rx="17" fill="#0b1018" stroke="#2b3041"/>
<path d="M30 95H395l22-22 26 38 31-64 33 77 29-47 18 18h516" stroke="#313247" fill="none"/>
<path class="flow" d="M30 95H395l22-22 26 38 31-64 33 77 29-47 18 18h516" stroke="url(#accent)" stroke-width="2" fill="none"/>
<text x="30" y="42" fill="#d9daeb" font-size="20">Есть идея? Дадим ей форму.</text>
<text x="1070" y="42" fill="#88f3cf" font-size="15" class="mono" text-anchor="end">@dwertyfa ↗</text>
''', 'Есть идея? Дадим ей форму. Telegram: @dwertyfa')
print('Generated 12 SVG assets.')
