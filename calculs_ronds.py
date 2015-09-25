#-------------------------------------------------------------------------------
# Name:        Calculs pour jeux des ronds
# Purpose:
#
# Author:      Patrice Weisz
#
# Created:     06/09/2015
# Copyright:   (c) ss 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
import random as rd


class Calcul(object):
    """ bibliothèque de calcul des petits ronds """

    def __init__(self,nbli,nbcol,taille):
        self.CASE = taille
        self.NBLIG = nbli
        self.NBCOL = nbcol
        self.mat = np.zeros((self.NBLIG,self.NBCOL),dtype=np.uint8)
        self.jeu_vide = Nuage(self.mat) # flocons vides
        self.jeu_J1 = Nuage_jeu(self.jeu_vide,'1') # initialisation jeu de J1
        self.jeu_J2 = Nuage_jeu(self.jeu_vide,'2') # initialisation jeu de J2



    def convert(self,x,y):
        """ convertit la position souris en indices matrice """
        taille=30
        cx = x // taille
        cy = y // taille
        return (cx,cy)

    def vide(self,x,y,joueur):
        """ regarde si la position est vide et met la matrice mat à jour"""
        i,j = self.convert(x,y)
        if self.mat[i,j] == 0:
            if joueur == 'J1':
                self.mat[i,j] = 1 # ajoute la position joueur 1
                self.jeu_J1.liste_coups.append((i,j))
            else:
                self.mat[i,j] = 2 #joueur 2
                self.jeu_J2.liste_coups.append((i,j))
            return True
        else:
            return False

    def fini(self,x,y,joueur):
        """ cherche un seul alignement gagnant de 5 ronds """
        if joueur == 'J1':
            AL5=[1,1,1,1,1]
        else:
            AL5=[2,2,2,2,2]
        i,j = self.convert(x,y)
        for test in [self.horiz5, self.verti5, self.diago5]:
            Ga,Coord = test(i,j,AL5) # teste les lignes
            if Ga:
                return Coord
        return  False

    def horiz5(self,i,j,AL5):
        """ alignement en ligne ?"""
        ki=max(i-4,0)
        ks=min(i+5,20)
        tranch=self.mat[ki:ks,j]
        for k in range(len(tranch)-4):
            alig=[tranch[k+a] for a in range(5)]
            if alig==AL5: # 5 ronds en ligne
                return True,[ki+k,j,ki+k+4,j] # return les extrémités gagnantes
        return False,[]

    def verti5(self,i,j,AL5):
        """ alignement en colonne ?"""
        ki = max(j-4,0)
        ks = min(j+5,20)
        tranch = self.mat[i,ki:ks]
        for k in range(len(tranch)-4):
            alig = [tranch[k+a] for a in range(5)]
            if alig == AL5: # 5 ronds en colonne
                return True,[i,ki+k,i,ki+k+4] # return les extrémités gagnantes
        return False,[]


    def diago5(self,i,j,AL5):
        """ alignement en diagonale ?"""
        binf = max(min(i,j)-4,0) - min(i,j)
        bsup = min(max(i,j)+4,19) - max(i,j)
        tranch = [self.mat[i+a,j+a] for a in range(binf,bsup+1)]
        for k in range(len(tranch)-4):
            alig = [tranch[k+a] for a in range(5)]
            if alig == AL5: # 5 ronds diago descendante
                return True,[i+binf+k,j+binf+k,i+binf+k+4,j+binf+k+4]
        ddeb = -(min(i-max(i-4,0), min(j+4,19)-j))
        dfin = min(min(i+4,19)-i, j-max(j-4,0))
        tranch = [self.mat[i+a,j-a] for a in range(ddeb,dfin+1)]
        for k in range(len(tranch)-4):
            alig = [tranch[k+a] for a in range(5)]
            if alig == AL5: # 5 ronds diago montante
                return True,[i+ddeb+k,j-ddeb-k,i+ddeb+k+4,j-ddeb-k-4]
        return False,[]

    def AI(self,joueur,mat):
        """ stratégie de jeu de l'ordi """
        if joueur == 'J1': # humain ou 1er joueur
            return self.AI_J2(mat)
        elif joueur == 'J2':
            return self.AI_J2(mat)

    def AI_J1(self,mat):
        """ strategie J1 """
        # jeu_J1=nuage(mat)
        x = rd.randint(0,self.NBCOL-1)*self.CASE
        y = rd.randint(0,self.NBLIG-1)*self.CASE
        return x,y

    def AI_J2(self,mat):
        """ strategie J2 """
        # lit le nuage des flocons joués
