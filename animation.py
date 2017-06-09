#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
from constantes import *




class FeuilleSpriteAnimation:
    def __init__(self, nomFichierImage, vitesseAnim = VITESSE_ANIMATION_PAR_DEFAUT, nbSpriteLargeur = NOMBRE_SPRITE_LARGEUR_PAR_DEFAUT, \
                 nbSpriteHauteur = NOMBRE_SPRITE_HAUTEUR_PAR_DEFAUT):
        self.imageFeuilleSprite = pygame.image.load(nomFichierImage).convert_alpha() #on ne va afficher qu'une partie de la feuille en fonction de l'animation
        self.rectImageFeuilleSprite = self.imageFeuilleSprite.get_rect()
        
        self.nombreSpriteLargeur = nbSpriteLargeur
        self.nombreSpriteHauteur = nbSpriteHauteur

        self.hauteurSprite = self.rectImageFeuilleSprite.h / self.nombreSpriteHauteur
        self.largeurSprite = self.rectImageFeuilleSprite.w / self.nombreSpriteLargeur
        
        #les positions iront de 0 à nbSpriteLargeur - 1 ou nbSpriteHauteur - 1
        self.positionXFeuilleSprite = 0 #on se place sur la frame tout en haut à gauche
        self.positionYFeuilleSprite = 0 #servira Par exemple à obtenir la "direction" d'un personnage par exemple ; 0 : Bas , 1 : Gauche , 2 : Droite , 3 : Haut

        self.vitesseAnimation = vitesseAnim #temps en secondes entre chaque frame de l'animation
        self.animer = True #pour savoir si on anime le sprite ou pas
        self.chrono = 0 #(en secondes)

    def afficherAnimer(self, systeme, rect, chrono): #(chrono est le nombre de secondes passées depuis le dernier appel de framerate.get_time())
        #on choisi la frame à afficher
        sousSurface = pygame.Rect(self.positionXFeuilleSprite * (self.rectImageFeuilleSprite.w / self.nombreSpriteLargeur), \
                                  self.positionYFeuilleSprite * (self.rectImageFeuilleSprite.h / self.nombreSpriteHauteur), \
                                  self.rectImageFeuilleSprite.w / self.nombreSpriteLargeur, \
                                  self.rectImageFeuilleSprite.h / self.nombreSpriteHauteur)
        if(self.animer):
            self.chrono += chrono
        if(self.animer and self.chrono >= self.vitesseAnimation): 
            #si on anime et que le temps entre une frame et l'autre est passé on passe à la frame suivante
            self.positionXFeuilleSprite = (self.positionXFeuilleSprite + 1) % self.nombreSpriteLargeur
            self.chrono = 0
        
        systeme.fenetre.blit(self.imageFeuilleSprite.subsurface(sousSurface), rect)

    def afficherAnimer2(self, systeme, chrono): #affiche au rect de l'image même (voir rect des attributs de la classe)
        #on choisi la frame à afficher
        sousSurface = pygame.Rect(self.positionXFeuilleSprite * (self.rectImageFeuilleSprite.w / self.nombreSpriteLargeur), \
                                  self.positionYFeuilleSprite * (self.rectImageFeuilleSprite.h / self.nombreSpriteHauteur), \
                                  self.rectImageFeuilleSprite.w / self.nombreSpriteLargeur, \
                                  self.rectImageFeuilleSprite.h / self.nombreSpriteHauteur)
        if(self.animer):
            self.chrono += chrono
        if(self.animer and self.chrono >= self.vitesseAnimation): 
            #si on anime et que le temps entre une frame et l'autre est passé on passe à la frame suivante
            self.positionXFeuilleSprite = (self.positionXFeuilleSprite + 1) % self.nombreSpriteLargeur
            self.chrono = 0
        
        systeme.fenetre.blit(self.imageFeuilleSprite.subsurface(sousSurface), (self.rectImageFeuilleSprite.x, self.rectImageFeuilleSprite.y))

    def demarrerAnimation(self):
        self.animer = True
        
    def arreterAnimation(self):
        self.animer = False
        self.positionXFeuilleSprite = 0

    def changerPositionX(self, valeurPos): #sera utilisé pour changer la position d'un personnage
        if(valeurPos >= 0 and valeurPos < self.nombreSpriteLargeur):
            self.positionXFeuilleSprite = valeurPos

    def changerPositionY(self, valeurPos): #sera utilisé pour changer la position d'un personnage
        if(valeurPos >= 0 and valeurPos < self.nombreSpriteHauteur):
            self.positionYFeuilleSprite = valeurPos



"""
pygame.init()
fenetre = pygame.display.set_mode((640,480))

feuille = FeuilleSpriteAnimation(""8.png"")
posX = 0
posY = 0

image = pygame.image.load(""image.png"").convert() #on ne va afficher qu'une partie de la feuille en fonction de l'animation
rectImage = image.get_rect()
    
# servira a regler l'horloge du jeu
framerate = pygame.time.Clock()
continuer=1

while continuer:
    # fixons le nombre max de frames / secondes
    framerate.tick(20)

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    if touches[K_LEFT]:
        posX = posX - 5
        feuille.changerPositionY(1)

    elif touches[K_RIGHT]:
        posX = posX + 5
        feuille.changerPositionY(2)

    elif touches[K_DOWN]:
        posY = posY + 5
        feuille.changerPositionY(0)

    elif touches[K_UP]:
        posY = posY - 5
        feuille.changerPositionY(3)

    elif touches[K_RETURN]:
        if(feuille.animer == 1):
            feuille.arreterAnimation()
        else:
            feuille.demarrerAnimation()

    fenetre.blit(image, rectImage)
    feuille.afficherAnimer(fenetre, (posX,posY), framerate.get_time() / 1000)
    #get_time() renvoit un temps en millisecondes, on le converti en secondes
    #car la vitesse de l'animation est en secondes

    # On vide la pile d'evenements et on verifie certains evenements
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0      # On arrete la boucle

    # raffraichissement
    pygame.display.flip()

# fin du programme principal...
pygame.quit()
"""
















