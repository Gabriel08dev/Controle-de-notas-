# MEMORY — a memória do projeto

Este arquivo registra **o que foi decidido, por que foi decidido e como o programa está organizado**. Ele ajuda uma pessoa a continuar o trabalho sem precisar conhecer toda a conversa que deu origem ao projeto.

Para aprender a usar o aplicativo, leia o [README.md](README.md). Para acompanhar melhorias futuras, veja o [ROADMAP.md](ROADMAP.md).

## O projeto em um minuto

| Pergunta | Resposta |
|---|---|
| Para que serve? | Registrar notas e mostrar a situação de cada aluno |
| O que decide a situação? | A soma total das avaliações |
| A média continua existindo? | Sim, como informação individual e no resumo da turma |
| Quais situações existem? | Aprovado, Recuperação e Reprovado |
| O que pode ser configurado? | Quantidade de alunos, notas por aluno, nota máxima do sistema e notas mínimas para aprovação e recuperação |
| Os dados ficam salvos ao sair? | Não. Eles existem apenas durante a sessão aberta |
| Qual tecnologia é usada? | Python, com Tkinter e ttk para construir a janela |
| Onde está o código? | No arquivo [main.py](main.py), organizado em funções |

## De onde vieram as regras

O ponto de partida foi o arquivo `Trabalho_Programacao_2_Controle_de_Notas_Final.pdf`, que descreve o cenário acadêmico. As orientações para construir o código estão em [ia/Prompt Python.md](ia/Prompt%20Python.md).

O cenário inicial tinha cinco alunos, três avaliações e aprovação pela média. Durante o desenvolvimento, o solicitante pediu estas mudanças:

| Pedido | Decisão adotada |
|---|---|
| Adaptar o programa a diferentes áreas | Permitir configurar quantidades e critérios de notas |
| Aceitar menos de cinco alunos e remover o máximo fixo | Aceitar quantidades inteiras a partir de 1, sem teto programado |
| Incluir recuperação | Criar uma faixa entre reprovação e aprovação |
| Deixar a janela mais arredondada | Usar cartões e botões arredondados e reduzir as molduras |
| Classificar pelo total, mantendo a média | Comparar a soma com os totais configurados; continuar mostrando a média |
| Simplificar a configuração das notas | Usar uma nota máxima total do sistema e duas notas mínimas: aprovação e recuperação |
| Tornar a documentação fácil de entender | Usar exemplos, tabelas, passos de uso e explicações de termos técnicos |
| Deixar o fundo e o layout mais amigáveis | Adotar creme claro, verde sálvia, campos espaçosos e indicação de foco pelo teclado |

**Essas orientações posteriores definem o comportamento atual.** Ao alterar o código, não volte a fixar cinco alunos ou a usar a média para classificar.

## Como a regra atual funciona

O programa soma todas as notas de cada aluno e compara o resultado com dois limites configuráveis. A soma deve ficar entre zero e a nota máxima do sistema.

| Total do aluno | Situação |
|---|---|
| Menor que o total para recuperação | Reprovado |
| Igual ou maior que o total para recuperação, mas menor que o de aprovação | Recuperação |
| Igual ou maior que o total para aprovação | Aprovado |

Exemplo com recuperação em 12 e aprovação em 18:

```text
Notas: 4, 5 e 6
Total: 4 + 5 + 6 = 15
Média: 15 ÷ 3 = 5

Situação: Recuperação, porque 15 está entre 12 e menos de 18.
```

Cada campo contribui para a soma com o valor digitado. O programa ainda não trata pesos, frequência, prova extra de recuperação ou uma nova nota final após essa prova.

Os dois limites precisam ficar entre zero e a nota máxima do sistema, e a recuperação deve começar antes da aprovação. Com nota máxima 30, recuperação em 12 e aprovação em 18, a configuração é válida. Uma soma de 31 é recusada, mesmo que cada nota isolada esteja entre zero e 30.

## Como os dados são organizados

Um **vetor** é uma lista. Uma **matriz** é uma tabela de linhas e colunas. O programa usa essas duas estruturas para manter cada nome associado às suas notas.

```python
alunos = ["Ana", "Bruno"]
notas = [
    [8, 7, 9],  # Notas de Ana
    [4, 5, 6],  # Notas de Bruno
]
```

A primeira posição de `alunos` corresponde à primeira linha de `notas`. Em Python, a contagem de posições começa em zero: `alunos[0]` é Ana e `notas[0]` contém as notas dela.

