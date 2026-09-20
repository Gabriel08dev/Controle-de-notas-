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
    assert app.validar_nota("10") == 10
    for entrada in ["", " ", "nan", "Infinity", "-1", "10.01", "1e2", "1,2.3", "abc", ".", "-", "1_0"]:
        deve_falhar(app.validar_nota, entrada)
    nomes = ["Ana", "Bia", "Caio", "Davi", "Eva"]
    matriz = [[6, 6, 6], [0, 0, 0], [10, 10, 10], [5, 6, 7], [5, 5, 5]]
    resultado = app.calcular_resultados(nomes, matriz)
    assert resultado["medias"] == [6, 0, 10, 6, 5]
    assert resultado["aprovados"] == 3 and resultado["reprovados"] == 2
    assert resultado["media_turma"] == Decimal("5.4")
    assert resultado["maior"] == 10 and resultado["menor"] == 0
    matriz[0] = ["5.9999", "5.9999", "5.9999"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Reprovado"
    deve_falhar(app.calcular_resultados, [], [])
    for dados in [["0", "3", "0", "10", "6"], ["5", "0", "0", "10", "6"], ["5", "3", "10", "0", "6"], ["5", "3", "0", "10", "11"], ["5.5", "3", "0", "10", "6"]]:
        deve_falhar(app.validar_configuracao, dados)
    nova = app.validar_configuracao(["2", "4", "-10", "100", "70"])
    app.QUANTIDADE_ALUNOS, app.QUANTIDADE_NOTAS, app.NOTA_MINIMA, app.NOTA_MAXIMA, app.MEDIA_APROVACAO = nova
    resultado = app.calcular_resultados(["A", "B"], [[70, 70, 70, 70], [-10, 0, 10, 20]])
    assert resultado["medias"] == [70, 5]
    assert resultado["media_turma"] == Decimal("37.5")
    assert resultado["aprovados"] == 1
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
                app.variaveis_notas[aluno][avaliacao].set("80" if aluno == 0 else "60")
        app.processar_resultados()
        assert app.resultados_atuais
        assert app.resumo["media_turma"].cget("text") == "70,00"
        assert app.rotulos_situacoes[0].cget("text") == "Aprovado"
        app.variaveis_notas[0][0].set("inválida")
        assert not app.resultados_atuais
        assert app.resumo["media_turma"].cget("text") == "—"
        app.processar_resultados()
        assert erro.call_count == 2
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
            elif isinstance(widget, app.ttk.Button) and widget.cget("text") == "Aplicar":
                botao = widget
        for indice, texto in enumerate(["3", "2", "0", "20", "12"]):
            entradas[indice].delete(0, app.tk.END)
            entradas[indice].insert(0, texto)
        botao.invoke()
        raiz.update()
        assert app.QUANTIDADE_ALUNOS == 3 and app.QUANTIDADE_NOTAS == 2
        assert len(app.campos_notas) == 3 and len(app.campos_notas[0]) == 2
        for aluno in range(3):
            app.variaveis_nomes[aluno].set(f"Aluno {aluno}")
            for avaliacao in range(2):
                app.variaveis_notas[aluno][avaliacao].set("12")
        app.processar_resultados()
        assert app.resumo["aprovados"].cget("text") == "3"
        app.encerrar()
    print("OK: validação, cálculos, limites, configuração dinâmica, GUI, limpeza e saída.")


if __name__ == "__main__":
    executar()
