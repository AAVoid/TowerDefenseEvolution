#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
#import pickle #Pour la sérialisation/désérialisation
from constantes import *
from random import *
import barreDeVie
import personnage
import math
import animation
import system





"""
CODE SERIALISATION ET DESERIALISATION : EXEMPLE AVEC UNE CLASSE PERSONNAGE BASIQUE

class Personne:
    def __init__(self):
        self.nom = "Test"
        self.prenom = "ABC"
        self.age = 20

fichier = open("fichier.txt", "wb")
perso = Personne()
pickler = pickle.Pickler(fichier)
pickler.dump(perso)
fichier.close()

fichier = open("fichier.txt", "rb")
depickler = pickle.Unpickler(fichier)
perso2 = depickler.load()
fichier.close()

print(perso2.nom, " ", perso2.prenom, " ", perso2.age)"""






#Renseigne sur l'état d'une case, le nombre de directions possibles depuis celle-ci et les directions en question
class Case: 
    def __init__(self): #par défaut, inutile de faire plus car la carte sera entièrement crée via un fichier
        self.nombreDirectionsPossibles = 1
        self.direction = ["i", "i", "i", "i"]
        self.nombreDestinationsTeleportation = 0 #Il faudra que la ou les directions soient à "t"
        self.tableauCoordonneesDestinationTeleportation = [] #tableau à 1 dimension
        


#Stocke les informations sur une vague durant une partie
class Vague: #par défaut, inutile de faire plus car la carte sera entièrement crée via un fichier
    def __init__(self):
        self.nombreDeMonstres = 0 #car dans chaque vague il y a un nombre différent de monstre
        self.tableauMonstres = []
        self.tempsAvantDebutVague = 0 #temps en secondes avant le début de la vague
        self.texteDebutVague = "" #message qui sera affiché avant que la vague ne commence



def creerTab2DCases(largeur, hauteur): #crée un tableau à 2 dimensions rempli de Cases
    tab = []
    for i in range(0, hauteur):
        ligne = []
        for j in range(0, largeur):
             ligne.append (Case())
        tab.append(ligne)
    return tab


def creerTabMonstres(taille): #crée un tableau à 2 dimensions rempli de Cases
    tab = []
    for i in range(0, taille):
        tab.append(personnage.Monstre())
    return tab



def creerTabVagues(taille): #crée un tableau à 1 dimension remplie de Vagues
    tab = []
    for i in range(0, taille):
        tab.append(Vague())
    return tab
        


