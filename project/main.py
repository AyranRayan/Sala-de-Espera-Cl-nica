import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from gtts import gTTS
import os
import tempfile
from datetime import datetime

class SistemaChamadas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Chamadas - Consultório")
        self.root.state('zoomed')  # Maximiza a janela

        # Inicializa pygame para sons
        pygame.mixer.init()
        
        # Dados
        self.procedimentos = {}  # Dicionário para armazenar pacientes por procedimento
        self.pacientes_chamados = []

        # Cores e estilos
        self.bg_color = "#2E8B57"  # Verde escuro
        self.text_color = "white"
        self.highlight_color = "#98FB98"  # Verde claro

        # Layout principal
        self.frame_esquerdo = tk.Frame(root, width=800)
        self.frame_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.frame_direito = tk.Frame(root, bg=self.bg_color)
        self.frame_direito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.criar_area_cadastro()
        self.criar_area_tv()

    def criar_area_cadastro(self):
        # Área de Cadastro de Procedimentos
        frame_proc = tk.LabelFrame(self.frame_esquerdo, text="Cadastro de Procedimentos", 
                                 padx=10, pady=10, font=("Helvetica", 12, "bold"))
        frame_proc.pack(fill=tk.X, pady=10)

        tk.Label(frame_proc, text="Procedimento:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        self.entry_proc = tk.Entry(frame_proc, width=30, font=("Helvetica", 10))
        self.entry_proc.grid(row=0, column=1, padx=5)

        tk.Label(frame_proc, text="Sala:", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)
        self.entry_sala = tk.Entry(frame_proc, width=10, font=("Helvetica", 10))
        self.entry_sala.grid(row=0, column=3, padx=5)

        tk.Button(frame_proc, text="Cadastrar Procedimento", 
                 command=self.cadastrar_procedimento,
                 font=("Helvetica", 10, "bold"),
                 bg="#4CAF50", fg="white").grid(row=0, column=4, padx=5)

        # Lista de Procedimentos
        self.lista_proc = tk.Listbox(frame_proc, width=50, height=5, font=("Helvetica", 10))
        self.lista_proc.grid(row=1, column=0, columnspan=5, pady=10)

        # Área de Cadastro de Pacientes
        frame_pac = tk.LabelFrame(self.frame_esquerdo, text="Cadastro de Pacientes", 
                                padx=10, pady=10, font=("Helvetica", 12, "bold"))
        frame_pac.pack(fill=tk.X, pady=10)

        tk.Label(frame_pac, text="Nome do Paciente:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        self.entry_nome = tk.Entry(frame_pac, width=40, font=("Helvetica", 10))
        self.entry_nome.grid(row=0, column=1, columnspan=2, padx=5)

        tk.Label(frame_pac, text="Procedimento:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.combo_proc = ttk.Combobox(frame_pac, width=37, font=("Helvetica", 10))
        self.combo_proc.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(frame_pac, text="Cadastrar Paciente",
                 command=self.cadastrar_paciente,
                 font=("Helvetica", 10, "bold"),
                 bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

        # Frame para listas de pacientes por procedimento
        self.frame_listas = tk.Frame(frame_pac)
        self.frame_listas.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def criar_area_tv(self):
        # Título
        titulo = tk.Label(self.frame_direito, 
                         text="PAINEL DE CHAMADAS", 
                         font=("Montserrat", 42, "bold"), 
                         bg=self.bg_color, 
                         fg=self.text_color)
        titulo.pack(pady=30)

        # Área de chamada atual
        self.frame_chamada_atual = tk.Frame(self.frame_direito, bg=self.bg_color)
        self.frame_chamada_atual.pack(fill=tk.X, pady=30)

        self.label_chamada_atual = tk.Label(self.frame_chamada_atual, 
                                          text="Aguardando chamada...", 
                                          font=("Montserrat", 36),
                                          bg=self.bg_color, 
                                          fg=self.highlight_color)
        self.label_chamada_atual.pack()

        # Lista de últimas chamadas
        self.frame_ultimas_chamadas = tk.Frame(self.frame_direito, bg=self.bg_color)
        self.frame_ultimas_chamadas.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame_ultimas_chamadas, 
                text="Últimas Chamadas:", 
                font=("Montserrat", 28), 
                bg=self.bg_color, 
                fg=self.text_color).pack(pady=20)

        self.lista_ultimas_chamadas = tk.Listbox(self.frame_ultimas_chamadas, 
                                                font=("Montserrat", 24),
                                                bg=self.bg_color, 
                                                fg=self.text_color,
                                                selectmode=tk.NONE,
                                                width=50, height=10)
        self.lista_ultimas_chamadas.pack(pady=20)

    def cadastrar_procedimento(self):
        proc = self.entry_proc.get().strip()
        sala = self.entry_sala.get().strip()
        
        if proc and sala:
            item = f"{proc} - Sala {sala}"
            if item not in self.procedimentos:
                self.procedimentos[item] = []
                self.lista_proc.insert(tk.END, item)
                self.atualizar_combo_procedimentos()
                self.criar_lista_procedimento(item)
            
            self.entry_proc.delete(0, tk.END)
            self.entry_sala.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def criar_lista_procedimento(self, procedimento):
        # Cria um frame para o procedimento
        frame = tk.LabelFrame(self.frame_listas, text=procedimento, 
                            font=("Helvetica", 10, "bold"))
        frame.pack(fill=tk.X, pady=5)

        # Lista de pacientes para este procedimento
        lista = tk.Listbox(frame, width=50, height=5, font=("Helvetica", 10))
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Botão de chamada para este procedimento
        btn = tk.Button(frame, text="Chamar Próximo",
                       command=lambda: self.chamar_proximo(procedimento),
                       font=("Helvetica", 10, "bold"),
                       bg="#4CAF50", fg="white")
        btn.pack(side=tk.LEFT, padx=5)

        # Armazena as referências
        self.procedimentos[procedimento] = {"lista": lista, "frame": frame}

    def atualizar_combo_procedimentos(self):
        self.combo_proc['values'] = list(self.procedimentos.keys())

    def cadastrar_paciente(self):
        nome = self.entry_nome.get().strip()
        proc = self.combo_proc.get()
        
        if nome and proc and proc in self.procedimentos:
            horario = datetime.now().strftime("%H:%M")
            paciente = f"{horario} - {nome}"
            self.procedimentos[proc]["lista"].insert(tk.END, paciente)
            self.entry_nome.delete(0, tk.END)
            self.combo_proc.set('')
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos corretamente!")

    def tocar_som_chamada(self):
        pygame.mixer.music.load("sound.mp3")  # Você precisa ter este arquivo
        pygame.mixer.music.play()
        self.root.after(1000, self.falar_chamada)  # Espera 1 segundo antes de falar

    def falar_chamada(self):
        if not hasattr(self, 'ultimo_paciente_chamado'):
            return

        # Extrai as informações do paciente
        horario, nome = self.ultimo_paciente_chamado.split(" - ")
        proc_info = self.ultimo_procedimento.split(" - ")
        procedimento = proc_info[0]
        sala = proc_info[1]

        # Cria o texto para ser falado
        texto = f"{nome} compareça ao {procedimento} na {sala}"
        
        # Converte texto para fala
        tts = gTTS(text=texto, lang='pt-br')
        
        # Salva temporariamente e reproduz
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            pygame.mixer.music.load(fp.name)
            pygame.mixer.music.play()
            # Remove o arquivo após alguns segundos
            self.root.after(5000, lambda: os.remove(fp.name))

    def chamar_proximo(self, procedimento):
        lista = self.procedimentos[procedimento]["lista"]
        if lista.size() > 0:
            paciente = lista.get(0)
            lista.delete(0)
            
            # Atualiza a chamada atual
            chamada = f"{paciente} - {procedimento}"
            self.label_chamada_atual.config(text=chamada)
            
            # Guarda informações para o texto-para-fala
            self.ultimo_paciente_chamado = paciente
            self.ultimo_procedimento = procedimento
            
            # Adiciona às últimas chamadas
            self.pacientes_chamados.insert(0, chamada)
            self.lista_ultimas_chamadas.delete(0, tk.END)
            for p in self.pacientes_chamados[:10]:  # Mantém apenas as últimas 10 chamadas
                self.lista_ultimas_chamadas.insert(tk.END, p)

            # Toca o som e faz a chamada
            self.tocar_som_chamada()
        else:
            messagebox.showinfo("Aviso", f"Não há pacientes aguardando para {procedimento}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaChamadas(root)
    root.mainloop()