import datetime

class MaquinaPost:
    def __init__(self, palavra, instrucoes):
        """
        Inicializa a máquina com a palavra a ser processada e o arquivo com instruções.
        """
        try:
            with open(instrucoes, 'r') as arq:
                self.transicoes = self.Mapear(arq)
            self.qtd_transicoes = len(self.transicoes)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de instruções '{instrucoes}' não encontrado.")

        self.palavra = list(palavra.strip())
        self.estado_atual = 's'
        self.fita_atual = self.palavra[0] if self.palavra else ''
        self.transicao_atual = ''
        self.historico = []

        # Utilizando o nome do arquivo para indentificar as instruções
        self.instrucoes = instrucoes.split('\\')[-1].split('.')[0]  # Extrai o nome do arquivo sem extensão

    def Mapear(self, instrucoes):
        """
        Mapeia instruções do arquivo para transições reconhecidas pela máquina.
        """
        mapeamento = []
        for linha in instrucoes:
            linha = linha.strip()
            if not linha or linha.startswith('*'):
                continue

            partes = [p.strip('<>') for p in linha.split('><')]

            estado_atual, fita_atual = partes[0], partes[1]

            if len(partes) == 4:
                estado_novo, escrever, comando = partes[2], partes[3], 'W'
            elif len(partes) == 3:
                estado_novo, escrever, comando = partes[2], '', 'R'
            else:
                raise ValueError(f"Formato inesperado na linha: {linha}")

            mapeamento.append((estado_atual, fita_atual, estado_novo, escrever, comando))

        return mapeamento

    def Prox_Transicao(self):
        """
        Busca a próxima transição possível baseada no estado e fita atual.
        """
        for transicao in self.transicoes:
            if self.estado_atual == transicao[0]:
                if transicao[4] == 'R' and self.fita_atual == transicao[1]:
                    self.transicao_atual = transicao
                    return 0
                elif transicao[4] == 'W':
                    self.transicao_atual = transicao
                    return 0
        return -1

    def Processar_Transicao(self):
        """
        Executa a transição atualmente selecionada.
        """
        try:
            comando = self.transicao_atual[4]

            if comando == 'R':
                self.palavra.pop(0)
                self.fita_atual = self.palavra[0] if self.palavra else ''
            elif comando == 'W':
                self.palavra.append(self.transicao_atual[3])
                self.fita_atual = self.palavra[0]

            self.estado_atual = self.transicao_atual[2]
            return 0

        except (IndexError, TypeError):
            return -1

    def Fim(self):
        """
        Verifica se o estado atual é o estado final ('h').
        """
        return self.estado_atual == 'h'

    def Historico(self):
        """
        Registra o estado atual da fita no histórico.
        """
        self.historico.append(self.palavra.copy())

    def SalvaHistorico(self):
        """
        Salva o histórico da fita em um arquivo.
        """
        timestamp = datetime.datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        historico_filename = f'Historico/historico_{self.instrucoes}_{timestamp}.txt'
        with open(historico_filename, 'w') as f:
            for estado in self.historico:
                f.write(''.join(estado) + '\n')

    def __str__(self):
        """
        Formata a saída visual para exibição da máquina de forma bonita.
        """
        tamanho_fita = len(self.palavra)
        base = 57 - (tamanho_fita * 2)
        if tamanho_fita == 0:
            base = 56

        estado_formatado = f'''
║ 🔸 Estado Atual: {self.estado_atual:<56}║
║ 📑 Fita Atual: [{" ".join(self.palavra)}]{'':<{base}}║
║ 🔄 Transição: ({self.estado_atual}, {'ε' if not self.transicao_atual[1] else self.transicao_atual[1]}) ➜  ({self.transicao_atual[2]}, {'ε' if not self.transicao_atual[3] else self.transicao_atual[3]}, {self.transicao_atual[4]}){'':<39} ║
╚══════════════════════════════════════════════════════════════════════════╝'''

        return estado_formatado