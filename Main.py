import sys
from parseExpressao import parseExpressao
from geradorAssembly import gerarAssembly, lerArquivo
from exibirResultados import exibirResultados

def main():
    if len(sys.argv) < 2:
        print("ERRO: informe o arquivo de entrada.")
        print("Uso: python main.py arquivo.txt")
        return

    nome_arquivo = sys.argv[1]

    # Passo 1 — lê o arquivo
    linhas = []
    lerArquivo(nome_arquivo, linhas)
    if not linhas:
        return

    # Passo 2 — tokeniza e gera Assembly linha por linha
    todos_tokens = []
    assembly_final = ""

    for linha in linhas:
        tokens = []
        parseExpressao(linha, tokens)
        if tokens:
            todos_tokens.append(tokens)
            assembly_final = gerarAssembly(tokens)  # sobrescreve = fica só a última

    # Passo 3 — salva o Assembly da última execução
    with open("saida.asm", "w") as f:
        f.write(assembly_final)
    print("Assembly gerado em saida.asm")

    # Passo 4 — salva os tokens da última execução
    with open("tokens.txt", "w") as f:
        for tokens in todos_tokens:
            f.write(str(tokens) + "\n")
    print("Tokens salvos em tokens.txt")

    # Passo 5 — exibe o Assembly gerado
    exibirResultados([assembly_final])

if __name__ == "__main__":
    main()