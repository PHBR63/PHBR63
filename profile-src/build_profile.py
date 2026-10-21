"""Gera os painéis SVG e o README legado a partir do texto aprovado e dos dados públicos."""
from pathlib import Path
from html import escape
import json
import re

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent if SOURCE.name == "profile-src" else SOURCE
ASSETS = ROOT / "assets"
TYPE_PATH = SOURCE / "heading-paths.json"
TYPE = json.loads(TYPE_PATH.read_text(encoding="utf-8")) if TYPE_PATH.exists() else {}
INK, MUTED, CYAN, AMBER = "#eaf5ff", "#9bb2cc", "#70dfff", "#eebc70"


def text(x, y, value, size=26, color=INK, weight=400, extra=""):
    """Recebe posição e rótulo; retorna texto SVG com conteúdo escapado."""
    value = str(value)
    shape = TYPE.get(value) if size >= 30 or (size >= 24 and weight >= 600) else None
    if shape and value != "↗":
        scale = size / shape["units"]
        start = x - shape["width"] * scale if 'text-anchor="end"' in extra else x
        paths = "".join(f'<path transform="translate({g["x"]} 0)" d="{g["d"]}"/>' for g in shape["glyphs"])
        return f'<g fill="{color}" transform="translate({start} {y}) scale({scale} {-scale})"><title>{escape(value)}</title>{paths}</g>'
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def panel(width, height, title, content, subtitle=""):
    """Envolve o conteúdo em um painel de sistema escalável e independente de rede."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#10243b"/><stop offset=".52" stop-color="#091525"/><stop offset="1" stop-color="#101e32"/></linearGradient><radialGradient id="halo"><stop stop-color="#1b94ba" stop-opacity=".22"/><stop offset="1" stop-color="#0a1525" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="url(#bg)" stroke="#2c536e"/>
<ellipse cx="{width*.23}" cy="20" rx="{width*.5}" ry="180" fill="url(#halo)"/>
<path d="M26 48V26h36M{width-62} 26h36v22M26 {height-48}v22h36M{width-62} {height-26}h36v-22" stroke="{CYAN}" stroke-opacity=".65" fill="none"/>
<g font-family="'Segoe UI',Arial,sans-serif">{text(48,72,title,24,CYAN,600, 'letter-spacing="3"')}{text(width-48,72,subtitle,18,MUTED,400,'text-anchor="end"')}
<path d="M48 96H{width-48}" stroke="#31506b"/>{content}</g></svg>'''


def save(name, value):
    """Salva um SVG UTF-8 no diretório de imagens consumido pelo README."""
    (ASSETS / name).write_text(value, encoding="utf-8", newline="\n")


def project(name, description, tech, kind, mobile=False):
    """Monta um cartão de projeto; o README fornece o link clicável externo."""
    width, height = (640, 360) if mobile else (1200, 290)
    icon = '<path d="M0-25 25-12v28L0 30-25 16v-28zM-25-12 0 2 25-12M0 2v28M0-25V2"/>' if kind == "rpg" else '<path d="M-30-20h60M-24-10h48M-19-25v55M19-25v55M-27 8h54"/>'
    content = f'<g transform="translate(80 160)" fill="none" stroke="{CYAN}" stroke-width="2.5">{icon}</g>'
    content += text(140,170,name,46,INK,650)
    if mobile:
        for i,line in enumerate(description):
            content += text(48,228+i*35,line,27,MUTED)
        content += text(48,320,tech,22,CYAN)
    else:
        content += text(140,218," ".join(description),26,MUTED)
        content += text(140,258,tech,22,CYAN)
        content += text(width-48,164,"↗",40,AMBER,400,'text-anchor="end"')
    return panel(width,height,"QUEST LOG",content,"EM DESENVOLVIMENTO" if not mobile else "PROJETO")


SKILLS = [
    ("01", "Back-end e integrações", "Java · Spring Boot · REST", "Swagger · Apache Camel"),
    ("02", "Interfaces web", "React · TypeScript · JavaScript", "HTML · CSS · Tailwind CSS"),
    ("03", "Dados e visualização", "PostgreSQL · MySQL · Oracle", "SQL · Supabase · Tableau"),
    ("04", "Automação e análise", "Python", "Ferramentas para o trabalho diário"),
    ("05", "Jogos e realidade virtual", "C# · Unity", "Experiências e ambientes interativos"),
    ("06", "Versionamento", "Git · GitHub", "Histórico e evolução do código"),
]


def skills(mobile=False):
    """Apresenta competências sem atribuir percentuais ou níveis fictícios."""
    width, height = (640, 1230) if mobile else (1200, 680)
    content = ""
    for i,(number,title,line1,line2) in enumerate(SKILLS):
        x = 38 if mobile else 38+(i%2)*570
        y = 120+i*177 if mobile else 120+(i//2)*174
        cardwidth = 564 if mobile else 554
        content += f'<rect x="{x}" y="{y}" width="{cardwidth}" height="155" rx="10" fill="#0d2033" stroke="#24465e"/>'
        content += text(x+22,y+37,number,18,AMBER,600)
        content += text(x+66,y+38,title,27,INK,600)
        content += text(x+24,y+88,line1,25,CYAN)
        content += text(x+24,y+124,line2,23,MUTED)
    return panel(width,height,"SKILL RECORDS",content,"TECNOLOGIAS")


def activity(user, mobile=False):
    """Renderiza uma fotografia datada das contribuições públicas do GitHub."""
    calendar = user["contributionsCollection"]["contributionCalendar"]
    width,height = (640,520) if mobile else (1200,500)
    content=""
    values=[(user["repositories"]["totalCount"],"REPOSITÓRIOS PÚBLICOS"),(calendar["totalContributions"],"CONTRIBUIÇÕES NA JANELA")]
    for i,(number,label) in enumerate(values):
        x=48+i*(280 if mobile else 560)
        content += text(x,188,number,70,INK,300)
        content += text(x,228,label,16,CYAN,600)
    weeks=calendar["weeks"]
    cell,gap=(8,2) if mobile else (16,4)
    top=290 if mobile else 270
    for col,week in enumerate(weeks):
        for row,day in enumerate(week["contributionDays"]):
            count=day["contributionCount"]
            fill="#112a3c" if count==0 else ("#24627b" if count<5 else "#38a7c8" if count<20 else CYAN)
            content += f'<rect x="{48+col*(cell+gap)}" y="{top+row*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{fill}"><title>{day["date"]}: {count} contribuições</title></rect>'
    dates=[d["date"] for w in weeks for d in w["contributionDays"]]
    lines=["DADOS DO GITHUB · CONSULTA EM 21/10/2026",f'{dates[0]} a {dates[-1]} · Atualização por geração']
    for i,line in enumerate(lines):
        content += text(48,(430 if mobile else 440)+i*30,line,18,MUTED)
    return panel(width,height,"ACTIVITY RECORD",content,"SNAPSHOT" if mobile else "DADOS PÚBLICOS")


def picture(base, alt):
    """Gera marcação compatível com o GitHub, com variante para telas pequenas."""
    return f'<picture>\n  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./assets/{base}-mobile.svg">\n  <source media="(prefers-color-scheme: dark)" srcset="./assets/{base}.svg">\n  <source media="(max-width: 600px)" srcset="./assets/{base}-light-mobile.svg">\n  <img src="./assets/{base}-light.svg" width="100%" alt="{escape(alt)}">\n</picture>'


def main():
    """Lê as fontes locais e gera SVGs e README.legacy.md, sem alterar o README da raiz."""
    ASSETS.mkdir(exist_ok=True)
    payload=json.loads((SOURCE/"github-public-data.json").read_text(encoding="utf-8-sig"))
    user=payload.get("data",{}).get("user")
    if not user or user.get("login")!="PHBR63":
        raise ValueError("Dados públicos ausentes ou pertencentes a outro perfil.")
    for mobile in [False,True]:
        suffix="-mobile" if mobile else ""
        save(f"quest-lets-roll{suffix}.svg",project("Let's Roll",["RPG de mesa online.","Campanhas, regras e interação."],"React · TypeScript · Supabase","rpg",mobile))
        save(f"quest-anime-check{suffix}.svg",project("Anime Check",["Organização e descoberta de animes.","Interfaces, APIs e informações."],"React · TypeScript · APIs","anime",mobile))
        save(f"skill-records{suffix}.svg",skills(mobile))
        save(f"activity-record{suffix}.svg",activity(user,mobile))
    strip='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="88" viewBox="0 0 1200 88" role="img" aria-label="PHBR63 · Software, integrações e dados"><style>@keyframes travel{to{stroke-dashoffset:-1200}}.signal{animation:travel 12s linear infinite}@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style><path d="M0 18h1200" stroke="#264a64"/><path class="signal" d="M0 18h1200" stroke="#70dfff" stroke-width="2" stroke-dasharray="80 1120"/><g font-family="Segoe UI,Arial,sans-serif" font-size="22" fill="#9bb2cc"><text x="0" y="62">PHBR63 / DEVELOPER PROFILE</text><text x="1200" y="62" text-anchor="end" fill="#eebc70">CODE · BUILD · EXPLORE</text></g></svg>'''
    save("system-link.svg",strip)
    palette = {"#eaf5ff":"#212933", "#9bb2cc":"#596873", "#70dfff":"#ad7900", "#eebc70":"#169ab8", "#10243b":"#fffdf5", "#091525":"#f6fafc", "#101e32":"#f3f8fb", "#2c536e":"#d5dfe5", "#1b94ba":"#ead88c", "#0a1525":"#f9fbfd", "#31506b":"#dce4e9", "#0d2033":"#ffffff", "#24465e":"#e0e7ec", "#112a3c":"#e5edf1", "#24627b":"#f0d582", "#38a7c8":"#dfaf32"}
    for asset in list(ASSETS.glob("*.svg")):
        if "-light" in asset.stem or asset.name == "aincrad-header.svg":
            continue
        content = asset.read_text(encoding="utf-8")
        light = re.sub("|".join(map(re.escape,palette)), lambda m: palette[m.group()], content, flags=re.IGNORECASE)
        name = asset.stem.replace("-mobile", "-light-mobile") if "-mobile" in asset.stem else asset.stem+"-light"
        save(name+".svg",light)
    approved=(SOURCE/"texto-aprovado.md").read_text(encoding="utf-8").strip()
    readme=f'''<p align="center"><img src="./assets/aincrad-hero-reference.png" width="100%" alt="Pedro Zampronha. Arte de Aincrad com castelo flutuante sobre as nuvens e menu holográfico Link Start."></p>

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/system-link.svg"><img src="./assets/system-link-light.svg" width="100%" alt="PHBR63 · Code, build, explore"></picture>

<p align="center"><b>Desenvolvimento de software · Integrações · Dados · Experiências interativas</b><br><sub>Java e Spring Boot no back-end. Interfaces, dados e mundos interativos nos projetos.</sub></p>

<p align="center"><a href="#quest-log">Projetos</a> · <a href="#skill-records">Tecnologias</a> · <a href="#activity-record">Atividade</a> · <a href="#player-profile">Sobre mim</a></p>

<a id="quest-log"></a>
<details open>
<summary><b>⚔️ Quest Log · Projetos em desenvolvimento</b></summary>
<br>

<a href="https://github.com/PHBR63/lets-roll-cursor">
{picture('quest-lets-roll',"Let's Roll — RPG de mesa online. Abrir repositório.")}
</a>

<a href="https://github.com/PHBR63/anime-check">
{picture('quest-anime-check',"Anime Check — Organização e descoberta de animes. Abrir repositório.")}
</a>

<sub>Projetos em desenvolvimento e experimentações, com diferentes estágios de maturidade.</sub>
</details>

<a id="skill-records"></a>
<details open>
<summary><b>🗡️ Skill Records · Tecnologias e ferramentas</b></summary>
<br>

{picture('skill-records','Back-end: Java e Spring Boot. Web: React e TypeScript. Dados: SQL e Tableau. Automação: Python. Jogos: C# e Unity. Versionamento: Git e GitHub.')}

Escolho as ferramentas de acordo com o problema, considerando a complexidade da solução e o trabalho necessário para mantê-la.
</details>

<a id="activity-record"></a>
<details open>
<summary><b>💠 Activity Record · Atividade no GitHub</b></summary>
<br>

{picture('activity-record',f'{user["repositories"]["totalCount"]} repositórios públicos e {user["contributionsCollection"]["contributionCalendar"]["totalContributions"]} contribuições na janela consultada. Dados coletados em 21/10/2026.')}

<sub>Fotografia dos dados públicos consultados em 21/10/2026; não é um indicador em tempo real.</sub>
</details>

<a id="player-profile"></a>
<details>
<summary><b>👤 Player Profile · Minha trajetória, experiência e forma de trabalhar</b></summary>
<br>

{approved}

</details>

<p align="center"><br><b>O próximo projeto começa com uma boa ideia.</b><br><sub>Software, RPG, animes e realidade virtual fazem parte do caminho.</sub><br><br><a href="https://github.com/PHBR63?tab=repositories">Explorar meus repositórios</a></p>

<p align="center"><sub>PHBR63 · Inspirado em Sword Art Online / Aincrad · Sem vínculo oficial.<br>Referências: <a href="https://aincrad-archive.hecate2.chatgpt.site/">Aincrad Memory Archive</a> · <a href="https://wallpapersafari.com/w/F8j0Gb">Wallpaper de Aincrad</a>. Arte do cabeçalho adaptada com IA.</sub></p>
'''
    (SOURCE/"README.legacy.md").write_text(readme,encoding="utf-8",newline="\n")
    for name in re.findall(r'(?:src|srcset)="\./assets/([^"]+)"',readme):
        if not (ASSETS/name).is_file():
            raise FileNotFoundError(f"Imagem referenciada não encontrada: {name}")
    print(f"Gerados README.legacy.md e {len(list(ASSETS.glob('*')))} arquivos visuais.")


if __name__ == "__main__":
    main()