#La carte, qui contient l'image, le tableau 2x2 de cases, les monstres et d'autres informations
class Carte:
    def __init__(self):
        self.nomAnnonceCarte = 0 #nom qui sera affiché pour annoncer la carte
        self.image = 0 #image de la carte
        self.rectImage = 0 #utilisé pour déplacer la vue (caméra)
        self.nomMusique = ""
        self.nomMusiqueBoss = ""
        self.musiqueEnLecture = False #pour savoir si la musique normale est en lecture
        self.musiqueEnLecture2 = False #pour savoir si la musique du boss est en lecture
        self.largeur = 0 #nombre de cases en largeur
        self.hauteur = 0 #nombre de cases en hauteur
        self.tableauCases = [] #Tableau  à deux dimensions de Cases
        self.vagueActuelle = 0 #ira de 0 à self.nombreDeVagues - 1
        self.nombreDeVagues = 0
        self.tableauVagues = [] #tableau à une dimension de Vagues
        self.pvRestant = 0 #nombre de point de vie restant à infliger pour terminer la partie
        self.barreDeVie = 0
        self.imageCoeur = 0 #(ici car sinon il faudrait la créer en boucle dans un boucle while : pas très optimal...)
        self.rectImageCoeur = 0 #(idem, et on a besoin du rect de l'image du coeur, car le coeur est placé en fonction de sa largeur et longueur...)
        self.imageMonstre = 0 #afficher le symbol des monstres pour afficher le nombre de monstres qu'il reste à battre dans la vague actuelle
        self.rectImageMonstre = 0 
        self.nombreViePerdrePartie = 0 #nombre de monstres qui peuvent passer la carte avant de perdre la partie
        self.tabHeros11m = [] #tableau qui contiendra les héros de type 11m placé sur la carte (VOIR DOSSIER Heros)
        self.tabHeros11p = []
        self.tabHeros1m = []
        self.tabHeros1p = []
        self.tabHeros21p = []
        self.tabHeros2m = []
        self.tabHeros2p = []
        self.tabHeros31p = []
        self.tabHeros3m = []
        self.tabHeros3p = []
        self.tabHeros41p = []
        self.tabHeros4m = []
        self.tabHeros4p = []
        self.tabHeros5A = []
        self.tabHeros5F = []
        self.choixHeros = 0 #pour savoir quel Héros qu'on place sur la carte lorsque c'est possible
        #0 : 11m; 1 : 11p; 2 : 1m; 3 : 1p; 4 : 21p; 5 : 2m; 6 : 2p; 7 : 31p; 8 : 3m; 9 : 3p;
        #10 : 41p; 11 : 4m; 12 : 4p; 13 : 5A; 14 : 5F;
        self.tabFeuillesSpriteCasesPossibles = [] #pour afficher les cases bleue aux emplacements où on peut placer un héros
        self.afficherInterfacePlacerHero = False #Si le joueur va placer un personnage (si on affiche l'interface pour sélectionner le héros à placer)
        self.chronoAfficherInterfacePlacerHero = 0 #pour eviter que le joueur puisse afficher/effacer trop vite l'interface du choix du Heros
        self.vaPlacerUnHero = False #Si le joueur va placer un personnage (sa position)
        self.imageInterfacePlacerHero = 0
        self.rectImageInterfacePlacerHero = 0
        self.chronoChangerHeros = 0
        self.imageSymbolePlacerHero = 0
        self.rectImageSymbolePlacerHero = 0
        self.imageIconeDefenseFlouz = 0
        self.rectImageIconeDefenseFlouz = 0
        self.partieEnPause = False #pour pouvoir gérer la mise en pause du jeu
        self.chronoPartieEnPause = 0 #évite que le joueur puisse mettre la partie en pause et la reprendre dans un intervalle de temps trop court
        self.imagePartieEnPause = 0 #afficher quand même un truc quand la partie est en pause
        self.sonPause = 0
        self.sonAchatHero = 0
        self.sonChoixHeroInterface = 0
        self.sonPerdreVie = 0



    #def verifierPerdu(self, fenetre): #Vérifie si le joueur n'a plus de vie
        #if(self.self.nombreViePerdrePartie == 0):
            #

    #def victoire


    def demarrerPartie(self, systeme): #Lance la partie comme il se doit
        #On annonce la carte
        self.jouerMusique()
        
        imageFont = pygame.image.load(FICHIER_IMAGE_FONT_ANNONCE).convert_alpha()
        #on charge une image de fond pour faire éventuellement un effet de fondu lors de l'affichage en
        #modifiant l'opacité de l'image
        rectImageFont = imageFont.get_rect()
        fontAnnonce = pygame.font.Font(POLICE_ANNONCE_CARTE, TAILLE_TEXTE_ANNONCE_CARTE)
        imageTexteAnnonce = fontAnnonce.render(self.nomAnnonceCarte, True, (COULEUR_ROUGE_TEXTE_ANNONCE_CARTE, COULEUR_VERTE_TEXTE_ANNONCE_CARTE, \
                                                                            COULEUR_BLEU_TEXTE_ANNONCE_CARTE))
        rectImageTexteAnnonce = imageTexteAnnonce.get_rect()
        rectImageTexteAnnonce.x = LARGEUR_FENETRE / 2 - rectImageTexteAnnonce.w / 2
        rectImageTexteAnnonce.y = HAUTEUR_FENETRE / 2 - rectImageTexteAnnonce.h / 2

        system.apparaitreImageFondu(systeme, imageFont, rectImageFont, TEMPS_FONDU_ANNONCE_CARTE)
        systeme.fenetre.blit(imageTexteAnnonce, rectImageTexteAnnonce)
        pygame.display.flip()

        system.attendreXSecondes(systeme, TEMPS_ANNONCE_CARTE)

        system.apparaitreImageFondu(systeme, self.image, self.rectImage, TEMPS_FONDU_AFFICHAGE_CARTE)
        
        self.attendreDebutVague(systeme) #on place les Héros, etc. pour la première vague
        self.afficherImage(systeme)
        self.afficherHeros(systeme, 0)
        #on joue le son d'affichage des monstres
        self.afficherMonstres(systeme, 0) #On affiche les monstre
        #on attend un peu
        system.attendreXSecondes(systeme, TEMPS_ATTENTE_DEBUT_MOUVEMENT_MONSTRES)
        continuer = True
        framerate = pygame.time.Clock()

        while continuer:
            framerate.tick(FREQUENCE_BOUCLE)
            secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000

            self.chronoPartieEnPause += secondesEcouleesDepuisLeDernierAppelDeTick
                
            # on recupere l'etat du clavier
            touches = pygame.key.get_pressed();
            if touches[K_i]:
                son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
                son.play()
                pygame.image.save(systeme.fenetre, system.determinerNomCapture(systeme))
            elif (self.chronoPartieEnPause >= TEMPS_CHANGEMENT_PAUSE and touches[K_SPACE]):
                if(self.partieEnPause):
                    self.partieEnPause = False
                    self.chronoPartieEnPause = 0
                else:
                    self.partieEnPause = True
                    self.chronoPartieEnPause = 0
                    self.sonPause.play()
                
            # On vide la pile d'evenements et on verifie certains evenements
            for event in pygame.event.get():   # parcours de la liste des evenements recus
                if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                    continuer = False      # On arrete la boucle
                    pygame.quit()

            if(self.partieEnPause): #on affiche quand même une image si la partie est en pause
                systeme.fenetre.blit(self.imagePartieEnPause, (0,0))
                pygame.display.flip()

            if(not self.partieEnPause):
                self.chronoAfficherInterfacePlacerHero += secondesEcouleesDepuisLeDernierAppelDeTick

                self.perdreVieMonstrePasser() #on fait le joueur perdre une vie si un monstre passe la carte et on supprime le monstre en question

                self.changerAfficherInterfaceHero(systeme) #pour que le joueur puisse placer des Heros
                self.afficherImage(systeme) #affichage de la carte sans les monstres
                self.retirerHero(systeme) #on peut effacer un héro si on l'a mal placé quand même...
                self.afficherHeros(systeme, 0) #on affiche les Héros si placé, mais on ne les anime pas pour l'instant
                self.afficherMonstres(systeme, secondesEcouleesDepuisLeDernierAppelDeTick)
                self.deplacerMonstres(systeme.fenetre, secondesEcouleesDepuisLeDernierAppelDeTick)
                self.invoquerHero(systeme, secondesEcouleesDepuisLeDernierAppelDeTick) #possibilité de placer des Héros
                self.herosAttaquent(systeme, secondesEcouleesDepuisLeDernierAppelDeTick)
                self.afficherBarreVieMonstres(systeme.fenetre)
                self.afficherInterfaceChoixHeros(systeme, secondesEcouleesDepuisLeDernierAppelDeTick) #pour que le joueur puisse placer des Heros
                self.afficherSymbolePlacerHero(systeme)
                self.afficherDefenseFlouz(systeme)
                self.afficherVie(systeme)
                self.afficherNombreMonstres(systeme)

                pygame.display.flip()

                #self.verifierPerdu(fenetre) #on vérifie si le joueur n'a pas perdu toutes ses vies
                self.verifierVagueFinie(systeme) #pour pouvoir passer à la vague suivante


    def synchroniserStatistiques(self, systeme): #synchronise les statistiques des héros avec celles utilisées en mémoire
        for i in range (0, len(self.tabHeros11m)):
            system.synchroStat(self.tabHeros11m[i],systeme.statistiquesHeros11m) #fonction systeme

        for i in range (0, len(self.tabHeros11p)):
            system.synchroStat(self.tabHeros11p[i],systeme.statistiquesHeros11p)

        for i in range (0, len(self.tabHeros1m)):
            system.synchroStat(self.tabHeros1m[i],systeme.statistiquesHeros1m)

        for i in range (0, len(self.tabHeros1p)):
            system.synchroStat(self.tabHeros1p[i],systeme.statistiquesHeros1p)

        for i in range (0, len(self.tabHeros21p)):
            system.synchroStat(self.tabHeros21p[i],systeme.statistiquesHeros21p)

        for i in range (0, len(self.tabHeros2m)):
            system.synchroStat(self.tabHeros2m[i],systeme.statistiquesHeros2m)

        for i in range (0, len(self.tabHeros2p)):
            system.synchroStat(self.tabHeros2p[i],systeme.statistiquesHeros2p)

        for i in range (0, len(self.tabHeros31p)):
            system.synchroStat(self.tabHeros31p[i],systeme.statistiquesHeros31p)

        for i in range (0, len(self.tabHeros3m)):
            system.synchroStat(self.tabHeros3m[i],systeme.statistiquesHeros3m)

        for i in range (0, len(self.tabHeros3p)):
            system.synchroStat(self.tabHeros3p[i],systeme.statistiquesHeros3p)

        for i in range (0, len(self.tabHeros41p)):
            system.synchroStat(self.tabHeros41p[i],systeme.statistiquesHeros41p)

        for i in range (0, len(self.tabHeros4m)):
            system.synchroStat(self.tabHeros4m[i],systeme.statistiquesHeros4m)

        for i in range (0, len(self.tabHeros4p)):
            system.synchroStat(self.tabHeros4p[i],systeme.statistiquesHeros4p)

        for i in range (0, len(self.tabHeros5A)):
            system.synchroStat(self.tabHeros5A[i],systeme.statistiquesHeros5A)

        for i in range (0, len(self.tabHeros5F)):
            system.synchroStat(self.tabHeros5F[i],systeme.statistiquesHeros5F)


    def afficherDefenseFlouz(self, systeme): #affiche les Defense Flouz possédés par le joueur en dessous de la barre de vie
        if(not self.afficherInterfacePlacerHero and not self.vaPlacerUnHero or self.afficherInterfacePlacerHero and not self.vaPlacerUnHero):
            font = pygame.font.Font(FONT_AFFICHAGE_DEFENSE_FLOUZ_CARTE, TAILLE_AFFICHAGE_DEFENSE_FLOUZ_CARTE)
            
            self.rectImageIconeDefenseFlouz.x = self.barreDeVie.rectImageCadre.x
            self.rectImageIconeDefenseFlouz.y = self.barreDeVie.rectImageCadre.y + self.barreDeVie.rectImageCadre.h + CORRECTION_Y_AFFICHAGE_DEFENSE_FLOUZ_CARTE
            imageDefenseFlouz = font.render(DEFENSE_FLOUZ + " : " + str(systeme.defenseFlouz), True, \
                                                                 (COULEUR_ROUGE_TEXTE_DEFENSE_FLOUZ, \
                                                                  COULEUR_VERTE_TEXTE_DEFENSE_FLOUZ, \
                                                                  COULEUR_BLEU_TEXTE_DEFENSE_FLOUZ))
            rectImageDefenseFlouz = imageDefenseFlouz.get_rect()
            rectImageDefenseFlouz.x = self.rectImageIconeDefenseFlouz.x + self.rectImageIconeDefenseFlouz.w + CORRECTION_X_AFFICHAGE_DEFENSE_FLOUZ
            rectImageDefenseFlouz.y = self.rectImageIconeDefenseFlouz.y

            systeme.fenetre.blit(self.imageIconeDefenseFlouz, self.rectImageIconeDefenseFlouz)
            systeme.fenetre.blit(imageDefenseFlouz, rectImageDefenseFlouz)
        
        


    def afficherVie(self, systeme): #(l'image du coeur + qu'il reste avant de perdre le niveau)
        fontVie = pygame.font.Font(POLICE_TEXTE_VIE, TAILLE_TEXTE_VIE)
        imageTexteVie = fontVie.render(str(self.nombreViePerdrePartie), True, (COULEUR_ROUGE_TEXTE_VIE, COULEUR_VERTE_TEXTE_VIE, COULEUR_BLEU_TEXTE_VIE))
        rectImageTexteVie = imageTexteVie.get_rect()
        rectImageTexteVie.x = self.rectImageCoeur.x + self.rectImageCoeur.w + CORRECTION_POS_X_TEXTE_VIE
        rectImageTexteVie.y = self.rectImageCoeur.y

        systeme.fenetre.blit(self.imageCoeur, self.rectImageCoeur)
        systeme.fenetre.blit(imageTexteVie, rectImageTexteVie)


    def afficherSymbolePlacerHero(self, systeme):
        if(not self.afficherInterfacePlacerHero and not self.vaPlacerUnHero):
            systeme.fenetre.blit(self.imageSymbolePlacerHero, self.rectImageSymbolePlacerHero)

            #on test si le joueur clic sur le symbole
            if(system.cliqueZone(self.rectImageSymbolePlacerHero.x, self.rectImageSymbolePlacerHero.y, \
                              self.rectImageSymbolePlacerHero.x + self.rectImageSymbolePlacerHero.w, \
                          self.rectImageSymbolePlacerHero.y + self.rectImageSymbolePlacerHero.h)): #on clic sur "PLACER"
                self.afficherInterfacePlacerHero = True #on effacer l'interface
                self.vaPlacerUnHero = False
                self.chronoAfficherInterfacePlacerHero = 0


    def afficherInfoHeroInterface(self, systeme, chrono):
        if(self.afficherInterfacePlacerHero and not self.vaPlacerUnHero):
            #affichage des sprites animé héros
            rect11mX = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_ORIGINE_ICONE_HEROS_INTERFACE
            rect11mY = POS_Y_ORIGINE_ICONE_HEROS_INTERFACE
            systeme.statistiquesHeros11m.feuilleSprite.afficherAnimer(systeme, (rect11mX, rect11mY), chrono)
            rect11pX = rect11mX + systeme.statistiquesHeros11m.feuilleSprite.largeurSprite
            rect11pY = rect11mY
            systeme.statistiquesHeros11p.feuilleSprite.afficherAnimer(systeme, (rect11pX, rect11pY), chrono)
            rect1mX = rect11pX + systeme.statistiquesHeros11p.feuilleSprite.largeurSprite
            rect1mY = rect11pY
            systeme.statistiquesHeros1m.feuilleSprite.afficherAnimer(systeme, (rect1mX, rect1mY), chrono)
            rect1pX = rect1mX + systeme.statistiquesHeros1m.feuilleSprite.largeurSprite
            rect1pY = rect1mY
            systeme.statistiquesHeros1p.feuilleSprite.afficherAnimer(systeme, (rect1pX, rect1pY), chrono)
            rect21pX = rect1pX + systeme.statistiquesHeros1p.feuilleSprite.largeurSprite
            rect21pY = rect1pY
            systeme.statistiquesHeros21p.feuilleSprite.afficherAnimer(systeme, (rect21pX, rect21pY), chrono)
            rect2mX = rect21pX + systeme.statistiquesHeros21p.feuilleSprite.largeurSprite
            rect2mY = rect21pY
            systeme.statistiquesHeros2m.feuilleSprite.afficherAnimer(systeme, (rect2mX, rect2mY), chrono)
            rect2pX = rect2mX + systeme.statistiquesHeros2m.feuilleSprite.largeurSprite
            rect2pY = rect2mY
            systeme.statistiquesHeros2p.feuilleSprite.afficherAnimer(systeme, (rect2pX, rect2pY), chrono)
            rect31pX = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_ORIGINE_ICONE_HEROS_INTERFACE
            rect31pY = rect2pY + systeme.statistiquesHeros2p.feuilleSprite.hauteurSprite
            systeme.statistiquesHeros31p.feuilleSprite.afficherAnimer(systeme, (rect31pX, rect31pY), chrono)
            rect3mX = rect31pX + systeme.statistiquesHeros31p.feuilleSprite.largeurSprite
            rect3mY = rect31pY
            systeme.statistiquesHeros3m.feuilleSprite.afficherAnimer(systeme, (rect3mX, rect3mY), chrono)
            rect3pX = rect3mX + systeme.statistiquesHeros3m.feuilleSprite.largeurSprite
            rect3pY = rect3mY
            systeme.statistiquesHeros3p.feuilleSprite.afficherAnimer(systeme, (rect3pX, rect3pY), chrono)
            rect41pX = rect3pX + systeme.statistiquesHeros3p.feuilleSprite.largeurSprite
            rect41pY = rect3mY
            systeme.statistiquesHeros41p.feuilleSprite.afficherAnimer(systeme, (rect41pX, rect41pY), chrono)
            rect4mX = rect41pX + systeme.statistiquesHeros41p.feuilleSprite.largeurSprite
            rect4mY = rect41pY
            systeme.statistiquesHeros4m.feuilleSprite.afficherAnimer(systeme, (rect4mX, rect4mY), chrono)
            rect4pX = rect4mX + systeme.statistiquesHeros4m.feuilleSprite.largeurSprite
            rect4pY = rect4mY
            systeme.statistiquesHeros4p.feuilleSprite.afficherAnimer(systeme, (rect4pX, rect4pY), chrono)
            rect5AX = rect4pX + systeme.statistiquesHeros4p.feuilleSprite.largeurSprite
            rect5AY = rect4pY
            systeme.statistiquesHeros5A.feuilleSprite.afficherAnimer(systeme, (rect5AX, rect5AY), chrono)
            rect5FX = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_ORIGINE_ICONE_HEROS_INTERFACE
            rect5FY = rect5AY + systeme.statistiquesHeros31p.feuilleSprite.hauteurSprite
            systeme.statistiquesHeros5F.feuilleSprite.afficherAnimer(systeme, (rect5FX, rect5FY), chrono)
            #informations héro
            font = pygame.font.Font(POLICE_AFFICHAGE_INFO_INTERFACE_HEROS, TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO)
            #--------- NOM
            imageNom = font.render(u"* Nom : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImageNom = imageNom.get_rect()
            rectImageNom.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageNom.y = POS_Y_TEXTE_NOM_HEROS_INTERFACE

            imageNom2 = font.render(NOMS_HEROS[self.choixHeros], True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageNom2 = imageNom2.get_rect()
            rectImageNom2.x = rectImageNom.x + rectImageNom.w
            rectImageNom2.y = rectImageNom.y
            #--------- NIVEAU + prix level up
            imageNiveau = font.render(u"* Niveau : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImageNiveau = imageNiveau.get_rect()
            rectImageNiveau.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageNiveau.y = rectImageNom.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imageNiveau2 = font.render(str(system.statHeroNiveau(systeme, self.choixHeros)) + \
                    " (suiv. : " + str(system.statHeroExperienceNiveauSuivant(systeme, self.choixHeros)) + SIGLE_DEFENSE_FLOUZ + ")", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageNiveau2 = imageNiveau2.get_rect()
            rectImageNiveau2.x = rectImageNiveau.x + rectImageNiveau.w
            rectImageNiveau2.y = rectImageNiveau.y
            #--------- FORCE
            imageForce = font.render(u"* Force : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImageForce = imageForce.get_rect()
            rectImageForce.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageForce.y = rectImageNiveau.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imageForce2 = font.render(str(system.statHeroForce(systeme, self.choixHeros)), True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageForce2 = imageForce2.get_rect()
            rectImageForce2.x = rectImageForce.x + rectImageForce.w
            rectImageForce2.y = rectImageForce.y
            #--------- INTELLIGENCE
            imageIntelligence = font.render(u"* Intelligence : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImageIntelligence = imageIntelligence.get_rect()
            rectImageIntelligence.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageIntelligence.y = rectImageForce.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imageIntelligence2 = font.render(str(system.statHeroIntelligence(systeme, self.choixHeros)), True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageIntelligence2 = imageIntelligence2.get_rect()
            rectImageIntelligence2.x = rectImageIntelligence.x + rectImageIntelligence.w
            rectImageIntelligence2.y = rectImageIntelligence.y
            #--------- TYPE
            if(system.statHeroType(systeme, self.choixHeros) == "p"):
                imageType = font.render(u"* Type : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
                imageType2 = font.render(u"Physique", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            elif(system.statHeroType(systeme, self.choixHeros) == "m"):
                imageType = font.render(u"* Type : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
                imageType2 = font.render(u"Magique", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            elif(system.statHeroType(systeme, self.choixHeros) == "pm"):
                imageType = font.render(u"* Type : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
                imageType2 = font.render(u"Mixte", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageType = imageType.get_rect()
            rectImageType.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageType.y = rectImageIntelligence.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO
            rectImageType2 = imageType2.get_rect()
            rectImageType2.x = rectImageType.x + rectImageType.w
            rectImageType2.y = rectImageType.y
            #--------- PORTEE
            imagePortee = font.render(u"* Portée : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImagePortee = imagePortee.get_rect()
            rectImagePortee.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImagePortee.y = rectImageType.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imagePortee2 = font.render(str(system.statHeroPortee(systeme, self.choixHeros))  + " " + NOM_PORTEE , True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImagePortee2 = imagePortee2.get_rect()
            rectImagePortee2.x = rectImagePortee.x + rectImagePortee.w
            rectImagePortee2.y = rectImagePortee.y
            #--------- VITESSE D'ATTAQUE
            imageVitesseAttaque = font.render(u"* Vitesse d'attaque : ", True, (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImageVitesseAttaque = imageVitesseAttaque.get_rect()
            rectImageVitesseAttaque.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImageVitesseAttaque.y = rectImagePortee.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imageVitesseAttaque2 = font.render(str(system.statHeroVitesseAttaque(systeme, self.choixHeros)) \
                                              + TEXTE_SECONDES_PAR_ATTAQUE, True, (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImageVitesseAttaque2 = imageVitesseAttaque2.get_rect()
            rectImageVitesseAttaque2.x = rectImageVitesseAttaque.x + rectImageVitesseAttaque.w
            rectImageVitesseAttaque2.y = rectImageVitesseAttaque.y
            #--------- PRECISION
            imagePrecision = font.render(u"* Précision : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImagePrecision = imagePrecision.get_rect()
            rectImagePrecision.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImagePrecision.y = rectImageVitesseAttaque.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imagePrecision2 = font.render(str(system.statHeroPrecision(systeme, self.choixHeros)), True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImagePrecision2 = imagePrecision2.get_rect()
            rectImagePrecision2.x = rectImagePrecision.x + rectImagePrecision.w
            rectImagePrecision2.y = rectImagePrecision.y
            #--------- POURCENTAGE COUP CRITIQUE
            imagePourcentageCoupCritique = font.render(u"* Chance coup critique : ", True, (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImagePourcentageCoupCritique = imagePourcentageCoupCritique.get_rect()
            rectImagePourcentageCoupCritique.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImagePourcentageCoupCritique.y = rectImagePrecision.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imagePourcentageCoupCritique2 = font.render(str(system.statHeroPourcentageCoupCritique(systeme, self.choixHeros)) \
                                                       + "%", True, (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImagePourcentageCoupCritique2 = imagePortee2.get_rect()
            rectImagePourcentageCoupCritique2.x = rectImagePourcentageCoupCritique.x + rectImagePourcentageCoupCritique.w
            rectImagePourcentageCoupCritique2.y = rectImagePourcentageCoupCritique.y
            #--------- PRIX DE PLACEMENT
            imagePrix = font.render(u"* Prix invoc. : ", True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE))
            rectImagePrix = imagePrix.get_rect()
            rectImagePrix.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_TEXTE_NOM_HEROS_INTERFACE
            rectImagePrix.y = rectImagePourcentageCoupCritique.y + TAILLE_POLICE_AFFICHAGE_INFO_INTERFACE_HERO

            imagePrix2 = font.render(str(system.statHeroPrixInvocation(systeme, self.choixHeros))\
                                    + SIGLE_DEFENSE_FLOUZ, True, \
                                                             (COULEUR_ROUGE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_VERTE_TEXTE_INFO_HEROS_INTERFACE2, \
                                                              COULEUR_BLEU_TEXTE_INFO_HEROS_INTERFACE2))
            rectImagePrix2 = imagePrix2.get_rect()
            rectImagePrix2.x = rectImagePrix.x + rectImagePrix.w
            rectImagePrix2.y = rectImagePrix.y
            #---------
            

            #affichage des informations
            systeme.fenetre.blit(imageNom, rectImageNom)
            systeme.fenetre.blit(imageNom2, rectImageNom2)
            systeme.fenetre.blit(imageNiveau, rectImageNiveau)
            systeme.fenetre.blit(imageNiveau2, rectImageNiveau2)
            systeme.fenetre.blit(imageForce, rectImageForce)
            systeme.fenetre.blit(imageForce2, rectImageForce2)
            systeme.fenetre.blit(imageIntelligence, rectImageIntelligence)
            systeme.fenetre.blit(imageIntelligence2, rectImageIntelligence2)
            systeme.fenetre.blit(imageType, rectImageType)
            systeme.fenetre.blit(imageType2, rectImageType2)
            systeme.fenetre.blit(imagePortee, rectImagePortee)
            systeme.fenetre.blit(imagePortee2, rectImagePortee2)
            systeme.fenetre.blit(imageVitesseAttaque, rectImageVitesseAttaque)
            systeme.fenetre.blit(imageVitesseAttaque2, rectImageVitesseAttaque2)
            systeme.fenetre.blit(imagePrecision, rectImagePrecision)
            systeme.fenetre.blit(imagePrecision2, rectImagePrecision2)
            systeme.fenetre.blit(imagePourcentageCoupCritique, rectImagePourcentageCoupCritique)
            systeme.fenetre.blit(imagePourcentageCoupCritique2, rectImagePourcentageCoupCritique2)
            systeme.fenetre.blit(imagePrix, rectImagePrix)
            systeme.fenetre.blit(imagePrix2, rectImagePrix2)

            #Comme les différents rect de placement de l'icone des héros sont déclarés ici, on va tester si on clic sur ces icones ici
            #au lieu de le faire dans la fonction afficherInterfaceChoixHeros(self, systeme, chrono)
            if(system.cliqueZone(rect11mX, rect11mY, \
                              rect11mX + systeme.statistiquesHeros11m.feuilleSprite.largeurSprite, \
                                 rect11mY + systeme.statistiquesHeros11m.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 0
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect11pX, rect11pY, \
                              rect11pX + systeme.statistiquesHeros11p.feuilleSprite.largeurSprite, \
                                 rect11pY + systeme.statistiquesHeros11p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 1
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect1mX, rect1mY, \
                              rect1mX + systeme.statistiquesHeros1m.feuilleSprite.largeurSprite, \
                                 rect1mY + systeme.statistiquesHeros1m.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 2
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect1pX, rect1pY, \
                              rect1pX + systeme.statistiquesHeros1p.feuilleSprite.largeurSprite, \
                                 rect1pY + systeme.statistiquesHeros1p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 3
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect21pX, rect21pY, \
                              rect21pX + systeme.statistiquesHeros21p.feuilleSprite.largeurSprite, \
                                 rect21pY + systeme.statistiquesHeros21p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 4
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect2mX, rect2mY, \
                              rect2mX + systeme.statistiquesHeros2m.feuilleSprite.largeurSprite, \
                                 rect2mY + systeme.statistiquesHeros2m.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 5
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect2pX, rect2pY, \
                              rect2pX + systeme.statistiquesHeros2p.feuilleSprite.largeurSprite, \
                                 rect2pY + systeme.statistiquesHeros2p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 6
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect31pX, rect31pY, \
                              rect31pX + systeme.statistiquesHeros31p.feuilleSprite.largeurSprite, \
                                 rect31pY + systeme.statistiquesHeros31p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 7
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect3mX, rect3mY, \
                              rect3mX + systeme.statistiquesHeros3m.feuilleSprite.largeurSprite, \
                                 rect3mY + systeme.statistiquesHeros3m.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 8
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect3pX, rect3pY, \
                              rect3pX + systeme.statistiquesHeros3p.feuilleSprite.largeurSprite, \
                                 rect3pY + systeme.statistiquesHeros3p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 9

                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect41pX, rect41pY, \
                              rect41pX + systeme.statistiquesHeros41p.feuilleSprite.largeurSprite, \
                                 rect41pY + systeme.statistiquesHeros41p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 10
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect4mX, rect4mY, \
                              rect4mX + systeme.statistiquesHeros4m.feuilleSprite.largeurSprite, \
                                 rect4mY + systeme.statistiquesHeros4m.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 11
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect4pX, rect4pY, \
                              rect4pX + systeme.statistiquesHeros4p.feuilleSprite.largeurSprite, \
                                 rect4pY + systeme.statistiquesHeros4p.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 12
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect5AX, rect5AY, \
                              rect5AX + systeme.statistiquesHeros5A.feuilleSprite.largeurSprite, \
                                 rect5AY + systeme.statistiquesHeros5A.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 13
                self.chronoChangerHeros = 0
            elif(system.cliqueZone(rect5FX, rect5FY, \
                              rect5FX + systeme.statistiquesHeros5F.feuilleSprite.largeurSprite, \
                                 rect5FY + systeme.statistiquesHeros5F.feuilleSprite.hauteurSprite)):
                self.sonChoixHeroInterface.play()
                self.choixHeros = 14
                self.chronoChangerHeros = 0

            
            

    def afficherInterfaceChoixHeros(self, systeme, chrono): #pour que le joueur puisse confirmer le héros qu'il choisit de placer
        if(self.afficherInterfacePlacerHero and not self.vaPlacerUnHero):
            systeme.fenetre.blit(self.imageInterfacePlacerHero, self.rectImageInterfacePlacerHero)
            self.chronoChangerHeros += chrono

            #on affiche les infos et icone héros
            self.afficherInfoHeroInterface(systeme, chrono)

            #Il est possible de procéder au clavier ou à la souris pour choisir et confirmer la placement du héros
            if(self.chronoChangerHeros >= TEMPS_ATTENTE_CHANGER_HEROS):
                #---------clavier
                touches = pygame.key.get_pressed();
                if touches[K_LEFT]:
                    self.sonChoixHeroInterface.play()
                    self.diminuerChoixHeros()
                    self.chronoChangerHeros = 0
                elif touches[K_RIGHT]:
                    self.sonChoixHeroInterface.play()
                    self.augmenterChoixHeros()
                    self.chronoChangerHeros = 0
                elif touches[K_c]: #on décide de placer le héros sélectionner
                    if(systeme.defenseFlouz >= system.statHero(systeme, self.choixHeros).prixInvocation): #on ne peut placer que si on a assez d'argent
                        self.sonChoixHeroInterface.play()
                        self.afficherInterfacePlacerHero = False #on effacer l'interface
                        self.vaPlacerUnHero = True
                        self.chronoChangerHeros = 0
                    else:
                        son = pygame.mixer.Sound(SON_ANNULE2)
                        son.play()
                if touches[K_n]: #augmenter le niveau du héros actuel
                    if(systeme.defenseFlouz >= system.statHero(systeme, self.choixHeros).experienceNiveauSuivant and \
                       system.statHero(systeme, self.choixHeros).niveau < NIVEAU_HERO_MAXIMUM):
                        self.sonChoixHeroInterface.play()
                        systeme.defenseFlouz -= system.statHero(systeme, self.choixHeros).experienceNiveauSuivant
                        self.chronoChangerHeros = 0
                        #on augmente le niveau
                        system.levelUpStat(systeme, system.statHero(systeme, self.choixHeros), self.choixHeros)
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        system.actualiserExperienceNiveauSuivant(systeme)
                        system.actualiserPrixInvocation(systeme)
                    else:
                        son = pygame.mixer.Sound(SON_ANNULE2)
                        son.play()
                #---------souris
                if(system.cliqueZone(LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MIN_CROIX_INTERFACE, POS_Y_MIN_CROIX_INTERFACE, \
                              LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MAX_CROIX_INTERFACE, POS_Y_MAX_CROIX_INTERFACE)): #on clic sur la croix
                    #on ferme l'interface
                    self.afficherInterfacePlacerHero = False #on effacer l'interface
                    self.vaPlacerUnHero = False
                    self.chronoAfficherInterfacePlacerHero = 0
                    self.chronoChangerHeros = 0
                elif(system.cliqueZone(LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MIN_PLACE, POS_Y_MIN_PLACE, \
                              LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MAX_PLACE, POS_Y_MAX_PLACE)): #on clic sur "PLACER"
                    if(systeme.defenseFlouz >= system.statHero(systeme, self.choixHeros).prixInvocation): #on ne peut placer que si on a assez d'argent
                        self.sonChoixHeroInterface.play()
                        self.afficherInterfacePlacerHero = False #on effacer l'interface
                        self.vaPlacerUnHero = True
                        self.chronoChangerHeros = 0
                    else:
                        son = pygame.mixer.Sound(SON_ANNULE2)
                        son.play()
                elif(system.cliqueZone(LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MIN_DIMINUER_CHOIX_HEROS, POS_Y_MIN_DIMINUER_CHOIX_HEROS, \
                              LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MAX_DIMINUER_CHOIX_HEROS, POS_Y_MAX_DIMINUER_CHOIX_HEROS)):
                    #on clic pour diminuer le choix Hero
                    self.sonChoixHeroInterface.play()
                    self.diminuerChoixHeros()
                    self.chronoChangerHeros = 0
                elif(system.cliqueZone(LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MIN_AUGMENTER_CHOIX_HEROS, POS_Y_MIN_AUGMENTER_CHOIX_HEROS, \
                              LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POS_X_MAX_AUGMENTER_CHOIX_HEROS, POS_Y_MAX_AUGMENTER_CHOIX_HEROS)):
                    #on clic pour augmenter le choix Hero
                    self.sonChoixHeroInterface.play()
                    self.augmenterChoixHeros()
                    self.chronoChangerHeros = 0
                if(system.cliqueZone(LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POX_X_MIN_AUGMENTER_NIVEAU, POX_Y_MIN_AUGMENTER_NIVEAU, \
                              LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w + POX_X_MAX_AUGMENTER_NIVEAU, POX_Y_MAX_AUGMENTER_NIVEAU)):
                    if(systeme.defenseFlouz >= system.statHero(systeme, self.choixHeros).experienceNiveauSuivant and \
                       system.statHero(systeme, self.choixHeros).niveau < NIVEAU_HERO_MAXIMUM):
                        systeme.defenseFlouz -= system.statHero(systeme, self.choixHeros).experienceNiveauSuivant
                        #augmenter le niveau du héro actuel
                        self.sonChoixHeroInterface.play()
                        self.chronoChangerHeros = 0
                        #on augmente le niveau
                        system.levelUpStat(systeme, system.statHero(systeme, self.choixHeros), self.choixHeros)
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        system.actualiserExperienceNiveauSuivant(systeme)
                        system.actualiserPrixInvocation(systeme)
                    else:
                        son = pygame.mixer.Sound(SON_ANNULE2)
                        son.play()
                

    #Pour que le joueur puisse choisir de placer un Héro sur la carte ou non
    def changerAfficherInterfaceHero(self, systeme):
        if(self.chronoAfficherInterfacePlacerHero >= TEMPS_ATTENTE_AFFICHER_INTERFACE_PLACER_HERO and not self.vaPlacerUnHero):
            # on recupere l'etat du clavier
                touches = pygame.key.get_pressed();
                if touches[K_p]: #Si le joueur appuie sur la touche p du clavier il valide et veut donc placer le héro sélectionné
                    if(self.afficherInterfacePlacerHero):
                        self.afficherInterfacePlacerHero = False
                        self.chronoAfficherInterfacePlacerHero = 0
                    else:
                        self.afficherInterfacePlacerHero = True
                        self.chronoAfficherInterfacePlacerHero = 0
                        
        
    def afficherNombreMonstres(self, systeme):
        fontNombreMonstres = pygame.font.Font(POLICE_TEXTE_NOMBRE_MONSTRES, TAILLE_TEXTE_NOMBRE_MONSTRES)
        imageTexteNombreMonstres = fontNombreMonstres.render(str(self.tableauVagues[self.vagueActuelle].nombreDeMonstres), True, \
                                                             (COULEUR_ROUGE_TEXTE_NOMBRE_MONSTRES, \
                                                              COULEUR_VERTE_TEXTE_NOMBRE_MONSTRES, \
                                                              COULEUR_BLEU_TEXTE_NOMBRE_MONSTRES))
        rectImageTexteNombreMonstres = imageTexteNombreMonstres.get_rect()
        rectImageTexteNombreMonstres.x = self.rectImageMonstre.x + self.rectImageMonstre.w + CORRECTION_POS_X_TEXTE_VIE
        rectImageTexteNombreMonstres.y = self.rectImageMonstre.y
        systeme.fenetre.blit(self.imageMonstre, self.rectImageMonstre)
        systeme.fenetre.blit(imageTexteNombreMonstres, rectImageTexteNombreMonstres)


    def passerVagueSuivante(self):
        self.vagueActuelle += 1
        if(self.vagueActuelle == self.nombreDeVagues): #On a gagne la partie
            return True
        else:
            return False
        

    def herosVersLeBas(self): #utilisé à la fin d'une vague, fait tous les héros regarder vers le bas
        for i in range (0, len(self.tabHeros11m)):
            self.tabHeros11m[i].feuilleSprite.changerPositionX(0)
            self.tabHeros11m[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros11p)):
            self.tabHeros11p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros11p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros1m)):
            self.tabHeros1m[i].feuilleSprite.changerPositionX(0)
            self.tabHeros1m[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros1p)):
            self.tabHeros1p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros1p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros21p)):
            self.tabHeros21p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros21p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros2m)):
            self.tabHeros2m[i].feuilleSprite.changerPositionX(0)
            self.tabHeros2m[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros2p)):
            self.tabHeros2p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros2p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros31p)):
            self.tabHeros31p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros31p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros3m)):
            self.tabHeros3m[i].feuilleSprite.changerPositionX(0)
            self.tabHeros3m[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros3p)):
            self.tabHeros3p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros3p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros41p)):
            self.tabHeros41p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros41p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros4m)):
            self.tabHeros4m[i].feuilleSprite.changerPositionX(0)
            self.tabHeros4m[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros4p)):
            self.tabHeros4p[i].feuilleSprite.changerPositionX(0)
            self.tabHeros4p[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros5A)):
            self.tabHeros5A[i].feuilleSprite.changerPositionX(0)
            self.tabHeros5A[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)

        for i in range (0, len(self.tabHeros5F)):
            self.tabHeros5F[i].feuilleSprite.changerPositionX(0)
            self.tabHeros5F[i].feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)
        

    def verifierVagueFinie(self, systeme): #Pour pouvoir passer à la vague suivante ou finir le niveau
        if (self.tableauVagues[self.vagueActuelle].tableauMonstres == []): #On a tué tous les monstres de la vague actuelle
            #on passe à la vague suivante et on gagne la partie éventuellement
            if(self.passerVagueSuivante()): #on a gagne la partie
                self.herosVersLeBas()
                #victoire
            else: #on n'a pas encore fini la partie
                self.herosVersLeBas()
                self.attendreDebutVague(systeme)
            

    def supprimerMonstreMort(self, systeme):
        for i in range(0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
            if(self.tableauVagues[self.vagueActuelle].tableauMonstres[i].pvActuels <= 0):
                #on rajoute de l'argent au joueur
                systeme.defenseFlouz += self.tableauVagues[self.vagueActuelle].tableauMonstres[i].defenseFlouz
                if(systeme.defenseFlouz > VALEUR_MAX_DEFENSE_FLOUZ):
                    systeme.defenseFlouz = VALEUR_MAX_DEFENSE_FLOUZ
                del self.tableauVagues[self.vagueActuelle].tableauMonstres[i]
                self.tableauVagues[self.vagueActuelle].nombreDeMonstres -= 1
                break


    def perdreVieMonstrePasser(self): #Si un monstre passe la carte en vie, on l'efface et on retire une vie au joueur
        for i in range(0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
            if(self.tableauVagues[self.vagueActuelle].tableauMonstres[i].posX >= (self.largeur + MARGE_MONSTRE_QUITTE_CARTE)):
                del self.tableauVagues[self.vagueActuelle].tableauMonstres[i]
                self.tableauVagues[self.vagueActuelle].nombreDeMonstres -= 1
                self.nombreViePerdrePartie -= 1
                #ON JOUE UN SON
                self.sonPerdreVie.play()
                break
            elif(self.tableauVagues[self.vagueActuelle].tableauMonstres[i].posX <= -MARGE_MONSTRE_QUITTE_CARTE):
                del self.tableauVagues[self.vagueActuelle].tableauMonstres[i]
                self.tableauVagues[self.vagueActuelle].nombreDeMonstres -= 1
                self.nombreViePerdrePartie -= 1
                #ON JOUE UN SON
                self.sonPerdreVie.play()
                break
            elif(self.tableauVagues[self.vagueActuelle].tableauMonstres[i].posY <= -MARGE_MONSTRE_QUITTE_CARTE):
                del self.tableauVagues[self.vagueActuelle].tableauMonstres[i]
                self.tableauVagues[self.vagueActuelle].nombreDeMonstres -= 1
                self.nombreViePerdrePartie -= 1
                #ON JOUE UN SON
                self.sonPerdreVie.play()
                break
            elif(self.tableauVagues[self.vagueActuelle].tableauMonstres[i].posY >= (self.hauteur + MARGE_MONSTRE_QUITTE_CARTE)):
                del self.tableauVagues[self.vagueActuelle].tableauMonstres[i]
                self.tableauVagues[self.vagueActuelle].nombreDeMonstres -= 1
                self.nombreViePerdrePartie -= 1
                #ON JOUE UN SON
                self.sonPerdreVie.play()
                break

        
    #attendre pour placer les Héros avant le début de la vague ou vérifier si on a terminé la partie
    def attendreDebutVague(self, systeme):
        self.jouerMusique() #pour pouvoir démarrer la musique de la vague du boss si necessaire
        
        framerate = pygame.time.Clock()
        continuer = True
        tempsAttente = self.tableauVagues[self.vagueActuelle].tempsAvantDebutVague
        imageHorloge = pygame.image.load(NOM_FICHIER_HORLOGE).convert_alpha()
        rectImageHorloge = imageHorloge.get_rect()
        rectImageHorloge.x = POS_X_HORLOGE
        rectImageHorloge.y = HAUTEUR_FENETRE - rectImageHorloge.h - CORRECTION_POS_Y_HORLOGE
        chrono = 0
        fontChrono = pygame.font.Font(POLICE_TEXTE_HORLOGE, TAILLE_TEXTE_HORLOGE)
        fontTexteDebutVague = pygame.font.Font(POLICE_TEXTE_DEBUT_VAGUE, TAILLE_TEXTE_DEBUT_VAGUE)
        imageTexteDebutVague = fontTexteDebutVague.render(self.tableauVagues[self.vagueActuelle].texteDebutVague, True, (COULEUR_ROUGE_TEXTE_DEBUT_VAGUE,\
                                                                                                    COULEUR_VERTE_TEXTE_DEBUT_VAGUE \
                                                                                                    ,COULEUR_BLEU_TEXTE_DEBUT_VAGUE))
        rectImageTexteDebutVague = imageTexteDebutVague.get_rect()
        rectImageTexteDebutVague.x = LARGEUR_FENETRE / 2 - rectImageTexteDebutVague.w / 2
        rectImageTexteDebutVague.y = HAUTEUR_FENETRE / 2 - rectImageTexteDebutVague.h / 2
        imageFont = pygame.image.load(NOM_FICHIER_IMAGE_FONT_DEBUT_VAGUE).convert_alpha()
        rectImageFont = imageFont.get_rect()
        rectImageFont.x = LARGEUR_FENETRE / 2 - rectImageFont.w / 2
        rectImageFont.y = HAUTEUR_FENETRE / 2 - rectImageFont.h / 2
        
        self.calculerCasesPossibles() #on calcule le nombre de cases possibles pour placer les héros
        ###chargement son explosion texte menu
        while continuer:
            # fixons le nombre max de frames / secondes
            framerate.tick(FREQUENCE_BOUCLE)
            secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000

            self.chronoAfficherInterfacePlacerHero += secondesEcouleesDepuisLeDernierAppelDeTick

            imageTexteHorloge = fontChrono.render(str(round(tempsAttente - chrono)) + TEXTE_APRES_CHRONO, True, \
                                                  (COULEUR_ROUGE_TEXTE_CHRONO,COULEUR_VERTE_TEXTE_CHRONO \
                                                             ,COULEUR_BLEU_TEXTE_CHRONO))
            rectImageTexteHorloge = imageTexteHorloge.get_rect()
            rectImageTexteHorloge.x = rectImageHorloge.x + rectImageHorloge.w + CORRECTION_POS_X_TEXTE_HORLOGE
            rectImageTexteHorloge.y = rectImageHorloge.y

            # on recupere l'etat du clavier
            touches = pygame.key.get_pressed();
            if touches[K_s]: #si on appuie sur la touche s on démarre tout de suite la partie
                chrono = tempsAttente
            elif touches[K_i]: #capture d'écran si la touche i est pressée
                son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
                son.play()
                pygame.image.save(systeme.fenetre, system.determinerNomCapture(systeme))

            # On vide la pile d'evenements et on verifie certains evenements
            for event in pygame.event.get():   # parcours de la liste des evenements recus
                if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                    continuer = False      # On arrete la boucle
                    pygame.quit()

            self.changerAfficherInterfaceHero(systeme) #pour que le joueur puisse placer des Heros
            self.afficherImage(systeme) #affichage de la carte sans les monstres
            self.retirerHero(systeme) #on peut effacer un héro si on l'a mal placé quand même...
            self.afficherHeros(systeme, 0) #on affiche les Héros si placé, mais on ne les anime pas pour l'instant
            self.invoquerHero(systeme, secondesEcouleesDepuisLeDernierAppelDeTick) #possibilité de placer des Héros
            systeme.fenetre.blit(imageHorloge, rectImageHorloge)
            systeme.fenetre.blit(imageTexteHorloge, rectImageTexteHorloge)
            self.afficherInterfaceChoixHeros(systeme, secondesEcouleesDepuisLeDernierAppelDeTick) #pour que le joueur puisse placer des Heros
            self.afficherSymbolePlacerHero(systeme)
            self.afficherDefenseFlouz(systeme)
            #affichage du texte indiquant qu'on peut démarrer de suite la vague en appuyant sur S
            if(not self.afficherInterfacePlacerHero and not self.vaPlacerUnHero):
                fontDebuterS = pygame.font.Font(FONT_AFFICHER_S_DEBUTER_VAGUE, TAILLE_POLICE_AFFICHER_S_DEBUT_VAGUE)
                imageTexteDebuterVague = fontDebuterS.render(TEXTE_DEBUTER_VAGUE_S, True, \
                                                             (COULEUR_ROUGE_TEXTE_S_DEBUTER_VAGUE, \
                                                              COULEUR_VERTE_TEXTE_S_DEBUTER_VAGUE, \
                                                              COULEUR_BLEU_TEXTE_S_DEBUTER_VAGUE))
                rectImageTexteDebuterVague = imageTexteDebuterVague.get_rect()
                rectImageTexteDebuterVague.x = self.rectImageIconeDefenseFlouz.x
                rectImageTexteDebuterVague.y = self.rectImageIconeDefenseFlouz.y + self.rectImageIconeDefenseFlouz.h
                systeme.fenetre.blit(imageTexteDebuterVague, rectImageTexteDebuterVague)

            if (chrono <= tempsAttente):
                chrono += secondesEcouleesDepuisLeDernierAppelDeTick
            else: #si le compte à rebour est terminé
                sonApparitionMonstre = pygame.mixer.Sound(SON_APPARITION_MONSTRE)
                sonExplosion = pygame.mixer.Sound(SON_EXPLOSION)
                #on reset ce qui doit être reseté
                self.afficherInterfacePlacerHero = False
                self.vaPlacerUnHero = False
                self.choixHeros = 0 
                pygame.display.flip() #pour effacer l'écran (les casesPossibles surtout) et n'afficher que la carte et les Héros
                self.afficherImage(systeme)
                self.afficherHeros(systeme, 0)
                pygame.display.flip()
                system.attendreXSecondes(systeme, TEMPS_AFFICHAGE_TEXTE_DEBUT_VAGUE)
                system.apparaitreImageFondu(systeme, imageFont, rectImageFont, 1)
                #on joue le son explosion menu
                sonExplosion.play()
                systeme.fenetre.blit(imageTexteDebutVague, rectImageTexteDebutVague)
                pygame.display.flip()
                #On attend et on passe à la fonction suivante
                system.attendreXSecondes(systeme, TEMPS_AFFICHAGE_TEXTE_DEBUT_VAGUE)
                pygame.display.flip() #pour effacer l'écran et n'afficher que la carte et les Héros
                self.afficherImage(systeme)
                self.afficherHeros(systeme, 0)
                pygame.display.flip()
                #Affichage des sceaux d'invocation
                for i in range(0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                    self.tableauVagues[self.vagueActuelle].tableauMonstres[i].spriteSceauInvocation.afficherAnimer2(systeme, 0)
                pygame.display.flip()
                system.attendreXSecondes(systeme, TEMPS_AFFICHAGE_TEXTE_DEBUT_VAGUE)
                self.afficherMonstres(systeme, 0)
                sonApparitionMonstre.play()
                pygame.display.flip()
                system.attendreXSecondes(systeme, TEMPS_AFFICHAGE_TEXTE_DEBUT_VAGUE)
                self.afficherImage(systeme)
                self.afficherHeros(systeme, 0)
                self.afficherMonstres(systeme, 0)
                pygame.display.flip()
                
                continuer = False
            
            # raffraichissement
            pygame.display.flip()


    def diminuerChoixHeros(self): #pour permettre au joueur de choisir un Héro à placer
        self.choixHeros = (self.choixHeros - 1)%NOMBRE_HEROS
        

    def augmenterChoixHeros(self): #pour permettre au joueur de choisir un Héro à placer
        self.choixHeros = (self.choixHeros + 1)%NOMBRE_HEROS
        

    def calculerCasesPossibles(self): #pour pouvoir calculer les cases bleue à afficher lorsqeu le placement de Héros est possible
        self.tabFeuillesSpriteCasesPossibles = [] #on reset (necessaire car si on place un Heros, la case n'est plus disponible par exemple)
        for i in range(0, self.hauteur):
            for j in range(0, self.largeur):
                if(self.verifierPlacer(j, i) and self.tableauCases[i][j].direction[0] == "p"): #s'il n'y a pas de Héros et qu'on peut placer à cette position
                    self.tabFeuillesSpriteCasesPossibles.append(animation.FeuilleSpriteAnimation(NOM_FICHIER_CASE_POSSIBLE, SECONDES_PAR_FRAMES_CASE_POSSIBLE\
                                                                                       ,NOMBRE_SPRITES_LARGEUR_CASE_POSSIBLE, NOMBRE_SPRITES_HAUTEUR_CASE_POSSIBLE))
                    self.tabFeuillesSpriteCasesPossibles[len(self.tabFeuillesSpriteCasesPossibles) - 1].rectImageFeuilleSprite.x = j * TAILLE_CASE
                    self.tabFeuillesSpriteCasesPossibles[len(self.tabFeuillesSpriteCasesPossibles) - 1].rectImageFeuilleSprite.y = i * TAILLE_CASE
                    
                    
    def verifierPlacer(self, posX, posY): #Permet de savoir si on peut placer son heros
        for i in range (0, len(self.tabHeros11m)):
            if(self.tabHeros11m[i].posX == posX and self.tabHeros11m[i].posY == posY):
                return False #on ne peut pas placer le personnage car la position est déjà utilisée

        for i in range (0, len(self.tabHeros11p)):
            if(self.tabHeros11p[i].posX == posX and self.tabHeros11p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros1m)):
            if(self.tabHeros1m[i].posX == posX and self.tabHeros1m[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros1p)):
            if(self.tabHeros1p[i].posX == posX and self.tabHeros1p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros21p)):
            if(self.tabHeros21p[i].posX == posX and self.tabHeros21p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros2m)):
            if(self.tabHeros2m[i].posX == posX and self.tabHeros2m[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros2p)):
            if(self.tabHeros2p[i].posX == posX and self.tabHeros2p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros31p)):
            if(self.tabHeros31p[i].posX == posX and self.tabHeros31p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros3m)):
            if(self.tabHeros3m[i].posX == posX and self.tabHeros3m[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros3p)):
            if(self.tabHeros3p[i].posX == posX and self.tabHeros3p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros41p)):
            if(self.tabHeros41p[i].posX == posX and self.tabHeros41p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros4m)):
            if(self.tabHeros4m[i].posX == posX and self.tabHeros4m[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros4p)):
            if(self.tabHeros4p[i].posX == posX and self.tabHeros4p[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros5A)):
            if(self.tabHeros5A[i].posX == posX and self.tabHeros5A[i].posY == posY):
                return False

        for i in range (0, len(self.tabHeros5F)):
            if(self.tabHeros5F[i].posX == posX and self.tabHeros5F[i].posY == posY):
                return False
        #si on arrive à ce point sans avoir fait de return alors on peut vérifier si on peut placer le héros
        #sur cette case à la base
        if(self.tableauCases[posY][posX].direction[0] == "p"):
            return True
        else:
            return False
        
        
    def invoquerHero(self, systeme, chrono): #pour placer un héros sur la carte si le joueur l'a décidé
        imageCaseSelection = pygame.image.load(NOM_FICHIER_CASE_SELECTION).convert_alpha()
        rectImageCaseSelection = imageCaseSelection.get_rect()
        (posXSouris,posYSouris) = pygame.mouse.get_pos()
        rectImageCaseSelection.x = round(posXSouris / TAILLE_CASE) * TAILLE_CASE
        rectImageCaseSelection.y = round(posYSouris / TAILLE_CASE) * TAILLE_CASE
        souris = pygame.mouse.get_pressed()

        #On verifie que le Héros veuille bien placer un Héro
        if(self.vaPlacerUnHero):
            for i in range(0, len(self.tabFeuillesSpriteCasesPossibles)): #on affiche les carrés bleue
                self.tabFeuillesSpriteCasesPossibles[i].afficherAnimer2(systeme, chrono)
            systeme.fenetre.blit(imageCaseSelection, rectImageCaseSelection) #on affiche le carre magenta de sélection

            #On indique au joueur qu'il peut encore annuler son invocation
            fontAnnuler = pygame.font.Font(FONT_ANNULER_INVOCATION, TAILLE_POLICE_ANNULER_INVOCATION)
            imageTexteDebuterVague = fontAnnuler.render(TEXTE_ANNULER_INVOCATION, True, \
                                                             (COULEUR_ROUGE_TEXTE_ANNULER_INVOCATION, \
                                                              COULEUR_VERTE_TEXTE_ANNULER_INVOCATION, \
                                                              COULEUR_BLEU_TEXTE_ANNULER_INVOCATION))
            rectImageTexteDebuterVague = imageTexteDebuterVague.get_rect()
            rectImageTexteDebuterVague.x = self.rectImageIconeDefenseFlouz.x
            rectImageTexteDebuterVague.y = self.rectImageIconeDefenseFlouz.y + self.rectImageIconeDefenseFlouz.h
            systeme.fenetre.blit(imageTexteDebuterVague, rectImageTexteDebuterVague)

            #si le joueur décide d'annuler le placement du personnage
            touches = pygame.key.get_pressed();
            if touches[K_BACKSPACE]:
                #jouer son annulation
                self.vaPlacerUnHero = False
                pygame.display.flip()
                self.afficherImage(systeme) #affichage de la carte sans les monstres
                self.retirerHero(systeme) #on peut effacer un héro si on l'a mal placé quand même...
            elif touches[K_i]: #capture d'écran si la touche i est pressée
                pygame.image.save(systeme.fenetre, system.determinerNomCapture(systeme))
            
            if(souris[0]): #si on fait un clic gauche
                (posXSouris,posYSouris) = pygame.mouse.get_pos() #on relève la position de la sourie
                #SON APPARITION HEROS
                self.sonAchatHero.play()
                if(self.verifierPlacer(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))):
                    #seulement si on peut placer le personnage
                    if(self.choixHeros == 0):
                        self.tabHeros11m.append(personnage.Hero())
                        self.tabHeros11m[len(self.tabHeros11m) - 1].chargerFichierTxt("1(1)m")
                        self.tabHeros11m[len(self.tabHeros11m) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros11m.prixInvocation
                    elif(self.choixHeros == 1):
                        self.tabHeros11p.append(personnage.Hero())
                        self.tabHeros11p[len(self.tabHeros11p) - 1].chargerFichierTxt("1(1)p")
                        self.tabHeros11p[len(self.tabHeros11p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros11p.prixInvocation
                    elif(self.choixHeros == 2):
                        self.tabHeros1m.append(personnage.Hero())
                        self.tabHeros1m[len(self.tabHeros1m) - 1].chargerFichierTxt("1m")
                        self.tabHeros1m[len(self.tabHeros1m) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros1m.prixInvocation
                    elif(self.choixHeros == 3):
                        self.tabHeros1p.append(personnage.Hero())
                        self.tabHeros1p[len(self.tabHeros1p) - 1].chargerFichierTxt("1p")
                        self.tabHeros1p[len(self.tabHeros1p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros1p.prixInvocation
                    elif(self.choixHeros == 4):
                        self.tabHeros21p.append(personnage.Hero())
                        self.tabHeros21p[len(self.tabHeros21p) - 1].chargerFichierTxt("2(1)p")
                        self.tabHeros21p[len(self.tabHeros21p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros21p.prixInvocation
                    elif(self.choixHeros == 5):
                        self.tabHeros2m.append(personnage.Hero())
                        self.tabHeros2m[len(self.tabHeros2m) - 1].chargerFichierTxt("2m")
                        self.tabHeros2m[len(self.tabHeros2m) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros2m.prixInvocation
                    elif(self.choixHeros == 6):
                        self.tabHeros2p.append(personnage.Hero())
                        self.tabHeros2p[len(self.tabHeros2p) - 1].chargerFichierTxt("2p")
                        self.tabHeros2p[len(self.tabHeros2p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros2p.prixInvocation
                    elif(self.choixHeros == 7):
                        self.tabHeros31p.append(personnage.Hero())
                        self.tabHeros31p[len(self.tabHeros31p) - 1].chargerFichierTxt("3(1)p")
                        self.tabHeros31p[len(self.tabHeros31p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros31p.prixInvocation
                    elif(self.choixHeros == 8):
                        self.tabHeros3m.append(personnage.Hero())
                        self.tabHeros3m[len(self.tabHeros3m) - 1].chargerFichierTxt("3m")
                        self.tabHeros3m[len(self.tabHeros3m) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros3m.prixInvocation
                    elif(self.choixHeros == 9):
                        self.tabHeros3p.append(personnage.Hero())
                        self.tabHeros3p[len(self.tabHeros3p) - 1].chargerFichierTxt("3p")
                        self.tabHeros3p[len(self.tabHeros3p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros3p.prixInvocation
                    elif(self.choixHeros == 10):
                        self.tabHeros41p.append(personnage.Hero())
                        self.tabHeros41p[len(self.tabHeros41p) - 1].chargerFichierTxt("4(1)p")
                        self.tabHeros41p[len(self.tabHeros41p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros41p.prixInvocation
                    elif(self.choixHeros == 11):
                        self.tabHeros4m.append(personnage.Hero())
                        self.tabHeros4m[len(self.tabHeros4m) - 1].chargerFichierTxt("4m")
                        self.tabHeros4m[len(self.tabHeros4m) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros4m.prixInvocation
                    elif(self.choixHeros == 12):
                        self.tabHeros4p.append(personnage.Hero())
                        self.tabHeros4p[len(self.tabHeros4p) - 1].chargerFichierTxt("4p")
                        self.tabHeros4p[len(self.tabHeros4p) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros4p.prixInvocation
                    elif(self.choixHeros == 13):
                        self.tabHeros5A.append(personnage.Hero())
                        self.tabHeros5A[len(self.tabHeros5A) - 1].chargerFichierTxt("5A")
                        self.tabHeros5A[len(self.tabHeros5A) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros5A.prixInvocation
                    else:
                        self.tabHeros5F.append(personnage.Hero())
                        self.tabHeros5F[len(self.tabHeros5F) - 1].chargerFichierTxt("5F")
                        self.tabHeros5F[len(self.tabHeros5F) - 1].placerCase(round(posXSouris / TAILLE_CASE), round(posYSouris / TAILLE_CASE))
                        self.calculerCasesPossibles()
                        self.vaPlacerUnHero = False
                        self.synchroniserStatistiques(systeme) #synchronisation des statistiques des héros avec celles en mémoire
                        systeme.defenseFlouz -= systeme.statistiquesHeros5F.prixInvocation
                    

    def retirerHero(self, systeme): #pour effacer un héros de la carte
        imageCaseSelection = pygame.image.load(NOM_FICHIER_CASE_SELECTION).convert_alpha()
        rectImageCaseSelection = imageCaseSelection.get_rect()
        (posXSouris,posYSouris) = pygame.mouse.get_pos()
        rectImageCaseSelection.x = round(posXSouris / TAILLE_CASE) * TAILLE_CASE
        rectImageCaseSelection.y = round(posYSouris / TAILLE_CASE) * TAILLE_CASE

        if(not self.afficherInterfacePlacerHero and not self.vaPlacerUnHero): #si l'interface d'invocation des héro n'est pas affichée et
            #qu'on ne va pas placer de héro
            systeme.fenetre.blit(imageCaseSelection, rectImageCaseSelection) #on affiche le carre magenta de sélection
            souris = pygame.mouse.get_pressed()
        
            if(souris[2]): #si on fait un clic droit
                (posXSouris,posYSouris) = pygame.mouse.get_pos() #on relève la position de la sourie
                posX = round(posXSouris / TAILLE_CASE)
                posY = round(posYSouris / TAILLE_CASE)
                #SON RETIRER HEROS
                self.sonAchatHero.play()
                #On scan tous les héros de la carte et on supprime le héro qui est à la position de la souris, il est unique
                for i in range (0, len(self.tabHeros11m)):
                    if(self.tabHeros11m[i].posX == posX and self.tabHeros11m[i].posY == posY):
                        del self.tabHeros11m[i] #on efface le héro
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros1p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True #on a efface un hero (ça permet aussi de terminer la fonction car il est alors
                                    #inutile de vérifier les autres tableaux de Héros

                for i in range (0, len(self.tabHeros11p)):
                    if(self.tabHeros11p[i].posX == posX and self.tabHeros11p[i].posY == posY):
                        del self.tabHeros11p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros11p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros1m)):
                    if(self.tabHeros1m[i].posX == posX and self.tabHeros1m[i].posY == posY):
                        del self.tabHeros1m[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros1m.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros1p)):
                    if(self.tabHeros1p[i].posX == posX and self.tabHeros1p[i].posY == posY):
                        del self.tabHeros1p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros1p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros21p)):
                    if(self.tabHeros21p[i].posX == posX and self.tabHeros21p[i].posY == posY):
                        del self.tabHeros21p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros21p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros2m)):
                    if(self.tabHeros2m[i].posX == posX and self.tabHeros2m[i].posY == posY):
                        del self.tabHeros2m[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros2m.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros2p)):
                    if(self.tabHeros2p[i].posX == posX and self.tabHeros2p[i].posY == posY):
                        del self.tabHeros2p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros2p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros31p)):
                    if(self.tabHeros31p[i].posX == posX and self.tabHeros31p[i].posY == posY):
                        del self.tabHeros31p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros31p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros3m)):
                    if(self.tabHeros3m[i].posX == posX and self.tabHeros3m[i].posY == posY):
                        del self.tabHeros3m[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros3m.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros3p)):
                    if(self.tabHeros3p[i].posX == posX and self.tabHeros3p[i].posY == posY):
                        del self.tabHeros3p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros3p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros41p)):
                    if(self.tabHeros41p[i].posX == posX and self.tabHeros41p[i].posY == posY):
                        del self.tabHeros41p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros41p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros4m)):
                    if(self.tabHeros4m[i].posX == posX and self.tabHeros4m[i].posY == posY):
                        del self.tabHeros4m[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros4m.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros4p)):
                    if(self.tabHeros4p[i].posX == posX and self.tabHeros4p[i].posY == posY):
                        del self.tabHeros4p[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros4p.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros5A)):
                    if(self.tabHeros5A[i].posX == posX and self.tabHeros5A[i].posY == posY):
                        del self.tabHeros5A[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros5A.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                for i in range (0, len(self.tabHeros5F)):
                    if(self.tabHeros5F[i].posX == posX and self.tabHeros5F[i].posY == posY):
                        del self.tabHeros5F[i]
                        #On rajoute de l'argent au joueur !
                        systeme.defenseFlouz += int((COEFFICIENT_DEFENSE_FLOUZ_RETIRER_HERO * systeme.statistiquesHeros5F.prixInvocation))
                        self.calculerCasesPossibles() #on recalcule les cases possibles
                        return True

                return False #si on arrive là c'est qu'aucun hero n'a été trouvé
            else:
                return False #on n'a pas effacé de héro car on n'a pas fait de clic droit


    def afficherImage(self, systeme): #affiche l'image de la carte
        systeme.fenetre.blit(self.image, self.rectImage)


    def jouerMusique(self): #joue la musique normale ou la musique de la vague du boss
        if(self.vagueActuelle == (self.nombreDeVagues - 1)): #si on est à la vague du boss
            if(not self.musiqueEnLecture and not self.musiqueEnLecture2): #aucune musique n'est jouée et n'a jamais été jouée
                pygame.mixer.music.load(self.nomMusiqueBoss)
                pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
                pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
                self.musiqueEnLecture = True
                self.musiqueEnLecture2 = True
            elif(self.musiqueEnLecture and not self.musiqueEnLecture2 and self.nomMusique != self.nomMusiqueBoss): #on coupe la musique normale
                #et on démarre celle du boss qui n'a jamais été jouée (la musique normale et celle du boss sont différentes)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.nomMusiqueBoss)
                pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
                pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
                self.musiqueEnLecture = True
                self.musiqueEnLecture2 = True
        else: #on n'est pas à la vague du boss
            if(not self.musiqueEnLecture):
                pygame.mixer.music.load(self.nomMusique)
                pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
                pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
                self.musiqueEnLecture = True
        

    def afficherMonstres(self, systeme, chrono):
        for i in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres): #on affiche les monstres de la vague
            self.tableauVagues[self.vagueActuelle].tableauMonstres[i].afficher(systeme, chrono)
            

    def deplacerMonstres(self, systeme, chrono):
        for i in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres): #on affiche les monstres de la vague
            self.tableauVagues[self.vagueActuelle].tableauMonstres[i].deplacer(systeme, self, chrono)


    def afficherHeros(self, systeme, chrono):
        for i in range (0, len(self.tabHeros11m)):
            self.tabHeros11m[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros11p)):
            self.tabHeros11p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros1m)):
            self.tabHeros1m[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros1p)):
            self.tabHeros1p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros21p)):
            self.tabHeros21p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros2m)):
            self.tabHeros2m[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros2p)):
            self.tabHeros2p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros31p)):
            self.tabHeros31p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros3m)):
            self.tabHeros3m[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros3p)):
            self.tabHeros3p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros41p)):
            self.tabHeros41p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros4m)):
            self.tabHeros4m[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros4p)):
            self.tabHeros4p[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros5A)):
            self.tabHeros5A[i].afficher(systeme, chrono)

        for i in range (0, len(self.tabHeros5F)):
            self.tabHeros5F[i].afficher(systeme, chrono)


    def afficherBarreVieMonstres(self, systeme): #affiche les points de degats à infliger aux monstres pour pouvoir gagner la partie
        self.actualiserBarreVie()
        self.barreDeVie.afficher(systeme)
        

    def afficherVies(self, systeme): #affiche la vie du joueur 
        rectImageCoeur = self.imageCoeur.get_rect()
        rectImageCoeur.x = POS_X_COEUR
        rectImageCoeur.y = HAUTEUR_FENETRE - rectImageCoeur.h - CORRECTION_POS_Y_COEUR
        systeme.fenetre.blit(self.imageCoeur, rectImageCoeur)


    def herosAttaquent(self, systeme, secondesEcouleesDepuisLeDernierAppelDeTick): #les Heros essayent d'attaquer les monstres à proximité
        for i in range (0, len(self.tabHeros11m)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros11m[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break #car le héro actuel du tableau a déjà attaqué un monstre, on passe au héro suivant
            self.supprimerMonstreMort(systeme) #on supprime les monstres qui perdent tous leurs points de vie au cas où il y aurait eu des morts !

        for i in range (0, len(self.tabHeros11p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros11p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme)

        for i in range (0, len(self.tabHeros1m)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros1m[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros1p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros1p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros21p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros21p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros2m)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros2m[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros2p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros2p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme)

        for i in range (0, len(self.tabHeros31p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros31p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros3m)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros3m[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros3p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros3p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros41p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros41p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme)

        for i in range (0, len(self.tabHeros4m)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros4m[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros4p)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros4p[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros5A)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros5A[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 

        for i in range (0, len(self.tabHeros5F)):
            for j in range (0, self.tableauVagues[self.vagueActuelle].nombreDeMonstres):
                if(self.tabHeros5F[i].testAttaque(self.tableauVagues[self.vagueActuelle].tableauMonstres[j], secondesEcouleesDepuisLeDernierAppelDeTick)):
                    break
            self.supprimerMonstreMort(systeme) 
        

    def actualiserBarreVie(self): #des degâts à infliger pour gagner la partie
        self.pvRestant = 0
        for i in range(0, self.nombreDeVagues):
            for j in range (0, self.tableauVagues[i].nombreDeMonstres):
                self.pvRestant += self.tableauVagues[i].tableauMonstres[j].pvActuels
        self.barreDeVie.actualiser(self.pvRestant)
                







    def chargerCarteTxt(self, nomFichier): #charge la carte depuis un fichier texte normal
        #LE NOM PASSE EN PARAMETRE SERA LE NOM DU DOSSIER DE LA CARTE PLACE DANS LE DOSSIER CARTES
        #LE FICHIER TXT DE LA CARTE AURA POUR NOM "LE_DOSSIER_DE_LA_CARTE_PLACE_DANS_LE_DOSSIER_CARTE.txt"
        #Dans ce même dossier on aura l'image de la carte et la musique normale + celle du boss
        #(.txt est l'extension du fichier de carte mais on peut la changer dans le fichier des constantes)
        #cette méthode sera utilisée jusqu'à ce que les fichiers sérialisés soient utilisables
        fichier = open(NOM_DOSSIER_CARTES + "/" + nomFichier + "/" + nomFichier + EXTENSION_FICHIER_CARTE, "r")

        lecture = fichier.readline() #nom annonce de la carte
        self.nomAnnonceCarte = str(lecture.replace('\n',""))
        lecture = fichier.readline() #le nom de l'image
        self.image = pygame.image.load(NOM_DOSSIER_CARTES + "/" + nomFichier + "/" + str(lecture.replace('\n',""))).convert()
        lecture = fichier.readline() #le nom de la musique
        self.nomMusique = str(NOM_DOSSIER_MUSIQUES + "/" + lecture.replace('\n',""))
        lecture = fichier.readline() #le nom de la musique du boss
        self.nomMusiqueBoss = str(NOM_DOSSIER_MUSIQUES + "/" + lecture.replace('\n',""))
        lecture = fichier.readline() #nombre de vie avant de perdre la partie
        self.nombreViePerdrePartie = int(lecture.replace('\n',""))
        lecture = fichier.readline() #largeur
        self.largeur = int(lecture.replace('\n',""))
        lecture = fichier.readline() #hauteur
        self.hauteur = int(lecture.replace('\n',""))
    
        self.tableauCases = creerTab2DCases(self.largeur, self.hauteur)
        for i in range (0, self.hauteur):
            for j in range (0, self.largeur):
                lecture = fichier.read(1) #On lit 5 cractères, le nombre de directions possibles et les directions
                self.tableauCases[i][j].nombreDirectionsPossibles = int(lecture)
                lecture = fichier.read(1)
                self.tableauCases[i][j].direction[0] = str(lecture)
                lecture = fichier.read(1)
                self.tableauCases[i][j].direction[1] = str(lecture)
                lecture = fichier.read(1)
                self.tableauCases[i][j].direction[2] = str(lecture)
                lecture = fichier.read(1)
                self.tableauCases[i][j].direction[3] = str(lecture)
            lecture = fichier.read(1) #uniquement là pour pouvoir aller à la ligne dans la lecture du fichier
        lecture = fichier.readline() #le nombre de vagues
        self.nombreDeVagues = int(lecture.replace('\n',""))
        self.tableauVagues = creerTabVagues(self.nombreDeVagues)
        for i in range (0, self.nombreDeVagues):
            lecture = fichier.readline() #nombre de monstres de la vague
            self.tableauVagues[i].nombreDeMonstres = int(lecture.replace('\n',""))
            self.tableauVagues[i].tableauMonstres = creerTabMonstres(self.tableauVagues[i].nombreDeMonstres)
            lecture = fichier.readline() #nombre de positions de Spawn
            nombrePositionsSpawn = (int(lecture.replace('\n',""))) #Pour la vague actuelle
            tableauPosSpawn = [] #de la vague actuelle
            for k in range(0, nombrePositionsSpawn):
                lecture = fichier.readline() #posX position de Spawn
                x = int(lecture.replace('\n',""))
                lecture = fichier.readline() #nombre de positions de Spawn
                y = int(lecture.replace('\n',""))
                tableauPosSpawn.append((x, y)) #on ajoute la position au tableau
            for j in range (0, self.tableauVagues[i].nombreDeMonstres):
                lecture = fichier.readline() #nom du monstre
                self.tableauVagues[i].tableauMonstres[j].chargerFichierTxt(NOM_DOSSIER_MONSTRES + "/" + str(lecture.replace('\n',"")) + "/" + \
                                                                        str(lecture.replace('\n',"")) + EXTENSION_FICHIER_MONSTRE)
                lecture = fichier.readline() #temps debut marche du monstre
                self.tableauVagues[i].tableauMonstres[j].tempsDebutMarche = float(lecture.replace('\n',""))
                self.pvRestant += self.tableauVagues[i].tableauMonstres[j].pvMax
                spawn = randint(0, nombrePositionsSpawn - 1)
                (posX,posY) = tableauPosSpawn[spawn]
                self.tableauVagues[i].tableauMonstres[j].placerCase(posX, posY)
                self.tableauVagues[i].tableauMonstres[j].spriteSceauInvocation.rectImageFeuilleSprite.x = \
                    (TAILLE_CASE * self.tableauVagues[i].tableauMonstres[j].posX) + TAILLE_CASE / 2 - \
                    self.tableauVagues[i].tableauMonstres[j].spriteSceauInvocation.rectImageFeuilleSprite.w / 2
                self.tableauVagues[i].tableauMonstres[j].spriteSceauInvocation.rectImageFeuilleSprite.y = \
                    (TAILLE_CASE * self.tableauVagues[i].tableauMonstres[j].posY) + TAILLE_CASE / 2 - \
                    self.tableauVagues[i].tableauMonstres[j].spriteSceauInvocation.rectImageFeuilleSprite.h / 2
            lecture = fichier.readline() #temps avant le début de la vague
            self.tableauVagues[i].tempsAvantDebutVague = int(lecture.replace('\n',""))
            lecture = fichier.readline() #Message avant le début de la vague
            self.tableauVagues[i].texteDebutVague = str(lecture.replace('\n',""))
        
        lecture = fichier.readline() #Nombre de cases sur la carte où la téléportation sera possible
        nombreTeleportations = int(lecture.replace('\n',""))
        for i in range(0, nombreTeleportations):
            lecture = fichier.readline() #Coordonnées X de la case
            x = int(lecture.replace('\n',""))
            lecture = fichier.readline() #Coordonnées Y de la case
            y = int(lecture.replace('\n',""))
            lecture = fichier.readline() #Nombre de zones accessibles depuis la case (X,Y)
            nombreDestinations = int(lecture.replace('\n',""))
            self.tableauCases[y][x].nombreDestinationsTeleportation = nombreDestinations
            for j in range(0, nombreDestinations):
                lecture = fichier.readline() #Coordonnées X de la case de destination
                x2 = int(lecture.replace('\n',""))
                lecture = fichier.readline() #Coordonnées Y de la case de destination
                y2 = int(lecture.replace('\n',""))
                self.tableauCases[y][x].tableauCoordonneesDestinationTeleportation.append((x2,y2))
        
        fichier.close()

        #l'image et le rect ne sont pas écrits dans le fichier, on les actualise
        self.rectImage = self.image.get_rect()
        self.barreDeVie = barreDeVie.BarreDeVie(self.pvRestant, self.pvRestant)
        self.imageCoeur = pygame.image.load(FICHIER_IMAGE_COEUR).convert_alpha()
        self.rectImageCoeur = self.imageCoeur.get_rect()
        self.rectImageCoeur.x = POS_X_COEUR
        self.rectImageCoeur.y = HAUTEUR_FENETRE - self.rectImageCoeur.h - CORRECTION_POS_Y_COEUR
        self.imageMonstre = pygame.image.load(FICHIER_IMAGE_SYMBOLE_MONSTRES).convert_alpha() 
        self.rectImageMonstre = self.imageMonstre.get_rect()
        self.rectImageMonstre.x = POS_X_COEUR + self.rectImageMonstre.w * 2
        self.rectImageMonstre.y = HAUTEUR_FENETRE - self.rectImageMonstre.h - CORRECTION_POS_Y_COEUR
        self.imageInterfacePlacerHero = pygame.image.load(FICHIER_IMAGE_FONT_PLACER_HEROS).convert_alpha() 
        self.rectImageInterfacePlacerHero = self.imageInterfacePlacerHero.get_rect()
        self.rectImageInterfacePlacerHero.x = LARGEUR_FENETRE - self.rectImageInterfacePlacerHero.w
        self.rectImageInterfacePlacerHero. y = 0
        self.imageSymbolePlacerHero = pygame.image.load(FICHIER_IMAGE_SYMBOLE_PLACER_HERO).convert_alpha() 
        self.rectImageSymbolePlacerHero = self.imageSymbolePlacerHero.get_rect()
        self.rectImageSymbolePlacerHero.x = LARGEUR_FENETRE - self.rectImageSymbolePlacerHero.w - CORRECTION_X_SYMBOLE_PLACEMENT_HERO
        self.rectImageSymbolePlacerHero.y = HAUTEUR_FENETRE - self.rectImageSymbolePlacerHero.h - CORRECTION_Y_SYMBOLE_PLACEMENT_HERO
        self.imageIconeDefenseFlouz = pygame.image.load(FICHIER_IMAGE_ICONE_DEFENSE_FLOUZ).convert_alpha()
        self.rectImageIconeDefenseFlouz = self.imageIconeDefenseFlouz.get_rect()
        self.imagePartieEnPause = pygame.image.load(FICHIER_IMAGE_PARTIE_EN_PAUSE).convert_alpha()
        self.sonPause = pygame.mixer.Sound(SON_MISE_EN_PAUSE)
        self.sonAchatHero = pygame.mixer.Sound(SON_ACHAT_HERO)
        self.sonChoixHeroInterface = pygame.mixer.Sound(SON_CHOIX_HERO_INTERFACE)
        self.sonPerdreVie = pygame.mixer.Sound(SON_PERDRE_VIE)

        




    """ POUR LA DESERIALISATION : NON UTILISE CAR NON FONCTIONNEL, CHARGEMENT DE LA CARTE VIA FICHIER TEXTE
    def chargerCarteCarte(self, nomFichier):
        fichier = open(nomFichier, "rb")
        depickler = pickle.Unpickler(fichier)
        self = depickler.load()
        fichier.close()
        self.image = pygame.image.load(self.nomImage).convert()
        self.rectImage = self.image.get_rect()"""

            

    """ POUR LA SERIALISATION : NON UTILISE CAR NON FONCTIONNEL, CHARGEMENT DE LA CARTE VIA FICHIER TEXTE
    def __getstate__(self): #dictionnaire des attributs à sérialiser
        #il faut que tous les attributs soit sérialisés sinon il y a des problèmes lors de l'affichage de la carte par exemple
        dict_attr = dict(self.__dict__)
        dict_attr["image"] = 0 #on enregistre à 0 car inutile d'enregistrer l'image
        dict_attr["rectImage"] = 0 #idem
        return dict_attr"""



    """ POUR LA DESERIALISATION : NON UTILISE CAR NON FONCTIONNEL, CHARGEMENT DE LA CARTE VIA FICHIER TEXTE
    def __setstate__(self, dict_attr): #Méthode appelée lors de la désérialisation de l'objet
        dict_attr = dict(self.__dict__)
        return dict_attr"""
        





###############################################################################################
#POUR LES DEVELOPPEURS : SERIALISATION/ DESERIALISATION (NON UTILISE POUR L'INSTANT
###############################################################################################



"""def txtToCarte(): #Convertit un fichier carte développeur en fichier carte sérialisé
    nomFichier = input("Nom du fichier carte developpeur : ")
    nomFichier2 = input("Nom du fichier carte serialise : ")
    fichier = open(nomFichier, "r")
    carte = Carte()

    #on crée la carte à partir du contenu du fichier
    lecture = fichier.readline() #le nom de l'image
    carte.nomImage = str(lecture.replace('\n',"")) #on ne compte pas le retour à la ligne
    lecture = fichier.readline() #largeur
    carte.largeur = int(lecture.replace('\n',""))
    lecture = fichier.readline() #hauteur
    carte.hauteur = int(lecture.replace('\n',""))
    
    carte.tableauDirections = creerTab2DCases(carte.largeur, carte.hauteur)
    for i in range (0, carte.hauteur):
        for j in range (0, carte.largeur):
            lecture = fichier.read(1) #On lit 5 cractères, le nombre de directions possibles et les directions
            carte.tableauDirections[i][j].nombreDirectionsPossibles = int(lecture)
            lecture = fichier.read(1)
            carte.tableauDirections[i][j].direction[0] = str(lecture)
            lecture = fichier.read(1)
            carte.tableauDirections[i][j].direction[1] = str(lecture)
            lecture = fichier.read(1)
            carte.tableauDirections[i][j].direction[2] = str(lecture)
            lecture = fichier.read(1)
            carte.tableauDirections[i][j].direction[3] = str(lecture)
        lecture = fichier.read(1) #uniquement là pour pouvoir aller à la ligne dans la lecture du fichier
    vague = Vague()
    lecture = fichier.readline() #le nombre de vagues
    carte.nombreDeVagues = int(lecture.replace('\n',""))
    carte.tableauVagues = creerTabVagues(carte.nombreDeVagues)
    for i in range (0, carte.nombreDeVagues):
        lecture = fichier.readline() #nombre de monstres de la vague
        carte.tableauVagues[i].nombreDeMonstres = int(lecture.replace('\n',""))
        for j in range (0, carte.tableauVagues[i].nombreDeMonstres):
            lecture = fichier.readline()
            carte.tableauVagues[i].tableauNomMonstres.append(str(lecture.replace('\n',"")))
        lecture = fichier.readline() #temps avant le début de la vague
        carte.tableauVagues[i].tempsAvantDebutVague = int(lecture.replace('\n',""))
        lecture = fichier.readline() #Message avant le début de la vague
        carte.tableauVagues[i].texteDebutVague = str(lecture.replace('\n',""))
    fichier.close()

    #on sérialise la carte crée plus haut
    fichierCarte = open(nomFichier2, "wb")
    pickler = pickle.Pickler(fichierCarte)
    pickler.dump(carte)
    fichierCarte.close()"""
   


"""def carteToTxt(): #Convertit un fichier carte sérialisé en fichier de carte développeur afin de modifier la carte puis de la resérialiser
    nomFichier = input("Nom du fichier carte serialise : ")
    nomFichier2 = input("Nom du fichier carte developpeur : ")
    fichier = open(nomFichier, "rb")
    #on désérialise la carte
    depickler = pickle.Unpickler(fichier)
    carte = depickler.load()
    fichier.close()
    fichier2 = open(nomFichier2, "w")

    #on écrit ses attributs dans le fichier développeur
    fichier2.write(str(carte.nomImage) + "\n")
    fichier2.write(str(carte.largeur) + "\n")
    fichier2.write(str(carte.hauteur) + "\n")
    
    for i in range (0, carte.hauteur):
        for j in range (0, carte.largeur):
            fichier2.write(str(carte.tableauDirections[i][j].nombreDirectionsPossibles))
            fichier2.write(str(carte.tableauDirections[i][j].direction[0]))
            fichier2.write(str(carte.tableauDirections[i][j].direction[1]))
            fichier2.write(str(carte.tableauDirections[i][j].direction[2]))
            fichier2.write(str(carte.tableauDirections[i][j].direction[3]))
        fichier2.write("\n")
    fichier2.write(str(carte.nombreDeVagues) + "\n")
    for i in range (0, carte.nombreDeVagues):
        fichier2.write(str(carte.tableauVagues[i].nombreDeMonstres) + "\n")
        for j in range (0, carte.tableauVagues[i].nombreDeMonstres):
            fichier2.write(str(carte.tableauVagues[i].tableauNomMonstres[j]) + "\n")
        fichier2.write(str(carte.tableauVagues[i].tempsAvantDebutVague) + "\n")
        fichier2.write(str(carte.tableauVagues[i].texteDebutVague) + "\n")
    fichier2.close()"""




#txtToCarte()
#carteToTxt()



###############################################################################################







###############################################################################################
#CARTE DU MONDE
###############################################################################################