Quando uma nota está vazia ou inválida, a matriz guarda `None`, que significa “sem valor válido”. Isso evita confundir uma nota ausente com a nota zero.

As linhas da matriz são independentes: editar a nota de um aluno não deve alterar a de outro.

## O caminho de uma nota dentro do programa

1. A pessoa digita um nome ou uma nota.
2. O programa atualiza os dados em memória e o contador de preenchimento.
3. Os resultados anteriores são retirados da tela para evitar informações desatualizadas.
4. Ao clicar em **Calcular resultados**, o programa verifica todos os campos.
5. Se houver erro, mostra uma mensagem e indica o campo a corrigir.
6. Se tudo estiver válido, calcula totais e médias, classifica os alunos e atualiza o resumo.

Essa sequência explica por que editar uma nota exige um novo cálculo.

## Onde encontrar cada responsabilidade no código

Uma **função** é um bloco de código com uma tarefa específica. Os nomes abaixo ajudam a localizar o trecho certo em [main.py](main.py).

| Função ou grupo | Tarefa explicada de forma simples |
|---|---|
| `converter_decimal` | Transformar um texto como `7,5` em um número |
| `validar_nota` | Conferir se cada nota está entre zero e a nota máxima do sistema |
| `validar_configuracao` | Conferir quantidades, nota máxima e as duas notas mínimas |
| `calcular_resultados` | Somar, calcular médias e classificar a turma |
| `formatar_numero` | Mostrar médias com vírgula, duas casas e arredondamento escolar |
| `formatar_total` | Mostrar todos os dígitos do total que podem mudar a classificação |
| `atualizar_estado` e `invalidar_resultados` | Acompanhar o preenchimento e retirar resultados antigos |
| `processar_resultados` | Coordenar a ação do botão de cálculo |
| `criar_interface` e `abrir_configuracoes` | Montar a janela e as opções da turma |
| `desenhar_retangulo_arredondado`, `criar_cartao_arredondado` e `criar_botao_arredondado` | Desenhar o visual arredondado |
| `limpar_dados` e `encerrar` | Limpar a turma ou fechar o programa |
| `main` | Iniciar a aplicação e mantê-la aberta para receber ações |

A função `calcular_resultados` não depende dos controles da janela para fazer as contas. Ela recebe os nomes e as notas, consulta os critérios configurados e devolve os resultados sem alterar as listas recebidas. Isso facilita conferir os cálculos separadamente.

## Decisões que devem ser preservadas

| Decisão | Motivo ou efeito |
|---|---|
| Classificar pelo total exato | A coluna Total preserva os dígitos decisivos para que o valor visível explique a situação |
| Manter a média | Permitir consultar o desempenho médio de cada aluno e da turma |
| Arredondar médias com `ROUND_HALF_UP` | Apresentar o arredondamento escolar esperado, como `6,125 → 6,13` |
| Usar números `Decimal` | Trabalhar com notas decimais sem as pequenas diferenças típicas da representação binária |
| Usar precisão de 60 dígitos nos cálculos de resultados | Dar margem às operações com entradas numéricas de até 30 caracteres |
| Exigir o preenchimento da turma inteira | Evitar resultados de turma baseados em dados faltantes |
| Permitir nomes repetidos | Cada aluno é associado à sua linha, não apenas ao nome |
| Aceitar quantidades a partir de 1, sem teto programado | Adaptar o formulário à necessidade do usuário; o computador ainda tem limites de recursos |
| Guardar os dados apenas durante a sessão | Salvar e abrir turmas ainda é uma melhoria proposta |
| Confirmar alterações quando há dados preenchidos | Permitir que a pessoa cancele antes de perder a turma; uma tela vazia não exige confirmação |
| Avisar configurações com mais de 2.000 campos | Reduzir o risco de lentidão sem criar um máximo rígido |
| Manter o prompt original | Preservar as orientações pedagógicas do trabalho |

As opções da turma são guardadas em variáveis de configuração:

| Nome no código | Significado |
|---|---|
| `QUANTIDADE_ALUNOS` | Número de alunos da turma |
| `QUANTIDADE_NOTAS` | Número de notas por aluno |
| `NOTA_MAXIMA_SISTEMA` | Maior soma permitida para cada aluno |
| `TOTAL_APROVACAO` | Nota total mínima para aprovação |
| `TOTAL_RECUPERACAO` | Nota total mínima para fazer recuperação |

## Escolhas para uma janela mais amigável

