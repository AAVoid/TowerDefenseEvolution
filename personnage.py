#-*- coding:utf-8 -*-
from random import * #nombre aléatoire
from constantes import *
from animation import *
from carte import *
from math import sqrt #pour la racine carrée (calculer les distances)
from math import fabs #pour la valeur absolue





#permet de supprimer tout ce qui est après le dernier slash d'une chaine de caractère
#Exemple : transforme "Monstres/grenouille/grenouille.txt" en
#"Monstres/grenouille"
#(permettra de charger l'image de la feuille de sprite du monstre
def trouverNomFeuilleSprite(chaine):
    i = len(chaine) - 1
    while(chaine[i] != '/'):
        i -= 1
    chaine = chaine.replace(chaine[i : len(chaine)], "")
    return chaine


#permettra au Héros de se tourner vers son ennemi lorsqu'il tente de l'attaquer
def trouverDirectionAttaque(personnage, monstre):
    distanceX = personnage.posX - monstre.posX
    distanceY = personnage.posY - monstre.posY

    if(fabs(distanceX) > fabs(distanceY) and distanceX > 0):
        return LIGNE_PERSONNAGE_GAUCHE
    elif (fabs(distanceX) > fabs(distanceY) and distanceX < 0):
        return LIGNE_PERSONNAGE_DROITE
    elif(fabs(distanceY) > fabs(distanceX) and distanceY < 0):
        return LIGNE_PERSONNAGE_BAS
    elif(fabs(distanceY) > fabs(distanceX) and distanceY > 0):
        return LIGNE_PERSONNAGE_HAUT
    elif(fabs(distanceX) == fabs(distanceY) and distanceX < 0):
        return LIGNE_PERSONNAGE_DROITE
    elif(fabs(distanceX) == fabs(distanceY) and distanceX > 0):
        return LIGNE_PERSONNAGE_GAUCHE
    else: #ne devrait pas arriver mais on met un cas par défaut
        return LIGNE_PERSONNAGE_BAS




class Personnage: #ce qui est commun au Hero et au Monstre
    def __init__(self):
        self.feuilleSprite = 0 #permet de gérer l'animation du personnage via la classe FeuilleSpriteAnimation
        #dans le fichier animation.py
        self.posX = 0 #utilisé pour les déplacements
        self.posY = 0 #utilisé pour les déplacements
        self.posXAffiche = 0 #position X où l'image du sprite du personnage est affiché
        self.posYAffiche = 0
        self.direction = "i" #la direction du personnage
        #les directions possibles sont "h" : haut ; "b" : bas ; "g" : gauche ; "d" : droite ; "i" : immobile


    def afficher(self, systeme, chrono):
        self.feuilleSprite.afficherAnimer(systeme, (self.posXAffiche, self.posYAffiche), chrono)


    #Téléporte le personnage à la position (x,y) sur la carte                                   
    def placerCase(self, posX, posY): #posX et posY sont des index de cases sur la carte (a partir de 0)
        self.posX = posX 
        self.posY = posY
        #on centre le sprite sur la case
        largeur = self.feuilleSprite.rectImageFeuilleSprite.w / self.feuilleSprite.nombreSpriteLargeur
        hauteur = self.feuilleSprite.rectImageFeuilleSprite.h / self.feuilleSprite.nombreSpriteHauteur
        self.posXAffiche = (TAILLE_CASE * self.posX) + TAILLE_CASE / 2 - largeur / 2
        self.posYAffiche = (TAILLE_CASE * self.posY) + TAILLE_CASE / 2 - hauteur + CORRECTION_PIXEL_Y_PLACEMENT_CARTE



