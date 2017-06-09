#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
from constantes import *
import math
import animation
from personnage import *



#CE FICHIER CONTIENDRA LES FONCTIONS SYSTEMES DU JEU, EN DESSOUS LA CLASSE QUI PERMETTRA DE GERER LA FENETRE ET ENSUITE
#CELLE QUI PERMETTRA DE GERER DIVERSES CHOSES COMME LA SAUVEGARDE DU JEU OU AUTRE



def attendreXSecondes(systeme, secondes): #met le programme en pause pendant X secondes, durant la pause on peut
#uniquement fermer la fenêtre ou prendre une capture d'écran avec la touche i du clavier
    framerate = pygame.time.Clock()
    continuer = True
    chrono = 0
    while continuer:
        framerate.tick(FREQUENCE_BOUCLE)
        secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000
        if (chrono <= secondes):
            chrono += secondesEcouleesDepuisLeDernierAppelDeTick
        else:
            continuer = False

        touches = pygame.key.get_pressed();
        if touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
                
        for event in pygame.event.get():   # parcours de la liste des evenements recus
            if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()


#permet de savoir si on a fait un clic gauche alors que la souris était dans une zone précise délimitée par un rectangle :
#permettra de savoir si on clic sur un bouton par exemple
def cliqueZone(xMin, yMin, xMax, yMax): #renvoie True si on a cliqué dans la zone et False sinon
    souris = pygame.mouse.get_pressed()
    if(souris[0]): #si on fait un clic gauche
        (posXSouris,posYSouris) = pygame.mouse.get_pos()
        if(posXSouris >= xMin and posXSouris <= xMax and posYSouris >= yMin and posYSouris <= yMax):
            return True
        else:
            return False

        
def apparaitreImageFondu(systeme, image, rectImage, dureeFondu): #l'image apparait en fondu, l'apparition dure dureeFondu secondes
    framerate = pygame.time.Clock()
    continuer = True
    chrono = dureeFondu
    while continuer:
        framerate.tick(FREQUENCE_BOUCLE)
        secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000

        systeme.fenetre.blit(image, rectImage)
        systeme.fenetre.fill((round(chrono/dureeFondu*255),round(chrono/dureeFondu*255),round(chrono/dureeFondu*255)), \
                             (rectImage.x, rectImage.y, rectImage.w, rectImage.h),BLEND_RGB_SUB)
        pygame.display.flip()
        
        if (chrono > 0):
            chrono -= secondesEcouleesDepuisLeDernierAppelDeTick
            if(chrono < 0):
                chrono = 0
        else:
            continuer = False

        touches = pygame.key.get_pressed();
        if touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
                
        for event in pygame.event.get():   # parcours de la liste des evenements recus
            if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()
        
        
    
def disparaitreImageFondu(systeme, image, rectImage, dureeFondu): #l'image disparait en fondu, on suppose que l'image qu'on fait disparaitre
#a été affichée auparavant ; la disparition dure dureeFondu secondes
    framerate = pygame.time.Clock()
    continuer = True
    chrono = 0
    while continuer:
        framerate.tick(FREQUENCE_BOUCLE)
        secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000

        systeme.fenetre.blit(image, rectImage)
        systeme.fenetre.fill((round(chrono/dureeFondu*255),round(chrono/dureeFondu*255),round(chrono/dureeFondu*255)), \
                             (rectImage.x, rectImage.y, rectImage.w, rectImage.h),BLEND_RGB_SUB)
        pygame.display.flip()
        
        if (chrono < dureeFondu):
            chrono += secondesEcouleesDepuisLeDernierAppelDeTick
            if(chrono > dureeFondu):
                chrono = dureeFondu
        else:
            continuer = False

        touches = pygame.key.get_pressed();
        if touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
                
        for event in pygame.event.get():   # parcours de la liste des evenements recus
            if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()


