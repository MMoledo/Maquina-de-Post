**README.md**

---

## Projeto: Máquina de Post (PCG - POST)

Este repositório reúne uma implementação em Python de uma **Máquina de Post**, capaz de reconhecer e processar linguagens formais (por exemplo, `s → anbn` e `s → anbncn`), registrar o histórico de execução e gerar saídas visuais ilustrativas do estado da máquina em cada passo.

---

### 1. Visão Geral

A **Máquina de Post** aqui implementada recebe como entrada:

* Uma **palavra** inicial (cadeia de símbolos).
* Um **arquivo de instruções** que define as transições a partir de um alfabeto definido.

A execução da máquina percorre as regras de transição até atingir um estado de **halt** (ou até um limite máximo de iterações), exibindo, a cada iteração, o estado atual, o conteúdo da fita e a transição aplicada. Ao final, grava-se um **arquivo de histórico** contendo todos os passos da execução.

---

### 2. Pré-requisitos

* **Python 3.7** (ou superior) instalado no sistema.
* Terminal/console (Windows, macOS ou Linux).
* Nenhuma biblioteca externa além das bibliotecas padrão do Python.

---

### 3. Estrutura do Repositório

```
PCG - POST/
├── app.py
├── MaquinaPost.py
├── Instrucoes/
│   ├── instrucoes_anbn.txt
│   └── instrucoes_anbncn.txt
├── Historico/
│   ├── historico_instrucoes_anbn_*.txt
│   └── historico_instrucoes_anbncn_*.txt
└── Image/
    ├── Exercicio.png
    └── Exercicio2.png
```

* **app.py**
  Script principal que inicializa e executa a Máquina de Post, definindo a palavra de entrada, o arquivo de instruções e o número máximo de iterações.

* **MaquinaPost.py**
  Implementação da classe `MaquinaPost`, contendo:

  * Parsing do arquivo de instruções.
  * Controles de estado/fita/transição.
  * Métodos para avançar passo a passo (`Prox_Transicao`).
  * Registro de histórico de execução (`Historico`, `SalvaHistorico`).
  * Formatação `__str__` para exibição visual (caixa estilizada com estado, fita e transição corrente).

