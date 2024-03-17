######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Lassi Tuominen
# Opiskelijanumero: 001119893
# Päivämäärä: 17.11.2022
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat 
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
# 
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse 
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Tehtävä HTTavoite.py
import HTTavoiteKirjasto



def Valikko ():
    VALINTA = None
    print("Valitse haluamasi toiminto:")
    print("1) Lue tiedosto")
    print("2) Analysoi")
    print("3) Kirjoita tiedosto")
    print("4) Analysoi viikonpäivittäiset keskiarvot")
    print("5) Lue sähkönkulutusdata")
    print("6) Analysoi viikoittaiset tuntilaskut")
    print("0) Lopeta")
    try:
        VALINTA = int(input("Anna valintasi: "))
    except (Exception):
        VALINTA = "EIKOKONAISLUKU"
    return VALINTA
def paaohjelma ():
    MatriisiTulosteLista = []
    SahkoDataOlioLista = []
    MuotoiltuAnalyysi = []       
    PaivaAnalyysiLista = []
    VkpvTulos = []
    KulutusDataSanakirja = {}
    TiedostoLue = ""
    TiedostoKirjoita = ""
    while (True):
        VALINTA = Valikko()
        if (VALINTA == 0):
            print("Lopetetaan.")
            break
        elif (VALINTA == 1):
            TiedostoLue = HTTavoiteKirjasto.KysyNimi("Anna luettavan tiedoston nimi: ")
            SahkoDataOlioLista = HTTavoiteKirjasto.TiedostoLuku(TiedostoLue,SahkoDataOlioLista)
        elif (VALINTA == 2):
            if (len(SahkoDataOlioLista) != 0): #kokeillaan onko tiedot analysoitu
                MuotoiltuAnalyysi.clear() #tyhjentää listan uusia tietoja varten
                PaivaAnalyysiLista.clear()
                AnalyysiLista = HTTavoiteKirjasto.Analyysi(SahkoDataOlioLista)
                PaivaAnalyysiLista = HTTavoiteKirjasto.PaivaAnalyysi(SahkoDataOlioLista,PaivaAnalyysiLista)
                MuotoiltuAnalyysi = HTTavoiteKirjasto.AnalyysinMuotoilu(AnalyysiLista,PaivaAnalyysiLista,MuotoiltuAnalyysi)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.\n")
                continue    
        elif (VALINTA == 3):
            if(len(MuotoiltuAnalyysi) != 0):  #kokeillaan onko tiedot analysoitu
                TiedostoKirjoita = HTTavoiteKirjasto.KysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                MuotoiltuAnalyysi = HTTavoiteKirjasto.TiedostoKirjoitus(TiedostoKirjoita,MuotoiltuAnalyysi)
            else:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.\n")
                continue
        elif (VALINTA ==4):
            if(len(SahkoDataOlioLista) != 0):  #kokeillaan onko tiedot luettu
                VkpvKirjoitus = HTTavoiteKirjasto.KysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                VkpvTulos = HTTavoiteKirjasto.VkpvAnalyysi(SahkoDataOlioLista,VkpvTulos)
                HTTavoiteKirjasto.TiedostoKirjoitus(VkpvKirjoitus,VkpvTulos)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.\n")
                continue
        elif (VALINTA == 5):
            if(len(SahkoDataOlioLista) != 0):
                KulutusDataTiedosto = HTTavoiteKirjasto.KysyNimi("Anna luettavan tiedoston nimi: ")
                KulutusDataSanakirja = HTTavoiteKirjasto.KulutusAnalyysi(KulutusDataSanakirja,SahkoDataOlioLista,KulutusDataTiedosto)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.\n")
                continue
        elif (VALINTA == 6):
            if(len(SahkoDataOlioLista) !=0 and len(KulutusDataSanakirja) != 0):
                MatriisiTulosteLista = HTTavoiteKirjasto.MatriisiMuotoilu(KulutusDataSanakirja,SahkoDataOlioLista,MatriisiTulosteLista)
                MatriisiKirjoitus = HTTavoiteKirjasto.KysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                HTTavoiteKirjasto.TiedostoKirjoitus(MatriisiKirjoitus,MatriisiTulosteLista)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.\n")
                continue
        elif (VALINTA == "EIKOKONAISLUKU"):
            print("Anna valinta kokonaislukuna.")
        else:
            print("Tuntematon valinta, yritä uudestaan.")
        print()
    print("\nKiitos ohjelman käytöstä.")
    SahkoDataOlioLista.clear()
    PaivaAnalyysiLista.clear()
    MuotoiltuAnalyysi.clear()
    VkpvTulos.clear()
    KulutusDataSanakirja.clear()
    MatriisiTulosteLista.clear()
    return None
paaohjelma ()
#eof
