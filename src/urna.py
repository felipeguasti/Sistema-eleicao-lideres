import tkinter as tk
import csv
import subprocess
from tkinter import ttk
import datetime
from PIL import Image, ImageTk

file_path = 'data/eleitores.csv'

def carregar_turmas():
    turmas = set()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pule o cabeçalho se houver um

        for row in reader:
            turma = row[1].strip()
            turmas.add(turma)

    return sorted(turmas)

def carregar_nomes_da_turma(turma_selecionada):
    nomes = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pule o cabeçalho

        for row in reader:
            nome, turma = row[0].strip(), row[1].strip()
            if turma == turma_selecionada:
                nomes.append(nome)

    return nomes

def criar_segunda_tela(turma_selecionada):
    segunda_tela = tk.Toplevel()
    segunda_tela.title("Escolha seu Nome")

    # Abre a segunda tela maximizada
    segunda_tela.state('zoomed')

    cor_de_fundo = "#3498db"
    cor_texto = "white"

    segunda_tela.configure(bg=cor_de_fundo)

    titulo_cabecalho = tk.Label(segunda_tela, text="Votação do líder de turma do " + turma_selecionada, font=("Helvetica", 36, "bold"), bg=cor_de_fundo, fg=cor_texto)
    titulo_cabecalho.pack(pady=20)

    escola_label = tk.Label(segunda_tela, text="EEEFM Coronel Olímpio Cunha", font=("Helvetica", 20), bg=cor_de_fundo, fg=cor_texto)
    escola_label.pack()

    # Cria um frame para centralizar elementos
    frame_central = tk.Frame(segunda_tela, bg=cor_de_fundo)
    frame_central.pack(expand=True, fill='both')

    titulo = tk.Label(frame_central, text="Escolha o seu nome na Lista Abaixo", font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
    titulo.pack(pady=(100,0), padx=0)

    nomes_da_turma = carregar_nomes_da_turma(turma_selecionada)

    var_nome = tk.StringVar(segunda_tela)
    var_nome.set(nomes_da_turma[0])

    dropdown_nome = tk.OptionMenu(frame_central, var_nome, *nomes_da_turma)
    dropdown_nome.config(font=("Helvetica", 20), bg=cor_de_fundo, fg=cor_texto)
    dropdown_nome.pack(pady=(0, 20), padx=0)

    def voltar():
        segunda_tela.destroy()
        criar_janela_selecao_turma()

    def avancar():
        nome_selecionado = var_nome.get()
        subprocess.Popen(["python", "votacao.py", nome_selecionado, turma_selecionada])
        segunda_tela.destroy()


    # Cria um frame para posicionar os botões lado a lado
    frame_botoes = tk.Frame(frame_central, bg=cor_de_fundo)
    frame_botoes.pack()

    btn_voltar = tk.Button(frame_botoes, text="Voltar", font=("Helvetica", 20), bg="#e74c3c", fg=cor_texto, padx=20, pady=10, command=voltar)
    btn_voltar.pack(side=tk.LEFT, padx=10)

    btn_avancar = tk.Button(frame_botoes, text="Avançar", font=("Helvetica", 20), bg="#2ecc71", fg=cor_texto, padx=20, pady=10, command=avancar)
    btn_avancar.pack(side=tk.LEFT, padx=10)

def criar_janela_selecao_turma():
    janela = tk.Tk()
    janela.title("Seleção de Turma")

    # Abre a janela principal maximizada
    janela.state('zoomed')

    cor_de_fundo = "#3498db"
    cor_texto = "white"

    janela.configure(bg=cor_de_fundo)

    current_time = datetime.datetime.now()

    titulo = tk.Label(janela, text=f"Eleição do lider de turma {current_time.year}", font=("Helvetica", 36, "bold"), bg=cor_de_fundo, fg=cor_texto)
    titulo.pack(pady=20)
    titulo = tk.Label(janela, text="EEEFM Coronel Olímpio Cunha", font=("Helvetica", 20, "bold"), bg=cor_de_fundo, fg=cor_texto)
    titulo.pack(pady=0)

    titulo = tk.Label(janela, text="Selecione sua Turma", font=("Helvetica", 30), bg=cor_de_fundo, fg=cor_texto)
    titulo.pack(pady=(200,0), padx=0)

    turmas = carregar_turmas()

    var_turma = tk.StringVar(janela)
    var_turma.set(turmas[0])

    dropdown_turma = tk.OptionMenu(janela, var_turma, *turmas)
    dropdown_turma.config(font=("Helvetica", 20), bg=cor_de_fundo, fg=cor_texto)
    dropdown_turma.pack(pady=10)

    def avancar():
        turma_selecionada = var_turma.get()
        criar_segunda_tela(turma_selecionada)
        janela.withdraw()

    btn_avancar = tk.Button(janela, text="Avançar", font=("Helvetica", 20), bg="#2ecc71", fg=cor_texto, padx=20, pady=10, command=avancar)
    btn_avancar.pack(pady=20)

    janela.mainloop()

if __name__ == '__main__':
    criar_janela_selecao_turma()
