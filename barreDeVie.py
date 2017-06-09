#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
from constantes import *




class BarreDeVie:
    def __init__(self, pvAct = PV_PAR_DEFAUT, pvMax = PV_MAX_PAR_DEFAUT):
        self.pvActuels = pvAct
        self.pvMaximum = pvMax
            
        self.font = pygame.font.Font(FONT_TEXTE_BARRE_DE_VIE, TAILLE_POLICE_TEXTE_BARRE_DE_VIE)
        self.imageCadre = pygame.image.load(IMAGE_CADRE_BARRE_DE_VIE).convert()
        #on affiche le cadre de la barre de vie (son contour) pour l'esthétique et ensuite la barre elle-même
        #on va travailler avec la barre, le cadre sera inchangé
        self.rectImageCadre = self.imageCadre.get_rect()
        self.rectImageCadre.x = (LARGEUR_FENETRE / 2) - (self.rectImageCadre.w / 2)
        self.rectImageCadre.y = POSITION_Y_CADRE_BARRE_DE_VIE
        self.i = 0 #Pour pouvoir changer la couleur de la barre, 0 : barre normale, 1 : barre moyenne, 2 : barre danger
        #peu importe la valeur ici puisqu'elle sera modifiée pendant l'actualisation de la barre
        self.imageBarre = []
        self.imageBarre.append(pygame.image.load(IMAGE_BARRE_DE_VIE_NORMAL).convert())
        self.imageBarre.append(pygame.image.load(IMAGE_BARRE_DE_VIE_MOYEN).convert())
        self.imageBarre.append(pygame.image.load(IMAGE_BARRE_DE_VIE_DANGER).convert())
        self.rectImageBarre = self.imageBarre[0].get_rect()
        self.rectImageBarre.x = self.rectImageCadre.x
        self.rectImageBarre.y = self.rectImageCadre.y
        #on indique la couleur de transparence : le magenta ici
        #pour l'image du cadre de la barre et les barres elles-même
        self.imageCadre.set_colorkey((COULEUR_TRANSPARENCE_ROUGE,COULEUR_TRANSPARENCE_VERT,COULEUR_TRANSPARENCE_BLEU), RLEACCEL)
        self.imageBarre[0].set_colorkey((COULEUR_TRANSPARENCE_ROUGE,COULEUR_TRANSPARENCE_VERT,COULEUR_TRANSPARENCE_BLEU), RLEACCEL)
        self.imageBarre[1].set_colorkey((COULEUR_TRANSPARENCE_ROUGE,COULEUR_TRANSPARENCE_VERT,COULEUR_TRANSPARENCE_BLEU), RLEACCEL)
        self.imageBarre[2].set_colorkey((COULEUR_TRANSPARENCE_ROUGE,COULEUR_TRANSPARENCE_VERT,COULEUR_TRANSPARENCE_BLEU), RLEACCEL)
        self.imageTexte = self.font.render("{} / {}".format(self.pvActuels, self.pvMaximum), True, (COULEUR_ROUGE_TEXTE_BARRE_DE_VIE, \
                                            COULEUR_VERT_TEXTE_BARRE_DE_VIE, COULEUR_BLEU_TEXTE_BARRE_DE_VIE))
        self.rectImageTexte = self.imageTexte.get_rect() #on place le texte au centre de la barre
        self.rectImageTexte.x = ((self.rectImageBarre.x + self.rectImageBarre.w) / 2) - (self.rectImageTexte.w / 2) #On place le texte au centre de la barre
        self.rectImageTexte.y = ((self.rectImageBarre.y + self.rectImageBarre.h) / 2) - (TAILLE_POLICE_TEXTE_BARRE_DE_VIE / 2 - CORRECTION_PIXEL)

    def actualiser(self, pvAct):
        if (pvAct <= self.pvMaximum and pvAct >= 0):
            self.pvActuels = pvAct
            
        self.imageTexte = self.font.render("{} / {}".format(self.pvActuels, self.pvMaximum), True, (COULEUR_ROUGE_TEXTE_BARRE_DE_VIE, \
                                            COULEUR_VERT_TEXTE_BARRE_DE_VIE, COULEUR_BLEU_TEXTE_BARRE_DE_VIE))
        self.rectImageTexte = self.imageTexte.get_rect()
        self.rectImageTexte.x = ((self.rectImageCadre.x + self.rectImageCadre.w) / 2) - (self.rectImageTexte.w / 2) #On place le texte au centre de la barre
        self.rectImageTexte.y = ((self.rectImageCadre.y + self.rectImageCadre.h) / 2) - (TAILLE_POLICE_TEXTE_BARRE_DE_VIE / 2 - CORRECTION_PIXEL)

        #on modifie l'apparence de la barre en fonction des points de vie
        if (self.pvActuels <= (POURCENTAGE_BARRE_DANGER / 100) * self.pvMaximum):
            self.i = 2
        elif (self.pvActuels <= (POURCENTAGE_BARRE_MOYEN / 100) * self.pvMaximum):
            self.i = 1
        else:
            self.i = 0

    def afficher(self, fenetre):
        sousSurface = pygame.Rect(0, 0, (self.pvActuels / self.pvMaximum) * self.rectImageBarre.w ,self.rectImageBarre.h)
        fenetre.blit(self.imageCadre, self.rectImageCadre)
        fenetre.blit(self.imageBarre[self.i].subsurface(sousSurface), self.rectImageBarre)
        fenetre.blit(self.imageTexte, self.rectImageTexte)
            




"""
pygame.init()
fenetre = pygame.display.set_mode((640,480))
    
imageFont = pygame.image.load(""image.PNG"").convert()
rectImageFont = imageFont.get_rect()

pygame.mixer.music.load(""musique.ogg"")
pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé

barreDeVie = BarreDeVie()

# servira a regler l'horloge du jeu
framerate = pygame.time.Clock()
continuer=1

while continuer:
    # fixons le nombre max de frames / secondes
    framerate.tick(30)

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    if touches[K_LEFT]:
        barreDeVie.actualiser(barreDeVie.pvActuels - 1)

    elif touches[K_RIGHT]:
        barreDeVie.actualiser(barreDeVie.pvActuels + 1)

    # On vide la pile d'evenements et on verifie certains evenements
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0      # On arrete la boucle
            
    # Affichage du fond
    fenetre.blit(imageFont, rectImageFont)

    barreDeVie.afficher(fenetre)

    # raffraichissement
    pygame.display.flip()

# fin du programme principal...
pygame.quit()
"""
















