"""
Macierz Hamminga wykorszystywana w zadaniu.
"""

H = [[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
     [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
     [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
     [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]]

"""
Otrzymujemy tablicę intów znaku do zakodowania. Bity wiadomości przepisujemy,
zaś dodatkowo dołączamy bity parzystości obliczane odpowiednią funkcją
(iloczyn macierzy H i wektora przedstawiającego wiadomość do zakodowania).
"""


def zakoduj(wiadomosc_integer):
    wiadomosc_po_zakodowaniu = []
    for bit in wiadomosc_integer:
        wiadomosc_po_zakodowaniu.append(bit)
    for wiersz in range(0, 8):
        wiadomosc_po_zakodowaniu.append(obliczBitParzystosci(wiersz, wiadomosc_integer))
    return wiadomosc_po_zakodowaniu


"""
Obliczamy składową iloczynu macierzy H i wektora z wiadomością dla
poszczególnej kolmny. Otrzymujemy odpowiedni bit parzystości.
"""


def obliczBitParzystosci(wiersz, wiadomosc_integer):
    suma: int = 0
    for kolumna in range(len(wiadomosc_integer)):
        suma += (wiadomosc_integer[kolumna] * H[wiersz][kolumna])
    return suma % 2


"""
Funkcja wykrywająca miejsce błędu. Dzięki pomnożeniu wiadomości przez
daną kolumnę macierzy, zostaje wygenerowany wektor błędu. O błędzie świadczy
obecność, w jakimkolwiek miejscu, jedynki w wektorze błędu.
"""


def dokonajSprawdzenia(wiadomosc_integer):
    Blad = []
    flaga = True
    for wiersz in range(0, 8):
        suma = obliczBitParzystosci(wiersz, wiadomosc_integer)
        Blad.append(suma)
        if suma == 1:
            flaga = False
    if not flaga:
        print("Wektor błędu:", Blad)
        wiadomosc_integer = dokonajPoprawy(wiadomosc_integer, Blad)
    elif flaga:
        print("Nie wykryto błędu")
    return wiadomosc_integer


"""
Funkcja wyszukująca, w którym miejscu znajduje się błąd i poprawiająca go.
W przypadku jednego błędu:
- porównuje wektor błędu z kolumnami w macierzy. Jeśli jakaś kolumna i wektor będą
sobie równe, to w tym miejscu w wiadomości znajduje się błąd. Działa na zasadzie
takiej, że jeżeli np. wektor błędu zgadza się z trzecią kolumną, to w trzecim miejscu
w wiadomości znajduje się błąd. Bit w tym miejscu program zmienia na przeciwny.
Jeżeli funkcja nie wykryje błędu, to przechodzi do drugiego przypadku, dwóch błędów
W przypadku dwóch błędów:
- XOR'uje ze sobą 2 kolumny w macierzy i porównuje je z wektorem błędu. W przypadku, gdy
suma kolumn = wektorowi błędu, następuje wykrycie błędu.
"""


def dokonajPoprawy(wiadomosc_integer, Blad):
    for kolumna in range(0, 16):
        for wiersz in range(0, 8):
            if H[wiersz][kolumna] != Blad[wiersz]:
                break
            if wiersz == 7:
                wiadomosc_integer[kolumna] = zmien(wiadomosc_integer[kolumna])
    for kolumna in range(0, 16):
        for i in range(kolumna, 16):
            for wiersz in range(0, 8):
                if H[wiersz][kolumna] ^ H[wiersz][i] != Blad[wiersz]:
                    break
                if wiersz == 7:
                    wiadomosc_integer[kolumna] = zmien(wiadomosc_integer[kolumna])
                    wiadomosc_integer[i] = zmien(wiadomosc_integer[i])
    print("Poprawiony znak:")
    print(wiadomosc_integer)
    return wiadomosc_integer


"""
Funkcja zmieniajaca bit na przeciwny.
"""


def zmien(bit):
    if bit == 0:
        return 1
    else:
        return 0

if __name__ == '__main__':
    while True:

        """
        Menu pozwalające wybrać co chemy zrobić.
        """
        wybor:int = 0
        while wybor not in range(1, 3):
            wybor:int = int(input("1.Zakoduj podana w pliku wiadomosc,\n"
                              "2.Odkoduj i sprawdz zakodowana wiadomosc.\n"
                              "3.Wyjdz z programu\n"))
        if wybor == 3:
            break
        if wybor == 1:

            """
            plik1 - zawiera wiadomość, z której zczytujemy jej bity i
            przedstawiamy je jako znaki w formie napisu.
            
            plik2 i 3 - tu zapisujemy wiadomość po zakodowaniu przy pomocy macierzy Hamminga.
            Jednen będzie używany do odczytu przy dekodowaniu, zaś drugi posłuży do porównania,
            gdybyśmy wprowadzili celowo jakiś błąd do pliku dekodowanego.
            """

            plik1 = open('wiadomosc.txt', 'r')
            plik2 = open('zakodowana_wiadomosc_oryginal.txt', 'w')
            plik3 = open('zakodowana_wiadomosc_kopia.txt', 'w')
            wczytana_linia = plik1.read()
            postac_binarna = ''.join(format(ord(i), '08b') for i in wczytana_linia)

            """
            Dla każdego znaku z osobna będziemy kodować, dlatego tniemy nasz napis co 8 znaków symbolizujących bity.
            Następnie, aby można było wygodnie oddziaływać na poszczególnych reprezentacjach bitów, tworzymy listę
            reprezentującą bity jako integer. Funkcja "zakoduj" koduje tak przygotowaną postać binarną znaku ASCII,
            a następnie zapisuje jeden po drugim każdy taki kod bitowy do obu wymienionych wcześniej plików.
            """

            for i in range(0, int(len(postac_binarna)), 8):
                wiadomosc_napis = postac_binarna[i:i + 8]
                wiadomosc_integer = []
                for bit in wiadomosc_napis:
                    wiadomosc_integer.append(int(bit))
                for bit in zakoduj(wiadomosc_integer):
                    plik2.write(str(bit))
                    plik3.write(str(bit))
            print("Kodowanie wiadomosci zostalo zakonczone.\n\n")
            plik1.close()
            plik2.close()
            plik3.close()
        if wybor == 2:
            print("zaczynam")
            plik1 = open("zakodowana_wiadomosc_oryginal.txt", 'r')
            plik2 = open("zdekodowana_wiadomosc.txt", 'w')
            wczytana_linia = plik1.read()
            plik1.close()
            """
            Ponizszy for pozwala nam operowac na poszczegolnych szesnastkach bitow, 
            czyli u nas na jednej literce.
            """
            for i in range(int(len(wczytana_linia) / 16)):
                zakodowana_wiadomosc = str(wczytana_linia[i * 16: (i + 1) * 16])
                bity = []
                for j in range(16):
                    bity.append(int(zakodowana_wiadomosc[j]))
                print("Zczytany znak w postaci binarnej")
                print(bity)
                wiad_int = dokonajSprawdzenia(bity)
                napis = ""
                for k in range(16):
                    napis += str(wiad_int[k])

                """
                Mechanizm sprawdzania i poprawiania bledow pozwala nam uzyc juz gotowej pierwsze osemki bitow 
                z wiadomosci by przekonwertowac ja na ASCII i odczytac.
                """
                fragment_do_odkodowania = napis[:8]
                plik2.write(chr(int(fragment_do_odkodowania[:8], 2)))
                """
                Konwertujemy jakiegos inta na chara, a wiec na jakis element tablicy ASCII.
                Fragment int(str, 2) mowi, ze to co podamy w stringu bedzie w systemie dwojkowym i ma to
                przeliczyc na dziesietny, potem poda do chara i ten wypluje na przyklad char(65) czyli A
                """
                print(chr(int(fragment_do_odkodowania[:8], 2)))
            print("Zdekodowano wiadomosc")
            plik2.close()