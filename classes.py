import pygame
from pygame.locals import *
# -*- coding: utf-8 -*-
import random
import time

class Fond:
	def __init__(self):
		self.fond1 = pygame.image.load("data/background.jpg").convert()
		self.x1=0
		self.fond2 = pygame.image.load("data/background.jpg").convert()
		self.x2=1440
	#Permet le deplacement du fond
	def update(self):
		self.x1-=1
		self.x2-=1
		if self.x1==-1440:
			self.x1=1440
		if self.x2==-1440:
			self.x2=1440
	def affiche(self,fenetre):	
		fenetre.blit(self.fond1, (self.x1,0))
		fenetre.blit(self.fond2, (self.x2,0))


class Vais:
	
	#Permet de creer le vaisseau
	def __init__(self):
		#Vaisseau
		self.vais_img = pygame.image.load("data/Vaisseau.png").convert_alpha()
		self.position_vais = self.vais_img.get_rect()
		self.tla = 1
		#Explosion
		self.exp = pygame.image.load("data/explosion.png").convert_alpha()
                self.position_exp = self.exp.get_rect()
                self.position_exp.center = 1400,70
		self.son_explosion = pygame.mixer.Sound("data/explosion.wav")
	
	def deplacer(self,x,y):
		self.position_vais.x = x
        	self.position_vais.y = y

	def explose(self):
		self.tla=0
		self.position_exp.center = self.position_vais.center
		self.position_vais.x = 1440
        	self.position_vais.y = 70
	
	def tirer(self,laser):
		laser.tirer_deb(self.position_vais.x,self.position_vais.y,1)
	
	def update(self,mechants):
		if (mechants.nbsession!=-1):
			for i in range(0,len(mechants.session.tab)):
				if (self.position_vais.colliderect(mechants.session.tab[i].laser.position_laser)):
					self.explose()
			n=2
		else:
			for i in range(0,len(mechants.session.boss.tablaser)):
				if (self.position_vais.colliderect(mechants.session.boss.tablaser[i].position_laser)):
					self.explose()
			a=2
	def affiche(self,fenetre):
    		fenetre.blit(self.vais_img, (self.position_vais.x,self.position_vais.y))
    		fenetre.blit(self.exp, (self.position_exp.x,self.position_exp.y))

class Laser:
		def __init__(self):
			self.laser = pygame.image.load("data/laser.png").convert_alpha()
                	self.position_laser = self.laser.get_rect()
			self.position_laser.center= 1400,70
			self.tire = 0
			self.son_laser = pygame.mixer.Sound("data/laser.wav")

		#Initialise le tire quand il va s'effectuer
		def tirer_deb(self,x,y,sens):
			if(self.tire == 0):
				self.son_laser.play()
				self.position_laser.center = x,y
				if sens==1:
					self.position_laser = self.position_laser.move(150,35)
				if sens==0:
					self.position_laser = self.position_laser.move(-3,20)
				self.tire = 1
				self.sens = sens
		#Deplace le laser dans le sens demande
		def deplacer(self):
			if (self.sens == 0):
				self.position_laser = self.position_laser.move(-3,0)	
			if (self.sens == 1):
				self.position_laser = self.position_laser.move(5,0)	
				
		#Remet le laser quand il a fini sa course ou detruis un vaisseau
		def tirer_fin(self,stop):
			if(self.position_laser.x >= 1200 or self.position_laser.x <= 0 or stop==True):
				self.tire = 0
				self.position_laser.center = 1400,70
		#Methode a appeller pour la mise a jour du laser
		def update(self):
			self.tirer_fin(False)
			if self.tire == 1:
				self.deplacer()	
		
		def affiche(self,fenetre):
			fenetre.blit(self.laser,self.position_laser)

#Classe gerant plusieurs laser (pour le joueur)
class Lasers:
		def __init__(self):
			self.laser1=Laser()
			self.laser2=Laser()
			self.laser3=Laser()
			self.laser4=Laser()
			self.laser5=Laser()
			self.laser6=Laser()
			self.laser7=Laser()
			self.tab=[self.laser1,self.laser2,self.laser3,self.laser4,self.laser5,self.laser6,self.laser7]
	
		#Verifie si le laser tire et le fais tirer si ce n'est pas le cas
		def tirer(self,vais):
			test=0
			for i in range(0,len(self.tab)):
				if self.tab[i].tire==0:
					test=1
					vais.tirer(self.tab[i])
				if test==1:
					break
		#Appelle l'update des lasers
		def update(self):
			for i in range (0,len(self.tab)):
				self.tab[i].update()

        	def affiche(self,fenetre):
			for i in range (0,len(self.tab)):
				self.tab[i].affiche(fenetre)

