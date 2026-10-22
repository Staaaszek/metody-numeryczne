# Metody numeryczne — rozwiązania zestawów

📱 **PDF-y online:** https://staaaszek.github.io/metody-numeryczne/

Każdy zestaw jest w dwóch wersjach:
- **telefon** — wąska strona (11 × 19,5 cm), czyta się bez przybliżania,
- **A4** — do druku / na komputer, ze spisem treści.

Na stronie jest też **jeden plik ze wszystkimi zestawami** (`wszystko.pdf`,
`wszystko-telefon.pdf`) — ze wspólnym spisem treści i zakładkami; generuje się
sam przy każdym pełnym buildzie, nic nie trzeba dopisywać.

W każdym zadaniu: przepisana treść, potrzebne definicje i twierdzenia,
intuicja, rozwiązanie formalne i odpowiedź.

## Struktura

```
zestawy/mnNN/mnNN.tex    rozwiązania zestawu NN
zestawy/mnNN/tresc.pdf   oryginalna treść zestawu
wyklady/                 notatki z wykładów (źródło teorii do zestawów)
common/mn.sty            wspólny styl (pudełka, notacja, tryb telefonu)
weryfikacja/mnNN.py      numeryczne sprawdzenie wyników z zestawu
weryfikacja/marginesy.py sprawdza, czy nic nie wystaje poza stronę
szablon/zestaw.tex       szablon nowego zestawu
```

## Budowanie lokalne

Wymaga TeX Live (`latexmk`, `pdflatex`, pakiety polskie) i `python3`.

```bash
./build.sh            # wszystkie zestawy -> build/
./build.sh mn01       # jeden zestaw (bez pliku zbiorczego)
./build.sh --check    # + weryfikacja numeryczna i test marginesów
./build.sh --clean
```

## Nowy zestaw

```bash
./nowy-zestaw.sh 03 ~/Pobrane/exercises-03.pdf   # tworzy zestawy/mn03/ z szablonu
# uzupełnij zestawy/mn03/mn03.tex (+ opcjonalnie weryfikacja/mn03.py)
./build.sh --check mn03
git add . && git commit -m "Zestaw 3" && git push
```

Po `git push` GitHub Actions buduje PDF-y i publikuje je na stronie
(GitHub Pages) — zwykle w ~3 minuty.