#Dans le cas où le joueur prendrait une capture d'écran avec la touche i du clavier, cette fonction
#détermine le nom de cette capture d'écran à partir du nombre de captures déjà prises écrit dans le
#fichier info.txt du dossier Capture d'écran
def determinerNomCapture(systeme):
    #systeme.nombreCaptures contient le numéro de la prochaine capture d'écran = nombre de captures
    #effectuées jusqu'à maintenant
    nom = NOM_DOSSIER_CAPTURE_D_ECRAN + "/" + NOM_CAPTURE + str(systeme.nombreCaptures) + EXTENSION_FICHIER_CAPTURE
    #on incrémente le nombre de captures
    systeme.nombreCaptures += 1
    #on met à jour le fichier info
    fichierInfo = open (NOM_FICHIER_INFO, "w")
    fichierInfo.write(str(systeme.nombreCaptures))
    fichierInfo.close()
    #on renvoie le nom de la nouvelle capture
    return nom
    


            


class Systeme(): #fenetre de jeu + sauvegarde + autres choses liées au système
    def __init__(self):
        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE,HAUTEUR_FENETRE)) #la fenêtre
        pygame.display.set_icon(pygame.image.load(ICONE_JEU)) #On change l'icone de la fenêtre
        pygame.display.set_caption(NOM_JEU) #On change le nom de la fenêtre
        #self.posXVue = 0 #permettra de "déplacer la vue de la fenêtre"
        #self.posYVue = 0

        self.nombreCaptures = 0 #aidera à déterminer le numéro du screen (son nom) lors d'une capture
        #nombreCaptures contient le nombre de captures effectuées jusqu'à maintenant mais aussi le numéro
        #de la prochaine capture d'écran
        #On lit le nombre de screens pris dans le fichier info du dossier de captures
        fichierInfo = open (NOM_FICHIER_INFO, "r")
        lecture = fichierInfo.readline() #nombre de screen pris jusqu'à maintenant
        self.nombreCaptures = int(lecture.replace('\n',""))
        fichierInfo.close()

        #Pour la sauvegarde et autres variables systemes (dont statistiques des héros durant le jeu)
        #ce sont ces statistiques qui seront sauvegardées
        self.defenseFlouz = 0 #argent du joueur
        self.positionCarteDuMonde = 0 #la numéro de la position actuelle du joueur sur la carte du monde
        self.avancementAventure = 0 #va déterminer la position maximale que le joueur peut atteindre sur la carte du monde
        
        self.statistiquesHeros11m = 0 #statistiques du héros X qui sont utilisées dans l'interface invocation, la partie et sauvegarde pour le héro concerné
        self.statistiquesHeros11p = 0
        self.statistiquesHeros1m = 0
        self.statistiquesHeros1p = 0
        self.statistiquesHeros21p = 0
        self.statistiquesHeros2m = 0
        self.statistiquesHeros2p = 0
        self.statistiquesHeros31p = 0
        self.statistiquesHeros3m = 0
        self.statistiquesHeros3p = 0
        self.statistiquesHeros41p = 0
        self.statistiquesHeros4m = 0
        self.statistiquesHeros4p = 0
        self.statistiquesHeros5A = 0
        self.statistiquesHeros5F = 0


    def chargerStatistiquesTxt(self): #charge les statistiques des Heros en mémoire
        self.statistiquesHeros11m = StatistiquesHero()
        self.statistiquesHeros11m.chargerFichierTxt("1(1)m")
        self.statistiquesHeros11p = StatistiquesHero()
        self.statistiquesHeros11p.chargerFichierTxt("1(1)p")
        self.statistiquesHeros1m = StatistiquesHero()
        self.statistiquesHeros1m.chargerFichierTxt("1m")
        self.statistiquesHeros1p = StatistiquesHero()
        self.statistiquesHeros1p.chargerFichierTxt("1p")
        self.statistiquesHeros21p = StatistiquesHero()
        self.statistiquesHeros21p.chargerFichierTxt("2(1)p")
        self.statistiquesHeros2m = StatistiquesHero()
        self.statistiquesHeros2m.chargerFichierTxt("2m")
        self.statistiquesHeros2p = StatistiquesHero()
        self.statistiquesHeros2p.chargerFichierTxt("2p")
        self.statistiquesHeros31p = StatistiquesHero()
        self.statistiquesHeros31p.chargerFichierTxt("3(1)p")
        self.statistiquesHeros3m = StatistiquesHero()
        self.statistiquesHeros3m.chargerFichierTxt("3m")
        self.statistiquesHeros3p = StatistiquesHero()
        self.statistiquesHeros3p.chargerFichierTxt("3p")
        self.statistiquesHeros41p = StatistiquesHero()
        self.statistiquesHeros41p.chargerFichierTxt("4(1)p")
        self.statistiquesHeros4m = StatistiquesHero()
        self.statistiquesHeros4m.chargerFichierTxt("4m")
        self.statistiquesHeros4p = StatistiquesHero()
        self.statistiquesHeros4p.chargerFichierTxt("4p")
        self.statistiquesHeros5A = StatistiquesHero()
        self.statistiquesHeros5A.chargerFichierTxt("5A")
        self.statistiquesHeros5F = StatistiquesHero()
        self.statistiquesHeros5F.chargerFichierTxt("5F")


    def chargerSauvegardeTxt(self):
        fichierSauvegarde = open (FICHIER_SAUVEGARDE, "r")
        lecture = fichierSauvegarde.readline() #defense flouz possedés par la joueur
        if(int(lecture.replace('\n',"")) > VALEUR_MAX_DEFENSE_FLOUZ):
            lecture = str(VALEUR_MAX_DEFENSE_FLOUZ)
        self.defenseFlouz = int(lecture.replace('\n',""))
        lecture = fichierSauvegarde.readline() #position du joueur sur la carte du monde
        self.positionCarteDuMonde = int(lecture.replace('\n',""))
        lecture = fichierSauvegarde.readline() #avancement du joueur dans l'aventure
        self.avancementAventure = int(lecture.replace('\n',""))
        fichierSauvegarde.close()


    #def charger(self):


    #def sauvegarder(self):
    
    ###########################
    """
    def afficherImageVue(self, image, rectImage):
        #on affiche correctement l'image en fonction de la vue
        self.window.blit(image, (rectImage.x - self.posXVue, rectImage.y - self.posYVue))
        

    def deplacerVue(self, direct, rectImage):
        #si par malheur l'image est plus petite que la fenêtre... ce qui n'est pas censé arriver.
        #l'image doit faire au moins la taille de la fenêtre.
        if(rectImage.h - HAUTEUR_FENETRE > 0 and rectImage.w - LARGEUR_FENETRE > 0):
            if(direct == VUE_DIRECTION_BAS): #on a appuyé sur la flèche du bas
                if(self.posYVue < rectImage.h - HAUTEUR_FENETRE):
                    self.posYVue += PAS_DEPLACEMENT_VUE
                else:
                    self.posYVue = rectImage.h - HAUTEUR_FENETRE
            elif(direct == VUE_DIRECTION_HAUT):
                if(self.posYVue > 0):
                    self.posYVue -= PAS_DEPLACEMENT_VUE
                else:
                    self.posYVue = 0
            elif(direct == VUE_DIRECTION_GAUCHE):
                if(self.posXVue > 0):
                    self.posXVue -= PAS_DEPLACEMENT_VUE
                else:
                    self.posXVue = 0
            else:
                if(self.posXVue < rectImage.w - LARGEUR_FENETRE):
                    self.posXVue += PAS_DEPLACEMENT_VUE
                else:
                    self.posXVue = rectImage.w - LARGEUR_FENETRE
    """
    ###########################


