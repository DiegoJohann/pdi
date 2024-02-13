from itertools import permutations
import math
import os
import statistics
import random
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from scipy.spatial.distance import cdist

import cv2
import numpy as np
from PIL import Image, ImageTk, ImageOps


# Métodos
# -------------------------------------------------------------------------
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def instancia_imagem_processada(imagem):
    global imagemProcessada
    imagemProcessada = ImageTk.PhotoImage(ImageOps.contain(imagem, (770, 770)))
    global frmImagemProcessada
    frmImagemProcessada.destroy()
    frmImagemProcessada = Label(boxImagemProcessada, image=imagemProcessada, width=770, height=770,
                                bg='SystemButtonFace')
    frmImagemProcessada.place(x=0, y=0)


def instancia_imagem_reduzida(imagem, lar, alt):
    global imagemProcessada
    imagemProcessada = ImageTk.PhotoImage(ImageOps.contain(imagem, (lar, alt)))
    global frmImagemProcessada
    frmImagemProcessada.destroy()
    frmImagemProcessada = Label(boxImagemProcessada, image=imagemProcessada, width=770, height=770,
                                bg='SystemButtonFace')
    frmImagemProcessada.place(x=0, y=0)


def carrega_imagem():
    root.caminhoImgOriginal = filedialog.askopenfilename(initialdir='imagens',
                                                         title='Selecione uma imagem',
                                                         filetypes=(('Imagens PNG', '*.png'),
                                                                    ('Imagens JPG', '*.jpg'),
                                                                    ('Imagens BMP', '*.bmp')))
    global imagemOriginal
    imagemOriginal = ImageTk.PhotoImage(ImageOps.contain(Image.open(root.caminhoImgOriginal), (770, 770)))
    global frmImagemOriginal
    frmImagemOriginal.destroy()
    frmImagemOriginal = Label(boxImagemOriginal, image=imagemOriginal, width=770, height=770, bg='SystemButtonFace')
    frmImagemOriginal.pack(side=LEFT)


def salva_imagem():
    arquivo = filedialog.asksaveasfilename(defaultextension=".png",
                                           filetypes=(
                                               ("Imagem PNG", "*.png"), ("Imagem JPG", "*.jpg"),
                                               ("Imagem BMP", "*.bmp"), ("Todos os arquivos", "*.*")))
    if arquivo:
        global imagemProcessada
        imagem = ImageTk.getimage(imagemProcessada)
        imagem_rgb = imagem.convert('RGB')
        imagem_rgb.save(arquivo)


def abre_menu_translacao():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe os valores de translação em pixels:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    lbl_x = Label(container_opcoes, text='X: ', font=fontePadrao)
    lbl_x.place(x=20, y=40)

    edt_x = Entry(container_opcoes, width=10, font=fontePadrao)
    edt_x.place(x=40, y=40)

    lbl_y = Label(container_opcoes, text='Y: ', font=fontePadrao)
    lbl_y.place(x=125, y=40)

    edt_y = Entry(container_opcoes, width=10, font=fontePadrao)
    edt_y.place(x=145, y=40)

    btn_transladar = Button(container_opcoes, font=fontePadrao)
    btn_transladar['text'] = 'OK'
    btn_transladar['width'] = '5'
    btn_transladar['command'] = lambda: translacao(edt_x.get(), edt_y.get())
    btn_transladar.place(x=20, y=70)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=80, y=70)


def abre_menu_espelhamento():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe a orientação do espelhamento:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    btn_horizontal = Button(container_opcoes, font=fontePadrao)
    btn_horizontal['text'] = 'Horizontal'
    btn_horizontal['width'] = '10'
    btn_horizontal['command'] = espelhamento_horizontal
    btn_horizontal.place(x=20, y=40)

    btn_vertical = Button(container_opcoes, font=fontePadrao)
    btn_vertical['text'] = 'Vertical'
    btn_vertical['width'] = '10'
    btn_vertical['command'] = espelhamento_vertical
    btn_vertical.place(x=115, y=40)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=20, y=75)


def abre_menu_preprocessamento():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe a opção desejada:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    btn_horizontal = Button(container_opcoes, font=fontePadrao)
    btn_horizontal['text'] = 'Greyscale'
    btn_horizontal['width'] = '11'
    btn_horizontal['command'] = executa_greyscale
    btn_horizontal.place(x=20, y=40)

    btn_vertical = Button(container_opcoes, font=fontePadrao)
    btn_vertical['text'] = 'Brilho e Contraste'
    btn_vertical['width'] = '15'
    btn_vertical['command'] = mostra_opcao_brilho_contraste
    btn_vertical.place(x=115, y=40)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=20, y=75)


def mostra_opcao_brilho_contraste():
    global container_opcoes

    lbl_brilho = Label(container_opcoes, text='Brilho:', font=fontePadrao)
    lbl_brilho.place(x=240, y=42)

    edt_brilho = Entry(container_opcoes, width=8, font=fontePadrao)
    edt_brilho.insert(0, '0')
    edt_brilho.place(x=285, y=44)

    lbl_contraste = Label(container_opcoes, text='Contraste:', font=fontePadrao)
    lbl_contraste.place(x=350, y=42)

    edt_contraste = Entry(container_opcoes, width=8, font=fontePadrao)
    edt_contraste.insert(0, '1')
    edt_contraste.place(x=420, y=44)

    btn_ok = Button(container_opcoes, font=fontePadrao)
    btn_ok['text'] = 'OK'
    btn_ok['width'] = '10'
    btn_ok['command'] = lambda: brilho_contraste(edt_brilho.get(), edt_contraste.get())
    btn_ok.place(x=490, y=40)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_transf
    btn_cancelar.place(x=575, y=40)


def cancela_transf():
    for i in range(1, 7):
        container_opcoes.winfo_children().pop().destroy()


