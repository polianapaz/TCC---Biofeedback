########### BIBLIOTECAS ############
import pygame
from random import randint
import serial
import time

############## CORES ###############
branco, azul = [255,255,255], [0,0,255]
M_lin_col, M_lin = [], []
posimax, posimin = 0, 0

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
#print(largura, altura)

larguras, alturas = zip(*[(largura//36*i, altura//36*i) for i in range(37)])
M_lin_col = [[[l1, a1, l2, a2, j, i]
    for j, (l1, l2) in enumerate(zip(larguras[:-1], larguras[1:]))]
    for i, (a1, a2) in enumerate(zip(alturas[:-1], alturas[1:]))]


##ser = serial.Serial('COM8', baudrate = 76900, timeout=0.01)

############### SONS ###############
GameOver_sound = pygame.mixer.Sound("sons/game_over1.wav")
GameOverPauseScreen_sound = pygame.mixer.Sound("sons/Undersea-Powerplant (online-audio-converter.com).wav")
Inicio_sound = pygame.mixer.Sound("sons/Bubble-Puzzle.wav")
new_record = pygame.mixer.Sound("sons/novo_record.wav")
colision_sound = pygame.mixer.Sound("sons/tapa.wav")
pygame.mixer.music.load("sons/the_little_mermai.wav")


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
        filenames = ['imagens/Ariel1.png', 'imagens/Ariel2.png','imagens/Ariel_morta.png']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        for i in range(len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i], (int(largura/5.7), int(altura/6.2)))
        self.rect = self.imgs[0].get_rect()

    def show(self, tela, pos_x, pos_y, posicao):
        img, rect = self.imgs[posicao], self.rect
        tela.blit(img, rect)
        rect.centerx, rect.centery = pos_x, pos_y


class letras(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/gameover.png', 'imagens/biofeedback.png',
                     'imagens/continuar_peq.png', 'imagens/pontuação.png',
                     'imagens/record.png', 'imagens/restart.png',
                     'imagens/sair.png', 'imagens/start.png', 'imagens/pause.png']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        self.imgs[1] = pygame.transform.scale(self.imgs[1], (int(largura/1.6), int(altura/3.5)))
        self.imgs[-3] = pygame.transform.scale(self.imgs[-3], (int(largura/8), int(altura/14)))
        self.imgs[-2] = pygame.transform.scale(self.imgs[-2], (int(largura/4), int(altura/6.5)))
        self.rects = [img.get_rect() for img in self.imgs]

        self.imagemover, self.imagembio, self.imagemcont, self.imagempont, \
        self.imagemrec, self.imagemres, self.imagemsair, self.imagemstart,  \
        self.imagempause = self.imgs

    def show(self, tela, pos_x, pos_y, escolha):
        if 0 < escolha <= 9:
            img, rect = self.imgs[escolha - 1], self.rects[escolha - 1]
            tela.blit(img, rect)
            rect.centerx, rect.centery = pos_x, pos_y

class fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/fund1.gif', 'imagens/fund2.gif']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        for i in range(len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i], (int(largura+50), int(altura+50)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagemfundo, self.imagemfundo2 = self.imgs

    def show(self, tela, pos_x, pos_y, imagem):
        img, rect = self.imgs[imagem], self.rects[imagem]
        tela.blit(img, rect)
        rect.centerx, rect.centery = pos_x, pos_y



class bubble (pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/bolha_maior.gif', 'imagens/bolha_menor.gif']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        self.imgs[0] = pygame.transform.scale(self.imgs[0], (int(largura/50), int(altura/30)))
        self.imgs[1] = pygame.transform.scale(self.imgs[1], (int(largura/100), int(altura/80)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagembolha,self.imagembolha2 = self.imgs

    def show(self, tela, pos_x, pos_y, nova):
        pos_x_v = [altura//2,altura//4,-(altura//8),0,-altura//2.6,-altura//2,altura//1.8,-(altura//1.2),-(altura//12),-altura//10]
        pos_y_v = [altura//17.5,altura//70,altura//5.3,altura//13,altura//20,altura//6,(altura//6),(altura//12),altura//10,altura//5]
        for i in range(len(self.imgs)*5):
            if i%2 == 0:
                escolha=0
            else:
                escolha=1
            img, rect = self.imgs[escolha], self.rects[escolha]
            tela.blit(img, rect)
            rect.centerx, rect.centery = pos_x+nova+pos_x_v[i], pos_y+nova+pos_y_v[i]


class fish (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/peixe3.png', 'imagens/peixe5.png', 'imagens/peixe1.png',
                     'imagens/peixe7.png', 'imagens/peixe4.png', 'imagens/peixe2.png',
                     'imagens/peixe9.png', 'imagens/peixe7.png', 'imagens/peixe8.png',
                     'imagens/peixe6.png']

        self.imgs = [pygame.image.load(fn) for fn in filenames]

        for i in range(0,len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i], (int(largura/50), int(altura/30)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagempeixe1, self.imagempeixe2, self.imagempeixe3, \
        self.imagempeixe4, self.imagempeixe5, self.imagempeixe6, \
        self.imagempeixe7, self.imagempeixe8, self.imagempeixe9, \
        self.imagempeixe10 = self.imgs

    def show(self, tela, pos_x, pos_y, nova, escolha):
        pos_x_v = [altura//25.6, altura//17, 0, altura//5.12, altura//2.56, altura//8, altura//12.8, altura//3.6, altura//2.13, 0]
        pos_y_v = [altura//5.12, -altura//5.12, altura//5.12, -altura//5.12, altura//5.12, -altura//5.12, altura//5.12, -altura//5.12, altura//5.12, -altura//5.12]
        if 0 < escolha <= 9:
            img, rect = self.imgs[escolha - 1], self.rects[escolha - 1]
            tela.blit(img, rect)
            rect.centerx, rect.centery = pos_x - pos_x_v[escolha], pos_y + nova + pos_y_v[escolha]



class numeros (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/0.png', 'imagens/1.png', 'imagens/2.png',
                     'imagens/3.png', 'imagens/4.png', 'imagens/5.png',
                     'imagens/6.png', 'imagens/7.png', 'imagens/8.png',
                     'imagens/9.png']

        self.imgs = [pygame.image.load(fn) for fn in filenames]
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagem0, self.imagem1, self.imagem2, self.imagem3, \
        self.imagem4, self.imagem5, self.imagem6, self.imagem7, \
        self.imagem8, self.imagem9 = self.imgs

    def show(self, tela, pos_x, pos_y, escolha):
        if 0 <=escolha <= 9:
            img, rect = self.imgs[escolha], self.rects[escolha]
            tela.blit(img, rect)
            rect.centerx, rect.centery = pos_x, pos_y

class letr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/A.png', 'imagens/B.png', 'imagens/C.png',
                     'imagens/D.png', 'imagens/E.png', 'imagens/F.png',
                     'imagens/G.png', 'imagens/H.png', 'imagens/I.png',
                     'imagens/J.png','imagens/K.png', 'imagens/L.png',
                     'imagens/M.png','imagens/N.png', 'imagens/O.png',
                     'imagens/P.png','imagens/Q.png', 'imagens/R.png',
                     'imagens/S.png','imagens/T.png', 'imagens/U.png',
                     'imagens/V.png','imagens/W.png', 'imagens/X.png',
                     'imagens/Y.png', 'imagens/Z.png']

        self.imgs = [pygame.image.load(fn) for fn in filenames]
        for i in range(0,len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i],(int(largura/10), int(altura/6)))
        self.imgs[4] = pygame.transform.scale(self.imgs[4],(int(largura/10.5), int(altura/6)))
        self.rects = [img.get_rect() for img in self.imgs]

        self.imagemA, self.imagemB, self.imagemC, self.imagemD, self.imagemE, self.imagemF, \
        self.imagemG, self.imagemH, self.imagemI, self.imagemJ,self.imagemK, self.imagemL, \
        self.imagemM,self.imagemN, self.imagemO, self.imagemP,self.imagemQ, self.imagemR, \
        self.imagemS,self.imagemT, self.imagemU, self.imagemV,self.imagemW, self.imagemX, \
        self.imagemY, self.imagemZ = self.imgs

    def show(self, tela, quad_x, quad_y, palavra):
        cont=0
        pos_y= int(posicao(quad_x,quad_y,"y"))
        for caracter in palavra:
            cont+=1
            escolha=ord(caracter)-65
            if caracter==' ':
                cont=cont+0.001
            elif caracter=='E':
                img, rect = self.imgs[escolha], self.rects[escolha]
                tela.blit(img, rect)
                rect.centerx, rect.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y+3
            else:
                img, rect = self.imgs[escolha], self.rects[escolha]
                tela.blit(img, rect)
                rect.centerx, rect.centery = int(posicao(quad_x,quad_y,"x")+largura*cont/23), pos_y



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
    M_lin=M_lin_col[quad_y]
    posi=M_lin[quad_x]
    if eixo == 'x':
        return((posi[0]+posi[2])/2)
    if eixo == 'y':
        return((posi[1]+posi[3])/2)


############################ NAO ESTA SENDO USADO POR ENQUANTO #################################
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

    let, let2, let3, let4, let5, col, cor, fund, bolhas = letras(), letras(), letras(), letras(), letras(), coluna(), coral(), fundo(), bubble()
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

############################################################################################################################################


def inicio():

    ## TODAS AS IMAGENS DEVEM SER CARREGADAS ANTES DO LOOP PARA EVITAR QUE ELAS APAREÇAM EM POSICOES ERRADAS NO INICIO DA FUNCAO
    inter = [(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]


    pos_buble_y, let, let2, let3, let4, col, cor = 700, letras(), letras(), letras(), letras(), coluna(), coral()
    ariel, fund, bolhas, pontos, dez, uni = sereia(), fundo(), bubble(), melhor_pont(), numeros(), numeros()
    teste, teste2 = letr(),letr()
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
    ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), 0)
    ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), 1)
    teste.show(tela, 11,11, "TARAGEM")
    teste.show(tela, 14,16, "MODO")
    teste.show(tela,14,21, "SAIR")
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    pygame.display.update()

    menu=True

    while menu:
        ###### INTERFACE FUNDO ###
        fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
        cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
        cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
        col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
        col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))
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

        ########## POSICAO E MOVIMENTO DA SEREIA #######
        if (pos_buble_y%15)==0:
            posi=0
        else:
            posi=1
        ariel.show(tela,  posicao(18,27,"x"), posicao(18,27,"y"), posi)

        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

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
                ######EVOLUIR ISSO PARA LER UM ARQUIVO E VER SE ESSE VALOR DE MAXIMO E MINIMO È VALIDO ###########
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
                pygame.mixer.music.stop()
                menu=modo()
        if menu:
            if posicao(14,15,"x") < mouse[0] < posicao(21,15,"x") and posicao(14,20,"y") < mouse[1] < posicao(14,22,"y") and click[0] == 1:
                menu=False


        pygame.display.update()
        tempo.tick(15)

def modo():

    inter=[(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]


    pos_buble_y, col, cor = 700, coluna(), coral()
    fund, bolhas = fundo(), bubble()
    teste, teste2=letr(),letr()
    #pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
    cor.show(tela, posicao(35,9,"x")+largura//36, posicao(35,9,"y"), 1)
    cor.show(tela, posicao(0,9,"x"), posicao(0,9,"y"), 1)
    col.show(tela, posicao(35,23,"x")+largura//36, posicao(35,23,"y"))
    col.show(tela, posicao(0,23,"x"), posicao(0,23,"y"))

    teste.show(tela, 2,11, "TRABALHO ISOMETRICO")
    teste.show(tela, 2,16, "TRABALHO ASCENDENTE")
    teste.show(tela, 9,21, "RELAXAMENTO")
    teste.show(tela, 5,26, "CONTRACAO TONICA")
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

        teste.show(tela, 2,11, "TRABALHO ISOMETRICO")
        teste.show(tela, 2,16, "TRABALHO ASCENDENTE")
        teste.show(tela, 9,21, "RELAXAMENTO")
        teste.show(tela, 5,26, "CONTRACAO TONICA")

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
        ##botão_1 = TRABALHO ISOMETRICO
        if mod:
            if posicao(11,9,"x") < mouse[0] < posicao(27,12,"x") and posicao(14,9,"y") < mouse[1] < posicao(22,12,"y") and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                graf=1
                fund.show(tela, posicao(18,18,"x"), posicao(18,18,"y"), 1)
                pygame.display.update()
                pygame.mixer.music.stop()
                mod=grafico(graf)


        pygame.display.update()

def taragem():

    global posimax
    global posimin
    inter=[(-100,largura), (-100,largura), (-100,largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    cont =  [letras()]*6 + [numeros()]*7 + [coluna(), coral(), sereia(),
             fundo(), bubble(), melhor_pont(), 700,350,350,0, 0,0,0,altura,
             True,2]
    pmax1, pmax2, pmax3, pmin1, pmin2, pmin3,uni, posimaxcen, posimaxdez, \
    posimaxuni, posimincen, posimindez, posiminuni,col, cor, ariel, fund, \
    bolhas, pontos, pos_buble_y, posi, posi2, contagem2, contagem3,check, \
    posimax, posimin, tara, velocidade_y = [i for i in cont]
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

            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)

            if (pos_buble_y%15)==0:
                escolha=1
            else:
                escolha=0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tara = False
                if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                    if event.key == pygame.K_UP:
                        velocidade_y=-2
                else:
                    velocidade_y=2

            posi+=velocidade_y
            if posi>=1000:
                posi=999
            if posi<=0:
                posi=10
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
            tempo.tick(25)
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

            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)

            if (pos_buble_y%15)==0:
                escolha=1
            else:
                escolha=0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tara = False
                if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                    if event.key == pygame.K_UP:
                        velocidade_y=-2
                else:
                    velocidade_y=2

            posi2+=velocidade_y
            if posi2>=1000:
                posi2=999
            if posi2<=0:
                posi2=10
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
            tempo.tick(25)
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

def altura_col(tipo):
    with open("graficos/" + str(tipo), "r") as arquivo:
        valores = [float(val) for linha in arquivo for val in linha.split()]
    return valores


def grafico(graf):

    pos_y, pos_x, velocidade_y, larg, pos_yf, pos_xf, pos_xf2 = 350, 250, 0, largura-((largura%100)%10)+altura//9.6, altura//2, largura//2,round(largura*1.537)-1
    pos_obs_x, pos_obs_x2, pos_obs_x3, velocidade_obs = larg, larg, larg, 20

    pos_buble_x=randint(-100,largura)
    pos_buble_y, pos_peix_x, pos_peix_y = 700, -100, 350
    lims = [(-100, 300), (-100, 300), (-100, 300), (1, 10), (-400, 200), (1, 10), (-160, 100), (-160, 100), (-160, 100)]
    nova, nova2, novapeixe, escolhapeixe, novapeixe2, escolhapeixe2, pos_obs_y, pos_obs_y2, pos_obs_y3 = [randint(*pair) for pair in lims]

    sair, pontos, pausa, musica, colidiu, cont,escolha = True, 0, 1, True, 0, 0,0

    #player funciona
    if musica:
        pygame.mixer.music.play(-1)


    #ser.reset_input_buffer()
#####################################
    ariel, bolhas, fund1, fund2, peixe = sereia(), bubble(), fundo(), fundo(), fish()
    obs1, obs2, obs3, pause_bt = coluna(), coluna(), coluna(), coral()
    musica_bt, musica_simb, dez, uni, let = coral(), coral(), numeros(), numeros(), letras()
#####################################
    for conta in range(0,9):
        dez.show(tela, -100, -100, conta)
        uni.show(tela, -100, -100, conta)
        peixe.show(tela, -100, -100, -100,conta+1)
    obs1.show(tela, -80,-80)
    obs2.show(tela, -80,-80)
    obs3.show(tela, -80,-80)
    ariel.show(tela, -30, -30, 0)
    ariel.show(tela, -30, -30, 1)
    let.show(tela, -30, -30, 4)
   # pause_bt.show(tela, -100, -100, 2)
   # musica_bt.show(tela, -100, -100, 3)
    fund1.show(tela, pos_xf,pos_yf, 0)
    fund2.show(tela,pos_xf2, pos_yf, 1)
    contagem=0

    if graf==1:
        pos_col_y = altura_col("Contração Tônica a 50%.txt")

    iniciocontag=time.time()
    while sair:

######################### FUNDO ###############################
        tela.fill(azul)
        fund1.show(tela, pos_xf, int(altura//2), 0)
        fund2.show(tela, pos_xf2, int(altura//2), 1)

        pos_xf = round(largura*1.537)-1 if pos_xf2 == largura//2 else pos_xf - 1
        pos_xf2 = round(largura*1.537)-1 if pos_xf == largura//2 else pos_xf2 -1
       # print (pos_xf,pos_xf2)

################### ALEATORIEDADE DAS BOLHAS ################
        if pos_buble_y == altura:
            nova, nova2 = randint(-largura//3,largura//3), randint(-largura//3,largura//3)
        if pos_buble_y < -altura*1.8:
            pos_buble_y = altura*1.1
        #bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.7, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.3, nova-nova2)
        pos_buble_y-=2

##################PEIXES

        if pos_peix_x == -largura//13:
            aleatorio = [(-400, altura//1.5), (-400, altura//1.5), (1, 5), (1, 5)]
            novapeixe, novapeixe2, escolhapeixe, escolhapeixe2 = [randint(*pair) for pair in aleatorio]
        if pos_peix_x>largura+largura//7:
            pos_peix_x=-altura//2

        peixe.show(tela, pos_peix_x, pos_peix_y, novapeixe, escolhapeixe)
        peixe.show(tela, pos_peix_x*1.5, pos_peix_y, novapeixe2+novapeixe, escolhapeixe2-escolhapeixe)
        peixe.show(tela, pos_peix_x*1.10, pos_peix_y, novapeixe2, escolhapeixe2)
        peixe.show(tela, pos_peix_x*1.25, pos_peix_y, novapeixe2-novapeixe, escolhapeixe2+escolhapeixe)
        peixe.show(tela, pos_peix_x*1.05, pos_peix_y, novapeixe-150, escolhapeixe+2)
        peixe.show(tela, pos_peix_x*1.45, pos_peix_y, novapeixe2+novapeixe-20, escolhapeixe2-escolhapeixe+1)
        peixe.show(tela, pos_peix_x*1.15, pos_peix_y, novapeixe2-150, escolhapeixe2+2)
        peixe.show(tela, pos_peix_x*1.30, pos_peix_y, novapeixe2-novapeixe+200, escolhapeixe2+escolhapeixe+1)

        pos_peix_x += 2


####### LIMITAÇÃO DE MOVIMENTOS #################

        if pos_y < 10:
            pos_y += 20

        if pos_y >= altura - 10:
            pos_y -= 10

####### CONTROLE DE MOVIMENTOS DO OBSTÁCULO #################

    ######### CONTRACAO TONICA

        #if contagem>60:
        #    pygame.mixer.music.stop()
        #    sair=inicio()
        if 6000 > contagem >= 0:
            if contagem == 0.00:
                pos_obs_y = altura*(1/2 - pos_col_y[cont])

########### EXIBIÇÃO DAS COLUNAS
            if pos_obs_x>=0 and pos_obs_x<=largura:
                obs1.show(tela, pos_obs_x, pos_obs_y)
            if pos_obs_x2>=0 and pos_obs_x2<=largura:
                obs1.show(tela, pos_obs_x2, pos_obs_y2)

########### DESLOCAMENTO DAS COLUNAS
            if cont==0:
                pos_obs_x-=velocidade_obs
            else:
                pos_obs_x-=velocidade_obs
                pos_obs_x2-=velocidade_obs

########### DETERMINAR ALTURA DAS COLUNAS
            if  pos_obs_x>(largura/3)-velocidade_obs/2 and pos_obs_x<(largura/3)+velocidade_obs/2 and cont<=28: ##dist de 640 pixels entre os obstaculos
                cont+=1
                pos_obs_x2, pos_obs_y2 = largura, altura*(1/2 - pos_col_y[cont])
                #pos_obs_x2-=velocidade_obs

            if  pos_obs_x>-(largura/3)-velocidade_obs/2 and pos_obs_x<-(largura/3)+velocidade_obs/2 and cont<=28:
                cont+=1
                pos_obs_x, pos_obs_y = largura, altura*(1/2 - pos_col_y[cont])

########### FIM DO GRÁFICO
            if cont>=29 and pos_obs_x2<velocidade_obs:
                pygame.mixer.music.stop()
                sair=inicio()
            #if  pos_obs_x2>(largura/3)-velocidade_obs/2 and pos_obs_x2<(largura/3)+velocidade_obs/2: ##dist de 640 pixels entre os obstaculos
            #    cont+=1
            #    pos_obs_x2, pos_obs_y2 = largura, altura*(1/2 - pos_col_y[cont])
            #    #pos_obs_x2-=velocidade_obs

            #if  pos_obs_x2>-(largura/3)-velocidade_obs/2 and pos_obs_x2<-(largura/3)+velocidade_obs/2:
            #    cont+=1
            #    pos_obs_x, pos_obs_y = largura, altura*(1/2 - pos_col_y[cont])

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
                    velocidade_y=-2
                    escolha=0
            else:
                velocidade_y=2
                escolha=1

        pos_y+=velocidade_y

        if sair==True:
            ariel.show(tela, pos_x, pos_y, escolha)
##            pause_bt.show(tela, 740, 68, 2)
##            musica_bt.show(tela, 670, 68, 3)
            let.show(tela, 100, 70, 4)
            dez.show(tela, 200, 70, pontos//10)
            uni.show(tela, 220, 70, pontos%10)
        contagem=time.time()-iniciocontag
        pygame.display.update()
        #tempo.tick(2000)
inicio()
pygame.quit()
