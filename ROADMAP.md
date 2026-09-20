# ROADMAP — o que está pronto e os próximos passos

Este arquivo é o **mapa de evolução do projeto**. Ele ajuda a equipe a acompanhar o que já funciona, o que ainda depende de uma ação e quais melhorias podem ser desenvolvidas depois.

Para aprender a usar o aplicativo, abra o [README.md](README.md). Para entender as decisões e o código, consulte o [MEMORY.md](MEMORY.md).

## Como ler este planejamento

| Marcação | Significado |
|---|---|
| `[x]` | Recurso concluído |
| `[ ]` | Ação pendente ou ideia ainda não implementada |
| Versão proposta | Agrupamento de melhorias possíveis; não é uma promessa de entrega |

As versões abaixo organizam o trabalho. **Não há datas de entrega definidas para as propostas futuras.**

## Visão rápida

| Etapa | Situação | O que significa para quem usa |
|---|---|---|
| 1.0 — Controle de notas | Implementada | É possível lançar notas, consultar totais e médias e ver a situação de cada aluno |
| Preparação de IA no VS Code | Depende das credenciais pessoais | Gemini e OpenRouter ainda precisam de autenticação e teste |
| 1.1 — Guardar e compartilhar turmas | Proposta | Poder salvar o trabalho e abrir os resultados em uma planilha |
| 1.2 — Mais regras acadêmicas | Proposta | Poder trabalhar com pesos e uma prova de recuperação |

## Versão 1.0 — o que já funciona

### Preencher e configurar

- [x] Abrir o aplicativo em uma janela do Windows.
- [x] Escolher a quantidade de alunos e avaliações, a partir de 1 e sem máximo fixado no código.
- [x] Definir a menor e a maior nota aceita em cada avaliação.
- [x] Definir os totais necessários para recuperação e aprovação.
- [x] Avisar quando faltam dados ou uma nota está fora da faixa permitida.

### Calcular e acompanhar

- [x] Somar as notas e mostrar o total de cada aluno.
- [x] Calcular e mostrar a média individual.
- [x] Usar o total para classificar em **Aprovado**, **Recuperação** ou **Reprovado**.
- [x] Mostrar a média da turma, a maior e a menor média.
- [x] Contar os alunos em cada situação.
- [x] Retirar resultados antigos quando algum campo é editado.

### Usar e entregar

- [x] Organizar a janela com cartões e botões arredondados.
- [x] Permitir rolagem para ver mais alunos e avaliações.
- [x] Limpar a turma e confirmar o descarte de dados.
- [x] Disponibilizar um executável, o arquivo `.exe` que abre com duplo clique.
- [x] Verificar cálculos e ações da janela por testes automáticos.
- [x] Documentar o uso, o planejamento e as decisões do projeto.
- [x] Preservar as diretrizes pedagógicas em `ia/Prompt Python.md`.

> O aplicativo atual guarda o preenchimento apenas enquanto está aberto. Salvar turmas em arquivo é uma proposta da próxima etapa.

## Pendência do ambiente de programação

- [x] Instalar a extensão Continue no ambiente de desenvolvimento.
- [x] Preparar um exemplo de configuração para Gemini e OpenRouter.
- [ ] Informar os modelos e as chaves pessoais na configuração do Continue.
- [ ] Fazer uma pergunta de teste e receber uma resposta de cada serviço.

Essa pendência se refere à ajuda de IA dentro do VS Code. O aplicativo de notas já funciona sem essas conexões. O passo a passo está no [README.md](README.md).

## Versão 1.1 — guardar e compartilhar turmas

**Objetivo proposto:** permitir que a pessoa feche o programa e continue o trabalho depois.

| Melhoria ainda não implementada | Benefício | Como confirmar que ficou pronta |
|---|---|---|
| Salvar e abrir uma turma | Recuperar nomes, notas e critérios em outra sessão | Salvar uma turma, fechar, abrir de novo e conferir os mesmos dados |
| Exportar os resultados em CSV | Abrir a tabela em um programa de planilhas | Comparar nomes, totais, médias e situações do arquivo com os da tela |
| Lembrar a última configuração | Evitar repetir a configuração a cada abertura | Reabrir o programa e encontrar os critérios escolhidos anteriormente |

**CSV** é um arquivo de texto que organiza os dados em linhas e colunas e pode ser aberto em programas como Excel.

Essas melhorias são sugestões. O formato dos arquivos e o local de armazenamento precisarão ser definidos antes da implementação.

## Versão 1.2 — mais regras acadêmicas

**Objetivo proposto:** atender disciplinas que tenham critérios diferentes dos atuais.

| Melhoria ainda não implementada | Exemplo de uso | Decisão necessária antes de programar |
|---|---|---|
| Pesos diferentes nas avaliações | Uma prova contribuir mais que um trabalho | Definir como os pesos afetam o total e a média |
| Prova de recuperação e nova nota final | Reavaliar um aluno após uma prova extra | Definir a fórmula e os critérios para a situação final |
| Nome da disciplina, turma e período | Identificar melhor cada conjunto de notas | Definir quais informações serão obrigatórias |

O sistema atual já indica quem está em recuperação. **Ele ainda não recebe uma prova extra nem calcula uma nota final após essa prova.**

## Como manter este arquivo útil

1. Antes de começar uma melhoria, descreva o problema que ela resolve.
2. Defina um exemplo do resultado esperado e como conferir se funciona.
3. Depois de implementar e verificar, marque o item como concluído.
4. Atualize o [README.md](README.md) com as instruções de uso e o [MEMORY.md](MEMORY.md) com as decisões tomadas.
5. Quando houver alteração no programa, gere novamente o executável para distribuir a versão atualizada.

Uma ideia só deve aparecer como concluída quando estiver disponível no programa e tiver sido verificada.
