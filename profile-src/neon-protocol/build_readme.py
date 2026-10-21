#!/usr/bin/env python3
"""Monta o README gráfico e mantém uma leitura completa em Markdown nativo."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[2]
ART = './assets/neon-protocol'
YELLOW = './assets/yellow-protocol'


def picture(name, alt):
    return f'''<picture>
  <source media="(max-width: 600px)" srcset="{ART}/{name}-mobile.svg">
  <img src="{ART}/{name}-desktop.svg" width="100%" alt="{escape(alt, quote=True)}">
</picture>'''


def project(key, repo, cover, name, alt):
    return f'''<p>
<a href="https://github.com/PHBR63/{repo}">
  <img src="{cover}" width="100%" alt="Capa ilustrada de {escape(name, quote=True)}. Abrir o repositório.">
  {picture(f'project-{key}', alt)}
</a>
</p>'''


def main():
    blocks = [f'''<picture>
  <source media="(max-width: 600px)" srcset="{YELLOW}/banners/banner-compacto.webp">
  <img src="{YELLOW}/banners/banner-principal.webp" width="100%" alt="Pedro Zampronha — @phbr63. Desenvolvimento, experimentação e projetos. Identidade visual inspirada em Cyberpunk 2077.">
</picture>''',
    picture('intro', 'Pedro Zampronha. Formado em Sistemas de Informação pela ESPM. Desenvolvimento de software, integração de sistemas e dados. Interesses em jogos, RPG, animes e realidade virtual.'),
    f'''<picture>
  <source media="(max-width: 600px) and (prefers-reduced-motion: no-preference)" srcset="{ART}/terminal-mobile.gif">
  <source media="(max-width: 600px)" srcset="{ART}/terminal-mobile.svg">
  <source media="(prefers-reduced-motion: no-preference)" srcset="{YELLOW}/animacoes/terminal-conexao.gif">
  <img src="{YELLOW}/animacoes/terminal-conexao.png" width="100%" alt="Criando. Experimentando. Evoluindo.">
</picture>''',
    picture('stack', 'Tecnologias por área: back-end e integrações — Java, Spring Boot, APIs REST e Apache Camel; web — React, TypeScript, HTML, CSS e Tailwind CSS; dados — SQL, PostgreSQL, MySQL, Oracle, Supabase e Tableau; automação — Python; jogos e realidade virtual — C# e Unity; versionamento — Git e GitHub.'),
    picture('section-projects', 'Projetos — explorar o código.'),
    project('3dgame', '3dGame', f'{YELLOW}/projetos/projeto-3dgame.webp', '3dGame', '3dGame — Jogo da turma da ESPM. Abrir repositório.'),
    project('vr', 'jogo-vr', f'{YELLOW}/projetos/projeto-jogo-vr.webp', 'jogo-vr', 'jogo-vr — Unity e C#. Projeto de jogo em realidade virtual. Abrir repositório.'),
    project('roll', 'lets-roll-cursor', f'{YELLOW}/projetos/projeto-lets-roll-cursor.webp', "Let's Roll", "Let's Roll — React, TypeScript e Supabase. Plataforma para RPG de mesa online, em desenvolvimento. Abrir repositório."),
    project('anime', 'anime-check', f'{ART}/projeto-anime-check.webp', 'Anime Check', 'Anime Check — Organização e descoberta de animes. Abrir repositório.'),
    picture('about', 'Minha trajetória reúne desenvolvimento, integração de sistemas e dados. Experiência com Java, Spring Boot e APIs REST. No setor financeiro, trabalhei com cobrança, modernização de aplicações e correção de vulnerabilidades. Interesses em jogos, RPG, animes e realidade virtual.'),
    f'''<picture>
  <source media="(prefers-reduced-motion: no-preference)" srcset="{YELLOW}/animacoes/divisoria-scan.gif">
  <img src="{YELLOW}/animacoes/divisoria-scan.png" width="100%" alt="">
</picture>''',
    f'''<a href="https://github.com/PHBR63?tab=repositories">
{picture('footer', 'Ver todos os repositórios de @phbr63 no GitHub.')}
</a>''',
    '''<details>
<summary><b>Ler perfil em texto — apresentação, tecnologias e projetos</b></summary>

## Pedro Zampronha

Sou **Pedro Zampronha**, formado em Sistemas de Informação pela **ESPM**. Trabalho com desenvolvimento de software, integração de sistemas e dados. Gosto de conectar a necessidade de quem usa, a regra de negócio, a interface, a API e os dados.

Jogos, RPG, animes e realidade virtual também fazem parte desse percurso — e frequentemente viram projetos.

### Tecnologias e ferramentas

Tecnologias presentes na minha experiência e nos meus projetos. Escolho as ferramentas considerando o problema, a complexidade da solução e o trabalho necessário para mantê-la.

| Área | Tecnologias e ferramentas |
| :--- | :--- |
| Back-end e integrações | Java · Spring Boot · APIs REST · Swagger · Apache Camel |
| Desenvolvimento web | JavaScript · TypeScript · React · HTML · CSS · Tailwind CSS |
| Dados e bancos | SQL · PostgreSQL · MySQL · Oracle · Supabase · Tableau |
| Automação e análise | Python |
| Jogos e realidade virtual | C# · Unity |
| Versionamento | Git · GitHub |

### Projetos

#### 01 · 3dGame

**Jogo da turma da ESPM.** Um registro de desenvolvimento de jogos em 3D.

[Explorar o código de 3dGame →](https://github.com/PHBR63/3dGame)

#### 02 · jogo-vr

**Unity · C#** — Projeto de jogo em realidade virtual, explorando experiências interativas.

[Explorar o código de jogo-vr →](https://github.com/PHBR63/jogo-vr)

#### 03 · Let's Roll

**React · TypeScript · Supabase** — Plataforma em desenvolvimento para RPG de mesa online, com organização de campanhas e recursos para mestres e jogadores.

[Explorar o código de Let's Roll →](https://github.com/PHBR63/lets-roll-cursor)

#### 04 · Anime Check

Projeto voltado à organização e descoberta de animes.

[Explorar o código de Anime Check →](https://github.com/PHBR63/anime-check)

Os projetos estão em diferentes estágios de desenvolvimento. As capas são ilustrações conceituais de apresentação.

### Experiência e forma de trabalhar

Minha trajetória reúne desenvolvimento de software, integração de sistemas, análise de dados e experiência com infraestrutura e liderança técnica.

Tenho experiência com back-end em **Java e Spring Boot**, criação e documentação de APIs REST, integração entre sistemas e modernização de aplicações. Minha passagem pelo setor financeiro incluiu projetos de cobrança, atualização de tecnologias e correção de vulnerabilidades.

Também trabalho com aplicações web, automação e visualização de dados. Gosto de transformar informações dispersas em interfaces, análises e ferramentas que facilitem o trabalho e apoiem decisões.

Valorizo código legível, responsabilidades bem definidas e documentação que explique o caminho dos dados e o motivo das decisões. Procuro compreender o contexto, fazer mudanças objetivas e validar o comportamento esperado. Uso ferramentas de inteligência artificial como apoio à pesquisa e ao desenvolvimento, mantendo a revisão crítica sobre o resultado.

[Todos os repositórios](https://github.com/PHBR63?tab=repositories) · [Atividade no GitHub](https://github.com/PHBR63?tab=overview)

</details>''',
    '''<p align="center">
  <sub>Identidade visual inspirada em <a href="https://www.cyberpunk.net/br/pt-br/cyberpunk-2077">Cyberpunk 2077</a>. Capas conceituais criadas com IA.</sub>
</p>''']
    (ROOT / 'README.md').write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')
    print('README.md atualizado: Neon Protocol / PHBR63.')


if __name__ == '__main__':
    main()
