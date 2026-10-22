"""Sprawdza, czy w PDF-ie jakiś tekst wystaje poza prawy margines strony.

Użycie: python3 -I weryfikacja/marginesy.py plik.pdf [margines_mm]
Wymaga pdftotext (poppler-utils). Kod wyjścia 1, jeśli coś wystaje.
"""
import re
import subprocess
import sys

pdf = sys.argv[1]
margin_mm = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
margin = margin_mm / 25.4 * 72

xml = subprocess.run(
    ["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True
).stdout

bad = []
page_no = 0
width = 0.0
for line in xml.splitlines():
    m = re.search(r'<page width="([\d.]+)"', line)
    if m:
        page_no += 1
        width = float(m.group(1))
        continue
    m = re.search(r'xMax="([\d.]+)".*>(.*)</word>', line)
    if m and float(m.group(1)) > width - margin:
        bad.append((page_no, m.group(2), float(m.group(1)) - width))

for page, word, over in bad:
    print(f"{pdf}: strona {page}: '{word}' wystaje ({over:+.1f}pt względem krawędzi)")
if bad:
    sys.exit(1)
print(f"ok  {pdf}: nic nie wystaje poza stronę")
