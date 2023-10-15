import tkinter as tk
from PIL import Image, ImageTk
import csv
import os
import time
import subprocess
import sys

# Verifica se os argumentos foram passados na linha de comando
if len(sys.argv) >= 3:
    nome_eleitor = sys.argv[1]
    turma_eleitor = sys.argv[2]
else:
    # Trate o caso em que os argumentos não foram passados
    nome_eleitor = "Escolha uma turma"
    turma_eleitor = "Escolha um eleitor"

# Caminho para o arquivo de candidatos
candidatos_file_path = 'data/candidatos.csv'

# Caminho para a pasta de imagens de candidatos
imagens_candidatos_path = 'images'

# Função para gravar o voto em um arquivo CSV e lidar com a interface
def gravar_voto(nome_candidato):
    # Formate a linha de voto
    linha_voto = [nome_eleitor, turma_eleitor, nome_candidato]

    # Abra o arquivo CSV
    with open('data/votos.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Escreva a linha de voto no arquivo
        writer.writerow(linha_voto)

    # Limpe a tela
    limpar_tela()

    # Exiba a mensagem de sucesso
    mensagem_sucesso = f"{nome_eleitor}, seu voto para\n {nome_candidato} \nfoi computado com sucesso!"

    mensagem_label = tk.Label(votacao_tela, text=mensagem_sucesso, font=("Helvetica", 20), bg=cor_de_fundo, fg=cor_texto)
    mensagem_label.place(relx=0.5, rely=0.5, anchor='center')

    votacao_tela.update()

    # Aguarde 5 segundos antes de iniciar a próxima votação e executar urna.py
    votacao_tela.after(3000, iniciar_urna)

# Função para iniciar urna.py
def iniciar_urna():
    votacao_tela.destroy()  # Fecha a aplicação atual
    subprocess.run(["python", "urna.py"])  # Execute urna.py

# Função para limpar a tela
def limpar_tela():
    for widget in votacao_tela.winfo_children():
        widget.destroy()

# Carregue a lista de candidatos com base na turma do eleitor
def carregar_candidatos(turma):
    candidatos = []
    with open(candidatos_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pule o cabeçalho

        for row in reader:
            nome, numero, turma_candidato, foto = row
            if turma_candidato == turma:
                candidatos.append((nome, numero, foto))

    return candidatos

# Crie a tela de votação
def criar_tela_de_votacao():
    global votacao_tela  # Tornar a janela de votação global para que possamos acessá-la em diferentes funções
    votacao_tela = tk.Tk()
    votacao_tela.title("Votação")

    # Defina o tamanho da tela de votação com base na resolução da tela
    largura_tela = votacao_tela.winfo_screenwidth()
    altura_tela = votacao_tela.winfo_screenheight()
    votacao_tela.geometry(f"{largura_tela}x{altura_tela}")

    global cor_de_fundo, cor_texto  # Defina as cores como globais
    cor_de_fundo = "#3498db"
    cor_texto = "white"

    votacao_tela.configure(bg=cor_de_fundo)

    cabecalho_text = "Vote no líder de turma do " + turma_eleitor
    titulo_cabecalho = tk.Label(votacao_tela, text=cabecalho_text, font=("Helvetica", 36, "bold"), bg=cor_de_fundo, fg=cor_texto)
    titulo_cabecalho.pack(pady=20)

    # Crie um quadro para dispor os candidatos em um grid centralizado
    candidato_quadro = tk.Frame(votacao_tela, bg=cor_de_fundo)
    candidato_quadro.place(relx=0.5, rely=0.5, anchor='center')

    # Defina a quantidade de colunas e linhas no grid
    num_colunas = 4
    num_linhas = 3

    for i, (nome, numero, foto) in enumerate(carregar_candidatos(turma_eleitor), 1):
        linha = (i - 1) // num_colunas
        coluna = (i - 1) % num_colunas

        candidato_frame = tk.Frame(candidato_quadro, bg=cor_de_fundo)
        candidato_frame.grid(row=linha, column=coluna, padx=10, pady=10)

        # Carregue a imagem do candidato da pasta de imagens
        foto_path = os.path.join(imagens_candidatos_path, foto)
        imagem = Image.open(foto_path)
        imagem.thumbnail((200, 200))
        foto_candidato = ImageTk.PhotoImage(imagem)

        # Exiba a imagem do candidato
        imagem_label = tk.Label(candidato_frame, image=foto_candidato, bg=cor_de_fundo)
        imagem_label.image = foto_candidato
        imagem_label.pack()

        # Exiba o nome e o número do candidato
        nome_label = tk.Label(candidato_frame, text=nome, font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
        nome_label.pack(pady=10)
        numero_label = tk.Label(candidato_frame, text="Número: " + numero, font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
        numero_label.pack(pady=10)

        # Botão de voto para o candidato
        votar_button = tk.Button(candidato_frame, text="Votar", font=("Helvetica", 20), bg="#2ecc71", fg=cor_texto, padx=20, pady=10, command=lambda nome=nome: gravar_voto(nome))
        votar_button.pack(pady=10)

    votacao_tela.mainloop()

if __name__ == '__main__':
    criar_tela_de_votacao()
