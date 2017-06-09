#-*- coding:utf-8 -*-
from system import *
from personnage import *
from carte import *
from animation import *
from menuPrincipal import *



pygame.init()

systeme = Systeme()

systeme.chargerStatistiquesTxt()
system.actualiserExperienceNiveauSuivant(systeme)
system.actualiserPrixInvocation(systeme)
systeme.chargerSauvegardeTxt()

demarrerJeu(systeme)

c = Carte()
c.chargerCarteTxt("0")
c.demarrerPartie(systeme)
pygame.quit()


"""while continuer:
    # fixons le nombre max de frames / secondes
    framerate.tick(FREQUENCE_BOUCLE)
    secondesEcouleesDepuisLeDernierAppelDeTick = framerate.get_time() / 1000

    # On vide la pile d'evenements et on verifie certains evenements
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == QUIT:     #Si un de ces evenements est de type QUIT
            continuer = False      # On arrete la boucle

    c.afficherImage(fenetre)
    pygame.display.flip()

# fin du programme principal...
pygame.quit()"""




















