from itertools import permutations
from operator import index


def zadanie_1():
    def koduj(napis, klucz=1):
        zakodowane = []
        for i in napis:
            uc = ord(i)
            cesar = uc + klucz
            if cesar > ord('Z'):
                cesar = ord('A') + cesar - ord('Z')
            if cesar < ord('A'):
                cesar = ord('Z') + cesar - ord('A')
            symb = chr(cesar)
            zakodowane.append(symb)

        return ''.join(zakodowane)

    def dekoduj(napis, klucz=1):
        zdekodowane = []
        for i in napis:
            uc = ord(i)
            cesar = uc - klucz
            if cesar > ord('Z'):
                cesar = ord('A') + (cesar - ord('Z') - 1)
            if cesar < ord('A'):
                cesar = ord('Z') - (ord('A') - cesar - 1)
            symb = chr(cesar)
            zdekodowane.append(symb)

        return ''.join(zdekodowane)

    def freq_counter(text):
        dictionary = {chr(x):0 for x in range(ord('A'), ord('Z')+1)}
        percent = 1 / len(text)

        for i in text:
            dictionary[i] += percent

        return dictionary


    def porównaj(freq1, freq2):
        delta = 0
        for litera, częstość in freq1.items():
            if litera not in freq2:
                delta += częstość
            else:
                delta += abs(częstość - freq2[litera])
        for litera, częstość in freq2.items():
            if litera not in freq1:
                delta += częstość
        return delta


    freq = {
        'A': 0.099, 'B': 0.0147, 'C': 0.0436, 'D': 0.0325, 'E': 0.0877, 'F': 0.003, 'G': 0.0142,
        'H': 0.0108, 'I': 0.0821, 'J': 0.0228, 'K': 0.0351, 'L': 0.0392, 'M': 0.028, 'N': 0.0572,
        'O': 0.086, 'P': 0.0313, 'Q': 0.0014, 'R': 0.0469, 'S': 0.0498, 'T': 0.0398, 'U': 0.025,
        'V': 0.004, 'W': 0.0465, 'X': 0.0002, 'Y': 0.0376, 'Z': 0.0653
    }

    wiadomość = """CNJRYVTNJRYJWRQALZFGNYVQBZH
                    CNJRYANTBEMRNTNJRYANQBYR
                    CNJRYFCBXBWALAVRJNQMVYAVXBZH
                    TNJRYANWQMVXFMRJLZLFYNYFJNJBYR
                    PVNTYRCBYBJNYCBFJBVZCBXBWH
                    GBCVRFGBMNWNPZVRQMLFGBYLFGBYXV
                    TBAVYHPVRXNYJLJENPNYXBMVBYXV
                    FGEMRYNYVGENOVYVXEMLPMNYQBMABWH""".replace(' ', '').replace('\n', '')


    simil_table = []
    decoded_text = []

    for i in range(26):
        decoded = dekoduj(wiadomość, i)
        decoded_text.append(decoded)
        freq2 = freq_counter(decoded)
        similarity = porównaj(freq, freq2)
        simil_table.append(similarity)

    results = list(zip(range(26), simil_table, decoded_text))
    sorted_results = sorted(results, key=lambda x: x[1])

    for x in sorted_results:
        print(x)


def zadanie_2():
    def levenshtein(napis1, napis2):
        if len(napis1) == 0:
            return len(napis2)
        elif len(napis2) == 0:
            return len(napis1)
        elif napis1[-1] == napis2[-1]:
            return levenshtein(napis1[:-1], napis2[:-1])
        else:
            fir = levenshtein(napis1, napis2[:-1]) + 1
            sec = levenshtein(napis1[:-1], napis2) + 1
            thd = levenshtein(napis1[-1], napis2[:-1]) + 2
            return min(fir, sec, thd)

    def guess(napis, lista):
        dict = {}

        for i in lista:
            dict[i] = levenshtein(napis, i)
        min_val = min(dict.values())

        min_keys = [k for k, v in dict.items() if v == min_val]
        return min_keys


    napis = ['lista']
    lista = ['ala', 'ma', 'kota', 'olek', 'ma', 'kotki']

    print(levenshtein('ala ma kota', 'olek ma kotki'))
    print(guess(napis, lista))


def zadanie_3():
    def brut_force(slownik, wiadomosc):
        '''
        wszystkie rozwiazania ale praktycznie nie wykonywalne przez ilość obliczeń: O(n!*m*n)
        '''
        for slownik_perm in permutations(slownik):
            temp_wiad = list(wiadomosc)
            slownik_elem = {x:list(x) for x in slownik_perm}
            max_len = len(max(slownik, key= len))

            for i, w in enumerate(temp_wiad):
                for s in slownik_elem.keys():
                    if len(slownik_elem[s]) > len(temp_wiad) - i:
                        break
                    if w == slownik_elem[s][0]:
                        slownik_elem[s].remove(w)
                        if len(slownik_elem[s]) == 0:
                            slownik_elem[s] = [True]
                        break
            solutions = [x for x in slownik_elem.keys() if slownik_elem[x][0] == True]
            print(solutions)

    def backtracking(message, slownik):
        """
        rozwiązanie heurystyczne - nie do końca optymalne rozwiazania, ale poprawne i w rozsądnym czasie - O(2^n)
        """
        slownik = sorted(slownik, key=lambda x: -len(x))  # sortowanie malejące
        best = []

        def func(current, remaining_msg, used_words, start_idx):
            nonlocal best

            if len(current) > len(best):
                best = current.copy()

            if len(best) == len(slownik):  # wszysktie słowa
                return

            for i in range(start_idx, len(slownik)):
                word = slownik[i]
                if word in used_words:
                    continue

                temp_msg = remaining_msg
                temp_msg_perm = remaining_msg
                positions = []
                valid = True
                for char in word:
                    pos = temp_msg.find(char)
                    if pos == -1:
                        valid = False
                        break

                    if positions: positions.append(pos + positions[-1] + 1)
                    else: positions.append(pos)

                    temp_msg = temp_msg[pos + 1:]

                if valid:
                    used_words.add(word)
                    current.append(word)
                    temp_msg_perm = list(temp_msg_perm)
                    for j in sorted(positions, reverse=True):
                        del temp_msg_perm[j]
                    temp_msg_perm = ''.join(temp_msg_perm)

                    func(current, temp_msg_perm, used_words, i + 1)
                    current.pop()
                    used_words.remove(word)
                else:
                    temp_msg = remaining_msg

        func([], message, set(), 0)
        return best


    slownik = {'kalafior', 'rower', 'krowa', 'pieczarka',
               'prezydent', 'usa', 'pi', 'sigma', 'python',
               'naleśniki'
               }

    wiadomosc = "uslppiapniepyrtswczehazdoyrkcnadvientjqlkjeogijpzxczx"

    # print(brut_force(slownik, wiadomosc))
    print(backtracking(wiadomosc, slownik))


if __name__ == '__main__':
    print("zadanie 1:")
    zadanie_1()
    print("\nzadanie 2:")
    zadanie_2()
    print("\nzadanie 3:")
    zadanie_3()