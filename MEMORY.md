# Memória de trabalho

## Objetivo e fontes

Construir o Sistema de Controle de Notas descrito em `Trabalho_Programacao_2_Controle_de_Notas_Final.pdf`, seguindo as diretrizes de `ia/Prompt Python.md`: Python procedural, Tkinter/ttk nativo, validação com messagebox e explicação pedagógica de utilitários.

**Orientações posteriores do usuário:** a quantidade de alunos e avaliações não deve ficar presa ao PDF nem possuir um máximo programado. A interface permite qualquer quantidade inteira a partir de 1, sujeita apenas aos recursos do computador. A faixa das avaliações e os totais para recuperação e aprovação são configuráveis. A situação é definida pela soma total; a média permanece como informação. A interface foi simplificada com cartões arredondados e menos áreas delimitadas.

## Arquitetura

- `main.py`: aplicação inteira, organizada em funções, sem classes próprias.
- Vetor `alunos` e matriz `notas`: estado da turma, associado pelo índice do aluno.
- Configuração global: quantidades, faixa de cada nota, total para recuperação e total para aprovação.
- `converter_decimal`, `validar_nota`, `validar_configuracao`: validação de entradas.
- `calcular_resultados`: cálculo independente dos widgets, sem mutação dos argumentos; lê os critérios globais.
- `atualizar_estado`: observadores das entradas sincronizam o estado e invalidam resultados antigos.
- `criar_interface`: construção/reconstrução dos controles e da área com rolagem.
- `abrir_configuracoes`: diálogo de configuração; aplicar alterações reinicia a turma após confirmação.
- `processar_resultados`, `limpar_dados`, `encerrar`: ações do usuário.

## Decisões

1. Notas de peso igual e três situações: Aprovado, Recuperação e Reprovado. A soma total classifica; a média continua sendo calculada e exibida. Frequência e prova final de recuperação não fazem parte da regra atual.
2. Decimal e precisão de 60 dígitos nos cálculos para evitar erros binários. Entradas limitadas a 30 caracteres.
3. Aprovação e recuperação comparam diretamente a soma das avaliações com os totais configurados, antes de qualquer formatação.
4. Formulário exige todos os alunos configurados; reduzir a turma é feito em Configurar turma.
5. Não existe teto programado para alunos ou avaliações. Ambos devem ser inteiros a partir de 1; memória e desempenho do computador são os limites práticos.
6. Dados/configurações somente em memória. Não há persistência, integração de IA no aplicativo ou banco de dados.
7. Aplicativo sem dependências externas em tempo de execução. PyInstaller apenas para distribuição Windows.
8. Mudanças de configuração limpam a turma com confirmação; alteração de entrada invalida os resultados imediatamente.

## Verificação e ambiente

`python testes.py` cobre classificação pela nota total, cálculo e exibição da média, três situações, limites exatos, extremos, entradas inválidas, quantidades sem teto artificial, critérios variáveis, GUI, reconfiguração e limpeza. O teste também impede a introdução de definição de classes em `main.py`. Reexecutar após alterar regras ou interface e reconstruir o `.exe` para manter a distribuição sincronizada.

Ambiente desta implementação: Python 3.13.0 no Windows, PyInstaller 6.22.3. As versões mencionadas no PDF descrevem a comprovação anterior da equipe, não o runtime aqui utilizado.

Verificação realizada em 19/09/2026: suíte `testes.py` aprovada; criação de formulário 100 × 20 e independência das linhas da matriz verificadas; janela com resultados inspecionada visualmente. Executável `dist/ControleDeNotas.exe` gerado e iniciado no Windows, com título da janela confirmado e encerramento normal com código 0. Não foi testado em outro computador.

Revisão visual e funcional posterior em 19/09/2026: adicionadas as faixas de recuperação e reprovação, removidos os tetos programados de quantidade e adotado o layout com cartões e botões arredondados. A suíte foi aprovada novamente, a nova janela foi inspecionada por captura e o executável reconstruído abriu e encerrou com código 0.

Revisão da regra de classificação em 19/09/2026: a situação passou a usar diretamente a nota total configurável; a média foi mantida como informação individual e da turma. A coluna Total foi inspecionada visualmente, os testes da nova regra foram aprovados e o executável atualizado abriu e encerrou normalmente com código 0.

Continue 2.0.0 instalado no VS Code. Modelos, credenciais e chamadas de teste Gemini/OpenRouter dependem do usuário; não declarar integração autenticada antes da verificação com as duas APIs.

## Continuidade

Manter o prompt original intacto, preservar a organização procedural e atualizar README/ROADMAP ao implementar novos recursos. Qualquer persistência futura deve explicitar onde os dados são salvos e tratar erros de leitura/escrita. Nunca incluir chaves de APIs em commits.