* **Instrucoes/**
  Contém arquivos de exemplo com as regras de transição para duas linguagens:

  * `instrucoes_anbn.txt`
    Regras para reconhecer a linguagem `{ aⁿ bⁿ | n ≥ 1 }`.
  * `instrucoes_anbncn.txt`
    Regras para reconhecer a linguagem `{ aⁿ bⁿ cⁿ | n ≥ 1 }`.

  Cada arquivo segue o formato de linhas do tipo:

  ```
  <estado_atual><símbolo_lido><estado_destino><símbolo_escrito>
  ```

  * **Exemplo de linha:**
    `<s><><1><#>`

    * Ao entrar em estado `s`, se o símbolo lido for “vazio” (ε), vá para estado `1` e escreva “#”.
  * Os símbolos “<>” devem envolver cada componente (estado, símbolo da fita, novo estado, símbolo a ser escrito).

* **Historico/**
  Toda vez que a máquina é executada via `app.py`, cria-se um arquivo de histórico com timestamp:

  * `historico_instrucoes_anbn_DD_MM_AA_hh_mm_ss.txt`
  * `historico_instrucoes_anbncn_DD_MM_AA_hh_mm_ss.txt`
    Cada arquivo contém, em texto puro, uma sequência de linhas que descrevem cada iteração (estado, fita antes/depois, transição usada).

* **Image/**
  Imagens exemplificando exercícios e salvando prints de exemplo para facilitar entendimento visual:

  * `Exercicio.png`
  * `Exercicio2.png`

---

### 4. Como Funciona

1. **Definição da Palavra Inicial e do Arquivo de Instruções**
   No topo de `app.py`, edite as linhas:

   ```python
   MAX_ITERACOES = 10000
   palavra = "cc"
   arquivo_instrucoes = "Instrucoes/instrucoes_anbncn.txt"
   ```

   * `palavra` é a cadeia de símbolos a ser processada.
   * `arquivo_instrucoes` deve apontar para o caminho relativo (ou absoluto) de um arquivo `.txt` que obedeça ao formato descrito na seção de Instruções.

2. **Inicialização da Máquina de Post**
   Ao executar:

   ```bash
   python app.py
   ```

   a instância `maquina = MaquinaPost(palavra, arquivo_instrucoes)` vai:

   * Abrir o arquivo de instruções.
   * Chamar `self.Mapear(arq)` para transformar cada linha em uma tupla de transição.
   * Armazenar em `self.transicoes` uma lista de todas as regras.

3. **Execução das Transições**
   Dentro do laço:

   ```python
   while iteracao < MAX_ITERACOES:
       # Exibe o estado atual, a fita e a transição pendente
       print(f"\n╔═ Iteração: {iteracao} ═════════════════════════╗", end='')
       print(maquina)               # Chamando __str__ para exibir o quadro visual
       maquina.Historico()          # Registra no histórico de execução
       # ... chamada interna para avançar à próxima transição:
       resultado = maquina.Prox_Transicao()
       if resultado == "HALT":
           break
       iteracao += 1
   else:
       print("Limite de iterações atingido sem halt.")
   maquina.SalvaHistorico()
   ```

   * Em cada passo:

     1. `__str__` monta uma representação visual (caixa Unicode) com:

        * Estado atual (`self.estado_atual`)
        * Conteúdo da fita (`self.palavra`)
        * Transição aplicada (`(estado, símbolo_lido, novo_estado, símbolo_escrito)`)
     2. `maquina.Historico()` anexa essa informação numa lista interna para posterior gravação.
     3. `maquina.Prox_Transicao()` busca, a partir de `self.estado_atual` e símbolo lido na fita, qual regra aplicar.

        * Se não houver transição aplicável, retorna `"HALT"`.
        * Caso haja, escreve novo símbolo, move cabeçote (pode ser implícito “para direita” em máquinas de Post), atualiza `self.estado_atual` e prepara `self.transicao_atual` para exibição.
     4. Se `resultado == "HALT"`, o laço se encerra antes de atingir `MAX_ITERACOES`.

4. **Gravação do Histórico**
   Ao final (após `break` ou esgotar `MAX_ITERACOES`), chama-se:

   ```python
   maquina.SalvaHistorico()
   ```

   * Gera um arquivo de texto em `Historico/` com nome padronizado:

     ```
     historico_instrucoes_<nome_do_arquivo>_DD_MM_AA_hh_mm_ss.txt
     ```
   * Contém, linha a linha, a descrição do estado da máquina a cada iteração (estado, fita, transição utilizada).

---

### 5. Formato dos Arquivos de Instruções

Cada regra de transição deve estar em uma linha, no padrão:

```
<estado_atual><símbolo_lido><estado_destino><símbolo_escrito>
```

* **estado\_atual**: identificador de estado (por exemplo, `s`, `1`, `2`, …).
* **símbolo\_lido**: símbolo que a máquina lê na posição corrente da fita.

  * Caso queira representar “vazio” (ε), basta deixar a área entre `< >` em branco (por exemplo: `<s><><1><#>`).
* **estado\_destino**: identificador de estado para o próximo passo.
* **símbolo\_escrito**: símbolo a ser escrito na fita naquela posição.

  * Para não alterar o símbolo (copiar o mesmo), pode escrever o mesmo símbolo lido.
  * Se quiser deletar/caracter “vazio”, deixe em branco (ex.: `<3><><2><a>`).

**Exemplo completo** (arquivo `instrucoes_anbncn.txt`):

```
<s><><1><#>
<1><a><2>
<1><b><0>
<1><c><0>
<1><#><h>
<2><a><3>
<3><><2><a>
<2><#><0>
<2><c><0>
<2><b><4>
<4><b><5>
<5><><4><b>
<4><c><6>
<4><a><0>
<4><#><0>
<6><c><7>
<7><><6><c>
<6><#><8>
<6><a><0>
<6><b><0>
<8><><1><#>
```

* Neste exemplo, ao iniciar em estado `s` e ler “vazio” (`ε`), escreve-se “#” e vai para estado `1`.
* Em cada transição, a máquina procura exatamente o estado e o símbolo lido, aplica a regra correspondente e avança no processamento.

---

### 6. Como Executar

1. **Prepare a palavra de entrada** em `app.py`, alterando a variável:

   ```python
   palavra = "cc"
   ```

   Pode ser qualquer sequência de símbolos (`a`, `b`, `c` etc.), de acordo com as instruções que deseja testar.

2. **Aponte o arquivo de instruções**:

   ```python
   arquivo_instrucoes = "Instrucoes/instrucoes_anbncn.txt"
   ```

   * Use sempre a barra (“/”) ou contrabarra de forma consistente para o seu sistema operacional (no Windows, `"\\"` ou `"/"` também funciona).
   * Os exemplos disponíveis estão em `Instrucoes/`.

3. **Defina o número máximo de iterações** (padrão: `10000`), para evitar loops infinitos:

   ```python
   MAX_ITERACOES = 10000
   ```

4. **Execute**:

   ```bash
   python app.py
   ```

5. **Acompanhe a saída no terminal**:

   * A cada iteração, será exibida uma “caixa” contendo:

     ```
     ╔════════════════════════ Iteração:  0 ════════════════════════╗
     ║ 🔸 Estado Atual: s                                           ║
     ║ 📑 Fita Atual: [ c c ]                                        ║
     ║ 🔄 Transição: (s, ε, #)                                       ║
     ╚══════════════════════════════════════════════════════════════╝
     ```
   * Em seguida, o cabeçote de instruções aplica a transição e passa para o próximo passo, imprimindo a próxima iteração.

6. **Verifique o histórico gerado** na pasta `Historico/`:
   Um arquivo `historico_instrucoes_<nome>_<timestamp>.txt` conterá, em texto puro, todas as linhas exibidas (estado, fita, transição) durante a execução. Isso permite:

   * Revisar passo a passo o comportamento da máquina.
   * Depurar regras ou testar novas cadeias de entrada sem depender apenas do console.

---

### 7. Estrutura e Descrição de Cada Arquivo

* **app.py**

  * Responsável por:

    1. Importar `MaquinaPost`.
    2. Configurar `MAX_ITERACOES`, `palavra` e `arquivo_instrucoes`.
    3. Instanciar a máquina: `maquina = MaquinaPost(palavra, arquivo_instrucoes)`.
    4. Laço principal que exibe cada iteração, registra o histórico e chama `Prox_Transicao()`.
    5. Tratar condições de `HALT` e salvar log final com `SalvaHistorico()`.

* **MaquinaPost.py**

  * **Classe `MaquinaPost`**:

    * **`__init__(self, palavra, instrucoes)`**

      * Abre o arquivo de instruções e chama `Mapear(arq)`, gerando uma lista de tuplas `(estado_atual, símbolo_lido, estado_destino, símbolo_escrito)`.
      * Armazena em `self.transicoes` e define `self.qtd_transicoes`.
      * Inicializa:

        * `self.palavra` – lista de caracteres a ser processada.
        * `self.estado_atual` – começa em `'s'`.
        * `self.transicao_atual` – string vazia ou valor anterior.
        * `self.historico_execucao` – lista onde se armazenam snapshots de cada iteração.
    * **`Mapear(self, arquivo)`**

      * Lê linha a linha (ignorando comentários com `*` ou linhas vazias).
      * Divide cada linha nos campos entre “<>” e retorna uma lista de transições no formato `[ (estado_atual, símbolo_lido, estado_destino, símbolo_escrito), ... ]`.
    * **`Prox_Transicao(self)`**

      * Identifica, a partir de `(self.estado_atual, símbolo_lido na fita)`, qual transição aplicar.
      * Se não houver regra correspondente, retorna `"HALT"`.
      * Caso encontre:

        1. Atualiza o símbolo na fita (substitui ou “apaga” conforme instrução).
        2. Atualiza `self.estado_atual` para `estado_destino`.
        3. Armazena em `self.transicao_atual` a tupla aplicada.
        4. Ajusta a posição do cabeçote (no modelo simplificado, avança um casa para a direita ou LIFO, conforme implementação interna).
        5. Retorna algum indicador (por ex. `"OK"` ou o próprio registro).
    * **`Historico(self)`**

      * Adiciona à lista interna (`self.historico_execucao`) uma string formatada, contendo:

        ```
        [timestamp] Iteração: i – Estado: X – Fita: [...] – Transição: (...)
        ```
      * Cada chamada registra um snapshot *antes* ou *depois* da transição, conforme convenção.
    * **`SalvaHistorico(self)`**

      * Gera um arquivo de texto novo em `Historico/`, com nome padrão:

        ```
        historico_instrucoes_<nome_arquivo>_DD_MM_AA_hh_mm_ss.txt
        ```
      * Percorre `self.historico_execucao` e grava cada linha no arquivo.
    * **`__str__(self)`**

      * Retorna uma string multiline que formata:

        ```
        ╔════════════════════════════════════════════════════════╗
        ║ 🔸 Estado Atual: s                                        ║
        ║ 📑 Fita Atual: [c c a b ...]                             ║
        ║ 🔄 Transição: (s, ε, #)                                   ║
        ╚════════════════════════════════════════════════════════╝
        ```

* **Pasta `Instrucoes/`**

  * Cada arquivo de instruções segue o padrão explicado na seção “Formato dos Arquivos de Instruções”.
  * **`instrucoes_anbn.txt`**

    * Conjunto de regras que reconhecem cadeias da forma `aⁿ bⁿ`.
  * **`instrucoes_anbncn.txt`**

    * Conjunto de regras que reconhecem cadeias da forma `aⁿ bⁿ cⁿ`.

* **Pasta `Historico/`**

  * Armazena diversos arquivos `historico_*.txt` gerados em execuções anteriores.
  * Permite acompanhar detalhes de cada passo para fins de depuração ou análise posterior.

* **Pasta `Image/`**

  * Contém imagens ilustrativas dos exercícios (diagramas de máquina, exemplos de fita, etc.).
  * **`Exercicio.png`**, **`Exercicio2.png`** servem como referência visual para quem estiver aprendendo a modelar máquinas de Post.

---

### 8. Exemplos de Uso

1. **Reconhecer `anbn`**

   * Em `app.py`, defina:

     ```python
     palavra = "aaabbb"
     arquivo_instrucoes = "Instrucoes/instrucoes_anbn.txt"
     ```
   * Execute:

     ```bash
     python app.py
     ```
   * Saída no console:

     ```
     ╔════════════════════════ Iteração:  0 ════════════════════════╗
     ║ 🔸 Estado Atual: s                                           ║
     ║ 📑 Fita Atual: [ a a a b b b ]                               ║
     ║ 🔄 Transição: (s, ε, #)                                       ║
     ╚══════════════════════════════════════════════════════════════╝
     ...
     ║ 🔸 Estado Atual: h                                           ║
     ║ 📑 Fita Atual: [ # # # # # # ]                               ║
     ║ 🔄 Transição: (h, #, HALT)                                   ║
     ╚══════════════════════════════════════════════════════════════╝
     ```
   * Um arquivo em `Historico/` será criado, por exemplo:

     ```
     historico_instrucoes_anbn_31_05_25_21_07_46.txt
     ```

     Nele, cada linha descreve detalhadamente cada iteração.

2. **Reconhecer `anbncn`**

   * Em `app.py`, defina:

     ```python
     palavra = "aaabbbccc"
     arquivo_instrucoes = "Instrucoes/instrucoes_anbncn.txt"
     ```
   * Execute em terminal:

     ```bash
     python app.py
     ```
   * A saída exibirá cada transição, até atingir o estado de **halt** (geralmente marcado por `h` ou ausência de regra correspondente).

---

### 9. Boas Práticas e Observações

* **Caminhos de Arquivo**:
  No Windows, use `"\\"` ou `"/"` de forma consistente. Exemplo:

  ```python
  arquivo_instrucoes = "Instrucoes\\instrucoes_anbncn.txt"
  ```

  No Linux/macOS, basta:

  ```python
  arquivo_instrucoes = "Instrucoes/instrucoes_anbncn.txt"
  ```

* **Limite de Iterações (`MAX_ITERACOES`)**:
  Caso a Máquina de Post entre em loop infinito (sem encontrar “HALT”), o `app.py` interrompe após `MAX_ITERACOES` iterações para evitar travamentos.

* **Formato das Transições**:

  * Linhas em branco ou que começam com `*` são ignoradas.
  * Strings sempre envoltas em `<` `>`.
  * Exemplo de comentário no meio do arquivo:

    ```txt
    * Esta linha é ignorada pela máquina.
    <1><a><2><b>
    ```
  * Se quiser sobrescrever o mesmo símbolo (nenhuma mudança), repita o símbolo lido:
    `<3><a><4><a>`

* **Registro de Histórico**:

  * Cada chamada a `maquina.Historico()` guarda o estado completo ANTES da transição.
  * Ao final, `SalvaHistorico()` grava todas as linhas em arquivo, em ordem cronológica (com timestamps padrão em Python: `datetime.now()`).

---

### 10. Possíveis Extensões

* **Parâmetros dinâmicos via linha de comando**
  Permitir passar `palavra` e `arquivo_instrucoes` como argumentos (por ex., `python app.py aaabbb Instr/instr.txt`).
  Atualmente, é preciso editar `app.py` manualmente.

* **Suporte a Movimento de Cabeçote “para Esquerda”**
  A implementação atual pode supor sempre movimento “para a direita” (ou manipular a fita de forma simplificada). Para uma Máquina de Post tradicional, o cabeçote pode mover-se para a esquerda ou direita dependendo da instrução.

* **Validação de Formato de Instruções**
  Incluir checagem mais robusta se cada linha de instrução atende rigorosamente ao padrão `<estado><símbolo><novo_estado><escrever>`.

* **Interface Gráfica ou Web**
  Criar uma interface opcional (por exemplo, em Flask) que mostre cada iteração de forma interativa.

* **Geração de Relatório**
  Além do histórico em texto, exportar um arquivo `.csv` ou `.json` contendo detalhes das transições para análise posterior.

---

### 11. Licença

Este projeto está licenciado sob a **MIT License**. Sinta-se à vontade para copiar, modificar e redistribuir, desde que mantenha a atribuição original.


---

> **Observação Final:**
> Caso encontre problemas de encoding no Windows (por exemplo, ao abrir os arquivos de instruções), verifique se estão salvos em **UTF-8 sem BOM**. Isso evita que a leitura de linhas que começam com caracteres especiais (como `<` ou `#`) apresentem erros.