##        x = rd.randint(0,self.NBCOL-1)*self.CASE
##        y = rd.randint(0,self.NBLIG-1)*self.CASE
##        return x,y
        return self.best_coup()
        #algo stratégie :
        #Si un Batonnet de 4 à compléter : jouer l'extrémité libre : gagné
        #Sinon
        #    Si un Batonnet adverse de 4 a une extrémité libre : blocage (car coup perdant

    def test_pattern(self,exa):
        """ examine les patterns du joueur indiqué """
        qui, pattern = exa
        if qui == 'M': # mes patterns
            jeu=self.jeu_J2
        else:
            jeu=self.jeu_J1
        if jeu.liste_coups !=[]: # si coups existants
            for cp in jeu.liste_coups:
                pat=jeu.liste_patterns[cp]
                # print(qui,pat.name)
                if pat.name == pattern: # pattern trouvée
                    coup=pat.joue()
                    # print(coup)
                    if coup not in jeu.liste_coups and coup != (-1,-1):
                        x,y=coup
                        x=x*self.CASE
                        y=y*self.CASE
                        return x,y
        return -1,-1

    def best_coup(self):
        """ choisit les meilleurs coups à jouer """

        self.regenere_patterns()
        strategie =[('M','Batonnet_4'), # coups prioritaires
                    ('A','Batonnet_4'),
                    ('M','Batonnet_3'),
                    ('A','Batonnet_3'),
                    ('M','Batonnet_2'),
                    ('A','Batonnet_2'),
                    ('M','Singleton')]
        for exa in strategie:
            coup = self.test_pattern(exa)
            if coup != (-1,-1):
                # print(coup)
                return coup # on retourne le coup gagnant ou  non perdant

        # on poursuit avec les autres coups possibles :
        liste_patterns=[pa for jo,pa in strategie]
        bests=[]
        if self.jeu_J2.liste_coups !=[]:
            for cp in self.jeu_J2.liste_coups:
                # examine les patterns associées à chaque coup joué
                pat=self.jeu_J2.liste_patterns[cp]
                if pat not in liste_patterns:
                    coup=pat.joue()
                # si pas déjà joué et candidat trouvé :
                if coup not in self.jeu_J2.liste_coups and coup != (-1,-1):
                    bests.append(coup) # coup possible
        if self.jeu_J2.liste_coups ==[] or bests==[]: # coup tiré au hasard
            case_vide=False
            while case_vide == False:
                x = rd.randint(5,self.NBCOL-5)
                y = rd.randint(5,self.NBLIG-5)
                if self.mat[x,y] == 0: # c'est une case non occupée
                    case_vide=True
            bests.append((x,y))
        x,y=bests[0]
        x=x*self.CASE
        y=y*self.CASE
        return x,y

    def regenere_patterns(self):
        """ regenere les patterns à chaque coup joué """
        if self.jeu_J1.liste_coups !=[]:
            for cp in self.jeu_J1.liste_coups:
                x,y=cp
                ok=self.jeu_J1.cherche_patterns(x,y)
                if ok is not False:
                    self.jeu_J1.liste_patterns[cp]=self.jeu_J1.cherche_patterns(x,y)
                else:
                    print('patterns  pas trouvé en', (x,y))
                    self.jeu_J1.liste_patterns[cp]='????'
        if self.jeu_J2.liste_coups !=[]:
            for cp in self.jeu_J2.liste_coups:
                x,y=cp
                ok=self.jeu_J2.cherche_patterns(x,y)
                if ok is not False:
                    self.jeu_J2.liste_patterns[cp]=self.jeu_J2.cherche_patterns(x,y)
                else:
                    print('patterns  pas trouvé en', (x,y))
                    self.jeu_J2.liste_patterns[cp]='????'
        # print(self.jeu_J1.liste_patterns)
        # print(self.jeu_J2.liste_patterns)


class Nuage_jeu(object):
    """ liste des flocons et patterns d'un joueur """

    def __init__(self,flocs,joueur):
        self.flocons_vides=flocs # on recupere tous les flocons vides
        self.liste_coups=[]
        self.liste_patterns={}
        self.joueur=joueur # code du joueur '1' ou '2'

    def cherche_patterns(self,x,y):
        """ calcule la pattern pour le nouveau coup joué"""
        p =['Batonnet_4',
            'Batonnet_3',
            'Batonnet_2',
            'Singleton']
        for pa in p: # liste des patterns
            pat=eval(pa + '(x,y,self.flocons_vides,self.joueur)')
            ok,cp = pat.est()
            if ok:
                return pat # retourne l'instance de la pattern
        return False

    def is_Singleton(self,x,y):
        # cherche dans les branches du flocon si Singleton
        # si 2 vides autour dans chaque branche
        a=Singleton(x,y,self.flocons_vides)
        a.est()
        return a,a