O fundo creme claro e o cabeçalho verde sálvia criam uma aparência suave. Os textos escuros facilitam a leitura; os campos mais espaçosos e os cantos arredondados organizam o preenchimento. A situação continua escrita por extenso, para que a pessoa não precise distinguir as cores para entender o resultado.

Ao navegar com `Tab`, o botão selecionado recebe um contorno. Isso é o **foco do teclado**: a indicação de qual controle receberá a próxima ação. O tamanho inicial da janela se adapta à tela, e a tabela mantém a rolagem para turmas maiores.

Ao alterar esse visual novamente, confira as cores do fundo e dos cartões em conjunto, mantenha o foco visível e verifique se os textos e botões cabem em uma tela menor. Esta decisão visual não altera as regras de cálculo.

## Por que o código usa funções e repetições

O trabalho pede programação **procedural**: organizar as tarefas em funções e estruturas de controle, sem definir classes próprias. Os componentes prontos da biblioteca Python, como os controles Tkinter e os números Decimal, podem ser utilizados.

As três estruturas fundamentais aparecem assim:

| Estrutura | O que significa | Exemplo no programa |
|---|---|---|
| Sequência | Executar uma ação depois da outra | Conferir dados, calcular e mostrar os resultados |
| Seleção | Escolher um caminho por uma condição | Decidir entre aprovado, recuperação e reprovado |
| Repetição | Executar uma tarefa várias vezes | Percorrer as notas de cada aluno para somá-las |

Os comentários do código explicam também os métodos e atalhos utilizados. Ao acrescentar um recurso, mantenha esse cuidado para que o programa continue útil como material de estudo.

## O que já foi verificado

A revisão final de **20/09/2026** registra:

- Compilação sintática de `main.py` e `testes.py` sem erros.
- Testes de totais exatos, médias informativas, aprovação, recuperação e reprovação nos limites configurados.
- Testes da nota máxima do sistema, inclusive soma parcial acima do máximo, valores decimais, arredondamento escolar e normalização de `-0`.
- Testes de entradas inválidas, prévia dos critérios, mudança de configuração, limpeza e encerramento da janela.
- Revisão visual da janela no tamanho de notebook de 1180 × 658 pixels: os cinco alunos iniciais ficam visíveis e as barras de rolagem aparecem apenas quando necessárias.
- Revisão visual da tela de configuração com as três regras pedidas: nota máxima, mínima para aprovação e mínima para recuperação.
- Geração de `dist/ControleDeNotas.exe` e confirmação de que o processo abre e responde no Windows.
- Auditoria padrão do Codex Security em todos os 14 arquivos do projeto, sem vulnerabilidades reportáveis. A adoção futura de hashes para todas as dependências e de assinatura do executável foi registrada como melhoria de procedência do build.
- Ausência de teste do executável em outro computador até este registro.

Os registros acima descrevem as verificações desta versão. Mudanças futuras precisam de novas verificações apropriadas.

O ambiente usado na implementação tinha **Python 3.13.0**, **PyInstaller 6.22.3** e Windows. As versões citadas no PDF pertencem à comprovação anterior da equipe e podem ser diferentes desse ambiente.

## IA no desenvolvimento

A extensão Continue 2.0.0 foi registrada como instalada no VS Code durante o desenvolvimento. Há um exemplo para Gemini e OpenRouter em `ia/continue.config.example.yaml`.

Ainda faltam as credenciais pessoais e a confirmação de uma resposta de cada serviço. A conexão só deve ser considerada funcionando depois desses testes. As chaves de acesso não devem ser incluídas nos arquivos compartilhados.

O aplicativo de notas funciona localmente e não utiliza IA para calcular os resultados.

## Como continuar o projeto

1. Leia o [README.md](README.md) para entender o uso atual.
2. Consulte o [ROADMAP.md](ROADMAP.md) e defina a melhoria que será feita.
3. Localize as funções relacionadas usando o mapa deste arquivo.
4. Faça a alteração mantendo as regras pedagógicas e de classificação.
5. Para mudanças nos cálculos ou na interface, confira os exemplos e execute `python testes.py`.
6. Revise visualmente a janela quando alterar o layout.
7. Atualize estes documentos quando o comportamento ou as decisões mudarem.
8. Se o programa foi alterado, gere novamente o executável com `gerar_executavel.ps1`.

Ao implementar salvamento de turmas no futuro, documente onde os arquivos ficam, o que é salvo e o que acontece quando um arquivo não pode ser aberto.