def abre_menu_passabaixa():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe o tipo de filtro passa baixa:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    btn_media = Button(container_opcoes, font=fontePadrao)
    btn_media['text'] = 'Média'
    btn_media['width'] = '8'
    btn_media['command'] = media
    btn_media.place(x=20, y=40)

    btn_moda = Button(container_opcoes, font=fontePadrao)
    btn_moda['text'] = 'Moda'
    btn_moda['width'] = '10'
    btn_moda['command'] = moda
    btn_moda.place(x=90, y=40)

    btn_mediana = Button(container_opcoes, font=fontePadrao)
    btn_mediana['text'] = 'Mediana'
    btn_mediana['width'] = '10'
    btn_mediana['command'] = mediana
    btn_mediana.place(x=175, y=40)

    btn_gauss = Button(container_opcoes, font=fontePadrao)
    btn_gauss['text'] = 'Gauss'
    btn_gauss['width'] = '10'
    btn_gauss['command'] = gauss
    btn_gauss.place(x=260, y=40)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=20, y=75)


def abre_menu_passaalta():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe o tipo de filtro passa alta:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    btn_kirsch = Button(container_opcoes, font=fontePadrao)
    btn_kirsch['text'] = 'Kirsch'
    btn_kirsch['width'] = '8'
    btn_kirsch['command'] = chama_kirsch
    btn_kirsch.place(x=20, y=40)


def abre_menu_treshold():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe o valor do treshold:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    edt_treshold = Entry(container_opcoes, width=7, font=fontePadrao)
    edt_treshold.place(x=20, y=40)

    btn_ok = Button(container_opcoes, font=fontePadrao)
    btn_ok['text'] = 'OK'
    btn_ok['width'] = '10'
    btn_ok['command'] = lambda: treshold(edt_treshold.get())
    btn_ok.place(x=20, y=70)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=105, y=70)


def translacao(x_loc, y_loc):
    global container_opcoes
    try:
        processando_imagem(170, 73)
        int_x = int(x_loc)
        int_y = int(y_loc)

        destino = Image.open(root.caminhoImgOriginal)
        lar = destino.size[0]
        alt = destino.size[1]
        imagem_original = np.asarray(destino.convert('RGB'))
        for x in range(lar):
            for y in range(alt):
                if x >= int_x and y >= int_y:
                    yo = x - int_x
                    xo = y - int_y
                    destino.putpixel((x, y),
                                     (imagem_original[xo, yo][0], imagem_original[xo, yo][1],
                                      imagem_original[xo, yo][2]))
                else:
                    destino.putpixel((x, y), (255, 255, 255, 255))
        instancia_imagem_processada(destino)
        container_opcoes.winfo_children().pop().destroy()
    except ValueError:
        tkinter.messagebox.showerror('Erro', 'Valor informado não é um número!')
        container_opcoes.winfo_children().pop(2).focus_set()


def media():
    processando_imagem(120, 77)
    matriz_media = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
    imagem_destino = convolucao(imagem_greyscale, matriz_media)
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def moda():
    processando_imagem(120, 77)
    imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
    imagem_destino = Image.open(root.caminhoImgOriginal)
    lar = imagem_greyscale.size[0]
    alt = imagem_greyscale.size[1]
    for x in range(1, lar - 1):
        for y in range(1, alt - 1):
            mascara = gera_lista_9x9(imagem_greyscale, x, y)
            valor = statistics.mode(mascara)
            imagem_destino.putpixel((x, y), (valor, valor, valor))
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def mediana():
    processando_imagem(120, 77)
    imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
    imagem_destino = Image.open(root.caminhoImgOriginal)
    lar = imagem_greyscale.size[0]
    alt = imagem_greyscale.size[1]
    for x in range(1, lar - 1):
        for y in range(1, alt - 1):
            mascara = gera_lista_9x9(imagem_greyscale, x, y)
            mascara.sort()
            valor = mascara[4]
            imagem_destino.putpixel((x, y), (valor, valor, valor))
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def gauss():
    processando_imagem(120, 77)
    matriz_gauss = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
    imagem_destino = convolucao(imagem_greyscale, matriz_gauss)
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def brilho_contraste(brilho, contraste):
    try:
        num_brilho = float(brilho)
        num_contraste = float(contraste)
        processando_imagem(120, 77)
        imagem = Image.open(root.caminhoImgOriginal)
        imagem_destino = Image.open(root.caminhoImgOriginal)
        lar = imagem.size[0]
        alt = imagem.size[1]
        for x in range(1, lar - 1):
            for y in range(1, alt - 1):
                valores = np.empty(3, dtype=int)
                for i in range(0, 3):
                    valores[i] = math.floor(num_contraste * imagem.getpixel((x, y))[i] + num_brilho)
                imagem_destino.putpixel((x, y), (int(valores[0]), int(valores[1]), int(valores[2])))
        instancia_imagem_processada(imagem_destino)
        container_opcoes.winfo_children().pop().destroy()
    except ValueError:
        tkinter.messagebox.showerror('Erro', 'Informe um valor numérico! Se tiver casas decimais, separe com ponto.')


def treshold(valor):
    try:
        int_treshold = int(valor)
        processando_imagem(120, 77)
        imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
        imagem_destino = Image.open(root.caminhoImgOriginal)
        lar = imagem_greyscale.size[0]
        alt = imagem_greyscale.size[1]
        for x in range(1, lar - 1):
            for y in range(1, alt - 1):
                pixel = imagem_greyscale.getpixel((x, y))[0]
                if pixel > int_treshold:
                    imagem_destino.putpixel((x, y), (255, 255, 255))
                else:
                    imagem_destino.putpixel((x, y), (0, 0, 0))
        instancia_imagem_processada(imagem_destino)
        imagem_destino.save('C:\\Users\\diego.DIEGOPC\\Desktop\\trem pintado.png')
        container_opcoes.winfo_children().pop().destroy()
    except ValueError:
        tkinter.messagebox.showerror('Erro', 'Informe um valor numérico inteiro!')
        container_opcoes.winfo_children().pop(1).focus_set()


