import tkinter as tk
from tkinter import ttk
import csv
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import threading
from PIL import Image, ImageTk
import sys

# Função para carregar as turmas do arquivo de votos
def carregar_turmas():
    turmas = []
    with open('data/votos.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            turma = row[1]  # A turma está na segunda coluna do arquivo
            if turma not in turmas:
                turmas.append(turma)
    return turmas

# Função para carregar todos os candidatos com base nas turmas
def carregar_candidatos(turma_selecionada):
    candidatos = {}
    with open('data/votos.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nome = row[2]  # O nome do candidato está na terceira coluna do arquivo
            turma = row[1]  # A turma está na segunda coluna do arquivo
            if turma_selecionada == "Todas as turmas" or turma_selecionada == turma:
                if nome in candidatos:
                    candidatos[nome] += 1
                else:
                    candidatos[nome] = 1
    # Classifique os candidatos com base na contagem de votos
    candidatos_ordenados = sorted(candidatos.items(), key=lambda x: (-x[1], x[0]))
    return candidatos_ordenados

# Função para atualizar a lista de candidatos com base na turma selecionada
def atualizar_candidatos(event):
    # Limpa a lista de candidatos
    texto_candidatos.config(state='normal')
    texto_candidatos.delete('1.0', 'end')

    # Obtém a turma selecionada
    turma_selecionada = combo_turmas.get()

    if turma_selecionada:
        if turma_selecionada == "Todas as turmas":
            turmas = carregar_turmas()
            for turma in turmas:
                texto_candidatos.insert('end', f"Turma: {turma}\n")
                candidatos = carregar_candidatos(turma)
                for i, (candidato, votos) in enumerate(candidatos, 1):
                    plural = "s" if votos != 1 else ""
                    texto_candidatos.insert('end', f"{i}. {candidato} - {votos} Voto{plural}\n")
        else:
            texto_candidatos.insert('end', f"Turma: {turma_selecionada}\n")
            candidatos = carregar_candidatos(turma_selecionada)
            for i, (candidato, votos) in enumerate(candidatos, 1):
                plural = "s" if votos != 1 else ""
                texto_candidatos.insert('end', f"{i}. {candidato} - {votos} Voto{plural}\n")

        texto_candidatos.config(state='disabled')

# Função para obter os candidatos ordenados por quantidade de votos
def obter_candidatos_ordenados(candidatos):
    return sorted(candidatos, key=lambda x: (-candidatos.count(x), x))

# Função para formatar os candidatos no relatório
def formatar_candidatos(candidatos_ordenados):
    texto_formatado = ""
    for i, candidato in enumerate(candidatos_ordenados, 1):
        votos = candidatos_ordenados.count(candidato)
        plural = "s" if votos != 1 else ""
        texto_formatado += f"{i}. {candidato} - {votos} Voto{plural}\n"
    texto_formatado += "\n"
    return texto_formatado

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Função para criar o PDF com o relatório
def criar_pdf(aviso_label):
    # Obtém a turma selecionada
    turma_selecionada = combo_turmas.get()
    
    if turma_selecionada:
        try:
            # Obtenha o caminho da pasta "Downloads" do usuário atual
            pasta_downloads = os.path.expanduser("~\Downloads")
            
            # Crie o nome do arquivo PDF com base na turma e no ano
            nome_arquivo = f"{pasta_downloads}/{turma_selecionada} - Resultado das eleições {datetime.datetime.now().year}.pdf"
            doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
            elementos = []

            # Estilos do ReportLab para o título
            styles = getSampleStyleSheet()
            style_title = styles['Title']
            
            # Adicione o título
            titulo = Paragraph("Relatório das Eleições de Líder de Turma", style_title)
            elementos.append(titulo)
            
            # Adicione a turma ao PDF
            elementos.append(Paragraph(f"Turma: {turma_selecionada}", style_title))
            
            # Obtém a lista de candidatos da turma selecionada
            candidatos = carregar_candidatos(turma_selecionada)
            
            # Ordena os candidatos por quantidade de votos
            candidatos_ordenados = obter_candidatos_ordenados(candidatos)
            
            # Formata os candidatos em uma tabela para o PDF
            data = [['Posição', 'Candidato', 'Votos', 'Turma']]
    
            for i, (candidato, votos) in enumerate(candidatos_ordenados, 1):
                plural = "s" if votos != 1 else ""
                data.append([str(i), candidato, f"{votos} Voto{plural}", turma_selecionada])
            
            # Cria a tabela e aplica o estilo
            table = Table(data, colWidths=[1 * inch, 3 * inch, 1 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elementos.append(table)
            
            # Tente criar o PDF
            doc.build(elementos)
            aviso_label.config(text="Download concluído. Arquivo na pasta download", foreground="green")
        except Exception as e:
            # Em caso de erro, exiba a mensagem vermelha
            aviso_label.config(text="Erro ao criar o PDF.", foreground="red")
            print(e)
        finally:
            # Crie uma função para redefinir o texto do rótulo após 2 segundos
            def reset_aviso():
                aviso_label.config(text="")
            # Inicie uma thread para chamar a função reset_aviso após 2 segundos
            threading.Timer(2, reset_aviso).start()

# Crie a janela principal
janela = tk.Tk()
janela.title("Relatório de Eleições")
janela.state('zoomed')  # Abra a janela maximizada

executavel_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
caminho_logo = os.path.join(executavel_dir, 'favi.ico')

if os.path.exists(caminho_logo):
    imagem = Image.open(caminho_logo)
    janela.iconphoto(True, ImageTk.PhotoImage(imagem))
else:
    imagem = None

# Defina cores
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
titulo = tk.Label(frame_principal, text=f"Resultado das Eleições de Líder de Turma {datetime.datetime.now().year}", font=("Helvetica", 36), bg=cor_de_fundo, fg=cor_texto)
titulo.pack(pady=20)

# Adicione a caixa de seleção de turmas, incluindo a opção "Todas as turmas"
turmas = carregar_turmas()
turmas.insert(0, "Todas as turmas")
combo_turmas = ttk.Combobox(frame_principal, values=turmas, state="readonly", font=("Helvetica", 26), width=30)
combo_turmas.set("Selecione a turma")
combo_turmas.bind("<<ComboboxSelected>>", atualizar_candidatos)
combo_turmas.pack(padx=10, pady=0)


# Adicione o campo de texto para exibir os candidatos
texto_candidatos = tk.Text(frame_principal, font=("Helvetica", 16), bg=cor_de_fundo, fg=cor_texto, state='disabled', wrap=tk.WORD, height=20)
texto_candidatos.pack(padx=10, pady=10, fill='both', expand=True)


# Defina o estilo do rótulo de aviso
style = ttk.Style()
style.configure("Aviso.TLabel", background=cor_de_fundo, font=("Helvetica", 16))

# Adicione um rótulo para exibir a mensagem
aviso_label = ttk.Label(frame_principal, text="", foreground="green", style="Aviso.TLabel")
aviso_label.pack(padx=10, pady=5)

# Exiba o botão de download do PDF
botao_pdf = ttk.Button(frame_principal, text="Download PDF", command=lambda: criar_pdf(aviso_label), style="Custom.TButton")
botao_pdf.pack(padx=10, pady=(0, 30))  # Ajuste o espaço vertical

# Configurar a rolagem
canvas.create_window((janela.winfo_width() // 2, 0), window=frame_principal, anchor="n")
canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Configurar a rolagem com a roda do mouse
def on_mouse_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
frame_principal.bind_all("<MouseWheel>", on_mouse_scroll)

# Exiba a janela
janela.mainloop()

