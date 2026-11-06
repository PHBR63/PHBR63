"""Atualiza a cidade aprovada usando somente os níveis do calendário público."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import URLError
from urllib.request import Request, urlopen

COLORS = ['#1b2531', '#20546a', '#198c9c', '#a78bfa', '#f472b6']
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / 'profile-3d-contrib/profile-night-rainbow.svg'


class CalendarParser(HTMLParser):
    """Recebe HTML público e extrai datas e níveis, sem inferir contagens."""

    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag != 'td' or not {'data-date', 'data-level'} <= attrs.keys():
            return
        day = date.fromisoformat(attrs['data-date'])
        level = int(attrs['data-level'])
        if not 0 <= level < len(COLORS):
            raise ValueError(f'Nível inválido no calendário: {day}.')
        if day in self.days:
            raise ValueError(f'Data duplicada no calendário: {day}.')
        self.days[day] = level


def parse_calendar(html, today):
    """Valida um ano contínuo e recente antes de permitir a gravação do SVG."""
    parser = CalendarParser()
    parser.feed(html)
    parser.close()
    days = parser.days
    if not 365 <= len(days) <= 371:
        raise ValueError(f'Calendário incompleto: encontrados {len(days)} dias.')
    first, last = min(days), max(days)
    if (last - first).days + 1 != len(days):
        raise ValueError('O calendário contém lacunas entre as datas.')
    if first.weekday() != 6:
        raise ValueError('O calendário não começa no domingo esperado.')
    if not today - timedelta(days=2) <= last <= today:
        raise ValueError(f'Calendário desatualizado ou futuro: último dia {last}.')
    return days


def fetch_calendar(username):
    """Consulta o GitHub por HTTPS, com limite de tempo e sem credencial pessoal."""
    request = Request(
        f'https://github.com/users/{username}/contributions',
        headers={'User-Agent': 'PHBR63-Contribution-City', 'Accept': 'text/html'},
    )
    with urlopen(request, timeout=30) as response:
        return response.read(2_000_000).decode('utf-8')


def generate_city(days, username, today):
    """Converte níveis em prédios SVG, mantendo bases fixas e alturas ascendentes."""
    start = min(days)
    buildings = []
    for day, level in sorted(days.items()):
        week, weekday = divmod((day - start).days, 7)
        x = 80 + week * 13 + weekday * 7
        base_y = 210 + weekday * 8 - week * 1.3
        height = 3 + level * 13
        # Coordenadas Y menores ficam acima: aumentar o nível não desloca o solo.
        top_y = base_y - height
        color = COLORS[level]
        shape = (
            f'<g data-date="{day}" data-level="{level}" data-base-y="{base_y:.1f}" data-top-y="{top_y:.1f}">'
            f'<path d="M{x:.1f} {top_y:.1f}v{height}h10v-{height}z" fill="{color}" opacity=".72"/>'
            f'<path d="M{x+10:.1f} {top_y:.1f}l5 -4v{height}l-5 4z" fill="{color}" opacity=".45"/>'
            f'<path d="M{x:.1f} {top_y:.1f}l10 0 5 -4 -10 0z" fill="{color}"/>'
            '</g>'
        )
        buildings.append((base_y, x, shape))
    # Fachadas próximas são desenhadas depois das distantes para ocultação correta.
    shapes = '\n'.join(shape for _, _, shape in sorted(buildings))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300">\n'
        f'<desc>Níveis públicos do calendário de {escape(username)} consultado em {today:%d/%m/%Y} (UTC). '
        f'Período: {min(days)} a {max(days)}. Alturas representam níveis, não contagens de contribuições.</desc>\n'
        '<defs><linearGradient id="g"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs>\n'
        '<rect x="2" y="2" width="896" height="296" rx="18" fill="#0d0e16" stroke="url(#g)" stroke-width="2"/>\n'
        '<text x="30" y="40" fill="#22d3ee" font-family="Arial" font-size="21" font-weight="bold">// CIDADE DE CONTRIBUIÇÕES</text>\n'
        + shapes + '\n</svg>\n'
    )


def update_city(html, username, output, today):
    """Valida os dados e substitui atomicamente o arquivo; retorna se houve mudança."""
    days = parse_calendar(html, today)
    svg = generate_city(days, username, today)
    if output.exists() and output.read_text(encoding='utf-8') == svg:
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', dir=output.parent,
            prefix='.city-', suffix='.tmp', delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(svg)
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return True


def main():
    """Recebe usuário/saída pela CLI e informa falhas sem substituir a imagem válida."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='PHBR63')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', args.username):
        parser.error('Nome de usuário GitHub inválido.')
    try:
        today = datetime.now(timezone.utc).date()
        changed = update_city(fetch_calendar(args.username), args.username, args.output, today)
    except (OSError, URLError, ValueError, UnicodeError) as error:
        print(f'Falha ao atualizar a cidade; imagem anterior preservada: {error}', file=sys.stderr)
        return 1
    print('Cidade atualizada.' if changed else 'Cidade já atualizada; nenhuma alteração.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
