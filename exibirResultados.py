def exibirResultados(resultados: list):
    for resultado in resultados:
        if isinstance(resultado, (float, int)):
            print(f"{resultado:.1f}")
        else:
            print(resultado)