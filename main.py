"""Controle de Notas — Programação 2 / UEMG.

Programa procedural: vetor de nomes e matriz de notas com dimensões configuráveis.
Os objetos utilizados são exclusivamente os fornecidos pela biblioteca padrão.
"""

from decimal import Decimal, InvalidOperation, localcontext
import tkinter as tk
from tkinter import messagebox, ttk

QUANTIDADE_ALUNOS = 5
QUANTIDADE_NOTAS = 3
MEDIA_APROVACAO = Decimal("6")
NOTA_MINIMA = Decimal("0")
NOTA_MAXIMA = Decimal("10")

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
        raise ValueError("Informe a nota; o campo não pode ficar vazio.")
    # len conta caracteres, substituindo um contador em um laço.
    if len(texto) > 30:
        raise ValueError("Use no máximo 30 caracteres por nota.")
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
    return valor


def validar_nota(texto):
    valor = converter_decimal(texto)
    if valor < NOTA_MINIMA or valor > NOTA_MAXIMA:
        raise ValueError(f"A nota deve estar entre {NOTA_MINIMA} e {NOTA_MAXIMA}.")
    return valor


def calcular_resultados(nomes, matriz):
    """Validar toda a turma e devolver resultados sem modificar a interface."""
    # len obtém as dimensões, substituindo laços de contagem de elementos.
    if len(nomes) != QUANTIDADE_ALUNOS or len(matriz) != QUANTIDADE_ALUNOS:
        raise ValueError(f"A turma deve conter {QUANTIDADE_ALUNOS} alunos.")
    medias = []
    situacoes = []
    aprovados = 0
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
                # str converte o valor para texto, substituindo formatação manual.
                valor = validar_nota(str(matriz[aluno][avaliacao]))
                total += valor
            media = total / QUANTIDADE_NOTAS
            total_turma += total
            # Seleção: comparar a soma com o limite total evita arredondar a aprovação.
            if total >= MEDIA_APROVACAO * QUANTIDADE_NOTAS:
                situacao = "Aprovado"
                aprovados += 1
            else:
                situacao = "Reprovado"
            if maior is None or media > maior:
                maior = media
            if menor is None or media < menor:
                menor = media
            # append insere no final das listas, substituindo o índice de inserção.
            medias.append(media)
            situacoes.append(situacao)
        media_turma = total_turma / (QUANTIDADE_ALUNOS * QUANTIDADE_NOTAS)
    return {
        "medias": medias,
        "situacoes": situacoes,
        "media_turma": media_turma,
        "aprovados": aprovados,
        "reprovados": QUANTIDADE_ALUNOS - aprovados,
        "maior": maior,
        "menor": menor,
    }


def formatar_media(valor):
    # A formatação limita a exibição a 2 casas; replace localiza o separador.
    # Substituem arredondamento visual e montagem manual do texto em português.
    return f"{valor:.2f}".replace(".", ",")


