

def dodaj_predznake(niz):
    en_clen = ""
    s = []
    pozitivno = True if niz[0] != "-" else False
    pretvorba = {1: "", 0: "-"}
    for i, c in enumerate(niz):
        if i == 0 and not pozitivno:
            continue
        if c == "+" or c == "-":
            if "X" in en_clen and en_clen.split("X")[0] == "":
                en_clen = "1X" + "".join(en_clen.split("X")[1:])
            s.append(pretvorba[pozitivno] + en_clen)
            pozitivno = 1 if c == "+" else 0
            en_clen = ""
            continue
        en_clen += c
    if "X" in en_clen and en_clen.split("X")[0] == "":
        en_clen = "1X" + "".join(en_clen.split("X")[1:])
    s.append(pretvorba[pozitivno] + en_clen)
    return s


def niz_v_terko_stopnja_vrednost(s):
    r = []
    for vrednost in s:
        if "^" in vrednost:
            vrednost_stopnja = vrednost.split("^")
            moja_vrednost, stopnja = vrednost_stopnja[0].split("X")[0], vrednost_stopnja[1]
            r.append((moja_vrednost, int(stopnja)))
        else:
            if "X" in vrednost:
                prva_stopnja = vrednost.split("X")[0] if vrednost.split("X")[0] != "" else 1
                r.append((prva_stopnja, 1))
                continue
            r.append((vrednost, 0))

    return sorted(r, key=lambda x: x[1])


def naredi_prazne(spo_mej, zgo_meja):
    t = []
    for x in range(spo_mej,zgo_meja):
        t.append((0,x))
    return t


def napolni_polinom(s):
    s = sorted(s, key=lambda x: x[1])
    if s[-1][1] == len(s)-1:
        return s  # že poln
    dodatek = []
    for i,(_, stopnja) in enumerate(s, start=1):
        if i == 1 and stopnja != 0:
            dodatek += naredi_prazne(0, stopnja)
        if i==len(s):
            break
        razlika = s[i][1] - stopnja
        if razlika != 1:
            dodatek += naredi_prazne(stopnja+1, s[i][1])
    s += dodatek
    return sorted(s, key=lambda x: x[1])


def transformiraj(inp):
    # input --> "x^2 + 3x + 1"
    inp = "".join([c.capitalize() for c in inp if c != " "])  # remove whitespace
    s = dodaj_predznake(inp)
    if "" in s:
        return None
    s = niz_v_terko_stopnja_vrednost(s)
    s = napolni_polinom(s)
    return s[::-1]  # output --> [(x,y) --> x = vrednost, y = stopnja


def vsi_delitelji(stevilo):
    return [x for x in range(1,stevilo+1) if stevilo%x==0] if stevilo !=0 else [0]


def horner(poly):
    delitelji = vsi_delitelji(abs(int(poly[-1][0])))
    delitelji = delitelji + [-st for st in delitelji]
    nicle = []
    for delitelj in delitelji:
        dyn = 0
        for i,(koef,stopnja) in enumerate(poly):
            dyn += int(koef)
            if i == len(poly)-1:
                break
            dyn *= delitelj
        if dyn == 0:
            nicle.append(delitelj)
    return nicle
print("Primer: x^5 - 8x^4 -72x^3 + 382x^2 + 727x - 2310")
while True:
    try:
        allowed_chars = "xX0123456789^+- "
        while True:
            inp = input("P: ")
            for c in inp:
                if c not in allowed_chars:
                    print("sorry...check your input again")
                    break
            else:
                break
        print(horner(transformiraj(inp)))
        break
    except ValueError:
         print(f"Sorry something went wrong...\n{inp} was your input")