class Patterns(object):
    """ type de patterns jouées """

    def __init__(self,x,y,flocs,joueur):
        self.ancre = x,y
        self.flocons = flocs # flocons vides
        self.branches = flocs.coups[(x,y)].branches # branches du flocon
        self.joueur=joueur #code joueur '1' ou '2'


class Singleton(Patterns):
    """ codage de : ----O---- """

    name='Singleton'

    def joue(self): # methode qui joue le meilleur coup du Singleton
        """ retourne le plus proche voisin disponible dans la branche """
        x,y = self.ancre
        best_cp=[]
        candis=self.branches()
        for k in range(4):
            candi_v = candis[k][0] # liste des cases par branche
            if self.joueur == '2':
                coul = '1'
            else:
                coul = '2'
            if candi_v.count(coul) == 0 and candi_v.count(0) == 8:
                # compte les ronds adverses
                best_cp.append(k) # la voie est libre on stocke le num de la branche
        if best_cp !=[]: # il y a des branches libres (que des 0 ou joueur)
            rd.shuffle(best_cp)# on en prend une au hasard"
            brli=best_cp[0]
            vals=candis[brli][0] # on prend les valeurs de la branche libre
            # print(vals)
            pos_x=candis[brli][1].index(x) # renvoie la position de l'ancre
            # on regarde si le point suivant est dans la branche
            if pos_x + 1 < len(vals):
                print('singleton',x,y)
                return candis[brli][1][pos_x+1], candis[brli][2][pos_x+1]
            # on regarde si le point précédent est dans la branche
            elif pos_x > 0:
                print('singleton',x,y)
                return candis[brli][1][pos_x-1], candis[brli][2][pos_x-1]
        else:
            return -1,-1
        # sinon jouer la case avec le plus de voisins ??

    def est(self):
        """ verifie si c'est un Singleton """ # XXX voir si coup déjà joué ?
        # Singleton libre dans au moins une direction ?
        # les Singletons sont testés après les autres patterns
        patterns = ['0000X0000']
        ok = True
        for motif in patterns:
            for k in range(4):
                vals= self.branches()[k][0]
                if k == 1: # branche verticale prendre y au lieu de X pour indice
                    pos_x = self.branches()[k][2].index(self.ancre[1])
                else:
                    pos_x = self.branches()[k][1].index(self.ancre[0])
                vals[pos_x]='X'
                pat = ''.join([str(i) for i in vals])
                if motif == pat:
                    # print(pat, ' est un Singleton')
                    ok = True
                # else:
                    # print(pat, ' pas un Singleton')
        return ok,ok

class Batonnet_4(Patterns):
    """ codage des motifs de 4 ronds """

    name='Batonnet_4'
    patterns=[
    '0XXXX',
    'XXXX0',
    'XX0XX',
    'X0XXX',
    'XXX0X']

    def joue(self): # methode qui joue le meilleur coup du batonnet_4
        """ retourne l'extrémité ou le trou gagnant dans la branche """
        ok,gagne=self.est()
        if ok:
            return gagne
        else:
            return (-1,-1)

    def est(self):
        """ verifie si c'est un Batonnet_4 """
        ok = False
        pos_ind={0:0, 1:4, 2:2, 3:1, 4:3} # position des zeros gagnants
        for motif in Batonnet_4.patterns:
            pattern = motif.replace('X',self.joueur)
            for k in range(4):
                pat = ''.join([str(i) for i in self.branches()[k][0]])
                if pattern in pat: # la branche contient la pattern
                    pos = pat.index(pattern)+ pos_ind[Batonnet_4.patterns.index(motif)]
                    x,y =self.branches()[k][1][pos], self.branches()[k][2][pos]
                    print('Batonnet_4',x,y)
                    ok = True
                    return ok,(x,y)
        return ok,ok

class Batonnet_3(Patterns):
    """ codage de 3 Batonnets """

    name='Batonnet_3'
    patterns=[
    '00XXX00',
    '00XXX0',
    '0XX0X0',
    '0X0XX0',
    '0XXX00']

    def joue(self): # methode qui joue le meilleur coup du Batonnet_3
        """ retourne l'extrémité ou le trou gagnant dans la branche """
        ok,gagne=self.est()
        if ok:
            return gagne
        else:
            return (-1,-1)

    def est(self):
        """ verifie si c'est un Batonnet_3 """
        ok = False
        pos_ind={0:(1,5), 1:1, 2:3, 3:2, 4:4} # position des zeros gagnants
        for motif in Batonnet_3.patterns:
            pattern = motif.replace('X',self.joueur)
            for k in range(4):
                branch = self.branches()[k]
                pat = ''.join([str(i) for i in branch[0]])
                if pattern in pat: # la branche contient la pattern
                    extremi = pos_ind[Batonnet_3.patterns.index(motif)]

                    if type(extremi) is tuple:
                        # on choisit la meilleure extremité
                        total={}
                        for extr in extremi: # on prend les 2 extremités pour choisir
                            total[extr]=0
                            pos = pat.index(pattern) + extr # position de l'extremité
                            xe,ye = branch[1][pos], branch[2][pos] # coord des extremites
                            floc_extr=self.flocons.coups[(xe,ye)].branches
                            for kk in range(4):
                                branch_extr = floc_extr()[kk]
                                total[extr] += branch_extr[0].count(eval(self.joueur))
                        if total[extremi[0]] > total[extremi[1]]:
                            extremi = extremi[0] # prend le plus grand total de meme couleur
                        else:
                            extremi = extremi[1]

                    pos = pat.index(pattern) + extremi
                    x,y =branch[1][pos], branch[2][pos]
                    print('Batonnet_3',x,y)
                    ok = True
                    return ok,(x,y)
        return ok,ok

