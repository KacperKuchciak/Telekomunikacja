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
    for kolumna in range(0, 8):
        suma += (wiadomosc_integer[kolumna] * H[wiersz][kolumna])
    return suma % 2


if __name__ == '__main__':
    while True:

        """
        Menu pozwalające wybrać co chemy zrobić.
        """

        wybor: int = 0
        print("Wybierz operacje, ktora chcesz wykonac:")
        while wybor != 1 | wybor != 2 | wybor != 3:
            wybor = int(input("1.Zakoduj podana w pliku wiadomosc,\n"
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
        if wybor == 5:
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
                print("Zczytany znak w postaci binarnej")
                print(zakodowana_wiadomosc)


                """
                TODO: sprawdzanie i poprawianie bledu
                """


                """
                Mechanizm sprawdzania i poprawiania bledow pozwala nam uzyc juz gotowej pierwsze osemki bitow 
                z wiadomosci by przekonwertowac ja na ASCII i odczytac.
                """
                fragment_do_odkodowania = zakodowana_wiadomosc[:8]
                plik2.write(chr(int(fragment_do_odkodowania[:8], 2)))
                """
                Konwertujemy jakiegos inta na chara, a wiec na jakis element tablicy ASCII.
                Fragment int(str, 2) mowi, ze to co podamy w stringu bedzie w systemie dwojkowym i ma to
                przeliczyc na dziesietny, potem poda do chara i ten wypluje na przyklad char(65) czyli A
                """
                print(chr(int(fragment_do_odkodowania[:8], 2)))
            print("Zadekodowano wiadomosc")
            plik2.close()