def invalidar_resultados():
    global resultados_atuais
    resultados_atuais = False
    for indice in range(QUANTIDADE_ALUNOS):
        # configure altera propriedades do widget, encapsulando comandos Tcl/Tk.
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
    for aluno in range(QUANTIDADE_ALUNOS):
        # get lê a variável Tcl; strip remove espaços sem varreduras manuais.
        alunos[aluno] = variaveis_nomes[aluno].get().strip()
        if alunos[aluno] != "":
            nomes_preenchidos += 1
        for avaliacao in range(QUANTIDADE_NOTAS):
            try:
                # get lê o texto atual do campo por meio da variável Tcl.
                valor = validar_nota(variaveis_notas[aluno][avaliacao].get())
                notas[aluno][avaliacao] = valor
                notas_validas += 1
            except ValueError:
                notas[aluno][avaliacao] = None
    # set escreve a variável Tcl e notifica automaticamente o rótulo vinculado.
    estado.set(
        f"{nomes_preenchidos}/{QUANTIDADE_ALUNOS} nomes • "
        f"{notas_validas}/{QUANTIDADE_ALUNOS * QUANTIDADE_NOTAS} notas válidas. "
        "Preencha a turma e clique em Calcular Resultados."
    )


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
        for avaliacao in range(QUANTIDADE_NOTAS):
            try:
                # get recupera o conteúdo da variável associada à entrada.
                validar_nota(variaveis_notas[aluno][avaliacao].get())
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
        rotulos_medias[aluno].configure(text=formatar_media(resultado["medias"][aluno]))
        rotulos_situacoes[aluno].configure(text=situacao, style=f"{situacao}.TLabel")
    for chave in resumo:
        if chave == "aprovados" or chave == "reprovados":
            # str converte a contagem para seus caracteres decimais.
            texto = str(resultado[chave])
        else:
            texto = formatar_media(resultado[chave])
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
    if not 1 <= quantidade_alunos <= 100:
        raise ValueError("Escolha entre 1 e 100 alunos.")
    if not 1 <= quantidade_notas <= 20:
        raise ValueError("Escolha entre 1 e 20 avaliações.")
    minima = converter_decimal(textos[2])
    maxima = converter_decimal(textos[3])
    aprovacao = converter_decimal(textos[4])
    if minima >= maxima:
        raise ValueError("A nota mínima deve ser menor que a máxima.")
    if not minima <= aprovacao <= maxima:
        raise ValueError("A média de aprovação deve estar dentro da faixa de notas.")
    return quantidade_alunos, quantidade_notas, minima, maxima, aprovacao


def abrir_configuracoes():
    # Toplevel cria uma janela filha; transient e grab_set tornam o diálogo modal.
    dialogo = tk.Toplevel(janela)
    dialogo.title("Configurar turma e critérios")
    dialogo.transient(janela)
    dialogo.resizable(False, False)
    dialogo.grab_set()
    painel = ttk.Frame(dialogo, padding=22)
    painel.grid(sticky="nsew")
    campos = []
    definicoes = [
        ("Quantidade de alunos (1 a 100)", QUANTIDADE_ALUNOS),
        ("Avaliações por aluno (1 a 20)", QUANTIDADE_NOTAS),
        ("Nota mínima aceita", NOTA_MINIMA),
        ("Nota máxima aceita", NOTA_MAXIMA),
        ("Média para aprovação", MEDIA_APROVACAO),
    ]
    linha = 0
    for titulo, valor in definicoes:
        # Label/Entry e grid constroem cada linha do formulário de configuração.
        ttk.Label(painel, text=titulo).grid(row=linha, column=0, sticky="w", padx=(0, 20), pady=7)
        entrada = ttk.Entry(painel, width=20)
        entrada.grid(row=linha, column=1, pady=7)
        # str formata o valor; insert coloca o texto; append guarda a referência.
        entrada.insert(0, str(valor))
        campos.append(entrada)
        linha += 1

    def aplicar():
        global QUANTIDADE_ALUNOS, QUANTIDADE_NOTAS, NOTA_MINIMA, NOTA_MAXIMA, MEDIA_APROVACAO
        valores = []
        for campo in campos:
            # get lê o texto; append acrescenta cada entrada à lista de validação.
            valores.append(campo.get())
        try:
            configuracao = validar_configuracao(valores)
        except ValueError as erro:
            # str formata a exceção; showerror apresenta um diálogo de erro nativo.
            messagebox.showerror("Configuração inválida", str(erro), parent=dialogo)
            return
        if configuracao == (QUANTIDADE_ALUNOS, QUANTIDADE_NOTAS, NOTA_MINIMA, NOTA_MAXIMA, MEDIA_APROVACAO):
            # destroy fecha o diálogo quando nada mudou.
            dialogo.destroy()
            return
        # askyesno mostra uma confirmação antes de reiniciar os campos da turma.
        if not messagebox.askyesno("Aplicar configuração", "A alteração iniciará uma turma vazia. Continuar?", parent=dialogo):
            return
        QUANTIDADE_ALUNOS, QUANTIDADE_NOTAS, NOTA_MINIMA, NOTA_MAXIMA, MEDIA_APROVACAO = configuracao
        # destroy libera os controles antigos antes da reconstrução do formulário.
        dialogo.destroy()
        conteudo.destroy()
        criar_interface()

    # Button/grid criam comandos; destroy encerra apenas esta janela de opções.
    ttk.Label(painel, text="As novas regras iniciam uma turma vazia.").grid(row=5, column=0, columnspan=2, pady=12)
    ttk.Button(painel, text="Aplicar", command=aplicar).grid(row=6, column=0, sticky="w")
    ttk.Button(painel, text="Cancelar", command=dialogo.destroy).grid(row=6, column=1, sticky="e")
    # focus_set torna o primeiro campo pronto para digitação.
    campos[0].focus_set()