class Batonnet_2(Patterns):
    """ codage de 2 Batonnets """

    name='Batonnet_2'
    patterns=[
    '00X0X00',
    '00XX000',
    '000XX00']

    def joue(self): # methode qui joue le meilleur coup du Batonnet_3
        """ retourne l'extrémité ou le trou gagnant dans la branche """
        ok,gagne=self.est()
        if ok:
            return gagne
        else:
            return (-1,-1)

    def est(self):
        """ verifie si c'est un Batonnet_2 """
        ok = False
        pos_ind={0:3, 1:4, 2:2} # position des zeros gagnants
        for motif in Batonnet_2.patterns:
            pattern = motif.replace('X',self.joueur)
            for k in range(4):
                pat = ''.join([str(i) for i in self.branches()[k][0]])
                if pattern in pat: # la branche contient la pattern
                    pos = pat.index(pattern)+ pos_ind[Batonnet_2.patterns.index(motif)]
                    x,y =self.branches()[k][1][pos], self.branches()[k][2][pos]
                    ok = True
                    print('Batonnet_2',x,y)
                    return ok,(x,y)
        return ok,ok

class Nuage(object):
    """liste de tous les flocons de la grille
        Nuage.coups[(x,y)] contient le Flocon en x,y """

    def __init__(self,mat):
        coups={}
        for x in range(mat.shape[0]):
            for y in range(mat.shape[1]):
                coups[(x,y)]=Flocons(x,y,mat) #init des flocons
        self.coups=coups

class Flocons(object):
    """ codage des coups possibles à partir d'une position
        Algo de génération des flocons pour toute la grille
        Flocons.coord[x,y] centre du flocon
        Flocons.branches  branches du flocon """

    mat = [] # variable de class

    def __init__(self,x,y,matr):
        Flocons.mat=matr # matrice des ronds
        self.coord=np.array([x,y],dtype=np.uint8) # coord de la case en numpy

        def _horiz():
            """ coups en ligne ?"""
            i,j=self.coord[0],self.coord[1]
            ki=max(i-4,0)
            ks=min(i+5,20)
            val=Flocons.mat[ki:ks,j].tolist()
            ii=[i for i in range(ki,ks)]
            jj=[j]*(ks-ki)
            return [val,ii,jj]

        def _verti():
            """ coups en colonne """
            i,j=self.coord[0],self.coord[1]
            ki = max(j-4,0)
            ks = min(j+5,20)
            val = Flocons.mat[i,ki:ks].tolist()
            jj=[j for j in range(ki,ks)]
            ii=[i]*(ks-ki)
            return [val,ii,jj]

        def _diagog():
            """ alignement en diagonale gauche """
            i,j=self.coord[0],self.coord[1]
            binf = max(min(i,j)-4,0) - min(i,j)
            bsup = min(max(i,j)+4,19) - max(i,j)
            val = [Flocons.mat[i+a,j+a] for a in range(binf,bsup+1)]
            ii=[a for a in range(i+binf,i+bsup+1)]
            jj=[a for a in range(j+binf,j+bsup+1)]
            return [val,ii,jj]

        def _diagod():
            """ alignement en diagonale droite """
            i,j=self.coord[0],self.coord[1]
            binf = -(min(i-max(i-4,0), min(j+4,19)-j))
            bsup = min(min(i+4,19)-i, j-max(j-4,0))
            val = [Flocons.mat[i+a,j-a] for a in range(binf,bsup+1)]
            ii=[a for a in range(i+binf,i+bsup+1)]
            jj=[a for a in range(j-binf,j-bsup-1,-1)]
            return [val,ii,jj]

        def branches():
            """ calcul des branches du flocon """
            return [_horiz(),_verti(),_diagog(),_diagod()]

        self.branches=branches # reference le nom de la fonction





def main():
    Calcul()

if __name__ == '__main__':
    main()
