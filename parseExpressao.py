DIGITOS = "0123456789"
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
OPERADORES = "+-*/%^"
ESPACOS = " \t\n\r"
PARENTESIS = "()"

def estado_erro(char, acumulador, tem_ponto):
    # O estado de erro é um "buraco negro". Ele apenas se retorna
    # sinalizando que a máquina travou.
    return (estado_erro, None, False, acumulador, tem_ponto)


def estado_inicial(char, acumulador, tem_ponto):
    # A lógica dessa função é simples: Ela verifica a existência do caractere atual baseado nos dicionários acima
    # Isso funciona como um identificador de qual tipo de token está sendo processado, necessário para a lógica dos 
    #próximos estados
    if char in ESPACOS: #Além do "espaço" inclui \t para tab, \n para linebreak, e \r para carriage return
        # Todos são considerados espaços. 
        return (estado_inicial, None, True, "", False)#Retorna "none" para o token na lógica.
        
    elif char in DIGITOS: #Digitos são simples. O acumulador recebe o caractere e o estado muda para "estado_numero"
        return (estado_numero, None, True, char, False)
        
    elif char in LETRAS: #Letras também são simples, mas com a diferenca de retornar para o estado "estado_palavra"
        return (estado_palavra, None, True, char, False)
        
    elif char in OPERADORES: #Mesma coisa com operadores
        return (estado_operador, None, True, char, False)

    elif char in PARENTESIS:# Parentesis são separadores de tokens e tem o problema de balanceamento. 
        #Retornam ao estado inicial para não acumular o caractere, mas geram um token do tipo "parentese" para a lista de tokens.
        return (estado_inicial, char, True, "", False)

    else: #Se não for nada dos de cima o usuário fez input errado
        return (estado_erro, None, False, "", False)

def estado_numero(char, acumulador, tem_ponto):
    # Se for um dígito joga para o acumulador e continua no estado de número
    if char in DIGITOS:
        # Retorna: Mesmo estado, Sem token novo, Avança índice, Acumulador + char (fazendo append), Mantém a flag de ponto
        return (estado_numero, None, True, acumulador + char, tem_ponto)

    # Se tiver ponto decimal precisa verificar se já não tinha um ponto antes (através da flag)
    elif char == '.':
        if tem_ponto == False:
           
            # Retorna: Mesmo estado, Sem token novo, Avança índice, Acumulador + char (fazendo append), mas _altera_ a flag de ponto
            return (estado_numero, None, True, acumulador + char, True)
        else:
            #Se já tinha um ponto e achamos outro ponto é um número malformado. Erro, indica o erro e fim da história
            print("ERRO LÉXICO: Número malformado (múltiplos pontos decimais).")
            return (estado_erro, None, False, acumulador, tem_ponto)

    #A partir daqui é casos de saída

    #Um número pode acabar quando encontramos espaço ou parentesis    
    elif char in ESPACOS or char in PARENTESIS:
        # Retorna: Volta pro inicial, Token é o número acumulado, NÃO AVANÇA (devolve o char para ser processado em outro momento)
        # Zera acumulador, Zera ponto
        return (estado_inicial, acumulador, False, "", False)

    # Se for um operador matemático, o número também acabou validamente. 
    #Nota que não verificamos se o operador realmente faz sentido aqui, só que ele existe
    elif char in OPERADORES:
        # Mesma lógica: devolve o operador para ser lido no próximo turno
        return (estado_inicial, acumulador, False, "", False)

    #Apesar de letras serem válidas, elas devem ser separadas por espaço ou operador. Então qualquer outro caso é erro
    else:
        print(f"ERRO LÉXICO: Caractere inválido, verifique a ortografia: '{char}'")
        return (estado_erro, None, False, acumulador, tem_ponto)


