# Autorstwo i źródła

## Wkład autorów

| Autor | Wykonane elementy | Lokalizacja w projekcie |
| --- | --- | --- |
| Marcin Kowalczyk (Pixel of Software) | założenia, przegląd i akceptacja kodu, publikacja | całość |
| Asystent AI Claude (Anthropic) | kod modułów, testy, model referencyjny, układy przykładowe, dokumentacja | `app/`, `tests/`, `narzedzia/`, `uklady/`, `demo/`, `README.md` |

## Wykorzystane materiały

| Materiał | Autor i źródło | Wersja lub data | Licencja | Sposób wykorzystania |
| --- | --- | --- | --- | --- |
| `build.py`, `run.py`, `LICENSE` | Fundacja Duckling, szablon projektu z materiałów na start DuckQuest | 2026 | MIT (plik `LICENSE`) | skrypty skopiowane bez zmian; licencja z dopisanym autorem |
| Łańcuch ruda → metal → płytka → moduł | przykład z karty P03 DuckFactory (materiały DuckQuest) | 2026 | materiały konkursowe | receptury układów przykładowych i przypadek „12 rudy → najwyżej 3 moduły” |
| Duckling (kompilator i biblioteka standardowa) | ducktype-org/duckling | 0.3-alpha, commit 83882805a | licencja Ducklinga | zależność budowania |

## Narzędzia AI

Kod w `app/` i `tests/`, model referencyjny `narzedzia/model_referencyjny.py`, układy w `uklady/`, demonstrację i dokumentację przygotowano z pomocą asystenta AI Claude (Anthropic). Autor ustalił zakres, przejrzał wyniki, sprawdził działanie (budowa, testy, demonstracja, zgodność z modelem referencyjnym) i odpowiada za oddaną wersję.

## Licencja własnego projektu

MIT, treść w pliku `LICENSE` (szablon Fundacji Duckling z dopisaną linią `Copyright (c) 2026 Pixel of Software (Marcin Kowalczyk)`).
