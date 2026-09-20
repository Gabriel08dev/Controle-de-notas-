# Controle de Notas

Aplicação de janela para Windows, desenvolvida em Python com Tkinter/ttk e programação procedural para o trabalho de Programação 2 da UEMG, Unidade Carangola. Equipe indicada no enunciado: Gabriel da Silva, Samuel Pedrosa e Davi Gomes.

## Abrir o programa

Abra **`dist/ControleDeNotas.exe`** com duplo clique. O executável abre uma janela, sem console, e não requer Python instalado no computador de destino. A distribuição gerada é para Windows x64.

Para executar pelo código-fonte, instale Python com Tcl/Tk e use, na pasta do projeto:

```powershell
python main.py
```

No VS Code, também é possível pressionar F5 e escolher **Controle de Notas (Tkinter)**. A aplicação não usa APIs de IA, internet ou pacotes externos durante seu funcionamento.

## Usar e configurar

1. Use **Configurar turma e critérios** para escolher a quantidade de alunos e avaliações, a faixa de cada nota e as pontuações totais para recuperação e aprovação.
2. Preencha o nome e todas as notas de cada aluno. Aceitam-se vírgula ou ponto como separador decimal.
3. Clique em **Calcular Resultados** ou pressione Ctrl+Enter.
4. Consulte a nota total, a média individual, as situações **Aprovado**, **Recuperação** ou **Reprovado** e o resumo da turma.
5. Use **Limpar** (Ctrl+L) para uma nova turma com os mesmos critérios.

Os valores iniciais usam 5 alunos, 3 avaliações e notas de 0 a 10. Com essa configuração, o total inicial para recuperação é 12 e o total para aprovação é 18. **Todos esses valores são editáveis.** A turma e a quantidade de avaliações precisam ser de pelo menos 1, mas não possuem máximo programado; a capacidade prática depende dos recursos do computador. A faixa pode incluir valores negativos quando a área exigir.

O programa calcula automaticamente o menor e o maior total possíveis multiplicando a quantidade de avaliações pela nota mínima e pela nota máxima. Os critérios configurados devem respeitar:

```text
menor total possível ≤ total de recuperação < total de aprovação ≤ maior total possível
```

Por exemplo, com três avaliações de 0 a 10, o total possível vai de 0 a 30. Configurando recuperação em 12 e aprovação em 18, um total 17 fica em recuperação e um total 18 fica aprovado.

Alterar a configuração pede confirmação e inicia uma turma vazia. A interface tem rolagem horizontal e vertical para mais avaliações/alunos; Tab percorre e revela os campos. Os dados e as configurações são mantidos somente na memória durante a sessão. Fechar o programa perde o preenchimento, com confirmação quando houver dados.

## Regras de cálculo

- Nota total: soma de todas as avaliações do aluno.
- Aprovado: nota total igual ou superior ao total configurado para aprovação.
- Recuperação: nota total igual ou superior ao total de recuperação e inferior ao total de aprovação.
- Reprovado: nota total inferior ao total de recuperação.
- Média individual: nota total dividida pela quantidade de avaliações, com pesos iguais. A média é informativa e não altera a situação.
- A classificação usa o total exato antes da formatação visual.
- Média da turma: soma de todas as notas dividida pelo total de notas; equivale à média das médias porque todos têm a mesma quantidade de avaliações.
- Resumo: média da turma, números de aprovados, alunos em recuperação e reprovados, além da maior e menor média individual.
- Totais e médias são exibidos com duas casas decimais.

Entradas vazias, textos, NaN, infinito, notação científica e notas fora da faixa são recusados. Todos os alunos precisam estar preenchidos para calcular a turma. Ao editar qualquer campo, os resultados anteriores deixam de ser exibidos até novo cálculo. Nomes iguais são permitidos, pois a associação é feita pela posição na turma.

## Estrutura

```text
Controle-de-notas-/
├── MEMORY.md
├── ROADMAP.md
├── README.md
├── main.py
├── testes.py
├── requirements-dev.txt
├── gerar_executavel.ps1
├── .vscode/
│   ├── extensions.json
│   └── launch.json
├── ia/
│   ├── Prompt Python.md
│   └── continue.config.example.yaml
└── dist/
    └── ControleDeNotas.exe
```

Os documentos originais foram preservados na raiz. `dist/`, `build/` e arquivos temporários não são versionados. Para entregar somente o programa, copie o `.exe`; para entregar o trabalho acadêmico, inclua o código e os documentos.

## Estruturas e diretrizes pedagógicas

`alunos` é um vetor de nomes; `notas` é uma matriz cujas linhas correspondem aos mesmos índices do vetor. As dimensões seguem a configuração, sem teto fixo no programa. Entradas inválidas ou vazias são representadas por `None` na matriz, nunca por zero implícito.

Não há definição de classes próprias. Funções organizam validação, cálculos, renderização, configuração, limpeza e encerramento. Laços percorrem a matriz, acumulam notas, contam situações e procuram extremos. Comentários explicam sequência, seleção, repetição e métodos utilitários. Objetos da biblioteca padrão (Tkinter e Decimal) são usados conforme necessário; não há objetos personalizados.

## Testar e gerar o executável

```powershell
python testes.py
powershell -ExecutionPolicy Bypass -File .\gerar_executavel.ps1
```

O script instala a dependência de empacotamento, executa os testes e usa PyInstaller com `--onefile --windowed`. Execute-o no Windows. A opção de política vale somente para essa chamada do PowerShell. O programa em si utiliza apenas a biblioteca padrão. Os testes de interface precisam de uma sessão gráfica com Tkinter.

## Gemini e OpenRouter no VS Code

A extensão **Continue** foi instalada no ambiente de desenvolvimento e consta nas recomendações do projeto. A autenticação nas APIs precisa das chaves pessoais do usuário e não foi realizada. O exemplo `ia/continue.config.example.yaml` contém os dois provedores, sem credenciais.

1. Abra a pasta do projeto no VS Code e acesse a extensão Continue.
2. Abra a configuração YAML pessoal pelo menu de configuração da extensão.
3. Incorpore os blocos de `ia/continue.config.example.yaml`, preservando modelos que você já tiver configurado.
4. Informe os IDs de modelos disponíveis nas suas contas e as chaves obtidas no [Google AI Studio](https://aistudio.google.com/apikey) e no [OpenRouter](https://openrouter.ai/keys), apenas na configuração pessoal. Não grave chaves no repositório.
5. Selecione cada modelo e faça uma pergunta curta para validar o acesso. Disponibilidade, cotas e cobrança dependem do provedor/conta.
6. Para trabalhar no código, forneça ao chat `ia/Prompt Python.md`, o cenário do PDF e `MEMORY.md`; destaque que as quantidades e critérios agora são configuráveis.

A sintaxe dos provedores foi conferida na documentação oficial do Continue para [Gemini](https://docs.continue.dev/customize/model-providers/top-level/gemini) e [OpenRouter](https://docs.continue.dev/customize/model-providers/top-level/openrouter). A conexão só estará validada depois de uma resposta bem-sucedida de cada API.
