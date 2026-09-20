# Controle de Notas — guia para começar

Este programa ajuda a registrar as notas de uma turma e descobrir quem está **aprovado, em recuperação ou reprovado**. Ele abre em uma janela no Windows e permite escolher a quantidade de alunos, quantas notas cada um terá, a nota máxima do sistema e as notas mínimas para aprovação e recuperação.

**A situação do aluno depende da soma das notas.** A média também aparece na tela para facilitar a consulta. Você não precisa saber programar para usar o aplicativo.

## Escolha por onde começar

| Quero… | Onde encontro |
|---|---|
| Abrir o programa e lançar notas | [Primeiro uso](#primeiro-uso-em-5-passos) |
| Conhecer a organização da janela | [Uma tela mais acolhedora](#uma-tela-mais-acolhedora) |
| Entender total, média e situação | [Exemplo completo](#um-exemplo-para-entender-os-resultados) |
| Mudar os critérios da turma | [Configurações](#como-configurar-a-turma) |
| Resolver uma dúvida de uso | [Dúvidas frequentes](#dúvidas-frequentes) |
| Estudar ou alterar o código | [Guia de desenvolvimento](#para-quem-vai-estudar-ou-alterar-o-programa) |
| Saber o que está pronto e o que pode vir depois | [ROADMAP.md](ROADMAP.md) |
| Entender as decisões tomadas no projeto | [MEMORY.md](MEMORY.md) |

## Primeiro uso em 5 passos

1. Abra a pasta `dist` e dê dois cliques em **ControleDeNotas.exe**. Esse é o arquivo que inicia o programa. O executável fornecido é para Windows de 64 bits e não exige Python instalado.
2. Clique em **Configurar notas** se precisar mudar a quantidade de alunos, o número de notas, a nota máxima do sistema ou as notas mínimas. A própria janela mostra uma prévia das três situações.
3. Digite o nome e todas as notas de cada aluno. Você pode escrever `7,5` ou `7.5`: as duas formas são aceitas.
4. Clique em **Calcular resultados**. Cada linha mostrará o total, a média e a situação do aluno. O painel abaixo apresenta o resumo da turma.
5. Para começar outro preenchimento com as mesmas regras, clique em **Limpar** e confirme.

> Os dados ficam guardados somente enquanto o programa está aberto. Ao sair, nomes, notas e configurações não são salvos. Aplicar uma mudança nas configurações inicia uma turma vazia; quando já existe preenchimento, o programa pede confirmação antes de apagar.

Se a pasta `dist` ainda não estiver disponível, use o código Python ou gere o executável seguindo as instruções de desenvolvimento mais abaixo.

## Uma tela mais acolhedora

O fundo creme claro e o cabeçalho verde sálvia deixam a janela mais suave. Os cantos arredondados e os campos mais espaçosos ajudam a encontrar onde digitar e onde consultar os resultados.

- **Comece pelo cabeçalho:** ele apresenta a turma, a nota máxima, as três faixas de resultado e o acesso às configurações.
- **Preencha a área central:** cada aluno ocupa uma linha, com nome, notas e resultados.
- **Confira o resumo abaixo:** ele reúne as médias e a quantidade de alunos em cada situação.
- **Use o teclado se preferir:** `Tab` passa entre os controles; um contorno indica o botão selecionado, que pode ser acionado com `Enter` ou `Espaço`.

O tamanho inicial da janela se adapta à tela do computador. As barras de rolagem permitem acessar alunos e avaliações que não couberem na área visível.

## Um exemplo para entender os resultados

Imagine três notas, uma **nota máxima de 30 pontos no sistema**, recuperação a partir de **12 pontos no total** e aprovação a partir de **18 pontos no total**.

| Aluno | Nota 1 | Nota 2 | Nota 3 | Total | Média | Situação |
|---|---:|---:|---:|---:|---:|---|
| Ana | 8 | 7 | 9 | 24 | 8,00 | Aprovado |
| Bruno | 4 | 5 | 6 | 15 | 5,00 | Recuperação |
| Carla | 2 | 3 | 4 | 9 | 3,00 | Reprovado |

Para Ana, o programa faz estas contas:

```text
Total = 8 + 7 + 9 = 24 pontos
Média = 24 ÷ 3 = 8,00
Situação = Aprovado, pois o total 24 é maior ou igual a 18
```

Os limites também contam: **12 pontos já dão direito à recuperação e 18 pontos já aprovam**. Um total abaixo de 12 reprova; de 12 até menos de 18 fica em recuperação.

Para experimentar essa tabela no aplicativo, configure **3 alunos**. Se mantiver os 5 alunos iniciais, será necessário preencher os cinco antes de calcular.

Nesse exemplo, o resumo terá 1 aprovado, 1 em recuperação, 1 reprovado, média da turma de **5,33**, maior média de **8,00** e menor média de **3,00**. A média da turma é a média das médias individuais, pois todos têm a mesma quantidade de avaliações.

## Como configurar a turma

Abra **Configurar notas** e preencha:

| Campo | O que significa | Valor inicial |
|---|---|---:|
| Quantidade de alunos | Quantas linhas serão preenchidas | 5 |
| Notas por aluno | Quantos campos de nota cada aluno terá | 3 |
| Nota máxima do sistema | Maior total que um aluno pode alcançar | 30 |
| Nota mínima para aprovação | Total a partir do qual o aluno é aprovado | 18 |
| Nota mínima para fazer recuperação | Total a partir do qual o aluno entra em recuperação | 12 |

As quantidades aceitam números inteiros a partir de **1**, sem máximo rígido no código. Turmas maiores exigem mais memória e processamento. Se uma configuração criar mais de 2.000 campos de nota, o programa avisa que a janela pode ficar lenta e permite cancelar antes de construí-la.

A configuração segue esta ordem:

```text
0 ≤ nota mínima para recuperação
nota mínima para recuperação < nota mínima para aprovação
nota mínima para aprovação ≤ nota máxima do sistema
```

Cada nota digitada deve ficar entre zero e a nota máxima do sistema. Além disso, a **soma das notas de um aluno não pode ultrapassar a nota máxima**. Por exemplo, com nota máxima 100, quatro notas `20 + 15 + 30 + 25` formam um total válido de 90. O total `40 + 30 + 20 + 20 = 110` é recusado.

A prévia da configuração atualiza enquanto você digita. Ela mostra claramente os intervalos de reprovação, recuperação e aprovação. A quantidade de notas muda apenas o número de campos e o cálculo da média; a nota máxima e as duas notas mínimas continuam sendo os valores definidos por você.

## Botões, atalhos e avisos

| Ação | Como fazer | O que acontece |
|---|---|---|
| Calcular | **Calcular resultados** ou `Ctrl + Enter` | Confere o preenchimento e mostra os resultados |
| Limpar | **Limpar** ou `Ctrl + L` | Apaga nomes, notas e resultados após confirmação; mantém os critérios |
| Mudar as regras | **Configurar notas** | Permite definir uma nova turma e mostra uma prévia das situações |
| Passar ao próximo campo | `Tab` | Move o cursor entre os controles |
| Ver campos fora da tela | Barras de rolagem | Mostra mais alunos ou avaliações |
| Fechar | **Sair** ou o `X` da janela | Pede confirmação quando há dados preenchidos |

Se faltar um nome ou uma nota estiver incorreta, o programa mostra uma mensagem e direciona o cursor para o campo que precisa de correção. O contador de preenchimento ajuda a acompanhar o que já foi informado.

## Dúvidas frequentes

**Por que os resultados desapareceram quando editei uma nota?**

Eles são retirados para evitar mostrar um resultado antigo. Clique em **Calcular resultados** novamente após terminar a edição.

**Preciso preencher todas as linhas?**

Sim. Se você tiver dois alunos, configure a turma com dois. Um campo vazio não é interpretado como zero; quando a nota for zero, digite `0`.

**Posso colocar dois alunos com o mesmo nome?**

Sim. O programa identifica cada aluno pela sua linha na turma.

**A média é usada para aprovar?**

A decisão usa o **total**. A média permanece na tela como informação: total dividido pela quantidade de avaliações.

**O programa calcula a nota depois de uma prova de recuperação?**

Ainda não. Ele identifica quem está em recuperação. Uma prova extra e uma nova nota final são possibilidades futuras, descritas no [planejamento](ROADMAP.md).

**Quais notas são aceitas?**

Números de zero até a nota máxima do sistema, com vírgula ou ponto decimal. A soma do aluno também precisa respeitar essa nota máxima. Campos vazios, valores negativos, palavras, infinito e formatos como `1e2` são recusados. Cada entrada numérica pode ter até 30 caracteres.

**O arredondamento muda a situação?**

Não. A situação usa o total exato, e a coluna **Total** mantém todos os dígitos que podem influenciar a classificação. Assim, `17,999` continua visível como `17,999` e não parece ter alcançado 18. As médias são apenas informativas e aparecem com duas casas decimais, usando o arredondamento escolar comum: `6,125` aparece como `6,13`.

## Para quem vai estudar ou alterar o programa

O projeto foi desenvolvido para Programação 2 da UEMG, Unidade Carangola. A equipe indicada no enunciado é formada por Gabriel da Silva, Samuel Pedrosa e Davi Gomes.

O código segue o estilo **procedural**: funções dividem o trabalho em tarefas, como validar uma nota, calcular os resultados e montar a janela. A explicação das estruturas e das decisões está no [MEMORY.md](MEMORY.md).

### Conheça os arquivos

| Arquivo | Para que serve |
|---|---|
| [main.py](main.py) | Contém o programa e a interface de janela |
| [testes.py](testes.py) | Verifica automaticamente cálculos e ações da interface |
| [README.md](README.md) | Este guia de uso e primeiros passos |
| [ROADMAP.md](ROADMAP.md) | Mostra o que está pronto, pendente ou proposto |
| [MEMORY.md](MEMORY.md) | Explica as decisões para quem continuar o projeto |
| [ia/Prompt Python.md](ia/Prompt%20Python.md) | Guarda as diretrizes pedagógicas originais |
| [ia/continue.config.example.yaml](ia/continue.config.example.yaml) | Exemplo de configuração dos serviços de IA no VS Code |
| [gerar_executavel.ps1](gerar_executavel.ps1) | Gera o arquivo `.exe` para Windows |
| [requirements-dev.txt](requirements-dev.txt) | Indica a ferramenta necessária para gerar o `.exe` |
| `.vscode/` | Configurações de execução e extensões sugeridas para o VS Code |
| `dist/ControleDeNotas.exe` | Programa pronto para abrir com duplo clique, quando gerado |

O PDF do enunciado e o prompt original também foram preservados na raiz do projeto. A pasta `dist` não é incluída automaticamente no Git, a ferramenta que registra as versões do código.

### Executar pelo código

É necessário ter Python com suporte a Tkinter, a biblioteca que desenha a janela. No VS Code, abra a pasta do projeto e vá ao menu **Terminal → Novo Terminal**. Execute:

```powershell
python main.py
```

Também há uma configuração para executar com `F5`, chamada **Controle de Notas (Tkinter)**. O aplicativo funciona sem internet, sem chaves de IA e sem instalar pacotes adicionais para o uso comum.

### Conferir o funcionamento e gerar o executável

No terminal, dentro da pasta do projeto:

```powershell
python testes.py
```

Esse comando verifica os totais, as médias, as situações e operações da interface. Se tudo passar, aparece uma mensagem começando com `OK`. É necessária uma sessão com interface gráfica para os testes de janela.

Para criar ou atualizar o executável no Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\gerar_executavel.ps1
```

O script prepara a ferramenta PyInstaller, executa os testes e gera `dist/ControleDeNotas.exe`. PyInstaller reúne o programa e os componentes necessários em um arquivo executável. A instalação da ferramenta pode precisar de internet; a opção `ExecutionPolicy Bypass` vale apenas para essa chamada do PowerShell.

Após alterar o código, gere o `.exe` novamente para que ele contenha as mudanças. Para entregar apenas o aplicativo, copie o `.exe`; para entregar o trabalho acadêmico, inclua também o código e a documentação.

### IA no VS Code: Gemini e OpenRouter

Esses serviços ajudam durante a programação. O aplicativo de notas funciona independentemente deles.

A extensão **Continue** foi instalada no ambiente de desenvolvimento e existe um [exemplo de configuração](ia/continue.config.example.yaml). A conexão às duas APIs ainda depende das chaves pessoais do usuário e de uma chamada de teste bem-sucedida. **API** é a forma de um programa se comunicar com um serviço; a **chave de API** identifica o acesso da sua conta.

1. Abra a extensão Continue no VS Code e acesse sua configuração pessoal em YAML, um arquivo de texto com opções organizadas.
2. Acrescente os blocos do exemplo, preservando os modelos que você já utiliza.
3. Substitua os textos `SUBSTITUA_...` pelos identificadores dos modelos disponíveis na sua conta e pelas chaves pessoais do [Google AI Studio](https://aistudio.google.com/apikey) e do [OpenRouter](https://openrouter.ai/keys).
4. Guarde as chaves somente na configuração pessoal. Não as coloque nos arquivos compartilhados do projeto.
5. Selecione cada modelo e faça uma pergunta curta para confirmar que os dois acessos funcionam.
6. Ao pedir ajuda com o código, forneça `ia/Prompt Python.md` e `MEMORY.md` como contexto, além do cenário do trabalho.

Para consultar a configuração de cada serviço, use a documentação do Continue para [Gemini](https://docs.continue.dev/customize/model-providers/top-level/gemini) e [OpenRouter](https://docs.continue.dev/customize/model-providers/top-level/openrouter). Modelos disponíveis, limites de uso e cobrança dependem de cada conta.
