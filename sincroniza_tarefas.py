#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fecha o ciclo do TAREFAS.md: nuvem <-> arquivo, sem copiar e colar.

O painel e uma pagina estatica no GitHub Pages. Pagina estatica nao tem
servidor e nao pode escrever no repositorio, entao ate 14/08/2026 a unica ponte
entre o Supabase e o TAREFAS.md era o botao Exportar, com o Josemar copiando o
texto na mao. Este script e essa ponte, rodando onde ha credencial: na Action
agendada (.github/workflows/sincronizar-tarefas.yml) ou na maquina dele.

Como decide quem manda, quando arquivo e nuvem discordam da mesma tarefa:
**quem mexeu por ultimo ganha**. A hora da nuvem e a coluna `mod` da linha; a
hora do arquivo e a data do ultimo commit que tocou o TAREFAS.md. Sem essa
regra, uma Action que so escrevesse por cima comeria a edicao feita a mao no
.md na rodada seguinte.

Como sabe que uma tarefa foi apagada no painel: `estado_tarefas.json` guarda os
ids da ultima sincronizacao. Tarefa que esta no arquivo, nao esta na nuvem e
estava no estado anterior foi apagada no painel, entao sai do arquivo. Sem esse
registro, "sumiu da nuvem" e "ainda nao subiu" seriam indistinguiveis e a
tarefa apagada voltaria do arquivo a cada hora.

Uso:
    SUPABASE_EMAIL=... SUPABASE_SENHA=... python sincroniza_tarefas.py
    python sincroniza_tarefas.py --conferir   (mostra o que faria, nao escreve)

