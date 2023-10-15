import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Canvas
import os
import shutil
import sys

def abrir_urna():
    os.system("python urna.py")

def abrir_relatorio():
    os.system("python relatorio.py")

def fazer_upload(arquivo_destino):
    arquivo_origem = filedialog.askopenfilename()
    if arquivo_origem:
        try:
            if os.path.exists(arquivo_destino):
                os.remove(arquivo_destino)
            shutil.copy(arquivo_origem, arquivo_destino)
            mensagem.config(text="Arquivo carregado com sucesso.", fg="green")
        except Exception as e:
            mensagem.config(text="Erro ao carregar o arquivo.", fg="red")
            print(e)

def fazer_upload_imagens():
    arquivos_origem = filedialog.askopenfilenames()
    if arquivos_origem:
        for arquivo_origem in arquivos_origem:
            nome_arquivo = os.path.basename(arquivo_origem)
            destino = os.path.join("images", nome_arquivo)
            try:
                shutil.copy(arquivo_origem, destino)
                mensagem.config(text="Imagens carregadas com sucesso.", fg="green")
            except Exception as e:
                mensagem.config(text="Erro ao carregar as imagens.", fg="red")
                print(e)

def apagar_votacao():
    try:
        if os.path.exists("data/votos.csv"):
            os.remove("data/votos.csv")
            mensagem.config(text="Dados da votação apagados com sucesso.", fg="green")
        else:
            mensagem.config(text="Nenhum dado de votação encontrado.", fg="red")
        if os.exists("images"):
            shutil.rmtree("images")
            os.mkdir("images")
    except Exception as e:
        mensagem.config(text="Erro ao apagar os dados da votação ou pasta 'images'.", fg="red")
        print(e)

janela = tk.Tk()
janela.title("Sistema de Votação de Líder Escolar")
janela.state('zoomed')

executavel_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
caminho_logo = os.path.join(executavel_dir, 'favi.ico')

if os.path.exists(caminho_logo):
    imagem = Image.open(caminho_logo)
    janela.iconphoto(True, ImageTk.PhotoImage(imagem))
else:
    imagem = None

cor_de_fundo = "#3498db"
cor_texto = "white"

# Usar um canvas para habilitar a rolagem
canvas = tk.Canvas(janela, bg=cor_de_fundo)
canvas.pack(side="left", fill="both", expand=True)

# Adicionar barra de rolagem vertical
scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Frame principal dentro do canvas
frame_principal = tk.Frame(canvas, bg=cor_de_fundo)

# Adicione o título
titulo = tk.Label(frame_principal, text="Bem-vindo ao Sistema de Votação de Líder Escolar", font=("Helvetica", 30), bg=cor_de_fundo, fg=cor_texto)
titulo.pack(pady=20)

nome_escola = tk.Label(frame_principal, text="EEEFM Coronel Olímpio Cunha", font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
nome_escola.pack(pady=0)

imagem = Image.open("logo.png")
imagem.thumbnail((200, 100))
imagem = ImageTk.PhotoImage(imagem)
label_imagem = tk.Label(frame_principal, image=imagem, bg=cor_de_fundo)
label_imagem.image = imagem
label_imagem.pack(pady=10)

frame_botoes = tk.Frame(frame_principal, bg=cor_de_fundo)
frame_botoes.pack()

botao_urna = tk.Button(frame_botoes, text="Urna Eletrônica", font=("Helvetica", 20), command=abrir_urna, bg="#27ae60", fg="white")
botao_urna.grid(row=0, column=0, padx=40, pady=10)

botao_relatorio = tk.Button(frame_botoes, text="Relatório de Votação", font=("Helvetica", 20), command=abrir_relatorio, bg="#e74c3c", fg="white")
botao_relatorio.grid(row=0, column=1, padx=40, pady=10)

configuracao_label = tk.Label(frame_principal, text="Configure a votação aqui:", font=("Helvetica", 20), bg=cor_de_fundo, fg=cor_texto)
configuracao_label.pack(pady=10)

mensagem_candidatos = tk.Label(frame_principal, text="Faça upload do arquivo CSV com os candidatos (Nome,Número,Turma,Foto)", font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
mensagem_candidatos.pack(pady=5)

botao_upload_candidatos = tk.Button(frame_principal, text="Upload de Candidatos", font=("Helvetica", 16), command=lambda: fazer_upload("data/candidatos.csv"), bg=cor_de_fundo, fg="white")
botao_upload_candidatos.pack(pady=5)

mensagem_eleitores = tk.Label(frame_principal, text="Faça upload do arquivo CSV com os eleitores (Nome,Turma)", font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
mensagem_eleitores.pack(pady=5)

botao_upload_eleitores = tk.Button(frame_principal, text="Upload de Eleitores", font=("Helvetica", 16), command=lambda: fazer_upload("data/eleitores.csv"), bg=cor_de_fundo, fg="white")
botao_upload_eleitores.pack(pady=5)

mensagem_imagens = tk.Label(frame_principal, text="Faça upload de imagens para candidatos. (Mesmo nome do informado no candidatos.csv)", font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto)
mensagem_imagens.pack(pady=5)

botao_upload_imagens = tk.Button(frame_principal, text="Upload de Imagens", font=("Helvetica", 16), command=fazer_upload_imagens, bg=cor_de_fundo, fg="white")
botao_upload_imagens.pack(pady=5)

mensagem_votacao = tk.Label(frame_principal, text="Isso é irreversível. Tenha certeza do que você está fazendo.", font=("Helvetica", 16), bg=cor_de_fundo, fg="black")
mensagem_votacao.pack(pady=0)

botao_apagar_votacao = tk.Button(frame_principal, text="Apagar votação", font=("Helvetica", 16), command=apagar_votacao, bg="#e74c3c", fg="white")
botao_apagar_votacao.pack(pady=5)

mensagem = tk.Label(frame_principal, text="", font=("Helvetica", 16), bg=cor_de_fundo, fg="black")
mensagem.pack(pady=0)

# Configurar a rolagem
canvas.create_window((janela.winfo_width() // 2, 0), window=frame_principal, anchor="n")
canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Configurar a rolagem com a roda do mouse
def on_mouse_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
frame_principal.bind_all("<MouseWheel>", on_mouse_scroll)

janela.mainloop()

