########### BIBLIOTECAS ############
import pygame
from random import randint
import serial
import time
from datetime import datetime
from pygame.locals import *
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import sqlite3
from scipy.interpolate import interp1d

########### TESTE PYGAME ###########
try:
    pygame.init()
except:
    print("O modulo pygame não foi inicializado com sucesso")

############### TELA ###############
largura, altura, tamanho, tempo = pygame.display.Info().current_w, \
                                        pygame.display.Info().current_h, \
                                        pygame.display.Info().current_h/70,\
                                        pygame.time.Clock()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption ("BIOFEEDBACK")

############## CORES ###############

branco, azul = [255, 255, 255], [0, 0, 255]
M_lin_col, M_lin, pos_obs_y, pos_obs_x, n_paciente, idade_paciente, trata_paciente, posmax, posmin = [], [], [], [], [], [], [], [], []
posimax, posimin, larg = 0, largura, largura - ((largura % 100)%10) + altura//9.6

############### DEFINIÇÃO DOS QUADRANTES ##########

larguras, alturas = zip(*[(largura//36*i, altura//36*i) for i in range(37)])
M_lin_col = [[[l1, a1, l2, a2, j, i]
    for j, (l1, l2) in enumerate(zip(larguras[:-1], larguras[1:]))]
    for i, (a1, a2) in enumerate(zip(alturas[:-1], alturas[1:]))]

############### PREENCHIMENTO DAS POSIÇÕES INICIAIS ######

for i in range(5):
    pos_obs_x.append(larg)
    pos_obs_y.append(0)

##ser = serial.Serial('COM8', baudrate = 76900, timeout = 0.01)

############### SONS ###############

GameOver_sound = pygame.mixer.Sound("sons/game_over1.wav")
GameOverPauseScreen_sound = pygame.mixer.Sound("sons/Undersea-Powerplant (online-audio-converter.com).wav")
Inicio_sound = pygame.mixer.Sound("sons/Bubble-Puzzle.wav")
new_record = pygame.mixer.Sound("sons/novo_record.wav")
colision_sound = pygame.mixer.Sound("sons/tapa.wav")
##pygame.mixer.music.load("sons/the_little_mermai.wav")


########### SALVAMENTO DE DADOS ###########


db_obj = sqlite3.connect('resultados/Paciente_info.db')
db_obj2 = sqlite3.connect('resultados/Paciente_progresso.db')
db_obj3 = sqlite3.connect('graficos/Graf_ideal.db')

db_obj_cursor = db_obj.cursor()
db_obj2_cursor = db_obj2.cursor()
db_obj3_cursor = db_obj3.cursor()

class PacienteDados:
    def __init__(self):
        self.nome_arquivo = "resultados/"

    def data_entry(self, nome, idade, tipo_trat, data, posimax, posimin, pontos, tempo, grafico, id_pont, id_tempo, modo = 'Exercício'):
        db_obj_cursor.execute('CREATE TABLE IF NOT EXISTS dados (paciente text, idade integer, \
                                tratamento text, data text, pressao_max integer, pressao_min integer,\
                                pontos text, tempo text, nome_grafico text, ponto_ideal text, tempo_ideal text, modo text)')
        hora = data.strftime("%d-%m-%Y %H:%M:%S")

        db_obj_cursor.execute("INSERT INTO dados VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [nome, idade, \
                                tipo_trat, hora, posimax, posimin, pontos, tempo,  grafico, id_pont, id_tempo, modo])
        db_obj.commit()

    def paciente_select(self, modo):

        name = []
        db_obj_cursor.execute('CREATE TABLE IF NOT EXISTS dados (paciente text, idade integer, \
                                tratamento text, data text, pressao_max integer, pressao_min integer,\
                                pontos text, tempo text, nome_grafico text, ponto_ideal text, tempo_ideal text, modo text)')
        sql = 'SELECT paciente FROM dados WHERE modo = ? GROUP BY paciente'
        for row in db_obj_cursor.execute(sql, [modo]):
            name.append(row[0])
        return name

    def data_select(self, nome, modo = "Exercício"):
        dia = []
        for row in db_obj_cursor.execute("SELECT data FROM dados WHERE paciente = ? and modo = ?",\
                                        [nome, modo]):

            dia.append(row[0])
        return dia

    def tratamento_select(self, nome, data, modo = "Exercício"):
        tipo = []
        sql = 'SELECT tratamento FROM dados WHERE paciente = ? and data = ? and modo = ?'
        for row in db_obj_cursor.execute(sql, [nome, data, modo]):
            tipo.append(row[0])
        return tipo

    def grafico_select(self, nome, data, modo = "Exercício"):
        tipo_tra = []
        sql = 'SELECT nome_grafico FROM dados WHERE paciente = ? and data = ? and modo = ?'
        for row in db_obj_cursor.execute(sql, [nome, data, modo]):
            tipo_tra.append(row[0])
        return tipo_tra

    def id_select(self, nome, data, nome_graf, modo = 'Exercício'):
        x, y = [], []
        sql = 'SELECT ponto_ideal, tempo_ideal FROM dados WHERE paciente = ? and data = ? and nome_grafico = ? and modo = ?'
        for row in db_obj_cursor.execute(sql, [nome, data, nome_graf, modo]):
            x.append(row[0])
            y.append(row[1])
        return x,y

    def dados_select(self, nome, data, nome_graf, modo = 'Exercício'):
        x, y = [], []
        sql = 'SELECT pontos, tempo FROM dados WHERE paciente = ? and data = ? and nome_grafico = ? and modo = ?'
        for row in db_obj_cursor.execute(sql, [nome, data, nome_graf, modo]):
            x.append(row[0])
            y.append(row[1])
        return x,y
    
    def maxmin_select(self, nome, data, nome_graf, modo = 'Exercício'):
        x, y = [], []
        j=0
        print(type(data))
        sql = 'SELECT pressao_max, pressao_min FROM dados WHERE paciente = ? and data = ? and nome_grafico = ? and modo = ?'
        for i in data:
            if i == '.':
                j+=1
        if (j>0):
            data = data[:-j]    
        for row in db_obj_cursor.execute(sql, [nome, data, nome_graf, modo]):
            x.append(row[0])
            y.append(row[1])
        return x,y

    def atualizar_dados (self, nome, data, maxi, mini, modo = "Taragem"):
        hora = data.strftime("%d-%m-%Y %H:%M:%S")
        sql = ("UPDATE dados SET data = ?, pressao_min =?, pressao_max = ? WHERE paciente = ? and modo = ?")
        db_obj_cursor.execute(sql, [hora, mini, maxi, nome, modo])
        db_obj.commit()

    def trataId_select(self, nome, idade):
        for row in db_obj_cursor.execute("SELECT tratamento FROM dados GROUP BY \
                                        tratamento HAVING paciente = ? and idade = ?",\
                                        [n_paciente[0], idade_paciente[0]]):
            return row[0]

    def idade_select(self, nome):
        for row in db_obj_cursor.execute("SELECT idade FROM dados GROUP BY idade HAVING paciente = ?", [nome]):
            return row[0]

    def pressao_maxmin_select(self, nome, modo = 'Taragem'):
        sql1 = "SELECT pressao_max FROM dados WHERE paciente = ? and modo = ?"
        sql2 = "SELECT pressao_min FROM dados WHERE paciente = ? and modo = ?"
        for minimo in db_obj_cursor.execute(sql1, [nome, modo]):
            mini = minimo[0]
        for maximo in db_obj_cursor.execute(sql2, [nome, modo]):
            maxi = maximo[0]
        return mini,maxi

    def delete_row_from_table(self, nome, mode = "Taragem"):
        sql = ("DELETE FROM dados WHERE paciente = ? and modo = ?")
        db_obj_cursor.execute(sql,[nome, mode])
        db_obj.commit()

    def paciente_progresso(self):
        name = []
        db_obj2_cursor.execute('CREATE TABLE IF NOT EXISTS progresso (paciente text,\
                                data text, pressao_max integer, pressao_min integer, \
                                media_max_taragem float, media_min_taragem float,\
                                acertos integer, erros integer, media_acertos float,\
                                media_erros float)')
        sql = 'SELECT paciente FROM progresso GROUP BY paciente'
        for row in db_obj2_cursor.execute(sql):
            name.append(row[0])
        return name

    def nome_paciente_progresso(self, nome):
        dados = []
        for row in db_obj2_cursor.execute("SELECT media_max_taragem, media_min_taragem, \
                                            acertos, erros, media_acertos, media_erros \
                                            FROM progresso WHERE paciente = ? ",[nome]):
            include = (row[0],row[1],row[2],row[3],row[4],row[5])
            dados.append(include)
        return dados

    def data_entry_progresso (self, nome, data, posimax, posimin, acertos, erros):
        pos_max, pos_min, tam, acerto, erro = [], [], [], [],[]

        db_obj2_cursor.execute('CREATE TABLE IF NOT EXISTS progresso (paciente text,\
                                data text, pressao_max integer, pressao_min integer, \
                                media_max_taragem float,media_min_taragem float, \
                                acertos integer, erros integer, media_acertos float,\
                                media_erros float)')
        hora = data.strftime("%d-%m-%Y %H:%M:%S")
        media_max_taragem, media_min_taragem, cont, media_acertos, media_erros = 0, 0, 0, 0, 0
        sql = 'SELECT pressao_max, pressao_min, media_acertos, media_erros FROM progresso WHERE paciente = ? '
        for row in db_obj2_cursor.execute(sql, [nome]):
            tam.append("1")
        for row in db_obj2_cursor.execute(sql, [nome]):

            pos_max.append(row[0])
            pos_min.append(row[1])
            acerto.append(row[2])
            erro.append(row[3])
            media_max_taragem += pos_max[cont]/(len(tam)+1)
            media_min_taragem += pos_min[cont]/(len(tam)+1)
            media_acertos += acerto[cont]/(len(tam)+1)
            media_erros += erro[cont]/(len(tam)+1)

            cont+=1
        media_max_taragem += posimax/(len(tam)+1)
        media_min_taragem += posimin/(len(tam)+1)
        media_acertos += acertos/(len(tam)+1)
        media_erros += erros/(len(tam)+1)
        tam.clear()
        db_obj2_cursor.execute("INSERT INTO progresso VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [nome, hora, posimax,
                                                                                        posimin, media_max_taragem,
                                                                                        media_min_taragem, acertos,
                                                                                        erros, media_acertos, media_erros])
        db_obj2.commit()

    def make_plot(self,nome):

        dados_max, dados_min, acertos, erros = [], [], [], []
        for row in db_obj2_cursor.execute("SELECT media_max_taragem, media_min_taragem, \
                                                acertos, erros, media_acertos, media_erros \
                                                FROM progresso WHERE paciente = ?", [nome]):
            dados_max.append(row[0])
            dados_min.append(row[1])
            acertos.append(row[2])
            erros.append(row[3])

        plt.plot(dados_min, color='red', label='Taragem Minima')
        plt.plot(dados_max, color='green', label='Taragem Maxima') # green

        plt.ylabel("Taragem")
        plt.xlabel("Sessão")
        plt.legend(['Taragem Maxima', 'Taragem Minima'], loc=0)
        plt.grid(True)
        plt.savefig("make_plot/max_min.png")
        plt.close()

        plt.plot(acertos, color='green', label='Taragem Minima')
        plt.plot(erros, color='red', label='Taragem Maxima') # green

        plt.ylabel("Porcentagem (%)")
        plt.xlabel("Sessão")
        plt.legend(['Acertos', 'Erros'], loc=0)
        plt.grid(True)
        plt.savefig("make_plot/acerto_erro.png")
        plt.close()

    def pont_grafico(self, nome):
        pont = []
        sql = 'SELECT pontos FROM graf_ideal WHERE nome_grafico = ?'
        for row in db_obj3_cursor.execute(sql, [nome]):
            pont.append(row[0])
        return pont

######## DEFINIÇÃO DAS IMAGENS ######

class coluna(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemcoluna = pygame.transform.scale(pygame.image.load('imagens/coluna.png'), (int(largura/9), int(altura/1.5)))
        self.imagemcoluna2 = pygame.transform.scale(pygame.image.load('imagens/coluna.png'), (int(largura/9), int(altura/1.5)))
        self.rect1, self.rect2 = self.imagemcoluna.get_rect(), self.imagemcoluna2.get_rect()

    def show(self, tela, pos_x, pos_y):
            tela.blit(self.imagemcoluna, self.rect1)
            self.rect1.centerx, self.rect1.centery = int(pos_x), int(pos_y)
            tela.blit(self.imagemcoluna2, self.rect2)
            self.rect2.centerx , self.rect2.centery = int(pos_x), int(pos_y + (altura//1.18)) #espaço de 150 entre as colunas

class preview(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.prev = pygame.transform.scale(pygame.movie.Movie("teste"), (int(largura/5), int(altura/5)))
        self.rect = self.prev.get_rect()

    def show(self, tela, pos_x, pos_y):
            tela.blit(self.prev, self.rect)
            self.rect.centerx, self.rect.centery = int(pos_x), int(pos_y)

class botao(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagembotao = pygame.transform.scale(pygame.image.load('imagens/bota.png'), (int(largura//1.6), int(altura//2.5)))
        self.imagembotao2 = pygame.transform.scale(pygame.image.load('imagens/bota.png'), (int(largura//1.2), int(altura//2.5)))
        self.imagembotao3 = pygame.transform.scale(pygame.image.load('imagens/bota_peq.png'), (int(largura//7), int(altura//7)))
        self.imagembotao4 = pygame.transform.scale(pygame.image.load('imagens/bota.png'), (int(largura//4), int(altura//2.5)))
        self.rect, self.rect2, self.rect3,self.rect4 = self.imagembotao.get_rect(), self.imagembotao2.get_rect(), \
                                                       self.imagembotao3.get_rect(), self.imagembotao4.get_rect()

    def show(self, tela, pos_x, pos_y, escolha):
            if escolha == 0:
                tela.blit(self.imagembotao, self.rect)
                self.rect.centerx, self.rect.centery = int(pos_x), int(pos_y)
            if escolha == 1:
                tela.blit(self.imagembotao2, self.rect2)
                self.rect2.centerx, self.rect2.centery = int(pos_x), int(pos_y)
            if escolha == 2:
                tela.blit(self.imagembotao3, self.rect3)
                self.rect3.centerx, self.rect3.centery = int(pos_x), int(pos_y)
            if escolha == 3:
                tela.blit(self.imagembotao4, self.rect4)
                self.rect4.centerx, self.rect4.centery = int(pos_x), int(pos_y)


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
        rect.centerx, rect.centery = int(pos_x), int(pos_y)


class letras(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/gameover.png', 'imagens/biofeedback.png',
                     'imagens/tempo.png', 'imagens/pontuação.png',
                     'imagens/record.png', 'imagens/restart.png',
                     'imagens/sair.png', 'imagens/start.png', 'imagens/pause.png']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        self.imgs[1] = pygame.transform.scale(self.imgs[1], (int(largura/1.6), int(altura/3.5)))
        self.imgs[2] = pygame.transform.scale(self.imgs[2], (int(largura//5), int(altura//7)))
        self.imgs[-2] = pygame.transform.scale(self.imgs[-2], (int(largura/4), int(altura/6.5)))
        self.rects = [img.get_rect() for img in self.imgs]

        self.imagemover, self.imagembio, self.imagemcont, self.imagempont, \
        self.imagemrec, self.imagemres, self.imagemsair, self.imagemstart,  \
        self.imagempause = self.imgs

    def show(self, tela, pos_x, pos_y, escolha):
        if 0 < escolha <= 9:
            img, rect = self.imgs[escolha - 1], self.rects[escolha - 1]
            tela.blit(img, rect)
            rect.centerx, rect.centery = int(pos_x), int(pos_y)

class fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/fund1.gif', 'imagens/fund2.gif']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        for i in range(len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i], (int(largura + 50), int(altura + 50)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagemfundo, self.imagemfundo2 = self.imgs

    def show(self, tela, pos_x, pos_y, imagem):
        img, rect = self.imgs[imagem], self.rects[imagem]
        tela.blit(img, rect)
        rect.centerx, rect.centery = int(pos_x), int(pos_y)

class grafmmae(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemmaxmin = pygame.transform.scale(pygame.image.load('make_plot/acerto_erro.png'), (int(largura/3.5), int(largura/4.8)))
        self.imagemacererro = pygame.transform.scale(pygame.image.load('make_plot/max_min.png'), (int(largura/3.5), int(largura/4.8)))
        self.rect1, self.rect2 = self.imagemmaxmin.get_rect(), self.imagemacererro.get_rect()

    def show(self, tela, pos_x, pos_y):
            tela.blit(self.imagemmaxmin, self.rect1)
            self.rect1.centerx, self.rect1.centery = int(pos_x), int(pos_y)
            tela.blit(self.imagemacererro, self.rect2)
            self.rect2.centerx , self.rect2.centery = int(pos_x + (altura*1.03)), int(pos_y) #espaço de 150 entre as colunas


class bubble (pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/bolha_maior.gif', 'imagens/bolha_menor.gif']
        self.imgs = [pygame.image.load(fn) for fn in filenames]
        self.imgs[0] = pygame.transform.scale(self.imgs[0], (int(largura/50), int(altura/30)))
        self.imgs[1] = pygame.transform.scale(self.imgs[1], (int(largura/100), int(altura/80)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagembolha, self.imagembolha2 = self.imgs

    def show(self, tela, pos_x, pos_y, nova):
        pos_x_v = [altura//2, altura//4,-(altura//8),0,-altura//2.6,-altura//2, \
                   altura//1.8,-(altura//1.2),-(altura//12),-altura//10]

        pos_y_v = [altura//17.5, altura//70, altura//5.3, altura//13, altura//20, \
                   altura//6,(altura//6),(altura//12),altura//10, altura//5]
        for i in range(len(self.imgs)*5):
            if i % 2 == 0:
                escolha = 0
            else:
                escolha = 1
            img, rect = self.imgs[escolha], self.rects[escolha]
            tela.blit(img, rect)
            rect.centerx, rect.centery = int(pos_x + nova + pos_x_v[i]), int(pos_y + nova + pos_y_v[i])


class fish (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        filenames = ['imagens/peixe3.png', 'imagens/peixe5.png', 'imagens/peixe1.png',
                     'imagens/peixe7.png', 'imagens/peixe4.png', 'imagens/peixe2.png',
                     'imagens/peixe9.png', 'imagens/peixe7.png', 'imagens/peixe8.png',
                     'imagens/peixe6.png']

        self.imgs = [pygame.image.load(fn) for fn in filenames]

        for i in range(0, len(filenames)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i], (int(largura/50), int(altura/30)))
        self.rects = [img.get_rect() for img in self.imgs]
        self.imagempeixe1, self.imagempeixe2, self.imagempeixe3, \
        self.imagempeixe4, self.imagempeixe5, self.imagempeixe6, \
        self.imagempeixe7, self.imagempeixe8, self.imagempeixe9, \
        self.imagempeixe10 = self.imgs

    def show(self, tela, pos_x, pos_y, nova, escolha):
        pos_x_v = [altura//25.6, altura//17, 0, altura//5.12, altura//2.56, \
                   altura//8, altura//12.8, altura//3.6, altura//2.13, 0]
        pos_y_v = [altura//5.12, -altura//5.12, altura//5.12, -altura//5.12, \
                   altura//5.12, -altura//5.12, altura//5.12, -altura//5.12, \
                   altura//5.12, -altura//5.12]
        if 0 < escolha <= 9:
            img, rect = self.imgs[escolha - 1], self.rects[escolha - 1]
            tela.blit(img, rect)
            rect.centerx, rect.centery = int(pos_x - pos_x_v[escolha]), int(pos_y + nova + pos_y_v[escolha])



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
            rect.centerx, rect.centery = int(pos_x), int(pos_y)

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
                     'imagens/Y.png', 'imagens/Z.png',
                     'imagens/A.png', 'imagens/B.png', 'imagens/C.png',
                     'imagens/D.png', 'imagens/E.png', 'imagens/F.png',
                     'imagens/G.png', 'imagens/H.png', 'imagens/I.png',
                     'imagens/J.png','imagens/K.png', 'imagens/L.png',
                     'imagens/M.png','imagens/N.png', 'imagens/O.png',
                     'imagens/P.png','imagens/Q.png', 'imagens/R.png',
                     'imagens/S.png','imagens/T.png', 'imagens/U.png',
                     'imagens/V.png','imagens/W.png', 'imagens/X.png',
                     'imagens/Y.png', 'imagens/Z.png', 'imagens/doispontos.png']


        self.imgs = [pygame.image.load(fn) for fn in filenames]
        for i in range(0, len(filenames)):
            if i < 26:
                self.imgs[i] = pygame.transform.scale(self.imgs[i],(int(largura/13), int(altura/8)))
            else:
                 self.imgs[i] = pygame.transform.scale(self.imgs[i],(int(largura/10), int(altura/6)))
        self.imgs[4] = pygame.transform.scale(self.imgs[4],(int(largura/13.5), int(altura/8)))
        self.imgs[30] = pygame.transform.scale(self.imgs[30],(int(largura/10.5), int(altura/6)))
        self.imgs[52] = pygame.transform.scale(self.imgs[52],(int(largura/8), int(altura/7)))

        self.rects = [img.get_rect() for img in self.imgs]

        self.imagemA, self.imagemB, self.imagemC, self.imagemD, self.imagemE, self.imagemF, \
        self.imagemG, self.imagemH, self.imagemI, self.imagemJ, self.imagemK, self.imagemL, \
        self.imagemM, self.imagemN, self.imagemO, self.imagemP, self.imagemQ, self.imagemR, \
        self.imagemS, self.imagemT, self.imagemU, self.imagemV, self.imagemW, self.imagemX, \
        self.imagemY, self.imagemZ, \
        self.imagem2A, self.imagem2B, self.imagem2C, self.imagem2D, self.imagem2E, self.imagem2F, \
        self.imagem2G, self.imagem2H, self.imagem2I, self.imagem2J, self.imagem2K, self.imagem2L, \
        self.imagem2M, self.imagem2N, self.imagem2O, self.imagem2P, self.imagem2Q, self.imagem2R, \
        self.imagem2S, self.imagem2T, self.imagem2U, self.imagem2V, self.imagem2W, self.imagem2X, \
        self.imagem2Y, self.imagem2Z, self.imagem2pontos = self.imgs

    def show(self, tela, quad_x, quad_y, palavra, tamanho):
        cont = 0
        pos_y = int(posicao(quad_x, quad_y,"y"))
        if tamanho == 0:
            for caracter in palavra:
                cont += 1
                escolha = ord(caracter)-65
                if caracter==' ':
                    cont = cont + 0.001
                elif caracter=='E':
                    img, rect = self.imgs[escolha], self.rects[escolha]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/30), int(pos_y + 3)
                elif caracter==':':
                    img, rect = self.imgs[52], self.rects[52]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/30), int(pos_y - 1)
                else:
                    img, rect = self.imgs[escolha], self.rects[escolha]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/30), int(pos_y)
        else:
            for caracter in palavra:
                cont += 1
                escolha = ord(caracter)- 65 + 26
                if caracter==' ':
                    cont = cont + 0.001
                elif caracter=='E':
                    img, rect = self.imgs[escolha], self.rects[escolha]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/23), int(pos_y + 3)
                elif caracter==':':
                    img, rect = self.imgs[52], self.rects[52]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/30), int(pos_y + 3)
                else:
                    img, rect = self.imgs[escolha], self.rects[escolha]
                    tela.blit(img, rect)
                    rect.centerx, rect.centery = int(posicao(quad_x, quad_y,"x") + largura*cont/23), int(pos_y)


class coral (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemcor1 = pygame.transform.scale(pygame.image.load('imagens/alga.png'), (int(largura/7), int(altura/5)))
        self.imagemcor2 = pygame.image.load('imagens/concha_pausa.png')
        self.imagemcor3 = pygame.image.load('imagens/concha_musica.png')

        self.rect1, self.rect2, self.rect3 = self.imagemcor1.get_rect(), self.imagemcor2.get_rect(), self.imagemcor3.get_rect()

    def show(self, tela, pos_x, pos_y, escolha):
        if escolha == 1:
            tela.blit(self.imagemcor1, self.rect1)
            self.rect1.centerx, self.rect1.centery = int(pos_x), int(pos_y)
        if escolha == 2:
            tela.blit(self.imagemcor2, self.rect2)
            self.rect2.centerx, self.rect2.centery = int(pos_x), int(pos_y)
        if escolha == 3:
            tela.blit(self.imagemcor3, self.rect3)
            self.rect3.centerx, self.rect3.centery = int(pos_x), int(pos_y)

def posicao(quad_x, quad_y, eixo):
    M_lin = M_lin_col[quad_y]
    posi = M_lin[quad_x]
    if eixo == 'x':
        return((posi[0]+posi[2])/2)
    if eixo == 'y':
        return((posi[1]+posi[3])/2)

def gameover(pont, temp, paciente, data, tratamento, id_temp, id_pont):

    
    ## TODAS AS IMAGENS DEVEM SER CARREGADAS ANTES DO LOOP PARA EVITAR QUE ELAS APAREÇAM EM POSICOES ERRADAS NO INICIO DA FUNCAO
    inter = [(-100, largura), (-100, largura), (-100, largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]


    pos_buble_y, let, let2, let3, let4, col, cor, posibot = 700, letras(), letras(), letras(), letras(), coluna(), coral(), 11
    ariel, fund, bolhas, dez, uni = sereia(), fundo(), bubble(), numeros(), numeros()
    teste, teste2, bot = letr(), letr(), botao()


    ##### CARREGANDO TODAS AS IMAGENS UTILIZADAS NA FUNÇÂO####

    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
    cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
    col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
    col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
    ariel.show(tela,  posicao(18, 27,"x"), posicao(18, 4,"y"), 0)
    ariel.show(tela,  posicao(18, 27,"x"), posicao(18, 4,"y"), 1)
    bot.show(tela, posicao(11, 11,"x"), posicao(11, posibot,"y"), 0)
    teste.show(tela, 11, 11, "INICIO", 1)
    teste.show(tela, 14, 16, "MODO", 1)
    teste.show(tela, 10, 21, "DETALHES", 1)
    teste.show(tela, 14, 26, "SAIR", 1)
    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    pygame.display.update()

    final = True

    while final:
        ###### INTERFACE FUNDO ###
        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
        cor.show(tela, posicao(35, 9,"x") + largura//36, posicao(35, 10,"y"), 1)
        cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
        col.show(tela, posicao(35, 23,"x") + largura//36, posicao(35, 23,"y"))
        col.show(tela, posicao(0, 23,"x"), posicao(0, 23,"y"))
        bot.show(tela, posicao(17, 17,"x") + altura//45, posicao(posibot, posibot,"y"), 0)
        teste.show(tela, 12, 11, "INICIO", 1)
        teste.show(tela, 14, 16, "MODO", 1)
        teste.show(tela, 11, 21, "DETALHES", 1)
        teste.show(tela, 10, 26, "HISTORICO", 1)
        teste.show(tela, 14, 31, "SAIR", 1)

        ################################
        if pos_buble_y == altura:
            nova = randint(-300, 300)
            nova2 = randint(-300, 300)

        if pos_buble_y<-altura*1.5:
            pos_buble_y = altura-((altura % 100)%10)

        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.10, nova - nova2)
        pos_buble_y -= 5


        ########## POSICAO E MOVIMENTO DA SEREIA #######
        if (pos_buble_y % 15)==0:
            posi = 0
        else:
            posi = 1
        ariel.show(tela,  posicao(18, 27,"x"), posicao(18, 4,"y"), posi)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final = False
            elif event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                if event.key == pygame.K_UP:
                    posibot -= 5
                    if posibot <= 11:
                        posibot = 11
                elif event.key == pygame.K_DOWN:
                    posibot += 5
                    if posibot >= 31:
                        posibot = 31
                elif event.key == pygame.K_RETURN:
                    if posibot == 11:
                        pygame.mixer.Sound.stop(Inicio_sound)
                        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                        pygame.display.update()
                        final = inicio()
                    elif posibot == 16:
##                        pygame.mixer.music.stop()
                        final = modo()
                    elif posibot == 21:
                        date = data.strftime("%d-%m-%Y %H:%M:%S")
                        resultados(pont, temp, paciente, date, tratamento, id_temp, id_pont)
                    elif posibot == 26:
                        historico()
                    else:
                        final = False
        tempo.tick(25)
        pygame.display.update()
    return(False)


############################################################################################################################################

def inicio():
    ########## Criando o BD para uso pelo resto do código
    global bd_geral

    bd_geral = PacienteDados()

    ################PARA MOTIVOS DE TESTE
    posimax = 999
    posimin = 10
    ## TODAS AS IMAGENS DEVEM SER CARREGADAS ANTES DO LOOP PARA EVITAR QUE ELAS APAREÇAM EM POSICOES ERRADAS NO INICIO DA FUNCAO
    inter = [(-100, largura), (-100, largura), (-100, largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]


    pos_buble_y, let, let2, let3, let4, col, cor, posibot = 700, letras(), letras(), letras(), letras(), coluna(), coral(), 11
    ariel, fund, bolhas, dez, uni = sereia(), fundo(), bubble(), numeros(), numeros()
    teste, teste2,teste3, bot = letr(), letr(), letr(), botao()
    pygame.mixer.Sound.play(Inicio_sound, loops = -1)

    #####CARREGANDO TODAS AS IMAGENS UTILIZADAS NA FUNÇÂO####

    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    let.show(tela, posicao(18, 3,"x"), posicao(18, 3,"y"), 2)
    cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
    cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
    col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
    col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
    ariel.show(tela,  posicao(30, 27,"x"), posicao(18, 30,"y"), 0)
    ariel.show(tela,  posicao(30, 27,"x"), posicao(18, 30,"y"), 1)
    bot.show(tela, posicao(17, 17,"x")+altura//45, posicao(posibot, posibot,"y"), 0)
    teste.show(tela, 11, 11, "TARAGEM", 1 )
    teste.show(tela, 14, 16, "MODO", 1)
    teste.show(tela, 10, 21, "HISTORICO", 1)
    teste.show(tela, 10, 26, "PROGRESSO", 1)
    teste.show(tela, 14, 31, "SAIR", 1)
    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    pygame.display.update()

    menu = True


    while menu:
        ###### INTERFACE FUNDO ###

        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
        cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
        cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
        col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
        col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
        bot.show(tela, posicao(17, 17,"x")+altura//45, posicao(posibot, posibot,"y"), 0)
        teste.show(tela, 11, 11, "TARAGEM", 1 )
        teste.show(tela, 14, 16, "MODO", 1)
        teste.show(tela, 10, 21, "HISTORICO", 1)
        teste.show(tela, 10, 26, "PROGRESSO", 1)
        teste.show(tela, 14, 31, "SAIR", 1)

        ############## POSIÇÃO DAS BOLHAS ##################
        if pos_buble_y == altura:

            nova = randint(-300,300)
            nova2 = randint(-300,300)
            nova = randint(-300, 300)
            nova2 = randint(-300, 300)

        if pos_buble_y<-altura*1.5:
            pos_buble_y = altura-((altura % 100)%10)

        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.10, nova - nova2)
        pos_buble_y -= 5

        ###### INTERFACE LETRAS #############

        let.show(tela, posicao(18, 3,"x"), posicao(18, 3,"y"), 2) #Biofeedback

        ########## POSICAO E MOVIMENTO DA SEREIA #######
        if (pos_buble_y % 15)==0:
            posi = 0
        else:
            posi = 1

        ariel.show(tela,  posicao(30, 27,"x"), posicao(18, 30,"y"), posi)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                if event.key == pygame.K_UP:
                    posibot -= 5
                    if posibot <= 11:
                        posibot = 11
                elif event.key == pygame.K_DOWN:
                    posibot += 5
                    if posibot >= 31:
                        posibot = 31
                elif event.key == pygame.K_RETURN:
                    if posibot == 11:
                        pygame.mixer.Sound.stop(Inicio_sound)
                        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                        pygame.display.update()
                        menu = taragem()
                    elif posibot == 16:
                        #cont = time.time()
                        #pygame.mixer.music.stop()
                    ############### COLA AQUI POLI PORA V

                    ###############
                        if len(n_paciente) == 0:
                            janela = True

                            while janela:

                                sg.theme('DarkBlue10')

                                missing_taragem_warning_layout = [[sg.Text('Nenhuma taragem foi identificada.'\
                                    ' É recomendável sempre realizar a taragem antes de uma nova sessão' \
                                    'de exercícios. Selecione uma taragem anterior ou volte ao menu para '\
                                    'fazer uma nova.', justification = 'center' ,size=(49,5), font=("Arial", 18))], \
                                        [sg.Button("Selecionar taragem", size=(20,1), font=("Arial", 15)),
                                        sg.Button("Realizar nova taregem", size=(20,1), font=("Arial", 15)), \
                                        sg.Button("Voltar", size=(20,1), font=("Arial", 15))]]

                                window = sg.Window('', missing_taragem_warning_layout, no_titlebar=True)
                                event, val = window.read()

                                if event in (None, 'Voltar'):
                                    window.close()
                                    janela = False

                                elif event in ('Selecionar taragem'):
                                    window.close()
                                    janela = False
                                    menu = modo()

                                else:
                                    window.close()
                                    janela = False
                                    menu = taragem()

                        else:
                            cont = time.time()
##                            pygame.mixer.music.stop()
                            menu = modo()

                    elif posibot == 21:
                        historico()

                    elif posibot == 26:
                        menu = progresso()

                    else:
                        menu = False
        ##########
        pygame.display.update()
        tempo.tick(20)

def modo():


    inter=[(-100, largura), (-100, largura), (-100, largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    posibotao=[11, 16, 21, 26]

    pos_buble_y, col, cor, graf, posibot, rolagem, unid, deze, \
                 posibottem, check, move, moveseri_x, moveseri_y, \
                 posi = 700, coluna(), coral(), 0, 0, \
                 0, 0, 0, 0, 0, 0, 0, 0, 0

    fund, bolhas, bot, texto, texto2, uni, dez, ariel = fundo(), bubble(),\
                                                 botao(), letr(), \
                                                 letras(), numeros(),\
                                                 numeros(), sereia()
    ############Vídeos de Preview


    pygame.mixer.Sound.play(Inicio_sound, loops = -1)
    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    cor.show(tela, posicao(35, 9,"x") + largura//36, posicao(35, 10,"y"), 1)
    cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
    col.show(tela, posicao(35, 23,"x") + largura//36, posicao(35, 24,"y"))
    col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
    bot.show(tela, posicao(12, 12,"x") + altura//45, posicao(11, posibotao[posibot],"y"), 1)
    bot.show(tela, posicao(18, 18,"x"), posicao(18, 5,"y") + altura//240, 2)
    texto2.show(tela, posicao(18, 18,"x")+ largura//80, posicao(18, 3,"y"), 3)
    for conta in range(10):
        dez.show(tela, posicao(18, 18,"x"), posicao(18, 5,"y"), conta)
        uni.show(tela, posicao(18, 18,"x") + largura//50, posicao(18, 5,"y"), conta)
        fund.show(tela, posicao(18, 18, "x"), posicao(18, 18, "y"), 1)
    texto.show(tela, 3, 11, "CONTRACAO F UNI", 0)
    texto.show(tela, 2, 16, "CONTRACAO TONICA", 0)
    texto.show(tela, 5, 21, "RELAXAMENTO", 0)
    texto.show(tela, 3, 26, "TRAB ASCENDENTE", 0)
    texto.show(tela, 3, 11, "TRAB CONCENTRICO", 0)
    texto.show(tela, 3, 16, "TRAB EXCENTRICO", 0)
    texto.show(tela, 5, 21, "TRAB LIVRE", 0)
    texto.show(tela, 3, 26,  "TRAB ISOMETRICO", 0)
    preview = cv2.VideoCapture("videos/Contração Fasica Uniforme.mp4")
    preview = cv2.VideoCapture("videos/tenor.gif")
    preview = cv2.VideoCapture("videos/tenor2.gif")
    ariel.show(tela, posicao(34, 18, "x"), posicao(18, 3, "y"), 1)
    fund.show(tela, posicao(18, 18, "x"), posicao(18, 18, "y"), 1)
    pygame.display.update()

    ## SELEÇÃO DE PACIENTE ###

    sel = True
    ret = True
    mod = True

    while mod:
        ## SELEÇÃO DE PACIENTE ###
        while sel:
            sg.theme('DarkBlue10')
            sel_paciente = bd_geral.paciente_select("Taragem")

            if len(sel_paciente)==0:
                janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                event3, val3 = window3.read()
                if event3 in (None, 'OK'):
                    window3.close()
                    sel=False
                    mod = inicio()
            else:

                janela_sel_paciente = [[sg.Text('Selecione um paciente',justification='center', size=(60,1), font=("Arial", 15))],\
                                      [sg.Combo(sel_paciente, size=(60,1), font=("Arial", 15))], \
                                      [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                      sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                jan_sel_paciente = sg.Window('Selecionar Paciente', janela_sel_paciente, no_titlebar=True)
                event1, usuario = jan_sel_paciente.read()
                if event1 in ('Selecionar'):
                    n_paciente.clear()
                    idade_paciente.clear()
                    trata_paciente.clear()
                    posmin.clear()
                    posmax.clear()
                    n_paciente.append(usuario[0])
                    maxmin = bd_geral.pressao_maxmin_select(usuario[0])
                    posmin.append(maxmin[1])
                    posmax.append(maxmin[0])
                    idade_paciente.append(bd_geral.idade_select(n_paciente[0]))
                    trata_paciente.append(bd_geral.trataId_select(n_paciente[0], idade_paciente[0]))

                    if usuario[0]=="":
                        n_paciente.clear()
                        graf_selec.clear()
                        jan_sel_paciente.close()
                    else:
                        jan_sel_paciente.close()
                        sel = False

                elif event1 in (None, "Cancelar"):
                    n_paciente.clear()
                    idade_paciente.clear()
                    trata_paciente.clear()
                    posmin.clear()
                    posmax.clear()
                    jan_sel_paciente.close()
                    sel = False
                    mod = inicio()

        ###### INTERFACE FUNDO ###

        fund.show(tela, posicao(18, 18, "x"), posicao(18, 18,"y"), 1)
        cor.show(tela, posicao(35, 9,"x")+largura//36 + move, posicao(35, 10,"y"), 1)
        cor.show(tela, posicao(0, 9,"x")+ move, posicao(0, 10,"y"), 1)
        col.show(tela, posicao(35, 23,"x")+largura//36 + move, posicao(35, 24,"y"))
        col.show(tela, posicao(0, 23,"x") + move, posicao(0, 24,"y"))
        ariel.show(tela, posicao(33, 18, "x") + moveseri_x, posicao(18, 3, "y") + moveseri_y, posi)
        if check == 0:
            bot.show(tela, posicao(12, 12,"x") + altura//40, posicao(11, posibotao[posibot],"y"), 1)
        texto2.show(tela, posicao(18, 18,"x") + largura//80 + move, posicao(18, 3,"y"), 3)
        if check == 1:
            bot.show(tela, posicao(18, 18,"x") + posibottem, posicao(18, 5,"y") + altura//240, 2)
        dez.show(tela, posicao(18, 18,"x")+ move, posicao(18, 5,"y"), deze)
        uni.show(tela, posicao(18, 18,"x") + largura//50 + move, posicao(18, 5,"y"), unid)

        if rolagem == 0 and check < 2:
            texto.show(tela, 3, 11, "CONTRACAO F UNI", 0)
            texto.show(tela, 2, 16, "CONTRACAO TONICA", 0)
            texto.show(tela, 5, 21, "RELAXAMENTO", 0)
            texto.show(tela, 3, 26, "TRAB ASCENDENTE", 0)
        elif rolagem == 1 and check < 2:
            texto.show(tela, 2, 11, "TRAB CONCENTRICO", 0)
            texto.show(tela, 3, 16, "TRAB EXCENTRICO", 0)
            texto.show(tela, 5, 21, "TRAB LIVRE", 0)
            texto.show(tela, 3, 26,  "TRAB ISOMETRICO", 0)

        ################################
        if pos_buble_y == altura:
            nova = randint(-300, 300)
            nova2 = randint(-300, 300)

        if pos_buble_y<-altura*1.5:
            pos_buble_y = altura-((altura % 100)%10)

        bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.25, nova2)
        bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.10, nova - nova2)
        pos_buble_y -= 5

        if (pos_buble_y % 15)==0:
            posi = 0
        else:
            posi = 1

        mouse = pygame.mouse.get_pos() #pos=[x, y]
        click = pygame.mouse.get_pressed() #pressed=[bdir, centro, besq]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mod = False

            elif event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                if event.key == pygame.K_UP:
                    if check == 0:
                        posibot -= 1
                        if posibot < 0:
                            if rolagem == 0:
                                posibot = 0
                            else:
                                rolagem = 0
                                posibot = 3
                    elif check == 1 and posibottem == largura//50:
                        unid += 1
                        if unid > 9:
                            unid = 9
                    elif check == 1 and posibottem == 0:
                        deze+=1
                        if deze > 9:
                            deze = 9

                elif event.key == pygame.K_DOWN:
                    if check == 0:
                        posibot += 1
                        if posibot > 3:
                            if rolagem == 0:
                                posibot = 0
                                rolagem = 1
                            else:
                                posibot = 3
                    elif check == 1 and posibottem == largura//50:
                        unid -= 1
                        if unid < 0:
                            unid = 0
                    elif check == 1 and posibottem == 0:
                        deze -= 1
                        if deze < 0:
                            deze = 0
                elif event.key == pygame.K_LEFT:
                    posibottem = 0
                elif event.key == pygame.K_RIGHT:
                    posibottem = largura//50
                elif event.key == pygame.K_BACKSPACE:
                    check -= 1
                    if check < 0:
                        check = 0
                        n_paciente.clear()
                        mod = inicio()

                elif event.key == pygame.K_RETURN:
                    check += 1
                    if check > 2:
                        check = 2

        if posibot==0 and check == 0 and rolagem == 0:
            preview = cv2.VideoCapture("videos/Contração Fasica Uniforme.mp4")
        elif posibot==1 and check == 0 and rolagem == 0:
            preview = cv2.VideoCapture("videos/tenor2.gif")
        elif posibot==2 and check == 0 and rolagem == 0:
            preview = cv2.VideoCapture("videos/tenor.gif")
        elif posibot==3 and check == 0 and rolagem == 0:
            preview = cv2.VideoCapture("videos/tenor2.gif")
        elif posibot==0 and check == 0 and rolagem == 1:
            preview = cv2.VideoCapture("videos/tenor.gif")
        elif posibot==1 and check == 0 and rolagem == 1:
            preview = cv2.VideoCapture("videos/tenor2.gif")
        elif posibot==2 and check == 0 and rolagem == 1:
            preview = cv2.VideoCapture("videos/tenor.gif")
        elif posibot==3 and check == 0 and rolagem == 1:
            preview = cv2.VideoCapture("videos/tenor2.gif")

        if check == 2:
            if move > -largura*1.4:
                move -= 10
                moveseri_x -= 10
                moveseri_y += 10
                if moveseri_x < -largura//1.5:
                    moveseri_x += 10
                if moveseri_y > altura//2:
                    moveseri_y -= 10
            else:
                tempototal = ((deze * 10) + unid) * 60
                if rolagem == 0:
                        pygame.mixer.Sound.stop(Inicio_sound)
                        graf = posibot + 1
                        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                        pygame.display.update()
##                        pygame.mixer.music.stop()
                        mod = grafico(graf, tempototal)
                else:
                        pygame.mixer.Sound.stop(Inicio_sound)
                        graf = posibot + 5
                        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                        pygame.display.update()
##                        pygame.mixer.music.stop()
                        mod = grafico(graf, tempototal)
        if check == 1:
            try:
                ret, frame = preview.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.swapaxes(frame,0,1)
                frame = cv2.resize(frame, (int(altura/4), int(largura/4)))
                preview_surface = pygame.surfarray.make_surface(frame)
                tela.blit(preview_surface, (int(2.7/4*largura), int(altura/4)))
            except:
                cv2.destroyAllWindows()
                tempo.tick(30)
        if check == 2 or check == 0:
            tempo.tick(30)
        pygame.display.update()

def taragem():

    global posimax
    global posimin

    inter=[(-100, largura), (-100, largura), (-100, largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]
    cont =  [letras()]*6 + [numeros()]*7 + [coluna(), coral(), sereia(),
             fundo(), bubble(), 700, 350, 350, 0, 0, 0, 0, altura,
             True, 2]
    pmax1, pmax2, pmax3, pmin1, pmin2, pmin3, uni, posimaxcen, posimaxdez, \
    posimaxuni, posimincen, posimindez, posiminuni, col, cor, ariel, fund, \
    bolhas, pos_buble_y, posi, posi2, contagem2, contagem3, check, \
    posimax, posimin, tara, velocidade_y = [i for i in cont]
    test, test2, test3 = letr(),letr(),letr()
    dt = datetime.now()

    tara = True
    janelamax = True

    test.show(tela, 7, 12, "CONTRAIA O MAXIMO", 0)
    test2.show(tela, 8, 12, "RELAXE O MAXIMO", 0)
    test3.show(tela, 12, 14, "QUE PUDER", 0)
    test3.show(tela, 3, 5, "MAX", 1)
    test3.show(tela, 3, 11, "MIN", 1)
    cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
    col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
    ariel.show(tela, posicao(18, 18,"x"), altura - posi, 0)
    ariel.show(tela, posicao(18, 18,"x"), altura - posi, 1)

    sg.theme('DarkBlue10')


    while janelamax:

        janela_perfil = [[sg.Button('Selecionar Perfil Existente', size=(50,1), font=("Arial", 15))],
                         [sg.Button('Adicionar Novo Perfil',  size=(50,1), font=("Arial", 15))],
                         [sg.Button('Deletar Taragem',  size=(50,1), font=("Arial", 15))],
                         [sg.Button('Voltar', size=(50,1), font=("Arial", 15))],
                         [sg.Text('ATENÇÃO! Não realize duas taragens seguidas, espere pelo menos 10 min antes de continuar.'\
                         ' Consulte o manual de uso ou seu fisioterapeuta para maiores informações.', justification = 'c', size=(40,6), font=("Arial", 13))]]
        jan_perfil = sg.Window('Seleção de Perfil', janela_perfil, no_titlebar=True, size=(400,265))
        event, val = jan_perfil.read()
        janela = True

        if event in (None, 'Voltar'):
            jan_perfil.close()
            janelamax = False
            tara = inicio()

        elif event in ('Deletar Taragem'):
            jan_perfil.close()
            perfis = bd_geral.paciente_select("Taragem")
            if len(perfis)==0:
                janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                window4 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                event4, val4 = window4.read()
                if event4 in (None, 'OK'):
                    window4.close()

            else:
                janela_del_perfil = [[sg.Combo(perfis, size=(60,1), font=("Arial", 15))], \
                                     [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                      sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                jan_del_perfil = sg.Window('Selecionar Perfil', janela_del_perfil, no_titlebar=True)
                event, usuario = jan_del_perfil.read()
                n_paciente.append(usuario[0])
                if event in (None, 'Cancelar'):
                    jan_del_perfil.close()
                    n_paciente.clear()
                    idade_paciente.clear()
                    trata_paciente.clear()

                elif event in ('Selecionar'):

                    if n_paciente[0] == "" or len(n_paciente[0]) == 0:
                        n_paciente.clear()
                        jan_del_perfil.close()
                        janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                        window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                        event3, val3 = window3.read()
                        if event3 in (None, 'OK'):
                            window3.close()

                    else:
                        jan_del_perfil.close()
                        bd_geral.delete_row_from_table(n_paciente[0])
                        n_paciente.clear()
                        janela = False
                        tara = False


        elif event in ('Adicionar Novo Perfil'):

            jan_perfil.close()

            while janela:

                layout = [  [sg.Text('Nome do Paciente', size=(20,1), font=("Arial", 15)), sg.InputText(size=(40,1),font=("Arial", 15))],
                    [sg.Text('Idade', size=(20,1), font=("Arial", 15)), sg.InputText(size=(40,1),font=("Arial", 15))],
                    [sg.Text('Tratamento', size=(20,1), font=("Arial", 15)), sg.InputText(size=(40,1),font=("Arial", 15))],
                    [sg.Button('Salvar', size=(30,1), font=("Arial", 15)), sg.Button('Cancelar', size=(30,1), font=("Arial", 15))] ]

                window = sg.Window('Biofeedback - Dados do Paciente', layout, no_titlebar=True)

                event, val = window.read()

                if event in (None, 'Cancelar'):
                    window.close()
                    janela = False
                    tara = False

                elif event in ('Salvar'):
                    window.close()
                    check_nomes = bd_geral.paciente_select("Taragem")
                    for nome in check_nomes:
                        if val[0] == nome or len(val[0])==0 or val[0]=='':
                            check=1
                            janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                            window2 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                            event2, val2 = window2.read()
                            if event2 in (None, 'OK'):
                                window2.close()
                                break
                                tara = False
                        else:
                            check = 0
                    if check == 0:

                        janela = False
                        janelamax = False
                        tara = True


            if tara == True:
                dt = datetime.now()
                n_paciente.clear()
                idade_paciente.clear()
                trata_paciente.clear()
                n_paciente.append(val[0])
                idade_paciente.append(val[1])
                trata_paciente.append(val[2])
                bd_geral.data_entry(n_paciente[0], idade_paciente[0], trata_paciente[0], dt, 0, 0, "DEFAULT", "DEFAULT", "DEFAULT", "DEFAULT", "DEFAULT", "Taragem")

                if n_paciente[0] == '':
                    window.close()
                    n_paciente.clear()
                    tara = inicio()
                ## Subir mensagem de erro se tiver letras ou outros caracteres na idade (implementar)
                else:
                    pass
                window.close()

        elif event in (None, 'Selecionar Perfil Existente'):

            jan_perfil.close()

            perfis = bd_geral.paciente_select("Taragem")
            if len(perfis)==0:
                janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                event3, val3 = window3.read()
                if event3 in (None, 'OK'):
                    window3.close()

            else:
                janela_sel_perfil = [[sg.Combo(perfis, size=(60,1), font=("Arial", 15))], \
                                     [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                      sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                jan_sel_perfil = sg.Window('Selecionar Perfil', janela_sel_perfil, no_titlebar=True)
                event, usuario = jan_sel_perfil.read()
                if event in (None, 'Cancelar'):
                    jan_sel_perfil.close()
                    n_paciente.clear()
                    idade_paciente.clear()
                    trata_paciente.clear()

                elif event in ('Selecionar'):
                    n_paciente.clear()
                    n_paciente.append(usuario[0])
                    if n_paciente[0] == "" or len(n_paciente) == 0:
                        n_paciente.clear()
                        jan_sel_perfil.close()
                        janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                        window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                        event3, val3 = window3.read()
                        if event3 in (None, 'OK'):
                            window3.close()

                    else:
                        idade_paciente.clear()
                        trata_paciente.clear()
                        jan_sel_perfil.close()
                        idade_paciente.append(bd_geral.idade_select(n_paciente[0]))
                        trata_paciente.append(bd_geral.trataId_select(n_paciente[0], idade_paciente[0]))

                        janelamax = False
#####################

    for conta in range(10):
        uni.show(tela, -100, -100, conta)
        posimaxcen.show(tela, -100, -100, conta)
        posimaxdez.show(tela, -100, -100, conta)
        posimaxuni.show(tela, -100, -100, conta)
        posimincen.show(tela, -100, -100, conta)
        posimindez.show(tela, -100, -100, conta)
        posiminuni.show(tela, -100, -100, conta)

    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    pygame.display.update()

    while tara:

        while (contagem2 <= 10):
            fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
            cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
            cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
            col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
            col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
            if contagem2 == 0 and check == 0:
                for contagem in range(3, 0,-1):
                    startcont =  time.time()
                    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                    while time.time()-startcont < 1:
                        test.show(tela, 7, 12, "CONTRAIA O MAXIMO", 0)
                        test3.show(tela, 12, 14, "QUE PUDER", 0)
                        uni.show(tela, int(largura/2), int(altura/2), contagem)
                        pygame.display.update()
                startcont = time.time()
                #fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)

                #pygame.display.update()
                #while time.time()-startcont < 4:
                #    pass
                #fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                check = 1
                start = time.time()
            test3.show(tela, 3, 5, "MAX", 1)
            if pos_buble_y == altura:
                nova = randint(-300, 300)
                nova2 = randint(-300, 300)

            if pos_buble_y<-altura*1.5:
                pos_buble_y = altura-((altura % 100)%10)

            bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
            bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.25, nova2)
            bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.10, nova - nova2)
            pos_buble_y -= 5

            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos = int(ser.read(ser.inWaiting()))
            #    print(posi)

            if (pos_buble_y % 15)==0:
                escolha = 1
            else:
                escolha = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tara = False
                if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                    if event.key == pygame.K_UP:
                        velocidade_y = 10
                else:
                    velocidade_y = -10

            posi += velocidade_y
            if posi>= 1000:
                posi = 999
            if posi <= 0:
                posi = 10
            ariel.show(tela, posicao(18, 18,"x"), altura - posi, escolha)
            if posi > posimax:
                posimax = posi

            posimaxcen.show(tela, posicao(5, 8,"x"), posicao(3, 8,"y"), posimax//100)
            posimaxdez.show(tela, posicao(6, 8,"x"), posicao(3, 8,"y"), (posimax % 100)//10)
            posimaxuni.show(tela, posicao(7, 8,"x"), posicao(3, 8,"y"), (posimax % 100)%10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return(False)
                    tara = False
            contagem2 = time.time()-start
            pygame.display.update()
            tempo.tick(25)
        check = 0
        while (contagem3 <= 12):

            fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
            cor.show(tela, posicao(35, 9,"x")+largura//36, posicao(35, 10,"y"), 1)
            cor.show(tela, posicao(0, 9,"x"), posicao(0, 10,"y"), 1)
            col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
            col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))

            if contagem3 == 0 and check == 0:
                for contagem in range(3, 0,-1):
                    startcont =  time.time()
                    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                    while time.time()-startcont < 1:
                        test2.show(tela, 8, 12, "RELAXE O MAXIMO", 0)
                        test3.show(tela, 12, 14, "QUE PUDER", 0)
                        #uni.show(tela, int(largura/2), int(altura/2), contagem)
                        pygame.display.update()
                startcont = time.time()
                check = 1
                start = time.time()
            test3.show(tela, 3, 5, "MAX", 1)
            test3.show(tela, 3, 11, "MIN", 1)

            if pos_buble_y == altura:
                nova = randint(-300, 300)
                nova2 = randint(-300, 300)

            if pos_buble_y<-altura*1.5:
                pos_buble_y = altura-((altura % 100)%10)

            bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
            bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.25, nova2)
            bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.10, nova - nova2)
            pos_buble_y -= 5

            #Essa parte vai ser usada só com a ESP
            #if (ser.inWaiting()>0):
            #    pos = int(ser.read(ser.inWaiting()))
            #    print(posi)

            if (pos_buble_y % 15)==0:
                escolha = 1
            else:
                escolha = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tara = False
                if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                    if event.key == pygame.K_UP:
                        velocidade_y = 10
                else:
                    velocidade_y =- 10

            posi2 += velocidade_y
            if posi2 >= 1000:
                posi2 = 999
            if posi2 <= 0:
                posi2 = 10
            ariel.show(tela, posicao(18, 18,"x"), altura - posi2, escolha)
            if posi2 < posimin:
                posimin = posi2

            posimaxcen.show(tela, posicao(5, 8,"x"), posicao(5, 8,"y"), posimax//100)
            posimaxdez.show(tela, posicao(6, 8,"x"), posicao(6, 8,"y"), (posimax % 100)//10)
            posimaxuni.show(tela, posicao(7, 8,"x"), posicao(7, 8,"y"), (posimax % 100)%10)
            posimincen.show(tela,  posicao(5, 14,"x"), posicao(5, 14,"y"), posimin//100)
            posimindez.show(tela,  posicao(6, 14,"x"), posicao(6, 14,"y"), (posimin % 100)//10)
            posiminuni.show(tela, posicao(7, 14,"x"), posicao(7, 14,"y"), (posimin % 100)%10)

            pygame.display.update()
            tempo.tick(25)
            contagem3 = time.time()-start

        pygame.display.update()
        posmax.append(posimax)
        posmin.append(posimin)
        if tara == True:
            dt = datetime.now()
            bd_geral.atualizar_dados(n_paciente[0], dt, posimax, posimin)

            #bd_geral.paciente_gravar_taragem(n_paciente[0], posimax, posimin)
        tara = inicio()

        #tempo.tick(10)

def pausar_som(music_state):
    pygame.time.wait(150)
    if music_state:
##        pygame.mixer.music.stop()
        return(False)
    if music_state == False:
##        pygame.mixer.music.play(-1)
        return(True)

def altura_col(tipo):
    with open("graficos/" + str(tipo), "r") as arquivo:
        valores = [float(val) for linha in arquivo for val in linha.split()]
    arquivo.close()
    return valores



def resultados(pontos, tempo, paciente, data, trat, id_temp, id_pont): #DETALHES

    pont, temp, id_t, id_p, interp_inf, interp_sup, tempo2, sereia, posmin, posmax = [], [], [], [], [], [], [], [], [], []
    acerto, acerto_percentual = 0, 0
   
    maxmin = bd_geral.maxmin_select(paciente, data, trat, 'Exercício')
    print(maxmin)
    posmin.append(maxmin[1][0])
    posmax.append(maxmin[0][0])
    proporcao = (75*(posmax[0]-posmin[0])/altura)


    ## pontos, tempo, id_temp  e id_pont são recebidos como strings, e precisam ser convertidos para float
    aux_pont_1 = pontos.strip("[")
    aux_pont_2 = aux_pont_1.strip("]")
    x = aux_pont_2.split(",")

    aux_temp_1 = tempo.strip("[")
    aux_temp_2 = aux_temp_1.strip("]")
    y = aux_temp_2.split(",")

    for aux in x:
        pont.append(float(aux))
    for aux in y:
        temp.append(float(aux))

    
    aux_pont_1 = id_pont.strip("[")
    aux_pont_2 = aux_pont_1.strip("]")
    x = aux_pont_2.split(",")

    aux_temp_1 = id_temp.strip("[")
    aux_temp_2 = aux_temp_1.strip("]")
    y2 = aux_temp_2.split(",")

    for aux in x:
        id_p.append(float(aux))
    for aux in y2:
        id_t.append(float(aux))


    ## Interpolação
    ## A aproximação é cúbica e ela extrapola a interpolação para valores fora do intervalo
    f2 = interp1d(id_t, id_p, kind = 'linear') #função de interpolação #pode ser 'cubic' também

    ## Limitar o intervalo de tempo2 para o intervalo onde há colunas, pois foi extrapolado pela função acima
    for i in temp:
        primeira_col = id_t[0]
        ultima_col = id_t[len(id_t)-1]
        if i >= primeira_col and i <= ultima_col:
            sereia.append(pont[temp.index(i)])
            tempo2.append(i)
            
    ## Interpolação dos gráficos limitantes superior e inferior (possivelmente esse valor 75 precisa ser modificado)
    for aux in tempo2:
        interp_inf.append(f2(aux)-proporcao)
        interp_sup.append(f2(aux)+proporcao)

    ## Comparação entre a posição da sereia e o intervalo do exercício. Cálculo dos acertos.
    for aux in range(len(tempo2)): 
        if sereia[aux] >= interp_inf[aux] and sereia[aux] <= interp_sup[aux]:
            acerto += 1
    acerto_percentual = round(acerto*100/len(tempo2),2)
    print(acerto, "acertos de ", len(tempo2), "pontos totais. Percentual de acertos:", acerto_percentual)

   
    plt.plot(id_t, id_p,'gx') #gráfico ideal central
    plt.plot(temp, pont, 'r--') #gráfico sereia
    plt.plot(tempo2, sereia, 'm-')
    plt.plot(tempo2, interp_sup,'c-', linewidth = 2) #gráfico ideal das colunas superiores
    plt.plot(tempo2, interp_inf,'c-', linewidth = 2) #gráfico ideal das colunas superiores
    plt.legend(['Central ñ interp', 'Sereia'], loc='best')

    
    plt.grid(True)
    plt.title(trat)
    plt.ylabel("Pressão (mmHg)")
    plt.xlabel("Tempo (s)")
    plt.show()

def historico():

    aux, graf_selec, datasel, paciente = [], [], [], []
    hist = True
    while hist:
        sg.theme('DarkBlue10')
        pasta = bd_geral.paciente_select("Exercício")

        if len(pasta)==0:
            janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
            window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
            event3, val3 = window3.read()
            if event3 in (None, 'OK'):
                window3.close()
        else:

            janela_sel_paciente = [[sg.Text('Selecione um paciente',justification='center', size=(60,1), font=("Arial", 15))],\
                                   [sg.Combo(pasta, size=(60,1), font=("Arial", 15))], \
                                    [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                      sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
            jan_sel_paciente = sg.Window('Selecionar Paciente', janela_sel_paciente, no_titlebar=True)
            event1, diretorio = jan_sel_paciente.read()
            if event1 in ('Selecionar'):
                paciente.append(diretorio[0])

                if diretorio[0]=="":
                    paciente.clear()
                    graf_selec.clear()
                    jan_sel_paciente.close()

            elif event1 in (None, "Cancelar"):
                jan_sel_paciente.close()
                hist = False

        if hist == True and len(paciente)> 0:

            jan_sel_paciente.close()
            janela = True
            aux = bd_geral.data_select(paciente[0])


            while janela:
                if len(aux) == 0:
                    janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                   [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                    window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                    event3, val3 = window3.read()
                    if event3 in (None, 'OK'):
                        window3.close()
                        janela = False
                        del (paciente[0])
                        del (diretorio[0])

                if janela == True:
                    janela_sel_data = [[sg.Text('Selecione a data do exercicio',justification='center', size=(60,1), font=("Arial", 15))],\
                                   [sg.Combo(aux, size=(60,1), font=("Arial", 15))], \
                                    [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                      sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                    jan_sel_data = sg.Window('Selecionar data do exercicio', janela_sel_data,  no_titlebar=True)
                    event, data = jan_sel_data.read()
                    if event in (None, 'Cancelar'):
                        jan_sel_data.close()
                        janela = False
                        del (paciente[0])
                        del (diretorio[0])
                    elif event in ('Selecionar'):
                        jan_sel_data.close()
                        datasel.append(data[0])
                        #trata = bd_geral.tratamento_select(paciente[0],datasel[0])
                        trata = bd_geral.grafico_select(paciente[0],datasel[0])
                        if data[0] != "":
                            janela_sel_trat = [[sg.Text('Selecione o tipo de tratamento',justification='center', size=(60,1), font=("Arial", 15))],\
                                               [sg.Combo(trata, size=(60,1), font=("Arial", 15))], \
                                                [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                                  sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                            jan_sel_trat = sg.Window('Selecionar tipo de tratamento', janela_sel_trat,   no_titlebar=True)
                            event, trat = jan_sel_trat.read()
                            if event in (None, 'Cancelar'):
                                jan_sel_trat.close()
                                del (datasel[0])
                                del (data[0])
                            elif event in ('Selecionar'):
                                jan_sel_trat.close()
                                graf_selec.append(trat[0])
                                if trat[0] != "":
                                    dados = bd_geral.dados_select(paciente[0],datasel[0],graf_selec[0], 'Exercício')
                                    id_ponts = bd_geral.id_select(paciente[0],datasel[0],graf_selec[0], 'Exercício')
                                    janela = False
                                    hist = False
                                    resultados(dados[0][0], dados[1][0], paciente[0], datasel[0], graf_selec[0], id_ponts[1][0], id_ponts[0][0])
                                    #AJEITAR: Parametros de grafico ideal precisam ser mandados, criar função para pegar esses dados do banco                                 else:
                                    pass
                        else:
                            pass
        else:
            hist = False

def progresso():

    ## TODAS AS IMAGENS DEVEM SER CARREGADAS ANTES DO LOOP PARA EVITAR QUE ELAS APAREÇAM EM POSICOES ERRADAS NO INICIO DA FUNCAO
    inter = [(-100, largura), (-100, largura), (-100, largura)]
    pos_buble_x, nova, nova2 = [randint(*pos) for pos in inter]


    pos_buble_y, col, cor, posibot = 700, coluna(), coral(), 11
    ariel, fund, bolhas, dez, uni, cem, dez2, uni2, cem2,dez3, uni3, cem3, \
           dez4, uni4, cem4 = sereia(), fundo(), bubble(), numeros(), \
           numeros(), numeros(), numeros(), numeros(), numeros(),\
           numeros(), numeros(), numeros(), numeros(), numeros(), numeros()
    teste, teste2,teste3, teste4, bot = letr(), letr(), letr(), letr(), botao()
    #pygame.mixer.Sound.play(Inicio_sound, loops = -1)

    #####CARREGANDO TODAS AS IMAGENS UTILIZADAS NA FUNÇÂO####

    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
    col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
    #ariel.show(tela,  posicao(30, 27,"x"), posicao(18, 30,"y"), 0)
    #ariel.show(tela,  posicao(30, 27,"x"), posicao(18, 30,"y"), 1)
    #bot.show(tela, posicao(17, 17,"x")+altura//45, posicao(posibot, posibot,"y"), 0)
    #grafico.show(tela, posicao(8, 15,"x"), posicao(4, 28,"y"))
    teste.show(tela, 0, 3, "PROGRESSO DO PACIENTE", 1 )
    teste.show(tela, 1, 19, "ACERTO X ERRO", 0 )
    teste.show(tela, 23, 19, "MAX X MIN", 0 )
    teste2.show(tela, 24, 12, "TARAGEM", 0 )
    teste2.show(tela, 4, 12, "ACERTOS", 0 )
    bot.show(tela, posicao(19, 11,"x"), posicao(11, 32,"y"), 3)
    teste4.show(tela, 16, 32, "SAIR", 0 )
    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)

    for conta in range(10):
        uni.show(tela, posicao(25, 15,"x"), posicao(25, 15,"y"),conta)
        dez.show(tela, posicao(26, 15,"x"), posicao(26, 15,"y"),conta)
        cem.show(tela, posicao(27, 15,"x"), posicao(27, 15,"y"), conta)
        uni2.show(tela, posicao(31, 15,"x"), posicao(31, 15,"y"), conta)
        dez2.show(tela, posicao(32, 15,"x"), posicao(32, 15,"y"), conta)
        cem2.show(tela, posicao(33, 15,"x"), posicao(33, 15,"y"), conta)
        uni3.show(tela, posicao(5, 15,"x"), posicao(4, 15,"y"), conta)
        dez3.show(tela, posicao(6, 15,"x"), posicao(5, 15,"y"), conta)
        cem3.show(tela, posicao(7, 15,"x"), posicao(6, 15,"y"), conta)
        uni4.show(tela, posicao(11, 15,"x"), posicao(9, 15,"y"), conta)
        dez4.show(tela, posicao(12, 15,"x"), posicao(10, 15,"y"), conta)
        cem4.show(tela, posicao(13, 15,"x"), posicao(11, 15,"y"), conta)
    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
    col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
    col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
    pygame.display.update()

    prog = True
    hist = True
    paciente = []

    while prog:
        #fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
        #teste.show(tela, 0, 3, "PROGRESSO DO PACIENTE", 1 )
        #col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
        #col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
        #pygame.display.update()
        while hist:
            sg.theme('DarkBlue10')
            nome = bd_geral.paciente_progresso()

            if len(nome)==0:
                janela_erro =  [[sg.Text(' Nenhum paciente cadastrado, por favor, cadastre um paciente.', size=(51,2), font=("Arial", 15))],\
                                       [sg.Button('OK', size=(50,1), font=("Arial", 15))]]
                window3 = sg.Window('ERRO', janela_erro, no_titlebar=True)
                event3, val3 = window3.read()
                if event3 in (None, 'OK'):
                    window3.close()
                    hist = False


            else:

                janela_sel_paciente = [[sg.Text('Selecione um paciente',justification='center', size=(60,1), font=("Arial", 15))],\
                                       [sg.Combo(nome, size=(60,1), font=("Arial", 15))], \
                                        [sg.Button("Selecionar", size=(30,1), font=("Arial", 15)),\
                                          sg.Button("Cancelar", size=(30,1), font=("Arial", 15))]]
                jan_sel_paciente = sg.Window('Selecionar Paciente', janela_sel_paciente, no_titlebar=True)
                event1, diretorio = jan_sel_paciente.read()
                if event1 in ('Selecionar'):
                    paciente.append(diretorio[0])
                    dados = bd_geral.nome_paciente_progresso(paciente[0])
                    bd_geral.make_plot(paciente[0])
                    grafico = grafmmae()
                    pac = paciente[0].upper()
                    jan_sel_paciente.close()
                    paciente.clear()
                    teste3.show(tela, 1, 8, "PACIENTE: "+ pac, 0 )
                    fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
                    pygame.display.update()
                    hist = False

                    if diretorio[0]=="":
                        paciente.clear()
                        hist= True

                elif event1 in (None, "Cancelar"):
                    paciente.clear()
                    jan_sel_paciente.close()
                    hist = False
                    return(True)
        fund.show(tela, posicao(18, 18,"x"), posicao(18, 18,"y"), 1)
        col.show(tela, posicao(35, 23,"x")+largura//36, posicao(35, 24,"y"))
        col.show(tela, posicao(0, 23,"x"), posicao(0, 24,"y"))
        teste.show(tela, 0, 3, "PROGRESSO DO PACIENTE", 1 )
        teste3.show(tela, 1, 8, "PACIENTE: "+ pac, 0 )
        teste.show(tela, 1, 19, "ACERTO X ERRO", 0 )
        teste.show(tela, 23, 19, "MAX X MIN", 0 )
        teste2.show(tela, 24, 12, "TARAGEM", 0 )
        teste2.show(tela, 4, 12, "ACERTOS", 0 )
        uni.show(tela, posicao(25, 15,"x"), posicao(25, 15,"y"), int(dados[len(dados)-1][0])//100)
        dez.show(tela, posicao(26, 15,"x"), posicao(26, 15,"y"), (int(dados[len(dados)-1][0])%100)//10)
        cem.show(tela, posicao(27, 15,"x"), posicao(27, 15,"y"), (int(dados[len(dados)-1][0])%100)%10)
        uni2.show(tela, posicao(31, 15,"x"), posicao(31, 15,"y"), int(dados[len(dados)-1][1])//100)
        dez2.show(tela, posicao(32, 15,"x"), posicao(32, 15,"y"), (int(dados[len(dados)-1][1])%100)//10)
        cem2.show(tela, posicao(33, 15,"x"), posicao(33, 15,"y"), (int(dados[len(dados)-1][1])%100)%10)
        uni3.show(tela, posicao(5, 15,"x"), posicao(4, 15,"y"), int(dados[len(dados)-1][4])//100)
        dez3.show(tela, posicao(6, 15,"x"), posicao(5, 15,"y"), (int(dados[len(dados)-1][4])%100)//10)
        cem3.show(tela, posicao(7, 15,"x"), posicao(6, 15,"y"), (int(dados[len(dados)-1][4])%100)%10)
        uni4.show(tela, posicao(11, 15,"x"), posicao(9, 15,"y"), int(dados[len(dados)-1][5])//100)
        dez4.show(tela, posicao(12, 15,"x"), posicao(10, 15,"y"), (int(dados[len(dados)-1][5])%100)//10)
        cem4.show(tela, posicao(13, 15,"x"), posicao(11, 15,"y"), (int(dados[len(dados)-1][5])%100)%10)
        bot.show(tela, posicao(19, 11,"x"), posicao(11, 32,"y"), 3)
        teste4.show(tela, 16, 32, "SAIR", 0 )
        grafico.show(tela, posicao(8, 15,"x"), posicao(4, 28,"y"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog = False

            elif event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                if event.key == pygame.K_RETURN:
                    return(True)
        pygame.display.update()


def grafico(graf, tempototal):

    pos_y, pos_x, velocidade_y, pos_yf, pos_xf, pos_xf2, total_pts  = altura - posmin[0], \
                                                          posicao(33, 18, "x") - largura//1.5,\
                                                          0, altura//2, largura//2, \
                                                          round(largura*1.537)-1, 146
    velocidade_obs = 0.02*largura
    pos_buble_x = randint(-100, largura)
    pos_buble_y, pos_peix_x, pos_peix_y = 700, -100, 350
    lims = [(-100, 300), (-100, 300), (-100, 300), (1, 10), (-400, 200), (1, 10)]
    nova, nova2, novapeixe, escolhapeixe, novapeixe2, escolhapeixe2 = [randint(*pair) for pair in lims]
    pontos_result, pos_col_y_buffer, pos_col_y, cont_aux, pont_sinc, ideal_pont = [], [], [], [], [], []

    sair, pontos, pausa, musica, colidiu, ncolidiu, total_colisoes, cont, escolha, flag, tempo_desloc0, tempo_desloc1 = \
    True, 0, 1, True, 0, 0, 0, 0, 0, 0, 0, 0
    acertos,erros = 0,0
    #player funciona
##    if musica:
##        pygame.mixer.music.play(-1)

    #ser.reset_input_buffer()
#####################################
    ariel, bolhas, fund1, fund2, peixe = sereia(), bubble(), fundo(), fundo(), fish()
    obs1, obs2, obs3, pause_bt = coluna(), coluna(), coluna(), coral()
    musica_bt, musica_simb, dez, uni, let = coral(), coral(), numeros(), numeros(), letras()
#####################################
    for conta in range(0, 9):
        dez.show(tela, -100, -100, conta)
        uni.show(tela, -100, -100, conta)
        peixe.show(tela, -100, -100, -100, conta + 1)
    obs1.show(tela, -80,-80)
    obs2.show(tela, -80,-80)
    obs3.show(tela, -80,-80)
    ariel.show(tela, -30, -30, 0)
    ariel.show(tela, -30, -30, 1)
    let.show(tela, -30, -30, 4)
    pause_bt.show(tela, -100, -100, 2)
    musica_bt.show(tela, -100, -100, 3)
    fund1.show(tela, pos_xf, pos_yf, 1)
    fund2.show(tela, pos_xf2, pos_yf, 0)
    contagem = 0

    altcol = [ "Contração Fasica Uniforme.txt", "Contração Tônica.txt", "Relaxamento.txt", "Trabalho Ascendente.txt",
               "Trabalho Concêntrico.txt", "Trabalho Excêntrico.txt", "Trabalho Livre.txt",
               "Trabalho Isométrico.txt"]

    tempo_graf = 10
    pos_col_y_buffer = altura_col(altcol[graf-1])

    pts_graf = round(tempo_graf/0.4125)
    per_amostr = total_pts/pts_graf

    for j in range(0, 146, int(per_amostr)):
        pos_col_y.append(pos_col_y_buffer[j])

    for i in range(5):
        pos_obs_x[i] = larg
        pos_obs_y[i] = 0
    iniciocontag = time.time()

    while sair:

        ini = time.time()
######################### FUNDO ###############################
        tela.fill(azul)
        fund1.show(tela, pos_xf, int(altura//2), 1)
        fund2.show(tela, pos_xf2, int(altura//2), 0)

        pos_xf = round(largura*1.537)-1 if pos_xf2 == largura//2 else pos_xf - 1
        pos_xf2 = round(largura*1.537)-1 if pos_xf == largura//2 else pos_xf2 -1


################### ALEATORIEDADE DAS BOLHAS ################
        if pos_buble_y == altura:
            nova, nova2 = randint(-largura//3, largura//3), randint(-largura//3, largura//3)
        if pos_buble_y < -altura*1.8:
            pos_buble_y = altura*1.1
        #bolhas.show(tela, pos_buble_x, pos_buble_y, nova)
        bolhas.show(tela, pos_buble_x - nova2, pos_buble_y*1.7, nova2)
        bolhas.show(tela, pos_buble_x - nova + nova2, pos_buble_y*1.3, nova - nova2)
        pos_buble_y -= 2

##################PEIXES

        if pos_peix_x == -largura//13:
            aleatorio = [(-400, altura//1.5), (-400, altura//1.5), (1, 5), (1, 5)]
            novapeixe, novapeixe2, escolhapeixe, escolhapeixe2 = [randint(*pair) for pair in aleatorio]
        if pos_peix_x > largura + largura//7:
            pos_peix_x=-altura//2

        peixe.show(tela, pos_peix_x, pos_peix_y, novapeixe, escolhapeixe)
        peixe.show(tela, pos_peix_x*1.5, pos_peix_y, novapeixe2 + novapeixe, escolhapeixe2 - escolhapeixe)
        peixe.show(tela, pos_peix_x*1.10, pos_peix_y, novapeixe2, escolhapeixe2)
        peixe.show(tela, pos_peix_x*1.25, pos_peix_y, novapeixe2 - novapeixe, escolhapeixe2 + escolhapeixe)
        peixe.show(tela, pos_peix_x*1.05, pos_peix_y, novapeixe - 150, escolhapeixe + 2)
        peixe.show(tela, pos_peix_x*1.45, pos_peix_y, novapeixe2 + novapeixe - 20, escolhapeixe2 - escolhapeixe + 1)
        peixe.show(tela, pos_peix_x*1.15, pos_peix_y, novapeixe2 - 150, escolhapeixe2 + 2)
        peixe.show(tela, pos_peix_x*1.30, pos_peix_y, novapeixe2 - novapeixe + 200, escolhapeixe2 + escolhapeixe + 1)

        pos_peix_x += 2


####### LIMITAÇÃO DE MOVIMENTOS #################

        if pos_y < 10:
            pos_y += 20

        if pos_y >= altura - 10:
            pos_y -= 10

####### CONTROLE DE MOVIMENTOS DO OBSTÁCULO #################



        ########### DESLOCAMENTO DAS COLUNAS

        if cont <= 0:
            pos_obs_x[0]-=velocidade_obs
            pos_obs_y[0] = int(altura*(1/2 - pos_col_y[cont]))
            obs1.show(tela, pos_obs_x[0], pos_obs_y[0])

        elif cont == 1:
            for i in range (cont + 1):
                pos_obs_x[i]-=velocidade_obs
                obs1.show(tela, pos_obs_x[i], pos_obs_y[i])

        elif cont == 2:
            for i in range (cont + 1):
                pos_obs_x[i]-=velocidade_obs
                obs1.show(tela, pos_obs_x[i], pos_obs_y[i])

        elif cont == 3:
            for i in range (cont + 1):
                pos_obs_x[i]-=velocidade_obs
                obs1.show(tela, pos_obs_x[i], pos_obs_y[i])

        else:
            for i in range (5):
                pos_obs_x[i]-=velocidade_obs
                obs1.show(tela, pos_obs_x[i], pos_obs_y[i])

        ########### DETERMINAR ALTURA DAS COLUNAS

        if  pos_obs_x[0]>3*(largura//4)-velocidade_obs+(largura//18) and pos_obs_x[0]<=3*(largura//4)+(largura//18)and cont <= len(pos_col_y)-2: # Distância de 1//4 da largura da tela entre obstáculos.
            cont += 1                                                                                        # Limite dos intervalos deve ser subtraído de
            pos_obs_x[1], pos_obs_y[1] = larg, altura*(1/2 - pos_col_y[cont])                                  # 1//2 largura do obstáculo.

        if  pos_obs_x[0]>2*(largura//4)-velocidade_obs+(largura//18) and pos_obs_x[0]<=2*(largura//4)+(largura//18) and cont <= len(pos_col_y)-2:
            cont += 1
            pos_obs_x[2], pos_obs_y[2] = larg, altura*(1/2 - pos_col_y[cont])

        if  pos_obs_x[0]>(largura//4)-velocidade_obs+(largura//18) and pos_obs_x[0]<=(largura//4)+(largura//18) and cont <= len(pos_col_y)-2:
            cont += 1
            pos_obs_x[3], pos_obs_y[3] = larg, altura*(1/2 - pos_col_y[cont])

        if  pos_obs_x[0]>-velocidade_obs+(largura//18) and pos_obs_x[0]<=0+(largura//18) and cont <= len(pos_col_y)-2:
            cont += 1
            pos_obs_x[4], pos_obs_y[4] = larg, altura*(1/2 - pos_col_y[cont])

        if  pos_obs_x[0]>-(largura//4)-velocidade_obs+(largura//18) and pos_obs_x[0]<=-(largura//4)+(largura//18) and cont <= len(pos_col_y)-2:
            cont += 1
            pos_obs_x[0], pos_obs_y[0] = larg, altura*(1/2 - pos_col_y[cont])

        nova_posi = posmax[0] - (int(pos_y)*(posmax[0]-posmin[0])/altura)

        pontos_result.append(nova_posi) #Lista com pontos por onde a sereia passou.
        cont_aux.append(round(contagem, 2)) #Lista com instantes de tempo que a sereia passa por cada ponto de 'pontos_result'.

        ########### FIM DO GRÁFICO

        if cont >= len(pos_col_y)-1 and pos_obs_x[(len(pos_col_y)%5)-1]<-larg//4:
            if contagem < tempototal:
                cont=0
                for i in range (5):
                    pos_obs_x[i] = larg
                    pos_obs_y[i] = 0
            else:

##                pygame.mixer.music.stop()
                dt = datetime.now()
                pontos  = str(pontos_result)
                tempo = str(cont_aux)
                
                #acertos = 100
                #erros = 0
##                print(146/int(per_amostr))
##                print(total_colisoes)
                id_temp = str(pont_sinc)
                id_pont = str (ideal_pont)
                #print(pont_sinc)
                #print (ideal_pont)
                
                bd_geral.data_entry(n_paciente[0], idade_paciente[0],trata_paciente[0],\
                                    dt, posmax[0], posmin[0], pontos, tempo, \
                                    str(altcol[graf-1]).strip(".txt"), id_pont, id_temp)
                bd_geral.data_entry_progresso(n_paciente[0], dt, posmax[0], posmin[0], acertos, erros)


                ####################### PRECISO MANDAR OS DADOS PARA DETALHES
                
                sair = gameover(pontos, tempo, n_paciente[0], dt, str(altcol[graf-1]).strip(".txt"), id_temp, id_pont)

        ####### SISTEMA DE PONTUAÇÃO #################
        for i in range (5):
            if pos_x==(pos_obs_x[i]+(largura//15.17)):
                pontos += 1
                recorde(pontos)
        



###################### JOYSTICK ##################################
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
############### MÚSICA #####################################
        if 636 < mouse[0] < 704 and 37 < mouse[1] < 103 and click[0] == 1:
            musica = pausar_som(musica)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
            if event.type == pygame.KEYDOWN: #se qualquer tecla do teclado for selecionada
                if event.key == pygame.K_UP:
                    velocidade_y=-10
                    escolha = 0
            else:
                velocidade_y = 10
                escolha = 1

        ####### REGRAS DE LIMITAÇÃO = COLISÃO #################
        if altura_col(altcol[graf-1]) != "Trabalho Livre.txt":
            for i in range (5):
                if (pos_x >= pos_obs_x[i]-velocidade_obs/2 and pos_x <= pos_obs_x[i]+velocidade_obs/2):
                    pont_sinc.append(round(contagem, 2))
                    proporcao = (75*(posmax[0]-posmin[0])/altura)
                    ideal_pont.append(posmax[0] - (int((round(pos_obs_y[i]+325,2)))*(posmax[0]-posmin[0])/altura))
                    ## 325 = [(400-250)/2 + 250]
                    if(pos_y>=(pos_obs_y[i]+400) or pos_y<=(pos_obs_y[i]+250)): #Atualizar valores em função da altura da sereia.
                        pygame.mixer.Sound.play(colision_sound)
                        #colidiu += 1
                        #total_colisoes+=1
                        erros+=1
                        escolha = 2


                    if(pos_y<=(pos_obs_y[i]+400) and pos_y>=(pos_obs_y[i]+250)): #Atualizar valores em função da altura da sereia.
                        pygame.mixer.Sound.play(colision_sound)
                        acertos+=1
                        escolha = 2 ### DEPOIS ADICIONAR UMA IMAGEM POSITIVA DA SEREIA
        pos_y += velocidade_y


        if sair == True:
            ariel.show(tela, pos_x, pos_y, escolha)
##            pause_bt.show(tela, 740, 68, 2)
##            musica_bt.show(tela, 670, 68, 3)
            let.show(tela, 100, 70, 4)
            dez.show(tela, 200, 70, pontos//10)
            uni.show(tela, 220, 70, pontos % 10)
        contagem = time.time()-iniciocontag
        pygame.display.update()
        while time.time() - ini < 0.0333:
            continue


#def resultados (pontos_result):




inicio()
pygame.quit()