"""
class Sauvegarde():
    def __init__(self):
"""


def synchroStat(Hero, Stat): #pour faciliter l'écriture de la fonction juste en dessous
        Hero.force = Stat.force #pour les attaques physiques
        Hero.intelligence = Stat.intelligence #pour les attaques magiques
        Hero.portee = Stat.portee 
        Hero.vitesseAttaque = Stat.vitesseAttaque #défini aussi la vitesse d'animation / nombre d'attaques par secondes possibles
        Hero.precision = Stat.precision #pour faire réaliste il faut prévoir les "miss" ! Nombre de 0 à ... infini
        Hero.pourcentageCoupCritique = Stat.pourcentageCoupCritique #nombre de 0 à 100


def statHeroForce(systeme, choixHero): #renvoie la force du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.force
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.force
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.force
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.force
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.force
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.force
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.force
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.force
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.force
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.force
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.force
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.force
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.force
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.force
    else:
        return systeme.statistiquesHeros5F.force


def statHeroNiveau(systeme, choixHero): #renvoie la force du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.niveau
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.niveau
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.niveau
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.niveau
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.niveau
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.niveau
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.niveau
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.niveau
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.niveau
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.niveau
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.niveau
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.niveau
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.niveau
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.niveau
    else:
        return systeme.statistiquesHeros5F.niveau


