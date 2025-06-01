from MaquinaPost import MaquinaPost

# Configuração inicial
MAX_ITERACOES = 10000
palavra = "aaabbcc"
arquivo_instrucoes = "Instrucoes\instrucoes_anbncn.txt"

# Inicializa a Máquina de Post com a palavra e instruções fornecidas
maquina = MaquinaPost(palavra, arquivo_instrucoes)

# Contador de iterações
iteracao = 0

# Executa a máquina enquanto não alcançar o limite máximo de iterações
while iteracao < MAX_ITERACOES:

    # 1) Encontra a próxima transição possível
    resultado = maquina.Prox_Transicao()

    # Verifica se a transição foi encontrada
    if resultado == -1:
        print("Palavra não pode ser processada!!!")
        break

    # 2) Executa a transição encontrada
    resultado = maquina.Processar_Transicao()

    # Checa o resultado do processamento
    if resultado == -1:
        print("Palavra não pode ser processada!!!")
        break

    # 3) Verifica se a máquina atingiu o estado final (halt)
    if maquina.Fim():
        print("\n                  ✨🎉 Palavra encontrada com sucesso! 🎉✨\n")
        break

    # Incrementa contador de iterações
    iteracao += 1

    # Exibe informações detalhadas da iteração atual
    print(f"\n╔═══════════════════════════════ Iteração: {iteracao:<2} ═════════════════════════════╗",end='')
    print(maquina)

    # Registra o estado atual no histórico da máquina
    maquina.Historico()

else:
    # Caso atinja o máximo de iterações sem concluir
    print("Limite de iterações atingido sem halt.")

# Salva o histórico da execução da máquina em arquivo
maquina.SalvaHistorico()
