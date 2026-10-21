#!/usr/bin/env python3
"""Regenera os badges do README. Não altera textos nem imagens ilustradas."""

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "assets" / "yellow-protocol" / "tecnologias"
BADGES = [
    ("java", "Java", 32),
    ("spring-boot", "Spring Boot", 28),
    ("react", "React", 32),
    ("typescript", "TypeScript", 28),
    ("python", "Python", 32),
    ("sql", "SQL", 32),
    ("csharp", "C#", 32),
    ("unity", "Unity", 32),
]


def badge(label, font_size):
    text = escape(label)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="280" height="92" viewBox="0 0 280 92" role="img" aria-labelledby="title desc">
  <title id="title">{text}</title>
  <desc id="desc">Badge de texto {text}, em amarelo sobre fundo escuro.</desc>
  <path d="M15 1H279V77L265 91H1V15Z" fill="#080C12" stroke="#293D48" stroke-width="2"/>
  <path d="M17 27H23V59L17 65Z" fill="#FCEE09"/>
  <text x="40" y="58" font-family="DejaVu Sans,Arial,Helvetica,sans-serif" font-size="{font_size}" font-weight="700" fill="#FCEE09">{text}</text>
  <path d="M254 28H260V58L254 64Z" fill="#00F0FF"/>
</svg>
'''


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for filename, label, font_size in BADGES:
        svg = badge(label, font_size)
        ET.fromstring(svg)
        (DEST / f"{filename}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
