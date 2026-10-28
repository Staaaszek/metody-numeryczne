# Instrukcje dla Claude — repo z rozwiązaniami „Metod numerycznych”

Repo służy przez cały semestr: co jakiś czas dochodzi nowy zestaw zadań (PDF,
zwykle `exercises-NN.pdf`). Zadanie: rozwiązać go w LaTeX-u w tym samym stylu
co poprzednie zestawy. Bliźniacze repo z tym samym układem:
`../aa` (Analiza algorytmów) — zmiany w infrastrukturze warto przenosić.

## Notatki z wykładu
`wyklady/` jest na notatki z wykładów (PDF-y są w `.gitignore` — nie trafiają na GH). Jeśli coś tam jest,
**przed rozwiązywaniem zestawu przeczytaj wykład(y) z tego samego tematu**:
teoria w zestawie ma iść za wykładem (te same definicje i oznaczenia),
a w rozwiązaniach korzystaj przede wszystkim z metod pokazanych na wykładzie.
Rzeczy spoza wykładu wolno dodać, ale wyraźnie jako uzupełnienie. Zwracaj
uwagę na ograniczenia z treści (np. „bez wartości własnych”) — rozwiązanie
główne ma się w nich mieścić, resztę daj w `uwaga`.
Jeśli user doda nowy wykład, sprawdź, czy nie trzeba zaktualizować teorii
we wcześniejszych zestawach.

## Przy nowym zestawie
1. `./nowy-zestaw.sh NN ścieżka/do/zestawu.pdf` (treść ląduje w `zestawy/mnNN/tresc.pdf`).
2. Przeczytaj PDF (obraz, nie tylko pdftotext — wzory i macierze się psują).
3. Napisz `zestawy/mnNN/mnNN.tex` wg wzoru `zestawy/mn01`, `zestawy/mn02`:
   - wspólna teoria tematu na początku jako `\section{Teoria: ...}`;
   - każde zadanie to `\section{Zadanie N. krótki opis}` + pudełko `tresc`
     z wiernie przepisaną treścią;
   - nieoczywiste definicje/twierdzenia w `teoria` (z `definicja`, `twierdzenie`,
     `lemat`, `fakt`), wytłumaczone, nie tylko przytoczone; jeśli coś było już
     wyjaśnione we wcześniejszym zestawie, można się odwołać;
   - w teorii (sekcje `Teoria: ...` i pudełka `teoria` w zadaniach) po
     każdej ważniejszej definicji/twierdzeniu: pudełko `przyklad`
     (konkretne małe liczby, przykład + kontrprzykład, sprawdzone
     w `weryfikacja/`) i `poludzku` (to samo najprościej, bez wzorów,
     z analogią) — wersja formalna zostaje bez zmian;
   - `intuicja` (jak do studenta), potem `\formalnie` (pełny dowód),
     na końcu `odpowiedz`;
   - matematyka w tytułach sekcji przez `\texorpdfstring`;
   - zestaw trafia też automatycznie do pliku zbiorczego `wszystko.pdf`
     (`build.sh` → `\wlaczzestaw`); etykiety `\label` są tam prefiksowane
     nazwą zestawu, więc mogą się powtarzać między zestawami.
4. Wszystkie przykłady liczbowe / wzory sprawdź skryptem `weryfikacja/mnNN.py`
   (Python `float` = IEEE double, więc przykłady zmiennoprzecinkowe sprawdza
   się wprost; algebrę liniową dokładnie na `fractions`).
5. `./build.sh --check mnNN` musi przejść — w tym `marginesy.py` dla wersji
   telefonowej (strona ma tylko ~10 cm szerokości: długie wzory łam przez
   `align*`/`gather*`, tytuły sekcji krótkie, macierze najwyżej ~5 kolumn).
6. Commit + push na `main` → GitHub Actions buduje i publikuje na Pages.

## Konwencje
- Język: polski. Makra w `common/mn.sty`: `\norm`, `\abs`, `\fl`,
  `\eps` (= u, precyzja arytmetyki), `\oplusm`/`\otimesm` (działania maszynowe),
  `\R`, `\O`, `\floor`, `\ceil`.
- Nie zmieniaj wyglądu `common/mn.sty` bez potrzeby — wpływa na wszystkie zestawy.
- `\label` w displayach amsmath (`align`, `equation`) nie dostaje prefiksu
  zestawu w `wszystko.pdf` → niezdefiniowana referencja. Wzory oznaczaj
  `\tag{X}` i odwołuj się tekstem „(X)”; `\label` tylko w twierdzeniach itp.
