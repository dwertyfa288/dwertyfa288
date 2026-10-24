from .theme import SIGNAL, PAPER

REPO_TOTAL = 99
LANGUAGE_COUNT = 13
LANGUAGES = [
    ('Python', 29, SIGNAL),
    ('Java', 19, PAPER),
    ('TypeScript', 14, '#b9b7b0'),
    ('JavaScript', 12, '#8d8b85'),
    ('Kotlin', 5, '#62605a'),
    ('другие', 18, '#3d3c38'),
]
HIGHLIGHTS = [
    (LANGUAGE_COUNT, '', 'языков', 'Python · Java · TS · Rust · Go'),
    (5, '', 'живых сайтов', 'лендинги · продукты · портфолио'),
    (3, '', 'плагина для Astra', 'TG · Interject · PrimeAI'),
]
STATS_META = 'github · октябрь 2026'

LINKS = [
    ('link-telegram', 'Telegram', '@dwertyfa', 'https://t.me/dwertyfa'),
    ('link-portfolio', 'Портфолио', 'dwertyfa288.github.io/dwertyfa', 'https://dwertyfa288.github.io/dwertyfa/'),
    ('link-sphereprime', 'SpherePrime', 'github.com/SpherePrime', 'https://github.com/SpherePrime'),
]

SECTIONS = {
    'voice': ('01', 'Голос и Astra', 'Плагины, которые слушают, говорят и держат контекст разговора.', '02 ПРОЕКТА'),
    'prime': ('02', 'SpherePrime', 'Инструменты для разработчиков и AI: терминал, десктоп, роутинг, прокси.', '04 ПРОЕКТА'),
    'web': ('03', 'Веб', 'Сайты с характером — от лендингов до целых продуктов.', '05 ПРОЕКТОВ'),
}

