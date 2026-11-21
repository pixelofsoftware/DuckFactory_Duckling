# DuckFactory - symulator fabryki w Ducklingu

Zespół: Pixel of Software (Marcin Kowalczyk). Temat: P03 DuckFactory. Skład: 1 osoba.

Program symuluje fabrykę krok po kroku. Fabryka to maszyny, które przerabiają surowce według receptur, magazyny i źródła surowców, a stałe połączenia przewożą między nimi zasoby. Program porównuje dwa układy realizujące to samo zamówienie przy tych samych zapasach początkowych: który jest szybszy i co go ogranicza.

Całe minimum karty P03 działa i jest sprawdzone testami. Z rozszerzeń są:
* magazyny o ograniczonej pojemności;
* transport z przepustowością i czasem przejazdu;
* źródła z limitem;
* wykorzystanie maszyn i wykrywanie wąskiego gardła;
* diagnoza zatrzymania produkcji;
* podgląd kolejnych kroków.

## Uruchomienie

Wymagane są Python 3 i Duckling (`duckc` w `PATH`, instalacja według tutoriala). Z katalogu projektu:

```bash
python3 build.py --target all --output build               # aplikacja i testy, wariant natywny
python3 run.py --build build --workdir .                    # interfejs tekstowy; wpisz 'pomoc'
python3 run.py --build build --workdir . < demo/demo.txt    # cała demonstracja z pliku
python3 run.py --build build --target tests                 # testy: PASS/FAIL, kod = liczba błędów
```

`--workdir .` sprawia, że ścieżki do układów (np. `uklady/szeregowy.txt`) liczą się od katalogu projektu. Program czyta polecenia ze standardowego wejścia. Kod zakończenia to 0, gdy wszystkie polecenia się powiodły, albo 1, gdy któreś się nie udało; niezrealizowane zamówienie też liczy się jako niepowodzenie. `build.py` i `run.py` to niezmienione skrypty z szablonu konkursu.

## Funkcje i demonstracja

| Funkcja z minimum tematu | Sposób uruchomienia | Oczekiwany rezultat |
| --- | --- | --- |
| 3 rodzaje maszyn, 3 receptury w łańcuchu | `wczytaj A uklady/szeregowy.txt` | piec: 2 ruda → 1 metal (3 kroki); krajarka: 1 metal → 1 płytka (2 kroki); montownia: 2 płytki → 1 moduł (4 kroki) |
| Magazyny i transport po stałych połączeniach | `przebieg A 1 6` | zdarzenia każdego kroku: dostawy, start i koniec cykli, transport z czasem dotarcia |
| Symulacja krok po kroku z ograniczoną szybkością | `symuluj A` | zamówienie 6 modułów zrealizowane w kroku 44; cykle i wykorzystanie maszyn |
| Raport i porównanie dwóch układów przy tych samych zapasach | `porownaj A B` | A: krok 44, B (dwa piece): krok 33; B szybszy o 11 kroków; wąskie gardło A: piec, B: krajarka |
| Brak surowca zatrzymuje produkcję | `wczytaj K uklady/przyklad-karty.txt`, `symuluj K` | z 12 rudy powstają 3 moduły; zamówienie na 4 niezrealizowane, stop w kroku 27, z opisem przyczyn |
| Brak połączenia zatrzymuje część produkcji | `wylacz A KRAJARKA1 MONTAZ1`, `symuluj A` | krajarka i piec się blokują, montownia czeka na płytki; stop w kroku 26 |
| Źródło z limitem, magazyn o pojemności | `wczytaj Z uklady/kopalnia.txt`, `symuluj Z` | kopalnia wydobywa dokładnie 16 rudy; zamówienie 4 modułów w kroku 35 |

**Demonstracja** (`demo/demo.txt`) uruchamia oba układy z tym samym zamówieniem i porównuje czas realizacji z wyjaśnieniem różnicy. Potem pokazuje:
1. pierwsze kroki: kiedy maszyna pobiera surowce i kiedy produkt jest dostępny;
2. przykład z karty (12 rudy, najwyżej 3 moduły);
3. źródło z limitem;
4. skutki wyłączenia jednego połączenia;
5. skutki braku surowca.

