#!/usr/bin/env python3
"""Gera os painéis principais do README PHBR63. Somente biblioteca padrão."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'assets' / 'neon-protocol'
BG = '#080C12'
YELLOW = '#FCEE09'
CYAN = '#00F0FF'
RED = '#FF375A'
WHITE = '#F2F6FA'
LINE = '#253442'


def text(x, y, value, size=32, color=WHITE, weight=400, mono=False):
    family = 'DejaVu Sans Mono, monospace' if mono else 'DejaVu Sans, Arial, sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'


def rect(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def path(d, fill):
    return f'<path d="{d}" fill="{fill}"/>'


def save(name, w, h, title, desc, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
           f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
           + rect(0, 0, w, h, BG) + ''.join(body) + '</svg>\n')
    ET.fromstring(svg)
    (DEST / f'{name}.svg').write_text(svg, encoding='utf-8')


def intro(mobile=False):
    title = 'Pedro Zampronha — código que conecta'
    desc = 'Formado em Sistemas de Informação pela ESPM. Desenvolvimento de software, integração de sistemas e dados. Jogos, RPG, animes e realidade virtual também fazem parte dos meus projetos.'
    if mobile:
        w, h = 600, 776
        body = [rect(0, 0, w, 80, YELLOW), text(32, 52, 'PHBR63 // ARQUIVO PESSOAL', 28, BG, 700),
                path('M0 80H600V286L566 320H0Z', CYAN),
                text(32, 150, 'CÓDIGO QUE', 52, BG, 700),
                text(32, 214, 'CONECTA.', 60, BG, 700),
                text(32, 280, 'IDEIAS EM MOVIMENTO', 28, BG, 700, True),
                text(32, 384, 'FORMAÇÃO / ESPM', 28, CYAN, 700, True),
                text(32, 440, 'Sistemas de Informação', 34, WHITE, 700),
                text(32, 520, 'Desenvolvimento de software,', 32),
                text(32, 568, 'integração de sistemas', 32),
                text(32, 616, 'e dados.', 32),
                rect(32, 664, 536, 64, YELLOW),
                text(52, 706, 'JOGOS / RPG / ANIMES / VR', 29, BG, 700),
                rect(0, h-8, w, 8, RED)]
    else:
        w, h = 1200, 496
        body = [rect(0, 0, w, 80, YELLOW), text(40, 52, 'PHBR63 // ARQUIVO PESSOAL', 30, BG, 700),
                rect(1112, 0, 16, 80, BG), rect(1144, 0, 16, 80, BG), rect(1176, 0, 24, 80, RED),
                path('M0 80H424V448L384 488H0Z', CYAN),
                text(40, 167, 'CÓDIGO', 64, BG, 700),
                text(40, 245, 'QUE', 64, BG, 700),
                text(40, 323, 'CONECTA.', 61, BG, 700),
                text(40, 395, 'IDEIAS EM', 26, BG, 700, True),
                text(40, 433, 'MOVIMENTO', 26, BG, 700, True),
                text(480, 144, 'FORMAÇÃO / ESPM', 28, CYAN, 700, True),
                text(480, 202, 'Sistemas de Informação', 36, WHITE, 700),
                text(480, 280, 'Desenvolvimento de software,', 32),
                text(480, 328, 'integração de sistemas e dados.', 32),
                rect(480, 388, 680, 60, YELLOW),
                text(504, 428, 'JOGOS / RPG / ANIMES / VR', 29, BG, 700),
                rect(0, h-8, w, 8, RED)]
    save(f'intro-{"mobile" if mobile else "desktop"}', w, h, title, desc, body)


def heading(name, label, subtitle, number, color, mobile=False):
    w, h = (600, 176) if mobile else (1200, 160)
    accent = RED if color != RED else CYAN
    body = [rect(0, 0, w, h, color), rect(0, 0, 12, h, accent)]
    if mobile:
        body += [rect(32, 32, 64, 64, BG), text(43, 76, number, 35, color, 700, True),
                 text(120, 78, label, 40 if len(label) > 10 else 45, BG, 700),
                 text(32, 144, subtitle, 28, BG, 700, True), rect(w-32, h-32, 32, 32, BG)]
    else:
        body += [rect(40, 40, 80, 80, BG), text(54, 95, number, 43, color, 700, True),
                 text(152, 98, label, 56, BG, 700),
                 text(832, 68, '// PHBR63', 24, BG, 700, True),
                 text(832, 108, subtitle, 22, BG, 700, True),
                 path('M1152 160H1200V112Z', BG)]
    save(f'section-{name}-{"mobile" if mobile else "desktop"}', w, h, label, subtitle, body)


def terminal_mobile():
    body = [rect(0, 0, 12, 260, CYAN), rect(12, 0, 588, 12, CYAN),
            rect(32, 29, 216, 48, YELLOW), text(48, 63, '> @phbr63', 30, BG, 700, True),
            text(34, 123, 'CRIANDO.', 36, WHITE, 700, True),
            text(34, 171, 'EXPERIMENTANDO.', 36, WHITE, 700, True),
            text(34, 219, 'EVOLUINDO.', 36, CYAN, 700, True),
            rect(545, 200, 23, 30, RED), rect(12, 248, 588, 12, YELLOW)]
    save('terminal-mobile', 600, 260, 'Criando. Experimentando. Evoluindo.',
         'Versão estática e legível do terminal de criação de @phbr63.', body)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for mobile in (False, True):
        intro(mobile)
        heading('projects', 'PROJETOS', 'EXPLORAR / CÓDIGO', '02', YELLOW, mobile)
    terminal_mobile()
    print('Painéis principais gerados em assets/neon-protocol.')


if __name__ == '__main__':
    main()
