"""Controle de Notas — Programação 2 / UEMG.

Programa procedural: vetor de nomes e matriz de notas com dimensões configuráveis.
Os objetos utilizados são exclusivamente os fornecidos pela biblioteca padrão.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import tkinter as tk
from tkinter import messagebox, ttk

QUANTIDADE_ALUNOS = 5
QUANTIDADE_NOTAS = 3
NOTA_MAXIMA_SISTEMA = Decimal("30")
TOTAL_APROVACAO = Decimal("18")
TOTAL_RECUPERACAO = Decimal("12")

# Paleta única: trocar uma cor aqui mantém a janela e os diálogos consistentes.
CORES = {
    "fundo": "#F3F5EF",
    "superficie": "#FFFFFF",
    "cabecalho": "#DFECE4",
    "texto": "#233D36",
    "secundario": "#536B60",
    "acao": "#2F6B57",
    "acao_hover": "#245442",
    "suave": "#E3EBE2",
    "suave_hover": "#D2E0D3",
    "borda": "#CBD8CE",
    "aprovado": "#246244",
    "recuperacao": "#875611",
    "reprovado": "#A03E44",
    "aprovado_fundo": "#E5F2E9",
    "recuperacao_fundo": "#FFF1D8",
    "reprovado_fundo": "#F8E4E5",
    "previa": "#EAF1EA",
}

# Repetição: construir linhas independentes evita compartilhar a mesma lista.
alunos = ["", "", "", "", ""]
notas = []
for indice in range(QUANTIDADE_ALUNOS):
    # append inclui uma linha no final, substituindo a alocação/indexação manual.
    notas.append([None, None, None])

janela = None
campos_nomes = []
campos_notas = []
variaveis_nomes = []
variaveis_notas = []
rotulos_medias = []
rotulos_totais = []
rotulos_situacoes = []
resumo = {}
estado = None
atualizando = False
resultados_atuais = False
conteudo = None


def converter_decimal(texto):
    """Converter texto decimal finito, sem notação científica ou arredondamento."""
    # strip remove espaços nas extremidades, substituindo duas varreduras.
    texto = texto.strip()
    if texto == "":
        raise ValueError("Informe um valor; o campo não pode ficar vazio.")
    # len conta caracteres, substituindo um contador em um laço.
    if len(texto) > 30:
        raise ValueError("Use no máximo 30 caracteres por valor numérico.")
    # replace percorre o texto trocando vírgulas por pontos, em vez de um laço.
    normalizado = texto.replace(",", ".")
    separadores = 0
    digitos = 0
    # Repetição + seleção: aceitar apenas dígitos e um separador decimal.
    posicao = 0
    for caractere in normalizado:
        if "0" <= caractere <= "9":
            digitos += 1
        elif caractere == ".":
            separadores += 1
        elif caractere == "-" and posicao == 0:
            pass
        else:
            raise ValueError("Use um número decimal, como 7,5 ou 7.5.")
        posicao += 1
    if separadores > 1 or digitos == 0:
        raise ValueError("Informe um número válido, como 7,5 ou 7.5.")
    try:
        # Decimal interpreta os dígitos em base dez sem imprecisão binária.
        valor = Decimal(normalizado)
    except InvalidOperation:
        raise ValueError("Informe um número válido.") from None
    if valor == 0:
        # Decimal("0") elimina o sinal visual de entradas equivalentes a zero, como -0.
        valor = Decimal("0")
    return valor


def validar_nota(texto):
    valor = converter_decimal(texto)
    if valor < 0 or valor > NOTA_MAXIMA_SISTEMA:
        raise ValueError(
            f"Cada nota deve estar entre 0 e {formatar_total(NOTA_MAXIMA_SISTEMA)}. "
            "A soma das notas também não pode ultrapassar a nota máxima do sistema."
        )
    return valor


def calcular_resultados(nomes, matriz):
    """Validar toda a turma e devolver resultados sem modificar a interface."""
    # len obtém as dimensões, substituindo laços de contagem de elementos.
    if len(nomes) != QUANTIDADE_ALUNOS or len(matriz) != QUANTIDADE_ALUNOS:
        raise ValueError(f"A turma deve conter {QUANTIDADE_ALUNOS} alunos.")
    medias = []
    totais = []
    situacoes = []
    aprovados = 0
    recuperacao = 0
    reprovados = 0
    total_turma = Decimal("0")
    maior = None
    menor = None
    # localcontext isola a precisão decimal; 60 dígitos cobrem as entradas de 30.
    with localcontext() as contexto:
        contexto.prec = 60
        # Repetição: cada posição do vetor corresponde à mesma linha da matriz.
        for aluno in range(QUANTIDADE_ALUNOS):
            # strip remove espaços periféricos, substituindo varreduras das bordas.
            if nomes[aluno].strip() == "":
                raise ValueError(f"Informe o nome do aluno {aluno + 1}.")
            # len conta as colunas em vez de incrementar um contador manualmente.
            if len(matriz[aluno]) != QUANTIDADE_NOTAS:
                raise ValueError(f"Cada aluno deve ter {QUANTIDADE_NOTAS} notas.")
            total = Decimal("0")
            for avaliacao in range(QUANTIDADE_NOTAS):
                valor_original = matriz[aluno][avaliacao]
                if isinstance(valor_original, Decimal):
                    # format com "f" preserva números muito pequenos sem notação científica.
                    texto_valor = format(valor_original, "f")
                else:
                    # str aceita números e textos fornecidos por testes ou pela interface.
                    texto_valor = str(valor_original)
                valor = validar_nota(texto_valor)
                total += valor
            if total > NOTA_MAXIMA_SISTEMA:
                raise ValueError(
                    f"O total de {nomes[aluno].strip()} é {formatar_total(total)}, mas a nota máxima "
                    f"do sistema é {formatar_total(NOTA_MAXIMA_SISTEMA)}. Revise as notas desse aluno."
                )
            media = total / QUANTIDADE_NOTAS
            total_turma += total
            # Seleção: a soma total, e não a média, determina a situação do aluno.
            if total >= TOTAL_APROVACAO:
                situacao = "Aprovado"
                aprovados += 1
            elif total >= TOTAL_RECUPERACAO:
                situacao = "Recuperação"
                recuperacao += 1
            else:
                situacao = "Reprovado"
                reprovados += 1
            if maior is None or media > maior:
                maior = media
            if menor is None or media < menor:
                menor = media
            # append insere no final das listas, substituindo o índice de inserção.
            totais.append(total)
            medias.append(media)
            situacoes.append(situacao)
        media_turma = total_turma / (QUANTIDADE_ALUNOS * QUANTIDADE_NOTAS)
    return {
        "totais": totais,
        "medias": medias,
        "situacoes": situacoes,
        "media_turma": media_turma,
        "aprovados": aprovados,
        "recuperacao": recuperacao,
        "reprovados": reprovados,
        "maior": maior,
        "menor": menor,
    }


def formatar_numero(valor):
    """Exibir médias com duas casas e arredondamento escolar convencional."""
    with localcontext() as contexto:
        # len mede a precisão necessária antes de quantize arredondar para centésimos.
        contexto.prec = max(60, len(valor.as_tuple().digits) + 4)
        arredondado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # format com "f" evita notação científica; replace usa a vírgula brasileira.
    return format(arredondado, "f").replace(".", ",")


def formatar_total(valor):
    """Exibir todos os dígitos que podem influenciar a classificação pelo total."""
    # format com "f" evita notação científica e mantém a parte decimal exata.
    texto = format(valor, "f")
    if "." in texto:
        inteira, decimal = texto.split(".", 1)
        # rstrip remove zeros sem valor decisivo; ljust mantém ao menos duas casas.
        decimal = decimal.rstrip("0")
        decimal = decimal.ljust(2, "0")
        texto = f"{inteira}.{decimal}"
    else:
        texto = f"{texto}.00"
    return texto.replace(".", ",")


def invalidar_resultados():
    global resultados_atuais
    resultados_atuais = False
    for indice in range(QUANTIDADE_ALUNOS):
        # configure altera propriedades do widget, encapsulando comandos Tcl/Tk.
        rotulos_totais[indice].configure(text="—")
        rotulos_medias[indice].configure(text="—")
        rotulos_situacoes[indice].configure(text="Pendente", style="Pendente.TLabel")
    for chave in resumo:
        # configure atualiza o texto visível sem reconstruir o widget.
        resumo[chave].configure(text="—")


def atualizar_estado(*argumentos):
    """Espelhar entradas válidas nos vetores e retirar resultados desatualizados."""
    if atualizando:
        return
    invalidar_resultados()
    nomes_preenchidos = 0
    notas_validas = 0
    totais_acima_do_maximo = 0
    for aluno in range(QUANTIDADE_ALUNOS):
        # get lê a variável Tcl; strip remove espaços sem varreduras manuais.
        alunos[aluno] = variaveis_nomes[aluno].get().strip()
        if alunos[aluno] != "":
            nomes_preenchidos += 1
        total_aluno = Decimal("0")
        for avaliacao in range(QUANTIDADE_NOTAS):
            try:
                # get lê o texto atual do campo por meio da variável Tcl.
                valor = validar_nota(variaveis_notas[aluno][avaliacao].get())
                notas[aluno][avaliacao] = valor
                notas_validas += 1
                total_aluno += valor
            except ValueError:
                notas[aluno][avaliacao] = None
        if total_aluno > NOTA_MAXIMA_SISTEMA:
            totais_acima_do_maximo += 1
    # set escreve a variável Tcl e notifica automaticamente o rótulo vinculado.
    mensagem_estado = (
        f"{nomes_preenchidos}/{QUANTIDADE_ALUNOS} nomes • "
        f"{notas_validas}/{QUANTIDADE_ALUNOS * QUANTIDADE_NOTAS} notas válidas. "
        "Preencha a turma e clique em Calcular Resultados."
    )
    if totais_acima_do_maximo > 0:
        mensagem_estado += (
            f" Atenção: {totais_acima_do_maximo} aluno(s) ultrapassa(m) a nota máxima "
            f"de {formatar_total(NOTA_MAXIMA_SISTEMA)}."
        )
    estado.set(mensagem_estado)


def informar_erro(mensagem, campo):
    # showerror abre uma caixa modal nativa, substituindo uma janela manual.
    messagebox.showerror("Verifique os dados", mensagem, parent=janela)
    # focus_set e selection_range direcionam e selecionam o campo a corrigir.
    campo.focus_set()
    campo.selection_range(0, tk.END)


def processar_resultados():
    global resultados_atuais
    # Sequência: atualizar, validar tudo, calcular e somente então exibir.
    atualizar_estado()
    for aluno in range(QUANTIDADE_ALUNOS):
        if alunos[aluno] == "":
            informar_erro(f"Informe o nome do aluno {aluno + 1}.", campos_nomes[aluno])
            return
        total_aluno = Decimal("0")
        for avaliacao in range(QUANTIDADE_NOTAS):
            try:
                # get recupera o conteúdo da variável associada à entrada.
                total_aluno += validar_nota(variaveis_notas[aluno][avaliacao].get())
                if total_aluno > NOTA_MAXIMA_SISTEMA:
                    informar_erro(
                        f"O total parcial de {alunos[aluno]} já é {formatar_total(total_aluno)}, "
                        f"acima da nota máxima do sistema ({formatar_total(NOTA_MAXIMA_SISTEMA)}).",
                        campos_notas[aluno][avaliacao],
                    )
                    return
            except ValueError as erro:
                informar_erro(
                    f"Aluno {aluno + 1} ({alunos[aluno]}), nota {avaliacao + 1}:\n{erro}",
                    campos_notas[aluno][avaliacao],
                )
                return
    try:
        resultado = calcular_resultados(alunos, notas)
    except ValueError as erro:
        # str transforma a exceção em mensagem; showerror cria o diálogo nativo.
        messagebox.showerror("Verifique os dados", str(erro), parent=janela)
        return
    for aluno in range(QUANTIDADE_ALUNOS):
        situacao = resultado["situacoes"][aluno]
        # configure atualiza texto e estilo via Tcl, sem recriar os rótulos.
        rotulos_totais[aluno].configure(text=formatar_total(resultado["totais"][aluno]))
        rotulos_medias[aluno].configure(text=formatar_numero(resultado["medias"][aluno]))
        rotulos_situacoes[aluno].configure(text=situacao, style=f"{situacao}.TLabel")
    for chave in resumo:
        if chave == "aprovados" or chave == "recuperacao" or chave == "reprovados":
            # str converte a contagem para seus caracteres decimais.
            texto = str(resultado[chave])
        else:
            texto = formatar_numero(resultado[chave])
        # configure encaminha a atualização do texto ao widget nativo.
        resumo[chave].configure(text=texto)
    resultados_atuais = True
    # set propaga o estado para o rótulo vinculado, sem atualização manual.
    estado.set(f"Resultados calculados para {QUANTIDADE_ALUNOS} alunos. Editar qualquer campo exige novo cálculo.")


def limpar_dados():
    global atualizando
    possui_dados = False
    for aluno in range(QUANTIDADE_ALUNOS):
        # get lê a variável Tcl, encapsulando o acesso ao conteúdo do formulário.
        if variaveis_nomes[aluno].get() != "":
            possui_dados = True
        for avaliacao in range(QUANTIDADE_NOTAS):
            # get lê a variável Tcl associada a cada nota.
            if variaveis_notas[aluno][avaliacao].get() != "":
                possui_dados = True
    # askyesno implementa um diálogo modal e retorna a escolha do usuário.
    if possui_dados and not messagebox.askyesno(
        "Limpar turma", "Apagar todos os nomes, notas e resultados?", parent=janela
    ):
        return
    atualizando = True
    for aluno in range(QUANTIDADE_ALUNOS):
        # set limpa o conteúdo vinculado sem manipular os caracteres um a um.
        variaveis_nomes[aluno].set("")
        for avaliacao in range(QUANTIDADE_NOTAS):
            # set também aciona os observadores, suspensos pelo sinal atualizando.
            variaveis_notas[aluno][avaliacao].set("")
    atualizando = False
    atualizar_estado()
    # focus_set encaminha a próxima digitação para o primeiro nome.
    campos_nomes[0].focus_set()


def encerrar():
    possui_dados = False
    for aluno in range(QUANTIDADE_ALUNOS):
        # get lê a variável Tcl, inclusive textos ainda inválidos.
        if variaveis_nomes[aluno].get() != "":
            possui_dados = True
        for avaliacao in range(QUANTIDADE_NOTAS):
            # get recupera a nota digitada, sem depender da validação numérica.
            if variaveis_notas[aluno][avaliacao].get() != "":
                possui_dados = True
    # askyesno encapsula a construção do diálogo de confirmação de saída.
    if possui_dados and not messagebox.askyesno(
        "Encerrar", "Os dados ficam apenas nesta sessão. Deseja sair?", parent=janela
    ):
        return
    # destroy libera a janela e seus widgets e encerra o ciclo de eventos.
    janela.destroy()


def validar_configuracao(textos):
    # int interpreta os dígitos e converte para inteiro, sem acumulação manual.
    try:
        quantidade_alunos = int(textos[0])
        quantidade_notas = int(textos[1])
    except ValueError:
        raise ValueError("As quantidades devem ser números inteiros.") from None
    if quantidade_alunos < 1:
        raise ValueError("A turma deve ter pelo menos 1 aluno.")
    if quantidade_notas < 1:
        raise ValueError("Cada aluno deve ter pelo menos 1 avaliação.")
    nota_maxima_sistema = converter_decimal(textos[2])
    total_aprovacao = converter_decimal(textos[3])
    total_recuperacao = converter_decimal(textos[4])
    if nota_maxima_sistema <= 0:
        raise ValueError("A nota máxima do sistema deve ser maior que zero.")
    if total_recuperacao < 0 or total_recuperacao > nota_maxima_sistema:
        raise ValueError(
            "A nota mínima para fazer recuperação deve ficar entre 0 e "
            f"{formatar_total(nota_maxima_sistema)}."
        )
    if total_aprovacao < 0 or total_aprovacao > nota_maxima_sistema:
        raise ValueError(
            "A nota mínima para aprovação deve ficar entre 0 e "
            f"{formatar_total(nota_maxima_sistema)}."
        )
    if total_recuperacao >= total_aprovacao:
        raise ValueError(
            "A nota mínima para fazer recuperação deve ser menor que a nota mínima para aprovação."
        )
    return (
        quantidade_alunos,
        quantidade_notas,
        nota_maxima_sistema,
        total_aprovacao,
        total_recuperacao,
    )


def abrir_configuracoes():
    # Toplevel cria uma janela filha; transient e grab_set tornam o diálogo modal.
    dialogo = tk.Toplevel(janela)
    dialogo.title("Configurar notas e resultados")
    dialogo.transient(janela)
    dialogo.resizable(False, False)
    dialogo.configure(background=CORES["fundo"])
    dialogo.grab_set()
    painel = ttk.Frame(dialogo, padding=28, style="Pagina.TFrame")
    painel.grid(sticky="nsew")
    for coluna in range(4):
        # columnconfigure divide a largura igualmente entre os dois pares de campos.
        painel.columnconfigure(coluna, weight=1)

    valores_iniciais = [
        QUANTIDADE_ALUNOS,
        QUANTIDADE_NOTAS,
        NOTA_MAXIMA_SISTEMA,
        TOTAL_APROVACAO,
        TOTAL_RECUPERACAO,
    ]
    variaveis_configuracao = []
    campos = []
    for valor in valores_iniciais:
        if isinstance(valor, Decimal):
            # format com "f" reabre decimais pequenos sem notação científica.
            texto_inicial = format(valor, "f")
        else:
            # str converte as quantidades inteiras para o campo de texto.
            texto_inicial = str(valor)
        variavel = tk.StringVar(dialogo, value=texto_inicial)
        variaveis_configuracao.append(variavel)

    # Os títulos numerados apresentam a configuração como três passos curtos.
    ttk.Label(painel, text="Configurar notas e resultados", style="DialogoTitulo.TLabel").grid(
        row=0, column=0, columnspan=4, sticky="w"
    )
    ttk.Label(
        painel,
        text="Preencha os três passos. A prévia abaixo mostra exatamente como cada aluno será classificado.",
        style="Subtitulo.TLabel",
        wraplength=650,
    ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 20))

    def adicionar_campo(indice, titulo, linha, coluna):
        # Label e Entry formam um par; grid mantém os campos alinhados.
        ttk.Label(painel, text=titulo, style="Formulario.TLabel").grid(
            row=linha, column=coluna, sticky="w", padx=(0, 8), pady=6
        )
        entrada = ttk.Entry(
            painel,
            textvariable=variaveis_configuracao[indice],
            width=13,
            font=("Segoe UI", 11),
            style="Suave.TEntry",
        )
        entrada.grid(row=linha, column=coluna + 1, sticky="ew", padx=(0, 20), pady=6)
        # append guarda os campos para foco e compatibilidade com a navegação.
        campos.append(entrada)

    ttk.Label(painel, text="1  TAMANHO DA TURMA", style="Secao.TLabel").grid(
        row=2, column=0, columnspan=4, sticky="w", pady=(0, 6)
    )
    adicionar_campo(0, "Quantidade de alunos", 3, 0)
    adicionar_campo(1, "Notas por aluno", 3, 2)
    ttk.Label(
        painel,
        text="Use números inteiros a partir de 1. Todos os alunos terão a mesma quantidade de notas.",
        style="Ajuda.TLabel",
    ).grid(row=4, column=0, columnspan=4, sticky="w", pady=(2, 18))

    ttk.Label(painel, text="2  NOTA MÁXIMA DO SISTEMA", style="Secao.TLabel").grid(
        row=5, column=0, columnspan=4, sticky="w", pady=(0, 6)
    )
    adicionar_campo(2, "Nota máxima do sistema", 6, 0)
    texto_total_possivel = tk.StringVar(dialogo)
    ttk.Label(
        painel,
        textvariable=texto_total_possivel,
        style="DestaqueAjuda.TLabel",
        wraplength=650,
    ).grid(row=7, column=0, columnspan=4, sticky="w", pady=(3, 18))

    ttk.Label(painel, text="3  LIMITES DO RESULTADO", style="Secao.TLabel").grid(
        row=8, column=0, columnspan=4, sticky="w", pady=(0, 6)
    )
    adicionar_campo(3, "Nota mínima para aprovação", 9, 0)
    adicionar_campo(4, "Nota mínima para fazer recuperação", 9, 2)

    previa = ttk.Frame(painel, padding=(14, 12), style="Previa.TFrame")
    previa.grid(row=10, column=0, columnspan=4, sticky="ew", pady=(12, 4))
    previa.columnconfigure(0, weight=1)
    previa.columnconfigure(1, weight=1)
    previa.columnconfigure(2, weight=1)
    ttk.Label(previa, text="PRÉVIA DA CLASSIFICAÇÃO", style="PreviaTitulo.TLabel").grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 9)
    )
    texto_reprovado = tk.StringVar(dialogo)
    texto_recuperacao = tk.StringVar(dialogo)
    texto_aprovado = tk.StringVar(dialogo)
    rotulo_reprovado = ttk.Label(
        previa, textvariable=texto_reprovado, style="FaixaReprovado.TLabel",
        anchor="center", justify="center", wraplength=190
    )
    rotulo_recuperacao = ttk.Label(
        previa, textvariable=texto_recuperacao, style="FaixaRecuperacao.TLabel",
        anchor="center", justify="center", wraplength=190
    )
    rotulo_aprovado = ttk.Label(
        previa, textvariable=texto_aprovado, style="FaixaAprovado.TLabel",
        anchor="center", justify="center", wraplength=190
    )
    rotulo_reprovado.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    rotulo_recuperacao.grid(row=1, column=1, sticky="ew", padx=5)
    rotulo_aprovado.grid(row=1, column=2, sticky="ew", padx=(5, 0))
    mensagem_previa = tk.StringVar(dialogo)
    ttk.Label(previa, textvariable=mensagem_previa, style="PreviaTexto.TLabel", wraplength=620).grid(
        row=2, column=0, columnspan=3, sticky="w", pady=(9, 0)
    )

    def atualizar_previa(*argumentos):
        valores = []
        for variavel in variaveis_configuracao:
            # get lê cada entrada na ordem esperada; append forma a lista de validação.
            valores.append(variavel.get())
        try:
            quantidade_notas = int(valores[1])
            nota_maxima_sistema = converter_decimal(valores[2])
            if quantidade_notas < 1 or nota_maxima_sistema <= 0:
                raise ValueError
            # set atualiza automaticamente o texto associado ao rótulo.
            texto_total_possivel.set(
                f"As {quantidade_notas} nota(s) formam um único total, que pode ir de 0,00 a "
                f"{formatar_total(nota_maxima_sistema)}. A soma não pode ultrapassar esse máximo."
            )
        except (ValueError, InvalidOperation):
            texto_total_possivel.set("Preencha uma quantidade e uma faixa válidas para calcular o total possível.")
        try:
            configuracao = validar_configuracao(valores)
            total_aprovacao = configuracao[3]
            total_recuperacao = configuracao[4]
            texto_reprovado.set(f"Reprovado\nabaixo de {formatar_total(total_recuperacao)}")
            texto_recuperacao.set(
                f"Recuperação\nde {formatar_total(total_recuperacao)} a menos de "
                f"{formatar_total(total_aprovacao)}"
            )
            texto_aprovado.set(f"Aprovado\na partir de {formatar_total(total_aprovacao)}")
            mensagem_previa.set("Configuração válida. A média será mostrada apenas para consulta.")
        except ValueError as erro:
            texto_reprovado.set("Reprovado")
            texto_recuperacao.set("Recuperação")
            texto_aprovado.set("Aprovado")
            # str transforma a exceção em uma explicação legível.
            mensagem_previa.set(f"Revise os valores: {erro}")

    for variavel in variaveis_configuracao:
        # trace_add recalcula a prévia a cada alteração sem esperar o botão Aplicar.
        variavel.trace_add("write", atualizar_previa)
    atualizar_previa()

    def aplicar():
        global QUANTIDADE_ALUNOS, QUANTIDADE_NOTAS, NOTA_MAXIMA_SISTEMA
        global TOTAL_RECUPERACAO, TOTAL_APROVACAO
        valores = []
        for variavel in variaveis_configuracao:
            # get lê o texto; append acrescenta cada entrada à lista de validação.
            valores.append(variavel.get())
        try:
            configuracao = validar_configuracao(valores)
        except ValueError as erro:
            # str formata a exceção; showerror apresenta um diálogo de erro nativo.
            messagebox.showerror("Configuração inválida", str(erro), parent=dialogo)
            return
        configuracao_atual = (
            QUANTIDADE_ALUNOS,
            QUANTIDADE_NOTAS,
            NOTA_MAXIMA_SISTEMA,
            TOTAL_APROVACAO,
            TOTAL_RECUPERACAO,
        )
        if configuracao == configuracao_atual:
            # destroy fecha o diálogo quando nada mudou.
            dialogo.destroy()
            return
        possui_dados = False
        for variavel_nome in variaveis_nomes:
            if variavel_nome.get().strip() != "":
                possui_dados = True
        for linha_variaveis in variaveis_notas:
            for variavel_nota in linha_variaveis:
                if variavel_nota.get().strip() != "":
                    possui_dados = True
        quantidade_campos = configuracao[0] * configuracao[1]
        mensagem_confirmacao = ""
        if possui_dados:
            mensagem_confirmacao = "Os novos critérios apagarão o preenchimento atual e iniciarão uma turma vazia."
        if quantidade_campos > 2000:
            aviso_desempenho = (
                f"Esta configuração criará {quantidade_campos} campos de nota e pode deixar a janela lenta."
            )
            if mensagem_confirmacao:
                mensagem_confirmacao += f"\n\n{aviso_desempenho}"
            else:
                mensagem_confirmacao = aviso_desempenho
        if mensagem_confirmacao:
            # askyesno confirma perda de dados ou uma quantidade de campos muito alta.
            if not messagebox.askyesno(
                "Aplicar configuração",
                f"{mensagem_confirmacao}\n\nDeseja continuar?",
                parent=dialogo,
            ):
                return
        (
            QUANTIDADE_ALUNOS,
            QUANTIDADE_NOTAS,
            NOTA_MAXIMA_SISTEMA,
            TOTAL_APROVACAO,
            TOTAL_RECUPERACAO,
        ) = configuracao
        # destroy libera os controles antigos antes da reconstrução do formulário.
        dialogo.destroy()
        conteudo.destroy()
        criar_interface()

    # Button/grid criam comandos; destroy encerra apenas esta janela de opções.
    botoes = ttk.Frame(painel, style="Pagina.TFrame")
    botoes.grid(row=11, column=0, columnspan=4, sticky="ew", pady=(16, 0))
    botoes.columnconfigure(0, weight=1)
    ttk.Button(botoes, text="Cancelar", command=dialogo.destroy).grid(row=0, column=1, padx=(0, 8))
    ttk.Button(botoes, text="Aplicar e começar turma", command=aplicar, style="Destaque.TButton").grid(row=0, column=2)
    # update_idletasks mede o diálogo pronto para centralizá-lo sobre a janela principal.
    dialogo.update_idletasks()
    posicao_x = janela.winfo_rootx() + (janela.winfo_width() - dialogo.winfo_width()) // 2
    posicao_y = janela.winfo_rooty() + (janela.winfo_height() - dialogo.winfo_height()) // 2
    # max impede que a posição calculada fique fora do canto superior da tela.
    dialogo.geometry(f"+{max(posicao_x, 10)}+{max(posicao_y, 10)}")
    # focus_set torna o primeiro campo pronto para digitação.
    campos[0].focus_set()


def desenhar_retangulo_arredondado(canvas, x1, y1, x2, y2, raio, cor, etiqueta):
    """Desenhar uma superfície arredondada usando um polígono suavizado."""
    pontos = [
        x1 + raio, y1,
        x2 - raio, y1,
        x2, y1,
        x2, y1 + raio,
        x2, y2 - raio,
        x2, y2,
        x2 - raio, y2,
        x1 + raio, y2,
        x1, y2,
        x1, y2 - raio,
        x1, y1 + raio,
        x1, y1,
    ]
    # create_polygon liga os pontos e smooth calcula curvas entre eles,
    # substituindo o desenho manual de quatro arcos e quatro retas.
    return canvas.create_polygon(
        pontos,
        smooth=True,
        splinesteps=24,
        fill=cor,
        outline="",
        tags=etiqueta,
    )


def criar_cartao_arredondado(pai, altura, cor=CORES["superficie"], margem=16, raio=18):
    """Criar um cartão visual que recebe widgets Tkinter em seu interior."""
    canvas = tk.Canvas(
        pai,
        height=altura,
        background=CORES["fundo"],
        highlightthickness=0,
        borderwidth=0,
    )
    area = tk.Frame(canvas, background=cor, borderwidth=0)
    # create_window incorpora o frame no canvas para permitir o fundo arredondado.
    janela_interna = canvas.create_window(margem, margem, window=area, anchor="nw")

    def ajustar_cartao(evento):
        # delete remove somente o fundo anterior, evitando empilhar desenhos.
        canvas.delete("fundo_cartao")
        desenhar_retangulo_arredondado(
            canvas, 1, 1, evento.width - 1, evento.height - 1,
            raio, cor, "fundo_cartao"
        )
        # tag_lower envia o fundo para trás dos widgets incorporados.
        canvas.tag_lower("fundo_cartao")
        # max impede dimensões negativas enquanto a janela está sendo criada.
        largura = max(evento.width - margem * 2, 1)
        altura_interna = max(evento.height - margem * 2, 1)
        # coords e itemconfigure reposicionam e redimensionam a área interna.
        canvas.coords(janela_interna, margem, margem)
        canvas.itemconfigure(janela_interna, width=largura, height=altura_interna)

    # bind redesenha os cantos sempre que o cartão muda de tamanho.
    canvas.bind("<Configure>", ajustar_cartao)
    return canvas, area


def criar_botao_arredondado(
    pai, texto, comando, largura, cor, cor_texto, cor_hover, fundo_pai
):
    """Criar um botão arredondado acessível por mouse, Enter ou Espaço."""
    altura = 40
    botao = tk.Canvas(
        pai,
        width=largura,
        height=altura,
        background=fundo_pai,
        highlightthickness=0,
        borderwidth=0,
        cursor="hand2",
        takefocus=True,
    )
    fundo = desenhar_retangulo_arredondado(
        botao, 1, 1, largura - 1, altura - 1, 13, cor, "fundo_botao"
    )
    # create_text centraliza o título, substituindo cálculos manuais de fonte.
    botao.create_text(
        largura / 2,
        altura / 2,
        text=texto,
        fill=cor_texto,
        font=("Segoe UI", 10, "bold"),
    )

    def executar(evento=None):
        comando()
        return "break"

    def entrar(evento=None):
        # itemconfigure altera a cor do desenho existente durante o foco do mouse.
        botao.itemconfigure(fundo, fill=cor_hover)

    def sair(evento=None):
        botao.itemconfigure(fundo, fill=cor)

    def destacar_foco(evento=None):
        # itemconfigure contorna o botão ao receber foco, tornando o Tab visível.
        cor_foco = CORES["superficie"] if cor == CORES["acao"] else CORES["acao"]
        botao.itemconfigure(fundo, outline=cor_foco, width=2)

    def retirar_foco(evento=None):
        # itemconfigure remove apenas o contorno, mantendo a cor da ação.
        botao.itemconfigure(fundo, outline="", width=0)

    # bind associa clique, teclado e realce sem criar uma classe personalizada.
    botao.bind("<Button-1>", executar)
    botao.bind("<Return>", executar)
    botao.bind("<space>", executar)
    botao.bind("<Enter>", entrar)
    botao.bind("<Leave>", sair)
    botao.bind("<FocusIn>", destacar_foco)
    botao.bind("<FocusOut>", retirar_foco)
    return botao


def criar_interface():
    global janela, estado, conteudo, alunos, notas
    global campos_nomes, campos_notas, variaveis_nomes, variaveis_notas
    global rotulos_totais, rotulos_medias, rotulos_situacoes, resumo
    alunos, notas = [], []
    campos_nomes, campos_notas = [], []
    variaveis_nomes, variaveis_notas = [], []
    rotulos_totais, rotulos_medias, rotulos_situacoes, resumo = [], [], [], {}
    for aluno in range(QUANTIDADE_ALUNOS):
        # append acrescenta posições ao vetor e linhas independentes à matriz.
        alunos.append("")
        linha = []
        for avaliacao in range(QUANTIDADE_NOTAS):
            # append reserva uma posição ainda sem nota na linha atual.
            linha.append(None)
        notas.append(linha)
    if janela is None:
        # Tk cria a janela principal e inicializa o interpretador Tcl/Tk.
        janela = tk.Tk()
        largura_disponivel = max(janela.winfo_screenwidth() - 80, 760)
        altura_disponivel = max(janela.winfo_screenheight() - 110, 580)
        largura_inicial = min(1180, largura_disponivel)
        altura_inicial = min(760, altura_disponivel)
        # geometry adapta a primeira abertura à área útil de telas menores.
        janela.geometry(f"{largura_inicial}x{altura_inicial}+30+24")
        janela.minsize(min(900, largura_inicial), min(620, altura_inicial))
    # Métodos de configuração encapsulam chamadas ao gerenciador de janelas.
    janela.title("Controle de Notas | Programação 2")
    # configure define a cor ao redor do conteúdo, evitando áreas sem acabamento.
    janela.configure(background=CORES["fundo"])
    # Style controla a renderização nativa dos widgets; theme_names lista temas.
    estilo = ttk.Style(janela)
    # clam permite aplicar a mesma paleta clara de forma consistente no Windows.
    if "clam" in estilo.theme_names():
        estilo.theme_use("clam")
    # configure define atributos compartilhados, evitando configurar cada rótulo.
    estilo.configure(".", font=("Segoe UI", 10), foreground=CORES["texto"])
    estilo.configure("Pagina.TFrame", background=CORES["fundo"])
    estilo.configure("Cabecalho.TFrame", background=CORES["cabecalho"])
    estilo.configure(
        "Titulo.TLabel", font=("Segoe UI", 21, "bold"), foreground=CORES["texto"],
        background=CORES["cabecalho"]
    )
    estilo.configure(
        "SubtituloCabecalho.TLabel", font=("Segoe UI", 9), foreground=CORES["secundario"],
        background=CORES["cabecalho"]
    )
    estilo.configure(
        "Criterios.TLabel", font=("Segoe UI", 9, "bold"), foreground=CORES["texto"],
        background=CORES["cabecalho"]
    )
    estilo.configure(
        "Subtitulo.TLabel", font=("Segoe UI", 9), foreground=CORES["secundario"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "DialogoTitulo.TLabel", font=("Segoe UI", 18, "bold"), foreground=CORES["texto"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "Secao.TLabel", font=("Segoe UI", 9, "bold"), foreground=CORES["acao"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "Ajuda.TLabel", font=("Segoe UI", 9), foreground=CORES["secundario"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "DestaqueAjuda.TLabel", font=("Segoe UI", 9, "bold"), foreground=CORES["acao"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "Formulario.TLabel", font=("Segoe UI", 9), foreground=CORES["texto"],
        background=CORES["fundo"]
    )
    estilo.configure(
        "Suave.TEntry", font=("Segoe UI", 10), padding=(9, 4), relief="flat",
        fieldbackground="#FAFCF9", foreground=CORES["texto"], bordercolor=CORES["borda"]
    )
    estilo.map(
        "Suave.TEntry", fieldbackground=[("focus", "#FFFFFF")],
        bordercolor=[("focus", CORES["acao"])]
    )
    estilo.configure("Tabela.TFrame", background=CORES["superficie"])
    estilo.configure("Cartao.TFrame", background=CORES["superficie"])
    estilo.configure(
        "Tabela.TLabel", background=CORES["superficie"], foreground=CORES["texto"],
        font=("Segoe UI", 10)
    )
    estilo.configure(
        "CartaoTitulo.TLabel", background=CORES["superficie"], foreground=CORES["texto"],
        font=("Segoe UI", 13, "bold")
    )
    estilo.configure(
        "CartaoTexto.TLabel", background=CORES["superficie"], foreground=CORES["secundario"],
        font=("Segoe UI", 9)
    )
    estilo.configure(
        "Cabecalho.TLabel", background=CORES["superficie"], foreground=CORES["texto"],
        font=("Segoe UI", 9, "bold")
    )
    estilo.configure(
        "Valor.TLabel", background=CORES["superficie"], foreground=CORES["texto"],
        font=("Segoe UI", 19, "bold")
    )
    estilo.configure(
        "AprovadoValor.TLabel", background=CORES["superficie"], foreground=CORES["aprovado"],
        font=("Segoe UI", 19, "bold")
    )
    estilo.configure(
        "RecuperacaoValor.TLabel", background=CORES["superficie"], foreground=CORES["recuperacao"],
        font=("Segoe UI", 19, "bold")
    )
    estilo.configure(
        "ReprovadoValor.TLabel", background=CORES["superficie"], foreground=CORES["reprovado"],
        font=("Segoe UI", 19, "bold")
    )
    estilo.configure(
        "Aprovado.TLabel", background=CORES["aprovado_fundo"], foreground=CORES["aprovado"],
        font=("Segoe UI", 9, "bold"), padding=(10, 5)
    )
    estilo.configure(
        "Recuperação.TLabel", background=CORES["recuperacao_fundo"], foreground=CORES["recuperacao"],
        font=("Segoe UI", 9, "bold"), padding=(10, 5)
    )
    estilo.configure(
        "Reprovado.TLabel", background=CORES["reprovado_fundo"], foreground=CORES["reprovado"],
        font=("Segoe UI", 9, "bold"), padding=(10, 5)
    )
    estilo.configure(
        "Pendente.TLabel", background="#EEF1ED", foreground=CORES["secundario"],
        font=("Segoe UI", 9), padding=(10, 5)
    )
    estilo.configure("Previa.TFrame", background=CORES["previa"])
    estilo.configure(
        "PreviaTitulo.TLabel", background=CORES["previa"], foreground=CORES["texto"],
        font=("Segoe UI", 9, "bold")
    )
    estilo.configure(
        "FaixaReprovado.TLabel", background=CORES["previa"], foreground=CORES["reprovado"],
        font=("Segoe UI", 9, "bold"), padding=(5, 4)
    )
    estilo.configure(
        "FaixaRecuperacao.TLabel", background=CORES["previa"], foreground=CORES["recuperacao"],
        font=("Segoe UI", 9, "bold"), padding=(5, 4)
    )
    estilo.configure(
        "FaixaAprovado.TLabel", background=CORES["previa"], foreground=CORES["aprovado"],
        font=("Segoe UI", 9, "bold"), padding=(5, 4)
    )
    estilo.configure(
        "PreviaTexto.TLabel", background=CORES["previa"], foreground=CORES["secundario"],
        font=("Segoe UI", 9)
    )
    estilo.configure(
        "TButton", padding=(13, 8), relief="flat", background=CORES["suave"],
        foreground=CORES["texto"], borderwidth=0
    )
    estilo.map("TButton", background=[("active", CORES["suave_hover"]), ("pressed", CORES["borda"])])
    estilo.configure(
        "Destaque.TButton", font=("Segoe UI", 10, "bold"), padding=(15, 9),
        relief="flat", background=CORES["acao"], foreground="#FFFFFF", borderwidth=0
    )
    estilo.map(
        "Destaque.TButton", background=[("active", CORES["acao_hover"]), ("pressed", CORES["texto"])],
        foreground=[("disabled", CORES["borda"]), ("!disabled", "#FFFFFF")]
    )
    # columnconfigure/rowconfigure distribuem espaço extra; grid posiciona widgets.
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    conteudo = ttk.Frame(janela, style="Pagina.TFrame")
    conteudo.grid(row=0, column=0, sticky="nsew")
    conteudo.columnconfigure(0, weight=1)
    conteudo.rowconfigure(1, weight=1)
    # Um cartão arredondado mantém título, regras e configuração no mesmo bloco.
    cabecalho_canvas, cabecalho = criar_cartao_arredondado(
        conteudo, altura=126, cor=CORES["cabecalho"], margem=18, raio=26
    )
    cabecalho_canvas.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 0))
    cabecalho.columnconfigure(0, weight=1)
    ttk.Label(cabecalho, text="Controle de Notas", style="Titulo.TLabel").grid(row=0, column=0, sticky="w")
    subtitulo_cabecalho = ttk.Label(
        cabecalho,
        text=(
            f"{QUANTIDADE_ALUNOS} aluno(s)  •  {QUANTIDADE_NOTAS} nota(s) por aluno  •  "
            f"Nota máxima do sistema: {formatar_total(NOTA_MAXIMA_SISTEMA)}"
        ),
        style="SubtituloCabecalho.TLabel",
    )
    subtitulo_cabecalho.grid(row=1, column=0, sticky="w", pady=(1, 0))
    criterios_cabecalho = ttk.Label(
        cabecalho,
        text=(
            f"Reprovado: abaixo de {formatar_total(TOTAL_RECUPERACAO)}  •  "
            f"Recuperação: de {formatar_total(TOTAL_RECUPERACAO)} até menos de "
            f"{formatar_total(TOTAL_APROVACAO)}  •  "
            f"Aprovado: a partir de {formatar_total(TOTAL_APROVACAO)}"
        ),
        style="Criterios.TLabel",
        justify="left",
    )
    criterios_cabecalho.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
    botao_configurar = criar_botao_arredondado(
        cabecalho,
        "Configurar notas",
        abrir_configuracoes,
        172,
        CORES["superficie"],
        CORES["acao"],
        CORES["suave"],
        CORES["cabecalho"],
    )
    botao_configurar.grid(row=0, column=1, rowspan=2, padx=(24, 0))
    # O formulário ocupa um único cartão branco, sem moldura quadrada externa.
    tabela_canvas, area_tabela = criar_cartao_arredondado(
        conteudo, altura=305, cor=CORES["superficie"], margem=16, raio=24
    )
    tabela_canvas.grid(row=1, column=0, sticky="nsew", padx=22, pady=(12, 0))
    area_tabela.columnconfigure(0, weight=1)
    area_tabela.rowconfigure(2, weight=1)
    ttk.Label(area_tabela, text="1  Preencha os alunos e as notas", style="CartaoTitulo.TLabel").grid(
        row=0, column=0, sticky="w"
    )
    ttk.Label(
        area_tabela,
        text=(
            f"A soma das notas de cada aluno pode chegar a {formatar_total(NOTA_MAXIMA_SISTEMA)}. "
            "Use vírgula ou ponto para valores decimais."
        ),
        style="CartaoTexto.TLabel",
    ).grid(
        row=1, column=0, sticky="w", pady=(2, 9)
    )
    # Canvas fornece uma área rolável; Scrollbar delega o deslocamento ao Tk.
    tela = tk.Canvas(
        area_tabela, highlightthickness=0, height=205, background=CORES["superficie"], borderwidth=0
    )
    tela.grid(row=2, column=0, sticky="nsew")
    vertical = ttk.Scrollbar(area_tabela, orient="vertical", command=tela.yview)
    vertical.grid(row=2, column=1, sticky="ns")
    horizontal = ttk.Scrollbar(area_tabela, orient="horizontal", command=tela.xview)
    horizontal.grid(row=3, column=0, sticky="ew")
    # configure liga a posição das barras à região visível do canvas.
    tela.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    tabela = ttk.Frame(tela, padding=4, style="Tabela.TFrame")
    # create_window incorpora o formulário no canvas para rolagem nos dois eixos.
    item_tabela = tela.create_window((0, 0), window=tabela, anchor="nw")

    def ajustar_rolagem(evento=None):
        # winfo_reqwidth mede a largura necessária; max escolhe a maior largura.
        # itemconfigure ajusta o formulário; bbox calcula o retângulo de rolagem.
        largura_necessaria = tabela.winfo_reqwidth()
        altura_necessaria = tabela.winfo_reqheight()
        largura_visivel = tela.winfo_width()
        altura_visivel = tela.winfo_height()
        largura = max(largura_necessaria, largura_visivel)
        tela.itemconfigure(item_tabela, width=largura)
        tela.configure(scrollregion=tela.bbox("all"))
        if largura_necessaria <= largura_visivel:
            horizontal.grid_remove()
        else:
            horizontal.grid()
        if altura_necessaria <= altura_visivel:
            vertical.grid_remove()
        else:
            vertical.grid()

    def revelar_campo(evento):
        # winfo obtém posições/dimensões; canvasx/canvasy convertem coordenadas.
        campo = evento.widget
        x, y = campo.winfo_x(), campo.winfo_y()
        largura = max(tabela.winfo_width(), 1)
        altura = max(tabela.winfo_height(), 1)
        if x < tela.canvasx(0) or x + campo.winfo_width() > tela.canvasx(tela.winfo_width()):
            # xview_moveto reposiciona a rolagem horizontal pela fração da largura.
            tela.xview_moveto(x / largura)
        if y < tela.canvasy(0) or y + campo.winfo_height() > tela.canvasy(tela.winfo_height()):
            # yview_moveto revela o campo focado pelo teclado na rolagem vertical.
            tela.yview_moveto(y / altura)

    def rolar_tabela(evento):
        # delta informa o sentido da roda; yview_scroll move somente a lista de alunos.
        direcao = -1 if evento.delta > 0 else 1
        tela.yview_scroll(direcao * 3, "units")
        return "break"

    # bind recalcula a região quando o formulário ou a janela mudam de tamanho.
    tabela.bind("<Configure>", ajustar_rolagem)
    tela.bind("<Configure>", ajustar_rolagem)
    tela.bind("<MouseWheel>", rolar_tabela)
    tabela.bind("<MouseWheel>", rolar_tabela)
    tabela.columnconfigure(1, weight=3)
    for coluna in range(2, QUANTIDADE_NOTAS + 2):
        # columnconfigure reparte a largura disponível entre os campos de notas.
        tabela.columnconfigure(coluna, weight=1)
    cabecalhos = ["Nº", "Nome do aluno"]
    for avaliacao in range(QUANTIDADE_NOTAS):
        # append adiciona o cabeçalho de cada avaliação sem um índice manual.
        cabecalhos.append(f"Nota {avaliacao + 1}")
    # extend percorre a lista de títulos e acrescenta cada elemento ao destino.
    cabecalhos.extend(["Total", "Média", "Situação"])
    for coluna in range(QUANTIDADE_NOTAS + 5):
        # Label cria o texto e grid posiciona o cabeçalho sem coordenadas fixas.
        rotulo_cabecalho = ttk.Label(tabela, text=cabecalhos[coluna], style="Cabecalho.TLabel")
        rotulo_cabecalho.grid(row=0, column=coluna, sticky="w", padx=7, pady=(2, 8))
        rotulo_cabecalho.bind("<MouseWheel>", rolar_tabela)
    for aluno in range(QUANTIDADE_ALUNOS):
        # StringVar liga texto do formulário ao Tcl; append armazena ao final.
        nome = tk.StringVar(janela)
        variaveis_nomes.append(nome)
        # Label/Entry criam widgets; grid organiza cada linha do formulário.
        numero_aluno = ttk.Label(tabela, text=f"{aluno + 1:02d}", style="Tabela.TLabel")
        numero_aluno.grid(row=aluno + 1, column=0, padx=7, pady=3)
        numero_aluno.bind("<MouseWheel>", rolar_tabela)
        entrada = ttk.Entry(tabela, textvariable=nome, width=24, style="Suave.TEntry")
        entrada.grid(row=aluno + 1, column=1, sticky="ew", padx=7, pady=3)
        # bind revela automaticamente o campo ao receber foco, inclusive por Tab.
        entrada.bind("<FocusIn>", revelar_campo)
        entrada.bind("<MouseWheel>", rolar_tabela)
        # append substitui a escrita em um índice de inserção controlado à mão.
        campos_nomes.append(entrada)
        linha_variaveis = []
        linha_campos = []
        for avaliacao in range(QUANTIDADE_NOTAS):
            # StringVar/Entry vinculam o conteúdo digitado ao estado da interface.
            variavel = tk.StringVar(janela)
            entrada_nota = ttk.Entry(
                tabela, textvariable=variavel, width=9, justify="center", style="Suave.TEntry"
            )
            # grid delega ao Tk o cálculo de posição e redimensionamento do campo.
            entrada_nota.grid(row=aluno + 1, column=avaliacao + 2, sticky="ew", padx=7, pady=3)
            # bind mantém acessível um campo fora da região visível.
            entrada_nota.bind("<FocusIn>", revelar_campo)
            entrada_nota.bind("<MouseWheel>", rolar_tabela)
            # append acrescenta as referências à linha sem gerenciar índices livres.
            linha_variaveis.append(variavel)
            linha_campos.append(entrada_nota)
        # append acrescenta cada linha independente à matriz de controles.
        variaveis_notas.append(linha_variaveis)
        campos_notas.append(linha_campos)
        # Label e grid criam/posicionam células de resultado que não são editáveis.
        total = ttk.Label(tabela, text="—", anchor="center", style="Cabecalho.TLabel")
        total.grid(row=aluno + 1, column=QUANTIDADE_NOTAS + 2, padx=7)
        total.bind("<MouseWheel>", rolar_tabela)
        media = ttk.Label(tabela, text="—", anchor="center", style="Cabecalho.TLabel")
        media.grid(row=aluno + 1, column=QUANTIDADE_NOTAS + 3, padx=7)
        media.bind("<MouseWheel>", rolar_tabela)
        situacao = ttk.Label(tabela, text="Pendente", width=13, anchor="center", style="Pendente.TLabel")
        situacao.grid(row=aluno + 1, column=QUANTIDADE_NOTAS + 4, padx=7)
        situacao.bind("<MouseWheel>", rolar_tabela)
        # append guarda rótulos para atualizações futuras sem procurar widgets.
        rotulos_totais.append(total)
        rotulos_medias.append(media)
        rotulos_situacoes.append(situacao)
    # Um único cartão de resumo evita seis caixas separadas na tela.
    painel_canvas, painel = criar_cartao_arredondado(
        conteudo, altura=82, cor=CORES["superficie"], margem=10, raio=24
    )
    painel_canvas.grid(row=2, column=0, sticky="ew", padx=22, pady=(12, 7))
    indicadores = [
        ("media_turma", "Média da turma", "Valor.TLabel"),
        ("aprovados", "Aprovados", "AprovadoValor.TLabel"),
        ("recuperacao", "Em recuperação", "RecuperacaoValor.TLabel"),
        ("reprovados", "Reprovados", "ReprovadoValor.TLabel"),
        ("maior", "Maior média", "Valor.TLabel"),
        ("menor", "Menor média", "Valor.TLabel"),
    ]
    coluna = 0
    for chave, titulo, estilo_valor in indicadores:
        # columnconfigure divide o único cartão em seis indicadores equivalentes.
        painel.columnconfigure(coluna, weight=1, uniform="indicadores")
        indicador = ttk.Frame(painel, padding=(10, 3), style="Cartao.TFrame")
        indicador.grid(row=0, column=coluna, sticky="nsew")
        ttk.Label(indicador, text=titulo, style="CartaoTexto.TLabel").grid(row=0, column=0, sticky="w")
        resumo[chave] = ttk.Label(indicador, text="—", style=estilo_valor)
        resumo[chave].grid(row=1, column=0, sticky="w", pady=(3, 0))
        coluna += 1
    # Label e grid criam uma explicação permanente sobre a precisão dos resultados.
    ajuda_principal = ttk.Label(
        conteudo,
        text=(
            f"2  Confira se a soma de cada aluno não passa de {formatar_total(NOTA_MAXIMA_SISTEMA)} e "
            "calcule os resultados. O total define a situação; a média fica disponível para consulta."
        ),
        style="Subtitulo.TLabel",
        justify="left",
    )
    ajuda_principal.grid(row=3, column=0, sticky="w", padx=26, pady=(0, 8))
    acoes = tk.Frame(conteudo, background=CORES["fundo"], borderwidth=0)
    acoes.grid(row=4, column=0, sticky="ew", padx=22)
    acoes.columnconfigure(2, weight=1)
    # Botões em Canvas mantêm as ações principais arredondadas e sem caixas duras.
    botao_calcular = criar_botao_arredondado(
        acoes, "Calcular resultados", processar_resultados, 180,
        CORES["acao"], "#FFFFFF", CORES["acao_hover"], CORES["fundo"]
    )
    botao_calcular.grid(row=0, column=0, padx=(0, 8))
    botao_limpar = criar_botao_arredondado(
        acoes, "Limpar", limpar_dados, 100,
        CORES["suave"], CORES["texto"], CORES["suave_hover"], CORES["fundo"]
    )
    botao_limpar.grid(row=0, column=1)
    botao_sair = criar_botao_arredondado(
        acoes, "Sair", encerrar, 92,
        CORES["suave"], CORES["texto"], CORES["suave_hover"], CORES["fundo"]
    )
    botao_sair.grid(row=0, column=3)
    # StringVar e Label propagam o texto de estado sem reconstruir o rótulo.
    estado = tk.StringVar(janela)
    rotulo_estado = ttk.Label(
        conteudo, textvariable=estado, style="Subtitulo.TLabel", justify="left"
    )
    rotulo_estado.grid(row=5, column=0, sticky="w", padx=26, pady=(9, 13))

    def ajustar_quebras_texto(evento):
        # max mantém uma medida útil; wraplength quebra as frases conforme a janela.
        largura_geral = max(evento.width - 60, 280)
        criterios_cabecalho.configure(wraplength=largura_geral)
        subtitulo_cabecalho.configure(wraplength=max(evento.width - 280, 280))
        ajuda_principal.configure(wraplength=largura_geral)
        rotulo_estado.configure(wraplength=largura_geral)

    conteudo.bind("<Configure>", ajustar_quebras_texto)
    for aluno in range(QUANTIDADE_ALUNOS):
        # trace_add registra observadores, substituindo uma consulta periódica.
        variaveis_nomes[aluno].trace_add("write", atualizar_estado)
        for avaliacao in range(QUANTIDADE_NOTAS):
            # trace_add chama a função a cada edição de uma nota.
            variaveis_notas[aluno][avaliacao].trace_add("write", atualizar_estado)
    # bind registra atalhos; protocol intercepta o botão X para confirmar a saída.
    janela.bind("<Control-Return>", lambda evento: processar_resultados())
    janela.bind("<Control-l>", lambda evento: limpar_dados())
    janela.protocol("WM_DELETE_WINDOW", encerrar)
    atualizar_estado()
    # focus_set direciona o teclado ao primeiro campo na abertura.
    campos_nomes[0].focus_set()
    return janela


def main():
    # Sequência: construir a interface e iniciar o ciclo de eventos.
    criar_interface()
    # mainloop repete a espera e o despacho de eventos até a janela ser destruída.
    janela.mainloop()


if __name__ == "__main__":
    main()