## Środowisko i zależności

| Element | Wartość |
| --- | --- |
| Kompilator | `duckc 0.3-alpha (83882805a 2026-11-20)`, `commit-hash: 83882805a` |
| Uruchomienie | natywnie (`--mode native`) |
| System operacyjny | macOS 27.2, Apple Silicon (arm64) |
| Zależności | Python 3 (do `build.py`, `run.py` i modelu referencyjnego) i Duckling; brak innych bibliotek |

Pliki są czytane przez `fopen`/`fread`/`fclose` ze standardowej biblioteki C, takie same na Linuksie i macOS. Budowę i testy sprawdziłem na macOS. Na Linuksie x86_64 (Ubuntu 24.04) i w wariancie DVM projektu nie sprawdzałem.

## Struktura i działanie

| Plik | Odpowiedzialność |
| --- | --- |
| `app/app.dk` | punkt wejścia: czyta polecenia wiersz po wierszu i wypisuje odpowiedzi |
| `app/sesja.dk` | polecenia: wczytanie układów, symulacja, przebieg, porównanie, wyłączanie połączeń, zmiana zapasów |
| `app/konfiguracja.dk` | odczyt i walidacja pliku układu (błędy z numerami wierszy) |
| `app/model.dk` | dane: zasoby, receptury, elementy, połączenia, przesyłki |
| `app/symulacja.dk` | reguły jednego kroku, symulacja, bilans zasobów |
| `app/raport.dk` | raport produkcji, diagnoza zatrzymania, wąskie gardło, porównanie układów |
| `app/tekst.dk`, `app/pliki.dk` | pomocnicze operacje na tekście i odczyt plików |
| `tests/testy.dk` | testy modelu i poleceń, bez plików |
| `narzedzia/model_referencyjny.py` | niezależny model w Pythonie, z którego pochodzą liczby oczekiwane w testach |
| `uklady/*.txt` | konfiguracje układów do porównania i demonstracji |

**Format układu** (`uklady/*.txt`): jedno polecenie w wierszu, `#` zaczyna komentarz, a kolejność wierszy jest dowolna.

```
receptura NAZWA TYP_MASZYNY CZAS zasob:ilosc[,zasob:ilosc] -> zasob:ilosc[,...]
magazyn NAZWA POJEMNOSC|bez_limitu
zrodlo NAZWA ZASOB NA_KROK LIMIT
maszyna NAZWA TYP_MASZYNY RECEPTURA
polaczenie Z DO ZASOB PRZEPUSTOWOSC OPOZNIENIE
zapas MAGAZYN ZASOB ILOSC
zamowienie ZASOB ILOSC MAGAZYN
limit MAKS_KROKOW            (domyślnie 10000)
```

Program sprawdza każdy wiersz i zgłasza wszystkie błędy naraz. Układ z błędem nie jest przyjmowany wcale. Sprawdza między innymi:
* czy maszyna ma typ zgodny z recepturą;
* czy połączenie przewozi zasób, który nadawca wytwarza, a odbiorca potrzebuje;
* nieznane zasoby, czyli literówki;
* powtórzone nazwy;
* zapas większy od pojemności magazynu;
* czy jest dokładnie jedno zamówienie.

**Jednostka czasu:** 1 krok, w przykładach umownie 1 minuta. **Kolejność zdarzeń w kroku t** jest zawsze ta sama, a elementy są obsługiwane w kolejności z pliku:

1. **Dostawy:** przesyłki z czasem dostawy t trafiają do odbiorcy. Miejsce zostało zarezerwowane przy wysyłce, więc pojemność nigdy nie jest przekroczona.
2. **Maszyny:**
   * maszyna z gotowym produktem, który się nie mieścił, próbuje go oddać;
   * wolna maszyna zaczyna cykl, jeśli bufor wejściowy ma komplet surowców;
   * pracująca maszyna odlicza krok, a po ostatnim kroku cyklu produkt trafia do bufora wyjściowego.
