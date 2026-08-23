#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fecha o ciclo das caixinhas: nuvem <-> .md, sem reconciliar na mao.

O TAREFAS.md ja tinha via de mao dupla desde 14/08/2026. As outras abas com
caixinha (Compras, Mala, Rotina...) nao tinham: o tique subia para o Supabase e
morria la. O .md ficava mostrando em aberto o que ja tinha sido comprado, e a
unica saida era alguem reconciliar na mao, item por item. Foi o que aconteceu
em 18/08/2026 com o COMPRAS.md, depois da ida a ConfecBell.

Este script e a volta que faltava. Ele nao inventa identificador: usa a MESMA
chave que o painel ja usa, "<id da aba>/<md5 do texto do item>", entao um item so
muda de identidade se o texto mudar - que e exatamente a regra ja documentada em
PAINEL.md. Ate 23/08/2026 a chave daqui saia sem a aba e nao batia com a do
painel: veja o comentario em chave_do_item().

Quem manda, quando arquivo e nuvem discordam do mesmo item: **quem mexeu por
ultimo**. A hora da nuvem e a coluna `mod`; a hora do arquivo e a data do
ultimo commit que tocou aquele .md. Mesma regra do sincroniza_tarefas.py, para
nao existirem duas logicas diferentes de conflito no mesmo repositorio.

Item que a nuvem nunca viu (sem linha em cao_ticados) e decidido pelo arquivo, e
o script SOBE esse estado. E o que faz a marcacao feita a mao no .md aparecer no
celular, em vez de ficar so no arquivo.

Uso:
    SUPABASE_EMAIL=... SUPABASE_SENHA=... python sincroniza_ticados.py
    python sincroniza_ticados.py --conferir   (mostra o que faria, nao escreve)