PROJECTS = {
    'telegram': dict(
        kind='ASTRA PLUGIN · TS', title='TG for Astra', art='telegram',
        lines=['Telegram голосом: озвучка сообщений, голосовые', 'и ответы под диктовку. Рассылки и автоответы.'],
        chips=['TypeScript', 'Astra SDK', 'MTProto'],
        url='https://github.com/dwertyfa288/dwertyfa-astra-tg',
        alt='TG for Astra — Telegram голосом: озвучка сообщений, голосовые и ответы под диктовку. Открыть репозиторий.'),
    'interject': dict(
        kind='ASTRA PLUGIN · TS', title='Astra Interject', art='interject',
        lines=['Продолжение диалога после ответа Astra —', 'без повторного триггерного слова.'],
        chips=['TypeScript', 'getUserMedia', 'VAD'],
        url='https://github.com/dwertyfa288/astra-interject',
        alt='Astra Interject — продолжение диалога после ответа Astra без повторного триггерного слова. Открыть репозиторий.'),
    'cli': dict(
        kind='SPHEREPRIME · GO', title='Prime CLI', art='cli',
        lines=['Агентный AI-ассистент для кода в терминале.', 'Любые модели, MCP и LSP-контекст, сессии,', '12 дизайнов интерфейса и голосовой ввод.'],
        chips=['Go', 'MCP', 'LSP', 'Multi-model'],
        cta='репозиторий', url_label='github.com/SpherePrime/CLI',
        url='https://github.com/SpherePrime/CLI',
        alt='Prime CLI — агентный AI-ассистент для кода в терминале: любые модели, MCP, LSP. Go. Открыть репозиторий SpherePrime.'),
    'desktop': dict(
        kind='SPHEREPRIME · TAURI', title='Prime Desktop', art='desktop',
        lines=['Десктоп-воркспейс Prime для Windows и Linux:', 'проекты, чаты, апрувы, диффы, терминалы,', 'SSH, автоматизации, MCP/LSP/Skills и голос.'],
        chips=['Rust', 'Tauri', 'React', 'Go engine'],
        cta='репозиторий', url_label='github.com/SpherePrime/CLI/desktop',
        url='https://github.com/SpherePrime/CLI/tree/main/desktop',
        alt='Prime Desktop — десктоп-воркспейс Prime для Windows и Linux на Rust/Tauri и React: проекты, чаты, диффы, терминалы, SSH, MCP и голос. Открыть исходники.'),
    'primeai': dict(
        kind='SPHEREPRIME · TS', title='PrimeAI', art='router',
        lines=['AI-провайдер для Astra: Router API сам выбирает', 'маршрут, повторяет запросы и знает vision-модели.'],
        chips=['TypeScript', 'Bun', 'Router API'],
        url='https://github.com/SpherePrime/PrimeAi',
        alt='PrimeAI — AI-провайдер для Astra с автоматической маршрутизацией через Router API. Открыть репозиторий SpherePrime.'),
    'proxy': dict(
        kind='SPHEREPRIME · RUST', title='PrimeProxy', art='proxy',
        lines=['Локальный MTProto-прокси для Telegram', 'с WebSocket-транспортом. Быстро и тихо.'],
        chips=['Rust', 'MTProto', 'WebSocket'],
        url='https://github.com/SpherePrime/PrimeProxy',
        alt='PrimeProxy — локальный MTProto-прокси для Telegram с WebSocket-транспортом. Rust. Открыть репозиторий SpherePrime.'),
    'portfolio': dict(
        kind='PORTFOLIO · NEXT.JS', title='Портфолио', art='portfolio',
        lines=['Интерактивное портфолио с 3D-сценой,', 'плавной анимацией и живыми проектами.', 'Всё, что не влезло в этот README.'],
        chips=['Next.js', 'React', 'Three.js'],
        cta='открыть сайт', url_label='dwertyfa288.github.io/dwertyfa',
        url='https://dwertyfa288.github.io/dwertyfa/',
        alt='Портфолио dwertyfa — интерактивное портфолио на Next.js, React и Three.js. Открыть сайт.'),
    'nova': dict(
        kind='САЙТ · ЖИЛОЙ ДОМ', title='Nova Prestige', art='nova',
        lines=['Промо-сайт жилого дома: атмосфера,', 'адаптив и анимации на каждом экране.'],
        chips=['Landing', 'Motion', 'Adaptive'],
        url='https://novaprestige.ru/',
        alt='Nova Prestige — промо-сайт жилого дома: атмосфера, адаптив и анимации. Открыть сайт.'),
    'roxy': dict(
        kind='ПРОДУКТ · VPN', title='Roxy Boost', art='globe',
        lines=['VPN-продукт целиком: инфраструктура,', 'приложения и сайт.'],
        chips=['VPN', 'Apps', 'Infra'],
        url='https://roxyvpn.ru/',
        alt='Roxy Boost — VPN-продукт: инфраструктура, приложение и сайт. Открыть сайт.'),
    'danek': dict(
        kind='ПОРТФОЛИО · ВИДЕО', title='danek montage', art='timeline',
        lines=['Портфолио видеомонтажёра', 'с акцентом на движение и ритм.'],
        chips=['Web', 'Motion', 'Video'],
        url='https://fazedanek-hub.github.io/danekmontage/',
        alt='danek montage — портфолио видеомонтажёра с акцентом на движение. Открыть сайт.'),
    'ksusha': dict(
        kind='ЛЕНДИНГ · ИНТЕНСИВ', title='Hey Ksusha', art='landing',
        lines=['Лендинг интенсива с записью', 'и платёжной интеграцией.'],
        chips=['Landing', 'Payments', 'Forms'],
        url='https://heyksusha.ru/intensive',
        alt='Hey Ksusha — лендинг интенсива с записью и платёжной интеграцией. Открыть сайт.'),
}

LAYOUT = [
    ('hero',),
    ('links',),
    ('stats',),
    ('section', 'voice'),
    ('pair', 'telegram', 'interject'),
    ('section', 'prime'),
    ('wide', 'cli'),
    ('wide', 'desktop'),
    ('pair', 'primeai', 'proxy'),
    ('section', 'web'),
    ('wide', 'portfolio'),
    ('pair', 'nova', 'roxy'),
    ('pair', 'danek', 'ksusha'),
    ('footer',),
]
