# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

def prenesiPodatkeOKnjigi(url):
    #Dobis html spletne strani
    html = requests.get(url).text

    #To bo treba popraviti
    html = html.encode("latin1").decode("utf-8")

    #Pretvoris za parsanje
    html = BeautifulSoup(html, "html.parser")

    #Najdes tabelo z idjem nolist-full
    tabela = html.find("table", {"id": "nolist-full"})

    #Izpises html tabele
    #print(tabela)

    #Dobis vse vrstice v tabeli
    vrstice = tabela.findAll("tr")

    #Temu se rece slovar - ful dora zadeva
    podatki = {}

    #Python ma standardno zanko foreach
    for vrstica in vrstice:
        naziv = vrstica.find("th")
        vrednost = vrstica.find("td")
        if naziv and vrednost:
            if naziv.text == "Avtor":
                avtorji = []
                vsiAvtorji = vrednost.findAll("a")
                for avtor in vsiAvtorji:
                    avtorji.append(avtor.text.strip())
                podatki[naziv.text.lower().strip()] = avtorji
            else:
                podatki[naziv.text.lower().strip()] = vrednost.text.strip()

    return podatki

class Knjiga(object):
    def __init__(self, podatki):
        self.podatki = podatki

        #Izluscimo ime in priimek avtorja
        self.avtor = self.podatki["avtor"]

        #Najdemo naslov oziroma enotni naslov gradiva
        self.naslov = self.podatki["naslov"]
        if "enotni naslov" in self.podatki:
            self.naslov = self.podatki["enotni naslov"]

        self.vrsta = self.podatki["vrsta/vsebina"]
        self.jezik = self.podatki["jezik"]
        self.leto = self.podatki["leto"]
        self.izdaja = self.podatki["izdaja"]
        self.ISBN = self.podatki["isbn"]
        self.cobissId = self.podatki["cobiss.si-id"]

    def generirajZapis(self):
        #Predvidevamo, da podatke beremo dokler ne naletimo na besedo z malo zacetnico
        regex = r"([A-ZŠČŽ][a-zščž]+),?"
        for a in self.avtor:
            matches = re.findall(regex, a, re.UNICODE)
            #for matchNum, match in enumerate(matches):
                #print match
        return "{{navedi knjigo |title=%s}}" % (self.naslov)
