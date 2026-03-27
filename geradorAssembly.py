
#Teste para ver se o token é número ou não. O retorno de "Falso" se dá quando o token é uma variável ou operador
# Exemplo: "3.14" → Verdadeiro, "BANANAS" → Falso, "+" → Falso, "2.0" → Verdadeiro, "VAR1" → Falso
def is_num(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


#Funão para ler o .txt e colocar as linhas em uma lista, ignorando linhas vazias
#Utiliza funções nativas de tratamento de arquivos. open() e strip() para limpar as linhas.
def lerArquivo(nomeArquivo: str, linhas: list):
    try:
        with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:  # Abre o arquivo para leitura
            for linha in arquivo: #Passa de linha a linha 
                linha_limpa = linha.strip() #strip() remove espaços em branco no inicio ou fim de linha. 
                if linha_limpa:
                    linhas.append(linha_limpa) #Joga os valores na lista de linhas, ignorando as linhas vazias
        print(f"SUCESSO: Arquivo '{nomeArquivo}' carregado. ({len(linhas)} expressões encontradas)\n")

    #Tratamento de erros, necessário pela ementa do trabalho. 
    except FileNotFoundError:
        #Caso o arquivo não exista. 
        print(f"ERRO CRÍTICO: O arquivo '{nomeArquivo}' não foi encontrado.")
        print("-> Verifique se o nome está correto e se ele está na mesma pasta do script.\n")
        #Caso o arquivo exista mas haja um erro inesperado ao ler, como problemas de permissão.
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha inesperada ao ler o arquivo '{nomeArquivo}'. Detalhes: {e}\n")

def gerarAssembly(tokens: list) -> str:
    #Listas de strings, que na verdade são as linhas do código assembly. 
    #.data é a seção de dados, onde ficam as declarações de variáveis e números.
    #codigo_text inclui o texto do código, .global main como declaração de entrada, main: como rótulo de início
    #push {lr} é o endereço de retorno para a main. 

    codigo_data = [".data"] 
    codigo_text = [".text", ".global main", ".thumb", ".thumb_func", "main:", "    push {lr, pc}"]

    #Representam as primeiras linhas de código assembly, e são fundamentais para todo tipo de programa em ARM

    tabela_nums = {}# Dicionário para mapear números a rótulos (ex: "3.14" → "num_0"). Preenchido dinamicamente
    contador_nums = 0 #Por que não estamos usando uma função para contar numeros? 


    for i, token in enumerate(tokens):
        if token in "()": #Parentesis não geram código, só organizam e gerenciam ordem de acontecimentos
            continue

        if is_num(token):
            if token not in tabela_nums:
                #Se o token for número e ainda não tiver rótulo cria um novo e aumenta o contador
                label = f"num_{contador_nums}"
                tabela_nums[token] = label
                contador_nums += 1
                #Joga ao fim da fila, com double porque é o formato que a VFP espera. Ex: "3.14" → "num_0: .double 3.14"
                codigo_data.append(f"{label}: .double {token}")
            
            #Operações de carregamento de número na pilha
            label_atual = tabela_nums[token]#VFP é cego para RAM, então utilizamos r0 para buscar a coordenada na RAM
            codigo_text.append(f"    ldr r0, ={label_atual}") #Formatação de código para carregar o número usando o rótulo criado
            #VFP upera com registradores de float, então precisamos carregar para um registrador e, em seguida, em d0 
            codigo_text.append(f"    vldr.f64 d0, [r0]") #Carrega o número do rótulo para o registrador de float d0
            codigo_text.append(f"    vpush {{d0}}") #E finalmente empilha o valor de d0 na pilha de execução

        elif token in ["+", "-", "*", "/"]: #Se for um operador precisa de condições especiais para cada operador
            codigo_text.append(f"    vpop {{d0, d1}}") 
            #Isso está tudo registrado na documentação da VFP, disponível em 
            #https://developer.arm.com/documentation/dui0472/m/arm-and-thumb-instructions/vpop--vpush--vstm--vldm-?lang=en

            #A estrutura arqui é a mesma para os 4 operadores, só muda a instrução de operação. 
            #A ordem fica: v{opp}.f64(float 64) -> d2 recebe o resultado entre d1 e d0
            if token == "+":
                
                codigo_text.append(f"    vadd.f64 d2, d1, d0")
            elif token == "-":
                codigo_text.append(f"    vsub.f64 d2, d1, d0")
            elif token == "*":
                codigo_text.append(f"    vmul.f64 d2, d1, d0")
            elif token == "/":
                codigo_text.append(f"    vdiv.f64 d2, d1, d0")
            #e depois d2 é empilhado.
            codigo_text.append(f"    vpush {{d2}}")


        #Essas foram as operações especiais que deram trabalho anteriormente. 
        elif token in ["//", "%", "^"]:
            

            #Realizamos essas operações usando inteiras nas 3 instruções, então é mais fácil fazer essas conversões antes das 
            #condicionais.
            codigo_text.append(f"    vpop {{d0, d1}}")
            codigo_text.append(f"    vcvt.s32.f64 s0, d0")
            codigo_text.append(f"    vcvt.s32.f64 s1, d1")
            codigo_text.append(f"    vmov r0, s0")
            codigo_text.append(f"    vmov r1, s1")
            
            #Essas operações são curiosas. O VFP não sabe fazer divisão inteira, só divisão de float. 
            #Então estamos puxando os valores de d0 e d1, convertendo para inteiro (vcvt é vconvert), aí movemos para r0 e r1
            #E depois disso fazemos a operação usando registradores inteiros
            
            if token == "//":
                #O resultado da divisão inteira é armazenado em r2, e depois convertido de volta para float e empilhado.
                codigo_text.append(f"    sdiv r2, r1, r0")
            elif token == "%":
                #mls -> Multiply and Subtract. r2 recebe r1 * r0, e depois r1 - r2 para obter o resto da divisão inteira.
                codigo_text.append(f"    sdiv r3, r1, r0")
                codigo_text.append(f"    mls r2, r3, r0, r1")

                #Assembly não tem operador de potencia, então estamos usando "pow" da biblioteca matemática do ARM
                
            elif token == "^":
                codigo_text.append(f"    bl pow")
                codigo_text.append(f"    mov r2, r0")
            
            #move o resultado para s2, converte de volta para float e empilha
            codigo_text.append(f"    vmov s2, r2")
            codigo_text.append(f"    vcvt.f64.s32 d2, s2")
            codigo_text.append(f"    vpush {{d2}}")

        #  RES e MEM são bem mais difíceis, porque tem que lidar com a memória.
        # RES é mais fácil, porque é só puxar o número de linhas para trás e pegar o resultado daquelas linhas.
        elif token == "RES":
            linha_hist = "historico: .space 800" #Pede 800 bytes de armazenamento para a RAM
            if linha_hist not in codigo_data: #E se não tiver a linha no código, adiciona
                codigo_data.append(linha_hist)
                
            
            codigo_text.append(f"    vpop {{d0}}") #Puxa o número de linhas para trás, que deve estar no topo da pilha. 
            codigo_text.append(f"    vcvt.s32.f64 s0, d0") #Converte para inteiro, porque o número de linhas é um inteiro
            codigo_text.append(f"    vmov r0, s0") #Move para r0 para usar como índice de acesso à memória
            
            #Carrega o endereço base em r1 e puxa o primeiro valor que estiver lá, que é o resultado da linha mais recente.
            codigo_text.append(f"    ldr r1, =historico")
            codigo_text.append(f"    vldr.f64 d0, [r1]")
            codigo_text.append(f"    vpush {{d0}}")

        else: #Se não for RES nem operador, nem número, nem parêntese, só pode ser MEM ou uma variável.
            linha_declaracao = f"var_{token}: .double 0.0" #Declara a variável como um double, inicializada com 0.0
            if linha_declaracao not in codigo_data:#Se não for declarada ainda, declara
                #Isso é necessário para evitar declarações duplicadas, já que uma variável pode ser usada várias vezes.
                codigo_data.append(linha_declaracao)
            
            #Necessário devido aos parentesis: Se o token anterior foi um parentesis significa que estamos lendo uma variavel (?)
            #E não tem nada na pilha para guardar, então só carregamos o valor da variável.
            token_anterior = tokens[i - 1] if i > 0 else ""
            

            if token_anterior != "(": #Se o token anterior não for um parentesis, significa que tem coisa na pilha da APPEND
                #Significa que o valor a ser guardado é o resultado da linha, e o resultado da linha é o valor da variável.
                codigo_text.append(f"    vpop {{d0}}") #Faz o pop do valor a ser guardado, que deve estar no topo da pilha.
                codigo_text.append(f"    ldr r0, =var_{token}") #Carrega o endereço em r0, e depois guarda o valor de d0 no endereço de r0
                codigo_text.append(f"    vstr.f64 d0, [r0]") #Empilhamos d0 de volta, por que o resultado de linha deve ser o valor da variavel
                codigo_text.append(f"    vpush {{d0}}")#E se for parêntese antes, significa que estamos lendo a variável para usar em uma operação
                #então só carregamos o valor da variável e empilhamos.
            
            #Se não for parêntese antes, significa que tem coisa na pilha da APPEND 
            #então o valor a ser guardado é o resultado da linha, e o resultado da linha é o valor da variável.
            else:
                codigo_text.append(f"    ldr r0, =var_{token}")
                codigo_text.append(f"    vldr.f64 d0, [r0]")
                codigo_text.append(f"    vpush {{d0}}")

    #Finalmente, depois de processar todos os tokens, precisamos adicionar as linhas de código para finalizar a função main 
    #o pop pc é a instrução de retorno, que vai pegar o endereço de retorno que guardamos no início da função e retornar para ele.
    codigo_text.append("    pop {pc, pc}")
    

    #Agora juntamos as linhas de código da seção de dados e da seção de texto para formar o arquivo completo.
    arquivo_completo = "\n".join(codigo_data) + "\n\n" + "\n".join(codigo_text)
    return arquivo_completo

if __name__ == "__main__":
    linhas_teste = []
    lerArquivo("testes.txt", linhas_teste)
    
    tokens_teste = ['(', '10', '3', '//', ')']
    print(gerarAssembly(tokens_teste))

