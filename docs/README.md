# RA1-12
Repositório para o primeiro TDE da matéria Linguagens Formais e Compiladores

Pontifícia Universidade Católica do Paraná (PUCPR)
Disciplina: Linguagens Formais e Compiladores
Professor: Frank de Alcantara
Semestre: 2026-1

## Integrantes

Mariana Alves da Silva (@himarialves)
Dani Heart Basso (@dani-heart)

Grupo no Canvas: RA1-12

## Sobre o Projeto

Este projeto implementa a Fase 1 de um compilador para uma linguagem de expressões aritméticas em notação polonesa reversa (RPN). O programa lê um arquivo de texto com expressões RPN, faz a análise léxica usando um Autômato Finito Determinístico e gera código Assembly compatível com o simulador Cpulator ARMv7 DEC1-SOC(v16.1).

## Como Executar

Pré-requisitos: Python 3.x instalado. Nenhuma biblioteca externa necessária.

Executar no terminal: python main.py 'arquivo_de_teste'.txt

Exemplo:
python main.py testes1.txt

O programa vai ler e tokenizar as expressões do arquivo, gerar o código Assembly ARMv7, salvar o Assembly em saida.asm, salvar os tokens em tokens.txt e exibir o Assembly gerado no terminal.

## Como Testar o Analisador Léxico

Executar no terminal: python parseExpressao.py

Roda a bateria de 10 testes do AFD cobrindo entradas válidas e inválidas.

## Como Testar o Assembly no Cpulator

1. Execute o programa com um arquivo de teste
2. Copie o conteúdo do saida.asm gerado
3. Acesse https://cpulator.01xz.net/
4. Selecione o modelo ARMv7 DEC1-SOC(v16.1)
5. Cole o Assembly no editor
6. Clique em Compile and Load
7. Clique em Continue para executar
8. O resultado estará no registrador d2

## Operadores Suportados nos arquivos de teste:

+, -, *, / (divisão real), // (divisão inteira), % (resto), ^ (potenciação)

Comandos especiais: (N RES) para resultado N linhas atrás, (V MEM) para armazenar valor, (MEM) para ler valor armazenado.