class Hero(Personnage): #un héro est un personnage, on rajoute des attributs supplémentaires
#Le héros sera un personnage allié qui attaquera les monstres à proximité une fois placé sur le terrain
    def __init__(self):
        Personnage.__init__(self)
        self.niveau = 0 #le niveau du personnage, l'expérience necessaire pour monter de niveau est calculée et n'a pas
        #besoin d'être un attribut
        self.force = 0 #pour les attaques physiques
        self.intelligence = 0 #pour les attaques magiques
        self.type = 0 #"p" : Physique ; "m" : Magique ; "pm" : Mixte (physique et magique)
        self.portee = 0 
        self.vitesseAttaque = 0 #nombre de seconde entre chaque attaque (définit aussi la vitesse d'animation)
        self.chronoAttaque = 0 #pour chronométrer le temps écoulé depuis la dernière attaque
        self.precision = 0 #pour faire réaliste il faut prévoir les "miss" ! Nombre de 0 à ... infini
        self.pourcentageCoupCritique = 0 #nombre de 0 à 100
        self.sonAttaqueNormale = 0 #le son est placé dans le dossier son du jeu
        self.sonAttaqueCritique = 0
        self.sonManque = 0


    def attaquer(self, monstre): #attaque le monstre en tenant compte de la précision, de l'esquive et du
        #pourcentage de coup critique
        self.chronoAttaque = 0
        #on se tourne plus ou moins vers le monstre
        self.feuilleSprite.changerPositionY(trouverDirectionAttaque(self, monstre))
        if(monstre.esquive == 0):
            chancesAAvoirPourToucher = 101 #on génère un nombre entre 0 et 100 toujours inférieur à 101 donc on touche à 100%
        else:
            chancesAAvoirPourToucher = int(round((self.precision * 100) / monstre.esquive)) #un pourcentage
        aleatoireTouche = randint(0, 100)
        #On rajoute une petit oscillation de X% pour "améliorer l'aléatoire"
        aleatCh = randint(POURCENTAGE_MIN_CHANCE_TOUCHE_SUPPLEMENTAIRE, POURCENTAGE_MAX_CHANCE_TOUCHE_SUPPLEMENTAIRE)
        if(aleatoireTouche + aleatCh < chancesAAvoirPourToucher): #on touche l'ennemi
            aleatoireCoupCritique = randint(0, 100) #pour vérifier si on fait un coup critique
            if(aleatoireCoupCritique < self.pourcentageCoupCritique): #c'est un coup critique !
                pourcentageMax = randint(POURCENTAGE_MIN_DEGATS_SUPPLEMENTAIRES_COUP_CRITIQUE, \
                                         POURCENTAGE_MAX_DEGATS_SUPPLEMENTAIRES_COUP_CRITIQUE)
                #on joue le son coup critique
                self.sonAttaqueCritique.play()
                if(self.type == "p"):
                    monstre.perdreVies(int(self.force + self.force * pourcentageMax / 100 - monstre.defensePhysique))
                elif(self.type == "m"):
                    monstre.perdreVies(int(self.intelligence + self.intelligence * pourcentageMax / 100 - monstre.defenseMagique))
                else: #type == "pm"
                    choixTypeAttaque = randint(0, 1)
                    if(choixTypeAttaque == 0): #physique
                        monstre.perdreVies(int(self.force + self.force * pourcentageMax / 100 - monstre.defensePhysique))
                    else: #magique
                        monstre.perdreVies(int(self.intelligence + self.intelligence * pourcentageMax / 100 - monstre.defenseMagique))
            else: #c'est un coup normal !
                #même si on ne fait pas des coups critiques les dégats infligés peuvent varier
                #on peut infliger entre X% de dégats en moins ou jusqu'à X% de dégats en plus
                pourcentage = randint(POURCENTAGE_MIN_DEGATS_SUPPLEMENTAIRES, \
                                      POURCENTAGE_MAX_DEGATS_SUPPLEMENTAIRES)
                #on joue le son normal
                self.sonAttaqueNormale.play()
                if(self.type == "p"):
                    monstre.perdreVies(int(self.force + self.force * pourcentage / 100 - monstre.defensePhysique))
                elif(self.type == "m"):
                    monstre.perdreVies(int(self.intelligence + self.intelligence * pourcentage / 100 - monstre.defenseMagique))
                else: #type == "pm"
                    choixTypeAttaque = randint(0, 1)
                    if(choixTypeAttaque == 0): #physique
                        monstre.perdreVies(int(self.force + self.force * pourcentage / 100 - monstre.defensePhysique))
                    else: #magique
                        monstre.perdreVies(int(self.intelligence + self.intelligence * pourcentage / 100 - monstre.defenseMagique))
        else: #on rate l'ennemi
            #on joue le son "Raté" et on l'affiche à côté du monstre
            self.sonManque.play()
            monstre.imageTexteDegats = monstre.fontDegats.render(TEXTE_HERO_RATE_ENNEMI, True, (COULEUR_ROUGE_TEXTE_DEGATS, \
                                                                                     COULEUR_VERT_TEXTE_DEGATS, COULEUR_BLEU_TEXTE_DEGATS))
            monstre.rectImageTexteDegats = monstre.imageTexteDegats.get_rect()
            monstre.rectImageTexteDegats.x = monstre.posXAffiche + monstre.feuilleSprite.largeurSprite \
                                          + CORRECTION_POSX_TEXTE_DEGATS
            monstre.rectImageTexteDegats.y = monstre.posYAffiche + CORRECTION_POSY_TEXTE_DEGATS
            monstre.chronoTexteDegats = 0
    


    def testAttaque(self, monstre, chrono): #test si le Héro peut attaquer le monstre
        #en fonction de la vitesse d'attaque du personnage
        #on calcul la distance entre le Héro et le monstre
        if(monstre.chronoDebutMarche >= monstre.tempsDebutMarche): #ça serait dommage que le monstre commence à perdre de la vie
        #alors qu'il ne bouge même pas encore
            #alors qu'il ne bouge pas encore !!!
            self.chronoAttaque += chrono #pour la fréquence d'attaque du Héros
            if(self.chronoAttaque >= self.vitesseAttaque): #le héro peut attaquer
                self.chronoAttaque = 0
                #sont accessibles
                distance = self.portee * sqrt(2)
                if(sqrt((self.posY - monstre.posY) * (self.posY - monstre.posY) + (self.posX - monstre.posX) * (self.posX - monstre.posX)) <= distance):
                    #on attaque le monstre
                    self.attaquer(monstre)
                    return True #le héro a essaye d'attaquer
                else:
                    return False #ne héro n'a pas pu essayer d'attaquer (ennemi trop loin)
            else:
                return False #le héro n'a pas attaqué (chrono)
        else:
            return False #le héro n'a pas attaqué car le monstre ne bouge pas encore



    def chargerFichierTxt(self, nomFichier):
        fichier = open(NOM_DOSSIER_HEROS + "/" + nomFichier + "/" + nomFichier + EXTENSION_FICHIER_HEROS, "r")

        lecture = fichier.readline() #nom image feuille de sprites
        nomFeuilleSprite = str(lecture.replace('\n',""))
        lecture = fichier.readline() #niveau du héro
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
        self.sonAttaqueNormale = pygame.mixer.Sound(NOM_DOSSIER_SONS + "/" + str(lecture.replace('\n',"")))
        lecture = fichier.readline() #son coup critique
        self.sonAttaqueCritique = pygame.mixer.Sound(NOM_DOSSIER_SONS + "/" + str(lecture.replace('\n',"")))
        lecture = fichier.readline() #son coup manque (miss)
        self.sonManque = pygame.mixer.Sound(NOM_DOSSIER_SONS + "/" + str(lecture.replace('\n',"")))

        fichier.close()

        #l'image et le rect ne sont pas écrits dans le fichier, on les actualise
        self.feuilleSprite = FeuilleSpriteAnimation(trouverNomFeuilleSprite(NOM_DOSSIER_HEROS + "/" + nomFichier + "/" + nomFichier + EXTENSION_FICHIER_HEROS) \
                                                    + "/" + nomFeuilleSprite, self.vitesseAttaque / COEFFICIENT_CORRECTION_ANIMATION_HEROS)
        #on fait une addition pour l'animation afin que la vitesse de déplacement des monstre affiche une animation d'une vitesse
        #cohérente



