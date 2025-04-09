import random
from pomiar_algorytmy import zmierz_sortowanie, sortowanie_bąbelkowe, sortowanie_scalanie, sortowanie_wstawianie, sortowanie_wybieranie


def zadanie_1():
    def inwersje(n):
        L = random.sample(range(n*2), n)
        print(f"lista f:inwersje {L}")
        pary = []

        for i in range(n):
            for j in range(i, n):
                if L[i] > L[j]:
                    pary.append((L[i], L[j]))

        return pary

    def rank(n):
        L = random.sample(range(n*2), n)
        print(f"lista f:rank {L}")
        S = sorted(L)
        R = []

        for i in range(n):
            current = L[i]
            for j in range(n):
                R.append(j) if S[j] == current else None

        return R


    print(f"inwersje: {inwersje(4)}")
    print(f"rangi: {rank(4)}")


def zadanie_2():
    def sortowanie_zliczanie(lista, klucze):
        wystapienia = {x: 0 for x in klucze}

        for x in lista:
            wystapienia[x] += 1

        pozycje = {x: 0 for x in klucze}
        pozycja = 0

        for x in range(1, len(klucze)):
            pozycja += wystapienia[klucze[x - 1]]
            pozycje[klucze[x]] += pozycja

        posortowana = [None for _ in lista]
        for x in lista:
            posortowana[pozycje[x]] = x
            pozycje[x] += 1

        return posortowana


    algorytmy = {sortowanie_bąbelkowe:[],
                 sortowanie_scalanie:[],
                 sortowanie_wstawianie:[],
                 sortowanie_wybieranie:[],
                 }

    lista = [random.randint(0, 9) for x in range(1_000)]
    klucze = list(range(10))
    #
    for algorytm in algorytmy:
        algorytmy[algorytm] = zmierz_sortowanie(algorytm, lista)

    def sortowanie_zliczanie_shell(lista):
        sortowanie_zliczanie(lista, klucze)

    algorytmy[sortowanie_zliczanie] = zmierz_sortowanie(sortowanie_zliczanie_shell, lista)

    for algorytm in algorytmy:
        print(f"{algorytm.__name__}: {algorytmy[algorytm]} sekund")


def zadanie_3():
    def sortowanie_zliczanie(lista, k):
        klucze = list(range(10))
        wystapienia = [0] * len(klucze)
        pozycje = [0] * len(klucze)

        for x in lista:
            strx = str(x)
            if len(strx) >= k:
                wystapienia[int(strx[-k])] += 1
            else:
                wystapienia[0] += 1

        pozycja = 0
        for x in range(1, len(klucze)):
            pozycja += wystapienia[x - 1]
            pozycje[x] += pozycja

        posortowana = [None for _ in lista]

        for x in lista:
            strx = str(x)
            if len(strx) <= k:
                strx = "0"*k  + strx

            posortowana[pozycje[int(strx[-k])]] = x
            pozycje[int(strx[-k])] += 1


        return posortowana


    def sortowanie_pozycyjne(lista):
        max_k = len(str(max(lista)))
        lista_copy = lista.copy()

        for k in range(1, max_k+1):
            lista_copy = sortowanie_zliczanie(lista_copy, k)

        return lista_copy

    lista = [random.randint(0, 100) for x in range(15)]

    print(f"Oryginalna lista: {lista}")
    print(f"Posortowana lista: {sortowanie_pozycyjne(lista)}")

if __name__ == '__main__':
    print("zadanie 1:")
    zadanie_1()
    print("\nzadanie 2:")
    zadanie_2()
    print("\nzadanie 3:")
    zadanie_3()