#!/usr/bin/env python3
"""Gera os 14 painéis SVG secundários do perfil PHBR63.

Os SVGs finais são independentes: sem imagens, fontes remotas, scripts ou
foreignObject. Pillow é usado somente na geração, para medir e validar texto.
Execute com: python profile-src/neon-protocol/build_secondary.py
"""

from __future__ import annotations

from html import escape
from pathlib import Path
import json
import xml.etree.ElementTree as ET

from PIL import ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "neon-protocol"
BG = "#080C12"
YELLOW = "#FCEE09"
CYAN = "#00F0FF"
RED = "#FF375A"
MAGENTA = "#F35CDB"
WHITE = "#EDF3FA"
MUTED = "#B9CCD7"
DARK_CYAN = "#123440"
DARK_BLUE = "#14232F"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FAMILIES = {
    "sans": "DejaVu Sans, Arial, Helvetica, sans-serif",
    "mono": "DejaVu Sans Mono, Consolas, monospace",
}
FONT_CACHE: dict[tuple[int, str, bool], ImageFont.FreeTypeFont] = {}


def font(size: int, family: str = "sans", bold: bool = False):
    key = (size, family, bold)
    if key not in FONT_CACHE:
        stem = "DejaVuSansMono" if family == "mono" else "DejaVuSans"
        filename = stem + ("-Bold" if bold else "") + ".ttf"
        FONT_CACHE[key] = ImageFont.truetype(str(FONT_DIR / filename), size)
    return FONT_CACHE[key]


def wrap(value: str, width: float, size: int, *, bold=False, family="sans"):
    selected = font(size, family, bold)
    lines: list[str] = []
    current = ""
    for word in value.split():
        if selected.getlength(word) > width:
            raise ValueError(f"Palavra excede largura: {word!r}")
        candidate = (current + " " + word).strip()
        if current and selected.getlength(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


class Panel:
    def __init__(self, filename: str, width: int, height: int, title: str, description: str):
        self.filename, self.w, self.h = filename, width, height
        self.title, self.description = title, description
        self.parts = [f'<rect width="{width}" height="{height}" fill="{BG}"/>']
        self.text_boxes: list[tuple[float, float, float, float, str]] = []

    def rect(self, x, y, width, height, fill):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}"/>')

    def path(self, d, fill, *, stroke=None, stroke_width=1):
        extra = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
        self.parts.append(f'<path d="{d}" fill="{fill}"{extra}/>')

    def text(self, value, x, y, size, *, fill=WHITE, bold=False, family="sans", anchor="start", max_width=None):
        selected = font(size, family, bold)
        width = selected.getlength(value)
        if max_width is not None and width > max_width + .5:
            raise ValueError(f"{self.filename}: texto excede área: {value!r}: {width:.1f}>{max_width}")
        left = x - (width / 2 if anchor == "middle" else width if anchor == "end" else 0)
        bx0, by0, bx1, by1 = selected.getbbox(value, anchor="ls")
        box = (left + bx0, y + by0, left + bx1, y + by1, value)
        if box[0] < -0.5 or box[1] < -0.5 or box[2] > self.w + .5 or box[3] > self.h + .5:
            raise ValueError(f"{self.filename}: texto fora da tela: {box}")
        self.text_boxes.append(box)
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{FAMILIES[family]}" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" fill="{fill}" text-anchor="{anchor}">{escape(value)}</text>'
        )

    def paragraph(self, value, x, y, width, size=32, line_height=43, *, fill=WHITE, bold=False, family="sans"):
        lines = wrap(value, width, size, bold=bold, family=family)
        for i, line in enumerate(lines):
            self.text(line, x, y + i * line_height, size, fill=fill, bold=bold, family=family, max_width=width)
        return y + len(lines) * line_height

    def header(self, title, subtitle, color, mobile):
        height = 148 if mobile else 136
        notch = 30 if mobile else 48
        self.path(f'M0 0H{self.w-notch}L{self.w} {notch}V{height-24}L{self.w-24} {height}H0Z', color)
        self.text(title, 28 if mobile else 32, 70 if mobile else 73, 44 if mobile else 52,
                  fill=BG, bold=True, max_width=self.w - 64)
        self.text(subtitle, 28 if mobile else 34, 113 if mobile else 113, 26,
                  fill=BG, family="mono", max_width=self.w - 64)
        self.rect(self.w - 50, height - 18, 18, 6, BG)
        self.rect(self.w - 76, height - 18, 18, 6, BG)
        self.rect(self.w - 102, height - 18, 18, 6, BG)
        return height

    def finish(self):
        # Interseções de caixas de texto, usando as mesmas fontes do SVG.
        for i, a in enumerate(self.text_boxes):
            for b in self.text_boxes[i + 1:]:
                overlap_x = min(a[2], b[2]) - max(a[0], b[0])
                overlap_y = min(a[3], b[3]) - max(a[1], b[1])
                if overlap_x > 1 and overlap_y > 1:
                    raise ValueError(f"{self.filename}: sobreposição textual: {a[4]!r} / {b[4]!r}")
        content = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                   f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc">\n'
                   f'<title id="title">{escape(self.title)}</title>\n'
                   f'<desc id="desc">{escape(self.description)}</desc>\n'
                   + "\n".join(self.parts) + "\n</svg>\n")
        ET.fromstring(content)
        for forbidden in ("<script", "<image", "foreignObject", "href=", "@font-face"):
            if forbidden in content:
                raise ValueError(f"{self.filename}: recurso proibido {forbidden}")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / self.filename).write_text(content, encoding="utf-8")
        return {"file": self.filename, "width": self.w, "height": self.h,
                "text_blocks": len(self.text_boxes), "text_overlaps": 0, "text_overflows": 0}


