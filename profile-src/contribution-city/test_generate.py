"""Proteções de dados e regressão da geometria da cidade, sem acesso à rede."""

from datetime import date, timedelta
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generate import generate_city, parse_calendar, update_city

FIRST = date(2025, 11, 2)
TODAY = date(2026, 11, 6)


def calendar_html(count=370):
    return ''.join(
        f'<td data-date="{FIRST + timedelta(days=index)}" data-level="{index % 5}"></td>'
        for index in range(count)
    )


class CityTests(unittest.TestCase):
    def test_complete_public_calendar(self):
        days = parse_calendar(calendar_html(), TODAY)
        self.assertEqual(len(days), 370)
        self.assertEqual(max(days), TODAY)

    def test_invalid_calendar_preserves_previous_file(self):
        valid = calendar_html()
        cases = {
            'empty': '<html>Service unavailable</html>',
            'incomplete': calendar_html(20),
            'duplicate': valid + f'<td data-date="{FIRST}" data-level="0"></td>',
            'invalid_level': valid.replace('data-level="0"', 'data-level="5"', 1),
            'invalid_date': valid.replace(str(FIRST), '2025-13-02', 1),
            'gap': valid.replace(f'<td data-date="{FIRST + timedelta(days=5)}" data-level="0"></td>', ''),
            'stale': calendar_html(365),
            'future': calendar_html(371),
        }
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'city.svg'
            output.write_text('previous-city', encoding='utf-8')
            for name, html in cases.items():
                with self.subTest(name=name):
                    with self.assertRaises(ValueError):
                        update_city(html, 'PHBR63', output, TODAY)
                    self.assertEqual(output.read_text(encoding='utf-8'), 'previous-city')
            self.assertEqual(len(list(Path(folder).iterdir())), 1)

    def test_buildings_grow_up_with_fixed_bases(self):
        days = parse_calendar(calendar_html(), TODAY)
        namespace = {'svg': 'http://www.w3.org/2000/svg'}
        low = ET.fromstring(generate_city(dict.fromkeys(days, 0), 'PHBR63', TODAY))
        high = ET.fromstring(generate_city(dict.fromkeys(days, 4), 'PHBR63', TODAY))
        low_buildings = low.findall('svg:g', namespace)
        high_buildings = high.findall('svg:g', namespace)
        self.assertEqual(len(high_buildings), 370)
        for a, b in zip(low_buildings, high_buildings):
            self.assertEqual(a.attrib['data-base-y'], b.attrib['data-base-y'])
            self.assertLess(float(b.attrib['data-top-y']), float(a.attrib['data-top-y']))
            self.assertLess(float(b.attrib['data-top-y']), float(b.attrib['data-base-y']))

    def test_repeat_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'city.svg'
            self.assertTrue(update_city(calendar_html(), 'PHBR63', output, TODAY))
            original = output.read_bytes()
            self.assertFalse(update_city(calendar_html(), 'PHBR63', output, TODAY))
            self.assertEqual(output.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
