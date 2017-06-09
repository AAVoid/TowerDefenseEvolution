#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
from constantes import *
import carte
from system import *
import animation



def afficherCarteDuMonde(systeme):
    tabImages = []
    for i in range(0, AVANCEMENT_MAX_AVENTURE): #chargement des images de la carte du monde
        tabImages.append(pygame.image.load(NOM_DOSSIER_IMAGES + "/" + str(i) + ".PNG").convert())
    rectImage = tabImages[0].get_rect()
    ######### Musique
    pygame.mixer.music.load(MUSIQUE_CARTE_DU_MONDE)
    pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
    pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
    ######### Son
    son = pygame.mixer.Sound(SON_DEPLACEMENT_CARTE_DU_MONDE)
    sonEngagement = pygame.mixer.Sound(SON_ENGAGEMENT)
    
    # servira a regler l'horloge du jeu
    framerate = pygame.time.Clock()
    continuer = True
    chrono = 0 #pour le déplacement sur la carte
    chronoAnimation = 0 #pour l'animation du personnage

    c = carte.Carte() #la carte actuelle

    spritePersonnage = animation.FeuilleSpriteAnimation(IMAGE_PERSONNAGE, VITESSE_ANIMATION_PERSONNAGE_CARTE_DU_MONDE)

    apparaitreImageFondu(systeme, tabImages[systeme.positionCarteDuMonde], rectImage, TEMPS_FONDU_AFFICHAGE_CARTE_DU_MONDE)

    while continuer:
        # fixons le nombre max de frames / secondes
        framerate.tick(FREQUENCE_BOUCLE)
        secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000
        chrono += secondesEcouleesDepuisLeDernierAppelDeTick
        chronoAnimation += secondesEcouleesDepuisLeDernierAppelDeTick

        touches = pygame.key.get_pressed()
        if touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
        elif touches[K_LEFT] and chrono >= TEMPS_ATTENTE_CHANGEMENT_POSITION:
            chrono = 0
            if(systeme.positionCarteDuMonde > 0):
                systeme.positionCarteDuMonde -= 1
                son.play()

        elif touches[K_RIGHT] and chrono >= TEMPS_ATTENTE_CHANGEMENT_POSITION:
            chrono = 0
            if(systeme.positionCarteDuMonde < (systeme.avancementAventure - 1) and systeme.positionCarteDuMonde < (AVANCEMENT_MAX_AVENTURE - 1)):
                systeme.positionCarteDuMonde += 1
                son.play()

        elif touches[K_RETURN] and chrono >= TEMPS_ATTENTE_CHANGEMENT_POSITION:
            pygame.mixer.music.stop()
            sonEngagement.play()
            attendreXSecondes(systeme, TEMPS_ENGAGEMENT)
            c.chargerCarteTxt(str(systeme.positionCarteDuMonde))
            c.demarrerPartie(systeme)
            

        # On vide la pile d'evenements et on verifie certains evenements
        for event in pygame.event.get():   # parcours de la liste des evenements recus
            if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle

        systeme.fenetre.blit(tabImages[systeme.positionCarteDuMonde], rectImage)
        spritePersonnage.afficherAnimer(systeme, (LARGEUR_FENETRE / 2 - spritePersonnage.largeurSprite / 2, \
                                                        HAUTEUR_FENETRE / 2 - spritePersonnage.hauteurSprite / 2), chronoAnimation)
        chronoAnimation = 0

        # raffraichissement
        pygame.display.flip()

    # fin du programme principal...
    pygame.quit()

























