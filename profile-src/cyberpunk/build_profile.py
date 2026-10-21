"""Gera o perfil Cyberpunk legado a partir do texto aprovado e de dados públicos locais."""
from pathlib import Path
from html import escape
import json
import re

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1] if SOURCE.name == 'cyberpunk' and SOURCE.parent.name == 'profile-src' else SOURCE
ASSETS = ROOT / 'assets' / 'cyberpunk'
TYPE_FILE = SOURCE / 'title-paths.json'
TYPE = json.loads(TYPE_FILE.read_text(encoding='utf-8')) if TYPE_FILE.exists() else {}
YELLOW, CYAN, RED, WHITE, MUTED = '#fcee0a', '#00e5ff', '#ff3c54', '#edf3f5', '#a3b2bc'
DATE = '21/10/2026'


def label(x, y, value, size=28, color=WHITE, bold=False, anchor='start'):
    """Recebe texto e posição; retorna texto escapado ou contornos já preparados."""
    value = str(value)
    shape = TYPE.get(value) if bold or size >= 65 else None
    if shape:
        scale = size / shape['units']
        offset = shape['width'] * scale if anchor == 'end' else 0
        paths = ''.join(f'<path transform="translate({g["x"]} 0)" d="{g["d"]}"/>' for g in shape['glyphs'])
        return f'<g fill="{color}" transform="translate({x-offset} {y}) scale({scale} {-scale})"><title>{escape(value)}</title>{paths}</g>'
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>'


