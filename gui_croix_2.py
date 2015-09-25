#-------------------------------------------------------------------------------
# Name:        5 Petits Ronds
# Purpose:      Jeu avec PyGame
#
# Author:      Patrice
#
# Created:     04/09/2015
# Copyright:   (c) ss 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, sys
from pygame.locals import *
import calculs_ronds as calc
import time


class Gui:
    """ Creation du tableau de Jeu et interface"""

    NBLIG = 20 # Damier nbre de cases
    NBCOL = 20
    COUL1 = (128,128,128) #couleurs utilisées
    COUL2 = (100,100,100)
    VERT = (0,255,0)
    ROUGE = (255,0,0)
    BLEU = (100,100,255)
    NOIR = (0,0,0)
    GRIS = (50,50,50)
    GRIS2 = (30,30,30)
    COUL_JOU = {'J1' : ROUGE, 'J2': BLEU}
    CASE = 30 # taille du coté d'une case
    TEXTES = 400 # zone de texte
    BTN_R = pygame.Rect(733,93,34,34) # boutons des parametres
    BTN_B = pygame.Rect(773,93,34,34)
    BTN_RZ = pygame.Rect(848,96,67,28)
    BTN_ORDI = pygame.Rect(698,136,78,28)

    def __init__(self):
        """ initalise le jeu et lance la boucle d'evenements """
        tabl_larg = Gui.NBLIG * Gui.CASE
        tabl_haut = Gui.NBCOL * Gui.CASE
        joueur = 'J1' # joueur humain en 1er avec les rouges
        self.ordi=False
        biblio=''
        self.fenetre = pygame.display.set_mode((tabl_larg + self.TEXTES,tabl_haut),0,32)
        pygame.display.set_caption('Petits Ronds ')
        # affichage du titre :
        self.affi_texte('Jeux des 5 Petits Ronds', 'Arial', 26,
        tabl_larg+60, 8, Gui.VERT, Gui.NOIR)
        # affichage de la grille :
        # affichage des boutons de paramètres :
        # pygame.draw.rect(fenetre,self.GRIS,self.BTN_B)
        self.affi_texte('Joueur :', 'Arial', 20,
        tabl_larg+60, 98, Gui.VERT, Gui.NOIR)
        pygame.draw.rect(self.fenetre,Gui.VERT,Gui.BTN_RZ)
        self.affi_texte('<RAZ>', 'Arial', 20,
        850, 98, Gui.VERT, Gui.GRIS2)
        pygame.draw.rect(self.fenetre,Gui.VERT,Gui.BTN_ORDI)
        self.affi_texte('<ORDI>', 'Arial', 20,
        700, 138, Gui.VERT, Gui.GRIS2)
        self.params(750,110,joueur) # affiche les ronds de départ
        self.raz()


        while True: # boucle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_o: # appuie sur la touche 'o'
                        print( 'ordi vs ordi')
                        self.ordi_vs_ordi()
                if event.type == MOUSEBUTTONUP:
                    cux,cuy = event.pos
                    if cux > tabl_larg : # zone des boutons
                        bouton_clic = self.params(cux,cuy,joueur)
                        joueur=bouton_clic # recupere le rang du joueur
                        if joueur=='J2': # humain en 2e
                            self.ordi=True
                    else:
                        jeu_clic = self.joue(cux,cuy,joueur)
                        if jeu_clic: # coup valide joué à la souris
                            self.ordi=True
            if self.ordi==True:
                self.ordi_joue(joueur)
                self.ordi=False
            pygame.display.update()


    def affi_texte(self, txt, fonte, taille, x, y, coul1, coul2):
        """ Affiche un texte """
        basicFont = pygame.font.SysFont(fonte, taille)
        titre = basicFont.render(txt,True, coul1, coul2)
        titreRect = titre.get_rect()
        titreRect.topleft = (x, y)
        self.fenetre.blit(titre,titreRect)

    def affi_cadri(self, nli=20, nco=20, taille=30):
        """ trace le quadrillage """
        pygame.draw.rect(self.fenetre,Gui.GRIS2,pygame.Rect(0,0,nli*taille,nco*taille))
        for i in range(nli + 1):
            pygame.draw.line(self.fenetre,Gui.GRIS,(i*taille,0),(i*taille,nco*taille),1)
        for j in range(nco):
            pygame.draw.line(self.fenetre,Gui.GRIS,(0,j*taille),(nli*taille,j*taille),1)

    def affi_rond(self, x, y, coul, taille,*libre):
        """ affiche les ronds ou les cercles """
        if libre: # placement libre
            pygame.draw.circle(self.fenetre, coul, (x,y), int(taille/2))
        else: # centré sur la grille :
            cx = int((x // taille)*taille + taille/2)
            cy = int((y // taille)*taille + taille/2)
            self.affi_Flocon(cx,cy)
            pygame.draw.circle(self.fenetre, coul, (cx,cy), int(taille/2)-2)

    def affi_Flocon(self,x,y):
        """ affiche les branches du flocon """

        def branche(floc):
            coul=[Gui.GRIS,Gui.ROUGE,Gui.BLEU]
            for k in range(len(floc[0])):
                i = floc[1][k]*Gui.CASE+Gui.CASE//2
                j = floc[2][k]*Gui.CASE+Gui.CASE//2
                contenu = self.biblio.mat[floc[1][k],floc[2][k]]
                pygame.draw.circle(self.fenetre, coul[contenu],(i,j), 13)

        (x,y)=self.biblio.convert(x,y)
        for k in range(4): # affiche les branches du flocon en gris
            floc=self.biblio.jeu_vide.coups[(x,y)].branches()[k]
            branche(floc)


    def params(self, x, y, joueur):
        """ gere les boutons cliqués """
        if Gui.BTN_R.collidepoint((x,y)):
            self.affi_rond(600+190,110,Gui.NOIR, 28,1)
            self.affi_rond(600+190,110,Gui.BLEU, 20,1)
            self.affi_rond(600+150,110,Gui.VERT, 28,1)
            self.affi_rond(600+150,110,Gui.ROUGE, 20,1)
            self.raz(100) # raz + pause 100
            return 'J1'
        if self.BTN_B.collidepoint((x,y)):
            self.affi_rond(600+150,110,Gui.NOIR, 28,1)
            self.affi_rond(600+150,110,Gui.ROUGE, 20,1)
            self.affi_rond(600+190,110,Gui.VERT, 28,1)
            self.affi_rond(600+190,110,Gui.BLEU, 20,1)
            self.raz(100) # raz + pause 100
            return 'J2'
        if Gui.BTN_RZ.collidepoint((x,y)):
            self.raz(100) # raz + pause 100
            return joueur
        if Gui.BTN_ORDI.collidepoint((x,y)):
            print( 'ordi vs ordi')
            self.ordi_vs_ordi()
            # self.raz(100) # raz + pause 100
            return joueur


    def raz(self,pause=100):
        """ remet le jeu à Zero """
        pygame.draw.rect(self.fenetre,Gui.VERT,Gui.BTN_RZ)
        pygame.display.update()
        if pause:
            pygame.time.delay(pause)
        self.affi_cadri() # efface la grille
        self.biblio=calc.Calcul(Gui.NBLIG,Gui.NBCOL,Gui.CASE) # réinitialise la matrice
        self.affi_texte('<RAZ>', 'Arial', 20,
        850, 98, Gui.VERT, Gui.GRIS2)
        self.affi_texte('-- G A G N E --', 'Arial', 40,
                700, 300, Gui.NOIR, Gui.NOIR)


    def joue(self, x, y, joueur,affi=True):
        """ gere le clic dans la grille """

        if self.biblio.vide(x,y,joueur) == True: # position vide
            if affi: # on n'affiche pas forcement si ordi vs ordi
                self.affi_rond(x, y, Gui.COUL_JOU[joueur], Gui.CASE)
            coords=self.biblio.fini(x,y,joueur) # test si fini (5 alignés) ?
            if coords:
                if affi:  # tire le trait
                    pygame.draw.line(self.fenetre,Gui.COUL_JOU[joueur],
                    (coords[0]*30+15,coords[1]*30+15),(coords[2]*30+15,
                    coords[3]*30+15),14)
                print('Gagné !')
                self.affi_texte('-- G A G N E --', 'Arial', 40,
                700, 300, Gui.ROUGE, Gui.NOIR)
                return 'GAGNE'
            return True
        else:
            return False # case occupée


    def ordi_joue(self,joueur,affi=True):
        """ calcul du coup de l'ordi """
        x,y=self.biblio.AI(joueur,self.biblio.mat)
        if joueur == 'J1' :
            return self.joue(x,y,'J2',affi)
        else:
            return self.joue(x,y,'J1',affi)

    def ordi_vs_ordi(self):
        """ ordi contre ordi
        stratégie J1 contre J2 """

        NB_PARTIES=20   # nbre de parties jouées
        AFFI=True        # affichage des coups

        start_time=time.time()
        print ('début de la simulation de ',NB_PARTIES,'parties')
        results={'J1':0,'J2':0}
        for i in range(NB_PARTIES):
            self.raz(0) # pas de pause en automatique
            while True:
                if self.ordi_joue('J1',AFFI)=='GAGNE':
                    results['J1']+=1
                    break
                elif self.ordi_joue('J2',AFFI)=='GAGNE':
                    results['J2']+=1
                    break
                pygame.display.update()
            # print ('GAGNE')
        print (results)
        print ('Simulation des ', NB_PARTIES, ' parties en :',
        "{:5.4f}".format(time.time() - start_time), 'secondes')



def main():
    pygame.init()
    Gui()


if __name__ == '__main__':
    main()
