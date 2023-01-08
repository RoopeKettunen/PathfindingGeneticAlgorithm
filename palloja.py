#Kimmoisia palloja. Palloja on helppo lisätä kohdassa PALLOT.
#14.1.2022 Jouko Kettunen

import sys, pygame
import math

pygame.init()
koko = w,h = 800,800
ikkuna = pygame.display.set_mode(koko)
pygame.display.set_caption('KIMMOISIA PALLOJA')
rect = pygame.Rect(0,0,w,h)
musta = 20,20,20
puna = 250,20,20
k = 1.0 #kimmokerroin (1.0 = täysin kimmoisa)

class Pallo:

    def __init__(self,paikka,nopeus,massa):
        self.paikka = paikka
        self.nopeus = nopeus
        self.massa = massa
        self.sade = int(4.0*(math.sqrt(massa/math.pi)))

    def Paikka(self):
        return self.paikka

    def Nopeus(self):
        return self.nopeus

    def Massa(self):
        return self.massa

    def Sade(self):
        return self.sade

#PALLOT
n = 5
pallo = [0,0,0,0,0]
pallo[0] = Pallo([50,50],[0.5,0.3],100.0)
pallo[1] = Pallo([400,400],[0.4,-0.3],200.0)
pallo[2] = Pallo([200,200],[-0.4,-0.3],300.0)
pallo[3] = Pallo([250,350],[-0.1,-0.2],400.0)
pallo[4] = Pallo([600,200],[0.3,0.1],500.0)


def OnReuna(paikka,nopeus,sade):
    if paikka[0] < sade or paikka[0] > w-50:
        nopeus[0] = -nopeus[0]
    if paikka[1] < sade or paikka[1] > h-50:
        nopeus[1] = -nopeus[1]

def OnTormays(paikkaA,nopeusA,sadeA,massaA,paikkaB,nopeusB,sadeB,massaB):
    valimatka = math.sqrt((paikkaA[0]-paikkaB[0])*(paikkaA[0]-paikkaB[0]) + (paikkaA[1]-paikkaB[1])*(paikkaA[1]-paikkaB[1]))
    if (sadeA+sadeB) > valimatka:   #on törmäys
        #törmäyskulma ku
        ku = math.atan2(paikkaB[1]-paikkaA[1],paikkaB[0]-paikkaA[0])
        #nopeuskomponentit törmäyssuoran suhteen ennen törmäystä (törmäyksen suuntainen us ja kohtisuora uk)
        sku = math.sin(ku)
        cku = math.cos(ku)
        usA = nopeusA[0]*cku + nopeusA[1]*sku
        ukA = nopeusA[1]*cku - nopeusA[0]*sku
        usB = nopeusB[0]*cku + nopeusB[1]*sku
        ukB = nopeusB[1]*cku - nopeusB[0]*sku
        #törmäyssuoran kohtisuorat nopeuskomponentit (uk) eivät muutu, törmäyksen suuntaiset (us) muuttuvat, uudet vs
        vsA = (massaA*usA + massaB*usB - k*massaB*(usA-usB))/(massaA + massaB)
        vsB = (massaA*usA + massaB*usB + k*massaA*(usA-usB))/(massaA + massaB)
        #uudet nopeuskomponentit palautetaan xy-koordinatiston suuntaisiksi komponenteiksi
        sku = math.sin(-ku)
        cku = math.cos(-ku)
        nopeusA[0] = vsA*cku + ukA*sku
        nopeusA[1] = ukA*cku - vsA*sku
        nopeusB[0] = vsB*cku + ukB*sku
        nopeusB[1] = ukB*cku - vsB*sku

while 1:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.rect(ikkuna,musta,rect,0)
    for i in range(n):
        pygame.draw.circle(ikkuna,puna,pallo[i].Paikka(),pallo[i].Sade())
        OnReuna(pallo[i].Paikka(),pallo[i].Nopeus(),pallo[i].Sade())
    for i in range(n-1):
        for j in range(i+1,n):
            OnTormays(pallo[i].Paikka(),pallo[i].Nopeus(),pallo[i].Sade(),pallo[i].Massa(),pallo[j].Paikka(),pallo[j].Nopeus(),pallo[j].Sade(),pallo[j].Massa())
    for i in range(n):
        pallo[i].Paikka()[0] += pallo[i].Nopeus()[0]
        pallo[i].Paikka()[1] += pallo[i].Nopeus()[1]
    pygame.display.update()