import pygame
from pygame.locals import *
# -*- coding: utf-8 -*-
from classes import *
import time
pygame.init()
pygame.mouse.set_visible(0)

#Ouverture fenetre Pygame + Titre
fenetre = pygame.display.set_mode((1200, 850),RESIZABLE)
pygame.display.set_caption("Vaispace")

#BOUCLE PRINCIPALE
continuer = 1
while continuer:
	
	#Variable boucle a 1
	continuer_jeu = 1
	continuer_accueil = 1
	quit = 0	

	#Chargement et collage de l'ecran acceuil
	accueil = pygame.image.load("data/background_accueil.jpg").convert()
	fenetre.blit(accueil, (-100,0))
	pygame.display.flip()
	
	#BOUCLE ACCUEIL
	while continuer_accueil:
		
		#Limitation de vitesse de la boucle
    		pygame.time.Clock().tick(30)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					continuer_accueil = 0
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                continuer_jeu = 0
                                continuer = 0
                                continuer_accueil = 0
                                quit = 1
	if quit==0:
		#Parametrage fond du jeu
		fond=Fond()
		#Creation du vaisseau
		vais=Vais()
		#Creation du lasers
		lasers=Lasers()
		#Creation des mechants
		mechants=Mechants()
		#Creation du score + gameover
		gameover=GameOver()
		score=Score()	

	#BOUCLE JEU
	while continuer_jeu:
		for event in pygame.event.get(): 
			if event.type == QUIT:
				continuer = 0
				continuer_jeu = 0
			if event.type == KEYDOWN:
				if event.key==K_ESCAPE:
					continuer_jeu=0
					continuer_accueil=1
					quit = 1
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					lasers.tirer(vais)
			if event.type == MOUSEMOTION: #Si mouvement de souris
       		 		x = event.pos[0]
       		 		y = event.pos[1]
				vais.deplacer(x,y)            	
	
		#Mouvements des lasers
		lasers.update()	
		#Mouvements Fond
		fond.update()
		#Mechant update
		mechants.update(fenetre,lasers,score)
		#Vaisseau update
		vais.update(mechants)

		#Re-collage
    		fond.affiche(fenetre)
		lasers.affiche(fenetre)
		mechants.affiche(fenetre)
		vais.affiche(fenetre)
		
    		#Rafraichissement
    		pygame.display.flip()
		
		#GameOver
		if (gameover.test(vais)):
			time.sleep(2)
			gameover.affiche(fenetre)
			continuer_jeu = 0
	if quit == 0:
		score.affiche(fenetre)
