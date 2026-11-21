#!/usr/bin/env python3
"""Niezależny model referencyjny DuckFactory w Pythonie (do sprawdzania liczb, nie do oceny).

Odtwarza te same reguły kroku co program w Ducklingu (opis w README), aby testy w Ducklingu
porównywały wyniki z obliczeniami wykonanymi osobno. Zakłada poprawną konfigurację.
Użycie: python3 narzedzia/model_referencyjny.py uklady/szeregowy.txt [uklady/inny.txt ...]
"""
import sys


def wczytaj(sciezka):
    rec, el, pol, zapas, zam, limit = {}, {}, [], [], None, 10000
    kolejnosc = []
    for linia in open(sciezka, encoding="utf-8"):
        s = linia.split("#")[0].split()
        if not s:
            continue
        k = s[0]
        if k == "receptura":
            nazwa, typ, czas = s[1], s[2], int(s[3])
            strz = s.index("->")
            we = [(a.split(":")[0], int(a.split(":")[1])) for a in " ".join(s[4:strz]).replace(" ", "").split(",")]
            wy = [(a.split(":")[0], int(a.split(":")[1])) for a in " ".join(s[strz + 1:]).replace(" ", "").split(",")]
            rec[nazwa] = dict(typ=typ, czas=czas, we=we, wy=wy)
        elif k == "magazyn":
            el[s[1]] = dict(rodzaj="magazyn", poj=None if s[2] == "bez_limitu" else int(s[2]), zap={})
            kolejnosc.append(s[1])
        elif k == "zrodlo":
            el[s[1]] = dict(rodzaj="zrodlo", zasob=s[2], na_krok=int(s[3]), limit=int(s[4]), wydano=0, wy={})
            kolejnosc.append(s[1])
        elif k == "maszyna":
            el[s[1]] = dict(rodzaj="maszyna", rec=s[3], we={}, wy={}, poz=0, gotowe=False,
                            cykle=0, praca=0, glod=0, blokada=0)
            kolejnosc.append(s[1])
        elif k == "polaczenie":
            pol.append(dict(z=s[1], do=s[2], zasob=s[3], prz=int(s[4]), op=int(s[5])))
        elif k == "zapas":
            zapas.append((s[1], s[2], int(s[3])))
        elif k == "zamowienie":
            zam = (s[1], int(s[2]), s[3])
        elif k == "limit":
            limit = int(s[1])
    for m, z, n in zapas:
        el[m]["zap"][z] = el[m]["zap"].get(z, 0) + n
    return rec, el, kolejnosc, pol, zam, limit


def symuluj(sciezka):
    rec, el, kol, pol, zam, limit = wczytaj(sciezka)
    w_drodze = []  # [dociera, polaczenie, ilosc]

    def dostepne(e, z):
        return e["zap"].get(z, 0) if e["rodzaj"] == "magazyn" else e["wy"].get(z, 0)

    def zdejmij(e, z, n):
        d = e["zap"] if e["rodzaj"] == "magazyn" else e["wy"]
        d[z] -= n

    def w_transporcie(nazwa, z):
        return sum(p[2] for p in w_drodze if pol[p[1]]["do"] == nazwa and pol[p[1]]["zasob"] == z)

    def w_transporcie_razem(nazwa):
        return sum(p[2] for p in w_drodze if pol[p[1]]["do"] == nazwa)

    def wolne(nazwa, z):
        e = el[nazwa]
        if e["rodzaj"] == "magazyn":
            if e["poj"] is None:
                return 10 ** 12
            return e["poj"] - sum(e["zap"].values()) - w_transporcie_razem(nazwa)
        if e["rodzaj"] == "maszyna":
            r = rec[e["rec"]]
            potrzeba = dict(r["we"]).get(z, 0)
            return 2 * potrzeba - e["we"].get(z, 0) - w_transporcie(nazwa, z)
        return 0

    t = 0
    while t < limit:
        t += 1
        ruch = False
        # 1. dostawy
        nowe = []
        for p in w_drodze:
            if p[0] == t:
                c = pol[p[1]]
                e = el[c["do"]]
                d = e["zap"] if e["rodzaj"] == "magazyn" else e["we"]
                d[c["zasob"]] = d.get(c["zasob"], 0) + p[2]
                ruch = True
            else:
                nowe.append(p)
        w_drodze = nowe
        # 2. maszyny
        for nazwa in kol:
            e = el[nazwa]
            if e["rodzaj"] != "maszyna":
                continue
            r = rec[e["rec"]]
            pracowala = False
            if e["gotowe"]:
                if all(e["wy"].get(z, 0) + n <= 2 * n for z, n in r["wy"]):
                    for z, n in r["wy"]:
                        e["wy"][z] = e["wy"].get(z, 0) + n
                    e["gotowe"] = False
                    e["cykle"] += 1
                    ruch = True
            if not e["gotowe"] and e["poz"] == 0:
                if all(e["we"].get(z, 0) >= n for z, n in r["we"]):
                    for z, n in r["we"]:
                        e["we"][z] -= n
                    e["poz"] = r["czas"]
                    ruch = True
            if e["poz"] > 0:
                pracowala = True
                ruch = True
                e["praca"] += 1
                e["poz"] -= 1
                if e["poz"] == 0:
                    if all(e["wy"].get(z, 0) + n <= 2 * n for z, n in r["wy"]):
                        for z, n in r["wy"]:
                            e["wy"][z] = e["wy"].get(z, 0) + n
                        e["cykle"] += 1
                    else:
                        e["gotowe"] = True
            if not pracowala:
                if e["gotowe"]:
                    e["blokada"] += 1
                else:
                    e["glod"] += 1
        # 3. źródła
        for nazwa in kol:
            e = el[nazwa]
            if e["rodzaj"] == "zrodlo":
                n = min(e["na_krok"], e["limit"] - e["wydano"])
                if n > 0:
                    e["wy"][e["zasob"]] = e["wy"].get(e["zasob"], 0) + n
                    e["wydano"] += n
                    ruch = True
        # 4. transport
        for i, c in enumerate(pol):
            n = min(c["prz"], dostepne(el[c["z"]], c["zasob"]), wolne(c["do"], c["zasob"]))
            if n > 0:
                zdejmij(el[c["z"]], c["zasob"], n)
                w_drodze.append([t + c["op"], i, n])
                ruch = True
        # 5. zamówienie
        produkt, ile, cel = zam
        if el[cel]["zap"].get(produkt, 0) >= ile:
            return t, True, el, kol
        if not ruch and not w_drodze:
            return t, False, el, kol
    return t, False, el, kol


def main():
    for sciezka in sys.argv[1:]:
        t, ok, el, kol = symuluj(sciezka)
        print(f"{sciezka}: {'ukonczono w kroku' if ok else 'stop w kroku'} {t}")
        for nazwa in kol:
            e = el[nazwa]
            if e["rodzaj"] == "maszyna":
                print(f"  {nazwa}: cykle {e['cykle']} praca {e['praca']} glod {e['glod']} blokada {e['blokada']}")
            elif e["rodzaj"] == "magazyn":
                print(f"  {nazwa}: {dict(sorted(e['zap'].items()))}")
            else:
                print(f"  {nazwa}: wydano {e['wydano']} w buforze {e['wy']}")


if __name__ == "__main__":
    main()