def statHeroIntelligence(systeme, choixHero): #renvoie l'intelligence du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.intelligence
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.intelligence
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.intelligence
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.intelligence
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.intelligence
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.intelligence
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.intelligence
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.intelligence
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.intelligence
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.intelligence
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.intelligence
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.intelligence
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.intelligence
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.intelligence
    else:
        return systeme.statistiquesHeros5F.intelligence


def statHeroType(systeme, choixHero): #renvoie le type du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.type
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.type
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.type
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.type
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.type
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.type
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.type
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.type
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.type
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.type
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.type
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.type
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.type
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.type
    else:
        return systeme.statistiquesHeros5F.type


def statHeroPortee(systeme, choixHero): #renvoie la portee du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.portee
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.portee
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.portee
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.portee
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.portee
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.portee
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.portee
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.portee
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.portee
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.portee
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.portee
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.portee
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.portee
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.portee
    else:
        return systeme.statistiquesHeros5F.portee


def statHeroVitesseAttaque(systeme, choixHero): #renvoie la vitesse d'attaque du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.vitesseAttaque
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.vitesseAttaque
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.vitesseAttaque
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.vitesseAttaque
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.vitesseAttaque
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.vitesseAttaque
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.vitesseAttaque
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.vitesseAttaque
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.vitesseAttaque
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.vitesseAttaque
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.vitesseAttaque
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.vitesseAttaque
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.vitesseAttaque
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.vitesseAttaque
    else:
        return systeme.statistiquesHeros5F.vitesseAttaque


def statHeroPrecision(systeme, choixHero): #renvoie la precision du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.precision
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.precision
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.precision
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.precision
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.precision
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.precision
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.precision
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.precision
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.precision
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.precision
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.precision
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.precision
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.precision
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.precision
    else:
        return systeme.statistiquesHeros5F.precision


def statHeroPourcentageCoupCritique(systeme, choixHero): #renvoie le pourcentage de coup critique du hero défini par choix
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.pourcentageCoupCritique
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.pourcentageCoupCritique
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.pourcentageCoupCritique
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.pourcentageCoupCritique
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.pourcentageCoupCritique
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.pourcentageCoupCritique
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.pourcentageCoupCritique
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.pourcentageCoupCritique
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.pourcentageCoupCritique
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.pourcentageCoupCritique
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.pourcentageCoupCritique
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.pourcentageCoupCritique
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.pourcentageCoupCritique
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.pourcentageCoupCritique
    else:
        return systeme.statistiquesHeros5F.pourcentageCoupCritique


def statHeroExperienceNiveauSuivant(systeme, choixHero): #renvoie le prix qu'il faut payer pour pouvoir invoquer le héro
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.experienceNiveauSuivant
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.experienceNiveauSuivant
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.experienceNiveauSuivant
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.experienceNiveauSuivant
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.experienceNiveauSuivant
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.experienceNiveauSuivant
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.experienceNiveauSuivant
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.experienceNiveauSuivant
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.experienceNiveauSuivant
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.experienceNiveauSuivant
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.experienceNiveauSuivant
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.experienceNiveauSuivant
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.experienceNiveauSuivant
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.experienceNiveauSuivant
    else:
        return systeme.statistiquesHeros5F.experienceNiveauSuivant


def statHeroPrixInvocation(systeme, choixHero): #renvoie le prix qu'il faut payer pour pouvoir invoquer le héro
    if(choixHero == 0):
        return systeme.statistiquesHeros11m.prixInvocation
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p.prixInvocation
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m.prixInvocation
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p.prixInvocation
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p.prixInvocation
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m.prixInvocation
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p.prixInvocation
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p.prixInvocation
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m.prixInvocation
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p.prixInvocation
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p.prixInvocation
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m.prixInvocation
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p.prixInvocation
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A.prixInvocation
    else:
        return systeme.statistiquesHeros5F.prixInvocation