Sem dependencias externas. Python 3.8+.
"""

import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone

from gerar_painel import extrai_cabecalho, extrai_tarefas

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(RAIZ, "TAREFAS.md")
ESTADO = os.path.join(RAIZ, "estado_tarefas.json")
CONFIG = os.path.join(RAIZ, "supabase.json")
TABELA = "cao_tarefas"

CAB_PADRAO = (
    "# TAREFAS — CAO 2026\n\n"
    "> Lista de tarefas correntes do curso. Marcar como feito, não apagar "
    "(histórico do que já foi cumprido).\n"
    "> Editável aqui ou pelo painel (aba Tarefas). "
    "Formato: `- [ ] texto [dd/mm/aaaa] #categoria`."
)


# ------------------------------------------------------------------- ids ---

def norm(s):
    """Igual ao norm() do painel: minusculas, sem acento, sem espaco nas pontas."""
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip()


def id_base(texto):
    """Reproduz o idBase() do painel (gerar_painel.py, bloco JS_TAREFAS).

    Tarefa que nasce no arquivo tem id derivado do proprio texto, e por isso o
    mesmo texto gera o mesmo id em qualquer aparelho. O hash e o classico
    h*31+char em inteiro de 32 bits com sinal, que e o que o `|0` do JavaScript
    faz. Se este calculo divergir do painel, arquivo e nuvem param de se
    reconhecer e tudo vira duplicata, entao tem teste para ele.
    """
    h = 0
    for ch in norm(texto):
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    if h >= 0x80000000:            # volta para inteiro com sinal, como o `|0`
        h -= 0x100000000
    return "md" + _base36(abs(h))


def _base36(n):
    if n == 0:
        return "0"
    d, s = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while n:
        n, r = divmod(n, 36)
        s = d[r] + s
    return s


# ------------------------------------------------------------------ horas ---

def para_hora(v):
    """ISO 8601 (com Z ou offset) para datetime com fuso. None se nao der."""
    if not v:
        return None
    t = str(v).strip().replace("Z", "+00:00")
    t = re.sub(r"(\.\d{6})\d+", r"\1", t)          # microssegundos de sobra
    try:
        d = datetime.fromisoformat(t)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def hora_do_arquivo():
    """Quando o TAREFAS.md mudou pela ultima vez.

    A data do commit, e nao a mtime, porque a Action faz checkout novo a cada
    rodada e toda mtime nasce "agora": o arquivo ganharia sempre.
    """
    try:
        saida = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", "TAREFAS.md"],
            cwd=RAIZ, capture_output=True, text=True, timeout=30)
        h = para_hora(saida.stdout.strip())
        if h:
            return h
    except Exception:
        pass
    try:
        return datetime.fromtimestamp(os.path.getmtime(ARQUIVO), timezone.utc)
    except OSError:
        return datetime.now(timezone.utc)


# --------------------------------------------------------------- supabase ---

class Supabase(object):
    def __init__(self, url, chave, token):
        self.url, self.chave, self.token = url.rstrip("/"), chave, token

    @classmethod
    def entrar(cls, email, senha):
        cfg = json.load(io.open(CONFIG, encoding="utf-8"))
        url, chave = cfg["url"].rstrip("/"), cfg["anonKey"]
        corpo = json.dumps({"email": email, "password": senha}).encode("utf-8")
        req = urllib.request.Request(
            url + "/auth/v1/token?grant_type=password", data=corpo,
            headers={"apikey": chave, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            ses = json.loads(r.read().decode("utf-8"))
        return cls(url, chave, ses["access_token"])

    def _req(self, caminho, metodo="GET", corpo=None, extra=None):
        cab = {"apikey": self.chave,
               "Authorization": "Bearer " + self.token,
               "Content-Type": "application/json"}
        cab.update(extra or {})
        dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
        req = urllib.request.Request(self.url + caminho, data=dados,
                                     headers=cab, method=metodo)
        with urllib.request.urlopen(req, timeout=60) as r:
            bruto = r.read().decode("utf-8")
        return json.loads(bruto) if bruto.strip() else None

    def tarefas(self):
        return self._req("/rest/v1/%s?select=*" % TABELA) or []

    def gravar(self, linhas):
        if not linhas:
            return
        self._req("/rest/v1/" + TABELA, "POST", linhas,
                  {"Prefer": "resolution=merge-duplicates,return=minimal"})


# ----------------------------------------------------------------- merge ---

def iguais(a, b):
    return (a["txt"] == b["txt"] and (a["data"] or None) == (b["data"] or None)
            and (a["cat"] or "") == (b["cat"] or "") and bool(a["feito"]) == bool(b["feito"]))


def do_arquivo(t):
    return {"id": id_base(t["t"]), "txt": t["t"], "data": t["d"],
            "cat": t["c"] or "", "feito": bool(t["f"]), "secao": t.get("s") or ""}


def da_nuvem(r, secao=""):
    return {"id": r["id"], "txt": r["txt"], "data": r.get("data"),
            "cat": r.get("cat") or "", "feito": bool(r.get("feito")),
            "secao": secao, "mod": r.get("mod")}


def juntar(arquivo, nuvem, estado, t_arquivo):
    """Devolve (tarefas finais, o que subir para a nuvem, relatorio)."""
    no_arq = {t["id"]: t for t in arquivo}
    na_nuv = {r["id"]: r for r in nuvem}
    ordem = [t["id"] for t in arquivo] + [r["id"] for r in nuvem if r["id"] not in no_arq]

    final, subir, rel = [], [], {"baixadas": 0, "subidas": 0, "apagadas": 0, "novas_da_nuvem": 0}

    for tid in ordem:
        a, n = no_arq.get(tid), na_nuv.get(tid)

        if a and n:
            if iguais(a, da_nuvem(n)):
                final.append(dict(a, mod=n.get("mod")))
                continue
            t_nuvem = para_hora(n.get("mod"))
            if t_nuvem is None or t_arquivo > t_nuvem:
                final.append(a)                       # o arquivo mexeu depois
                subir.append(a)
                rel["subidas"] += 1
            else:
                final.append(da_nuvem(n, a["secao"]))  # o painel mexeu depois
                rel["baixadas"] += 1

        elif a and not n:
            if tid in estado:
                rel["apagadas"] += 1                  # existia na nuvem e sumiu
            else:
                final.append(a)                       # nasceu aqui, ainda nao subiu
                subir.append(a)
                rel["subidas"] += 1

        elif n and not a:
            # Linha de id "md" que nao esta mais no arquivo e linha reescrita ou
            # apagada a mao. Vale a mesma regra da poda do painel: para o que
            # nasceu no arquivo, o arquivo manda. Nao ressuscita.
            if str(tid).startswith("md"):
                continue
            final.append(da_nuvem(n))                 # criada no painel
            rel["novas_da_nuvem"] += 1

    return final, subir, rel


# --------------------------------------------------------------- escrita ---

def para_markdown(tarefas, cabecalho, ordem_secoes):
    """Mesmo formato do botao Exportar do painel, para os dois nunca brigarem.

    Ordena por data dentro de cada secao, que e a ordem que a aba Tarefas
    mostra. A ordenacao e estavel, entao tarefa de mesma data nao troca de
    lugar a cada rodada e o arquivo nao gera commit de barulho.
    """
    pend = [t for t in tarefas if not t["feito"]]
    feitas = [t for t in tarefas if t["feito"]]

    pend.sort(key=lambda t: t["data"] or "9999-99-99")
    feitas.sort(key=lambda t: t.get("mod") or "", reverse=True)

    grupos = {}
    for t in pend:
        grupos.setdefault(t["secao"] or "", []).append(t)

    corpo = ""
    if grupos.get(""):
        corpo += "\n".join(linha(t) for t in grupos[""]) + "\n"
    for s in ordem_secoes:
        if not grupos.get(s):
            continue                                  # secao que esvaziou sai junto
        corpo += "\n### %s\n%s\n" % (s, "\n".join(linha(t) for t in grupos[s]))
    if not pend:
        corpo = "- [ ] ...\n"

    cab = (cabecalho or "").strip() or CAB_PADRAO
    return (cab + "\n\n## Pendentes\n" + corpo + "\n## Concluídas\n"
            + ("\n".join(linha(t) for t in feitas) + "\n" if feitas else ""))


def linha(t):
    s = "- [%s] %s" % ("x" if t["feito"] else " ", t["txt"])
    if t["data"]:
        a, m, d = t["data"].split("-")
        s += " [%s/%s/%s]" % (d, m, a)
    if t["cat"]:
        s += " #" + t["cat"]
    return s


# ------------------------------------------------------------------ main ---

def main():
    conferir = "--conferir" in sys.argv
    email = os.environ.get("SUPABASE_EMAIL", "").strip()
    senha = os.environ.get("SUPABASE_SENHA", "")
    if not email or not senha:
        print("Faltam SUPABASE_EMAIL e SUPABASE_SENHA no ambiente.", file=sys.stderr)
        return 2

    texto = io.open(ARQUIVO, encoding="utf-8").read() if os.path.exists(ARQUIVO) else ""
    brutas = extrai_tarefas(texto)
    arquivo = [do_arquivo(t) for t in brutas]
    ordem_secoes, vistas = [], set()
    for t in brutas:
        s = t.get("s") or ""
        if s and s not in vistas:
            vistas.add(s)
            ordem_secoes.append(s)

    try:
        sb = Supabase.entrar(email, senha)
        nuvem = sb.tarefas()
    except urllib.error.HTTPError as e:
        print("Supabase respondeu %s. Confira o login nos Secrets." % e.code, file=sys.stderr)
        return 1
    except Exception as e:
        print("Nao consegui falar com o Supabase: %s" % e, file=sys.stderr)
        return 1

    estado = set()
    if os.path.exists(ESTADO):
        try:
            estado = set(json.load(io.open(ESTADO, encoding="utf-8")).get("ids", []))
        except Exception:
            pass

    # Primeira rodada: sem estado anterior, "sumiu da nuvem" nao e conclusao
    # possivel, entao nada e apagado e o arquivo so sobe.
    primeira = not estado

    final, subir, rel = juntar(arquivo, nuvem, estado, hora_do_arquivo())
    novo = para_markdown(final, extrai_cabecalho(texto), ordem_secoes)
    mudou = novo != texto

    print("arquivo: %d | nuvem: %d | resultado: %d" % (len(arquivo), len(nuvem), len(final)))
    print("sobem: %d | descem: %d | criadas no painel: %d | apagadas no painel: %d%s"
          % (rel["subidas"], rel["baixadas"], rel["novas_da_nuvem"], rel["apagadas"],
             " (primeira rodada: nada e apagado)" if primeira else ""))
    print("TAREFAS.md: " + ("muda" if mudou else "ja estava em dia"))

    if conferir:
        return 0

    if subir:
        agora = datetime.now(timezone.utc).isoformat()
        sb.gravar([{"id": t["id"], "txt": t["txt"], "data": t["data"],
                    "cat": t["cat"], "feito": t["feito"], "mod": agora} for t in subir])

    if mudou:
        with io.open(ARQUIVO, "w", encoding="utf-8", newline="\n") as f:
            f.write(novo)

    with io.open(ESTADO, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"ids": sorted(t["id"] for t in final)}, f,
                  ensure_ascii=False, indent=1)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
