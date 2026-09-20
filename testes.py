"""Verificações procedurais: execute python testes.py (inclui Tkinter)."""

from decimal import Decimal
from unittest.mock import patch
import ast
from pathlib import Path
import main as app


def deve_falhar(funcao, *argumentos):
    try:
        funcao(*argumentos)
    except ValueError:
        return
    raise AssertionError(f"Entrada deveria ser recusada: {argumentos}")


def executar():
    # ast.parse interpreta a sintaxe; walk percorre todos os nós sem laço recursivo manual.
    arvore = ast.parse(Path("main.py").read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        assert not isinstance(no, ast.ClassDef), "Não criar classes no projeto procedural."
    assert app.validar_nota(" 7,5 ") == Decimal("7.5")
    assert app.validar_nota("0") == 0
    assert app.validar_nota("-0") == Decimal("0")
    assert app.validar_nota("30") == 30
    for entrada in ["", " ", "nan", "Infinity", "-1", "30.01", "1e2", "1,2.3", "abc", ".", "-", "1_0"]:
        deve_falhar(app.validar_nota, entrada)
    nomes = ["Ana", "Bia", "Caio", "Davi", "Eva"]
    matriz = [[6, 6, 6], [0, 0, 0], [10, 10, 10], [5, 6, 7], [5, 5, 5]]
    resultado = app.calcular_resultados(nomes, matriz)
    assert resultado["totais"] == [18, 0, 30, 18, 15]
    assert resultado["medias"] == [6, 0, 10, 6, 5]
    assert resultado["aprovados"] == 3
    assert resultado["recuperacao"] == 1
    assert resultado["reprovados"] == 1
    assert resultado["aprovados"] + resultado["recuperacao"] + resultado["reprovados"] == len(nomes)
    assert resultado["media_turma"] == Decimal("5.4")
    assert resultado["maior"] == 10 and resultado["menor"] == 0
    matriz[0] = ["3.9999", "3.9999", "3.9999"]
    resultado_preciso = app.calcular_resultados(nomes, matriz)
    assert resultado_preciso["situacoes"][0] == "Reprovado"
    assert app.formatar_total(resultado_preciso["totais"][0]) == "11,9997"
    matriz[0] = ["5.9999", "5.9999", "5.9999"]
    resultado_preciso = app.calcular_resultados(nomes, matriz)
    assert resultado_preciso["situacoes"][0] == "Recuperação"
    assert app.formatar_total(resultado_preciso["totais"][0]) == "17,9997"
    matriz[0] = ["4", "4", "4"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Recuperação"
    matriz[0] = ["6", "6", "6"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Aprovado"
    matriz[0] = [app.Decimal("0.0000001"), 0, 0]
    assert app.calcular_resultados(nomes, matriz)["totais"][0] == app.Decimal("0.0000001")
    matriz[0] = [20, 20, 0]
    deve_falhar(app.calcular_resultados, nomes, matriz)
    assert app.formatar_numero(Decimal("6.125")) == "6,13"
    deve_falhar(app.calcular_resultados, [], [])
    for dados in [
        ["0", "3", "30", "18", "12"],
        ["5", "0", "30", "18", "12"],
        ["5", "3", "0", "0", "0"],
        ["5", "3", "30", "31", "12"],
        ["5", "3", "30", "18", "-1"],
        ["5", "3", "30", "18", "18"],
        ["5", "3", "30", "12", "18"],
        ["5.5", "3", "30", "18", "12"],
    ]:
        deve_falhar(app.validar_configuracao, dados)
    # Uma quantidade grande comprova que não existe o teto artificial anterior.
    sem_limite_programado = app.validar_configuracao(["1001", "25", "100", "60", "40"])
    assert sem_limite_programado[0] == 1001 and sem_limite_programado[1] == 25
    zero_normalizado = app.validar_configuracao(["1", "1", "30", "18", "-0"])
    assert zero_normalizado[4] == 0 and app.formatar_total(zero_normalizado[4]) == "0,00"
    nova = app.validar_configuracao(["2", "4", "100", "70", "50"])
    (
        app.QUANTIDADE_ALUNOS,
        app.QUANTIDADE_NOTAS,
        app.NOTA_MAXIMA_SISTEMA,
        app.TOTAL_APROVACAO,
        app.TOTAL_RECUPERACAO,
    ) = nova
    resultado = app.calcular_resultados(["A", "B"], [[20, 20, 20, 20], [15, 15, 15, 15]])
    assert resultado["medias"] == [20, 15]
    assert resultado["media_turma"] == Decimal("17.5")
    assert resultado["aprovados"] == 1
    assert resultado["recuperacao"] == 1
    # patch troca diálogos por respostas determinísticas durante os testes de GUI.
    with patch.object(app.messagebox, "showerror") as erro, patch.object(app.messagebox, "askyesno", return_value=True):
        raiz = app.criar_interface()
        raiz.withdraw()
        raiz.update()
        app.processar_resultados()
        assert erro.call_count == 1
        for aluno in range(2):
            app.variaveis_nomes[aluno].set(f"Aluno {aluno + 1}")
            for avaliacao in range(4):
                app.variaveis_notas[aluno][avaliacao].set("20" if aluno == 0 else "15")
        app.processar_resultados()
        assert app.resultados_atuais
        assert app.rotulos_totais[0].cget("text") == "80,00"
        assert app.rotulos_totais[1].cget("text") == "60,00"
        assert app.resumo["media_turma"].cget("text") == "17,50"
        assert app.rotulos_situacoes[0].cget("text") == "Aprovado"
        assert app.rotulos_situacoes[1].cget("text") == "Recuperação"
        assert app.resumo["recuperacao"].cget("text") == "1"
        app.variaveis_notas[0][0].set("60")
        app.variaveis_notas[0][1].set("50")
        app.variaveis_notas[0][2].set("")
        app.variaveis_notas[0][3].set("")
        assert "ultrapassa" in app.estado.get()
        app.processar_resultados()
        assert erro.call_count == 2
        app.variaveis_notas[0][0].set("inválida")
        assert not app.resultados_atuais
        assert app.rotulos_totais[0].cget("text") == "—"
        assert app.resumo["media_turma"].cget("text") == "—"
        app.processar_resultados()
        assert erro.call_count == 3
        app.limpar_dados()
        assert app.alunos == ["", ""]
        assert app.notas == [[None] * 4, [None] * 4]
        # Configuração pelo diálogo real: percorre widgets e aciona o botão Aplicar.
        app.abrir_configuracoes()
        dialogo = raiz.winfo_children()[-1]
        painel = dialogo.winfo_children()[0]
        entradas = []
        botao = None
        for widget in painel.winfo_children():
            if isinstance(widget, app.ttk.Entry):
                entradas.append(widget)
            elif isinstance(widget, app.ttk.Button) and widget.cget("text") == "Aplicar e começar turma":
                botao = widget
            for filho in widget.winfo_children():
                if isinstance(filho, app.ttk.Button) and filho.cget("text") == "Aplicar e começar turma":
                    botao = filho
        for indice, texto in enumerate(["3", "2", "20", "12", "8"]):
            entradas[indice].delete(0, app.tk.END)
            entradas[indice].insert(0, texto)
        textos_dialogo = []
        pilha = [painel]
        while pilha:
            atual = pilha.pop()
            pilha.extend(atual.winfo_children())
            try:
                texto = atual.cget("text")
                if texto:
                    textos_dialogo.append(str(texto))
                variavel_texto = atual.cget("textvariable")
                if variavel_texto:
                    textos_dialogo.append(str(atual.getvar(variavel_texto)))
            except app.tk.TclError:
                pass
        explicacao = "\n".join(textos_dialogo)
        assert "0,00 a 20,00" in explicacao
        assert "Aprovado\na partir de 12,00" in explicacao
        assert botao is not None
        botao.invoke()
        raiz.update()
        assert app.QUANTIDADE_ALUNOS == 3 and app.QUANTIDADE_NOTAS == 2
        assert len(app.campos_notas) == 3 and len(app.campos_notas[0]) == 2
        for aluno in range(3):
            app.variaveis_nomes[aluno].set(f"Aluno {aluno}")
            for avaliacao in range(2):
                app.variaveis_notas[aluno][avaliacao].set("6")
        app.processar_resultados()
        assert app.resumo["aprovados"].cget("text") == "3"
        app.encerrar()
    print("OK: classificação pelo total, média informativa, critérios, GUI, limpeza e saída.")


if __name__ == "__main__":
    executar()