class Mechant:
	def __init__(self,x,y,nbtype):
		#Mechant
		if nbtype==1:
			self.mech = pygame.image.load("data/mechant1.png").convert_alpha()
                if nbtype==2:
			self.mech = pygame.image.load("data/mechant2.png").convert_alpha()
		if nbtype==3:		
			self.mech = pygame.image.load("data/mechant3.png").convert_alpha()
		self.position_mech = self.mech.get_rect()
                self.position_mech.center = x,y
		self.tla=1
		#Explosion
		self.exp = pygame.image.load("data/explosion.png").convert_alpha()
                self.position_exp = self.exp.get_rect()
                self.position_exp.center = 1400,70
		self.son_explosion = pygame.mixer.Sound("data/explosion.wav")
		self.texp=0
		#Laser	
		self.laser=Laser()

	def explose(self,fenetre,lasers,score):
		#Introduis un temps avant fin de l'explosion
		if(self.texp>=1):
                        self.texp+=1
                if self.texp>=30:
                        self.position_exp.center = 1300,70
			self.tla=0
		#Detecte la collision
		for i in range(0,len(lasers.tab)):
			if (self.position_mech.colliderect(lasers.tab[i].position_laser) and self.texp==0):
				score.plusun()
				lasers.tab[i].tirer_fin(True)
				self.son_explosion.play()
				self.position_exp.center = self.position_mech.center
				self.texp+=1
				self.position_mech.center=1400,70
				break
		#Affiche l'explosion
		fenetre.blit(self.mech, self.position_mech)
		fenetre.blit(self.exp, self.position_exp)


	def tirer(self):
		self.laser.tirer_deb(self.position_mech.x,self.position_mech.y,0)
	
	def update(self,fenetre,lasers,score):
		self.laser.update()
		if self.tla==1:
			self.explose(fenetre,lasers,score)

	def affiche(self,fenetre):	
		fenetre.blit(self.exp,(self.position_exp.x,self.position_exp.y))
		fenetre.blit(self.mech,(self.position_mech.x,self.position_mech.y))
		self.laser.affiche(fenetre)

#Classe gerant les differentes session d'ennemis
class Mechants:
	def __init__(self):
		self.test=0
		self.nbsession=0
		self.sessionter=True
		self.session=None

	#Verifie si la session en cour est termine et en recreer une si necessaire
	def sessiontest(self):
		if self.sessionter==True:
			if self.nbsession==5:
				self.session=Sessionboss()
				self.sessionter=False
				self.nbsession=-1
			else:
				self.test=random.randint(0,2)
				if self.test==0:
					self.session=Session1()
					self.sessionter=False
				if self.test==1:
					self.session=Session2()
					self.sessionter=False			
				if self.test==2:
					self.session=Session3()
					self.sessionter=False
		
	#Appelle l'update de la session en cour et verifie si la session est fini 
	def update(self,fenetre,lasers,score):
		if self.sessionter==False:
			self.session.update(fenetre,lasers,score)
			if self.session.session_fin() == True:
				self.nbsession+=1
				self.session=None
				self.sessionter=True
		self.sessiontest()

	def affiche(self,fenetre):
		if self.sessionter==False:
			self.session.affiche(fenetre)
			
class Session1:
	def __init__(self):
		self.mech1=Mechant(1100,300,1)
		self.mech2=Mechant(1100,400,3)
		self.mech3=Mechant(1100,500,1)
		self.tab=[self.mech1,self.mech2,self.mech3]
	
	#Renvoi true si la session est fini, False sinon
	def session_fin(self):
		for i in range (0,len(self.tab)):
			if (self.tab[i].tla==True):
				return False
		return True


	#Effectue les tire et les deplacement
	def update(self,fenetre,lasers,score):
		for i in range(0,len(self.tab)):
			if random.randint(0,500)==1 and self.tab[i].laser.tire==0 and self.tab[i].tla==1:
				self.tab[i].tirer()
			self.tab[i].update(fenetre,lasers,score)

	def affiche(self,fenetre):
		for i in range(0,len(self.tab)):
			self.tab[i].affiche(fenetre)

class Session2:
	def __init__(self):
		self.mech1=Mechant(1100,200,1)
		self.mech2=Mechant(1000,300,2)
		self.mech3=Mechant(900,400,3)
		self.mech4=Mechant(1000,500,2)
		self.mech5=Mechant(1100,600,1)
		self.mech6=Mechant(1100,400,1)
		self.tab=[self.mech1,self.mech2,self.mech3,self.mech4,self.mech5,self.mech6]
	
	#Renvoi true si la session est fini, False sinon
	def session_fin(self):
		for i in range (0,len(self.tab)):
			if (self.tab[i].tla==True):
				return False
		return True


	#Effectue les tire et les deplacement
	def update(self,fenetre,lasers,score):
		for i in range(0,len(self.tab)):
			if random.randint(0,500)==1 and self.tab[i].laser.tire==0 and self.tab[i].tla==1:
				self.tab[i].tirer()
			self.tab[i].update(fenetre,lasers,score)

	def affiche(self,fenetre):
		for i in range(0,len(self.tab)):
			self.tab[i].affiche(fenetre)

