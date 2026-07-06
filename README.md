# 🟢 Simulador de Processador - ARQ. COMP. 🟡

Esta aplicação implementa um simulador visual de processador baseado no modelo de Von Neumann (semelhante ao simulador K&S), capaz de executar um conjunto de instruções em Assembly e demonstrar na prática o ciclo de *Fetch*, *Decode* e *Execute*.

## 🛠️ Tecnologias Utilizadas

* **Python 3:** Lógica backend do hardware simulado, encapsulamento em Orientação a Objetos e manipulação de arquivos de entrada e saída.
* **Tkinter:** Interface gráfica nativa customizada construída como uma IDE com estética de terminal retrô.

## ⚙️ Funcionalidades

* **IDE Integrada e Sincronização:** Editor de texto próprio para escrita livre ou importação de código Assembly (validado estritamente para o arquivo `entrada.txt`), com injeção direta na memória RAM simulada.
* **Execução Visual (Step-by-Step):** Acompanhamento do *datapath* em tempo real. O usuário pode visualizar alterações simultâneas no *Program Counter* (PC), *Instruction Register* (IR), gavetas da Memória RAM e Banco de Registradores.
* **ALU e Desvios Condicionais:** Suporte a operações lógicas e aritméticas (ADD, SUB, AND, OR) conectadas a um sistema reativo de *Flags* (ZERO e NEG). Permite a execução complexa de rotinas com saltos condicionais (BZERO, BNEG) e incondicionais (BRANCH).
* **Geração de Core Dump (Snapshot):** Ao encontrar a instrução HALT, o sistema exporta automaticamente três arquivos físicos de saída (`unidade_controle.txt`, `banco_registradores.txt` e `memoria_ram.txt`), registrando o estado final do hardware para auditoria.

## 💻 Como executar no Linux

Certifique-se de ter o pacote do Tkinter instalado:

```bash
sudo apt update && sudo apt install python3-tk
```

Execute o arquivo principal:

```bash
python3 simulatorProcessor.py
```

## ✒️ Autoria

Projeto desenvolvido em dupla para a disciplina de Arquitetura de Computadores - 4º semestre 2026/1.

* **Isadora Martins**
* **Pedro Sperandio**

Estudantes de Engenharia de Computação do IFMS Campus Três Lagoas.
