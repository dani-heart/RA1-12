#executarExpressao
#hora que o filho chora e a mãe vê: recebe tokens, memoria, historico, retorna float
#entrada: ["(", "3.14", "2.0", "+", ")"] ; saída: 5.14 (float)
#a ideia aqui é uma PILHA -> append e pop
### APPEND primeiro token na pilha
### APPEND segundo token na pilha
### SOBRA o operador -> POP p tirar tokens da pilha
### SOMA os tokens (relativo operador) -> APPEND no resultado na pilha (e retorna)
## se tem MEM? chora? também!
##  ["(", "MEM", ")"] vai ler MEM e APPEND na pilha, 0.0 se nada.
##  ["(", "3.14", "MEM", ")"] -> pop 3.14 da pilha, guardar na memória MEM, APPEND 3.14 da pilha
## RES N vc decide as linhas que tu quer buscar o resultado das ultimas operacoes
## tratar erro de N maior que num de resultados anteriores
## ["(", "2", "RES", ")"] -> APPEND -> verificar se N é numero e APPEND na pilha
## RES, POP o 2, busca historica -2, APPEND resultado encontrado.
## agora se prepare para o meu surto de 4 da manhã de um sabado
def executarExpressao(tokens, memoria, historico):
    pilha = []
    OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}
    
    # Apenas adicionei o enumerate aqui para conseguirmos espiar o token anterior no MEM
    for i, token in enumerate(tokens):
        if is_num(token):
            pilha.append(float(token))
        elif token in "()":
            pass
        elif token in OPERADORES:
            b = pilha.pop()  # topo, segundo operando
            a = pilha.pop()  # embaixo, primeiro operando
            if token == "+":
                pilha.append(a + b)
            elif token == "-":
                pilha.append(a - b)
            elif token == "*":
                pilha.append(a * b)
            elif token == "/":
                if b == 0:
                    print("ERRO: divisão por zero")
                    return 0.0
                pilha.append(a / b)
            elif token == "//":
                if b == 0:
                    print("ERRO: divisão por zero")
                    return 0.0
                pilha.append(float(int(a) // int(b)))
            elif token == "%":
                if b == 0:
                    print("ERRO: divisão por zero")
                    return 0.0
                pilha.append(float(int(a) % int(b)))
            elif token == "^":
                pilha.append(a ** int(b))
        elif token == "RES":
            n = int(pilha.pop())
            if n <= 0 or n > len(historico):
                print(f"ERRO: não existe resultado {n} linhas atrás")
                pilha.append(0.0)
            else:
                pilha.append(historico[-n])
        else:  # esse é pra MEM
            # token é um nome de variável ("X", "BANANAS", "MACAS", etc.)
            token_anterior = tokens[i - 1] if i > 0 else ""
            
            if token_anterior != "(": 
                # tem coisa na pilha da APPEND (mudança: verifica se não era parêntese antes)
                if len(pilha) > 0:
                    valor = pilha.pop()
                    memoria[token] = valor   # cria ou sobrescreve, não importa!!
                    pilha.append(valor)      # APPEND o valor na pilha (resultado da linha)
                else:
                    pilha.append(0.0)
            else:
                # pilha vazia → BUSCAR (mudança: se tinha parêntese antes, é leitura)
                pilha.append(memoria.get(token, 0.0))  # 0.0 se nunca foi salvo

    # Adicionei uma verificação de segurança aqui caso a pilha termine vazia
    return pilha[0] if len(pilha) > 0 else 0.0


def is_num(token: str) -> bool:  # verifica se é um num real (int ou float)
    try:
        float(token)  # ex: 3, 3.14, -7, 1e10,
        return True
    except ValueError:
        return False  # ex: abc, 3.14.5, 3,14, +, " ", space, RES, 3 14,


# ==========================================
# TESTES (Rode no terminal com: python seu_arquivo.py)
# ==========================================
if __name__ == "__main__":
    print("Iniciando testes da Pilha de Execução RPN...\n")
    
    memoria_teste = {}
    historico_teste = [10.0, 25.5] 

    tokens1 = ['(', '3.14', '2.0', '+', ')']
    print(f"Teste 1 (3.14 + 2.0): {executarExpressao(tokens1, memoria_teste, historico_teste)}")

    tokens2 = ['(', '(', '10', '2', '*', ')', '4', '/', ')']
    print(f"Teste 2 ((10 * 2) / 4): {executarExpressao(tokens2, memoria_teste, historico_teste)}")

    tokens3 = ['(', '5.0', 'BANANAS', ')']
    print(f"Teste 3 (Gravar 5.0 em BANANAS): Pilha={executarExpressao(tokens3, memoria_teste, historico_teste)}, Memoria={memoria_teste}")

    tokens4 = ['(', '(', 'BANANAS', ')', '10.0', '+', ')']
    print(f"Teste 4 (BANANAS + 10.0): {executarExpressao(tokens4, memoria_teste, historico_teste)}")