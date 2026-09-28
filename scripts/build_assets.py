"""Generate self-contained, animated SVG assets. Python standard library only."""
from pathlib import Path
from html import escape
import math
import base64
import hashlib
import re

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

avatar_data = base64.b64encode((ASSETS / 'avatar.png').read_bytes()).decode('ascii')

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
<defs><clipPath id="avatar-clip"><circle cx="854" cy="208" r="56"/></clipPath></defs>
<image x="798" y="152" width="112" height="112" href="data:image/jpeg;base64,{avatar_data}" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
<circle cx="854" cy="208" r="58" fill="none" stroke="#bba7ff" stroke-opacity=".65"/>
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
        art = f'<path d="M942 48 1000 70v39c0 26-26 48-58 62-32-14-58-36-58-62V70Z" fill="#1b1930" stroke="{color}" stroke-width="2" stroke-linejoin="round"/><path d="M942 59 989 77v32c0 19-20 39-47 52-27-13-47-33-47-52V77Z" fill="none" stroke="{color}" opacity=".15"/><rect x="922" y="99" width="40" height="33" rx="7" fill="{color}" opacity=".9"/><path d="M929 99V88a13 13 0 0 1 26 0v11" fill="none" stroke="{color}" stroke-width="3"/><circle cx="942" cy="113" r="3" fill="#1b1930"/><path d="M942 114v7" stroke="#1b1930" stroke-width="2"/>'
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
        art = f'<rect x="882" y="65" width="132" height="100" rx="10" fill="#181b27" stroke="{color}" opacity=".22"/><rect x="867" y="50" width="140" height="102" rx="10" fill="#151923" stroke="{color}" stroke-width="2"/><path d="M867 77h140" stroke="{color}" opacity=".35"/><circle cx="881" cy="64" r="3" fill="{color}"/><circle cx="892" cy="64" r="3" fill="{color}" opacity=".55"/><circle cx="903" cy="64" r="3" fill="{color}" opacity=".25"/><path d="m911 95-15 17 15 17m51-34 15 17-15 17m-18-38-14 42" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
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
directions = ''
for x, color, title, line1, line2 in [
    (36, '#88f3cf', 'Веб и интерфейсы', 'Сайты с характером,', '3D и анимации.'),
    (390, '#bba7ff', 'Голос и диалог', 'Плагины для Astra', 'и управление Telegram.'),
    (744, '#f2b99b', 'Интеграции', 'Связываю сервисы', 'в удобные инструменты.'),
]:
    directions += f'''<rect x="{x}" y="164" width="320" height="120" rx="12" fill="#141a26" stroke="#282f40"/>
<circle cx="{x+21}" cy="188" r="3" fill="{color}"/>
<text x="{x+35}" y="195" fill="{color}" font-size="23" font-weight="600">{title}</text>
<text x="{x+20}" y="232" fill="#b5bfd2" font-size="21">{line1}</text>
<text x="{x+20}" y="260" fill="#b5bfd2" font-size="21">{line2}</text>'''

chips = ''
x = 36
for label, width in [('TypeScript', 156), ('React', 110), ('Next.js', 131), ('Go', 80), ('Rust', 97), ('Tauri', 104), ('Python', 122)]:
    chips += f'<rect x="{x}" y="342" width="{width}" height="42" rx="9" fill="#171b2b" stroke="#39364f"/><text x="{x+width/2}" y="370" text-anchor="middle" fill="#ded6f5" font-size="21" class="mono">{label}</text>'
    x += width + 13
svg('about.svg', 460, f'''
<rect x=".5" y=".5" width="1099" height="459" rx="18" fill="url(#panel)" stroke="#2b3041"/>
<text x="36" y="36" fill="#bba7ff" font-size="13" class="mono" letter-spacing="2">BEHIND THE CODE</text>
<text x="36" y="91" fill="#f3f0ff" font-size="42" font-weight="600">Привет, я dwertyfa<tspan fill="#88f3cf">.</tspan></text>
<text x="36" y="132" fill="#bdc5d6" font-size="24">Создаю сайты, плагины и интеграции, которыми удобно пользоваться.</text>
{directions}
<text x="36" y="322" fill="#939eb6" font-size="14" class="mono" letter-spacing="2">МОЙ СТЕК</text>
{chips}
<text x="36" y="427" fill="#939eb6" font-size="20">Графика <tspan fill="#88f3cf">/ Three.js</tspan></text>
<text x="344" y="427" fill="#939eb6" font-size="20">Голосовые плагины <tspan fill="#bba7ff">/ Astra Plugin SDK</tspan></text>
<path class="flow" d="M842 421h222" stroke="url(#accent)" stroke-width="2"/>
''', 'Привет, я dwertyfa. Создаю сайты, плагины и интеграции. Веб: 3D и анимации. Голос: Astra и Telegram. Стек: TypeScript, React, Next.js, Go, Rust, Tauri, Python. Также Three.js и Astra Plugin SDK.')
print('Generated 13 SVG assets.')

# Change each image URL with its content so GitHub cannot reuse stale images.
readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
def version_asset(match):
    path = match.group(1)
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f'src="{path}?v={digest}"'
readme = re.sub(r'src="(\./assets/[^"?]+\.svg)(?:\?[^\"]*)?"', version_asset, readme)
readme_path.write_text(readme, encoding='utf-8')
