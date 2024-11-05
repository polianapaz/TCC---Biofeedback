########### BIBLIOTECAS ############
import pygame
from random import randint
import serial


############## CORES ###############
branco = [255,255,255]
azul= [0,0,255]
TUPLA=[]
lista=[]
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
            self.rect2.centerx , self.rect2.centery = pos_x, pos_y+650 #espaço de 150 entre as colunas


class sereia(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemsereia = pygame.transform.scale(pygame.image.load('imagens/Ariel1.png'), (int(largura/4.7), int(altura/5.2)))
        self.imagemsereia2 = pygame.transform.scale(pygame.image.load('imagens/Ariel2.png'), (int(largura/4.7), int(altura/5.2)))
        self.rect = self.imagemsereia.get_rect()

    def show(self, tela, pos_x, pos_y, posicao):
        if posicao==10:
            tela.blit(self.imagemsereia2, self.rect)
            self.rect.centerx, self.rect.centery = pos_x, pos_y
        if posicao==-20 or posicao==0:            
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
        self.imagemsair = pygame.image.load('imagens/sair.png')
        self.imagemstart = pygame.image.load('imagens/start.png')
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
        self.imagemfundo = pygame.transform.scale(pygame.image.load('imagens/fund2.png'), (int(largura), int(altura)))
        self.imagemfundo2 = pygame.transform.scale(pygame.image.load('imagens/fund1.png'), (int(largura), int(altura)))
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
        self.imagempeixe3 = pygame.transform.scale(pygame.image.load('imagens/baleia.png'), (int(largura/5), int(altura/10)))
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

        num = [self.imagem0.get_rect(), self.imagem1.get_rect(), self.imagem2.get_rect(), self.imagem3.get_rect(), self.imagem4.get_rect()]
        num2 = [self.imagem5.get_rect(), self.imagem6.get_rect(), self.imagem7.get_rect(), self.imagem8.get_rect(), self.imagem9.get_rect()]

        self.rect0, self.rect1, self.rect2, self.rect3, self.rect4 = [retangulo for retangulo in num]
        self.rect5, self.rect6, self.rect7, self.rect8, self.rect9 = [retangulo for retangulo in num2]
        
    def show(self, tela, pos_x, pos_y, escolha):
        if escolha==0:
            tela.blit(self.imagem0, self.rect0)
            self.rect0.centerx, self.rect0.centery = pos_x, pos_y        
        if escolha==1:
            tela.blit(self.imagem1, self.rect1)
            self.rect1.centerx, self.rect1.centery = pos_x, pos_y
        if escolha==2:
            tela.blit(self.imagem2, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x, pos_y
        if escolha==3:
            tela.blit(self.imagem3, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y
        if escolha==4:
            tela.blit(self.imagem4, self.rect4)
            self.rect4.centerx, self.rect4.centery = pos_x, pos_y
        if escolha==5:
            tela.blit(self.imagem5, self.rect5)
            self.rect5.centerx, self.rect5.centery = pos_x, pos_y
        if escolha==6:
            tela.blit(self.imagem6, self.rect6)
            self.rect6.centerx, self.rect6.centery = pos_x, pos_y
        if escolha==7:
            tela.blit(self.imagem7, self.rect7)
            self.rect7.centerx, self.rect7.centery = pos_x, pos_y
        if escolha==8:
            tela.blit(self.imagem8, self.rect8)
            self.rect8.centerx, self.rect8.centery = pos_x, pos_y
        if escolha==9:
            tela.blit(self.imagem9, self.rect9)
            self.rect9.centerx, self.rect9.centery = pos_x, pos_y

     
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
            self.rect1.centerx, self.rect1.centery = pos_x-200, pos_y
        if escolha==2:
            tela.blit(self.imagemcor2, self.rect2)
            self.rect2.centerx, self.rect2.centery = pos_x, pos_y
        if escolha==3:
            tela.blit(self.imagemcor3, self.rect3)
            self.rect3.centerx, self.rect3.centery = pos_x, pos_y

for i in range(9): #o range é 9 pois são 9 quadrantes, 0 até 8
    adicionar = []
    for j in range(9):
        adicionar.append([(largura//9)*j, (altura//9)*i,(largura//9),(altura//9),j,i]) #colunas
        # esse vetor preenche com as posições x e y do primeiro pixel e do ultimo pixel do quadrante, respectivamente, no final j e i são só para saber a posição
    TUPLA.append(adicionar)#linhas

def posicao(quad_x,quad_y, eixo):
    lista=TUPLA[quad_y] #recebe uma lista da lista que contem todas as posições de todos os quadrantes da linha
    posi=lista[quad_x] #recebe a posição de um quadrante especifico da linha, ou seja, a coluna desejada   
    if eixo == 'x':
        return((posi[0]+posi[2])/2)
    if eixo == 'y':
        return((posi[1]+posi[3])/2)

def taragem():
    inter=[(-100,350), (-100,300), (-100,300)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    
    pos_buble_y, pmax1, pmax2, pmax3, pmin1, pmin2, pmin3, col, cor = 700, letras()*6, coluna(), coral()
    ariel, fund, bolhas, pontos, posimaxcen, posimaxdez, posimaxuni, posimincen, posimindez, posiminuni, uni = sereia(), fundo(), bubble(), melhor_pont(), numeros()*7
    pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    
    tara=True
    
    while tara:
        ###### INTERFACE ### NAO MEXE NAS POSICOES,ELAS NAO FAZEM MUITO SENTIDO
        fund.show(tela, 440, 350, 1)
        cor.show(tela, largura+largura/7.6, 205, 1)
        cor.show(tela, largura/6.2, 205, 1)
        col.show(tela, largura-largura/45, 500)
        col.show(tela, largura/45, 500)

        ###################ALEATORIEDADE DAS BOLHAS
        if pos_buble_y==700:
            nova=randint(-300,300)
            nova2=randint(-300,300)
            
        if pos_buble_y<-2050:
            pos_buble_y=800

        if (pos_buble_y%10)==0:
            posi=10
        else:
            posi=0
        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5
        
        ################
        for contagem in range(3,0,-1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False
            #imprimir a mensagem "ao final da contagem contraia o máximo que conseguir"
            uni.show(tela, largura/2, 650, contagem)
            sleep.time(1)
        start=time.time()   
        while (contagem2<=10):
            posimaxcen.show(tela, 389, 280, posimax//100)
            posimaxdez.show(tela, 411, 280, (posimax%100)//10)
            posimaxuni.show(tela, 433, 280, (posimax%100)%10)

            #pmax.show()
            #pmin.show()
            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)
            ariel.show(tela, largura/2, 550, posi)

            if posi>posimax:
                posimax=posi
            if posi<posimin:
                posimin=posi

            mouse=pygame.mouse.get_pos() #pos=[x,y]
            click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False
                            
            pygame.display.update()
            contagem2=time.time()-start    
        for contagem in range(3,0,-1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False
            #imprimir a mensagem "ao final da contagem relaxe o máximo que conseguir"
            uni.show(tela, largura/2, 650, contagem)
            sleep.time(1)    
        start=time.time()   
        while (contagem3<=120):
            posimaxcen.show(tela, 389, 280, posimax//100)
            posimaxdez.show(tela, 411, 280, (posimax%100)//10)
            posimaxuni.show(tela, 433, 280, (posimax%100)%10)
            posimincen.show(tela, 389, 310, posimin//100)
            posimindez.show(tela, 411, 310, (posimin%100)//10)
            posiminuni.show(tela, 433, 310, (posimin%100)%10)

            #pmax.show()
            #pmin.show()
            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos=int(ser.read(ser.inWaiting()))
            #    print(posi)
            ariel.show(tela, largura/2, 550, posi)

            if posi>posimax:
                posimax=posi
            if posi<posimin:
                posimin=posi

            mouse=pygame.mouse.get_pos() #pos=[x,y]
            click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara=False
                            
            pygame.display.update()
            contagem3=time.time()-start
        tara=inicio()



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
    
    inter=[(-100,350), (-100,300), (-100,300)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    
    pos_buble_y, let, let2, let3, let4, col, cor = 700, letras(), letras(), letras(), letras(), coluna(), coral()
    ariel, fund, bolhas, pontos, dez, uni = sereia(), fundo(), bubble(), melhor_pont(), numeros(), numeros()
    pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    
    menu=True
    
    while menu:
        ###### INTERFACE ### NAO MEXE NAS POSICOES,ELAS NAO FAZEM MUITO SENTIDO
        fund.show(tela, 440, 350, 1)
        let.show(tela, largura/2, 80, 2) #Biofeedback
        let2.show(tela, 250, 550, 8) # 200 X 84 START
        let3.show(tela, 550, 550, 7) # 126 X 40 SAIR
        let4.show(tela, 400, 280, 5) #Recorde
        cor.show(tela, largura+largura/7.6, 205, 1)
        cor.show(tela, largura/6.2, 205, 1)
        col.show(tela, largura-largura/45, 500)
        col.show(tela, largura/45, 500)

        ################
        dez.show(tela, 389, 320, pontos//10)
        uni.show(tela, 411, 320, pontos%10)
        ###################ALEATORIEDADE DAS BOLHAS
        if pos_buble_y==700:
            nova=randint(-300,300)
            nova2=randint(-300,300)
            
        if pos_buble_y<-2050:
            pos_buble_y=800

        if (pos_buble_y%10)==0:
            posi=10
        else:
            posi=0
        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x-nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x-nova+nova2, pos_buble_y*1.10, nova-nova2)
        pos_buble_y-=5

        ariel.show(tela, largura/2, 550, posi)
        
            

        mouse=pygame.mouse.get_pos() #pos=[x,y]
        click=pygame.mouse.get_pressed() #pressed=[bdir,centro,besq]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu=False
                
        ##botão_1 = START
        if menu:
            if 150 < mouse[0] < 350 and 508 < mouse[1] < 592 and click[0] == 1:
                pygame.mixer.Sound.stop(Inicio_sound)
                menu=taragem()

            ##botao_2 = SAIR
            if menu:
                if  487 < mouse[0] < 613 and 530 < mouse[1] < 570 and click[0] == 1:
                    menu=False
        
        pygame.display.update()


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
                return(pausa)g
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

def game():

    pos_y, pos_x, velocidade_y, larg, pos_yf, pos_xf, pos_xf2 = 350, 250, 0, largura+80, 350, 410, 1487
    pos_obs_x, pos_obs_x2, pos_obs_x3 = larg, larg, larg

    pos_buble_x=randint(-100,350)
    pos_buble_y, pos_peix_x, pos_peix_y = 700, -100, 350

    lims = [(-100, 300), (-100, 300), (-100, 300), (1, 10), (-400, 200), (1, 10), (-160, 100), (-160, 100), (-160, 100)]
    nova, nova2, novapeixe, escolhapeixe, novapeixe2, escolhapeixe2, pos_obs_y, pos_obs_y2, pos_obs_y3 = [randint(*pair) for pair in lims]

    sair, pontos, pausa, musica = True, 0, 1, True

    #player funciona
    if musica:
        pygame.mixer.music.play(-1)
        print("carrega primeiro")
        
    ser.reset_input_buffer()
#####################################
    classes = [sereia(), bubble(), fundo(), fundo(), fish(), dead(), coluna(), coluna(), coluna(), coral(), coral(), coral(), numeros(), numeros(), letras()]
    ariel, bolhas, fund1, fund2, peixe, morta, obs1, obs2, obs3, pause_bt, musica_bt, musica_simb, dez, uni, let = [pair for pair in classes]
#####################################
   
    while sair:

####### SAIDA #################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return(False)
######################### FUNDO ###############################
        tela.fill(azul)
        fund1.show(tela, pos_xf, pos_yf, 1)
        fund2.show(tela, pos_xf2, pos_yf, 2)
        
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
###################### JOYSTICK ##################################

##        arduinoData = ser.read(1)
##        if len(arduinoData)!=0:
##            lido=int(arduinoData)
           ## if lido==0:
        velocidade_y=tamanho
    ##        if lido:
      ##          velocidade_y=-2*tamanho
        
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        pos_y+=velocidade_y

####### LIMITAÇÃO DE MOVIMENTOS #################

        if pos_y<10:
            pos_y+=20

        if pos_y>=altura-10: 
            pos_y-=10
            morta.show(tela, pos_x-100, pos_y) ##VER SE APARECE
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(colision_sound)
            sair = gameover(pontos)
            if sair==False:
                  pausa=0
            pos_y, pos_x, velocidade_y, pos_obs_x, pos_obs_y, pos_obs_x2, pos_obs_x3, pontos = 350, 250, 0, larg, randint(-160, 100), larg, larg, 0
        
####### CONTROLE DE MOVIMENTOS DO OBSTÁCULO #################

        obs1.show(tela, pos_obs_x, pos_obs_y)
        
        pos_obs_x-=10
        if pos_obs_x==380: ##dist de 500 pixels entre os obstaculos
            pos_obs_x2, pos_obs_y2 = larg, randint(-160, 100)
        if pos_obs_x==-120: ##dist de 500 pixels entre os obstaculos
            pos_obs_x3, pos_obs_y3 = larg, randint(-160, 100)

        if pos_obs_x2<=380: ##dist de 500 pixels entre os obstaculos
            obs2.show(tela, pos_obs_x2, pos_obs_y2)
            pos_obs_x2-=10
        if -120<=pos_obs_x<380: ##dist de 500 pixels entre os obstaculos
            obs2.show(tela, pos_obs_x2, pos_obs_y2)
            pos_obs_x2-=10

        if pos_obs_x3<=380: ##dist de 500 pixels entre os obstaculos
            obs3.show(tela, pos_obs_x3, pos_obs_y3)
            pos_obs_x3-=10
        if -620<=pos_obs_x<-120: ##dist de 500 pixels entre os obstaculos
            obs3.show(tela, pos_obs_x3, pos_obs_y3)
            pos_obs_x3-=10

        if pos_obs_x==-620: ##dist de 500 pixels entre os obstaculos
            pos_obs_x=larg
            
####### SISTEMA DE PONTUAÇÃO #################

        if pos_x==(pos_obs_x+90) or pos_x==(pos_obs_x2+90) or pos_x==(pos_obs_x3+90):
            pontos+=1
            recorde(pontos)

####### REGRAS DE LIMITAÇÃO = COLISÃO #################
#A coluna tem dimensões 500 X 150 pixels

        if pos_x>=pos_obs_x-50 and pos_x<=pos_obs_x+50:
            if pos_y>=(pos_obs_y+400) or pos_y<=(pos_obs_y+250):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(colision_sound)
                sair = gameover(pontos)
                if sair==False:
                    pausa=0
                pos_y, pos_x, velocidade_y, pos_obs_x, pos_obs_y, pos_obs_x2, pos_obs_x3, pontos = 350, 250, 0, larg, randint(-160, 100), larg, larg, 0
            
        if pos_x>=pos_obs_x2-50 and pos_x<=pos_obs_x2+50:
            if pos_y>=pos_obs_y2+400 or pos_y<=(pos_obs_y2+250):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(colision_sound)
                sair = gameover(pontos)
                if sair==False:
                    pausa=0
                pos_y, pos_x, velocidade_y, pos_obs_x, pos_obs_y, pos_obs_x2, pos_obs_x3, pontos = 350, 250, 0, larg, randint(-160, 100), larg, larg, 0

        if pos_x>=pos_obs_x3-50 and pos_x<=pos_obs_x3+50:
            if pos_y>=pos_obs_y3+400 or pos_y<=(pos_obs_y3+250):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(colision_sound)
                sair = gameover(pontos)
                if sair==False:
                    pausa=0
                pos_y, pos_x, velocidade_y, pos_obs_x, pos_obs_y, pos_obs_x2, pos_obs_x3, pontos = 350, 250, 0, larg, randint(-160, 100), larg, larg, 0    

############## PAUSAR ####################################        
        if 706 < mouse[0] < 774 and 36 < mouse[1] < 104 and click[0] == 1:
            pausa=pause(pontos)

        if pausa==0:
            tela.fill(branco)
            return(False)
        if pausa==1:
            sair=True
        if pausa==2:
            sair=True
            pos_y, pos_x, velocidade_y, pos_obs_x, pos_obs_y, pos_obs_x2, pos_obs_x3, pontos, pausa = 350, 250, 0, largura, 0, largura, largura, 0, 1
            
############### MÚSICA #####################################
        if 636 < mouse[0] < 704 and 37 < mouse[1] < 103 and click[0] == 1:
            musica = pausar_som(musica)
                
        if sair==True:
            ariel.show(tela, pos_x, pos_y, velocidade_y)
            pause_bt.show(tela, 740, 68, 2)
            musica_bt.show(tela, 670, 68, 3)
            let.show(tela, 100, 70, 4)
            dez.show(tela, 200, 70, pontos//10)
            uni.show(tela, 220, 70, pontos%10)
        
        pygame.display.update()           
        tempo.tick(2000)

inicio()    
pygame.quit()