#Muito parecido com número. Tem algumas peculiaridades:
# 1) Variáveis não podem conter números, então se encontrar um dígito é erro
# 2) Variáveis são formadas por letras coladas, então se encontrar um espaço ou parentesis a palavra acabou
# 3) Operadores também são considerados como "finalizadores" de palavras, então se encontrar um operador a palavra também acabou.
def estado_palavra(char, acumulador, tem_ponto):
    # Se for letra, continua acumulando para formar a palavra
    if char in LETRAS:
        # Retorna: Mesmo estado, Sem token novo, Avança índice, Acumulador + char, flag de ponto (irrelevante aqui, fica False)
        return (estado_palavra, None, True, acumulador + char, False)

    # Se encontrar espaço ou parêntese, a palavra acabou validamente
    elif char in ESPACOS or char in PARENTESIS:
        # Retorna: Volta pro inicial, Token é a palavra acumulada, NÃO AVANÇA (devolve o char), Zera acumulador
        return (estado_inicial, acumulador, False, "", False)

    # Se encontrar um operador, a palavra também acabou (ex: na expressão "(VAR+19)" o token "VAR" termina no "+")
    elif char in OPERADORES: #Mesma coisa com operadores
        # A MÁGICA AQUI: Retorna False para NÃO avançar o índice, e passa o acumulador vazio "".
        # Assim, o estado_operador assume o controle olhando para o operador do zero!
        return (estado_operador, None, False, "", False)

    # Se tiver dígito colado em palavra, é erro. Variáveis e expressões não podem conter números.
    elif char in DIGITOS:
        print(f"ERRO LÉXICO: Comandos e variáveis não podem conter números (encontrado '{char}').")
        return (estado_erro, None, False, acumulador, False)

    # Qualquer outra coisa é erro
    else:
        print(f"ERRO LÉXICO: Caractere inválido grudado na palavra: '{char}'")
        return (estado_erro, None, False, acumulador, False)
    

# O estado operador lida com a ambiguidade entre divisão real (/) e divisão inteira (//). É o único caso que requer
# uma análise mais detalhada
# O estado operador lida com a ambiguidade entre divisão real (/) e divisão inteira (//).
def estado_operador(char, acumulador, tem_ponto):
    
    # CASO 1: O operador de 1 caractere (+, -, *, %, ^) já veio do estado inicial
    if acumulador in "+-*%^":
        # O token já está pronto.
        # Retorna: Volta pro inicial, Token é o acumulador, NÃO AVANÇA (devolve o char para não pular ele), zera acumulador
        return (estado_inicial, acumulador, False, "", False)

    # CASO 2: O acumulador tem uma barra "/", estamos analisando o caractere seguinte em suspense
    elif acumulador == "/":
        if char == '/':
            # Achou a segunda barra! É uma divisão inteira "//"
            # Retorna: Volta pro inicial, Token é "//", AVANÇA (consome a segunda barra), zera acumulador
            return (estado_inicial, "//", True, "", False)
        else:
            # O caractere seguinte NÃO é uma barra. A primeira barra era só uma divisão real "/".
            # Retorna: Volta pro inicial, Token é "/", NÃO AVANÇA (devolve o caractere para o inicial lidar com ele), zera acumulador
            return (estado_inicial, "/", False, "", False)
            
    # Segurança de sistema
    else:
        return (estado_erro, None, False, acumulador, False)

#Tarefa Aluno1:

