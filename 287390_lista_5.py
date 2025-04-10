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


if __name__ == '__main__':
    print("zadanie 1:")
    zadanie_1()
    # print("\nzadanie 2:")
    #
    # print("\nzadanie 3:")