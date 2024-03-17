######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Lassi Tuominen
# Opiskelijanumero: 001119893
# Päivämäärä: 13.11.2022
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat 
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
# 
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse 
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Tehtävä HTTavoiteKirjasto.py
import datetime
import sys
import numpy
##Kiintoarvot##
EROTIN = ";"
##Luokat""
class ANALYYSINTULOKSET:
    Keskihinta = None
    Halvin = None
    Halvinaika = None
    Kallein = None
    Kalleinaika = None
    Tunnit = None

class SAHKODATA :
    Aika = None
    Hinta = None
##ALiohjelmat##
def KysyNimi (Indeksi):
    Syote = input(Indeksi)
    return Syote

def TiedostoLuku (TiedostoLue,TiedotLista):
    try:
        TiedotLista.clear()
        tiedosto = open(TiedostoLue, "r")
        rivi = tiedosto.readline()
        rivi = tiedosto.readline() #otsikkorivi pois
        while(len(rivi)>0):
            RivinTiedot = rivi.split(EROTIN)
            TiedotLista = OlioListaanLisays(RivinTiedot,TiedotLista)
            rivi = tiedosto.readline()
        tiedosto.close()
        print("Tiedosto","'"+TiedostoLue+"'", "luettu.")
    except FileNotFoundError:
        print("Tiedoston '" + TiedostoLue + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    return TiedotLista

def OlioListaanLisays(RivinTiedot,SahkoDataOlioLista):
    PorssiSahkoData = SAHKODATA()
    PorssiSahkoData.Aika = datetime.datetime.strptime(RivinTiedot[0],'"%Y-%m-%d %H:%M:%S"')
    PorssiSahkoData.Hinta = float(RivinTiedot[1][:-1])
    SahkoDataOlioLista.append(PorssiSahkoData)
    return SahkoDataOlioLista

def Analyysi(LuetutTiedot):
    HinnatLista=[]
    for i in range (len(LuetutTiedot)):
        HinnatLista.append(float(LuetutTiedot[i].Hinta))
    Tulokset = ANALYYSINTULOKSET()
    KalleinAika = LuetutTiedot[HinnatLista.index(max(HinnatLista))].Aika  #paivamaara jolloin sahkö kalleinta
    KalleinAika = KalleinAika.strftime("%d.%m.%Y %H:%M")
    Tulokset.Kallein = max(HinnatLista)
    Tulokset.Kalleinaika = KalleinAika
    HalvinAika = LuetutTiedot[HinnatLista.index(min(HinnatLista))].Aika  #paivamaara jolloin sahkö halvinta
    HalvinAika = HalvinAika.strftime("%d.%m.%Y %H:%M")
    Tulokset.Halvin = min(HinnatLista)
    Tulokset.Halvinaika = HalvinAika
    Tulokset.Keskihinta= sum(HinnatLista)/len(HinnatLista)
    Tulokset.Tunnit = len(HinnatLista)
    HinnatLista.clear()
    print("Tilastotietojen analyysi suoritettu", Tulokset.Tunnit, "alkiolle.")
    return Tulokset
    
def PaivaAnalyysi(LuetutTiedot,PaivaAnalyysiLista):
    SUMMA = 0
    TUNNIT = 0
    PVM = LuetutTiedot[0].Aika #alustetaan päivämäärä
    EDELLINENPAIVA = PVM.strftime("%d")
    for i in range (len(LuetutTiedot)):
        PVM = LuetutTiedot[i].Aika
        PAIVA = PVM.strftime("%d")
        if (PAIVA == EDELLINENPAIVA):
            TUNNIT += 1     #Kuinka monelta tunnilta dataa yhdeltä päivältä keskihintaa varten
            SUMMA += float(LuetutTiedot[i].Hinta)
            EDELLINENPAIVA = PAIVA
            EDELLINENPVM = PVM.strftime("%d.%m.%Y")
        else:
            if (TUNNIT == 0):
                PaivaAnalyysiLista.append(str(PVM.strftime("%d.%m.%Y")) + EROTIN + float(LuetutTiedot[i].Hinta) + "\n")
            else:
                KESKIARVO = round(float(SUMMA/TUNNIT),1)
                PaivaAnalyysiLista.append(str(EDELLINENPVM) + EROTIN + str(KESKIARVO) + "\n")
            SUMMA = 0
            SUMMA += float(LuetutTiedot[i].Hinta)
            EDELLINENPAIVA = PAIVA  
            TUNNIT = 1                 
            EDELLINENPVM = PVM.strftime("%d.%m.%Y")
    KESKIARVO = round(float(SUMMA/TUNNIT),1)                         #
    PaivaAnalyysiLista.append(str(EDELLINENPVM) + EROTIN + str(KESKIARVO))  #viimeisen paivan lisays listaan
    PaivaAnalyysiLista.insert(0,"Päivittäiset keskiarvot (Pvm;snt/kWh):\n") #otsikkorivin lisays ensimmaiseksi
    print("Päivittäiset keskiarvot laskettu", (len(PaivaAnalyysiLista)-1), "päivälle.")
    return PaivaAnalyysiLista

def AnalyysinMuotoilu(Tulokset,PaivaAnalyysiTuloksetLista,TulosteLista):
    TulosteLista.append("Analyysin tulokset " + str(Tulokset.Tunnit) + " tunnilta ovat seuraavat:\n")
    TulosteLista.append("Sähkön keskihinta oli " + str(round(Tulokset.Keskihinta,1))+" snt/kWh.\n")
    TulosteLista.append("Halvimmillaan sähkö oli " + str(Tulokset.Halvin) + " snt/kWh, " + str(Tulokset.Halvinaika) + ".\n")
    TulosteLista.append("Kalleimmillaan sähkö oli " + str(Tulokset.Kallein) + " snt/kWh, " + str(Tulokset.Kalleinaika) +".\n\n")
    TulosteLista.extend(PaivaAnalyysiTuloksetLista)
    PaivaAnalyysiTuloksetLista.clear()
    return TulosteLista

def TiedostoKirjoitus (TiedostoKirjoita,TulostettavaLista):
    try:
        tiedosto = open(TiedostoKirjoita, "w")
        for i in (range(len(TulostettavaLista))):    
            tiedosto.write(TulostettavaLista[i])
        tiedosto.close()
        print("Tiedosto '" + TiedostoKirjoita + "' kirjoitettu.")
    except FileNotFoundError:
        print("Tiedoston '" + TiedostoKirjoita + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    return TulostettavaLista

def VkpvAnalyysi(HintaAikaLista,Tulos):
    Tulos.clear()
    VkpvMaara = []
    VkpvSumma = []
    MONSUMMA = 0
    TUESUMMA = 0
    WEDSUMMA = 0
    THUSUMMA = 0
    FRISUMMA = 0
    SATSUMMA = 0
    SUNSUMMA = 0
    MONMAARA = 0
    TUEMAARA = 0
    WEDMAARA = 0
    THUMAARA = 0
    FRIMAARA = 0
    SATMAARA = 0
    SUNMAARA = 0
    Tulos.append("Viikonpäivä;Keskimääräinen hinta snt/kWh")#lisataan otsikkorivi listaan ensimmaiseksi
    Tulos.append("\nMaanantai" + EROTIN) #Lisätään viikonpäivät
    Tulos.append("Tiistai" + EROTIN)
    Tulos.append("Keskiviikko" + EROTIN)
    Tulos.append("Torstai" + EROTIN)
    Tulos.append("Perjantai" + EROTIN)
    Tulos.append("Lauantai" + EROTIN)
    Tulos.append("Sunnuntai" + EROTIN)
    for alkio in HintaAikaLista:
        VKPV = int(alkio.Aika.weekday())
        VkpvHinta = float(alkio.Hinta)
        if (VKPV == 0):
            MONSUMMA += VkpvHinta
            MONMAARA += 1  
        elif (VKPV == 1):
            TUESUMMA += VkpvHinta
            TUEMAARA += 1
        elif (VKPV == 2):
            WEDSUMMA += VkpvHinta
            WEDMAARA += 1
        elif (VKPV == 3):
            THUSUMMA += VkpvHinta
            THUMAARA += 1
        elif (VKPV == 4):
            FRISUMMA += VkpvHinta
            FRIMAARA += 1
        elif (VKPV == 5):
            SATSUMMA += VkpvHinta
            SATMAARA += 1
        elif (VKPV == 6):
            SUNSUMMA += VkpvHinta
            SUNMAARA += 1
    VkpvSumma.append(MONSUMMA)
    VkpvMaara.append(MONMAARA)
    VkpvSumma.append(TUESUMMA)
    VkpvMaara.append(TUEMAARA)
    VkpvSumma.append(WEDSUMMA)
    VkpvMaara.append(WEDMAARA)
    VkpvSumma.append(THUSUMMA)
    VkpvMaara.append(THUMAARA)
    VkpvSumma.append(FRISUMMA)
    VkpvMaara.append(FRIMAARA)
    VkpvSumma.append(SATSUMMA)
    VkpvMaara.append(SATMAARA)
    VkpvSumma.append(SUNSUMMA)
    VkpvMaara.append(SUNMAARA)
    for i in range(len(VkpvSumma)):
        if (VkpvMaara[i] == 0):
            Tulos[i+1] += (str(float(0)) + "\n")
        else:
            Tulos[i+1] += (str(round(VkpvSumma[i]/VkpvMaara[i],1)) + "\n")
    VkpvMaara.clear()
    VkpvSumma.clear()
    return Tulos


def KulutusAnalyysi(KulutusDataSanakirja,HintaAikaLista,KulutusDataTiedosto):
    KulutusDataSanakirja.clear()
    i = 0
    KulutusSumma = 0
    try: 
        tiedosto = open(KulutusDataTiedosto, "r")
        tiedosto.readline()  #otsikkorivi pois
        rivi = tiedosto.readline()
        while(len(rivi)>0):
            RivinTiedot = rivi.split(EROTIN)
            Pvm = datetime.datetime.strptime(RivinTiedot[0],"%d.%m.%Y %H:%M")
            if (Pvm in KulutusDataSanakirja):
                KulutusDataSanakirja[Pvm] += float(RivinTiedot[1]) + float(RivinTiedot[2][:-1])
            else:
                KulutusDataSanakirja[Pvm] = float(RivinTiedot[1]) + float(RivinTiedot[2][:-1])
            rivi = tiedosto.readline()
        tiedosto.close()
    except (Exception):
        print("Tiedoston '" + KulutusDataTiedosto + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    print("Tiedosto '" + KulutusDataTiedosto + "' luettu.")
    for Avain in KulutusDataSanakirja:
        if (Avain == HintaAikaLista[i].Aika):
            KulutusSumma += KulutusDataSanakirja[Avain] * HintaAikaLista[i].Hinta
        else:
            i += 1
            if (Avain != HintaAikaLista[i].Aika):
                i += -2
            KulutusSumma += KulutusDataSanakirja[Avain] * HintaAikaLista[i].Hinta
        i += 1
    KulutusSumma = round(KulutusSumma/100,2)#KulutusSumman muutto snt->Eur ja sen pyöristys
    print("Hinta- ja kulutustiedot yhdistetty. Lasku on yhteensä", KulutusSumma, "euroa.")
    return KulutusDataSanakirja

def MatriisiMuotoilu(KulutusDataSanakirja,HintaAikaLista,MatriisiTulosteLista):
    MatriisiTulosteLista.clear()
    Viikko = 0
    Tunti = 0
    Viikko = 0
    YHTSumma = 0
    SarakeSumma = 0
    RiviSumma = 0
    RIVEJA = 54
    SARAKKEITA = 24
    Matriisi = numpy.zeros((RIVEJA , SARAKKEITA), float)  #Matriisin alustus
    
    for alkio in HintaAikaLista:
        Pvm = alkio.Aika
        if Pvm not in KulutusDataSanakirja:   #kellonsiirrosta johtuvan alkion puutteen ohitus
            pass
        else:
            Avain = alkio.Aika
            Viikko = int(alkio.Aika.strftime("%W"))
            Tunti = int(alkio.Aika.hour)
            Matriisi[Viikko][Tunti] += float(alkio.Hinta)* float(KulutusDataSanakirja[Avain])

    MatriisiTulosteLista.append("Viikko\Tunti" + EROTIN)#Kirjoitettavan listan otsikkorivin muotoilu
    for i in range (24):
        MatriisiTulosteLista.append(str(i) + EROTIN)   #tunnit 0-23
    MatriisiTulosteLista.append("YHT\n")
    for Rivi in range(RIVEJA):
        MatriisiTulosteLista.append("Vko " + str(Rivi) + EROTIN)   #joka riville Vko (Viikko)
        for Sarake in range(SARAKKEITA):
            SarakeSumma += float(Matriisi[Rivi][Sarake])   #Viikon kulutuksen hinnan summa
            MatriisiTulosteLista.append(str(round(Matriisi[Rivi][Sarake],1)) + EROTIN)
        MatriisiTulosteLista.append(str(round(SarakeSumma,1)))#Viikon kulutuksen summa lisätään rivin loppuun
        MatriisiTulosteLista.append("\n")
        SarakeSumma = 0 
        
    MatriisiTulosteLista.append("YHT" + EROTIN)
    for Sarake in range(SARAKKEITA):
        for Rivi in range(RIVEJA):
            RiviSumma += float(Matriisi[Rivi][Sarake])
        MatriisiTulosteLista.append(str(round(RiviSumma,1)) + EROTIN)
        YHTSumma += RiviSumma
        RiviSumma = 0
    MatriisiTulosteLista.append(str(round(YHTSumma,1)) + "\n")
    print("Tuntikohtaiset hinnat analysoitu.")
    return MatriisiTulosteLista

#eof