def stack(mobile):
    width = 600 if mobile else 1200
    height = 1312 if mobile else 768
    p = Panel(f"stack-{'mobile' if mobile else 'desktop'}.svg", width, height,
              "Tech loadout — tecnologias e ferramentas",
              "Tecnologias organizadas em seis áreas: back-end, web, dados, automação, jogos e versionamento.")
    p.header("01 // TECH LOADOUT", "TECNOLOGIAS / FERRAMENTAS", YELLOW, mobile)
    groups = [
        ("BACK-END / INTEGRAÇÕES", ["Java · Spring Boot", "APIs REST · Apache Camel"], CYAN, BG, BG),
        ("WEB / INTERFACES", ["React · TypeScript", "HTML · CSS · Tailwind CSS"], YELLOW, BG, BG),
        ("DADOS / BANCOS", ["SQL · PostgreSQL · MySQL", "Oracle · Supabase · Tableau"], DARK_CYAN, WHITE, CYAN),
        ("AUTOMAÇÃO", ["Python"], DARK_BLUE, WHITE, MAGENTA),
        ("JOGOS / REALIDADE VIRTUAL", ["C# · Unity"], RED, BG, BG),
        ("VERSIONAMENTO", ["Git · GitHub"], YELLOW, BG, BG),
    ]
    for i, (label, lines, fill, text_color, label_color) in enumerate(groups):
        x = 24 if mobile else 32 + (i % 2) * 580
        y = 180 + i * 186 if mobile else 176 + (i // 2) * 190
        card_width = 552 if mobile else 556
        card_height = 170
        p.path(f'M{x} {y}H{x+card_width-18}L{x+card_width} {y+18}V{y+card_height}H{x+18}L{x} {y+card_height-18}Z', fill)
        if fill in (DARK_BLUE, DARK_CYAN):
            p.rect(x, y, card_width - 18, 8, label_color)
        p.text(label, x + 24, y + 45, 26, fill=label_color, bold=True,
               max_width=card_width - 48)
        for j, line in enumerate(lines):
            p.text(line, x + 24, y + 97 + j * 42, 32, fill=text_color,
                   bold=len(lines) == 1, max_width=card_width - 48)
        if len(lines) == 1:
            p.path(f'M{x+card_width-100} {y+126}H{x+card_width-30}V{y+132}H{x+card_width-106}Z',
                   label_color)
    return p.finish()


def about(mobile):
    width = 600 if mobile else 1200
    header_height = 148 if mobile else 136
    left = 28 if mobile else 32
    column = 544 if mobile else 730
    first = "Experiência com Java, Spring Boot e APIs REST, integração de sistemas e dados."
    second = "No setor financeiro, trabalhei com cobrança, modernização de aplicações e correção de vulnerabilidades."
    first_y = header_height + 58
    first_lines = wrap(first, column, 32)
    finance_y = first_y + len(first_lines) * 43 + 16
    finance_text_y = finance_y + 103
    finance_lines = wrap(second, column, 32)
    content_end = finance_text_y + (len(finance_lines) - 1) * 43 + 30
    interests_y = content_end + 24 if mobile else header_height + 32
    interests_height = 320 if mobile else 402
    height = interests_y + interests_height + 32 if mobile else max(content_end + 40, interests_y + interests_height + 32)
    p = Panel(f"about-{'mobile' if mobile else 'desktop'}.svg", width, height,
              "Sobre Pedro Zampronha",
              "Experiência em desenvolvimento e integração, passagem pelo setor financeiro e interesses em jogos, RPG, animes e realidade virtual.")
    p.header("03 // IDENTIFICAÇÃO", "SOBRE MIM", CYAN, mobile)
    p.paragraph(first, left, first_y, column, 32, 43)
    p.path(f'M{left} {finance_y}H{left+column-18}L{left+column} {finance_y+18}V{finance_y+58}H{left}Z', YELLOW)
    p.text("SETOR FINANCEIRO", left + 18, finance_y + 39, 28, fill=BG, bold=True,
           max_width=column - 36)
    p.paragraph(second, left, finance_text_y, column, 32, 43)
    ix = 28 if mobile else 804
    iw = 544 if mobile else 364
    iy = interests_y
    p.path(f'M{ix} {iy}H{ix+iw-32}L{ix+iw} {iy+32}V{iy+interests_height}H{ix+24}L{ix} {iy+interests_height-24}Z', YELLOW)
    p.text("ALÉM DO CÓDIGO", ix + 24, iy + 49, 28, fill=BG, bold=True,
           max_width=iw - 48)
    p.rect(ix + 24, iy + 70, iw - 48, 3, BG)
    for i, value in enumerate(["Jogos", "RPG", "Animes", "Realidade virtual"]):
        py = iy + 118 + i * (44 if mobile else 60)
        p.path(f'M{ix+24} {py-15}L{ix+36} {py-9}L{ix+24} {py-3}Z', BG)
        p.text(value, ix + 50, py, 32, fill=BG, max_width=iw - 70)
    p.rect(0, height - 8, width // 3, 8, CYAN)
    p.rect(width // 3, height - 8, width // 8, 8, RED)
    return p.finish()


def footer(mobile):
    width, height = (600, 284) if mobile else (1200, 248)
    p = Panel(f"footer-{'mobile' if mobile else 'desktop'}.svg", width, height,
              "Ver todos os repositórios — @phbr63",
              "Chamada para abrir todos os repositórios públicos de PHBR63 no GitHub.")
    p.rect(0, 0, width, height, YELLOW)
    split = 432 if mobile else 914
    p.path(f'M{split+48} 0H{width}V{height}H{split-48}L{split+30} {height-78}V78Z', CYAN)
    px = 28 if mobile else 40
    fs = 38 if mobile else 50
    p.text("VER TODOS OS", px, 83 if mobile else 85, fs, fill=BG, bold=True,
           max_width=split - px - 6)
    p.text("REPOSITÓRIOS", px, 139 if mobile else 150, fs, fill=BG, bold=True,
           max_width=split - px - 6)
    p.text("@phbr63", px, 226 if mobile else 213, 32, fill=BG, bold=True, family="mono")
    ax, ay = (482, 86) if mobile else (1014, 62)
    scale = 76 if mobile else 112
    thickness = 15 if mobile else 20
    p.path(f'M{ax} {ay}H{ax+scale}V{ay+scale}H{ax+scale-thickness}V{ay+thickness*2}L{ax+thickness} {ay+scale}L{ax} {ay+scale-thickness}L{ax+scale-thickness*2} {ay+thickness}H{ax}Z', BG)
    p.rect(0, height - 8, width - 90, 8, BG)
    p.rect(width - 70, height - 8, 70, 8, RED)
    return p.finish()


PROJECTS = [
    ("3dgame", "3dGame", "JOGOS", YELLOW, CYAN, None, "Jogo da turma da ESPM."),
    ("vr", "jogo-vr", "REALIDADE VIRTUAL", CYAN, YELLOW, "Unity · C#", "Projeto de jogo em realidade virtual."),
    ("roll", "Let's Roll", "RPG DE MESA", YELLOW, CYAN, "React · TypeScript · Supabase", "Plataforma para RPG de mesa online, em desenvolvimento."),
    ("anime", "Anime Check", "ANIMES", RED, YELLOW, None, "Organização e descoberta de animes."),
]


def project(item, mobile):
    key, title, tag, color, action_color, technologies, description = item
    width, height = (600, 344) if mobile else (1200, 240)
    header_height = 88 if mobile else 78
    action_height = 72 if mobile else 58
    margin = 28 if mobile else 32
    p = Panel(f"project-{key}-{'mobile' if mobile else 'desktop'}.svg", width, height,
              f"{title} — abrir repositório", description)
    p.path(f'M0 0H{width-28}L{width} 28V{header_height}H0Z', color)
    p.text(title, margin, 59 if mobile else 54, 38 if mobile else 40, fill=BG, bold=True,
           max_width=width - 2 * margin)
    if not mobile:
        p.text(tag, width - 36, 50, 24, fill=BG, family="mono", anchor="end",
               max_width=width // 2 - 36)
    body_lines: list[tuple[str, bool]] = []
    if technologies:
        body_lines.extend((line, True) for line in wrap(technologies, width - 2 * margin, 32, bold=True))
    body_lines.extend((line, False) for line in wrap(description, width - 2 * margin, 32))
    line_height = 43
    body_height = height - header_height - action_height
    first_baseline = header_height + (body_height - len(body_lines) * line_height) / 2 + 33
    for index, (line, bold) in enumerate(body_lines):
        p.text(line, margin, first_baseline + index * line_height, 32,
               fill=CYAN if bold else WHITE, bold=bold, max_width=width - 2 * margin)
    action_y = height - action_height
    p.rect(0, action_y, width, action_height, action_color)
    p.text("ABRIR REPOSITÓRIO ↗", margin, action_y + (48 if mobile else 40),
           28 if mobile else 26, fill=BG, bold=True, family="mono", max_width=width - 2 * margin)
    p.path(f'M{width-96} {action_y+20}H{width-40}V{action_y+26}H{width-102}Z', BG)
    if key == "roll":
        p.rect(0, header_height, 10, body_height, MAGENTA)
    return p.finish()


def main():
    report = []
    for mobile in (False, True):
        report.extend([stack(mobile), about(mobile), footer(mobile)])
        report.extend(project(item, mobile) for item in PROJECTS)
    print(json.dumps({"assets": report, "count": len(report)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
