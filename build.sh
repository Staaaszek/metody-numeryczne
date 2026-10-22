#!/usr/bin/env bash
# Buduje wszystkie zestawy (A4 + wersja na telefon) do katalogu build/
# oraz stronę build/index.html z linkami.
#
# Użycie:
#   ./build.sh            # wszystkie zestawy
#   ./build.sh mn01       # tylko wybrany zestaw (bez pliku zbiorczego)
#   ./build.sh --check    # dodatkowo uruchom skrypty z weryfikacja/
#   ./build.sh --clean    # usuń build/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/build"
export TEXINPUTS="$ROOT/common//:${TEXINPUTS:-}"

CHECK=0
ONLY=()
for arg in "$@"; do
  case "$arg" in
    --clean) rm -rf "$OUT"; echo "Usunięto $OUT"; exit 0 ;;
    --check) CHECK=1 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) ONLY+=("$arg") ;;
  esac
done

mkdir -p "$OUT"

if [[ ${#ONLY[@]} -gt 0 ]]; then
  ZESTAWY=("${ONLY[@]}")
else
  ZESTAWY=()
  for d in "$ROOT"/zestawy/*/; do ZESTAWY+=("$(basename "$d")"); done
fi

build_one() {
  local name="$1" dir="$ROOT/zestawy/$1"
  [[ -f "$dir/$name.tex" ]] || { echo "Brak $dir/$name.tex" >&2; return 1; }
  echo "==> $name (A4)"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet \
    -outdir="$OUT/tmp/$name" -cd "$dir/$name.tex" >/dev/null \
    || { tail -40 "$OUT/tmp/$name/$name.log" >&2; return 1; }
  cp "$OUT/tmp/$name/$name.pdf" "$OUT/$name.pdf"

  echo "==> $name (telefon)"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet \
    -usepretex='\def\TELEFON{}' -jobname="$name-telefon" \
    -outdir="$OUT/tmp/$name" -cd "$dir/$name.tex" >/dev/null \
    || { tail -40 "$OUT/tmp/$name/$name-telefon.log" >&2; return 1; }
  cp "$OUT/tmp/$name/$name-telefon.pdf" "$OUT/$name-telefon.pdf"

  [[ -f "$dir/tresc.pdf" ]] && cp "$dir/tresc.pdf" "$OUT/$name-tresc.pdf"
  if [[ $CHECK -eq 1 && -f "$ROOT/weryfikacja/$name.py" ]]; then
    echo "==> $name (weryfikacja numeryczna)"
    python3 -I "$ROOT/weryfikacja/$name.py"
  fi
  if [[ $CHECK -eq 1 ]]; then
    python3 -I "$ROOT/weryfikacja/marginesy.py" "$OUT/$name-telefon.pdf"
    python3 -I "$ROOT/weryfikacja/marginesy.py" "$OUT/$name.pdf" 15
  fi
}

for z in "${ZESTAWY[@]}"; do build_one "$z"; done

# ---------- wszystkie zestawy w jednym pliku ----------
build_all() {
  local dir="$OUT/tmp/wszystko" f
  mkdir -p "$dir"
  {
    echo '\documentclass[11pt]{article}'
    echo '\usepackage{mn}'
    echo '\begin{document}'
    echo '\begin{center}{\LARGE\bfseries Metody numeryczne}\\[0.3em]{\Large Rozwiązania wszystkich zestawów}\end{center}'
    echo '\tableofcontents'
    for f in "$ROOT"/zestawy/*/; do
      f="$(basename "$f")"
      if [[ -f "$ROOT/zestawy/$f/$f.tex" ]]; then
        echo "\\wlaczzestaw{$f}{$ROOT/zestawy/$f/$f.tex}"
      fi
    done
    echo '\end{document}'
  } > "$dir/wszystko.tex"

  echo "==> wszystko (A4)"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet \
    -usepretex='\def\WSZYSTKO{}' -outdir="$dir" -cd "$dir/wszystko.tex" >/dev/null \
    || { tail -40 "$dir/wszystko.log" >&2; return 1; }
  cp "$dir/wszystko.pdf" "$OUT/wszystko.pdf"

  echo "==> wszystko (telefon)"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet \
    -usepretex='\def\WSZYSTKO{}\def\TELEFON{}' -jobname=wszystko-telefon \
    -outdir="$dir" -cd "$dir/wszystko.tex" >/dev/null \
    || { tail -40 "$dir/wszystko-telefon.log" >&2; return 1; }
  cp "$dir/wszystko-telefon.pdf" "$OUT/wszystko-telefon.pdf"

  if [[ $CHECK -eq 1 ]]; then
    python3 -I "$ROOT/weryfikacja/marginesy.py" "$OUT/wszystko-telefon.pdf"
    python3 -I "$ROOT/weryfikacja/marginesy.py" "$OUT/wszystko.pdf" 15
  fi
}
# plik zbiorczy tylko przy pełnym buildzie (bez wybranego zestawu)
if [[ ${#ONLY[@]} -eq 0 ]]; then build_all; fi

# ---------- strona index.html (czytelna na telefonie) ----------
{
  cat <<'EOF'
<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Metody numeryczne — rozwiązania</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:40rem;margin:auto;padding:1rem;line-height:1.5}
 h1{font-size:1.4rem} li{margin:.8rem 0;list-style:none;padding:.8rem;border:1px solid #ddd;border-radius:.6rem}
 a{display:inline-block;margin:.2rem .6rem .2rem 0;padding:.35rem .7rem;border-radius:.4rem;
   background:#1d4ed8;color:#fff;text-decoration:none} a.alt{background:#64748b}
 ul{padding:0} small{color:#666}
</style></head><body>
<h1>Metody numeryczne — rozwiązania zestawów</h1>
<ul>
EOF
  if [[ -f "$OUT/wszystko.pdf" ]]; then
    echo "<li><b>Wszystkie zestawy w jednym pliku</b><br>"
    echo "<a href=\"wszystko-telefon.pdf\">📱 Telefon</a><a href=\"wszystko.pdf\">🖨️ A4</a></li>"
  fi
  for f in $(ls "$ROOT/zestawy" | sort -r); do
    [[ -f "$OUT/$f.pdf" ]] || continue
    num="${f#mn}"
    echo "<li><b>Zestaw $((10#$num))</b><br>"
    echo "<a href=\"$f-telefon.pdf\">📱 Telefon</a><a href=\"$f.pdf\">🖨️ A4</a>"
    [[ -f "$OUT/$f-tresc.pdf" ]] && echo "<a class=\"alt\" href=\"$f-tresc.pdf\">Treść zadań</a>"
    echo "</li>"
  done
  echo "</ul><small>Zbudowano: $(date -u '+%Y-%m-%d %H:%M UTC')</small></body></html>"
} > "$OUT/index.html"

echo "Gotowe: $OUT"
ls -1 "$OUT"/*.pdf