Sem dependencias externas. Python 3.8+.
"""

import hashlib
import io
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

from gerar_painel import ABAS, quantidade_do_item
from sincroniza_tarefas import Supabase, para_hora

RAIZ = os.path.dirname(os.path.abspath(__file__))
TABELA = "cao_ticados"

# TAREFAS.md tem sincronizador proprio (sincroniza_tarefas.py), com data,
# categoria e exclusao. Aqui e so caixinha ligada/desligada.
FORA = {"TAREFAS.md"}

ITEM = re.compile(r"^(\s*(?:[-*]|\d+[.)])\s+\[)([ xX])(\]\s*)(.*)$")


# ------------------------------------------------------------------ leitura

def chave_do_item(texto, aba):
    """A MESMA chave do painel (gerar_painel.py, funcao mkChave).

    O painel identifica cada caixinha por "<id da aba>/<md5 do texto>", por
    exemplo "ab-compras/2de055d428", e e assim que a linha sobe para o
    cao_ticados. Ate 23/08/2026 este script usava so o md5, sem a aba, entao
    NUNCA encontrava a linha que o painel tinha gravado. Duas consequencias, e
    as duas silenciosas:

      1. para o script, todo item era "a nuvem nunca viu este". O arquivo
         vencia sempre e o tique feito no celular nao voltava para o .md - que
         e a unica coisa que este script existe para fazer;
      2. a cada rodada ele semeava uma segunda familia de linhas na tabela, so
         com o md5, que nenhum painel le.

    O `aba` e o id da secao no painel ("ab-compras"), montado a partir de ABAS.
    """
    h = hashlib.md5(texto.strip().encode("utf-8")).hexdigest()[:10]
    return "%s/%s" % (aba, h)


def itens_do_arquivo(caminho, aba):
    """Devolve (indice_da_linha, chave, quantidade, feito, texto) por caixinha."""
    linhas = io.open(caminho, encoding="utf-8").read().split("\n")
    achados = []
    for i, linha in enumerate(linhas):
        m = ITEM.match(linha)
        if not m:
            continue
        texto = m.group(4)
        achados.append((i, chave_do_item(texto, aba), quantidade_do_item(texto),
                        m.group(2).lower() == "x", texto))
    return linhas, achados


def hora_do_arquivo(nome):
    """Quando aquele .md mudou pela ultima vez, pelo commit e nao pela mtime.

    A Action faz checkout novo a cada rodada e toda mtime nasce "agora": pela
    mtime o arquivo venceria sempre e a nuvem nunca conseguiria desmarcar nada.
    """
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", nome],
                           cwd=RAIZ, capture_output=True, text=True, timeout=30)
        h = para_hora(r.stdout.strip())
        if h:
            return h
    except Exception:
        pass
    try:
        return datetime.fromtimestamp(os.path.getmtime(os.path.join(RAIZ, nome)),
                                      timezone.utc)
    except OSError:
        return datetime.now(timezone.utc)


# ------------------------------------------------------------------ decisao

def decidir(feito_arq, qtd, linha_nuvem, hora_arq):
    """O que fazer com um item. Devolve (novo_estado_no_arquivo, n_para_subir).

    n_para_subir = None quer dizer "nao mexe na nuvem".
    """
    alvo = max(qtd, 1)
    if linha_nuvem is None:
        # A nuvem nunca viu este item: o arquivo manda e o estado dele sobe.
        return feito_arq, (alvo if feito_arq else 0)

    feito_nuvem = int(linha_nuvem.get("n") or 0) >= alvo
    if feito_nuvem == feito_arq:
        return feito_arq, None                      # ja concordam

    hora_nuvem = para_hora(linha_nuvem.get("mod"))
    if hora_nuvem and hora_arq and hora_nuvem > hora_arq:
        return feito_nuvem, None                    # a nuvem mexeu depois
    return feito_arq, (alvo if feito_arq else 0)    # o arquivo mexeu depois


# -------------------------------------------------------------------- fluxo

def main():
    conferir = "--conferir" in sys.argv
    email = os.environ.get("SUPABASE_EMAIL")
    senha = os.environ.get("SUPABASE_SENHA")
    if not (email and senha):
        print("Faltam SUPABASE_EMAIL e SUPABASE_SENHA no ambiente.")
        return 2

    sb = Supabase.entrar(email, senha)
    nuvem = {l["id"]: l for l in (sb._req("/rest/v1/%s?select=*" % TABELA) or [])}
    print("nuvem: %d itens ticados conhecidos" % len(nuvem))

    subir, tocados, vistos = [], 0, set()
    for nome, aba_id, _rot, _ic in ABAS:
        caminho = os.path.join(RAIZ, nome)
        if nome in FORA or not os.path.isfile(caminho):
            continue
        linhas, itens = itens_do_arquivo(caminho, "ab-" + aba_id)
        if not itens:
            continue
        hora_arq = hora_do_arquivo(nome)
        mudou = 0
        for idx, chave, qtd, feito, texto in itens:
            vistos.add(chave)
            novo, n = decidir(feito, qtd, nuvem.get(chave), hora_arq)
            if n is not None:
                subir.append({"id": chave, "n": n})
            if novo != feito:
                m = ITEM.match(linhas[idx])
                linhas[idx] = m.group(1) + ("x" if novo else " ") + m.group(3) + m.group(4)
                mudou += 1
                print("  %-12s %s  %s" % (nome, "marca " if novo else "desmarca",
                                          texto[:62]))
        if mudou and not conferir:
            io.open(caminho, "w", encoding="utf-8").write("\n".join(linhas))
        tocados += mudou
        print("%-14s %3d caixinhas, %d ajustada(s)" % (nome, len(itens), mudou))

    orfas = [c for c in nuvem if c not in vistos]
    # Chave sem "/" e das rodadas anteriores a 23/08/2026, quando este script
    # montava o id sem a aba e escrevia numa familia de linhas que nenhum painel
    # le. Ficam la sem atrapalhar: apagar linha do banco e decisao do Josemar,
    # nao de um robo que roda de hora em hora.
    velhas = [c for c in orfas if "/" not in c]
    if velhas:
        print("nuvem tem %d linha(s) no formato antigo (chave sem a aba), das "
              "rodadas anteriores ao conserto de 23/08/2026. Ninguem as le e "
              "nao atrapalham." % len(velhas))
    if len(orfas) - len(velhas):
        print("nuvem tem %d item(ns) que nenhum .md usa mais (texto editado). "
              "Nao atrapalham, so ocupam linha." % (len(orfas) - len(velhas)))

    if subir:
        print("subir para a nuvem: %d item(ns)" % len(subir))
        if not conferir:
            sb._req("/rest/v1/" + TABELA, "POST", subir,
                    {"Prefer": "resolution=merge-duplicates,return=minimal"})

    print(("[--conferir] nada foi escrito. " if conferir else "")
          + "%d linha(s) de .md ajustada(s)." % tocados)
    return 0


if __name__ == "__main__":
    sys.exit(main())