def statHero(systeme, choixHero): #permet d'accéder plus facilement aux statistiques de références des héros
    if(choixHero == 0):
        return systeme.statistiquesHeros11m
    elif(choixHero == 1):
        return systeme.statistiquesHeros11p
    elif(choixHero == 2):
        return systeme.statistiquesHeros1m
    elif(choixHero == 3):
        return systeme.statistiquesHeros1p
    elif(choixHero == 4):
        return systeme.statistiquesHeros21p
    elif(choixHero == 5):
        return systeme.statistiquesHeros2m
    elif(choixHero == 6):
        return systeme.statistiquesHeros2p
    elif(choixHero == 7):
        return systeme.statistiquesHeros31p
    elif(choixHero == 8):
        return systeme.statistiquesHeros3m
    elif(choixHero == 9):
        return systeme.statistiquesHeros3p
    elif(choixHero == 10):
        return systeme.statistiquesHeros41p
    elif(choixHero == 11):
        return systeme.statistiquesHeros4m
    elif(choixHero == 12):
        return systeme.statistiquesHeros4p
    elif(choixHero == 13):
        return systeme.statistiquesHeros5A
    else:
        return systeme.statistiquesHeros5F


def actualiserExperienceNiveauSuivant(systeme):
    systeme.statistiquesHeros11m.calculerExperienceRequiseNiveauSuivant(0)
    systeme.statistiquesHeros11p.calculerExperienceRequiseNiveauSuivant(1)
    systeme.statistiquesHeros1m.calculerExperienceRequiseNiveauSuivant(2)
    systeme.statistiquesHeros1p.calculerExperienceRequiseNiveauSuivant(3)
    systeme.statistiquesHeros21p.calculerExperienceRequiseNiveauSuivant(4)
    systeme.statistiquesHeros2m.calculerExperienceRequiseNiveauSuivant(5)
    systeme.statistiquesHeros2p.calculerExperienceRequiseNiveauSuivant(6)
    systeme.statistiquesHeros31p.calculerExperienceRequiseNiveauSuivant(7)
    systeme.statistiquesHeros3m.calculerExperienceRequiseNiveauSuivant(8)
    systeme.statistiquesHeros3p.calculerExperienceRequiseNiveauSuivant(9)
    systeme.statistiquesHeros41p.calculerExperienceRequiseNiveauSuivant(10)
    systeme.statistiquesHeros4m.calculerExperienceRequiseNiveauSuivant(11)
    systeme.statistiquesHeros4p.calculerExperienceRequiseNiveauSuivant(12)
    systeme.statistiquesHeros5A.calculerExperienceRequiseNiveauSuivant(13)
    systeme.statistiquesHeros5F.calculerExperienceRequiseNiveauSuivant(14)


def actualiserPrixInvocation(systeme):
    systeme.statistiquesHeros11m.calculerPrixInvocation(0)
    systeme.statistiquesHeros11p.calculerPrixInvocation(1)
    systeme.statistiquesHeros1m.calculerPrixInvocation(2)
    systeme.statistiquesHeros1p.calculerPrixInvocation(3)
    systeme.statistiquesHeros21p.calculerPrixInvocation(4)
    systeme.statistiquesHeros2m.calculerPrixInvocation(5)
    systeme.statistiquesHeros2p.calculerPrixInvocation(6)
    systeme.statistiquesHeros31p.calculerPrixInvocation(7)
    systeme.statistiquesHeros3m.calculerPrixInvocation(8)
    systeme.statistiquesHeros3p.calculerPrixInvocation(9)
    systeme.statistiquesHeros41p.calculerPrixInvocation(10)
    systeme.statistiquesHeros4m.calculerPrixInvocation(11)
    systeme.statistiquesHeros4p.calculerPrixInvocation(12)
    systeme.statistiquesHeros5A.calculerPrixInvocation(13)
    systeme.statistiquesHeros5F.calculerPrixInvocation(14)