def frame(width, height, title, content, note=''):
    """Monta um painel angular autônomo, sem scripts, imagens ou fontes externas."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<path d="M18 1H{width-1}V{height-24}L{width-24} {height-1}H1V18Z" fill="#0b1014" stroke="#36505b"/>
<path d="M18 1H450L425 64H1V18Z" fill="{YELLOW}"/>
<path d="M{width-140} 1h100l-18 14h-100z" fill="{CYAN}"/>
<path d="M1 {height-28}h10v27H1zM22 {height-10}h70v9H22z" fill="{YELLOW}"/>
<g font-family="'Segoe UI',Arial,sans-serif">{label(30,45,title,32,'#080a0d',True)}{label(width-28,44,note,18,MUTED,anchor='end')}{content}</g></svg>'''


def write(name, content):
    """Salva um SVG UTF-8 na pasta de imagens do perfil."""
    (ASSETS / name).write_text(content, encoding='utf-8', newline='\n')


def project(name, lines, tech, number, mobile=False):
    """Gera um cartão; o README contém o link do repositório correspondente."""
    width, height = (640, 350) if mobile else (1200, 245)
    content = label(34,138,name,54,YELLOW,True)
    for index,line in enumerate(lines if mobile else [' '.join(lines)]):
        content += label(34,191+index*37,line,27 if mobile else 30,MUTED)
    content += label(34,290 if mobile else 220,tech,23,CYAN)
    content += f'<path d="M{width-86} 108h45v45M{width-86} 153l45-45" fill="none" stroke="{RED}" stroke-width="4"/>'
    return frame(width,height,'PROJECT INDEX',content,f'REPO / {number:02}')


SKILLS = [
    ('BACK-END','Java · Spring Boot','REST · Swagger · Camel'),
    ('FRONT-END','React · TypeScript','JavaScript · HTML · CSS · Tailwind'),
    ('DADOS','SQL · PostgreSQL · MySQL','Oracle · Supabase · Tableau'),
    ('AUTOMAÇÃO','Python','Ferramentas para o trabalho diário'),
    ('JOGOS / VR','C# · Unity','Experiências interativas'),
    ('VERSIONAMENTO','Git · GitHub','Histórico e evolução do código'),
]


def skills(mobile=False):
    """Exibe tecnologias por responsabilidade, sem notas de proficiência fictícias."""
    width,height = (640,1090) if mobile else (1200,470)
    content = ''
    for index,(title,line1,line2) in enumerate(SKILLS):
        x = 34 if mobile else 30+(index%3)*390
        y = 106+index*158 if mobile else 112+(index//3)*170
        content += f'<path d="M{x} {y}h{560 if mobile else 350}" stroke="{CYAN}" stroke-width="2"/>'
        content += label(x,y+37,title,31,YELLOW,True)
        content += label(x,y+80,line1,28 if mobile else 25)
        content += label(x,y+118,line2,24 if mobile else 21,MUTED)
    return frame(width,height,'CYBERWARE',content,'TECNOLOGIAS')


def statistics(user, streak, mobile=False):
    """Apresenta contagens verificadas no snapshot público recebido pelo gerador."""
    width,height = (640,490) if mobile else (1200,285)
    values = [(user['repositories']['totalCount'],'REPOSITÓRIOS PÚBLICOS'),(user['contributionsCollection']['contributionCalendar']['totalContributions'],'CONTRIBUIÇÕES NA JANELA'),(streak,'DIAS / MAIOR SEQUÊNCIA')]
    content = ''
    for index,(value,title) in enumerate(values):
        x = 34 if mobile else 34+index*390
        y = 165+index*124 if mobile else 185
        content += label(x,y,value,84,YELLOW,True)
        content += label(175 if mobile else x,y-18 if mobile else 225,title,21,CYAN)
    content += label(width-28,height-22,f'SNAPSHOT / {DATE}',17,MUTED,anchor='end')
    return frame(width,height,'DATA SHARD',content,'GITHUB')


def activity(weeks, mobile=False):
    """Desenha o calendário com as contagens originais, incluindo dias sem atividade."""
    width,height = (640,245) if mobile else (1200,325)
    cell,gap = (8,2) if mobile else (18,3)
    content = ''
    for column,week in enumerate(weeks):
        for row,day in enumerate(week['contributionDays']):
            count = day['contributionCount']
            color = '#1c2d35' if count == 0 else '#14627a' if count < 5 else CYAN if count < 20 else YELLOW
            content += f'<rect x="{34+column*(cell+gap)}" y="{102+row*(cell+gap)}" width="{cell}" height="{cell}" fill="{color}"><title>{day["date"]}: {count} contribuições</title></rect>'
    content += label(34,height-35,'Registros públicos do GitHub',20,MUTED)
    content += label(width-28,height-35,DATE,20,CYAN,anchor='end')
    return frame(width,height,'SIGNAL TRACE',content,'ATIVIDADE')


def picture(name, alt):
    """Seleciona a imagem adequada à largura sem depender de estilos personalizados."""
    return f'<picture><source media="(max-width: 600px)" srcset="./assets/cyberpunk/{name}-mobile.svg"><img src="./assets/cyberpunk/{name}.svg" width="100%" alt="{escape(alt)}"></picture>'


def main():
    """Valida fontes e gera SVGs e README.legacy.md, sem alterar o README da raiz."""
    ASSETS.mkdir(parents=True,exist_ok=True)
    user = json.loads((SOURCE/'github-public-data.json').read_text(encoding='utf-8-sig')).get('data',{}).get('user')
    if not user or user.get('login') != 'PHBR63':
        raise ValueError('Dados públicos ausentes ou pertencentes a outra conta.')
    calendar = user['contributionsCollection']['contributionCalendar']
    days = [day for week in calendar['weeks'] for day in week['contributionDays']]
    current = longest = 0
    for day in days:
        current = current+1 if day['contributionCount'] else 0
        longest = max(longest,current)
    for mobile in [False,True]:
        suffix = '-mobile' if mobile else ''
        write(f'lets-roll{suffix}.svg',project("LET'S ROLL",['RPG de mesa online.','Campanhas, regras e interação.'],'React · TypeScript · Supabase',1,mobile))
        write(f'anime-check{suffix}.svg',project('ANIME CHECK',['Organização e descoberta de animes.','Interfaces, APIs e informações.'],'React · TypeScript · APIs',2,mobile))
        write(f'stack{suffix}.svg',skills(mobile))
        write(f'stats{suffix}.svg',statistics(user,longest,mobile))
        write(f'activity{suffix}.svg',activity(calendar['weeks'],mobile))
    contact = label(34,139,'PHBR63 // GITHUB',52,YELLOW,True)+label(34,190,'Desenvolvimento, integrações e dados.',28,MUTED)
    write('contact.svg',frame(1200,235,'CONTACT',contact,'PERFIL PESSOAL'))
    strip = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="70" viewBox="0 0 1200 70" role="img" aria-label="PHBR63 · Code, build, repeat"><style>@keyframes move{{to{{stroke-dashoffset:-1200}}}}.signal{{animation:move 14s linear infinite}}@media(prefers-reduced-motion:reduce){{.signal{{animation:none}}}}</style><path d="M0 12h1200" stroke="#34434a"/><path class="signal" d="M0 12h1200" stroke="{CYAN}" stroke-width="2" stroke-dasharray="80 1120"/><g font-family="monospace" font-size="20" fill="{CYAN}"><text x="0" y="53">PHBR63 // PERSONAL SYSTEM</text><text x="1200" y="53" text-anchor="end">CODE. BUILD. REPEAT.</text></g></svg>'''
    write('signal.svg',strip)
    about = (SOURCE/'about.md').read_text(encoding='utf-8').strip()
    sections = [
        ('projetos','📌 Projetos em destaque',f'<a href="https://github.com/PHBR63/lets-roll-cursor">{picture("lets-roll", "Let’s Roll — abrir repositório de RPG de mesa online")}</a>\n\n<a href="https://github.com/PHBR63/anime-check">{picture("anime-check", "Anime Check — abrir repositório de organização e descoberta de animes")}</a>\n\nProjetos em desenvolvimento e experimentações, com diferentes estágios de maturidade.',True),
        ('stack','🧰 Tecnologias e ferramentas',picture('stack','Back-end: Java e Spring Boot. Web: React e TypeScript. Dados: SQL e Tableau. Automação: Python. Jogos: C# e Unity. Versionamento: Git e GitHub.'),False),
        ('numeros','📊 Em números',picture('stats',f'{user["repositories"]["totalCount"]} repositórios públicos; {calendar["totalContributions"]} contribuições na janela; maior sequência de {longest} dias.')+f'\n\n<sub>Dados consultados em {DATE}. Fotografia da janela retornada pelo GitHub; atualização por geração.</sub>',False),
        ('atividade','🟩 Atividade no GitHub',picture('activity','Calendário das contribuições públicas consultadas em 21/10/2026.'),False),
        ('sobre','👤 Sobre mim e minha experiência',about,False),
        ('contato','👋 Onde me encontrar','<a href="https://github.com/PHBR63"><img src="./assets/cyberpunk/contact.svg" width="100%" alt="PHBR63 — perfil no GitHub"></a>',False),
    ]
    blocks = '\n\n'.join(f'<a id="{key}"></a>\n<details{" open" if opened else ""}>\n<summary><b>{title}</b></summary>\n<br>\n\n{body}\n\n</details>' for key,title,body,opened in sections)
    readme = f'''<p align="center"><img src="./assets/cyberpunk/hero.png" width="100%" alt="Pedro Zampronha / PHBR63. Cabeçalho amarelo e preto inspirado em Cyberpunk 2077, com cenário urbano neon."></p>

<img src="./assets/cyberpunk/signal.svg" width="100%" alt="PHBR63 · Code, build, repeat">

<p align="center"><b>Pedro Zampronha · Desenvolvimento de software, integrações e dados</b><br><sub>Java / Spring Boot · React / TypeScript · Python / SQL</sub></p>

<p align="center"><a href="#projetos">Projetos</a> · <a href="#stack">Stack</a> · <a href="#atividade">Atividade</a> · <a href="#sobre">Sobre mim</a></p>

{blocks}

<p align="center"><sub>Identidade visual inspirada em <a href="https://www.cyberpunk.net/br/pt-br/cyberpunk-2077">Cyberpunk 2077</a>. Arte do cabeçalho criada com IA. Perfil pessoal, sem vínculo oficial com CD PROJEKT RED.</sub></p>
'''
    for filename in re.findall(r'(?:src|srcset)="\./assets/cyberpunk/([^"]+)"',readme):
        if not (ASSETS/filename).is_file():
            raise FileNotFoundError(f'Imagem referenciada ausente: {filename}')
    (SOURCE/'README.legacy.md').write_text(readme,encoding='utf-8',newline='\n')
    print(json.dumps({'public_repos':user['repositories']['totalCount'],'contributions':calendar['totalContributions'],'longest_streak':longest,'visuals':len(list(ASSETS.glob('*')))}))


if __name__ == '__main__':
    main()

