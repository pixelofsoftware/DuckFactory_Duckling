# Scenariusze sprawdzenia

Próby z 2026-11-21 na macOS 27.2 (Apple Silicon), `duckc 0.3-alpha (83882805a 2026-11-20)`, wariant natywny, po `python3 build.py --target all --output build`. Wartości oczekiwane policzono niezależnie modelem `narzedzia/model_referencyjny.py`.

| Scenariusz | Dane lub czynności | Oczekiwany wynik | Komenda lub procedura | Otrzymany wynik |
| --- | --- | --- | --- | --- |
| Zwykłe działanie: układ A | `uklady/szeregowy.txt`, 24 rudy, zamówienie 6 modułów | krok 44; piec 12 cykli (36 kroków pracy, 8 czekania), krajarka 12 (24/20), montownia 6 (24/20) | `symuluj A` | zgodny; wąskie gardło PIEC1 81.82% - OK |
| Zwykłe działanie: układ B | `uklady/rownolegly.txt` (dwa piece), te same zapasy i zamówienie | krok 33; piece po 6 cykli (18/15), krajarka 12 (24/9), montownia 6 (24/9) | `symuluj B` | zgodny; wąskie gardło KRAJARKA1 72.73% - OK |
| Porównanie dwóch układów | A i B | B szybszy o 11 kroków (25%), wyjaśnienie przez wąskie gardło | `porownaj A B` | zgodny - OK |
| Kolejność zdarzeń w kroku | układ A, kroki 1-6 | ruda wysłana w kroku 1, piec zaczyna w kroku 2, metal w kroku 4, krajarka zaczyna w kroku 5 | `przebieg A 1 6` | zgodny - OK |
| Niepoprawne dane: brak surowca (karta) | `uklady/przyklad-karty.txt`: 12 rudy, zamówienie 4 modułów | najwyżej 3 moduły; stop w kroku 27 z przyczynami | `symuluj K` | „jest 3 z 4”, maszyny czekają na surowce - OK |
| Niepoprawne dane: brak połączenia | układ A bez KRAJARKA1 → MONTAZ1 | krajarka i piec zablokowane, montownia czeka; stop w kroku 26; 4 rudy w magazynie | `wylacz A KRAJARKA1 MONTAZ1`, `symuluj A` | zgodny - OK |
| Niepoprawne dane: brak rudy | zapas rudy 0 | nic nie powstaje, stop w kroku 1 | `zapas B MAG_WE ruda 0`, `symuluj B` | „PIEC1: czeka na ruda” - OK |
| Niepoprawne dane: błędy konfiguracji | zły typ maszyny, literówka zasobu, zły kierunek połączenia, czas 0, dwa zamówienia, zapas ponad pojemność | wszystkie błędy z numerami wierszy, układ odrzucony | `tests/testy.dk` | zgodny - OK |
| Porównanie przy różnych zapasach | A (24 rudy) i K (12 rud) | odmowa porównania | `porownaj A K` | „rozne zapasy” - OK |
| Przypadek graniczny: pojemność magazynu | `uklady/kopalnia.txt`, magazyn SKLAD na 6 sztuk | nigdy więcej niż 6; kopalnia wydobywa dokładnie 16; krok 35 | `symuluj Z`; test po każdym kroku | zgodny - OK |
| Przypadek graniczny: bilans | wszystkie układy | zapas + wyprodukowane = wszystkie sztuki + zużyte po każdym kroku | `tests/testy.dk` | zgodny - OK |
| Testy modelu | 37 sprawdzeń | `Bledy: 0`, kod 0 | `python3 run.py --build build --target tests` | `Bledy: 0`, kod 0 - OK |
| Odtworzenie w nowym katalogu | świeży klon repozytorium | budowa, demonstracja i testy zgodne z README | `git clone`, komendy z README | macOS: OK; Linux x86_64 (Ubuntu 24.04): nie sprawdzono |