def chama_kirsch():
    processando_imagem(130, 77)
    instancia_imagem_processada(kirsch(Image.open(root.caminhoImgOriginal)))
    container_opcoes.winfo_children().pop().destroy()


def kirsch(imagem):
    matriz_gauss = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    imagem_greyscale = greyscale(imagem)
    imagem_gauss = convolucao(imagem_greyscale, matriz_gauss)
    imagem_openCv = cv2.cvtColor(np.array(imagem_gauss), cv2.COLOR_BGR2GRAY)

    mascara1 = np.array([[5, 5, 5],
                         [-3, 0, -3],
                         [-3, -3, -3]], dtype=np.float32)
    mascara2 = np.array([[5, 5, -3],
                         [5, 0, -3],
                         [-3, -3, -3]], dtype=np.float32)
    mascara3 = np.array([[5, -3, -3],
                         [5, 0, -3],
                         [5, -3, -3]], dtype=np.float32)
    mascara4 = np.array([[-3, -3, -3],
                         [5, 0, -3],
                         [5, 5, -3]], dtype=np.float32)
    mascara5 = np.array([[-3, -3, -3],
                         [-3, 0, -3],
                         [5, 5, 5]], dtype=np.float32)
    mascara6 = np.array([[-3, -3, -3],
                         [-3, 0, 5],
                         [-3, 5, 5]], dtype=np.float32)
    mascara7 = np.array([[-3, -3, 5],
                         [-3, 0, 5],
                         [-3, -3, 5]], dtype=np.float32)
    mascara8 = np.array([[-3, 5, 5],
                         [-3, 0, 5],
                         [-3, -3, -3]], dtype=np.float32)

    # Aplica as máscaras de kirsch na imagem usando a biblioteca OpenCV
    g1 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara1), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g2 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara2), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g3 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara3), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g4 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara4), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g5 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara5), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g6 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara6), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g7 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara7), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    g8 = cv2.normalize(cv2.filter2D(imagem_openCv, cv2.CV_32F, mascara8), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

    imagem_destino_openCv = cv2.max(
        g1, cv2.max(
            g2, cv2.max(
                g3, cv2.max(
                    g4, cv2.max(
                        g5, cv2.max(
                            g6, cv2.max(
                                g7, g8
                            )
                        )
                    )
                )
            )
        )
    )
    imagem_destino = Image.fromarray(cv2.cvtColor(imagem_destino_openCv, cv2.COLOR_BGR2RGB))

    # Processo comentado - testes de alteração do contorno
    alt = imagem_destino.size[0]
    lar = imagem_destino.size[1]
    for x in range(0, lar - 1):
        for y in range(0, alt - 1):
            valor = imagem_destino.getpixel((y, x))[0]
            if valor > 160:
                valor = 0
            else:
                valor = 255
            imagem_destino.putpixel((y, x), (valor, valor, valor))

    return imagem_destino


def dilatacao(imagem):
    imagem_greyscale = greyscale(imagem)
    imagem_destino = Image.open(root.caminhoImgOriginal)
    matriz = np.array([[0, 10, 0],
                       [10, 10, 10],
                       [0, 10, 0]], dtype=np.int32)
    alt = imagem_greyscale.size[0]
    lar = imagem_greyscale.size[1]
    for y in range(1, lar - 1):
        for x in range(1, alt - 1):
            valor1 = imagem_greyscale.getpixel((x, y - 1))[0] - matriz[0][1]
            valor2 = imagem_greyscale.getpixel((x - 1, y))[0] - matriz[1][0]
            valor3 = imagem_greyscale.getpixel((x, y))[0] - matriz[1][1]
            valor4 = imagem_greyscale.getpixel((x, y + 1))[0] - matriz[1][2]
            valor5 = imagem_greyscale.getpixel((x + 1, y))[0] - matriz[2][1]

            valorFinal = min(valor1, valor2, valor3, valor4, valor5)

            imagem_destino.putpixel((x, y - 1), (valorFinal, valorFinal, valorFinal))
            imagem_destino.putpixel((x - 1, y), (valorFinal, valorFinal, valorFinal))
            imagem_destino.putpixel((x, y), (valorFinal, valorFinal, valorFinal))
            imagem_destino.putpixel((x, y + 1), (valorFinal, valorFinal, valorFinal))
            imagem_destino.putpixel((x + 1, y), (valorFinal, valorFinal, valorFinal))
    return imagem_destino


def erosao(imagem):
    imagem_greyscale = greyscale(imagem)
    imagem_erodida = Image.fromarray(np.array(imagem_greyscale))
    matriz = np.array([[0, 10, 0],
                       [10, 10, 10],
                       [0, 10, 0]], dtype=np.int32)
    alt = imagem_greyscale.size[0]
    lar = imagem_greyscale.size[1]
    for y in range(1, lar - 1):
        for x in range(1, alt - 1):
            valor1 = imagem_greyscale.getpixel((x, y - 1))[0] + matriz[0][1]
            valor2 = imagem_greyscale.getpixel((x - 1, y))[0] + matriz[1][0]
            valor3 = imagem_greyscale.getpixel((x, y))[0] + matriz[1][1]
            valor4 = imagem_greyscale.getpixel((x, y + 1))[0] + matriz[1][2]
            valor5 = imagem_greyscale.getpixel((x + 1, y))[0] + matriz[2][1]

            valorFinal = max(valor1, valor2, valor3, valor4, valor5)

            imagem_erodida.putpixel((x, y - 1), (valorFinal, valorFinal, valorFinal))
            imagem_erodida.putpixel((x - 1, y), (valorFinal, valorFinal, valorFinal))
            imagem_erodida.putpixel((x, y), (valorFinal, valorFinal, valorFinal))
            imagem_erodida.putpixel((x, y + 1), (valorFinal, valorFinal, valorFinal))
            imagem_erodida.putpixel((x + 1, y), (valorFinal, valorFinal, valorFinal))
    return imagem_erodida


def processando_imagem(x, y):
    lbl_processando = Label(container_opcoes, text='Processando imagem...', font=fonteProcessando)
    lbl_processando.place(x=x, y=y)
    container_opcoes.update()


def gera_lista_9x9(imagem, x, y):
    mascara = [imagem.getpixel((x - 1, y - 1))[0], imagem.getpixel((x, y - 1))[0],
               imagem.getpixel((x + 1, y - 1))[0],
               imagem.getpixel((x - 1, y))[0], imagem.getpixel((x, y))[0],
               imagem.getpixel((x + 1, y))[0],
               imagem.getpixel((x - 1, y + 1))[0], imagem.getpixel((x, y + 1))[0],
               imagem.getpixel((x + 1, y + 1))[0]]
    return mascara


def convolucao(imagem, mascara):
    alt = imagem.size[0]
    lar = imagem.size[1]
    for y in range(1, lar - 1):
        for x in range(1, alt - 1):
            valor = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    valor += imagem.getpixel((x + i, y + i))[0] * mascara[j + 1][i + 1]
            valor = valor // 16
            imagem.putpixel((x, y), (valor, valor, valor))
    return imagem


def espelhamento_horizontal():
    processando_imagem(120, 77)
    imagem_destino = Image.open(root.caminhoImgOriginal)
    lar = imagem_destino.size[0]
    alt = imagem_destino.size[1]
    imagem_original = np.asarray(imagem_destino.convert('RGB'))
    for x in range(lar):
        for y in range(alt):
            imagem_destino.putpixel((x, y),
                                    (imagem_original[y, lar - 1 - x][0], imagem_original[y, lar - 1 - x][1],
                                     imagem_original[y, lar - 1 - x][2]))
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def espelhamento_vertical():
    processando_imagem(120, 77)
    imagem_destino = Image.open(root.caminhoImgOriginal)
    lar = imagem_destino.size[0]
    alt = imagem_destino.size[1]
    imagem_original = np.asarray(imagem_destino.convert('RGB'))
    for y in range(alt):
        for x in range(lar):
            imagem_destino.putpixel((x, y),
                                    (imagem_original[alt - 1 - y, x][0], imagem_original[alt - 1 - y, x][1],
                                     imagem_original[alt - 1 - y, x][2]))
    instancia_imagem_processada(imagem_destino)
    container_opcoes.winfo_children().pop().destroy()


def abre_menu_ampliacao():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe a porcentagem de ampliação:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    edt_porcentagem = Entry(container_opcoes, width=10, font=fontePadrao)
    edt_porcentagem.place(x=20, y=43)

    btn_confirmar = Button(container_opcoes, font=fontePadrao)
    btn_confirmar['text'] = 'Confirmar'
    btn_confirmar['width'] = '10'
    btn_confirmar['command'] = lambda: ampliacao(edt_porcentagem.get())
    btn_confirmar.place(x=20, y=75)


def ampliacao(porcentagem):
    try:
        num_porcentagem = float(porcentagem) / 100
        processando_imagem(120, 77)
        imagem_cv2 = cv2.imread(root.caminhoImgOriginal)
        imagem_original = Image.open(root.caminhoImgOriginal)
        alt, lar, c = imagem_cv2.shape
        inicioX = math.floor(lar * num_porcentagem)
        inicioY = math.floor(alt * num_porcentagem)
        nLar = lar - inicioX
        nAlt = alt - inicioY
        imagem_processo = 255 * np.ones(shape=(nAlt, nLar, c), dtype=np.uint8)
        imagem_destino = Image.fromarray(imagem_processo)
        for x in range(nLar):
            for y in range(nAlt):
                imagem_destino.putpixel((x, y), imagem_original.getpixel((x + (inicioX // 2), y + (inicioY // 2))))
        instancia_imagem_processada(imagem_destino)
        container_opcoes.winfo_children().pop().destroy()
    except ValueError:
        tkinter.messagebox.showerror('Erro', 'Informe um valor numérico! Se usar casas decimais, utilize ponto.')
        container_opcoes.winfo_children().pop().destroy()
    except IndexError:
        tkinter.messagebox.showerror('Erro', 'Informe um valor válido! Não pode ser negativo!')
        container_opcoes.winfo_children().pop().destroy()


def abre_menu_reducao():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe a porcentagem de redução:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    edt_porcentagem = Entry(container_opcoes, width=10, font=fontePadrao)
    edt_porcentagem.place(x=20, y=43)

    btn_confirmar = Button(container_opcoes, font=fontePadrao)
    btn_confirmar['text'] = 'Confirmar'
    btn_confirmar['width'] = '10'
    btn_confirmar['command'] = lambda: reducao(edt_porcentagem.get())
    btn_confirmar.place(x=20, y=75)


def reducao(porcentagem):
    processando_imagem(120, 77)
    try:
        num_porcentagem = float(porcentagem)
        imagem = Image.open(root.caminhoImgOriginal)
        dimensao = math.floor(770 * (100 - num_porcentagem) / 100)
        instancia_imagem_reduzida(imagem, dimensao, dimensao)
    except ValueError:
        tkinter.messagebox.showerror('Erro', 'Informe um valor numérico! Se usar casas decimais, utilize ponto.')
    except ZeroDivisionError:
        tkinter.messagebox.showerror('Erro', 'Você não pode reduzir 100% da imagem!')
    container_opcoes.winfo_children().pop().destroy()


def abre_menu_rotacao():
    cancela_opcao()
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    lbl_titulo = Label(container_opcoes, text='Informe o ângulo de rotação:', font=fontePadrao)
    lbl_titulo.place(x=20, y=15)

    edt_angulo = Entry(container_opcoes, width=10, font=fontePadrao)
    edt_angulo.place(x=20, y=43)

    btn_confirmar = Button(container_opcoes, font=fontePadrao)
    btn_confirmar['text'] = 'Confirmar'
    btn_confirmar['width'] = '10'
    btn_confirmar['command'] = lambda: rotacao(Image.open(root.caminhoImgOriginal), edt_angulo.get())
    btn_confirmar.place(x=100, y=40)

    btn_cancelar = Button(container_opcoes, font=fontePadrao)
    btn_cancelar['text'] = 'Cancelar'
    btn_cancelar['width'] = '10'
    btn_cancelar['command'] = cancela_opcao
    btn_cancelar.place(x=20, y=75)


def rotacao(imagem, angulo):
    try:
        anguloNumero = float(angulo)
        processando_imagem(120, 77)

        # anguloNumero = anguloNumero % 360.0
        #
        # lar, alt = imagem.size
        # centro_rotacao = (lar / 2.0, alt / 2.0)
        #
        # anguloNumero = -math.radians(anguloNumero)
        # matriz = [
        #     round(math.cos(anguloNumero), 15),
        #     round(math.sin(anguloNumero), 15),
        #     0.0,
        #     round(-math.sin(anguloNumero), 15),
        #     round(math.cos(anguloNumero), 15),
        #     0.0,
        # ]
        #
        # def transformacao(x, y, m):
        #     (a, b, c, d, e, f) = m
        #     return a * x + b * y + c, d * x + e * y + f
        #
        # matriz[2], matriz[5] = transformacao(
        #     -centro_rotacao[0] - 0, -centro_rotacao[1] - 0, matriz
        # )
        #
        # xx = []
        # yy = []
        # for x, y in ((0, 0), (lar, 0), (lar, alt), (0, alt)):
        #     x, y = transformacao(x, y, matriz)
        #     xx.append(x)
        #     yy.append(y)
        # nLar = math.ceil(max(xx)) - math.floor(min(xx))
        # nAlt = math.ceil(max(yy)) - math.floor(min(yy))
        #
        # matriz[2], matriz[5] = transformacao(-(nLar - lar) / 2.0, -(nAlt - alt) / 2.0, matriz)
        # lar, alt = nLar, nAlt
        #
        # imagem_destino = imagem.transform((lar, alt), 0, matriz, 0, None)

        imagem_destino = imagem.rotate(anguloNumero, expand=True)
        instancia_imagem_processada(imagem_destino)
        container_opcoes.winfo_children().pop().destroy()
    except ValueError:
        tkinter.messagebox.showerror('Erro',
                                     'Valor informado não é um ponto flutuante válido! \nUse ponto ao invés de vírgula')


def cancela_opcao():
    global container_opcoes
    container_opcoes.destroy()


def greyscale(imagem):
    imagem_original = imagem
    imagem_destino = imagem
    lar = imagem_destino.size[0]
    alt = imagem_destino.size[1]
    for y in range(alt):
        for x in range(lar):
            pixel = imagem_original.getpixel((x, y))
            valor = sum(i for i in pixel[0:3]) // 3
            imagem_destino.putpixel((x, y), (valor, valor, valor))
    return imagem_destino


def executa_greyscale():
    processando_imagem(120, 77)
    instancia_imagem_processada(greyscale(Image.open(root.caminhoImgOriginal)))
    container_opcoes.winfo_children().pop().destroy()


def gera_cor_aleatoria():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def find_best_matching_subset(shape1, shape2):
    best_subset = None
    best_distance = float('inf')

    for permuted_shape2 in permutations(shape2):
        distance = np.linalg.norm(np.array(shape1) - np.array(permuted_shape2), axis=1).sum()
        if distance < best_distance:
            best_distance = distance
            best_subset = permuted_shape2

    return best_subset


def formas_proximas(forma1, forma2, tolerancia):
    distancias = cdist(np.array(forma1), np.array(forma2))
    min_distancias = np.min(distancias, axis=1)

    return all(distancia <= tolerancia for distancia in min_distancias)


def deteccao_formas():
    global container_opcoes
    container_opcoes = Frame(width=1500, height=135)
    container_opcoes.place(x=20, y=15)

    processando_imagem(120, 77)
    imagem_greyscale = greyscale(Image.open(root.caminhoImgOriginal))
    imagem_dilatada = dilatacao(dilatacao(imagem_greyscale))
    imagem_kirsch = kirsch(imagem_dilatada)

    # Coloca 50 pixels brancos a mais na imagem, para evitar índice fora do range se encontrar pixel preto na borda
    alt = imagem_kirsch.size[0]
    lar = imagem_kirsch.size[1]
    imagem_numpy = np.full([lar + 50, alt + 50, 3], 255, dtype=np.uint8)
    imagem_destino = Image.fromarray(imagem_numpy)
    for x in range(0, lar - 1):
        for y in range(0, alt - 1):
            valor = imagem_kirsch.getpixel((y, x))[0]
            if valor > 70:
                valor = 255
            else:
                valor = 0
            imagem_destino.putpixel((y + 25, x + 25), (valor, valor, valor))

    tabela_comparacoes = list()
    tabela_regioes = list()

    pilha = []
    num_regiao = 0
    alt = imagem_destino.size[0]
    lar = imagem_destino.size[1]
    for x in range(0, lar - 1):
        for y in range(0, alt - 1):
            if imagem_destino.getpixel((y, x))[0] == 0 and (y, x) not in tabela_comparacoes:
                num_regiao += 1
                pilha.append((y, x))
                tabela_comparacoes.append((y, x))
                tabela_regioes.append((num_regiao, (y, x)))
                while len(pilha) > 0:
                    if (peek(pilha)[0], peek(pilha)[1] + 1) not in tabela_comparacoes:
                        pixel = (peek(pilha)[0], peek(pilha)[1] + 1)
                        tabela_comparacoes.append(pixel)
                        if imagem_destino.getpixel(pixel)[0] == 0:
                            pilha.append(pixel)
                            tabela_regioes.append((num_regiao, pixel))
                    elif (peek(pilha)[0] - 1, peek(pilha)[1]) not in tabela_comparacoes:
                        pixel = (peek(pilha)[0] - 1, peek(pilha)[1])
                        tabela_comparacoes.append(pixel)
                        if imagem_destino.getpixel(pixel)[0] == 0:
                            pilha.append(pixel)
                            tabela_regioes.append((num_regiao, pixel))
                    elif (peek(pilha)[0], peek(pilha)[1] - 1) not in tabela_comparacoes:
                        pixel = (peek(pilha)[0], peek(pilha)[1] - 1)
                        tabela_comparacoes.append(pixel)
                        if imagem_destino.getpixel(pixel)[0] == 0:
                            pilha.append(pixel)
                            tabela_regioes.append((num_regiao, pixel))
                    elif (peek(pilha)[0] + 1, peek(pilha)[1]) not in tabela_comparacoes:
                        pixel = (peek(pilha)[0] + 1, peek(pilha)[1])
                        tabela_comparacoes.append(pixel)
                        if imagem_destino.getpixel(pixel)[0] == 0:
                            pilha.append(pixel)
                            tabela_regioes.append((num_regiao, pixel))
                    else:
                        pilha.pop()

    cores = [gera_cor_aleatoria() for _ in range(200)]

    imagem_teste_numpy = np.full([lar, alt, 3], 255, dtype=np.uint8)
    imagem_teste = Image.fromarray(imagem_teste_numpy)

    formas_quadrilaterais = dict()
    formas_circulares = dict()
    formas_triangulares = dict()
    regioes_identificadas = []

    for i in range(1, num_regiao + 1):
        filtrado = filter(lambda regiao: regiao[0] == i, tabela_regioes)
        coordenadas = list()
        for item in filtrado:
            coordenadas.append(item[1])

        # Começa processo para testar se forma é retângulo ou quadrado
        pontos = np.array(coordenadas)
        coord_x, coord_y = pontos[:, 0], pontos[:, 1]

        maior_x, maior_y = np.max(coord_x), np.max(coord_y)
        menor_x, menor_y = np.min(coord_x), np.min(coord_y)

        x_esquerdo = []
        x_direito = []
        for item in coord_x:
            if menor_x - 5 <= item <= menor_x + 5:
                x_esquerdo.append(item)
            if maior_x - 5 <= item <= maior_x + 5:
                x_direito.append(item)

        unique_x_esq, cont = np.unique(x_esquerdo, return_counts=True)
        linhas_x_esq = np.argsort(cont)[-1:]
        maior_x_esq = unique_x_esq[linhas_x_esq]

        unique_x_dir, cont = np.unique(x_direito, return_counts=True)
        linhas_x_dir = np.argsort(cont)[-1:]
        maior_x_dir = unique_x_dir[linhas_x_dir]

        y_superior = []
        y_inferior = []
        for item in coord_y:
            if menor_y - 5 <= item <= menor_y + 5:
                y_superior.append(item)
            if maior_y - 5 <= item <= maior_y + 5:
                y_inferior.append(item)

        unique_y_sup, cont = np.unique(y_superior, return_counts=True)
        linhas_y_sup = np.argsort(cont)[-1:]
        maior_y_sup = unique_y_sup[linhas_y_sup]

        unique_y_inf, cont = np.unique(y_inferior, return_counts=True)
        linhas_y_inf = np.argsort(cont)[-1:]
        maior_y_inf = unique_y_inf[linhas_y_inf]

        maior_linha_x_dir = []
        maior_linha_x_esq = []
        for item in coordenadas:
            if item[0] == maior_x_dir[0]:
                maior_linha_x_dir.append(item)
            if item[0] == maior_x_esq[0]:
                maior_linha_x_esq.append(item)

        maior_linha_y_sup = []
        maior_linha_y_inf = []
        for item in coordenadas:
            if item[1] == maior_y_sup[0]:
                maior_linha_y_sup.append(item)
            if item[1] == maior_y_inf[0]:
                maior_linha_y_inf.append(item)

        quadrilateral = False

        maiores_linhas_x = maior_linha_x_dir + maior_linha_x_esq
        maiores_linhas_y = maior_linha_y_sup + maior_linha_y_inf

        contador_cantos = 0
        for x in maiores_linhas_x:
            for y in maiores_linhas_y:
                if x == y:
                    contador_cantos += 1

        if 2 <= contador_cantos <= 4:
            direita = len(maior_linha_x_dir)
            esquerda = len(maior_linha_x_esq)
            superior = len(maior_linha_y_sup)
            inferior = len(maior_linha_y_inf)
            if (abs(direita - esquerda) <= (imagem_destino.size[0] * 0.05)) and (abs(superior - inferior) <= (imagem_destino.size[0] * 0.05)):
                quadrilateral = True
            elif abs(direita - esquerda) <= (imagem_destino.size[0] * 0.1):
                maior_linha = max(superior, inferior)
                menor_linha = min(superior, inferior)
                if ((menor_linha * 100) / maior_linha) > 15:
                    quadrilateral = True
            elif abs(superior - inferior) <= (imagem_destino.size[0] * 0.1):
                maior_linha = max(esquerda, direita)
                menor_linha = min(esquerda, direita)
                if ((menor_linha * 100) / maior_linha) > 15:
                    quadrilateral = True

        if quadrilateral:
            linhas = [maiores_linhas_x, maiores_linhas_y]

            if abs(len(maiores_linhas_x) - len(maiores_linhas_y)) <= (imagem_destino.size[0] * 0.05):
                formas_quadrilaterais.update({i: [linhas, 'Quadrado']})
                regioes_identificadas.append(i)
            else:
                formas_quadrilaterais.update({i: [linhas, 'Retangulo']})
                regioes_identificadas.append(i)

        # A partir daqui, processo para detecção de círculos
        pontos = np.array(coordenadas)
        coord_x = pontos[:, 0]

        maior_x, menor_x = np.max(coord_x), np.min(coord_x)
        raio = (maior_x - menor_x) // 2

        circunferencia = 2 * (math.pi * raio)
        media_pixels = len(coordenadas) / 2.7

        if abs(circunferencia - media_pixels) <= 6:
            formas_circulares.update({i: [coordenadas, 'Circulo']})
            regioes_identificadas.append(i)

        for item in coordenadas:
            imagem_destino.putpixel(item, cores[i - 1])

    # A partir daqui, método para detecção de triângulos
    for i in range(1, num_regiao + 1):
        if i not in regioes_identificadas:
            filtrado = filter(lambda regiao: regiao[0] == i, tabela_regioes)
            coordenadas = list()
            for coord in filtrado:
                coordenadas.append(coord[1])

            pontos = np.array(coordenadas)
            coord_x = pontos[:, 0]
            maior_x, menor_x = np.max(coord_x), np.min(coord_x)

            coord_y = pontos[:, 1]
            maior_y, menor_y = np.max(coord_y), np.min(coord_y)

            linhas_horizontais = dict()
            for pixel in coordenadas:
                if menor_x <= pixel[0] <= maior_x:
                    if pixel[1] in linhas_horizontais:
                        linhas_horizontais[pixel[1]].append(pixel[0])
                    else:
                        linhas_horizontais[pixel[1]] = [pixel[0]]

            for chave in list(linhas_horizontais):
                linhas_horizontais.get(chave).sort()
                if not array_sequencial(linhas_horizontais.get(chave)):
                    linhas_horizontais.pop(chave)
                elif len(linhas_horizontais.get(chave)) < 12:
                    linhas_horizontais.pop(chave)

            linha_horizontal_principal = []
            if len(linhas_horizontais) > 0:
                y = min(list(linhas_horizontais))
                for item in linhas_horizontais.get(y):
                    linha_horizontal_principal.append((item, y))

            linhas_verticais = dict()
            for pixel in coordenadas:
                if menor_y <= pixel[1] <= maior_y:
                    if pixel[0] in linhas_verticais:
                        linhas_verticais[pixel[0]].append(pixel[1])
                    else:
                        linhas_verticais[pixel[0]] = [pixel[1]]

            for chave in list(linhas_verticais):
                linhas_verticais.get(chave).sort()
                if not array_sequencial(linhas_verticais.get(chave)):
                    linhas_verticais.pop(chave)
                elif len(linhas_verticais.get(chave)) < 12:
                    linhas_verticais.pop(chave)

            linha_vertical_principal = []
            if len(linhas_verticais) > 0:
                x = min(list(linhas_verticais))
                for item in linhas_verticais.get(x):
                    linha_vertical_principal.append((x, item))

            if len(linha_horizontal_principal) > 0 and len(linha_vertical_principal) > 0:
                # Possível triângulo retângulo
                for coordX in linha_horizontal_principal:
                    for coordY in linha_vertical_principal:
                        if coordX[0] == coordY[0] and coordX[1] == coordY[1]:
                            formas_triangulares.update({i: [coordenadas, 'Triangulo']})
            elif len(linha_horizontal_principal) > 0:
                # Possível triângulo isósceles
                pixel_medio = linha_horizontal_principal[len(linha_horizontal_principal) // 2]
                ponto_medio = pixel_medio[0]
                for pixel in coordenadas:
                    if pixel[1] < pixel_medio[1] and pixel[1] == menor_y and pixel[0] == ponto_medio:
                        formas_triangulares.update({i: [coordenadas, 'Triangulo']})
                    elif pixel[1] > pixel_medio[1] and pixel[1] == maior_y and pixel[0] == ponto_medio:
                        formas_triangulares.update({i: [coordenadas, 'Triangulo']})

    # Identifica se formas quadrilaterais estão muito próximas umas das outras, para manter apenas uma
    for i in range(1, num_regiao):
        for j in range(2, num_regiao + 1):
            if formas_quadrilaterais.get(i) and formas_quadrilaterais.get(j):
                if i != j:
                    if (formas_proximas(formas_quadrilaterais.get(i)[0][0], formas_quadrilaterais.get(j)[0][0], 15) and
                            formas_proximas(formas_quadrilaterais.get(i)[0][1], formas_quadrilaterais.get(j)[0][1], 15)):
                        formas_quadrilaterais.pop(j)
                        regioes_identificadas.pop(j)

    # Identifica se formas circulares estão muito próximas umas das outras, para manter apenas uma
    for i in range(1, num_regiao):
        for j in range(2, num_regiao + 1):
            if formas_circulares.get(i) and formas_circulares.get(j):
                if i != j:
                    if formas_proximas(formas_circulares.get(i)[0], formas_circulares.get(j)[0], 15):
                        formas_circulares.pop(j)

    # Identifca se formas triangulares estão muito próximas umas das outras, para manter apenas uma
    for i in range(1, num_regiao):
        for j in range(2, num_regiao + 1):
            if formas_triangulares.get(i) and formas_triangulares.get(j):
                if i != j:
                    if formas_proximas(formas_triangulares.get(i)[0], formas_triangulares.get(j)[0], 15):
                        formas_triangulares.pop(j)

    # Desenha imagem para conferência com as formas encontradas
    for chave in formas_quadrilaterais:
        coords = formas_quadrilaterais.get(chave)[0][0] + formas_quadrilaterais.get(chave)[0][1]
        for item in coords:
            imagem_teste.putpixel(item, (0, 0, 0))

    for chave in formas_circulares:
        for item in formas_circulares.get(chave)[0]:
            imagem_teste.putpixel(item, (0, 0, 0))

    for chave in formas_triangulares:
        for item in formas_triangulares.get(chave)[0]:
            imagem_teste.putpixel(item, (0, 0, 0))

    # Escreve o nome das formas encontradas na imagem para conferência
    imagem_mostrar = np.array(imagem_teste)
    for chave in formas_quadrilaterais:
        cv2.putText(imagem_mostrar, str(chave) + '-' + formas_quadrilaterais.get(chave)[1],
                    formas_quadrilaterais.get(chave)[0][0][0],
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for chave in formas_circulares:
        cv2.putText(imagem_mostrar, str(chave) + '-' + formas_circulares.get(chave)[1],
                    formas_circulares.get(chave)[0][0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    for chave in formas_triangulares:
        cv2.putText(imagem_mostrar, str(chave) + '-' + formas_triangulares.get(chave)[1],
                    formas_triangulares.get(chave)[0][0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    instancia_imagem_processada(Image.fromarray(imagem_mostrar))
    container_opcoes.winfo_children().pop().destroy()


def array_sequencial(arr):
    n = len(arr)
    for i in range(n - 1):
        if arr[i] != arr[i + 1] - 1:
            return False
    return True


def peek(pilha):
    if pilha:
        return pilha[-1]


def sobre():
    tkinter.messagebox.showinfo('Informação', 'Autor: Diego Roberto Johann\nVersão: 1.0')


root = Tk()
root.resizable(False, False)

# Configuração do menu superior
# -----------------------------------------------------------------------
menubar = Menu(root)
root.config(menu=menubar)

menu_arquivo = Menu(menubar, tearoff=0)

menu_arquivo.add_command(label='Abrir Imagem', command=carrega_imagem)
menu_arquivo.add_command(label='Salvar Imagem', command=salva_imagem)
menu_arquivo.add_command(label='Sobre', command=sobre)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair', command=root.destroy)

menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_transformacoes = Menu(menubar, tearoff=0)

menu_transformacoes.add_command(label='Translação', command=abre_menu_translacao)
menu_transformacoes.add_command(label='Ampliação', command=abre_menu_ampliacao)
menu_transformacoes.add_command(label='Redução', command=abre_menu_reducao)
menu_transformacoes.add_command(label='Espelhamento', command=abre_menu_espelhamento)
menu_transformacoes.add_command(label='Rotação', command=abre_menu_rotacao)

menubar.add_cascade(label="Transformações", menu=menu_transformacoes)

menu_filtros = Menu(menubar, tearoff=0)

menu_filtros.add_command(label='Pré-processamento', command=abre_menu_preprocessamento)
menu_filtros.add_command(label='Passa Baixa', command=abre_menu_passabaixa)
menu_filtros.add_command(label='Passa Alta', command=abre_menu_passaalta)
menu_filtros.add_command(label='Threshold', command=abre_menu_treshold)

menubar.add_cascade(label="Filtros", menu=menu_filtros)

menu_morfologia = Menu(menubar, tearoff=0)

menu_morfologia.add_command(label='Dilatação',
                            command=lambda: instancia_imagem_processada(dilatacao(Image.open(root.caminhoImgOriginal))))
menu_morfologia.add_command(label='Erosão',
                            command=lambda: instancia_imagem_processada(erosao(Image.open(root.caminhoImgOriginal))))
menu_morfologia.add_command(label='Abertura',
                            command=lambda: instancia_imagem_processada(
                                dilatacao(erosao(Image.open(root.caminhoImgOriginal)))))
menu_morfologia.add_command(label='Fechamento',
                            command=lambda: instancia_imagem_processada(
                                erosao(dilatacao(Image.open(root.caminhoImgOriginal)))))

menubar.add_cascade(label="Morfologia Matemática", menu=menu_morfologia)

menu_extracao = Menu(menubar, tearoff=0)

menu_extracao.add_command(label='Extração de formas', command=deteccao_formas)

menubar.add_cascade(label="Desafio", menu=menu_extracao)

# ------------------------------------------------------------------------------
# Configuração da janela

root.state('zoomed')
# root.attributes('-zoomed', True)
# root.attributes('-topmost', True)
# root.geometry('1900x950')
root.title('PDI')

# center(root)

root.caminhoImgOriginal = os.path.join('imagens', 'noimage.jpg')
root.caminhoImgProcessada = os.path.join('imagens', 'noimage.jpg')

fontePadrao = ('Tahoma', '10')
fonteProcessando = ('Tahoma', '11', 'bold')

container_opcoes = Frame()
menu = ''

lbl_dica = Label(root, text='Carregue uma imagem no menu Arquivo, e depois escolha a opção desejada de processamento', font=fontePadrao)
lbl_dica.place(x=20, y=9)

containerImagens = Frame(root)
containerImagens['pady'] = 20
containerImagens['width'] = 1900
containerImagens['height'] = 820
containerImagens.place(x=20, y=130)

boxImagemOriginal = LabelFrame(containerImagens, text='Imagem Original', font=fontePadrao)
boxImagemOriginal['pady'] = 5
boxImagemOriginal['width'] = 800
boxImagemOriginal['height'] = 800
boxImagemOriginal.place(x=0, y=0)

imagemOriginal = ImageTk.PhotoImage(Image.open(root.caminhoImgOriginal).resize((770, 770)))
frmImagemOriginal = Label(boxImagemOriginal, image=imagemOriginal)
frmImagemOriginal.place(x=0, y=0)

boxImagemProcessada = LabelFrame(containerImagens, text='Imagem Processada', font=fontePadrao)
boxImagemProcessada['pady'] = 5
boxImagemProcessada['width'] = 800
boxImagemProcessada['height'] = 800
boxImagemProcessada.place(x=820, y=0)

imagemProcessada = ImageTk.PhotoImage(Image.open(root.caminhoImgProcessada).resize((770, 770)))
frmImagemProcessada = Label(boxImagemProcessada, image=imagemProcessada)
frmImagemProcessada.place(x=0, y=0)

root.mainloop()