def levelUpStat(systeme, stat, choixHero): #permet d'accéder plus facilement aux statistiques de références des héros
    aleat = 0 #pour calculer l'augmentation aléatoire bornée des statistiques
    if(choixHero == 0):
        #systeme.statistiquesHeros11m
        stat.niveau += 1
        #stat.force = 0
        aleat = randint(MIN_AUGMENTATION_1, INTELLIGENCE_MAX_LEVEL_UP_11M)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_1, PRECISION_MAX_LEVEL_UP_11M)
        stat.precision += aleat
    elif(choixHero == 1):
        #systeme.statistiquesHeros11p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_1, FORCE_MAX_LEVEL_UP_11P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_1, PRECISION_MAX_LEVEL_UP_11P)
        stat.precision += aleat
    elif(choixHero == 2):
        #systeme.statistiquesHeros1m
        stat.niveau += 1
        #stat.force = 0
        aleat = randint(MIN_AUGMENTATION_1, INTELLIGENCE_MAX_LEVEL_UP_1M)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_1, PRECISION_MAX_LEVEL_UP_1M)
        stat.precision += aleat
    elif(choixHero == 3):
        #systeme.statistiquesHeros1p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_1, FORCE_MAX_LEVEL_UP_1P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_1, PRECISION_MAX_LEVEL_UP_1P)
        stat.precision += aleat
    elif(choixHero == 4):
        #systeme.statistiquesHeros21p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_2, FORCE_MAX_LEVEL_UP_21P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_2, PRECISION_MAX_LEVEL_UP_21P)
        stat.precision += aleat
    elif(choixHero == 5):
        #systeme.statistiquesHeros2m
        stat.niveau += 1
        #stat.force = 0
        aleat = randint(MIN_AUGMENTATION_2, INTELLIGENCE_MAX_LEVEL_UP_2M)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_2, PRECISION_MAX_LEVEL_UP_2M)
        stat.precision += aleat
    elif(choixHero == 6):
        #systeme.statistiquesHeros2p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_2, FORCE_MAX_LEVEL_UP_2P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_2, PRECISION_MAX_LEVEL_UP_2P)
        stat.precision += aleat
    elif(choixHero == 7):
        #systeme.statistiquesHeros31p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_3, FORCE_MAX_LEVEL_UP_31P)
        stat.force += aleat
        aleat = randint(MIN_AUGMENTATION_3, INTELLIGENCE_MAX_LEVEL_UP_31P)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_3, PRECISION_MAX_LEVEL_UP_31P)
        stat.precision += aleat
    elif(choixHero == 8):
        #systeme.statistiquesHeros3m
        stat.niveau += 1
        #stat.force = 0
        aleat = randint(MIN_AUGMENTATION_3, INTELLIGENCE_MAX_LEVEL_UP_3M)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_3, PRECISION_MAX_LEVEL_UP_3M)
        stat.precision += aleat
    elif(choixHero == 9):
        #systeme.statistiquesHeros3p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_3, FORCE_MAX_LEVEL_UP_3P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_3, PRECISION_MAX_LEVEL_UP_3P)
        stat.precision += aleat
    elif(choixHero == 10):
        #systeme.statistiquesHeros41p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_4, FORCE_MAX_LEVEL_UP_41P)
        stat.force += aleat
        aleat = randint(MIN_AUGMENTATION_4, INTELLIGENCE_MAX_LEVEL_UP_41P)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_4, PRECISION_MAX_LEVEL_UP_41P)
        stat.precision += aleat
    elif(choixHero == 11):
        #systeme.statistiquesHeros4m
        stat.niveau += 1
        #stat.force = 0
        aleat = randint(MIN_AUGMENTATION_4, INTELLIGENCE_MAX_LEVEL_UP_4M)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_4, PRECISION_MAX_LEVEL_UP_4M)
        stat.precision += aleat
    elif(choixHero == 12):
        #systeme.statistiquesHeros4p
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_4, FORCE_MAX_LEVEL_UP_4P)
        stat.force += aleat
        #stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_4, PRECISION_MAX_LEVEL_UP_4P)
        stat.precision += aleat
    elif(choixHero == 13):
        #systeme.statistiquesHeros5A
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_5, FORCE_MAX_LEVEL_UP_5A)
        stat.force += aleat
        aleat = randint(MIN_AUGMENTATION_5, INTELLIGENCE_MAX_LEVEL_UP_5A)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_5, PRECISION_MAX_LEVEL_UP_5A)
        stat.precision += aleat
    else:
        #systeme.statistiquesHeros5F
        stat.niveau += 1
        aleat = randint(MIN_AUGMENTATION_5, FORCE_MAX_LEVEL_UP_5F)
        stat.force += aleat
        aleat = randint(MIN_AUGMENTATION_5, INTELLIGENCE_MAX_LEVEL_UP_5F)
        stat.intelligence += aleat
        aleat = randint(MIN_AUGMENTATION_5, PRECISION_MAX_LEVEL_UP_5F)
        stat.precision += aleat
        
                        


