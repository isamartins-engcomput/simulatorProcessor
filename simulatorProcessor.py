import tkinter as tk
from tkinter import filedialog, messagebox

class Processador:
    def __init__(self):
        # Inicializa o simulador
        self.memoria = ["0"] * 32 # Memória RAM com 32 posições
        self.regs = [0, 0, 0, 0] # Banco de registradores (R0 a R3)
        self.pc = 0 # Program Counter (PC)
        self.ir = "" # Instruction Register (IR)
        
        # Flags da ALU (Desvios condicionais)
        self.flag_zero = False
        self.flag_negativo = False        
        self.executando = True

    def carregar_programa_lista(self, linhas):
        # Limpa o estado da máquina simulando uma reinicialização total
        self.memoria = ["0"] * 32
        self.pc = 0
        self.ir = ""
        self.regs = [0, 0, 0, 0]
        self.flag_zero = False
        self.flag_negativo = False
        self.executando = True
        
        # Transfere as instruções para a memória, ignorando linhas vazias
        idx_memoria = 0
        for linha in linhas:
            conteudo = linha.strip()
            if conteudo and idx_memoria < 32: # Máximo de 32 linhas, conforme especificação
                self.memoria[idx_memoria] = conteudo
                idx_memoria += 1

    def atualizar_flags(self, resultado):
        """Atualiza as flags da ALU pós operações aritméticas/lógicas."""
        # Sempre que a ALU fizer uma conta, ela vai informar o resto do processador sobre o estado do resultado
        self.flag_zero = (resultado == 0) # Zero
        self.flag_negativo = (resultado < 0) # Número negativo

    def extrair_reg(self, reg_str):
        """Converte a string 'R0', 'R1', etc. para o índice inteiro 0, 1..."""
        return int(reg_str.replace('R', ''))

    def passo(self):
        """Ciclo Principal adaptado para interface: Busca, Decodificação e Execução de apenas 1 instrução."""
        # Se a máquina não estiver ligada (executando) ou ultrapassar o limite da RAM, para a execução visual
        if not self.executando or self.pc >= 32:
            return False
            
        # 1. BUSCA
        # PC aponta para o endereço da RAM
        # O dado é copiado para IR
        self.ir = self.memoria[self.pc]
        
        # Proteção contra "Falha de Segmentação" ou acesso a uma memória não inicializada
        # Se tentar ler um espaço vazio, interrompe o ciclo do processador
        if not self.ir or self.ir == "0":
            self.executando = False
            return False
            
        # O PC é incrementado após a Busca
        # Durante a fase de 'Execução', o PC já estará apontando para a próxima instrução
        self.pc += 1 
        
        # 2. DECODIFICAÇÃO
        # A UC analisa a instrução separando seus elementos
        partes = self.ir.split()
        if not partes: return False
        
        cmd = partes[0] # Extrai o Código de Operação (ex: "LOAD", "ADD", "BZERO")
        
        # 3. EXECUÇÃO
        try:
            if cmd == "HALT":
                # Encerra o laço de funcionamento do processador
                self.executando = False
                
            elif cmd == "NOP":
                # Nenhuma Operação: Gasta um ciclo de relógio sem alterar nenhum estado interno
                pass 
                
            elif cmd == "LOAD":
                # Acesso à Memória: Busca o dado na RAM e grava em um Registrador local na CPU
                reg = self.extrair_reg(partes[1]) # Destino
                end_mem = int(partes[2]) # Endereço Fonte
                self.regs[reg] = int(self.memoria[end_mem])
                
            elif cmd == "STORE":
                # Acesso à Memória: Pega o dado de um Registrador e grava de volta na RAM externa
                end_mem = int(partes[1]) # Endereço Destino
                reg = self.extrair_reg(partes[2]) # Fonte
                self.memoria[end_mem] = str(self.regs[reg])
                
            elif cmd == "MOVE":
                # Transferência de Registrador: Cópia direto na CPU, sem mexer na RAM
                reg_dest = self.extrair_reg(partes[1])
                reg_src = self.extrair_reg(partes[2])
                self.regs[reg_dest] = self.regs[reg_src]
                
            elif cmd == "ADD":
                # ALU executa a soma e atualiza as flags
                reg_dest = self.extrair_reg(partes[1])
                r_src1 = self.regs[self.extrair_reg(partes[2])]
                r_src2 = self.regs[self.extrair_reg(partes[3])]
                resultado = r_src1 + r_src2
                self.regs[reg_dest] = resultado
                self.atualizar_flags(resultado)
                
            elif cmd == "SUB":
                # ALU executa a subtração e atualiza as flags
                reg_dest = self.extrair_reg(partes[1])
                r_src1 = self.regs[self.extrair_reg(partes[2])]
                r_src2 = self.regs[self.extrair_reg(partes[3])]
                resultado = r_src1 - r_src2
                self.regs[reg_dest] = resultado
                self.atualizar_flags(resultado)
                
            elif cmd == "AND":
                # ALU Bit a Bit: Operação Lógica 'E'
                reg_dest = self.extrair_reg(partes[1])
                r_src1 = self.regs[self.extrair_reg(partes[2])]
                r_src2 = self.regs[self.extrair_reg(partes[3])]
                resultado = r_src1 & r_src2
                self.regs[reg_dest] = resultado
                self.atualizar_flags(resultado)
                
            elif cmd == "OR":
                # ALU Bit a Bit: Operação Lógica 'OU'
                reg_dest = self.extrair_reg(partes[1])
                r_src1 = self.regs[self.extrair_reg(partes[2])]
                r_src2 = self.regs[self.extrair_reg(partes[3])]
                resultado = r_src1 | r_src2
                self.regs[reg_dest] = resultado
                self.atualizar_flags(resultado)
                
            elif cmd == "BRANCH":
                # Salto Incondicional: Sobrescreve o PC forçando o código a desviar
                self.pc = int(partes[1])
                
            elif cmd == "BZERO":
                # Salto Condicional: Avalia a flag de zero da ALU antes de decidir se vai pular ou não
                if self.flag_zero:
                    self.pc = int(partes[1])
                    
            elif cmd == "BNEG":
                # Salto Condicional: Avalia a flag de negativo da ALU antes de pular
                if self.flag_negativo:
                    self.pc = int(partes[1])
                    
        except Exception as e:
            # Simula uma falha no hardware
            print(f"Erro ao executar a instrução '{self.ir}' na linha {self.pc-1}: {e}")
            self.executando = False
            raise e
            
        return True

    def gerar_arquivos_saida(self):
        """Gera os três arquivos de saída com o estado final da execução."""
        
        # 1. Unidade de Controle
        with open("unidade_controle.txt", "w") as f:
            f.write(f"PC: {self.pc}\n")
            f.write(f"IR: {self.ir}\n")
            
        # 2. Banco de Registradores
        with open("banco_registradores.txt", "w") as f:
            for i, reg in enumerate(self.regs):
                f.write(f"R{i}: {reg}\n")
                
        # 3. Memória RAM
        with open("memoria_ram.txt", "w") as f:
            for i, item in enumerate(self.memoria):
                f.write(f"M[{i}]: {item}\n")

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Processador - ARQ. COMP.")
        self.root.geometry("1100x680")
        
        # Paleta de Cores Estilo Terminal Retro
        self.black = "#000000"
        self.green = "#00FF00"
        self.yellow = "#FFFF00"
        
        # Fonte monoespaçada
        self.font_title = ("Consolas", 12, "bold")
        self.font_text = ("Consolas", 12)
        
        self.root.config(bg=self.black)
        
        self.processador = Processador()
        self.criar_widgets()
        self.atualizar_tela()

    def criar_widgets(self):
        # Painel Superior (Controles de Execução)
        frame_controles = tk.Frame(self.root, bg=self.black, pady=15)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        # Estilo base para botões da interface
        btn_style = {
            "font": self.font_title, 
            "bg": self.black, 
            "fg": self.green, 
            "activebackground": self.green, 
            "activeforeground": self.black,
            "highlightbackground": self.green,
            "highlightthickness": 1,
            "relief": tk.RIDGE,
            "padx": 10, "pady": 5
        }
        
        tk.Button(frame_controles, text="[ IMPORTAR ENTRADA.TXT ]", command=self.importar_arquivo, **btn_style).pack(side=tk.LEFT, padx=15)
        tk.Button(frame_controles, text="> EXECUTAR PASSO", command=self.executar_passo, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controles, text=">> RODAR TUDO", command=self.executar_tudo, **btn_style).pack(side=tk.LEFT, padx=5)
        
        btn_reset = btn_style.copy()
        btn_reset["fg"] = self.yellow
        btn_reset["activebackground"] = self.yellow
        tk.Button(frame_controles, text="[ REINICIAR ]", command=self.resetar, **btn_reset).pack(side=tk.RIGHT, padx=15)

        # Container Principal com 3 colunas
        frame_main = tk.Frame(self.root, bg=self.black)
        frame_main.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # 1. EDITOR DE CÓDIGO
        frame_editor = tk.LabelFrame(frame_main, text=" EDITOR DE INSTRUÇÕES (ENTRADA.TXT)", font=self.font_title, bg=self.black, fg=self.green, bd=2, relief=tk.RIDGE)
        frame_editor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        # Caixa de texto livre para escrever o Assembly antes de compilar para a RAM.
        self.text_editor = tk.Text(frame_editor, width=25, font=self.font_text, bg=self.black, fg=self.yellow, insertbackground=self.yellow, relief=tk.FLAT, padx=5, pady=5)
        self.text_editor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        tk.Button(frame_editor, text="v SINCRONIZAR COM A RAM v", command=self.carregar_do_editor, **btn_style).pack(fill=tk.X, padx=10, pady=(0, 10))

        # 2. MEMÓRIA RAM
        frame_memoria = tk.LabelFrame(frame_main, text=" MEMÓRIA RAM (32 pos) ", font=self.font_title, bg=self.black, fg=self.green, bd=2, relief=tk.RIDGE)
        frame_memoria.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        scrollbar = tk.Scrollbar(frame_memoria, bg=self.black, troughcolor=self.black)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Representação visual das gavetas de memória do hardware.
        self.lista_memoria = tk.Listbox(frame_memoria, width=22, font=self.font_text, bg=self.black, fg=self.green, selectbackground=self.yellow, selectforeground=self.black, yscrollcommand=scrollbar.set, relief=tk.FLAT)
        self.lista_memoria.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        scrollbar.config(command=self.lista_memoria.yview)

        # 3. CPU E REGISTRADORES
        frame_cpu = tk.Frame(frame_main, bg=self.black)
        frame_cpu.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

        # Visualização da UC
        frame_uc = tk.LabelFrame(frame_cpu, text=" UNIDADE DE CONTROLE ", font=self.font_title, bg=self.black, fg=self.green, bd=2, relief=tk.RIDGE)
        frame_uc.pack(fill=tk.X, pady=5)
        
        self.lbl_pc = tk.Label(frame_uc, text="PC: 0", font=("Consolas", 14, "bold"), bg=self.black, fg=self.yellow)
        self.lbl_pc.pack(anchor="w", padx=15, pady=5)
        self.lbl_ir = tk.Label(frame_uc, text="IR: -", font=("Consolas", 14, "bold"), bg=self.black, fg=self.yellow)
        self.lbl_ir.pack(anchor="w", padx=15, pady=5)

        # Visualização do Banco de Registradores
        frame_regs = tk.LabelFrame(frame_cpu, text=" BANCO DE REGISTRADORES", font=self.font_title, bg=self.black, fg=self.green, bd=2, relief=tk.RIDGE)
        frame_regs.pack(fill=tk.X, pady=10)
        
        self.lbl_regs = []
        for i in range(4):
            lbl = tk.Label(frame_regs, text=f"R{i}: 0", font=self.font_text, bg=self.black, fg=self.green)
            lbl.pack(anchor="w", padx=15, pady=2)
            self.lbl_regs.append(lbl)

        # Visualização da ULA e suas flags
        frame_alu = tk.LabelFrame(frame_cpu, text=" ALU (Operações / Flags)", font=self.font_title, bg=self.black, fg=self.green, bd=2, relief=tk.RIDGE)
        frame_alu.pack(fill=tk.X, pady=10)
        
        self.lbl_zero = tk.Label(frame_alu, text="FLAG ZERO: False", font=self.font_title, bg=self.black, fg=self.green)
        self.lbl_zero.pack(anchor="w", padx=15, pady=5)
        self.lbl_neg = tk.Label(frame_alu, text="FLAG NEG: False", font=self.font_title, bg=self.black, fg=self.green)
        self.lbl_neg.pack(anchor="w", padx=15, pady=5)

        # Botão de acesso a tabela de instruções
        tk.Button(
            frame_cpu, 
            text="[ TABELA DE INSTRUÇÕES ]", 
            command=self.mostrar_tabela, 
            font=self.font_title, 
            bg=self.black, 
            fg=self.yellow, 
            activebackground=self.yellow, 
            activeforeground=self.black, 
            relief=tk.RIDGE, 
            bd=2
        ).pack(pady=25)

    def importar_arquivo(self):
        # Abre o explorador de arquivos do SO para procurar a entrada
        caminho = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if caminho:
            nome_arquivo = caminho.split('/')[-1]

            if nome_arquivo != "entrada.txt":
                messagebox.showerror("ERRO!", "ACESSO NEGADO: O arquivo de instruções deve se chamar estritamente 'entrada.txt'.")
                return
                
            with open(caminho, 'r') as f:
                conteudo = f.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, conteudo)
            self.carregar_do_editor()
            messagebox.showinfo("Sucesso!", "Programa importado e sincronizado com a RAM!")

    def carregar_do_editor(self):
        texto_bruto = self.text_editor.get("1.0", tk.END)
        linhas = texto_bruto.split('\n')
        self.processador.carregar_programa_lista(linhas)
        self.atualizar_tela()

    def executar_passo(self):
        # Simula o processador em modo 'Debug'
        try:
            continuar = self.processador.passo()
            self.atualizar_tela()
            if not continuar:
                messagebox.showinfo("Fim!", "Execução finalizada ou instrução HALT encontrada.")
        except Exception as e:
            messagebox.showerror("Erro de Execução!", f"Falha na execução da instrução.\nIR: {self.processador.ir}\nErro: {str(e)}")

    def executar_tudo(self):
        # Executa o programa por completo
        while self.processador.executando and self.processador.pc < 32:
            try:
                self.processador.passo()
            except Exception as e:
                messagebox.showerror("Erro de Execução!", f"Falha na execução.\nErro: {str(e)}")
                break
        self.atualizar_tela()
        
        # Gera os arquivos .txt de saída
        self.processador.gerar_arquivos_saida()
        
        messagebox.showinfo("Fim!", "Execução finalizada. Arquivos de saída (.txt) gerados com sucesso no diretório atual!")

    def resetar(self):
        # Zera a instância da classe
        self.processador = Processador()
        self.text_editor.delete("1.0", tk.END)
        self.atualizar_tela()

    def atualizar_tela(self):
        self.lista_memoria.delete(0, tk.END)
        for i, item in enumerate(self.processador.memoria):
            marca = " > " if i == self.processador.pc else "   "
            texto = f"{marca} M[{i:02d}]: {item}"
            self.lista_memoria.insert(tk.END, texto)
            
            if i == self.processador.pc:
                # Linha de execução atual em amarelo
                self.lista_memoria.itemconfig(tk.END, {'bg': self.yellow, 'fg': self.black})
                self.lista_memoria.see(i)
            else:
                self.lista_memoria.itemconfig(tk.END, {'fg': self.green})

        self.lbl_pc.config(text=f"PC: {self.processador.pc}")
        self.lbl_ir.config(text=f"IR: {self.processador.ir if self.processador.ir else '-'}")

        for i in range(4):
            self.lbl_regs[i].config(text=f"R{i}: {self.processador.regs[i]}")

        # Se a flag for disparada pela ALU fica em amarelo
        self.lbl_zero.config(text=f"FLAG ZERO: {self.processador.flag_zero}", fg=self.yellow if self.processador.flag_zero else self.green)
        self.lbl_neg.config(text=f"FLAG NEG: {self.processador.flag_negativo}", fg=self.yellow if self.processador.flag_negativo else self.green)

    def mostrar_tabela(self):
        try:
            # Janela flutuante acima da principal
            janela_tabela = tk.Toplevel(self.root)
            janela_tabela.title("Tabela de Instruções")
            janela_tabela.config(bg=self.black)
            
            img_tabela = tk.PhotoImage(file="tabela.png").subsample(3, 3)
            
            lbl_img = tk.Label(janela_tabela, image=img_tabela, bg=self.black)
            
            lbl_img.image = img_tabela 
            lbl_img.pack(padx=10, pady=10)
            
        except Exception:
            messagebox.showerror(
                "ERRO!", 
                "IMAGEM NÃO ENCONTRADA!.\nSalve a imagem da sua tabela exatamente como 'tabela.png' na mesma pasta do simulador."
            )

# Execução do programa
if __name__ == "__main__":
    try:
        # Ponto de partida do Tkinter
        root = tk.Tk()
        app = Interface(root)
        root.mainloop()
    except Exception as e:
        print("Ambiente sem suporte a display de janela gráfica.")