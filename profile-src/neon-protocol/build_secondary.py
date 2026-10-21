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
import math
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

# Ritmo de espaçamento compartilhado: 8 / 16 / 24 / 32 / 40 / 48 px.
# A altura dos conteúdos vem das métricas da fonte, sem centralização em caixas fixas.
GRID = 8
BODY_SIZE = 32
BODY_LEADING = 48


def grid(value):
    return math.ceil(value / GRID) * GRID


def inset(mobile):
    return 32 if mobile else 40


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


def block_height(lines, size=BODY_SIZE, line_height=BODY_LEADING, *, bold=False, family="sans"):
    ascent, descent = font(size, family, bold).getmetrics()
    return ascent + descent + max(0, len(lines) - 1) * line_height


def centered_baseline(top, height, size, *, bold=False, family="sans"):
    ascent, descent = font(size, family, bold).getmetrics()
    return round(top + (height - ascent - descent) / 2 + ascent)


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

    def block(self, lines, x, top, width, *, size=BODY_SIZE, line_height=BODY_LEADING,
              fill=WHITE, bold=False, family="sans"):
        ascent, _ = font(size, family, bold).getmetrics()
        for i, line in enumerate(lines):
            self.text(line, x, top + ascent + i * line_height, size, fill=fill,
                      bold=bold, family=family, max_width=width)
        return top + block_height(lines, size, line_height, bold=bold, family=family)

    def header(self, title, subtitle, color, mobile):
        height = 160 if mobile else 152
        pad = inset(mobile)
        title_size = 44 if mobile else 52
        title_top = 24
        title_ascent, _ = font(title_size, "sans", True).getmetrics()
        subtitle_top = title_top + block_height([title], title_size, bold=True) + (16 if mobile else 8)
        subtitle_ascent, _ = font(26, "mono").getmetrics()
        notch = 32 if mobile else 48
        self.path(f'M0 0H{self.w-notch}L{self.w} {notch}V{height-24}L{self.w-24} {height}H0Z', color)
        self.text(title, pad, title_top + title_ascent, title_size,
                  fill=BG, bold=True, max_width=self.w - 2 * pad)
        self.text(subtitle, pad, subtitle_top + subtitle_ascent, 26,
                  fill=BG, family="mono", max_width=self.w - 2 * pad)
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
    pad = inset(mobile)
    header_height = 160 if mobile else 152
    gap = 24
    inner = 24
    label_height = block_height(["TECH"], 26, bold=True)
    card_height = grid(inner + label_height + 16 + block_height(["line", "line"]) + inner)
    card_width = width - 2 * pad if mobile else (width - 2 * pad - gap) // 2
    first_y = header_height + (32 if mobile else 40)
    rows = 6 if mobile else 3
    height = first_y + rows * card_height + (rows - 1) * gap + pad
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
        x = pad if mobile else pad + (i % 2) * (card_width + gap)
        y = first_y + (i if mobile else i // 2) * (card_height + gap)
        p.path(f'M{x} {y}H{x+card_width-18}L{x+card_width} {y+18}V{y+card_height}H{x+18}L{x} {y+card_height-18}Z', fill)
        if fill in (DARK_BLUE, DARK_CYAN):
            p.rect(x, y, card_width - 18, 8, label_color)
        label_bottom = p.block([label], x + inner, y + inner, card_width - 2 * inner,
                               size=26, fill=label_color, bold=True)
        p.block(lines, x + inner, label_bottom + 16, card_width - 2 * inner,
                fill=text_color, bold=len(lines) == 1)
        if len(lines) == 1:
            p.path(f'M{x+card_width-96} {y+card_height-32}H{x+card_width-24}V{y+card_height-26}H{x+card_width-102}Z',
                   label_color)
    return p.finish()


def about(mobile):
    width = 600 if mobile else 1200
    header_height = 160 if mobile else 152
    left = inset(mobile)
    column_gap = 48
    interests_width = width - 2 * left if mobile else 360
    column = width - 2 * left if mobile else width - 2 * left - column_gap - interests_width
    first = "Experiência com Java, Spring Boot e APIs REST, integração de sistemas e dados."
    second = "No setor financeiro, trabalhei com cobrança, modernização de aplicações e correção de vulnerabilidades."
    first_top = header_height + (32 if mobile else 40)
    first_lines = wrap(first, column, 32)
    finance_y = grid(first_top + block_height(first_lines) + 32)
    finance_height = 64
    finance_text_top = finance_y + finance_height + 24
    finance_lines = wrap(second, column, 32)
    content_end = finance_text_top + block_height(finance_lines)
    interests_y = grid(content_end + 32) if mobile else first_top
    inner = 24
    interest_title_height = block_height(["ALÉM DO CÓDIGO"], 28, bold=True)
    rule_y = interests_y + inner + interest_title_height + 16
    interest_list_top = rule_y + 2 + 24
    interest_line_height = 56
    interests_height = grid(interest_list_top - interests_y + block_height(["item"] * 4, line_height=interest_line_height) + inner)
    height = grid(max(content_end, interests_y + interests_height) + left)
    p = Panel(f"about-{'mobile' if mobile else 'desktop'}.svg", width, height,
              "Sobre Pedro Zampronha",
              "Experiência em desenvolvimento e integração, passagem pelo setor financeiro e interesses em jogos, RPG, animes e realidade virtual.")
    p.header("03 // IDENTIFICAÇÃO", "SOBRE MIM", CYAN, mobile)
    p.block(first_lines, left, first_top, column)
    p.path(f'M{left} {finance_y}H{left+column-24}L{left+column} {finance_y+24}V{finance_y+finance_height}H{left}Z', YELLOW)
    p.text("SETOR FINANCEIRO", left + 24, centered_baseline(finance_y, finance_height, 28, bold=True),
           28, fill=BG, bold=True, max_width=column - 48)
    p.block(finance_lines, left, finance_text_top, column)
    ix = left if mobile else left + column + column_gap
    iw = interests_width
    iy = interests_y
    p.path(f'M{ix} {iy}H{ix+iw-32}L{ix+iw} {iy+32}V{iy+interests_height}H{ix+24}L{ix} {iy+interests_height-24}Z', YELLOW)
    p.block(["ALÉM DO CÓDIGO"], ix + inner, iy + inner, iw - 2 * inner, size=28, fill=BG, bold=True)
    p.rect(ix + inner, rule_y, iw - 2 * inner, 2, BG)
    interest_ascent, _ = font(32).getmetrics()
    for i, value in enumerate(["Jogos", "RPG", "Animes", "Realidade virtual"]):
        py = interest_list_top + interest_ascent + i * interest_line_height
        p.path(f'M{ix+24} {py-15}L{ix+36} {py-9}L{ix+24} {py-3}Z', BG)
        p.text(value, ix + 50, py, 32, fill=BG, max_width=iw - 70)
    p.rect(0, height - 8, width // 3, 8, CYAN)
    p.rect(width // 3, height - 8, width // 8, 8, RED)
    return p.finish()


def footer(mobile):
    width = 600 if mobile else 1200
    px = inset(mobile)
    fs = 38 if mobile else 50
    title_leading = 56 if mobile else 64
    title_top = 32
    title_lines = ["VER TODOS OS", "REPOSITÓRIOS"]
    handle_top = title_top + block_height(title_lines, fs, title_leading, bold=True) + (32 if mobile else 24)
    height = grid(handle_top + block_height(["@phbr63"], 32, family="mono", bold=True) + px)
    p = Panel(f"footer-{'mobile' if mobile else 'desktop'}.svg", width, height,
              "Ver todos os repositórios — @phbr63",
              "Chamada para abrir todos os repositórios públicos de PHBR63 no GitHub.")
    p.rect(0, 0, width, height, YELLOW)
    split = 432 if mobile else 920
    p.path(f'M{split+48} 0H{width}V{height}H{split-48}L{split+32} {height-80}V80Z', CYAN)
    p.block(title_lines, px, title_top, split - px - 8, size=fs, line_height=title_leading, fill=BG, bold=True)
    p.block(["@phbr63"], px, handle_top, split - px - 8, size=32, fill=BG, bold=True, family="mono")
    scale = 80 if mobile else 112
    ax, ay = width - px - scale, 64
    thickness = 16 if mobile else 24
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
    width = 600 if mobile else 1200
    margin = inset(mobile)
    header_height = 96
    action_height = 80
    body_padding = 24 if mobile else 32
    content_width = width - 2 * margin
    # No mobile a cor já diferencia a tecnologia; o peso normal mantém a linha
    # legível sem reduzir os 32 px ou criar uma quebra por apenas um glifo.
    tech_bold = not mobile
    tech_lines = wrap(technologies, content_width, BODY_SIZE, bold=tech_bold) if technologies else []
    description_lines = wrap(description, content_width, BODY_SIZE)
    technology_top = header_height + body_padding
    description_top = technology_top
    if tech_lines:
        description_top += block_height(tech_lines, bold=tech_bold) + (16 if mobile else 24)
    action_y = grid(description_top + block_height(description_lines) + body_padding)
    height = action_y + action_height
    p = Panel(f"project-{key}-{'mobile' if mobile else 'desktop'}.svg", width, height,
              f"{title} — abrir repositório", description)
    p.path(f'M0 0H{width-32}L{width} 32V{header_height}H0Z', color)
    title_size = 38 if mobile else 40
    p.text(title, margin, centered_baseline(0, header_height, title_size, bold=True),
           title_size, fill=BG, bold=True, max_width=content_width)
    if not mobile:
        p.text(tag, width - margin, centered_baseline(0, header_height, 24, family="mono"),
               24, fill=BG, family="mono", anchor="end", max_width=width // 2 - margin)
    if tech_lines:
        p.block(tech_lines, margin, technology_top, content_width, fill=CYAN, bold=tech_bold)
    p.block(description_lines, margin, description_top, content_width)
    p.rect(0, action_y, width, action_height, action_color)
    p.text("ABRIR REPOSITÓRIO ↗", margin, centered_baseline(action_y, action_height, 28, bold=True, family="mono"),
           28, fill=BG, bold=True, family="mono", max_width=content_width)
    p.path(f'M{width-margin-64} {action_y+36}H{width-margin}V{action_y+42}H{width-margin-70}Z', BG)
    if key == "roll":
        p.rect(0, header_height, 8, action_y - header_height, MAGENTA)
    return p.finish()


def main():
    report = []
    for mobile in (False, True):
        report.extend([stack(mobile), about(mobile), footer(mobile)])
        report.extend(project(item, mobile) for item in PROJECTS)
    print(json.dumps({"assets": report, "count": len(report)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