class Monstre(Personnage): #un monstre est un personnage, on rajoute des attributs supplémentaires
    def __init__(self):
        Personnage.__init__(self)
        self.spriteSceauInvocation = 0 #sprite qui sera affiché lors de l'invocation du monstre
        self.pvMax = 0
        self.pvActuels = 0
        self.defensePhysique = 0
        self.defenseMagique = 0
        self.esquive = 0 #pour faire réaliste il faut prévoir les "miss" ! Nombre de 0 à ... infini
        self.vitesseDeplacement = 0 #définit aussi la vitesse d'animation
        self.distanceParcouruePrecedente = 0 #pour le déplacement
        self.distanceParcourue = 0 #pour le déplacement
        self.enDeplacement = False #pour le déplacement
        self.defenseFlouz = 0 #argent du jeu
        self.sonMort = 0 #son joué à la mort du monstre
        self.sonTeleportation = 0
        self.fontDegats = pygame.font.Font(FONT_DEGATS, TAILLE_FONT_DEGATS)
        self.imageTexteDegats = 0 #pour pouvoir afficher les dégats du monstre
        self.rectImageTexteDegats = 0
        self.chronoTexteDegats = TEMPS_AFFICHAGE_DEGATS + 1 #pour ne pas essayer d'afficher de dégats à l'apparition du monstre
        self.tempsDebutMarche = 0 #défini l'instant où le monstre commence à avancer après le début de la vague
        self.chronoDebutMarche = 0
        


    #Charge le monstre à partir d'un fichier texte
    #On crée un dossier du nom du monstre dans le dossier monstre
    #dans ce dossier monstre il y aura un fichier texte du nom du DOSSIER + l'image de la feuille de sprite du monstre
    def chargerFichierTxt(self, nomFichier):
        fichier = open(nomFichier, "r")

        lecture = fichier.readline() #nom image feuille de sprites
        nomFeuilleSprite = str(lecture.replace('\n',""))
        lecture = fichier.readline() #pvMax
        self.pvMax = int(lecture.replace('\n',""))
        lecture = fichier.readline() #defense Physique
        self.defensePhysique = int(lecture.replace('\n',""))
        lecture = fichier.readline() #defense Magique
        self.defenseMagique = int(lecture.replace('\n',""))
        lecture = fichier.readline() #esquive : pour faire réaliste il faut prévoir les "miss" !
        self.esquive = int(lecture.replace('\n',""))
        lecture = fichier.readline() #vitesse de déplacement
        self.vitesseDeplacement = float(lecture.replace('\n',""))
        lecture = fichier.readline() #expérience donnée
        self.defenseFlouz = int(lecture.replace('\n',""))
        lecture = fichier.readline() #son mort
        self.sonMort = pygame.mixer.Sound(NOM_DOSSIER_SONS + "/" + str(lecture.replace('\n',"")))
        lecture = fichier.readline() #son teleportation
        self.sonTeleportation = pygame.mixer.Sound(NOM_DOSSIER_SONS + "/" + str(lecture.replace('\n',"")))

        fichier.close()

        #l'image et le rect ne sont pas écrits dans le fichier, on les actualise
        self.pvActuels = self.pvMax
        self.feuilleSprite = FeuilleSpriteAnimation(trouverNomFeuilleSprite(nomFichier) + "/" + \
                                                    nomFeuilleSprite, 1/(self.vitesseDeplacement + CORRECTION_SYNCHRO_VITESSE_DEPLA_ANIMATION))
        #on fait une addition pour l'animation afin que la vitesse de déplacement des monstre affiche une animation d'une vitesse
        #cohérente
        #Le sprite affiché lors de l'apparition du monstre
        self.spriteSceauInvocation = FeuilleSpriteAnimation(FICHIER_IMAGE_SPRITE_SCEAU_INVOCATION, 0, 1, 1)


    def afficher(self, systeme, chrono): #on la redéfinie ici car il faut aussi afficher les dégats subits !
        self.feuilleSprite.afficherAnimer(systeme, (self.posXAffiche, self.posYAffiche), chrono)
        self.chronoTexteDegats += chrono
        if(self.chronoTexteDegats < TEMPS_AFFICHAGE_DEGATS):
            systeme.fenetre.blit(self.imageTexteDegats, self.rectImageTexteDegats)
            



    def perdreVies(self, nombreDeVies):
        if(nombreDeVies > self.pvActuels):
            self.pvActuels = 0
            self.sonMort.play()
            #del self ###LE MONSTRE EST EFFACE DANS LA METHODE SUPPRIMERMONSTRE DE LA CARTE
        elif(nombreDeVies >= 0): #car ça peut être négatif si la défense du monstre est trop élevée, voir la fonction attaquer du Héros
            self.pvActuels -= nombreDeVies
            #on modifie l'affichage des dégats
            self.imageTexteDegats = self.fontDegats.render(str(nombreDeVies), True, (COULEUR_ROUGE_TEXTE_DEGATS, \
                                                                                     COULEUR_VERT_TEXTE_DEGATS, COULEUR_BLEU_TEXTE_DEGATS))
            self.rectImageTexteDegats = self.imageTexteDegats.get_rect()
            self.rectImageTexteDegats.x = self.posXAffiche + self.feuilleSprite.rectImageFeuilleSprite.w / self.feuilleSprite.nombreSpriteLargeur \
                                          + CORRECTION_POSX_TEXTE_DEGATS
            self.rectImageTexteDegats.y = self.posYAffiche + CORRECTION_POSY_TEXTE_DEGATS
            self.chronoTexteDegats = 0



    def deplacer(self, systeme, carte, chrono): #chrono pour pouvoir commencer à déplacer le monstre quand c'est prévu après le début de la vague
        if(self.chronoDebutMarche >= self.tempsDebutMarche):
            #actualisation de la position du personnage/distance parcourue
            if(self.enDeplacement and self.distanceParcourue + self.vitesseDeplacement >= TAILLE_CASE):
                self.distanceParcouruePrecedente = self.distanceParcourue
                self.distanceParcourue = TAILLE_CASE
                self.enDeplacement = False #le déplacement est terminé
                if(self.direction == "d"):
                    self.posX += 1
                elif(self.direction == "g"):
                    self.posX -= 1
                elif(self.direction == "h"):
                    self.posY -= 1
                elif(self.direction == "b"):
                    self.posY += 1
                else: #i et p
                    self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)
            elif(self.enDeplacement and self.distanceParcourue + self.vitesseDeplacement < TAILLE_CASE):
                self.distanceParcouruePrecedente = self.distanceParcourue
                self.distanceParcourue += self.vitesseDeplacement


            #actualisation de la position d'affichage du personnage
            if(self.enDeplacement and self.direction == "d"):
                self.posXAffiche += (self.distanceParcourue - self.distanceParcouruePrecedente)
            elif(self.enDeplacement and self.direction == "g"):
                self.posXAffiche -= (self.distanceParcourue - self.distanceParcouruePrecedente)
            elif(self.enDeplacement and self.direction == "h"):
                self.posYAffiche -= (self.distanceParcourue - self.distanceParcouruePrecedente)
            elif(self.enDeplacement and self.direction == "b"):
                self.posYAffiche += (self.distanceParcourue - self.distanceParcouruePrecedente)
            else:
                self.enDeplacement = False #on n'arrête le personnage

            if(not self.enDeplacement): #on a terminé un précédent déplacement, on change de direction
                #génère un nombre "aléatoire" entre 0 et tabDir.[self.posY][self.posX].nombreDirectionsPossibles - 1
                if(not (self.posX >= (carte.largeur - 1) or self.posX < 0 or self.posY >= (carte.hauteur - 1) or self.posY < 0)):
                    #seulement si le personnage est sur la carte, pour éviter les erreur d'indice du tableau de directions
                    direc = randint(0, carte.tableauCases[self.posY][self.posX].nombreDirectionsPossibles - 1)
                    self.direction = carte.tableauCases[self.posY][self.posX].direction[direc]
                    if(self.direction == "d"):
                        self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_DROITE)
                        self.placerCase(self.posX, self.posY) #on s'assure que le personnage est bien au centre de la case
                        #car sans ceci des décalages apparaissent dans les déplacement, ceci résout le problème
                    elif(self.direction == "g"):
                        self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_GAUCHE)
                        self.placerCase(self.posX, self.posY)
                    elif(self.direction == "h"):
                        self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_HAUT)
                        self.placerCase(self.posX, self.posY)
                    elif(self.direction == "b"):
                        self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)
                        self.placerCase(self.posX, self.posY)
                    elif(self.direction == "t"): #On se téléporte
                        nbDestPossibles = carte.tableauCases[self.posY][self.posX].nombreDestinationsTeleportation
                        if(nbDestPossibles == 1):
                            dest = 0
                        else:
                            dest = randint(0, nbDestPossibles - 1)
                        (destX, destY) = carte.tableauCases[self.posY][self.posX].tableauCoordonneesDestinationTeleportation[dest]
                        self.sonTeleportation.play()
                        self.placerCase(destX, destY)
                    else: #i et p
                        self.feuilleSprite.changerPositionY(LIGNE_PERSONNAGE_BAS)
                        self.placerCase(self.posX, self.posY)
                self.enDeplacement = True
                self.distanceParcouruePrecedente = 0
                self.distanceParcourue = 0
        else: #si assez de temps n'est pas encore passe pour que le monstre commence à bouger
            self.chronoDebutMarche += chrono

        #on actualise la position d'affichage des dégats
        if(self.chronoTexteDegats < TEMPS_AFFICHAGE_DEGATS):
            self.rectImageTexteDegats = self.imageTexteDegats.get_rect()
            self.rectImageTexteDegats.x = self.posXAffiche + self.feuilleSprite.rectImageFeuilleSprite.w / self.feuilleSprite.nombreSpriteLargeur \
                                        + CORRECTION_POSX_TEXTE_DEGATS
            self.rectImageTexteDegats.y = self.posYAffiche + CORRECTION_POSY_TEXTE_DEGATS
                

        



