def criar_interface():
    global janela, estado, conteudo, alunos, notas
    global campos_nomes, campos_notas, variaveis_nomes, variaveis_notas
    global rotulos_medias, rotulos_situacoes, resumo
    alunos, notas = [], []
    campos_nomes, campos_notas = [], []
    variaveis_nomes, variaveis_notas = [], []
    rotulos_medias, rotulos_situacoes, resumo = [], [], {}
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
    # Métodos de configuração encapsulam chamadas ao gerenciador de janelas.
    janela.title("Controle de Notas | Programação 2")
    janela.geometry("1060x660")
    janela.minsize(900, 560)
    # Style controla a renderização nativa dos widgets; theme_names lista temas.
    estilo = ttk.Style(janela)
    # in faz uma busca sequencial pelo tema, substituindo um laço de comparação.
    if "vista" in estilo.theme_names():
        # theme_use aplica o conjunto de regras visuais nativas do Windows.
        estilo.theme_use("vista")
    # configure define atributos compartilhados, evitando configurar cada rótulo.
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 21, "bold"))
    estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10), foreground="#526074")
    estilo.configure("Cabecalho.TLabel", font=("Segoe UI", 10, "bold"))
    estilo.configure("Valor.TLabel", font=("Segoe UI", 22, "bold"))
    estilo.configure("Aprovado.TLabel", foreground="#176138", font=("Segoe UI", 10, "bold"))
    estilo.configure("Reprovado.TLabel", foreground="#a32424", font=("Segoe UI", 10, "bold"))
    estilo.configure("Pendente.TLabel", foreground="#526074")
    estilo.configure("TButton", padding=(12, 7))
    # columnconfigure/rowconfigure distribuem espaço extra; grid posiciona widgets.
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    conteudo = ttk.Frame(janela, padding=24)
    conteudo.grid(row=0, column=0, sticky="nsew")
    conteudo.columnconfigure(0, weight=1)
    conteudo.rowconfigure(2, weight=1)
    # Label cria rótulos; grid associa cada um a uma célula do layout.
    ttk.Label(conteudo, text="Controle de Notas", style="Titulo.TLabel").grid(row=0, column=0, sticky="w")
    ttk.Label(conteudo, text=f"{QUANTIDADE_ALUNOS} alunos · {QUANTIDADE_NOTAS} avaliações · aprovação com média ≥ {MEDIA_APROVACAO}", style="Subtitulo.TLabel").grid(row=1, column=0, sticky="w", pady=(4, 20))
    moldura = ttk.LabelFrame(conteudo, text=" Dados da turma ", padding=6)
    moldura.grid(row=2, column=0, sticky="nsew")
    moldura.columnconfigure(0, weight=1)
    moldura.rowconfigure(0, weight=1)
    # Canvas fornece uma área rolável; Scrollbar delega o deslocamento ao Tk.
    tela = tk.Canvas(moldura, highlightthickness=0, height=255)
    tela.grid(row=0, column=0, sticky="nsew")
    vertical = ttk.Scrollbar(moldura, orient="vertical", command=tela.yview)
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal = ttk.Scrollbar(moldura, orient="horizontal", command=tela.xview)
    horizontal.grid(row=1, column=0, sticky="ew")
    # configure liga a posição das barras à região visível do canvas.
    tela.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    tabela = ttk.Frame(tela, padding=8)
    # create_window incorpora o formulário no canvas para rolagem nos dois eixos.
    item_tabela = tela.create_window((0, 0), window=tabela, anchor="nw")

    def ajustar_rolagem(evento=None):
        # winfo_reqwidth mede a largura necessária; max escolhe a maior largura.
        # itemconfigure ajusta o formulário; bbox calcula o retângulo de rolagem.
        largura = max(tabela.winfo_reqwidth(), tela.winfo_width())
        tela.itemconfigure(item_tabela, width=largura)
        tela.configure(scrollregion=tela.bbox("all"))

    def revelar_campo(evento):
        # winfo obtém posições/dimensões; canvasx/canvasy convertem coordenadas.
        campo = evento.widget
        x, y = campo.winfo_x(), campo.winfo_y()
        largura, altura = tabela.winfo_width(), tabela.winfo_height()
        if x < tela.canvasx(0) or x + campo.winfo_width() > tela.canvasx(tela.winfo_width()):
            # xview_moveto reposiciona a rolagem horizontal pela fração da largura.
            tela.xview_moveto(x / largura)
        if y < tela.canvasy(0) or y + campo.winfo_height() > tela.canvasy(tela.winfo_height()):
            # yview_moveto revela o campo focado pelo teclado na rolagem vertical.
            tela.yview_moveto(y / altura)

    # bind recalcula a região quando o formulário ou a janela mudam de tamanho.
    tabela.bind("<Configure>", ajustar_rolagem)
    tela.bind("<Configure>", ajustar_rolagem)
    tabela.columnconfigure(1, weight=3)
    for coluna in range(2, QUANTIDADE_NOTAS + 2):
        # columnconfigure reparte a largura disponível entre os campos de notas.
        tabela.columnconfigure(coluna, weight=1)
    cabecalhos = ["Nº", "Nome do aluno"]
    for avaliacao in range(QUANTIDADE_NOTAS):
        # append adiciona o cabeçalho de cada avaliação sem um índice manual.
        cabecalhos.append(f"Nota {avaliacao + 1}")
    # extend percorre a lista de títulos e acrescenta cada elemento ao destino.
    cabecalhos.extend(["Média", "Situação"])
    for coluna in range(QUANTIDADE_NOTAS + 4):
        # Label cria o texto e grid posiciona o cabeçalho sem coordenadas fixas.
        ttk.Label(tabela, text=cabecalhos[coluna], style="Cabecalho.TLabel").grid(row=0, column=coluna, sticky="w", padx=6, pady=(0, 8))
    for aluno in range(QUANTIDADE_ALUNOS):
        # StringVar liga texto do formulário ao Tcl; append armazena ao final.
        nome = tk.StringVar(janela)
        variaveis_nomes.append(nome)
        # Label/Entry criam widgets; grid organiza cada linha do formulário.
        ttk.Label(tabela, text=f"{aluno + 1:02d}").grid(row=aluno + 1, column=0, padx=6, pady=9)
        entrada = ttk.Entry(tabela, textvariable=nome, width=28)
        entrada.grid(row=aluno + 1, column=1, sticky="ew", padx=6, pady=9)
        # bind revela automaticamente o campo ao receber foco, inclusive por Tab.
        entrada.bind("<FocusIn>", revelar_campo)
        # append substitui a escrita em um índice de inserção controlado à mão.
        campos_nomes.append(entrada)
        linha_variaveis = []
        linha_campos = []
        for avaliacao in range(QUANTIDADE_NOTAS):
            # StringVar/Entry vinculam o conteúdo digitado ao estado da interface.
            variavel = tk.StringVar(janela)
            entrada_nota = ttk.Entry(tabela, textvariable=variavel, width=9, justify="center")
            # grid delega ao Tk o cálculo de posição e redimensionamento do campo.
            entrada_nota.grid(row=aluno + 1, column=avaliacao + 2, sticky="ew", padx=6, pady=9)
            # bind mantém acessível um campo fora da região visível.
            entrada_nota.bind("<FocusIn>", revelar_campo)
            # append acrescenta as referências à linha sem gerenciar índices livres.
            linha_variaveis.append(variavel)
            linha_campos.append(entrada_nota)
        # append acrescenta cada linha independente à matriz de controles.
        variaveis_notas.append(linha_variaveis)
        campos_notas.append(linha_campos)
        # Label e grid criam/posicionam células de resultado que não são editáveis.
        media = ttk.Label(tabela, text="—", width=8, anchor="center", style="Cabecalho.TLabel")
        media.grid(row=aluno + 1, column=QUANTIDADE_NOTAS + 2, padx=6)
        situacao = ttk.Label(tabela, text="Pendente", width=12, style="Pendente.TLabel")
        situacao.grid(row=aluno + 1, column=QUANTIDADE_NOTAS + 3, padx=6)
        # append guarda rótulos para atualizações futuras sem procurar widgets.
        rotulos_medias.append(media)
        rotulos_situacoes.append(situacao)
    # Frame agrupa widgets; grid e columnconfigure gerenciam layout responsivo.
    painel = ttk.Frame(conteudo)
    painel.grid(row=3, column=0, sticky="ew", pady=(18, 12))
    indicadores = [("media_turma", "Média da turma"), ("aprovados", "Aprovados"), ("reprovados", "Reprovados"), ("maior", "Maior média"), ("menor", "Menor média")]
    coluna = 0
    for chave, titulo in indicadores:
        # columnconfigure e grid distribuem cinco cartões de mesma largura.
        painel.columnconfigure(coluna, weight=1, uniform="indicadores")
        cartao = ttk.LabelFrame(painel, text=f" {titulo} ", padding=10)
        cartao.grid(row=0, column=coluna, sticky="nsew", padx=4)
        resumo[chave] = ttk.Label(cartao, text="—", style="Valor.TLabel")
        resumo[chave].grid(row=0, column=0, sticky="w")
        coluna += 1
    # Label e grid criam uma explicação permanente sobre a precisão dos resultados.
    ttk.Label(conteudo, text=f"Notas de {NOTA_MINIMA} a {NOTA_MAXIMA}; use vírgula ou ponto. Médias exibidas com 2 casas; situação sem arredondamento.", style="Subtitulo.TLabel", wraplength=850).grid(row=4, column=0, sticky="w", pady=(0, 12))
    acoes = ttk.Frame(conteudo)
    acoes.grid(row=5, column=0, sticky="ew")
    acoes.columnconfigure(3, weight=1)
    # Button associa ações a funções; grid posiciona os comandos.
    ttk.Button(acoes, text="Calcular Resultados", command=processar_resultados).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(acoes, text="Limpar", command=limpar_dados).grid(row=0, column=1)
    ttk.Button(acoes, text="Configurar turma", command=abrir_configuracoes).grid(row=0, column=2, padx=8)
    ttk.Button(acoes, text="Sair", command=encerrar).grid(row=0, column=4)
    # StringVar e Label propagam o texto de estado sem reconstruir o rótulo.
    estado = tk.StringVar(janela)
    ttk.Label(conteudo, textvariable=estado, style="Subtitulo.TLabel", wraplength=940).grid(row=6, column=0, sticky="w", pady=(14, 0))
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
