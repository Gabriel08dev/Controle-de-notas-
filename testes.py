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
    assert resultado["totais"] == [18, 0, 30, 18, 15]
    assert resultado["medias"] == [6, 0, 10, 6, 5]
    assert resultado["aprovados"] == 3
    assert resultado["recuperacao"] == 1
    assert resultado["reprovados"] == 1
    assert resultado["media_turma"] == Decimal("5.4")
    assert resultado["maior"] == 10 and resultado["menor"] == 0
    matriz[0] = ["3.9999", "3.9999", "3.9999"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Reprovado"
    matriz[0] = ["4", "4", "4"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Recuperação"
    matriz[0] = ["6", "6", "6"]
    assert app.calcular_resultados(nomes, matriz)["situacoes"][0] == "Aprovado"
    deve_falhar(app.calcular_resultados, [], [])
    for dados in [
        ["0", "3", "0", "10", "4", "6"],
        ["5", "0", "0", "10", "4", "6"],
        ["5", "3", "10", "0", "12", "18"],
        ["5", "3", "0", "10", "18", "18"],
        ["5", "3", "0", "10", "19", "18"],
        ["5", "3", "0", "10", "12", "31"],
        ["5", "3", "0", "10", "-1", "18"],
        ["5.5", "3", "0", "10", "12", "18"],
    ]:
        deve_falhar(app.validar_configuracao, dados)
    # Uma quantidade grande comprova que não existe o teto artificial anterior.
    sem_limite_programado = app.validar_configuracao(["1001", "25", "0", "10", "100", "150"])
    assert sem_limite_programado[0] == 1001 and sem_limite_programado[1] == 25
    nova = app.validar_configuracao(["2", "4", "-10", "100", "160", "280"])
    (
        app.QUANTIDADE_ALUNOS,
        app.QUANTIDADE_NOTAS,
        app.NOTA_MINIMA,
        app.NOTA_MAXIMA,
        app.TOTAL_RECUPERACAO,
        app.TOTAL_APROVACAO,
    ) = nova
    resultado = app.calcular_resultados(["A", "B"], [[70, 70, 70, 70], [-10, 0, 10, 20]])
    assert resultado["medias"] == [70, 5]
    assert resultado["media_turma"] == Decimal("37.5")
    assert resultado["aprovados"] == 1
    assert resultado["reprovados"] == 1
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
        assert app.rotulos_totais[0].cget("text") == "320,00"
        assert app.rotulos_totais[1].cget("text") == "240,00"
        assert app.resumo["media_turma"].cget("text") == "70,00"
        assert app.rotulos_situacoes[0].cget("text") == "Aprovado"
        assert app.rotulos_situacoes[1].cget("text") == "Recuperação"
        assert app.resumo["recuperacao"].cget("text") == "1"
        app.variaveis_notas[0][0].set("inválida")
        assert not app.resultados_atuais
        assert app.rotulos_totais[0].cget("text") == "—"
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
            elif isinstance(widget, app.ttk.Button) and widget.cget("text") == "Aplicar configuração":
                botao = widget
            for filho in widget.winfo_children():
                if isinstance(filho, app.ttk.Button) and filho.cget("text") == "Aplicar configuração":
                    botao = filho
        for indice, texto in enumerate(["3", "2", "0", "20", "16", "24"]):
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
    print("OK: classificação pelo total, média informativa, critérios, GUI, limpeza e saída.")


if __name__ == "__main__":
    executar()
