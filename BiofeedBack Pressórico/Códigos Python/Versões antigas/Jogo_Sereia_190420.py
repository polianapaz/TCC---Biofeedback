########### BIBLIOTECAS ############
import pygame
from random import randint
import serial
import time
import pdb


############## CORES ###############
branco = [255,255,255]
azul= [0,0,255]
M_lin_col=[]
M_lin=[]
posimax=0
posimin=0
    

########### TESTE PYGAME ###########
try:
    pygame.init()
except:
    print("O modulo pygame não foi inicializado com sucesso")

############### TELA ###############
largura, altura, tamanho = pygame.display.Info().current_w, pygame.display.Info().current_h, pygame.display.Info().current_h/70
tela = pygame.display.set_mode((largura,altura))
tempo = pygame.time.Clock()
pygame.display.set_caption ("BIOFEEDBACK")
print(largura)

for i in range(36): #o range é 9 pois são 9 quadrantes, 0 até 8
    adicionar = []
    for j in range(36):
        larg=(largura//36)
        alt=(altura//36)
        adicionar.append([(largura//36)*j, (altura//36)*i,larg+(largura//36)*j,alt+(altura//36)*i,j,i])
    M_lin_col.append(adicionar)#linhas


##ser = serial.Serial('COM8', baudrate = 76900, timeout=0.01)

############### SONS ###############
GameOver_sound = pygame.mixer.Sound("sons/game_over1.wav")
GameOverPauseScreen_sound = pygame.mixer.Sound("sons/Undersea-Powerplant (online-audio-converter.com).wav")
Inicio_sound = pygame.mixer.Sound("sons/Bubble-Puzzle.wav")
new_record = pygame.mixer.Sound("sons/novo_record.wav")
colision_sound = pygame.mixer.Sound("sons/tapa.wav")
pygame.mixer.music.load("sons/the_little_mermai.wav")

print (altura)
class coluna(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemcoluna = pygame.transform.scale(pygame.image.load('imagens/coluna.png'), (int(largura/9), int(altura/1.5)))
        self.imagemcoluna2 = pygame.transform.scale(pygame.image.load('imagens/coluna.png'), (int(largura/9), int(altura/1.5)))
        self.rect1, self.rect2 = self.imagemcoluna.get_rect(), self.imagemcoluna2.get_rect()
        
    def show(self, tela, pos_x, pos_y):
            tela.blit(self.imagemcoluna, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x, pos_y

            tela.blit(self.imagemcoluna2, self.rect2) 
            self.rect2.centerx , self.rect2.centery = pos_x, pos_y+(altura//1.18) #espaço de 150 entre as colunas


class sereia(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemsereia = pygame.transform.scale(pygame.image.load('imagens/Ariel1.png'), (int(largura/4.7), int(altura/5.2)))
        self.imagemsereia2 = pygame.transform.scale(pygame.image.load('imagens/Ariel2.png'), (int(largura/4.7), int(altura/5.2)))
        self.rect = self.imagemsereia.get_rect()

    def show(self, tela, pos_x, pos_y, posicao):
        if posicao>0:
            tela.blit(self.imagemsereia2, self.rect)
            self.rect.centerx, self.rect.centery = pos_x, pos_y
        if posicao<0 or posicao==0:            
            tela.blit(self.imagemsereia, self.rect)
            self.rect.centerx, self.rect.centery = pos_x, pos_y   


class dead(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemsereia = pygame.transform.scale(pygame.image.load('imagens/Ariel_morta.png'), (int(largura/4.7), int(altura/5.2)))
        self.rect = self.imagemsereia.get_rect()
    def show(self, tela, pos_x, pos_y):
        tela.blit(self.imagemsereia, self.rect)
        self.rect.centerx, self.rect.centery = pos_x, pos_y


class letras(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemover = pygame.image.load('imagens/gameover.png')
        self.imagembio = pygame.transform.scale(pygame.image.load('imagens/biofeedback.png'), (int(largura/1.6), int(altura/3.5)))
        self.imagemcont = pygame.image.load('imagens/continuar_peq.png')
        self.imagempont = pygame.image.load('imagens/pontuação.png')
        self.imagemrec = pygame.image.load('imagens/record.png')
        self.imagemres = pygame.image.load('imagens/restart.png')
        self.imagemsair = pygame.transform.scale(pygame.image.load('imagens/sair.png'), (int(largura/8), int(altura/14)))
        self.imagemstart = pygame.transform.scale(pygame.image.load('imagens/start.png'), (int(largura/4), int(altura/6.5)))
        self.imagempause = pygame.image.load('imagens/pause.png')
        
        lets = [self.imagemover.get_rect(), self.imagembio.get_rect(), self.imagemcont.get_rect(), self.imagempont.get_rect(), self.imagemrec.get_rect()]
        lets2 = [self.imagemres.get_rect(), self.imagemsair.get_rect(), self.imagemstart.get_rect(), self.imagempause.get_rect()]

        self.rect1, self.rect2, self.rect3, self.rect4, self.rect5 = [retangulo for retangulo in lets]
        self.rect6, self.rect7, self.rect8, self.rect9 = [retangulo for retangulo in lets2]
        
    def show(self, tela, pos_x, pos_y, escolha):
        if escolha==1:
            tela.blit(self.imagemover, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x, pos_y
        if escolha==2:
            tela.blit(self.imagembio, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x, pos_y
        if escolha==3:
            tela.blit(self.imagemcont, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y
        if escolha==4:
            tela.blit(self.imagempont, self.rect4)
            self.rect4.centerx, self.rect4.centery = pos_x, pos_y
        if escolha==5:
            tela.blit(self.imagemrec, self.rect5)
            self.rect5.centerx, self.rect5.centery = pos_x, pos_y
        if escolha==6:
            tela.blit(self.imagemres, self.rect6)
            self.rect6.centerx, self.rect6.centery = pos_x, pos_y
        if escolha==7:
            tela.blit(self.imagemsair, self.rect7)
            self.rect7.centerx, self.rect7.centery = pos_x, pos_y
        if escolha==8:
            tela.blit(self.imagemstart, self.rect8)
            self.rect8.centerx, self.rect8.centery = pos_x, pos_y
        if escolha==9:
            tela.blit(self.imagempause, self.rect9)
            self.rect9.centerx, self.rect9.centery = pos_x, pos_y
    

class fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemfundo = pygame.transform.scale(pygame.image.load('imagens/fund2.png'), (int(largura+10), int(altura+10)))
        self.imagemfundo2 = pygame.transform.scale(pygame.image.load('imagens/fund1.png'), (int(largura+10), int(altura+10)))
        self.rect = self.imagemfundo.get_rect() #pega a imagem e associa a ela uma área retangular

    def show(self, tela, pos_x, pos_y, imagem):
        if imagem==1:
            tela.blit(self.imagemfundo, self.rect) #é preciso mandar o objeto e a área retangular
            self.rect.centerx, self.rect.centery = pos_x, pos_y
        if imagem==2:   
            tela.blit(self.imagemfundo2, self.rect)
            self.rect.centerx, self.rect.centery = pos_x, pos_y


class bubble (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagembolha = pygame.transform.scale(pygame.image.load('imagens/bolha_maior.png'), (int(largura/50), int(altura/30)))
        self.imagembolha2 = pygame.transform.scale(pygame.image.load('imagens/bolha_menor.png'), (int(largura/100), int(altura/80)))
        
        self.rect1 = self.imagembolha.get_rect()
        self.rect2 = self.imagembolha2.get_rect()
        
    def show(self, tela, pos_x, pos_y, nova):
        tela.blit(self.imagembolha, self.rect1)
        self.rect1.centerx, self.rect1.centery = pos_x+nova+400, pos_y+45+nova
        tela.blit(self.imagembolha2, self.rect2)
        self.rect2.centerx, self.rect2.centery = pos_x+200+nova, pos_y+11
        tela.blit(self.imagembolha, self.rect1)
        self.rect1.centerx, self.rect1.centery = pos_x-100+nova, pos_y+150+nova
        tela.blit(self.imagembolha2, self.rect2)
        self.rect2.centerx, self.rect2.centery = pos_x+nova, pos_y+62+nova
        tela.blit(self.imagembolha2, self.rect2)
        self.rect2.centerx, self.rect2.centery = pos_x-300+nova, pos_y+39
        tela.blit(self.imagembolha, self.rect1)
        self.rect1.centerx, self.rect1.centery = pos_x-400+nova, pos_y+130+nova


class fish (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagempeixe1 = pygame.transform.scale(pygame.image.load('imagens/peixe3.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe2 = pygame.transform.scale(pygame.image.load('imagens/peixe5.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe3 = pygame.transform.scale(pygame.image.load('imagens/baleia.png'), (int(largura/3), int(altura/2)))
        self.imagempeixe4 = pygame.transform.scale(pygame.image.load('imagens/peixe1.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe5 = pygame.transform.scale(pygame.image.load('imagens/peixe2.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe6 = pygame.transform.scale(pygame.image.load('imagens/peixe4.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe7 = pygame.transform.scale(pygame.image.load('imagens/peixe6.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe8 = pygame.transform.scale(pygame.image.load('imagens/peixe8.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe9 = pygame.transform.scale(pygame.image.load('imagens/peixe7.png'), (int(largura/50), int(altura/30)))
        self.imagempeixe10 = pygame.transform.scale(pygame.image.load('imagens/peixe9.png'), (int(largura/50), int(altura/30)))

        peixes = [self.imagempeixe1.get_rect(), self.imagempeixe2.get_rect(), self.imagempeixe3.get_rect(), self.imagempeixe4.get_rect(), self.imagempeixe5.get_rect()]
        peixes2 = [self.imagempeixe6.get_rect(), self.imagempeixe7.get_rect(), self.imagempeixe8.get_rect(), self.imagempeixe9.get_rect(), self.imagempeixe10.get_rect()]

        self.rect1, self.rect2, self.rect3, self.rect4, self.rect5 = [retangulo for retangulo in peixes]
        self.rect6, self.rect7, self.rect8, self.rect9, self.rect10 = [retangulo for retangulo in peixes2]

    def show(self, tela, pos_x, pos_y, nova, escolha):
        if escolha<=1:
            tela.blit(self.imagempeixe1, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x-10, pos_y+150+nova
        if escolha==2:
            tela.blit(self.imagempeixe2, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x-15, pos_y-150+nova
        if escolha==3:
            tela.blit(self.imagempeixe3, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y+150+nova
        if escolha==4:
            tela.blit(self.imagempeixe4, self.rect4)
            self.rect4.centerx, self.rect4.centery = pos_x-50, pos_y-150+nova
        if escolha==5:
            tela.blit(self.imagempeixe5, self.rect5)
            self.rect5.centerx, self.rect5.centery = pos_x-100, pos_y+150+nova
        if escolha==6:
            tela.blit(self.imagempeixe6, self.rect6)
            self.rect6.centerx, self.rect6.centery = pos_x-20, pos_y-150+nova
        if escolha==7:
            tela.blit(self.imagempeixe7, self.rect7)
            self.rect7.centerx, self.rect7.centery = pos_x-70, pos_y+150+nova
        if escolha==8:
            tela.blit(self.imagempeixe8, self.rect8)
            self.rect8.centerx, self.rect8.centery = pos_x-150, pos_y-150+nova
        if escolha==9:
            tela.blit(self.imagempeixe9, self.rect9)
            self.rect9.centerx, self.rect9.centery = pos_x-120, pos_y+150+nova
        if escolha>=10:
            tela.blit(self.imagempeixe10, self.rect10)
            self.rect10.centerx, self.rect10.centery = pos_x, pos_y-150+nova


class numeros (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem0 = pygame.image.load('imagens/0.png')
        self.imagem1 = pygame.image.load('imagens/1.png')
        self.imagem2 = pygame.image.load('imagens/2.png')
        self.imagem3 = pygame.image.load('imagens/3.png')
        self.imagem4 = pygame.image.load('imagens/4.png')
        self.imagem5 = pygame.image.load('imagens/5.png')
        self.imagem6 = pygame.image.load('imagens/6.png')
        self.imagem7 = pygame.image.load('imagens/7.png')
        self.imagem8 = pygame.image.load('imagens/8.png')
        self.imagem9 = pygame.image.load('imagens/9.png')

        num = [self.imagem0.get_rect(), self.imagem1.get_rect(), self.imagem2.get_rect(), self.imagem3.get_rect(), self.imagem4.get_rect(),
        self.imagem5.get_rect(), self.imagem6.get_rect(), self.imagem7.get_rect(), self.imagem8.get_rect(), self.imagem9.get_rect()]
        self.rect0, self.rect1, self.rect2, self.rect3, self.rect4, self.rect5, self.rect6, self.rect7, self.rect8, self.rect9 = [retangulo for retangulo in num]
        
    def show(self, tela, pos_x, pos_y, caracter):
      
        if caracter==0:
            tela.blit(self.imagem0, self.rect0)
            self.rect0.centerx, self.rect0.centery = pos_x, pos_y
        if caracter==1:
            tela.blit(self.imagem1, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x, pos_y
        if caracter==2:
            tela.blit(self.imagem2, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x, pos_y
        if caracter==3:
            tela.blit(self.imagem3, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y
        if caracter==4:
            tela.blit(self.imagem4, self.rect4)
            self.rect4.centerx, self.rect4.centery = pos_x, pos_y
        if caracter==5:
            tela.blit(self.imagem5, self.rect5)
            self.rect5.centerx, self.rect5.centery = pos_x, pos_y
        if caracter==6:
            tela.blit(self.imagem6, self.rect6)
            self.rect6.centerx, self.rect6.centery = pos_x, pos_y
        if caracter==7:
            tela.blit(self.imagem7, self.rect7)
            self.rect7.centerx, self.rect7.centery = pos_x, pos_y
        if caracter==8:
            tela.blit(self.imagem8, self.rect8)
            self.rect8.centerx, self.rect8.centery = pos_x, pos_y
        if caracter==9:
            tela.blit(self.imagem9, self.rect9)
            self.rect9.centerx, self.rect9.centery = pos_x, pos_y
            



class letr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.imagemA = pygame.transform.scale(pygame.image.load('imagens/A.png'), (int(largura/10), int(altura/6)))
        self.imagemB = pygame.transform.scale(pygame.image.load('imagens/B.png'), (int(largura/10), int(altura/6)))
        self.imagemC = pygame.transform.scale(pygame.image.load('imagens/C.png'), (int(largura/10), int(altura/6)))
        self.imagemD = pygame.transform.scale(pygame.image.load('imagens/D.png'), (int(largura/10), int(altura/6)))
        self.imagemE = pygame.transform.scale(pygame.image.load('imagens/E.png'), (int(largura/10.5), int(altura/6)))
        self.imagemF = pygame.transform.scale(pygame.image.load('imagens/F.png'), (int(largura/10), int(altura/6)))
        self.imagemG = pygame.transform.scale(pygame.image.load('imagens/G.png'), (int(largura/10), int(altura/6)))
        self.imagemH = pygame.transform.scale(pygame.image.load('imagens/H.png'), (int(largura/10), int(altura/6)))
        self.imagemI = pygame.transform.scale(pygame.image.load('imagens/I.png'), (int(largura/10), int(altura/6)))
        self.imagemJ = pygame.transform.scale(pygame.image.load('imagens/J.png'), (int(largura/10), int(altura/6)))
        self.imagemK = pygame.transform.scale(pygame.image.load('imagens/K.png'), (int(largura/10), int(altura/6)))
        self.imagemL = pygame.transform.scale(pygame.image.load('imagens/L.png'), (int(largura/10), int(altura/6)))
        self.imagemM = pygame.transform.scale(pygame.image.load('imagens/M.png'), (int(largura/10), int(altura/6)))
        self.imagemN = pygame.transform.scale(pygame.image.load('imagens/N.png'), (int(largura/10), int(altura/6)))
        self.imagemO = pygame.transform.scale(pygame.image.load('imagens/O.png'), (int(largura/10), int(altura/6)))
        self.imagemP = pygame.transform.scale(pygame.image.load('imagens/P.png'), (int(largura/10), int(altura/6)))
        self.imagemQ = pygame.transform.scale(pygame.image.load('imagens/Q.png'), (int(largura/10), int(altura/6)))
        self.imagemR = pygame.transform.scale(pygame.image.load('imagens/R.png'), (int(largura/10), int(altura/6)))
        self.imagemS = pygame.transform.scale(pygame.image.load('imagens/S.png'), (int(largura/10), int(altura/6)))
        self.imagemT = pygame.transform.scale(pygame.image.load('imagens/T.png'), (int(largura/10), int(altura/6)))
        self.imagemU = pygame.transform.scale(pygame.image.load('imagens/U.png'), (int(largura/10), int(altura/6)))
        self.imagemV = pygame.transform.scale(pygame.image.load('imagens/V.png'), (int(largura/10), int(altura/6)))
        self.imagemW = pygame.transform.scale(pygame.image.load('imagens/W.png'), (int(largura/10), int(altura/6)))
        self.imagemX = pygame.transform.scale(pygame.image.load('imagens/X.png'), (int(largura/10), int(altura/6)))
        self.imagemY = pygame.transform.scale(pygame.image.load('imagens/Y.png'), (int(largura/10), int(altura/6)))
        self.imagemZ = pygame.transform.scale(pygame.image.load('imagens/Z.png'), (int(largura/10), int(altura/6)))
        
        let = [self.imagemA.get_rect(), self.imagemB.get_rect(), self.imagemC.get_rect(), self.imagemD.get_rect(), self.imagemE.get_rect(),
        self.imagemF.get_rect(), self.imagemG.get_rect(), self.imagemH.get_rect(), self.imagemI.get_rect(), self.imagemJ.get_rect(), self.imagemK.get_rect(),
        self.imagemL.get_rect(),self.imagemM.get_rect(),self.imagemN.get_rect(),self.imagemO.get_rect(),self.imagemP.get_rect(),self.imagemQ.get_rect(),
        self.imagemR.get_rect(),self.imagemS.get_rect(), self.imagemT.get_rect(), self.imagemU.get_rect(), self.imagemV.get_rect(), self.imagemW.get_rect(),
        self.imagemX.get_rect(), self.imagemY.get_rect(), self.imagemZ.get_rect() ]
        self.rectA, self.rectB, self.rectC, self.rectD, self.rectE, self.rectF, self.rectG, self.rectH, self.rectI, self.rectJ, self.rectK, self.rectL, self.rectM, self.rectN,self.rectO, self.rectP,self.rectQ, self.rectR,self.rectS, self.rectT, self.rectU, self.rectV, self.rectW, self.rectX,self.rectY, self.rectZ = [retangulo for retangulo in let]
        
    def show(self, tela, quad_x, quad_y, palavra):
        cont=0
        pos_y= int(posicao(quad_x,quad_y,"y"))
        for caracter in palavra:
            cont=cont+1
            if caracter=='A':
                tela.blit(self.imagemA, self.rectA)
                self.rectA.centerx, self.rectA.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='B':
                tela.blit(self.imagemB, self.rectB)
                self.rectB.centerx, self.rectB.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='C':
                tela.blit(self.imagemC, self.rectC)
                self.rectC.centerx, self.rectC.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='D':
                tela.blit(self.imagemD, self.rectD)
                self.rectD.centerx, self.rectD.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='E':
                tela.blit(self.imagemE, self.rectE)
                self.rectE.centerx, self.rectE.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y+3
            if caracter=='F':
                tela.blit(self.imagemF, self.rectF)
                self.rectF.centerx, self.rectF.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='G':
                tela.blit(self.imagemG, self.rectG)
                self.rectG.centerx, self.rectG.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='H':
                tela.blit(self.imagemH, self.rectH)
                self.rectH.centerx, self.rectH.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y    
            if caracter=='I':
                tela.blit(self.imagemI, self.rectI)
                self.rectI.centerx, self.rectI.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='J':
                tela.blit(self.imagemJ, self.rectJ)
                self.rectJ.centerx, self.rectJ.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='K':
                tela.blit(self.imagemK, self.rectK)
                self.rectK.centerx, self.rectK.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='L':
                tela.blit(self.imagemL, self.rectL)
                self.rectL.centerx, self.rectL.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='M':
                tela.blit(self.imagemM, self.rectM)
                self.rectM.centerx, self.rectM.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='N':
                tela.blit(self.imagemN, self.rectN)
                self.rectN.centerx, self.rectN.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='O':
                tela.blit(self.imagemO, self.rectO)
                self.rectO.centerx, self.rectO.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='P':
                tela.blit(self.imagemP, self.rectP)
                self.rectP.centerx, self.rectP.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='Q':
                tela.blit(self.imagemQ, self.rectQ)
                self.rectQ.centerx, self.rectQ.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='R':
                tela.blit(self.imagemR, self.rectR)
                self.rectR.centerx, self.rectR.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='S':
                tela.blit(self.imagemS, self.rectS)
                self.rectS.centerx, self.rectS.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='T':
                tela.blit(self.imagemT, self.rectT)
                self.rectT.centerx, self.rectT.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='U':
                tela.blit(self.imagemU, self.rectU)
                self.rectU.centerx, self.rectU.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='V':
                tela.blit(self.imagemV, self.rectV)
                self.rectV.centerx, self.rectV.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='W':
                tela.blit(self.imagemW, self.rectW)
                self.rectW.centerx, self.rectW.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='X':
                tela.blit(self.imagemX, self.rectX)
                self.rectX.centerx, self.rectX.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='Y':
                tela.blit(self.imagemY, self.rectY)
                self.rectY.centerx, self.rectY.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter=='Z':
                tela.blit(self.imagemZ, self.rectZ)
                self.rectZ.centerx, self.rectZ.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y
            if caracter==' ':
                cont=cont+0.001

     
class coral (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemcor1 = pygame.transform.scale(pygame.image.load('imagens/alga.png'), (int(largura/7), int(altura/5)))
        self.imagemcor2 = pygame.image.load('imagens/concha_pausa.png')
        self.imagemcor3 = pygame.image.load('imagens/concha_musica.png')
        
        self.rect1, self.rect2, self.rect3 = self.imagemcor1.get_rect(), self.imagemcor2.get_rect(), self.imagemcor3.get_rect()
        
    def show(self, tela, pos_x, pos_y, escolha):
        if escolha==1:
            tela.blit(self.imagemcor1, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x, pos_y
        if escolha==2:
            tela.blit(self.imagemcor2, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x, pos_y
        if escolha==3:
            tela.blit(self.imagemcor3, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y

def posicao(quad_x,quad_y, eixo):
    M_lin=M_lin_col[quad_y] #recebe uma lista da lista que contem todas as posições de todos os quadrantes da linha
    posi=M_lin[quad_x] #recebe a posição de um quadrante especifico da linha, ou seja, a coluna desejada   
    if eixo == 'x':
        return((posi[0]+posi[2])/2)
    if eixo == 'y':
        return((posi[1]+posi[3])/2)




def recorde(pontos):
    placar=pontos

    with open ("recorde/Recorde", "r") as arquivo:
        cont=arquivo.readlines()
    ##arquivo vazio
    if len(cont)==0:
        with open("recorde/Recorde", "w") as arquivo:
            arquivo.write("%d\n" %placar)
    elif int(cont[0])<=placar:
        with open ("recorde/Recorde", "w") as arquivo:
            arquivo.write("%d\n" %placar)
            pygame.mixer.Sound.play(new_record)

def melhor_pont():
    with open ("recorde/Recorde", "+a") as arquivo:
        with open ("recorde/Recorde", "r") as arquivo:
            cont=arquivo.readlines()
    
    ##arquivo vazio
    if len(cont)==0 or cont[0]=="\n":
        with open ("recorde/Recorde", "w") as arquivo:
            arquivo.write('0\n')
            cont=0
        return(cont)
    return(int(cont[0]))


def gameover(pontos):
    
    pos_buble_y=700

    inter1=[(-100,350), (-100,300), (-100,300)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter1]
    
    let, let2, let3, let4, let5, col, cor, morta, fund, bolhas = letras(), letras(), letras(), letras(), letras(), coluna(), coral(), dead(), fundo(), bubble()
    dez, uni, rec_dez, rec_uni, recorde = numeros(), numeros(), numeros(), numeros(), melhor_pont()
    
    GO, parada = True, True

    pygame.mixer.Sound.play(GameOver_sound)
    pygame.mixer.Sound.play(GameOverPauseScreen_sound, loops = -1)
    
    while GO and parada:

        mouse=pygame.mouse.get_pos() #pos=[x,y]
        click=pygame.mouse.get_pressed()
        
        ###### INTERFACE ###
        fund.show(tela, 440, 350, 1)
        let.show(tela, 400, 100, 1) #GameOver
        let2.show(tela, 250, 550, 8) # 200 X 84 START
        let3.show(tela, 550, 550, 7) # 126 X 40 SAIR
        let4.show(tela, 400, 200, 4) #Pontuação
        let5.show(tela, 400, 400, 5) #Recorde
        cor.show(tela, 980, 205, 1)
        cor.show(tela, 220, 205, 1)
        col.show(tela, 780, 500)
        col.show(tela, 20, 500)

        ################
        dez.show(tela, 389, 280, pontos//10)
        uni.show(tela, 411, 280, pontos%10)

        rec_dez.show(tela, 389, 470, recorde//10)
        rec_uni.show(tela, 411, 470, recorde%10)

        ###################ALEATORIEDADE DAS BOLHAS
        if pos_buble_y==700:
            nova=randint(-300,300)
            nova2=randint(-300,300)
        if pos_buble_y<-2050:
            pos_buble_y=800
        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5
        morta.show(tela, 400, 550)

        ################# BOTÕES ##########################
        ##botão_1 = START
        if 150 < mouse[0] < 350 and 508 < mouse[1] < 592 and click[0] == 1:
            pygame.mixer.Sound.stop(GameOverPauseScreen_sound)
            pygame.mixer.music.play(-1)
            ser.reset_input_buffer()
            return(True)
            parada=False
                
        #botao_2 = SAIR
        if  487 < mouse[0] < 613 and 530 < mouse[1] < 570 and click[0] == 1:
            return(False)
            parada=False
        
    ############SAIDA
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return(False)
    return(True)


def inicio():

    ## TODAS AS IMAGENS DEVEM SER CARREGADAS ANTES DO LOOP PARA EVITAR QUE ELAS APAREÇAM EM POSICOES ERRADAS NO INICIO DA FUNCAO
    inter=[(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
  
    
    pos_buble_y, let, let2, let3, let4, col, cor = 700, letras(), letras(), letras(), letras(), coluna(), coral()
    ariel, fund, bolhas, pontos, dez, uni = sereia(), fundo(), bubble(), melhor_pont(), numeros(), numeros()
    teste, teste2=letr(),letr()
    pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    ##### CARREGANDO TODAS AS IMAGENS UTILIZADAS NA FUNÇÂO####
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    teste2.show(tela, 2,12, "REALIZAR A TARAGEM")
    teste2.show(tela, 2,15, "ANTES DE CONTINUAR")
    let.show(tela, posicao(18,3,"x"), posicao(18,3,"y"), 2)
    cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
    cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
    col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
    col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
    ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), -10)
    ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), 10)
    teste.show(tela, 11,11, "TARAGEM")
    teste.show(tela, 14,16, "MODO")
    teste.show(tela,14,21, "SAIR")
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    pygame.display.update()
    menu=True

    while menu:
        ###### INTERFACE FUNDO ###
        fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
        #let4.show(tela, 400, 280, 5) #Recorde
        cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
        cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
        col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
        col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
        ################
        #dez.show(tela, 389, 320, pontos//10)
        #uni.show(tela, 411, 320, pontos%10)
        ###################ALEATORIEDADE DAS BOLHAS
        #####FUNCAO PARA ESCREVER TEXTOS####
        #teste.show(tela, 9,3, "BIOFEEDBACK")
        teste.show(tela, 11,11, "TARAGEM")
        teste.show(tela, 14,16, "MODO")
        teste.show(tela,14,21, "SAIR")
        
        ################################
        if pos_buble_y==altura:
            nova=randint(-300,300)
            nova2=randint(-300,300)
            
        if pos_buble_y<-altura*1.5:
            pos_buble_y=altura-((altura%100)%10)

        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5

        ###### INTERFACE LETRAS #############
        
        let.show(tela, posicao(18,3,"x"), posicao(18,3,"y"), 2) #Biofeedback
        #let2.show(tela,posicao(18,11,"x"), posicao(18,11,"y"), 8) # 200 X 84 START
        #let3.show(tela,posicao(18,16,"x"), posicao(18,16,"y"), 7) # 126 X 40 SAIR

        ########## POSICAO E MOVIMENTO DA SEREIA #######
        if (pos_buble_y%15)==0:
            posi=10
        else:
            posi=0
        ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), posi)
        
            

        mouse=pygame.mouse.get_pos() #pos=[x,y]
        click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu=False
        ##botão_1 = TARAGEM
        if menu:
            if posicao(14,9,"x") < mouse[0] < posicao(22,12,"x") and posicao(14,9,"y") < mouse[1] < posicao(22,12,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                menu=taragem()

            ##botao_2 = MODO
        if menu:
            if posicao(14,15,"x") < mouse[0] < posicao(19,15,"x") and posicao(14,15,"y") < mouse[1] < posicao(14,17,"y") and click[0] == 1:
                #menu=False
##                if posimin==0 or posimax==0:
##                    pygame.display.update()
##                    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
##                    teste2.show(tela, 2,12, "REALIZAR A TARAGEM")
##                    teste2.show(tela, 2,15, "ANTES DE CONTINUAR")
##                    pygame.display.update()
##                    time.sleep(3)
##                    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
##                    menu=inicio()
##                else:
##                    menu=modo()
                menu=modo()
        if menu:
            if posicao(14,15,"x") < mouse[0] < posicao(21,15,"x") and posicao(14,20,"y") < mouse[1] < posicao(14,22,"y") and click[0] == 1:
                menu=False    
                    
        
        pygame.display.update()

def modo():
    
    inter=[(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
  
    
    pos_buble_y, col, cor = 700, coluna(), coral()
    fund, bolhas = fundo(), bubble()
    teste, teste2=letr(),letr()
    pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
    cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
    col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
    col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
    
    teste.show(tela, 5,11, "CONTRACAO TONICA")
    teste.show(tela, 2,16, "TRABALHO ASCENDENTE")
    teste.show(tela, 9,21, "RELAXAMENTO")
    teste.show(tela, 2,26, "TRABALHO ISOMETRICO")
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    pygame.display.update()
    mod=True

    while mod:
        ###### INTERFACE FUNDO ###
        fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
        cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
        cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
        col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
        col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
        
        teste.show(tela, 5,11, "CONTRACAO TONICA")
        teste.show(tela, 2,16, "TRABALHO ASCENDENTE")
        teste.show(tela, 9,21, "RELAXAMENTO")
        teste.show(tela, 2,26, "TRABALHO ISOMETRICO")

        ################################
        if pos_buble_y==altura:
            nova=randint(-300,300)
            nova2=randint(-300,300)
            
        if pos_buble_y<-altura*1.5:
            pos_buble_y=altura-((altura%100)%10)

        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5        
            

        mouse=pygame.mouse.get_pos() #pos=[x,y]
        click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mod=False
        ##botão_1 = CONTRACAO TONICA
        if mod:
            if posicao(11,9,"x") < mouse[0] < posicao(27,12,"x") and posicao(14,9,"y") < mouse[1] < posicao(22,12,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                graf=1
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                mod=grafico(graf)

        ##botao_2 = TRABALHO ASCENDENTE
        if mod:
            if posicao(11,15,"x") < mouse[0] < posicao(30,15,"x") and posicao(14,15,"y") < mouse[1] < posicao(14,17,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                graf=2
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                mod=grafico(graf)

        ##botao_3 = RELAXAMENTO
        if mod:
            if posicao(11,9,"x") < mouse[0] < posicao(27,12,"x") and posicao(20,20,"y") < mouse[1] < posicao(22,22,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                graf=3
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                mod=grafico(graf)

        ##botao_4 = TRABALHO ISOMETRICO
        if mod:
            if posicao(11,9,"x") < mouse[0] < posicao(30,12,"x") and posicao(14,25,"y") < mouse[1] < posicao(22,27,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                graf=4
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                mod=grafico(graf)                   
                        
        
        pygame.display.update()

def taragem():

    global posimax
    global posimin
    inter=[(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    cont =  [letras()]*6 + [numeros()]*6 + [coluna(), coral(), sereia(), fundo(), bubble(), melhor_pont(), 700,350,350,0, 0,0,0,altura, True]
    pmax1, pmax2, pmax3, pmin1, pmin2, pmin3, posimaxcen, posimaxdez, posimaxuni, posimincen, posimindez, posiminuni,col, cor, ariel, fund, bolhas, pontos, pos_buble_y, posi, posi2, contagem2, contagem3, check, posimax, posimin, tara = [i for i in cont] 
    uni=numeros()
    test, test2, test3=letr(),letr(),letr()
    
    tara=True
    test.show(tela, 5,12, "CONTRAIA O MAXIMO")
    test2.show(tela, 5,12, "RELAXE O MAXIMO")
    test3.show(tela, 8,15, "QUE PUDER")
    test3.show(tela, 3,5, "MAX")  
    test3.show(tela, 3,11, "MIN")
    cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
    col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
    ariel.show(tela, -100, -100, 0)
    for conta in range(0,9):
        uni.show(tela, int(largura/2), int(altura/2), conta)
        posimaxcen.show(tela, -100, -100, conta)
        posimaxdez.show(tela, -100, -100, conta)
        posimaxuni.show(tela, -100, -100, conta)
        posimincen.show(tela, -100, -100, conta)
        posimindez.show(tela, -100, -100, conta)
        posiminuni.show(tela, -100, -100, conta)
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    pygame.display.update()
    
    while tara:
       
        while (contagem2<=10):
            fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
            cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
            cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
            col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
            col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
            if contagem2==0 and check==0:
                for contagem in range(3,0,-1):
                    startcont=time.time()
                    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)    
                    while time.time()-startcont<1:
                        uni.show(tela, int(largura/2), int(altura/2), contagem)
                        pygame.display.update()
                startcont=time.time()
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                while time.time()-startcont<4:
                    test.show(tela, 5,12, "CONTRAIA O MAXIMO")
                    test3.show(tela, 8,15, "QUE PUDER")
                    pygame.display.update()
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                check=1
                start=time.time()        
            test3.show(tela, 3,5, "MAX")
            if pos_buble_y==altura:
                nova=randint(-300,300)
                nova2=randint(-300,300)
                
            if pos_buble_y<-altura*1.5:
                pos_buble_y=altura-((altura%100)%10)

            bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
            bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
            bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
            pos_buble_y-=5
            
            #pmax.show()
            #pmin.show()
            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)
            posi=posi-50
            if posi==100:
                posi=700
            if (pos_buble_y%15)==0:
                escolha=10
            else:
                escolha=0
            ariel.show(tela, posicao(18,18,"x"), posi, escolha)
            if posi>posimax:
                posimax=posi
            if posi<posimin:
                posimin=posi  
            posimaxcen.show(tela, posicao(5,8,"x"), posicao(3,8,"y"), posimax//100)
            posimaxdez.show(tela, posicao(6,8,"x"), posicao(3,8,"y"), (posimax%100)//10)
            posimaxuni.show(tela, posicao(7,8,"x"), posicao(3,8,"y"), (posimax%100)%10)
          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False                
            contagem2=time.time()-start
            pygame.display.update()
            #tempo.tick(10)  
        check=0
        while (contagem3<=12):
            fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
            cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
            cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
            col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
            col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
            if contagem3==0 and check==0:
                for contagem in range(3,0,-1):
                    startcont=time.time()
                    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)    
                    while time.time()-startcont<1:
                        uni.show(tela, int(largura/2), int(altura/2), contagem)
                        pygame.display.update()
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                startcont=time.time()
                while time.time()-startcont<4:
                    test2.show(tela, 5,12, "RELAXE O MAXIMO")
                    test3.show(tela, 8,15, "QUE PUDER")
                    pygame.display.update()
                check=1
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                start=time.time() 
            test3.show(tela, 3,5, "MAX")
            test3.show(tela, 3,11, "MIN")             
            if pos_buble_y==altura:
                nova=randint(-300,300)
                nova2=randint(-300,300)
                
            if pos_buble_y<-altura*1.5:
                pos_buble_y=altura-((altura%100)%10)

            bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
            bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
            bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
            pos_buble_y-=5
            

            #pmax.show()
            #pmin.show()
            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)
            posi2=posi2-50
            if posi2<=100:
                posi2=700
            if (pos_buble_y%15)==0:
                escolha=10
            else:
                escolha=0
            ariel.show(tela, posicao(18,18,"x"), posi2, escolha)
            if posi2>posimax:
                posimax2=posi
            if posi2<posimin:
                posimin=posi2
            
            posimaxcen.show(tela, posicao(5,8,"x"), posicao(5,8,"y"), posimax//100)
            posimaxdez.show(tela, posicao(6,8,"x"), posicao(6,8,"y"), (posimax%100)//10)
            posimaxuni.show(tela, posicao(7,8,"x"), posicao(7,8,"y"), (posimax%100)%10) 
            posimincen.show(tela,  posicao(5,14,"x"), posicao(5,14,"y"), posimin//100)
            posimindez.show(tela,  posicao(6,14,"x"), posicao(6,14,"y"), (posimin%100)//10)
            posiminuni.show(tela, posicao(7,14,"x"), posicao(7,14,"y"), (posimin%100)%10)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False
            contagem3=time.time()-start 

        pygame.display.update()
        tara=inicio()
        
        #tempo.tick(10)


def pause(pontos):

    pos_buble_y=700
    
    inter2=[(-100,350), (-100,300), (-100,300)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter2]
    
    let, let2, let3, let4, let5, col = letras(), letras(), letras(), letras(), letras(), coluna() 
    cor, fund, bolhas, dez, uni = coral(), fundo(), bubble(), numeros(), numeros()

    parada, pausa = True, 1

    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(GameOverPauseScreen_sound, loops = -1)
    
    while parada:
        ###### INTERFACE ### NAO MEXE NAS POSICOES,ELAS NAO FAZEM MUITO SENTIDO
        fund.show(tela, 440, 350, 1)
        let.show(tela, 400, 100, 9) #PAUSE
        let2.show(tela, 550, 550, 6) # 200 X 84 restart
        let3.show(tela, 250, 550, 3) # 106 X 16 continuar
        let4.show(tela, 400, 280, 4) #Pontuação
        cor.show(tela, 980, 205, 1)
        cor.show(tela, 220, 205, 1)
        col.show(tela, 780, 500)
        col.show(tela, 20, 500)
        dez.show(tela, 389, 320, pontos//10)
        uni.show(tela, 411, 320, pontos%10)

        mouse=pygame.mouse.get_pos() #pos=[x,y]
        click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pausa=0
                return(pausa)
                parada=False
                
        ##botão_1 = CONTINUAR
        if 152 < mouse[0] < 348 and 537 < mouse[1] < 563 and click[0] == 1:
            pausa=1
            pygame.mixer.Sound.stop(GameOverPauseScreen_sound)
            pygame.mixer.music.unpause()
            ser.reset_input_buffer()
            return(pausa)
            parada=False

        ##botao_2 = RESTART
        if 472 < mouse[0] < 628 and 537 < mouse[1] < 563 and click[0] == 1:
            pausa=2
            pygame.mixer.Sound.stop(GameOverPauseScreen_sound)
            pygame.mixer.music.play(-1)
            ser.reset_input_buffer()
            return(pausa)
            parada=False
        
        pygame.display.update()

def pausar_som(music_state):
    pygame.time.wait(150)
    if music_state:
        pygame.mixer.music.stop()
        return(False)
    if music_state==False:
        pygame.mixer.music.play(-1)
        return(True)   

def grafico(graf):
    
    pos_y, pos_x, velocidade_y, larg, pos_yf, pos_xf, pos_xf2 = 350, 250, 0, largura-((largura%100)%10)+80, 350, 410, 1487
    pos_obs_x, pos_obs_x2, pos_obs_x3, velocidade_obs = larg, larg, larg, 40

    pos_buble_x=randint(-100,350)
    pos_buble_y, pos_peix_x, pos_peix_y = 700, -100, 350
    lims = [(-100, 300), (-100, 300), (-100, 300), (1, 10), (-400, 200), (1, 10), (-160, 100), (-160, 100), (-160, 100)]
    nova, nova2, novapeixe, escolhapeixe, novapeixe2, escolhapeixe2, pos_obs_y, pos_obs_y2, pos_obs_y3 = [randint(*pair) for pair in lims]

    sair, pontos, pausa, musica, colidiu = True, 0, 1, True, 0

    #player funciona
    if musica:
        pygame.mixer.music.play(-1)
        
        
    #ser.reset_input_buffer()
#####################################
    classes = [sereia(), bubble(), fundo(), fundo(), fish(), dead(), coluna(), coluna(), coluna(), coral(), coral(), coral(), numeros(), numeros(), letras()]
    ariel, bolhas, fund1, fund2, peixe, morta, obs1, obs2, obs3, pause_bt, musica_bt, musica_simb, dez, uni, let = [pair for pair in classes]
#####################################
    for conta in range(0,9):
        dez.show(tela, -100, -100, conta)
        uni.show(tela, -100, -100, conta)
        peixe.show(tela, -100, -100, -100,conta)
    obs1.show(tela, -80,-80)
    obs2.show(tela, -80,-80)
    obs3.show(tela, -80,-80)
    ariel.show(tela, -30, -30, -10)
    ariel.show(tela, -30, -30, 10)
    let.show(tela, -30, -30, 4)
    pause_bt.show(tela, -100, -100, 2)
    musica_bt.show(tela, -100, -100, 3)
    fund1.show(tela, pos_xf,pos_yf, 1)
    fund2.show(tela,pos_xf2, pos_yf, 2)
    contagem=0
    iniciocontag=time.time()
    while sair:

######################### FUNDO ###############################
        fund1.show(tela, int(largura//2), int(altura//2), 1)
        #fund2.show(tela, pos_xf2, int(altura//2), 2)
        
        pos_xf = 1487 if pos_xf2 == 410 else pos_xf - 1
        pos_xf2 = 1487 if pos_xf == 410 else pos_xf2 -1

################### ALEATORIEDADE DAS BOLHAS ################
        if pos_buble_y == 700:
            nova, nova2 = randint(-300,300), randint(-300,300)
        if pos_buble_y < -2050:
            pos_buble_y = 800
        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5

####################PEIXES

        if pos_peix_x == -100:
            aleatorio = [(-400, 300), (-400, 300), (1, 5), (1, 5)]
            novapeixe, novapeixe2, escolhapeixe, escolhapeixe2 = [randint(*pair) for pair in aleatorio]
        if pos_peix_x>1000:
            pos_peix_x=-300
            
        peixe.show(tela, pos_peix_x, pos_peix_y, novapeixe, escolhapeixe)
        peixe.show(tela, pos_peix_x*1.5, pos_peix_y, novapeixe2+novapeixe, escolhapeixe2-escolhapeixe)
        peixe.show(tela, pos_peix_x*1.10, pos_peix_y, novapeixe2, escolhapeixe2)
        peixe.show(tela, pos_peix_x*1.25, pos_peix_y, novapeixe2-novapeixe, escolhapeixe2+escolhapeixe)
        peixe.show(tela, pos_peix_x*1.05, pos_peix_y, novapeixe-150, escolhapeixe+2)
        peixe.show(tela, pos_peix_x*1.45, pos_peix_y, novapeixe2+novapeixe-20, escolhapeixe2-escolhapeixe+1)
        peixe.show(tela, pos_peix_x*1.15, pos_peix_y, novapeixe2-150, escolhapeixe2+2)
        peixe.show(tela, pos_peix_x*1.30, pos_peix_y, novapeixe2-novapeixe+200, escolhapeixe2+escolhapeixe+1)
    
        pos_peix_x+=1


####### LIMITAÇÃO DE MOVIMENTOS #################

        if pos_y<10:
            pos_y+=20

        if pos_y>=altura-10: 
            pos_y-=10
        
####### CONTROLE DE MOVIMENTOS DO OBSTÁCULO #################

    ######### CONTRACAO TONICA
        
        if graf==1:
            if contagem>60:
                sair=inicio()
            if contagem>=0 and contagem<20:
                if contagem==0.00:
                    pos_obs_y= altura/2 - 0.5*altura*contagem/20
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=velocidade_obs

                if pos_obs_x>=(largura-((largura%100)%10))/1.7 and pos_obs_x<=(largura-((largura%100)%10))/1.7+velocidade_obs: ##dist de 640 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, altura/2 - 0.5*altura*contagem/20

                if pos_obs_x>=(largura-((largura%100)%10))/8.5 and pos_obs_x<=(largura-((largura%100)%10))/8.5+velocidade_obs: ##dist de 640 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, altura/2 - 0.5*altura*contagem/20

                if pos_obs_x2<=(largura-((largura%100)%10))/1.7: ##dist de 640 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if (largura-((largura%100)%10))/8.5<=pos_obs_x<(largura-((largura%100)%10))/1.7: ##dist de 640 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if pos_obs_x3<=(largura-((largura%100)%10))/1.7: ##dist de 640 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs
                if -(round(largura-((largura%100)%10))//2.83)<=pos_obs_x<(largura-((largura%100)%10))/8.5: ##dist de 640 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs

                if pos_obs_x<=-(round(largura-((largura%100)%10))//2.83) and pos_obs_x>=-(round(largura-((largura%100)%10))//2.83)-velocidade_obs: ##dist de 640 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=altura/2 - 0.5*altura*contagem/20
                print(pos_obs_x, -(round(largura-((largura%100)%10))//2.83))


            if contagem>=20 and contagem<40:

                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=velocidade_obs


                if pos_obs_x>=(largura-((largura%100)%10))/1.7 and pos_obs_x<=(largura-((largura%100)%10))/1.7+velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, altura/2 - 0.5*altura

                if pos_obs_x>=(largura-((largura%100)%10))/8.5 and pos_obs_x<=(largura-((largura%100)%10))/8.5+velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, altura/2 - 0.5*altura

                if pos_obs_x2<=(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if (largura-((largura%100)%10))/8.5<=pos_obs_x<(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if pos_obs_x3<=(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs
                if -(round(largura-((largura%100)%10))//2.83)<=pos_obs_x<(largura-((largura%100)%10))/8.5: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs

                if pos_obs_x<=-(round(largura-((largura%100)%10))//2.83) and pos_obs_x>=-(round(largura-((largura%100)%10))//2.83)-velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=altura/2 - 0.5*altura


            if contagem>=40 and contagem<61:

                if contagem==40:
                    pos_obs_y=altura/2 - 0.5*altura*(1-(contagem-40)/20)
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=velocidade_obs


                if pos_obs_x>=(largura-((largura%100)%10))/1.7 and pos_obs_x<=(largura-((largura%100)%10))/1.7+velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, altura/2 - 0.5*altura*(1-(contagem-40)/20)

                if pos_obs_x>=(largura-((largura%100)%10))/8.5 and pos_obs_x<=(largura-((largura%100)%10))/8.5+velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, altura/2 - 0.5*altura*(1-(contagem-40)/20)

                if pos_obs_x2<=(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if (largura-((largura%100)%10))/8.5<=pos_obs_x<(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=velocidade_obs
                if pos_obs_x3<=(largura-((largura%100)%10))/1.7: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs
                if -(round(largura-((largura%100)%10))//2.83)<=pos_obs_x<(largura-((largura%100)%10))/8.5: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=velocidade_obs

                if  pos_obs_x<=-(round(largura-((largura%100)%10))//2.83) and pos_obs_x>=-(round(largura-((largura%100)%10))//2.83)-velocidade_obs: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=altura/2 - 0.5*altura*(1-(contagem-40)/20)


                
    ######### TRABALHO ASCENDENTE
        if graf==2:
            
            if contagem>60000:
                sair=False
            if contagem>=0 and contagem<20000:
                if contagem==0:    
                    pos_obs_y=0.5*altura*contagem/20000
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*contagem/20000
                   
                    
                
                    
            if contagem>=20000 and contagem<40000:
        
                pos_obs_y=0.5*altura
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg

            if contagem>=40000 and contagem<60000:

                if contagem==40000:    
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*(1-(contagem-40000)/20000)
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*(1-(contagem-40000)/20000)

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)
    ######### RELAXAMENTO
        if graf==3:
            
            if contagem>60000:
                sair=False
            if contagem>=0 and contagem<20000:
                if contagem==0:    
                    pos_obs_y=0.5*altura*contagem/20000
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*contagem/20000
                   
                    
                
                    
            if contagem>=20000 and contagem<40000:
        
                pos_obs_y=0.5*altura
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg

            if contagem>=40000 and contagem<60000:

                if contagem==40000:    
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*(1-(contagem-40000)/20000)
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*(1-(contagem-40000)/20000)

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)
    ######### TRABALHO ISOMETRICO
        if graf==4:
            
            if contagem>60000:
                sair=False
            if contagem>=0 and contagem<20000:
                if contagem==0:    
                    pos_obs_y=0.5*altura*contagem/20000
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*contagem/20000
                   
                    
                
                    
            if contagem>=20000 and contagem<40000:
        
                pos_obs_y=0.5*altura
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*contagem/20000
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*contagem/20000

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg

            if contagem>=40000 and contagem<60000:

                if contagem==40000:    
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)
                obs1.show(tela, pos_obs_x, pos_obs_y)
                pos_obs_x-=10
                if pos_obs_x==largura/1.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x2, pos_obs_y2 = larg, 0.5*altura*(1-(contagem-40000)/20000)
                    
                if pos_obs_x==-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x3, pos_obs_y3 = larg, 0.5*altura*(1-(contagem-40000)/20000)

                if pos_obs_x2<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if -largura/5.8<=pos_obs_x<largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs2.show(tela, pos_obs_x2, pos_obs_y2)
                    pos_obs_x2-=10
                if pos_obs_x3<=largura/1.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10                    
                if -largura/1.12<=pos_obs_x<-largura/5.8: ##dist de 500 pixels entre os obstaculos
                    obs3.show(tela, pos_obs_x3, pos_obs_y3)
                    pos_obs_x3-=10

                if pos_obs_x==-largura/1.12: ##dist de 500 pixels entre os obstaculos
                    pos_obs_x=larg
                    pos_obs_y=0.5*altura*(1-(contagem-40000)/20000)   
####### SISTEMA DE PONTUAÇÃO #################

        if pos_x==(pos_obs_x+90) or pos_x==(pos_obs_x2+90) or pos_x==(pos_obs_x3+90):
            pontos+=1
            recorde(pontos)

####### REGRAS DE LIMITAÇÃO = COLISÃO #################
#A coluna tem dimensões 500 X 150 pixels

        if pos_x>=pos_obs_x-50 and pos_x<=pos_obs_x+50:
            if pos_y>=(pos_obs_y+400) or pos_y<=(pos_obs_y+250):
                pygame.mixer.Sound.play(colision_sound)
                colidiu+=1
                
            
        if pos_x>=pos_obs_x2-50 and pos_x<=pos_obs_x2+50:
            if pos_y>=pos_obs_y2+400 or pos_y<=(pos_obs_y2+250):
                pygame.mixer.Sound.play(colision_sound)
                colidiu+=1
                

        if pos_x>=pos_obs_x3-50 and pos_x<=pos_obs_x3+50:
            if pos_y>=pos_obs_y3+400 or pos_y<=(pos_obs_y3+250):
                pygame.mixer.Sound.play(colision_sound)
                colidiu+=1
                    

###################### JOYSTICK ##################################
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
############### MÚSICA #####################################
        if 636 < mouse[0] < 704 and 37 < mouse[1] < 103 and click[0] == 1:
            musica = pausar_som(musica)
            

##        arduinoData = ser.read(1)
##        if len(arduinoData)!=0:
##            lido=int(arduinoData)
           ## if lido==0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
            if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada   
                if event.key == pygame.K_UP: 
                    velocidade_y=-20
            else:
                velocidade_y=20
        
        pos_y+=velocidade_y            
                
        if sair==True:
            ariel.show(tela, pos_x, pos_y, velocidade_y)
            pause_bt.show(tela, 740, 68, 2)
            musica_bt.show(tela, 670, 68, 3)
            let.show(tela, 100, 70, 4)
            dez.show(tela, 200, 70, pontos//10)
            uni.show(tela, 220, 70, pontos%10)
        contagem=time.time()-iniciocontag
        pygame.display.update()           
        tempo.tick(2000)
inicio()    
pygame.quit()
