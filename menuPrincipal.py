#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
from constantes import *
from system import *
from carteDuMonde import *

            


def afficherCredits(systeme):
    ######### Choix de la police et sa taille pour le texte
    font = pygame.font.Font(FONT_CREDITS, TAILLE_POLICE_CREDITS)
    font2 = pygame.font.Font(FONT_CREDITS, TAILLE_POLICE_CREDITS) #pour souligner le texte des crédits
    font2.set_underline(1)

    ######### Images et rect
    imageFont = pygame.image.load(IMAGE_FOND_CREDITS).convert()
    rectImageFont = imageFont.get_rect()

    imageTexteCredits = [] #tableau car on ne sait pas combien de lignes de texte contiendra les crédits
    #Pour ajouter une ligne de crédit il suffit de l'ajouter au tableau, son texte étant dans le fichier constante de préférence et incrémenter le
    #nombre de lignes à afficher toujours dans le fichier constantes
    imageTexteCredits.append(font2.render(TEXTE_CREDITS_LIGNE_1, True, (COULEUR_ROUGE_TEXTE_CREDITS, COULEUR_VERT_TEXTE_CREDITS, COULEUR_BLEU_TEXTE_CREDITS)))
    imageTexteCredits.append(font2.render(TEXTE_CREDITS_LIGNE_2, True, (COULEUR_ROUGE_TEXTE_CREDITS, COULEUR_VERT_TEXTE_CREDITS, COULEUR_BLEU_TEXTE_CREDITS)))
    imageTexteCredits.append(font2.render(TEXTE_CREDITS_LIGNE_3, True, (COULEUR_ROUGE_TEXTE_CREDITS, COULEUR_VERT_TEXTE_CREDITS, COULEUR_BLEU_TEXTE_CREDITS)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_4, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_5, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_6, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font2.render(TEXTE_CREDITS_LIGNE_7, True, (COULEUR_ROUGE_TEXTE_CREDITS, COULEUR_VERT_TEXTE_CREDITS, COULEUR_BLEU_TEXTE_CREDITS)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_8, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_9, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_10, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_11, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_12, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_13, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_14, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_15, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_16, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_17, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font.render(TEXTE_CREDITS_LIGNE_18, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))
    imageTexteCredits.append(font2.render(TEXTE_CREDITS_LIGNE_19, True, (COULEUR_ROUGE_TEXTE_CREDITS2, COULEUR_VERT_TEXTE_CREDITS2, COULEUR_BLEU_TEXTE_CREDITS2)))

    #et de mettre à jour ici aussi
    rectTexteCredits = []
    rectTexteCredits.append(imageTexteCredits[0].get_rect())
    rectTexteCredits.append(imageTexteCredits[1].get_rect())
    rectTexteCredits.append(imageTexteCredits[2].get_rect())
    rectTexteCredits.append(imageTexteCredits[3].get_rect())
    rectTexteCredits.append(imageTexteCredits[4].get_rect())
    rectTexteCredits.append(imageTexteCredits[5].get_rect())
    rectTexteCredits.append(imageTexteCredits[6].get_rect())
    rectTexteCredits.append(imageTexteCredits[7].get_rect())
    rectTexteCredits.append(imageTexteCredits[8].get_rect())
    rectTexteCredits.append(imageTexteCredits[9].get_rect())
    rectTexteCredits.append(imageTexteCredits[10].get_rect())
    rectTexteCredits.append(imageTexteCredits[11].get_rect())
    rectTexteCredits.append(imageTexteCredits[12].get_rect())
    rectTexteCredits.append(imageTexteCredits[13].get_rect())
    rectTexteCredits.append(imageTexteCredits[14].get_rect())
    rectTexteCredits.append(imageTexteCredits[15].get_rect())
    rectTexteCredits.append(imageTexteCredits[16].get_rect())
    rectTexteCredits.append(imageTexteCredits[17].get_rect())
    rectTexteCredits.append(imageTexteCredits[18].get_rect())
    
    rectTexteCredits[0].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[1].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[2].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[3].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[4].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[5].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[6].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[7].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[8].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[9].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[10].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[11].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[12].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[13].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[14].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[15].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[16].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[17].x = POSITION_X_TEXTE_CREDITS
    rectTexteCredits[18].x = POSITION_X_TEXTE_CREDITS

    #et de le placer dans les crédits
    rectTexteCredits[0].y = HAUTEUR_FENETRE
    rectTexteCredits[1].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 2 #Incrémenter le produit de 1 signifie qu'on va a la ligne
    rectTexteCredits[2].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 3
    rectTexteCredits[3].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 4
    rectTexteCredits[4].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 5
    rectTexteCredits[5].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 6
    rectTexteCredits[6].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 7
    rectTexteCredits[7].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 8
    rectTexteCredits[8].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 9
    rectTexteCredits[9].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 10
    rectTexteCredits[10].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 11 #d'ici a la ligne précédente on a sauté trois lignes dans les crédits
    rectTexteCredits[11].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 12
    rectTexteCredits[12].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 14
    rectTexteCredits[13].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 15
    rectTexteCredits[14].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 16
    rectTexteCredits[15].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 17
    rectTexteCredits[16].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 18
    rectTexteCredits[17].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 19
    rectTexteCredits[18].y = HAUTEUR_FENETRE + TAILLE_POLICE_CREDITS * 22

    ######### Musique
    pygame.mixer.music.load(MUSIQUE_CREDITS)
    pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
    pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
    #pygame.mixer.music.pause() Met la musique en pause
    #pygame.mixer.music.unpause() Reprend la musique là où elle a été coupée
    #pygame.mixer.music.stop()
    #http://www.pygame.org/docs/ref/music.html => pygame.mixer.music.set_pos() (pour redémarrer
    #la musique à une position précise une fois qu'elle est arrêtée

    ######### Son
    son = pygame.mixer.Sound(SON_CURSEUR_ANNULE)

    # servira a regler l'horloge du jeu
    framerate = pygame.time.Clock()
    continuer=True
    i = 0 #Pour l'affichage du texte

    apparaitreImageFondu(systeme, imageFont, rectImageFont, TEMPS_FONDU_MENU_PRINCIPAL2)

    while continuer:
        # fixons le nombre max de frames / secondes
        framerate.tick(FREQUENCE_BOUCLE)

        # on recupere l'etat du clavier
        touches = pygame.key.get_pressed();

        if touches[K_BACKSPACE]:
            son.play()
            pygame.mixer.music.stop
            demarrerJeu(systeme)
        elif touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
            
        # Affichage du fond
        systeme.fenetre.blit(imageFont, rectImageFont)

        # Déplacement et affichage du texte des crédits
        for i in range(0, NOMBRE_LIGNES_CREDITS):
            rectTexteCredits[i].y -= VITESSE_TEXTE_CREDITS
            systeme.fenetre.blit(imageTexteCredits[i], rectTexteCredits[i])
    
        # On vide la pile d'evenements et on verifie certains evenements
        for event in pygame.event.get():   # parcours de la liste des evenements recus
             if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()
    

        # raffraichissement
        pygame.display.flip()

    # fin du programme principal...
    pygame.quit()



def afficherContinuer(systeme):
    ######### Choix de la police et sa taille pour le texte
    font = pygame.font.Font(FONT_CONTINUER, TAILLE_POLICE_CONTINUER)

    ######### Images et rect
    imageFont = pygame.image.load(IMAGE_FOND_CONTINUER).convert()
    rectImageFont = imageFont.get_rect()

    ######### Musique
    pygame.mixer.music.load(MUSIQUE_CONTINUER)
    pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
    pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
    #pygame.mixer.music.pause() Met la musique en pause
    #pygame.mixer.music.unpause() Reprend la musique là où elle a été coupée
    #pygame.mixer.music.stop()
    #http://www.pygame.org/docs/ref/music.html => pygame.mixer.music.set_pos() (pour redémarrer
    #la musique à une position précise une fois qu'elle est arrêtée

    ######### Son
    son = pygame.mixer.Sound(SON_MISE_EN_PAUSE)

    # servira a regler l'horloge du jeu
    framerate = pygame.time.Clock()
    continuer=True

    apparaitreImageFondu(systeme, imageFont, rectImageFont, TEMPS_FONDU_MENU_PRINCIPAL2)

    systeme.chargerStatistiquesTxt()
    system.actualiserExperienceNiveauSuivant(systeme)
    system.actualiserPrixInvocation(systeme)
    systeme.chargerSauvegardeTxt()

    while continuer:
        # fixons le nombre max de frames / secondes
        framerate.tick(FREQUENCE_BOUCLE)

        # on recupere l'etat du clavier
        touches = pygame.key.get_pressed();

        if touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
        elif touches[K_RETURN]:
            pygame.mixer.music.stop()
            son.play()
            afficherCarteDuMonde(systeme)
            
        # On vide la pile d'evenements et on verifie certains evenements
        for event in pygame.event.get():   # parcours de la liste des evenements recus
             if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()
    

        # raffraichissement
        pygame.display.flip()

    # fin du programme principal...
    pygame.quit()



def afficherNouvellePartie(systeme):
    ######### Choix de la police et sa taille pour le texte
    font = pygame.font.Font(FONT_NOUVELLE_PARTIE, TAILLE_POLICE_NOUVELLE_PARTIE)

    ######### Images et rect
    imageFont = pygame.image.load(IMAGE_FOND_NOUVELLE_PARTIE).convert()
    rectImageFont = imageFont.get_rect()

    ######### Musique
    pygame.mixer.music.load(MUSIQUE_NOUVELLE_PARTIE)
    pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
    pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
    #pygame.mixer.music.pause() Met la musique en pause
    #pygame.mixer.music.unpause() Reprend la musique là où elle a été coupée
    #pygame.mixer.music.stop()
    #http://www.pygame.org/docs/ref/music.html => pygame.mixer.music.set_pos() (pour redémarrer
    #la musique à une position précise une fois qu'elle est arrêtée

    ######### Son
    son = pygame.mixer.Sound(SON_CURSEUR_ANNULE)

    # servira a regler l'horloge du jeu
    framerate = pygame.time.Clock()
    continuer=True

    apparaitreImageFondu(systeme, imageFont, rectImageFont, TEMPS_FONDU_MENU_PRINCIPAL2)

    while continuer:
        # fixons le nombre max de frames / secondes
        framerate.tick(FREQUENCE_BOUCLE)

        # on recupere l'etat du clavier
        touches = pygame.key.get_pressed();

        if touches[K_BACKSPACE]:
            son.play()
            pygame.mixer.music.stop()
            demarrerJeu(systeme)
        elif touches[K_i]: #capture d'écran si la touche i est pressée
            son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
            son.play()
            pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
        #elif touches[K_RETURN]:
            
        # On vide la pile d'evenements et on verifie certains evenements
        for event in pygame.event.get():   # parcours de la liste des evenements recus
            if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                continuer = False      # On arrete la boucle
                pygame.quit()
    

        # raffraichissement
        pygame.display.flip()

    # fin du programme principal...
    pygame.quit()



def demarrerJeu(systeme):
        """Démarre le jeu et affiche le menu principal"""
        ######### Choix de la police et sa taille pour le texte
        font = pygame.font.Font(FONT_MENU, TAILLE_POLICE_MENU_PRINCIPAL)

        ######### Images et rect
        imageFont = pygame.image.load(IMAGE_FOND_NOUVELLE_PARTIE).convert() #pour le fondu vers les autres parties du menu
        rectImageFont = imageFont.get_rect()
    
        imageEcranTitre1 = pygame.image.load(IMAGE_ECRAN_TITRE_1).convert()
        imageEcranTitre2 = pygame.image.load(IMAGE_ECRAN_TITRE_2).convert()
        imageFlecheHaut = pygame.image.load(IMAGE_FLECHE_HAUT).convert()
        imageFlecheBas = pygame.image.load(IMAGE_FLECHE_BAS).convert()

        i = POSITION_DEPART_MENU #La position dans le menu, le menu va donc commencer par : 0 : Nouvelle Partie, 1 : Continuer, 2 : Crédits
        imageTexte = []
        imageTexte.append(font.render(TEXTE_NOUVELLE_PARTIE_MENU_PRINCIPAL, True, (COULEUR_ROUGE_TEXTE_MENU_PRINCIPAL, \
                                    COULEUR_VERT_TEXTE_MENU_PRINCIPAL, COULEUR_BLEU_TEXTE_MENU_PRINCIPAL)))
        imageTexte.append(font.render(TEXTE_CONTINUER_MENU_PRINCIPAL, True, (COULEUR_ROUGE_TEXTE_MENU_PRINCIPAL, \
                                    COULEUR_VERT_TEXTE_MENU_PRINCIPAL, COULEUR_BLEU_TEXTE_MENU_PRINCIPAL)))
        imageTexte.append(font.render(TEXTE_CREDITS_MENU_PRINCIPAL, True, (COULEUR_ROUGE_TEXTE_MENU_PRINCIPAL, \
                                    COULEUR_VERT_TEXTE_MENU_PRINCIPAL, COULEUR_BLEU_TEXTE_MENU_PRINCIPAL)))

        rectEcranTitre1 = imageEcranTitre1.get_rect()
        rectEcranTitre2 = imageEcranTitre2.get_rect()

        rectTexte = imageTexte[0].get_rect()
        rectTexte.x = (LARGEUR_FENETRE / 2) - (rectTexte.w / 2)
        rectTexte.y = (HAUTEUR_FENETRE / 2) - (rectTexte.h / 2)

        rectFlecheHaut = imageFlecheHaut.get_rect()
        rectFlecheBas = imageFlecheBas.get_rect()
        rectFlecheHaut.x = (LARGEUR_FENETRE / 2) + (rectTexte.w / 2)
        rectFlecheHaut.y = (HAUTEUR_FENETRE / 2) - (rectTexte.h - rectFlecheHaut.h) * 2
        rectFlecheBas.x = (LARGEUR_FENETRE / 2) + (rectTexte.w / 2)
        rectFlecheBas.y = (HAUTEUR_FENETRE / 2) + (rectFlecheBas.h)

        ######### Musique
        pygame.mixer.music.load(MUSIQUE_MENU_PRINCIPAL)
        pygame.mixer.music.set_volume(1) #Met le volume à 1 (à fond)
        pygame.mixer.music.play(-1) #On lit la chanson avec le loop activé
        #pygame.mixer.music.pause() Met la musique en pause
        #pygame.mixer.music.unpause() Reprend la musique là où elle a été coupée
        #pygame.mixer.music.stop()
        #http://www.pygame.org/docs/ref/music.html => pygame.mixer.music.set_pos() (pour redémarrer
        #la musique à une position précise une fois qu'elle est arrêtée

        ######### Son
        son = pygame.mixer.Sound(SON_CURSEUR1)

        # servira a regler l'horloge du jeu
        framerate = pygame.time.Clock()
        continuer=True

        apparaitreImageFondu(systeme, imageEcranTitre1, rectEcranTitre1, TEMPS_FONDU_MENU_PRINCIPAL)
        attendreXSecondes(systeme, ATTENTE_DEMARRAGE_MENU)
        disparaitreImageFondu(systeme, imageEcranTitre1, rectEcranTitre1, TEMPS_FONDU_MENU_PRINCIPAL)
        apparaitreImageFondu(systeme, imageEcranTitre2, rectEcranTitre1, TEMPS_FONDU_MENU_PRINCIPAL)

        while continuer:
                # fixons le nombre max de frames / secondes
                framerate.tick(FREQUENCE_BOUCLE)

                # on recupere l'etat du clavier
                touches = pygame.key.get_pressed();

                if touches[K_ESCAPE] :
                        continuer=False
                elif touches[K_UP]:
                        son.play()
                        i = (i - 1) % 3
                elif touches[K_DOWN]:
                        son.play()
                        i = (i + 1) % 3
                elif touches[K_RETURN]:#K_KP_ENTER
                        if i == 0: #On démarre une nouvelle partie
                            son.play()
                            pygame.mixer.music.stop()
                            afficherNouvellePartie(systeme)
                        elif i == 1: #On continue une partie
                            son.play()
                            pygame.mixer.music.stop()
                            afficherContinuer(systeme)
                        elif i == 2: #On lance les crédits
                            son.play()
                            pygame.mixer.music.stop()
                            afficherCredits(systeme)
                elif touches[K_i]: #capture d'écran si la touche i est pressée
                    son = pygame.mixer.Sound(SON_CAPTURE_ECRAN)
                    son.play()
                    pygame.image.save(systeme.fenetre, determinerNomCapture(systeme))
        

                attendreXSecondes(systeme, ATTENTE_DEPLACEMENT_MENU) #Pour ralentir le déplacement dans le menu

                # Affichage du fond
                systeme.fenetre.blit(imageEcranTitre2, rectEcranTitre2)

                # Affichage du Texte
                systeme.fenetre.blit(imageTexte[i], rectTexte)
                systeme.fenetre.blit(imageFlecheHaut, rectFlecheHaut)
                systeme.fenetre.blit(imageFlecheBas, rectFlecheBas)

                # On vide la pile d'evenements et on verifie certains evenements
                for event in pygame.event.get():   # parcours de la liste des evenements recus
                        if event.type == QUIT:     #Si un de ces evenements est de type QUIT
                                continuer = False      # On arrete la boucle
                                pygame.quit()

                # raffraichissement
                pygame.display.flip()

        # fin du programme principal...
        pygame.quit()



"""def main():
    ######### Initialisation et création de la fenetre et lancement du jeu
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE,HAUTEUR_FENETRE))
    pygame.display.set_icon(pygame.image.load(ICONE_JEU)) #On change l'icone de la fenêtre
    pygame.display.set_caption(NOM_JEU) #On change le nom de la fenêtre
    demarrerJeu(fenetre)"""




"""------------------------------------------------------------------------------------------------"""



"""
main()"""


















