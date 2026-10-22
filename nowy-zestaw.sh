#!/usr/bin/env bash
# Tworzy szkielet nowego zestawu: ./nowy-zestaw.sh 02 [ścieżka/do/tresci.pdf]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
num="${1:?Podaj numer zestawu, np. 02}"
name="mn$num"
dir="$ROOT/zestawy/$name"
[[ -e "$dir/$name.tex" ]] && { echo "$dir/$name.tex już istnieje" >&2; exit 1; }
mkdir -p "$dir"
sed -e "s/NUMER/$((10#$num))/" -e "s/NAZWA/$name/" "$ROOT/szablon/zestaw.tex" > "$dir/$name.tex"
[[ -n "${2:-}" ]] && cp "$2" "$dir/tresc.pdf"
echo "Utworzono $dir/$name.tex"