#Classe qui permettra d'avoir les statistiques de chaque Héro
#durant la partie
#ce sont ces statistiques qui seronts modifiées (niveau du héro augmente, etc.), etc
#et enregistrées lors de la sauvegarde
#les statistiques du héros correspondant seront synchronisées avec celles-ci durant la partie
#lors de l'invocation du héro il sera crée à partir des données du fichier (qui ne seront pas actualisées durant la partie)
#mais les valeurs de ce chargement seront aussitôt écrasées par ces statistiques
class StatistiquesHero():
    def __init__(self):
        self.feuilleSprite = 0 #le sprite animé du héro
        self.nomFeuilleSprite = 0 #ne sera pas synchronisé avec le héro, celà est là juste pour être enregistré ensuite
        self.niveau = 0 #niveau du héro
        self.experienceNiveauSuivant = 0
        self.prixInvocation = 0
        self.force = 0 #sera synchronisé
        self.intelligence = 0 #sera synchronisé
        self.type = 0 #ne sera pas synchronisé car n'est pas sencé changer
        self.portee = 0 #sera synchronisé
        self.vitesseAttaque = 0 #sera synchronisé
        self.precision = 0 #sera synchronisé
        self.pourcentageCoupCritique = 0 #sera synchronisé
        self.nomSonAttaqueNormale = 0 #ne sera pas synchronisé
        self.nomSonAttaqueCritique = 0 #ne sera pas synchronisé
        self.nomSonManque = 0 #ne sera pas synchronisé
        

    def chargerFichierTxt(self, nomFichier):
        fichier = open(NOM_DOSSIER_HEROS + "/" + nomFichier + "/" + nomFichier + EXTENSION_FICHIER_HEROS, "r")
        
        lecture = fichier.readline() #nom image feuille de sprites
        self.nomFeuilleSprite = str(lecture.replace('\n',""))
        lecture = fichier.readline() #niveau du personnage
        self.niveau = int(lecture.replace('\n',""))
        lecture = fichier.readline() #type
        self.type = str(lecture.replace('\n',""))
        lecture = fichier.readline() #force
        self.force = int(lecture.replace('\n',""))
        lecture = fichier.readline() #intelligence
        self.intelligence = int(lecture.replace('\n',""))
        lecture = fichier.readline() #portee (en nombre de cases)
        self.portee = int(lecture.replace('\n',""))
        lecture = fichier.readline() #vitesse d'attaque (en secondes par attaque)
        self.vitesseAttaque = float(lecture.replace('\n',""))
        lecture = fichier.readline() #precision
        self.precision = int(lecture.replace('\n',""))
        lecture = fichier.readline() #pourcentage coup critique
        self.pourcentageCoupCritique = int(lecture.replace('\n',""))
        lecture = fichier.readline() #son coup normal
        self.nomSonAttaqueNormale = str(lecture.replace('\n',""))
        lecture = fichier.readline() #son coup critique
        self.nomSonAttaqueCritique = str(lecture.replace('\n',""))
        lecture = fichier.readline() #son coup manque (miss)
        self.nomSonManque = str(lecture.replace('\n',""))
        
        fichier.close()

        #On définit la feuille de sprite
        self.feuilleSprite = animation.FeuilleSpriteAnimation(trouverNomFeuilleSprite(NOM_DOSSIER_HEROS + "/" + nomFichier + "/" + \
                                                                                      nomFichier + EXTENSION_FICHIER_HEROS) \
                                                    + "/" + self.nomFeuilleSprite, self.vitesseAttaque / COEFFICIENT_CORRECTION_ANIMATION_HEROS)


    def calculerExperienceRequiseNiveauSuivant(self, choixHero): #experience requise pour passer au niveau suivant = coefficient * niveau
        self.experienceNiveauSuivant = int(self.niveau * COEFFICIENT_NIVEAU_SUIVANT[choixHero])


    def calculerPrixInvocation(self, choixHero): #prix = coefficient x niveau
        self.prixInvocation = int(self.niveau * COEFFICIENT_PRIX_HERO[choixHero])
        
