class Session3:
	def __init__(self):
		self.mech1=Mechant(1100,150,2)
		self.mech2=Mechant(1000,150,2)
		self.mech3=Mechant(1050,250,3)
		self.mech4=Mechant(1100,350,2)
		self.mech5=Mechant(1000,350,2)
		self.mech6=Mechant(1050,450,3)
		self.mech7=Mechant(1100,550,2)
		self.mech8=Mechant(1000,550,2)
		self.tab=[self.mech1,self.mech2,self.mech3,self.mech4,self.mech5,self.mech6,self.mech7,self.mech8]
	
	#Renvoi true si la session est fini, False sinon
	def session_fin(self):
		for i in range (0,len(self.tab)):
			if (self.tab[i].tla==True):
				return False
		return True

	#Effectue les tire et les deplacement
	def update(self,fenetre,lasers,score):
		for i in range(0,len(self.tab)):
			if random.randint(0,500)==1 and self.tab[i].laser.tire==0 and self.tab[i].tla==1:
				self.tab[i].tirer()
			self.tab[i].update(fenetre,lasers,score)

	def affiche(self,fenetre):
		for i in range(0,len(self.tab)):
			self.tab[i].affiche(fenetre)
class Sessionboss:
	def __init__(self):
		self.boss=Boss()
		self.tab=[self.boss]
	
	#Renvoi true si la session est fini, False sinon
	def session_fin(self):
		if self.boss.tla==False:
			return True
		else:
			return False

	#Effectue les tire et les deplacement
	def update(self,fenetre,lasers,score):
		if random.randint(0,350)==1 and self.boss.tablaser[1].tire==0 and self.boss.tla==1:
			self.boss.tirer()
		self.boss.update(fenetre,lasers,score)

	def affiche(self,fenetre):
		self.boss.affiche(fenetre)

class Boss:
	def __init__(self):
		self.boss = pygame.image.load("data/Boss.png").convert_alpha()
		self.position_boss = self.boss.get_rect()
                self.position_boss.center = 900,400
		self.tla=1
		self.tempo=0
		self.sens=1
		#Explosion
		self.exp = pygame.image.load("data/explosion.png").convert_alpha()
                self.position_exp = self.exp.get_rect()
                self.position_exp.center = 1400,70
		self.son_explosion = pygame.mixer.Sound("data/explosion.wav")
		self.texp=0
		self.nbtouch=0
		#Laser	
		self.laser1=Laser()
		self.laser2=Laser()
		self.laser3=Laser()
		self.tablaser=[self.laser1,self.laser2,self.laser3]
	
	def explose(self,fenetre,lasers,score):
		#Introduis un temps avant fin de l'explosion
		if(self.texp>=1):
                        self.texp+=1
                if self.texp>=30:
                        self.position_exp.center = 1300,70
			self.tla=0
		#Detecte la collision
		for i in range(0,len(lasers.tab)):
			if (self.position_boss.colliderect(lasers.tab[i].position_laser) and self.texp==0):
				#Termine le laser du vaisseau
				lasers.tab[i].tirer_fin(True)
				self.nbtouch+=1
				if self.nbtouch>=40:
					score.score+=5
					self.son_explosion.play()
					self.position_exp.center = self.position_boss.center
					self.texp+=1
					self.position_boss.center=1400,70
					break
		#Affiche l'explosion
		fenetre.blit(self.boss, self.position_boss)
		fenetre.blit(self.exp, self.position_exp)
	
	def tirer(self):
		self.laser1.tirer_deb(self.position_boss.x+227,self.position_boss.y+59,0)
		self.laser2.tirer_deb(self.position_boss.x+140,self.position_boss.y+122,0)
		self.laser3.tirer_deb(self.position_boss.x+22,self.position_boss.y+95,0)

	def deplacer(self):
		if self.position_boss.y<=0:
			self.sens=0
		if self.position_boss.y>=685:
			self.sens=1
		if self.tempo==3:
			if self.sens==1:
				self.position_boss = self.position_boss.move(0,-1)
			if self.sens==0:
				self.position_boss = self.position_boss.move(0,1)
			self.tempo=0
		self.tempo+=1
	
	def update(self,fenetre,lasers,score):
		self.deplacer()
		for i in range(0,len(self.tablaser)):
			self.tablaser[i].update()
		if self.tla==1:
			self.explose(fenetre,lasers,score)

	def affiche(self,fenetre):
		fenetre.blit(self.boss,(self.position_boss.x,self.position_boss.y))
		fenetre.blit(self.exp,(self.position_exp.x,self.position_exp.y))
		for i in range(0,len(self.tablaser)):
			self.tablaser[i].affiche(fenetre)

#Class du score
class Score:
		def __init__(self):
			self.score=0
			self.myfont = pygame.font.SysFont("monospace", 40)
		
		def plusun(self):
			self.score+=1
		
		def affiche(self,fenetre):
			self.label = self.myfont.render("Score = " + str(self.score), 1, (250,250,250))
			fenetre.blit(self.label, (490, 580))
			pygame.display.flip()
			time.sleep(5)
class GameOver:

		def __init__(self):
			self.image=pygame.image.load("data/game_over.jpg")

		def test(self,vais):
			if (vais.tla==1):
				return False
			else:
				return True
					
		def affiche(self,fenetre):
			fenetre.blit(self.image,(0,0))
			pygame.display.flip()