def parseExpressao(linha: str, tokens: list):
    estado_atual = estado_inicial  # O estado atual tem que ser o inicial
    i = 0                          # Indice de percorrer linha
    acumulador = ""                # Caracteres do token atual
    tem_ponto = False              # Controle de erro de numeros
    saldo_parenteses = 0           # Controle de balanceamento
    
    leu_novo_char = True           # Flag para evitar contar o mesmo parêntese duas vezes

    while i < len(linha):  # Percorre a linha caractere por caractere
        char = linha[i]    # Pega o caractere atual para processar

        # Bloco controle para parentesis, já que eles são chatos por não serem acumulados 
        if leu_novo_char:
            if char == '(':
                saldo_parenteses += 1
            elif char == ')':
                saldo_parenteses -= 1
            
            if saldo_parenteses < 0:
                print("ERRO LÉXICO: Parênteses desbalanceados (fechamento extra).")
                return

                 # Fazer isso no início da análise já remove a carga de verificação do resto do código

 

        #O estado atual é uma função que recebe o caractere atual, o acumulador, e o controle de ponto

        resultado = estado_atual(char, acumulador, tem_ponto)
        proximo_estado = resultado[0] #O próximo estado é o primeiro elemento do resultado da função de estado
        token_gerado = resultado[1] #O token é o segundo elemento da função de estado
        avancar_indice = resultado[2] #O terceiro elemento é booleano, indica se o índice deve ir para o próximo caractere
        #ou se deve permanecer no atual. Isso é para lidar com operações, que serão lidas como "final" de um token, mas
        #devem ser processadas como o início de um token seguinte
        acumulador = resultado[3] #Joga o caractere atual para o acumulador. Caractere pode ser numero, letra ou operador
        tem_ponto = resultado[4]# Booleano que indica a existência de um ponto, para evitar casos como 3.1415.9 

        if token_gerado is not None: 
            # Se a função gerou um token, adiciona à lista de tokens
            tokens.append(token_gerado)
            
        if proximo_estado == estado_erro: 
            # Validação de erro. Simplesmente imprime a mensagem e interrompe
            print(f"ERRO LÉXICO: Caractere inválido ou malformado perto de '{char}'")
            return 

        # Atualiza a máquina para a próxima rodada
        estado_atual = proximo_estado
        # E se a máquina leu um char (Ao invés de um parentesis) vai avançar o índice
        leu_novo_char = avancar_indice
        
        # Só avança para a próxima letra se o estado permitir
        if avancar_indice:
            i += 1

    # Imprime o erro caso os parênteses estejam desbalanceados no final
    if saldo_parenteses > 0:
        print("ERRO LÉXICO: Parênteses desbalanceados (abertura sem fechamento).")
        return
    
    # Verifica se sobrou algum token acumulado no final da linha e o adiciona
    if acumulador != "":
        tokens.append(acumulador)

def testar_lexer():
    print("Iniciando bateria de testes do Analisador Léxico...\n")
    
    # Lista de expressões para testar (misturando casos de sucesso e de falha)
    testes = [
        "(3.14 2.0 +)",                # Válido: Operação simples
        "(5 RES)",                     # Válido: Teste de variável
        "((A B +) (C D *) /)",         # Válido: Expressões aninhadas, teste de parênteses e operadores
        "(10 3 //)",                   # Válido: Divisão inteira para testar o estado_operador
        "(3.14.5 2.0 +)",              # Inválido: Número malformado - múltiplos pontos
        "(3.14 2.0 &)",                # Inválido: Caractere inválido 
        "(3 4 +",                      # Inválido: Parênteses desbalanceados (falta fechar) esse teste demorou pra dar certo
        "(VAR1 5 +)",                  # Inválido: Número grudado em variável
        "(0.20 2 *)))))",              # Inválido: Parênteses desbalanceados (falta abrir)
        "Teste 1 2 Como + + + +"       # Válido: Teste de letra minúscula e sem parentesis
    ]

    #Faz todos os testes. Saudades do Rust que tem macro de teste =(
    for i, expressao in enumerate(testes):
        print(f"--- Teste {i+1} ---")
        print(f"Expressão Original: {expressao}")
        
        tokens_gerados = []
        parseExpressao(expressao, tokens_gerados)
        
        # Só imprime a lista de tokens se o Lexer não travou por erro e gerou algo
        if tokens_gerados:
            print(f"Tokens Reconhecidos: {tokens_gerados}")
        print("-" * 30 + "\n")

# Esse if garante que os testes só rodem se você executar este arquivo diretamente
if __name__ == "__main__":
    testar_lexer()