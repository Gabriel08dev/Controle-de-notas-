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
| O que pode ser configurado? | Quantidades de alunos e avaliações, faixa de notas e totais para recuperação e aprovação |
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
| Tornar a documentação fácil de entender | Usar exemplos, tabelas, passos de uso e explicações de termos técnicos |

**Essas orientações posteriores definem o comportamento atual.** Ao alterar o código, não volte a fixar cinco alunos ou a usar a média para classificar.

## Como a regra atual funciona

O programa soma todas as notas de cada aluno e compara o resultado com dois limites configuráveis.

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

Todas as avaliações têm o mesmo peso. O programa ainda não trata frequência, prova extra de recuperação ou uma nova nota final após essa prova.

Os limites precisam caber nos totais possíveis. Com três avaliações de 0 a 10, o total vai de 0 a 30; portanto, um limite de aprovação de 40 seria inválido.

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
| `validar_nota` | Conferir se a nota está na faixa permitida |
| `validar_configuracao` | Conferir quantidades, faixa das notas e limites totais |
| `calcular_resultados` | Somar, calcular médias e classificar a turma |
| `formatar_numero` | Preparar o número para aparecer com vírgula e duas casas decimais |
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
| Classificar pelo total exato | O arredondamento mostrado na tela não deve mudar a situação |
| Manter a média | Permitir consultar o desempenho médio de cada aluno e da turma |
| Usar números `Decimal` | Trabalhar com notas decimais sem as pequenas diferenças típicas da representação binária |
| Usar precisão de 60 dígitos nos cálculos de resultados | Dar margem às operações com entradas numéricas de até 30 caracteres |
| Exigir o preenchimento da turma inteira | Evitar resultados de turma baseados em dados faltantes |
| Permitir nomes repetidos | Cada aluno é associado à sua linha, não apenas ao nome |
| Aceitar quantidades a partir de 1, sem teto programado | Adaptar o formulário à necessidade do usuário; o computador ainda tem limites de recursos |
| Guardar os dados apenas durante a sessão | Salvar e abrir turmas ainda é uma melhoria proposta |
| Confirmar alterações que limpam a turma | Permitir que a pessoa cancele antes de perder o preenchimento |
| Manter o prompt original | Preservar as orientações pedagógicas do trabalho |

As opções da turma são guardadas em variáveis de configuração:

| Nome no código | Significado |
|---|---|
| `QUANTIDADE_ALUNOS` | Número de alunos da turma |
| `QUANTIDADE_NOTAS` | Número de avaliações por aluno |
| `NOTA_MINIMA` e `NOTA_MAXIMA` | Menor e maior nota aceitas por avaliação |
| `TOTAL_RECUPERACAO` e `TOTAL_APROVACAO` | Totais necessários para cada faixa de situação |

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

O histórico de desenvolvimento de **19/09/2026** registra:

- Testes de totais, médias, situações e valores nos limites de classificação.
- Testes de entradas inválidas, mudança de configuração, limpeza e ações da janela.
- Verificação de uma turma de 100 alunos com 20 avaliações e de linhas de notas independentes. Esse cenário foi um teste, não um limite do sistema.
- Revisão visual do layout arredondado e da coluna Total.
- Geração do executável e confirmação de abertura e encerramento normal no Windows, com código de saída 0.
- Ausência de teste em outro computador até esse registro.

**Código de saída 0** significa que o processo terminou normalmente. Os registros acima descrevem verificações anteriores; mudanças futuras precisam de novas verificações apropriadas.

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