3. **Źródła** wydobywają do swojego bufora najwyżej „na krok”, łącznie najwyżej limit.
4. **Transport:** każde połączenie wysyła min(przepustowość, dostępne u nadawcy, wolne miejsce u odbiorcy, z uwzględnieniem przesyłek już w drodze). Przesyłka dociera w kroku t + opóźnienie.
5. **Zamówienie** jest zrealizowane, gdy magazyn docelowy ma zamówioną ilość na koniec kroku.

**Kiedy maszyna pobiera surowce i kiedy produkt jest dostępny.** Surowce są pobierane w całości w chwili startu cyklu. Cykl o czasie c zaczęty w kroku t kończy się w kroku t + c − 1. Produkt jest wtedy w buforze wyjściowym i może wyjechać w tym samym kroku. Przykład: piec dostaje rudę w kroku 2, zaczyna od razu, a metal jest gotowy w kroku 4 i dociera do krajarki w kroku 5.

Bufor maszyny mieści 2 komplety wejść i 2 komplety wyjść receptury.

**Brak surowca:** maszyna bez kompletu surowców nie zaczyna cyklu i liczy krok „czeka na surowiec”. Produkt nigdy nie powstaje bez pobranych surowców; testy sprawdzają to bilansem po każdym kroku: zapas + wyprodukowane = wszystkie sztuki + zużyte.

**Brak miejsca:** gdy produkt się nie mieści, maszyna jest zablokowana do czasu zwolnienia miejsca.

**Zatrzymanie:** gdy w kroku nic się nie wydarzyło i nic nie jest w drodze, produkcja stanęła. Raport podaje wtedy:
* na co czeka każda maszyna;
* które maszyny są zablokowane;
* wyczerpane źródła i wyłączone połączenia;
* gdzie zostały zasoby.

**Źródło** (`zrodlo`) wydobywa NA_KROK sztuk w każdym kroku, aż wydobędzie łącznie LIMIT. W porównaniu układów limity źródeł liczą się razem z zapasami.

**Wykorzystanie i wąskie gardło.** Dla każdej maszyny raport podaje odsetek kroków:
* pracy;
* czekania na surowiec;
* blokady.

Wąskim gardłem jest maszyna o najwyższym wykorzystaniu. W układzie A to piec (81.82% kroków), a krajarka i montownia czekają na jego metal. W układzie B dwa piece podwajają dostawy metalu i ograniczeniem staje się krajarka (72.73%). Zamówienie kończy się 11 kroków wcześniej.

**Porównanie układów** jest dozwolone tylko przy tych samych zapasach początkowych i limitach źródeł (porównanych po nazwach zasobów) oraz przy tym samym zamówieniu. Każda symulacja zaczyna od stanu początkowego układu, więc wyniki są powtarzalne.

**Ograniczenia:**
* połączenia są stałe, nie ma priorytetów;
* gdy kilka połączeń ciągnie z jednego miejsca, decyduje kolejność z pliku;
* nie ma energii ani awarii;
* zmiany poleceniami `wylacz` i `zapas` dotyczą tylko bieżącej sesji.

## Sprawdzenie projektu

```bash
python3 run.py --build build --target tests                       # 37 sprawdzeń
python3 run.py --build build --workdir . < demo/demo.txt
python3 narzedzia/model_referencyjny.py uklady/szeregowy.txt uklady/rownolegly.txt uklady/przyklad-karty.txt uklady/kopalnia.txt
```

Model referencyjny w Pythonie liczy te same reguły niezależnie od programu. Testy w Ducklingu porównują z nim liczbę kroków oraz cykle i kroki pracy, czekania i blokady każdej maszyny we wszystkich układach. Testy sprawdzają też:
* walidację konfiguracji;
* bilans zasobów po każdym kroku;
* pojemność magazynu;
* chwilę pobrania surowców i powstania produktu;
* skutki braku połączenia i surowca;
* porównanie i odrzucenie porównania przy różnych zapasach.

Scenariusze z wynikami są w [tests/scenariusze.md](tests/scenariusze.md).

## Autorstwo i materiały

Kod i dokumentacja: Pixel of Software (Marcin Kowalczyk), z pomocą asystenta AI. Szczegóły są w [ZRODLA.md](ZRODLA.md). Licencja: MIT (plik `LICENSE`, szablon Fundacji Duckling z dopisanym autorem).
