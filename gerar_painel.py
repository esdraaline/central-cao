#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Painel da Central do CAO.

Le os arquivos .md da raiz e monta um painel HTML unico em docs/index.html.
Os .md continuam sendo a fonte de verdade: edite os .md, rode este script.

Uso:
    python gerar_painel.py

Sem dependencias externas. Python 3.8+.
"""

import hashlib
import html
import os
import re
import sys
from datetime import date

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "docs", "index.html")

# Inicio e fim estimados do curso (CAO-II/26), usados no contador da home.
CURSO_INICIO = date(2026, 8, 17)
CURSO_FIM = date(2027, 8, 17)
# Primeira ida a Sao Paulo. Dai em diante a semana se repete: viaja domingo,
# aula de segunda a quinta, volta quinta depois das 11h30 (ver ROTINA.md).
PRIMEIRA_VIAGEM = date(2026, 8, 16)

# Ordem das abas. (arquivo, id, rotulo, icone)
ABAS = [
    ("STATUS.md",    "painel",    "Painel",     "home"),
    ("PRAZOS.md",    "prazos",    "Prazos",     "calendar"),
    ("TAREFAS.md",   "tarefas",   "Tarefas",    "check"),
    ("ROTINA.md",    "rotina",    "Rotina",     "clock"),
    ("CONTATOS.md",  "contatos",  "Contatos",   "users"),
    ("DUVIDAS.md",   "duvidas",   "Dúvidas",    "help"),
    ("ANOTACOES.md", "anotacoes", "Anotações",  "note"),
    ("COMPRAS.md",   "compras",   "Compras",    "carrinho"),
    ("MALA.md",      "mala",      "Mala",       "mala"),
    ("VIAGENS.md",   "viagens",   "Viagens",    "map"),
]

MD_PARA_ABA = {arq: aba_id for arq, aba_id, _, _ in ABAS}

ICONES = {
    "home":     '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 11h18"/>',
    "check":    '<path d="M20 6 9 17l-5-5"/>',
    "clock":    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "users":    '<path d="M16 20v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1"/><circle cx="9.5" cy="8" r="3.5"/><path d="M21 20v-1a4 4 0 0 0-3-3.8"/><path d="M16 4.2a3.5 3.5 0 0 1 0 6.8"/>',
    "help":     '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.2 2.4c-.7.2-1.2.9-1.2 1.6v.5"/><path d="M12 17.5h.01"/>',
    "note":     '<path d="M5 3h9l5 5v13H5z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
    "map":      '<path d="M9 4 3 6.5v14L9 18l6 2.5 6-2.5v-14L15 6.5 9 4z"/><path d="M9 4v14M15 6.5v14"/>',
    "mala":     '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M9 7V4h6v3"/><path d="M3 12h18"/>',
    "carrinho": '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.2"/><circle cx="18" cy="20" r="1.2"/>',
    "prancheta": '<rect x="4" y="4" width="16" height="17" rx="2"/><path d="M9 3h6v3H9z"/><path d="m8.5 13 2 2 4-4"/>',
    "search":   '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "sun":      '<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
    "moon":     '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>',
    "file":     '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v4h4"/>',
    "mais":     '<path d="M12 5v14M5 12h14"/>',
    "lixo":     '<path d="M4 7h16M10 11v6M14 11v6"/><path d="M6 7l1 13h10l1-13"/><path d="M9 7V4h6v3"/>',
    "lapis":    '<path d="M4 20h4L20 8a2.8 2.8 0 0 0-4-4L4 16z"/>',
    "baixar":   '<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/>',
    "subir":    '<path d="M12 21V9"/><path d="m7 13 5-5 5 5"/><path d="M4 4h16"/>',
    "alerta":   '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
    "vazio":    '<circle cx="12" cy="12" r="9"/><path d="M8.5 13.5s1.2 1.5 3.5 1.5 3.5-1.5 3.5-1.5"/><path d="M9 9.5h.01M15 9.5h.01"/>',
    "fechar":   '<path d="M6 6l12 12M18 6 6 18"/>',
    "copiar":   '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
}

# Categorias das tarefas: (chave, rotulo, cor)
CATEGORIAS = [
    ("curso",       "Curso",          "#3b7dd8"),
    ("dissertacao", "Dissertação",    "#8b5cf6"),
    ("admin",       "Administrativo", "#e8892b"),
    ("pessoal",     "Pessoal",        "#0f9d58"),
]


# ---------------------------------------------------------------- markdown ---

def _inline(txt):
    """Formatacao inline: codigo, negrito, italico, links."""
    # codigo inline primeiro (protege o conteudo)
    guardados = []

    def _guarda(m):
        guardados.append(m.group(1))
        return "\x00%d\x00" % (len(guardados) - 1)

    txt = re.sub(r"`([^`]+)`", _guarda, txt)
    txt = html.escape(txt, quote=False)

    # links [texto](destino)
    def _link(m):
        rotulo, destino = m.group(1), m.group(2)
        alvo = destino.split("#")[0]
        arquivo = os.path.basename(alvo.replace("%20", " "))
        if arquivo in MD_PARA_ABA:
            return '<a href="#%s" class="lnk-aba">%s</a>' % (MD_PARA_ABA[arquivo], rotulo)
        if destino.startswith("mailto:") or destino.startswith("http"):
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (destino, rotulo)
        # caminho local: nao vira link (o arquivo nao vai para o site publico)
        return '<span class="arq" title="Arquivo na pasta local: %s">%s%s</span>' % (
            html.escape(destino.replace("%20", " "), quote=True), svg("file", 13), rotulo)

    txt = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, txt)

    # e-mails soltos viram mailto
    txt = re.sub(r"(?<!\">)(?<![\w.@-])([\w.+-]+@[\w-]+\.[\w.]+)",
                 r'<a href="mailto:\1">\1</a>', txt)

    txt = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", txt)

    for i, cod in enumerate(guardados):
        txt = txt.replace("\x00%d\x00" % i, "<code>%s</code>" % html.escape(cod, quote=False))
    return txt


# Itens de checklist que comecam com um numero ("6 camisetas...") ou terminam
# com "- 5" / "- 2 pares" viram contador, para dar para marcar so uma parte.
_QTD_INICIO = re.compile(r"^(?:\*\*)?(\d{1,2})\s+[A-Za-zÀ-ÿ]")
_QTD_FIM = re.compile(r"[—-]\s*(\d{1,2})\s*"
                      r"(?:conjuntos?|pares?|mudas?|unidades?|un\.?)?\s*$", re.I)


def quantidade_do_item(texto):
    """Devolve a quantidade do item, ou 0 se for item simples (sim/nao)."""
    for rx in (_QTD_INICIO, _QTD_FIM):
        m = rx.search(texto.strip())
        if m:
            n = int(m.group(1))
            if 2 <= n <= 30:
                return n
    return 0


def md_para_html(texto):
    """Converte markdown para HTML. Suporta o subconjunto usado nos docs."""
    linhas = texto.split("\n")
    saida = []
    i = 0
    # pilha de listas abertas: (indentacao, tag, aninhada_em_li)
    pilha = []

    def fecha_uma():
        indent, tag, dentro_li = pilha.pop()
        saida.append("</%s>" % tag)
        if dentro_li:
            saida.append("</li>")

    def fecha_lista():
        while pilha:
            fecha_uma()

    while i < len(linhas):
        ln = linhas[i]
        cru = ln.rstrip()
        strip = cru.strip()

        # bloco de codigo
        if strip.startswith("```"):
            fecha_lista()
            i += 1
            buf = []
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                buf.append(linhas[i])
                i += 1
            i += 1
            saida.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf), quote=False))
            continue

        # linha vazia
        if not strip:
            fecha_lista()
            i += 1
            continue

        # tabela
        if strip.startswith("|") and i + 1 < len(linhas) and re.match(r"^\s*\|[\s:|-]+\|\s*$", linhas[i + 1]):
            fecha_lista()
            cabec = [c.strip() for c in strip.strip("|").split("|")]
            i += 2
            corpo = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                corpo.append([c.strip() for c in linhas[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div class="tab-wrap"><table><thead><tr>']
            t += ["<th>%s</th>" % _inline(c) for c in cabec]
            t.append("</tr></thead><tbody>")
            for linha in corpo:
                t.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in linha) + "</tr>")
            t.append("</tbody></table></div>")
            saida.append("".join(t))
            continue

        # citacao
        if strip.startswith(">"):
            fecha_lista()
            buf = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                buf.append(linhas[i].strip().lstrip(">").strip())
                i += 1
            saida.append("<blockquote>%s</blockquote>" % _inline(" ".join(buf)))
            continue

        # regua
        if re.match(r"^-{3,}$", strip):
            fecha_lista()
            saida.append("<hr>")
            i += 1
            continue

        # titulo
        m = re.match(r"^(#{1,6})\s+(.*)$", strip)
        if m:
            fecha_lista()
            n = len(m.group(1))
            conteudo = m.group(2)
            if n == 1:
                i += 1
                continue  # o H1 vira o titulo da aba, nao repete no corpo
            saida.append("<h%d>%s</h%d>" % (n, _inline(conteudo), n))
            i += 1
            continue

        # item de lista (com ou sem numeracao, com ou sem indentacao)
        m = re.match(r"^(\s*)(?:[-*]|(\d+)[.)])\s+(.*)$", cru)
        if m:
            indent = len(m.group(1).replace("\t", "  "))
            numerada = m.group(2) is not None
            item = m.group(3)
            mk = re.match(r"^\[([ xX])\]\s*(.*)$", item)

            if mk:
                tag, classe = "ul", ' class="tarefas"'
            else:
                tag, classe = ("ol", "") if numerada else ("ul", "")

            # fecha niveis mais profundos que o atual
            while pilha and pilha[-1][0] > indent:
                fecha_uma()

            if not pilha or pilha[-1][0] < indent:
                # sub-lista: entra dentro do <li> anterior, que ainda nao fecha
                dentro_li = bool(pilha) and bool(saida) and saida[-1].endswith("</li>")
                if dentro_li:
                    saida[-1] = saida[-1][:-len("</li>")]
                saida.append("<%s%s>" % (tag, classe))
                pilha.append((indent, tag, dentro_li))
            elif pilha[-1][1] != tag:
                # mesmo nivel, mas mudou de <ul> para <ol> (ou vice-versa)
                anterior = pilha[-1][2]
                fecha_uma()
                saida.append("<%s%s>" % (tag, classe))
                pilha.append((indent, tag, anterior))

            if mk:
                feito = mk.group(1).lower() == "x"
                # data-mk: chave estavel do item, para o navegador lembrar o que
                # ja foi ticado. Vem do texto, entao editar o texto zera aquele item.
                chave = hashlib.md5(mk.group(2).strip().encode("utf-8")).hexdigest()[:10]
                qtd = quantidade_do_item(mk.group(2))
                saida.append('<li class="%s" data-mk="%s"%s><span class="box">%s</span>'
                             '<span>%s</span></li>' % (
                                 "ok" if feito else "pend", chave,
                                 ' data-qtd="%d"' % qtd if qtd else "",
                                 svg("check", 12) if feito else "",
                                 _inline(mk.group(2))))
            else:
                saida.append("<li>%s</li>" % _inline(item))
            i += 1
            continue

        # paragrafo
        fecha_lista()
        buf = [strip]
        i += 1
        while i < len(linhas):
            prox = linhas[i].strip()
            if (not prox or prox.startswith(("#", "-", "*", ">", "|", "```"))
                    or re.match(r"^\d+[.)]\s", prox)):
                break
            buf.append(prox)
            i += 1
        saida.append("<p>%s</p>" % _inline(" ".join(buf)))

    fecha_lista()
    return "\n".join(saida)


def svg(nome, tam=18):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % (tam, tam, ICONES[nome]))


# ------------------------------------------------------------------ dados ---

def conta_tarefas(texto):
    pend = len(re.findall(r"^\s*[-*]\s+\[ \]", texto, re.M))
    feito = len(re.findall(r"^\s*[-*]\s+\[[xX]\]", texto, re.M))
    return pend, feito


def extrai_cabecalho(texto):
    """Devolve o topo do TAREFAS.md (titulo e linhas de instrucao) ate o
    primeiro "## ".

    O botao Exportar reescreve o arquivo inteiro, entao ele precisa devolver
    este topo como ele esta. Antes o cabecalho era uma copia decorada dentro do
    JavaScript, e ela envelheceu: exportar apagava as linhas sobre categorias e
    sobre a data nao ser enfeite, que so existiam no arquivo.
    """
    corte = re.search(r"^##\s", texto, re.M)
    return (texto[:corte.start()] if corte else texto).rstrip()


def extrai_tarefas(texto):
    """Le as tarefas do TAREFAS.md em formato estruturado.

    Sintaxe reconhecida (a data e a categoria sao opcionais):
        - [ ] Entregar o artigo [15/09/2026] #dissertacao
        - [x] Tarefa ja concluida

    O campo "s" guarda o subtitulo (###) sob o qual a linha estava. E o que
    permite ao Exportar devolver o arquivo com as mesmas secoes, em vez de
    achatar tudo numa lista corrida.
    """
    tarefas = []
    validas = {c[0] for c in CATEGORIAS}
    secao = ""

    for linha in texto.splitlines():
        # "## Pendentes"/"## Concluidas" zeram a secao; "###" em diante define
        h = re.match(r"^(#{2,6})\s+(.*)$", linha)
        if h:
            secao = h.group(2).strip() if len(h.group(1)) >= 3 else ""
            continue

        m = re.match(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$", linha)
        if not m:
            continue
        feito = m.group(1).lower() == "x"
        corpo = m.group(2).strip()

        # data no formato [dd/mm/aaaa]
        iso = None
        md = re.search(r"\[(\d{1,2})/(\d{1,2})/(\d{4})\]", corpo)
        if md:
            d, mes, a = int(md.group(1)), int(md.group(2)), int(md.group(3))
            try:
                iso = date(a, mes, d).isoformat()
                corpo = corpo.replace(md.group(0), "").strip()
            except ValueError:
                pass  # data invalida fica como texto

        # categoria no formato #chave
        cat = ""
        mc = re.search(r"#(\w+)\b", corpo)
        if mc and mc.group(1).lower() in validas:
            cat = mc.group(1).lower()
            corpo = corpo.replace(mc.group(0), "").strip()

        # tira a sintaxe de markdown: o texto da tarefa e exibido puro
        corpo = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", corpo)   # links
        corpo = re.sub(r"\*\*([^*]+)\*\*", r"\1", corpo)         # negrito
        corpo = re.sub(r"`([^`]+)`", r"\1", corpo)               # codigo
        corpo = re.sub(r"\s{2,}", " ", corpo).strip(" -—")
        if corpo:
            tarefas.append({"t": corpo, "d": iso, "c": cat, "f": feito, "s": secao})

    return tarefas


def escapa_js(obj):
    """Serializa para JSON seguro dentro de uma tag <script>."""
    import json
    return (json.dumps(obj, ensure_ascii=False)
            .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


# --------------------------------------------------------------- template ---

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --vm:#c8102e; --vm-cl:#e63950;
  --bg:#f4f5f7; --card:#fff; --card2:#fafbfc;
  --tx:#1a1d21; --tx2:#5b6470; --tx3:#8a929c;
  --bd:#e2e5ea; --sh:0 1px 3px rgba(16,24,40,.06),0 1px 2px rgba(16,24,40,.04);
  --sh2:0 4px 16px rgba(16,24,40,.08);
  --ok:#0f9d58; --al:#e8a13a; --al-bg:#fef8ec;
}
@media (prefers-color-scheme:dark){
  :root{--bg:#0f1218;--card:#171b23;--card2:#1c212b;--tx:#e6e9ee;--tx2:#9aa4b2;
        --tx3:#6b7480;--bd:#262c37;--vm-cl:#ff5a72;--al-bg:#2a2415;
        --sh:0 1px 3px rgba(0,0,0,.4);--sh2:0 4px 20px rgba(0,0,0,.5)}
}
:root[data-theme=dark]{--bg:#0f1218;--card:#171b23;--card2:#1c212b;--tx:#e6e9ee;
  --tx2:#9aa4b2;--tx3:#6b7480;--bd:#262c37;--vm-cl:#ff5a72;--al-bg:#2a2415;
  --sh:0 1px 3px rgba(0,0,0,.4);--sh2:0 4px 20px rgba(0,0,0,.5)}
:root[data-theme=light]{--bg:#f4f5f7;--card:#fff;--card2:#fafbfc;--tx:#1a1d21;
  --tx2:#5b6470;--tx3:#8a929c;--bd:#e2e5ea;--vm-cl:#e63950;--al-bg:#fef8ec;
  --sh:0 1px 3px rgba(16,24,40,.06);--sh2:0 4px 16px rgba(16,24,40,.08)}

body{background:var(--bg);color:var(--tx);
  font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased}

/* cabecalho */
:root{--top1:#8f0a20;--top2:#c8102e;--top3:#a30d26}
@media (prefers-color-scheme:dark){:root{--top1:#4a0511;--top2:#7d0a1d;--top3:#5c0716}}
:root[data-theme=dark]{--top1:#4a0511;--top2:#7d0a1d;--top3:#5c0716}
:root[data-theme=light]{--top1:#8f0a20;--top2:#c8102e;--top3:#a30d26}
.topo{background:linear-gradient(100deg,var(--top1),var(--top2) 55%,var(--top3));color:#fff;
  padding:20px 0 0;box-shadow:var(--sh2);position:relative;overflow:hidden}
.topo::after{content:"";position:absolute;right:-60px;top:-70px;width:260px;height:260px;
  border-radius:50%;background:rgba(255,255,255,.06)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px;position:relative;z-index:1}
.marca{display:flex;align-items:center;gap:13px;flex-wrap:wrap}
.brasao{width:42px;height:42px;border-radius:9px;background:rgba(255,255,255,.16);
  display:grid;place-items:center;font-weight:800;font-size:13px;letter-spacing:.5px;flex:none}
.marca h1{font-size:19px;font-weight:700;letter-spacing:-.2px;line-height:1.25}
.marca p{font-size:12.5px;opacity:.82;margin-top:1px}
.acoes{margin-left:auto;display:flex;gap:8px;align-items:center}
.bt{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.2);color:#fff;
  border-radius:9px;padding:8px;cursor:pointer;display:grid;place-items:center;
  transition:background .15s}
.bt:hover{background:rgba(255,255,255,.26)}

/* busca */
.busca{position:relative;margin:16px 0 4px;max-width:420px}
.busca svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);opacity:.6;color:#fff}
.busca input{width:100%;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);
  border-radius:9px;padding:9px 12px 9px 36px;color:#fff;font-size:14px;font-family:inherit}
.busca input::placeholder{color:rgba(255,255,255,.62)}
.busca input:focus{outline:none;background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.45)}

/* abas */
nav{display:flex;gap:2px;margin-top:14px;overflow-x:auto;scrollbar-width:none}
nav::-webkit-scrollbar{display:none}
nav button{background:none;border:0;color:rgba(255,255,255,.72);font:600 13.5px/1 inherit;
  padding:12px 14px 13px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;
  display:flex;align-items:center;gap:7px;transition:color .15s}
nav button:hover{color:#fff}
nav button[aria-selected=true]{color:#fff;border-bottom-color:#fff}
nav .pill{background:rgba(255,255,255,.26);border-radius:20px;padding:1px 7px;font-size:11px;font-weight:700}
nav .pill-b{background:#fff;color:var(--top2)}
nav.buscando .pill:not(.pill-b){display:none}

/* conteudo */
main{max-width:1080px;margin:0 auto;padding:24px 20px 64px}
.aba{display:none;animation:sobe .22s ease}
.aba.on{display:block}
@keyframes sobe{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.card{background:var(--card);border:1px solid var(--bd);border-radius:13px;
  padding:22px 24px;box-shadow:var(--sh);margin-bottom:16px;overflow-wrap:break-word}

/* home */
.grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:13px;margin-bottom:16px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:13px;padding:17px 19px;box-shadow:var(--sh)}
.kpi .rot{font-size:11.5px;text-transform:uppercase;letter-spacing:.7px;color:var(--tx3);font-weight:700}
.kpi .val{font-size:29px;font-weight:750;letter-spacing:-1px;margin:5px 0 1px;line-height:1.1}
.kpi .sub{font-size:12.5px;color:var(--tx2)}
.kpi.dest{border-color:var(--vm);border-left-width:4px}
.barra{height:6px;background:var(--bd);border-radius:4px;overflow:hidden;margin-top:11px}
.barra i{display:block;height:100%;background:linear-gradient(90deg,var(--vm),var(--vm-cl));border-radius:4px}
.aviso{background:var(--al-bg);border:1px solid var(--al);border-left-width:4px;
  border-radius:11px;padding:15px 18px;margin-bottom:16px}
.aviso h3{font-size:13px;text-transform:uppercase;letter-spacing:.6px;color:var(--al);margin-bottom:9px}
.aviso ul{list-style:none}
.aviso li{padding:4px 0 4px 20px;position:relative;font-size:14px}
.aviso li::before{content:"";position:absolute;left:4px;top:12px;width:6px;height:6px;
  border-radius:50%;background:var(--al)}

/* ===================== guia do dia (abertura do painel) =====================
   E a primeira coisa que aparece: em que dia estamos, o que fazer hoje, o que
   vem amanha. Tudo montado no navegador, para nunca envelhecer sozinho.     */
.guia{background:var(--card);border:1px solid var(--bd);border-radius:14px;
  box-shadow:var(--sh);margin-bottom:16px;overflow:hidden}
.guia-topo{display:flex;gap:16px;align-items:center;flex-wrap:wrap;
  padding:17px 22px;background:linear-gradient(100deg,var(--top1),var(--top2) 60%);color:#fff}
.guia-ola{font-size:12.5px;text-transform:uppercase;letter-spacing:.8px;opacity:.85;font-weight:700}
.guia-dia{font-size:20px;font-weight:750;letter-spacing:-.3px;line-height:1.2;margin-top:2px}
.guia-fase{font-size:13px;opacity:.9;margin-top:3px}
.guia-conta{margin-left:auto;text-align:right;display:flex;align-items:baseline;gap:9px;
  background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.2);
  border-radius:11px;padding:9px 14px}
.guia-conta b{font-size:27px;font-weight:800;letter-spacing:-1px;line-height:1}
.guia-conta span{font-size:12px;line-height:1.35;text-align:left;opacity:.92}
.guia-corpo{padding:6px 22px 18px}
.guia-bloco{margin-top:15px}
.guia-cab{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;
  text-transform:uppercase;letter-spacing:.8px;color:var(--tx3);margin-bottom:7px}
.guia-cab .n{background:var(--bd);color:var(--tx2);border-radius:20px;padding:1px 8px;font-size:11px}
.guia-bloco.vencido .guia-cab{color:var(--vm)}
.guia-bloco.vencido .guia-cab .n{background:var(--vm);color:#fff}
.guia-bloco.agora .guia-cab{color:var(--al)}
.guia-bloco.agora .guia-cab .n{background:var(--al);color:#fff}
.guia-lista{list-style:none;margin:0}
.guia-lista li{display:flex;gap:10px;align-items:flex-start;padding:9px 12px;margin:6px 0;
  border:1px solid var(--bd);border-left-width:3px;border-radius:9px;background:var(--card2);
  font-size:14.5px;color:var(--tx)}
.guia-bloco.vencido .guia-lista li{border-left-color:var(--vm)}
.guia-bloco.agora .guia-lista li{border-left-color:var(--al)}
.guia-lista li .pt{width:8px;height:8px;border-radius:50%;flex:none;margin-top:7px;background:var(--tx3)}
.guia-lista li .qd{color:var(--tx3);font-size:12.5px;white-space:nowrap;margin-left:auto;
  padding-left:8px;font-variant-numeric:tabular-nums}
.guia-tudoem{display:flex;gap:9px;align-items:center;color:var(--ok);font-size:14px;
  padding:13px 0 4px;font-weight:600}
.guia-nota{font-size:13px;color:var(--tx2);margin-top:13px;padding-top:12px;
  border-top:1px solid var(--bd)}
.guia-nota b{color:var(--tx)}
@media(max-width:560px){
  .guia-topo{padding:15px 17px}
  .guia-corpo{padding:4px 17px 16px}
  .guia-conta{margin-left:0;width:100%;justify-content:flex-start}
  .guia-dia{font-size:18px}
}

/* tipografia do conteudo */
.card h2{font-size:17px;font-weight:700;letter-spacing:-.2px;margin:26px 0 11px;
  padding-bottom:8px;border-bottom:2px solid var(--bd)}
.card h2:first-child{margin-top:0}
.card h3{font-size:14.5px;font-weight:700;color:var(--tx);margin:19px 0 8px}
.card p{margin:9px 0;color:var(--tx2)}
.card ul,.card ol{margin:9px 0 9px 21px}
.card li{margin:5px 0;color:var(--tx2)}
.card li::marker{color:var(--vm-cl);font-weight:600}
.card li ul,.card li ol{margin:5px 0 5px 18px}
.card ol{list-style:decimal}
.card strong{color:var(--tx);font-weight:650}
.card a{color:var(--vm-cl);text-decoration:none;border-bottom:1px solid transparent}
.card a:hover{border-bottom-color:currentColor}
blockquote{border-left:3px solid var(--vm);background:var(--card2);padding:11px 16px;
  border-radius:0 9px 9px 0;margin:13px 0;font-size:13.5px;color:var(--tx2)}
code{background:var(--card2);border:1px solid var(--bd);border-radius:5px;padding:1.5px 5px;
  font:.88em/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--vm-cl)}
pre{background:var(--card2);border:1px solid var(--bd);border-radius:10px;padding:15px 17px;
  overflow-x:auto;margin:13px 0}
pre code{background:none;border:0;padding:0;color:var(--tx2);font-size:12.5px;line-height:1.55}
hr{border:0;border-top:1px solid var(--bd);margin:20px 0}
.arq{color:var(--tx2);font-size:.95em;border-bottom:1px dotted var(--tx3);cursor:help;
  overflow-wrap:anywhere}
.arq svg{flex:none;opacity:.55;vertical-align:-2px;margin-right:3px}

/* tabelas */
.tab-wrap{overflow-x:auto;margin:13px 0;border:1px solid var(--bd);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13.8px;min-width:400px}
th{background:var(--card2);text-align:left;padding:10px 14px;font-weight:700;font-size:12px;
  text-transform:uppercase;letter-spacing:.5px;color:var(--tx3);border-bottom:1px solid var(--bd)}
td{padding:10px 14px;border-bottom:1px solid var(--bd);color:var(--tx2)}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--card2)}

/* tarefas */
ul.tarefas{list-style:none;margin:11px 0}
ul.tarefas li{display:flex;gap:10px;align-items:flex-start;padding:9px 12px;margin:5px 0;
  border:1px solid var(--bd);border-radius:9px;background:var(--card2)}
ul.tarefas li .box{width:17px;height:17px;border-radius:5px;border:2px solid var(--bd);
  flex:none;margin-top:2px;display:grid;place-items:center}
ul.tarefas li.pend{border-left:3px solid var(--al)}
ul.tarefas li.pend .box{border-color:var(--al)}
ul.tarefas li.ok{opacity:.6}
ul.tarefas li.ok .box{background:var(--ok);border-color:var(--ok);color:#fff}
/* risca o texto (2o span), nunca o contador que vem depois dele */
ul.tarefas li.ok>span:nth-child(2){text-decoration:line-through}
/* itens ticaveis: os das abas geradas dos .md */
ul.tarefas li[data-mk]{cursor:pointer;user-select:none;
  transition:border-color .12s,background .12s}
ul.tarefas li[data-mk]:hover{border-color:var(--vm);background:var(--card)}
ul.tarefas li[data-mk]:active{transform:scale(.995)}
/* itens com quantidade: da para marcar so uma parte */
ul.tarefas li[data-qtd]{flex-wrap:wrap;row-gap:6px}
/* o texto ocupa o resto da 1a linha (junto da caixinha) e quebra dentro de si;
   quem desce para a linha de baixo, quando falta espaco, e o contador */
ul.tarefas li[data-qtd]>span:nth-child(2){flex:1 1 0;min-width:0}
ul.tarefas li.parcial .box{background:var(--al);border-color:var(--al)}
ul.tarefas li.parcial .box::after{content:"";width:9px;height:2.5px;
  border-radius:2px;background:#fff}
.mk-qtd{margin-left:auto;display:flex;align-items:center;gap:4px;flex:none}
.mk-qtd button{width:26px;height:26px;flex:none;border-radius:7px;
  border:1px solid var(--bd);background:var(--card);color:var(--tx2);
  font-size:1rem;line-height:1;cursor:pointer;display:grid;place-items:center;
  padding:0}
.mk-qtd button:hover:not(:disabled){border-color:var(--vm);color:var(--tx)}
.mk-qtd button:disabled{opacity:.35;cursor:default}
.mk-qtd .n{min-width:44px;text-align:center;font-size:.83rem;
  font-variant-numeric:tabular-nums;color:var(--tx2)}
ul.tarefas li.ok .mk-qtd .n{color:var(--ok);font-weight:600}
ul.tarefas li.parcial .mk-qtd .n{color:var(--al);font-weight:600}
/* contador de progresso no topo das abas com lista ticavel */
.mk-topo{display:flex;align-items:center;gap:12px;flex-wrap:wrap;
  margin:0 0 14px;padding:11px 14px;border:1px solid var(--bd);
  border-radius:10px;background:var(--card2)}
.mk-topo .mk-n{font-weight:700;color:var(--tx)}
.mk-topo .mk-barra{flex:1;min-width:120px;height:7px;border-radius:99px;
  background:var(--bd);overflow:hidden}
.mk-topo .mk-barra i{display:block;height:100%;background:var(--ok);
  border-radius:99px;transition:width .2s}
.mk-topo button{background:none;border:1px solid var(--bd);color:var(--tx3);
  border-radius:8px;padding:5px 11px;font-size:.82rem;cursor:pointer}
.mk-topo button:hover{color:var(--tx);border-color:var(--vm)}
/* estado da sincronizacao, igual ao das Tarefas mas dentro da barra */
.mk-topo .tf-status{margin-left:0;font-size:12px}
/* o que ja esta pronto sai da lista; o titulo da secao que ficou sem
   nenhuma lista visivel sai junto, para nao sobrar cabecalho solto */
.oculto{display:none!important}
.mk-topo .mk-ver{color:var(--vm);border-color:transparent}
.mk-topo .mk-ver:hover{border-color:var(--vm)}

/* ============================ app de tarefas ============================ */
.tf-topo{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.tf-status{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12.5px;
  color:var(--tx3);white-space:nowrap}
.tf-status .bola{width:8px;height:8px;border-radius:50%;background:var(--tx3);flex:none}
.tf-status.on .bola{background:var(--ok)}
.tf-status.off .bola{background:var(--al)}
.tf-status.erro .bola{background:var(--vm)}

/* caixa de entrada */
.tf-nova{background:var(--card);border:1px solid var(--bd);border-radius:13px;
  padding:14px 16px;box-shadow:var(--sh);margin-bottom:16px;transition:border-color .15s}
.tf-nova:focus-within{border-color:var(--vm);box-shadow:0 0 0 3px rgba(200,16,46,.1)}
.tf-linha{display:flex;gap:10px;align-items:center}
.tf-linha input[type=text]{flex:1;min-width:0;background:none;border:0;color:var(--tx);
  font:16px/1.4 inherit;padding:5px 0}
.tf-linha input[type=text]:focus{outline:none}
.tf-linha input[type=text]::placeholder{color:var(--tx3)}
.tf-add{background:var(--vm);border:0;color:#fff;border-radius:9px;width:38px;height:38px;
  flex:none;display:grid;place-items:center;cursor:pointer;transition:transform .12s,background .15s}
.tf-add:hover{background:#a80d26}
.tf-add:active{transform:scale(.93)}
.tf-add:disabled{opacity:.4;cursor:default;transform:none}
.tf-opts{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:11px;
  padding-top:11px;border-top:1px solid var(--bd)}
.chip{background:var(--card2);border:1px solid var(--bd);border-radius:20px;padding:5px 12px;
  font:600 12.5px/1 inherit;color:var(--tx2);cursor:pointer;transition:all .13s;
  display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.chip:hover{border-color:var(--tx3);color:var(--tx)}
.chip.on{background:var(--vm);border-color:var(--vm);color:#fff}
.chip .pt{width:8px;height:8px;border-radius:50%;flex:none}
.tf-data{background:var(--card2);border:1px solid var(--bd);border-radius:20px;padding:4px 10px;
  color:var(--tx2);font:600 12.5px/1.5 inherit;font-family:inherit}
.tf-data:focus{outline:none;border-color:var(--vm)}
.tf-detectada{background:rgba(15,157,88,.12);border-color:var(--ok);color:var(--ok)}

/* lista */
.tf-grupo{margin-bottom:20px}
.tf-cab{display:flex;align-items:center;gap:9px;margin:0 0 9px;font-size:12.5px;
  font-weight:750;text-transform:uppercase;letter-spacing:.7px;color:var(--tx3)}
.tf-cab .n{background:var(--bd);color:var(--tx2);border-radius:20px;padding:1px 8px;font-size:11px}
.tf-cab.urgente{color:var(--vm)}
.tf-cab.urgente .n{background:var(--vm);color:#fff}
.tf-cab.hoje{color:var(--al)}
.tf-cab.hoje .n{background:var(--al);color:#fff}

.tf-item{display:flex;gap:11px;align-items:flex-start;padding:11px 13px;margin:6px 0;
  background:var(--card);border:1px solid var(--bd);border-radius:11px;
  transition:border-color .15s,transform .12s,opacity .2s;position:relative}
.tf-item:hover{border-color:var(--tx3)}
.tf-item.atrasada{border-left:3px solid var(--vm)}
.tf-item.hoje{border-left:3px solid var(--al)}
.tf-item.feita{opacity:.5}
.tf-item.feita .tf-txt{text-decoration:line-through}
.tf-item.saindo{opacity:0;transform:translateX(14px)}
.tf-check{width:20px;height:20px;border-radius:6px;border:2px solid var(--bd);flex:none;
  margin-top:1px;cursor:pointer;display:grid;place-items:center;background:none;
  color:transparent;transition:all .15s;padding:0}
.tf-check:hover{border-color:var(--ok)}
.tf-item.feita .tf-check{background:var(--ok);border-color:var(--ok);color:#fff}
.tf-corpo{flex:1;min-width:0}
.tf-txt{font-size:14.5px;color:var(--tx);line-height:1.45;overflow-wrap:anywhere}
.tf-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:5px}
.tf-tag{font-size:11.5px;font-weight:650;padding:2px 8px;border-radius:20px;
  display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.tf-tag.dt{background:var(--card2);border:1px solid var(--bd);color:var(--tx2)}
.tf-tag.dt.venc{background:rgba(200,16,46,.12);border-color:var(--vm);color:var(--vm)}
.tf-tag.dt.prox{background:rgba(232,161,58,.15);border-color:var(--al);color:var(--al)}
.tf-tag.cat{color:#fff}
.tf-acoes{display:flex;gap:3px;flex:none;opacity:0;transition:opacity .15s}
.tf-item:hover .tf-acoes,.tf-item:focus-within .tf-acoes{opacity:1}
.tf-ac{background:none;border:0;color:var(--tx3);cursor:pointer;padding:5px;border-radius:6px;
  display:grid;place-items:center;transition:all .13s}
.tf-ac:hover{background:var(--card2);color:var(--tx)}
.tf-ac.del:hover{background:rgba(200,16,46,.12);color:var(--vm)}
/* a propria etiqueta de data e um botao: clicar nela remarca a tarefa */
.tf-tag.dt.mud{font-family:inherit;cursor:pointer}
.tf-tag.dt.mud:hover{border-color:var(--vm);color:var(--vm)}
.tf-dtbox{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:7px}
.tf-dtbox input[type=date]{background:var(--card2);border:1px solid var(--vm);border-radius:8px;
  padding:5px 9px;color:var(--tx);font:600 12.5px/1.5 inherit;font-family:inherit}
.tf-dtbox input[type=date]:focus{outline:none;box-shadow:0 0 0 3px rgba(200,16,46,.1)}
.tf-dtbox .chip{padding:4px 10px;font-size:12px}
.tf-edit{width:100%;background:var(--card2);border:1px solid var(--vm);border-radius:7px;
  padding:6px 9px;color:var(--tx);font:14.5px/1.4 inherit}
.tf-edit:focus{outline:none}

/* estado vazio */
.tf-vazio{text-align:center;padding:44px 20px;color:var(--tx3)}
.tf-vazio svg{opacity:.35;margin-bottom:11px}
.tf-vazio p{font-size:14.5px;margin:0 0 4px;color:var(--tx2)}
.tf-vazio small{font-size:13px}

/* aviso de nao sincronizado */
.tf-pend{display:flex;gap:11px;align-items:flex-start;background:var(--al-bg);
  border:1px solid var(--al);border-left-width:4px;border-radius:11px;padding:13px 16px;
  margin-bottom:15px;font-size:13.5px;color:var(--tx2)}
.tf-pend svg{color:var(--al);flex:none;margin-top:1px}
.tf-pend b{color:var(--tx);display:block;margin-bottom:2px}
.tf-pend button{margin-top:8px}

/* botoes gerais */
.btn{background:var(--card);border:1px solid var(--bd);border-radius:9px;padding:8px 14px;
  font:650 13px/1 inherit;color:var(--tx2);cursor:pointer;display:inline-flex;
  align-items:center;gap:7px;transition:all .13s}
.btn:hover{border-color:var(--tx3);color:var(--tx)}
.btn.pri{background:var(--vm);border-color:var(--vm);color:#fff}
.btn.pri:hover{background:#a80d26;border-color:#a80d26;color:#fff}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn:disabled:hover{border-color:var(--bd);color:var(--tx2)}
.btn.pri:disabled:hover{background:var(--vm);border-color:var(--vm);color:#fff}

/* modal */
.modal{position:fixed;inset:0;background:rgba(10,12,16,.62);display:none;place-items:center;
  z-index:50;padding:20px;backdrop-filter:blur(3px)}
.modal.on{display:grid}
.modal-cx{background:var(--card);border:1px solid var(--bd);border-radius:15px;
  box-shadow:0 20px 60px rgba(0,0,0,.35);max-width:560px;width:100%;max-height:86vh;
  display:flex;flex-direction:column;animation:sobe .2s ease}
.modal-cab{display:flex;align-items:center;gap:11px;padding:18px 20px 14px;
  border-bottom:1px solid var(--bd)}
.modal-cab h3{font-size:16px;font-weight:700;flex:1}
.modal-corpo{padding:18px 20px;overflow-y:auto}
.modal-corpo p{font-size:13.5px;color:var(--tx2);margin-bottom:12px}
.modal-corpo textarea{width:100%;min-height:190px;background:var(--card2);border:1px solid var(--bd);
  border-radius:9px;padding:12px;color:var(--tx);font:12.5px/1.6 ui-monospace,Consolas,monospace;
  resize:vertical}
.modal-corpo textarea:focus{outline:none;border-color:var(--vm)}
.modal-corpo label{display:block;font-size:12.5px;font-weight:650;color:var(--tx2);
  margin:0 0 6px}
.modal-corpo input[type=email],.modal-corpo input[type=password]{width:100%;
  background:var(--card2);border:1px solid var(--bd);border-radius:9px;padding:10px 12px;
  color:var(--tx);font:14.5px/1.4 inherit;margin-bottom:13px}
.modal-corpo input:focus{outline:none;border-color:var(--vm)}
.modal-rod{display:flex;gap:9px;justify-content:flex-end;padding:14px 20px;
  border-top:1px solid var(--bd);flex-wrap:wrap}
.modal-erro{background:rgba(200,16,46,.1);border:1px solid var(--vm);color:var(--vm);
  border-radius:9px;padding:10px 13px;font-size:13px;margin-bottom:13px;display:none}
.modal-erro.on{display:block}
.aviso-cx{background:var(--card2);border:1px solid var(--bd);border-radius:9px;
  padding:11px 13px;font-size:12.5px;color:var(--tx2);margin-bottom:13px;line-height:1.55}

/* busca: destaque e ocultacao */
mark{background:rgba(232,161,58,.35);color:inherit;border-radius:3px;padding:0 2px}
.sem-res{text-align:center;color:var(--tx3);padding:40px 20px;font-size:14px}
.rodape{text-align:center;color:var(--tx3);font-size:12.5px;padding:8px 0 0}
.rodape code{font-size:11.5px}

@media(max-width:640px){
  /* no celular o contador desce inteiro para a linha de baixo, alinhado a
     direita, para o texto do item nao ficar espremido numa coluna estreita.
     O texto mantem o flex-basis 0 da regra base, senao ele proprio quebra
     de linha e deixa a caixinha sozinha la em cima. */
  .mk-qtd{flex-basis:100%;justify-content:flex-end;margin-left:0}
  .wrap,main{padding-left:14px;padding-right:14px}
  .marca h1{font-size:16.5px}
  .marca p{font-size:11.5px}
  .brasao{width:36px;height:36px;font-size:11px}
  .card{padding:18px 16px;border-radius:11px}
  .kpi .val{font-size:25px}
  .grade{grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
  nav button{padding:11px 11px 12px;font-size:12.5px}
  .busca{max-width:none}
  .tf-acoes{opacity:1}
  .tf-nova{padding:12px 13px}
  .tf-opts{gap:6px}
  .chip{padding:5px 10px;font-size:12px}
  .modal{padding:12px;align-items:flex-end}
  .modal-cx{max-height:92vh}
  .modal-rod{justify-content:stretch}
  .modal-rod .btn{flex:1;justify-content:center}
}
@media print{.topo,nav,.busca,.acoes{display:none}.aba{display:block!important}}
"""

JS_TAREFAS = r"""
/* =================== app de tarefas: local + Supabase =================== */
(function(){
  var CHAVE='cao-tarefas', CHAVE_FILA='cao-fila', CHAVE_SES='cao-sessao';
  var el=function(s,r){return (r||document).querySelector(s)};
  var hoje=function(){var d=new Date();d.setHours(0,0,0,0);return d};
  var iso=function(d){
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+
           String(d.getDate()).padStart(2,'0');
  };
  var deIso=function(s){
    if(!s)return null;
    var p=s.split('-'); var d=new Date(+p[0],+p[1]-1,+p[2]); d.setHours(0,0,0,0); return d;
  };
  var dias=function(a,b){return Math.round((b-a)/86400000)};
  var uid=function(){
    return 't'+Date.now().toString(36)+Math.floor(Math.random()*1e6).toString(36);
  };
  var norm=function(s){
    return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim();
  };

  var CATS={};
  CATEGORIAS.forEach(function(c){CATS[c[0]]={rot:c[1],cor:c[2]}});

  /* ---------------------------- armazenamento ---------------------------- */
  var lerLS=function(k,pad){
    try{var v=localStorage.getItem(k);return v?JSON.parse(v):pad}catch(e){return pad}
  };
  var gravarLS=function(k,v){
    try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}
  };

  /* Fila de exclusoes a propagar para a nuvem. Definida aqui porque a poda
     abaixo precisa dela e este bloco carrega antes da camada de sincronizacao,
     que le a mesma chave. */
  window.K_APAGADAS='cao-apagadas';
  var K_APAGADAS=window.K_APAGADAS;

  /* tarefas vindas do TAREFAS.md viram a base; ganham id estavel pelo texto */
  var idBase=function(t){
    var s=norm(t), h=0;
    for(var i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0}
    return 'md'+Math.abs(h).toString(36);
  };

  var tarefas=[];

  function carregar(){
    var locais=lerLS(CHAVE,null);
    if(locais===null){
      /* primeira vez: semeia com o que veio do TAREFAS.md */
      tarefas=BASE.map(function(b){
        return {id:idBase(b.t),txt:b.t,data:b.d||null,cat:b.c||'',feito:!!b.f,
                orig:'md',mod:new Date().toISOString(),sinc:true};
      });
      gravarLS(CHAVE,tarefas);
    }else{
      tarefas=locais;
      /* traz do .md o que ainda nao existe aqui (ex.: editei o .md na mao) */
      var vistos={};
      tarefas.forEach(function(t){vistos[norm(t.txt)]=1});
      BASE.forEach(function(b){
        if(!vistos[norm(b.t)]){
          tarefas.push({id:idBase(b.t),txt:b.t,data:b.d||null,cat:b.c||'',feito:!!b.f,
                        orig:'md',mod:new Date().toISOString(),sinc:true});
        }
      });
      podarSumidasDoArquivo();
    }
  }

  /* Tira daqui a tarefa que veio do TAREFAS.md e nao existe mais nele.
     O id de uma tarefa do arquivo e derivado do texto (idBase, prefixo "md"),
     entao reescrever a linha no .md gera id novo. Sem esta poda o registro
     antigo ficava para sempre e cada reescrita virava uma duplicata: em
     12/08/2026 a aba mostrava 38 pendentes com 21 no arquivo, porque as
     tarefas foram reescritas varias vezes no mesmo dia.

     Regra: para o que nasceu no arquivo, o arquivo manda. Tarefa criada no
     painel tem id com prefixo "t" (uid) e nunca e podada. */
  function podarSumidasDoArquivo(){
    if(!BASE.length)return;          /* arquivo vazio ou ilegivel: nao poda nada */
    var noArquivo={};
    BASE.forEach(function(b){noArquivo[idBase(b.t)]=1});
    var mortas=tarefas.filter(function(t){
      return String(t.id).indexOf('md')===0 && !noArquivo[t.id];
    });
    if(!mortas.length)return;
    var fora={};
    mortas.forEach(function(t){fora[t.id]=1});
    tarefas=tarefas.filter(function(t){return !fora[t.id]});
    /* a nuvem tem que esquecer junto, senao a proxima sincronizacao traz
       tudo de volta: a mescla remota readiciona por id o que nao existe aqui */
    var lista=lerLS(K_APAGADAS,[]);
    mortas.forEach(function(t){if(lista.indexOf(t.id)<0)lista.push(t.id)});
    gravarLS(K_APAGADAS,lista);
    gravarLS(CHAVE,tarefas);
  }

  function salvar(){gravarLS(CHAVE,tarefas);desenhar();}

  /* ------------------------ datas em portugues -------------------------- */
  var SEMANA=['domingo','segunda','terca','quarta','quinta','sexta','sabado'];
  var MESES=['janeiro','fevereiro','marco','abril','maio','junho','julho','agosto',
             'setembro','outubro','novembro','dezembro'];

  /* le expressoes de data no texto e devolve {data, texto} */
  function lerData(txt){
    var h=hoje(), t=txt, achou=null;
    var tenta=function(re,fn){
      if(achou)return;
      var m=t.match(re);
      if(m){var d=fn(m);if(d){achou=d;t=t.replace(m[0],' ').replace(/\s{2,}/g,' ').trim();}}
    };
    var n=function(s){return norm(s)};

    /* dd/mm ou dd/mm/aaaa */
    tenta(/\b(\d{1,2})[\/.-](\d{1,2})(?:[\/.-](\d{2,4}))?\b/,function(m){
      var dia=+m[1],mes=+m[2],ano=m[3]?+m[3]:h.getFullYear();
      if(ano<100)ano+=2000;
      if(mes<1||mes>12||dia<1||dia>31)return null;
      var d=new Date(ano,mes-1,dia); d.setHours(0,0,0,0);
      if(d.getMonth()!==mes-1)return null;
      /* sem ano informado: se ja passou ha pouco, e tarefa atrasada deste ano;
         so joga para o ano seguinte se ficou muito para tras */
      if(!m[3]&&dias(d,h)>60)d.setFullYear(ano+1);
      return d;
    });
    /* "dia 15" */
    tenta(/\bdia\s+(\d{1,2})\b/i,function(m){
      var dia=+m[1]; if(dia<1||dia>31)return null;
      var d=new Date(h.getFullYear(),h.getMonth(),dia); d.setHours(0,0,0,0);
      if(d.getDate()!==dia)return null;
      /* dia que ja passou neste mes: assume o mes que vem */
      if(d<h){d=new Date(h.getFullYear(),h.getMonth()+1,dia);d.setHours(0,0,0,0)}
      return d;
    });
    /* "15 de setembro" */
    tenta(new RegExp('\\b(\\d{1,2})\\s+de\\s+('+MESES.join('|')+
                     '|marc\\u00e7o|fev|jan|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\\w*','i'),
      function(m){
        var dia=+m[1], alvo=n(m[2]), mes=-1;
        MESES.forEach(function(nm,i){if(nm.indexOf(alvo)===0||alvo.indexOf(nm.slice(0,3))===0)mes=i});
        if(mes<0)return null;
        var d=new Date(h.getFullYear(),mes,dia); d.setHours(0,0,0,0);
        if(d<h)d.setFullYear(h.getFullYear()+1);
        return d;
      });
    /* hoje / amanha / depois de amanha */
    tenta(/\bdepois\s+de\s+amanh[aã]\b/i,function(){
      var d=new Date(h);d.setDate(d.getDate()+2);return d;});
    tenta(/\bamanh[aã]\b/i,function(){var d=new Date(h);d.setDate(d.getDate()+1);return d;});
    tenta(/\bhoje\b/i,function(){return new Date(h)});
    /* "em 3 dias" / "em 2 semanas" */
    tenta(/\bem\s+(\d{1,3})\s+(dias?|semanas?|m[eê]s(?:es)?)\b/i,function(m){
      var q=+m[1], u=n(m[2]), d=new Date(h);
      if(u.indexOf('dia')===0)d.setDate(d.getDate()+q);
      else if(u.indexOf('semana')===0)d.setDate(d.getDate()+q*7);
      else d.setMonth(d.getMonth()+q);
      return d;
    });
    /* "semana que vem" */
    tenta(/\b(?:semana\s+que\s+vem|pr[oó]xima\s+semana)\b/i,function(){
      var d=new Date(h);d.setDate(d.getDate()+7);return d;});
    /* dia da semana, opcionalmente com "que vem" */
    tenta(new RegExp('\\b(?:na\\s+|no\\s+|)(segunda|ter[cç]a|quarta|quinta|sexta|s[aá]bado|domingo)'+
                     '(?:-feira|\\s+feira)?(\\s+que\\s+vem|\\s+pr[oó]xima?)?\\b','i'),
      function(m){
        var alvo=n(m[1]).replace('feira','').trim(), idx=-1;
        SEMANA.forEach(function(nm,i){if(nm.indexOf(alvo)===0)idx=i});
        if(idx<0)return null;
        var d=new Date(h), delta=(idx-d.getDay()+7)%7;
        if(delta===0)delta=7;
        d.setDate(d.getDate()+delta);
        if(m[2])d.setDate(d.getDate()+7);
        return d;
      });
    return {data:achou,texto:t.replace(/\s{2,}/g,' ').trim()};
  }

  function rotuloData(d){
    if(!d)return '';
    var h=hoje(), n=dias(h,d);
    if(n===0)return 'hoje';
    if(n===1)return 'amanhã';
    if(n===-1)return 'ontem';
    if(n<0)return Math.abs(n)+' dias atrás';
    if(n<7)return SEMANA[d.getDay()].replace('terca','terça').replace('sabado','sábado');
    var s=String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0');
    if(d.getFullYear()!==h.getFullYear())s+='/'+d.getFullYear();
    return s;
  }

  /* ------------------------------ interface ------------------------------ */
  var inp=el('#tf-txt'), btAdd=el('#tf-add'), inData=el('#tf-dt'), lista=el('#tf-lista');
  var catSel='';

  function pintaChips(){
    [].forEach.call(document.querySelectorAll('#tf-cats .chip'),function(c){
      c.classList.toggle('on',c.dataset.cat===catSel);
    });
  }

  /* enquanto digita, mostra a data que foi entendida */
  function previa(){
    var r=lerData(inp.value);
    if(r.data){
      inData.value=iso(r.data);
      inData.classList.add('tf-detectada');
      inData.title='Data entendida do texto: '+rotuloData(r.data);
    }else{
      /* limpa so o que veio da deteccao; data escolhida a mao permanece */
      if(inData.classList.contains('tf-detectada'))inData.value='';
      inData.classList.remove('tf-detectada');
      inData.title='';
    }
    btAdd.disabled=!inp.value.trim();
  }

  function adicionar(){
    var bruto=inp.value.trim();
    if(!bruto)return;
    var r=lerData(bruto);
    var d=inData.value?deIso(inData.value):r.data;
    var texto=r.data?r.texto:bruto;
    if(!texto)texto=bruto;
    var nova={id:uid(),txt:texto,data:d?iso(d):null,cat:catSel,feito:false,
              orig:'local',mod:new Date().toISOString(),sinc:false};
    tarefas.unshift(nova);
    inp.value='';inData.value='';inData.classList.remove('tf-detectada');
    btAdd.disabled=true;
    salvar();
    if(window.SUPA&&SUPA.ativo())SUPA.enviar(nova);
    inp.focus();
  }

  function alternar(id){
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!t)return;
    t.feito=!t.feito;t.mod=new Date().toISOString();t.sinc=false;
    salvar();
    if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
  }

  function excluir(id){
    var i=-1;
    tarefas.forEach(function(t,k){if(t.id===id)i=k});
    if(i<0)return;
    var t=tarefas[i];
    var no=el('[data-id="'+id+'"]');
    if(no)no.classList.add('saindo');
    setTimeout(function(){
      tarefas.splice(i,1);salvar();
      if(window.SUPA&&SUPA.ativo())SUPA.apagar(t);
    },160);
  }

  function editar(id){
    var no=el('[data-id="'+id+'"]');
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!no||!t)return;
    var corpo=el('.tf-corpo',no);
    var antigo=corpo.innerHTML;
    corpo.innerHTML='<input class="tf-edit" type="text">';
    var campo=el('.tf-edit',corpo);
    campo.value=t.txt;campo.focus();campo.select();
    var fim=function(ok){
      if(ok&&campo.value.trim()){
        t.txt=campo.value.trim();t.mod=new Date().toISOString();t.sinc=false;
        salvar();
        if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
      }else{corpo.innerHTML=antigo;}
    };
    campo.onblur=function(){fim(true)};
    campo.onkeydown=function(e){
      if(e.key==='Enter'){e.preventDefault();campo.onblur=null;fim(true)}
      if(e.key==='Escape'){campo.onblur=null;fim(false)}
    };
  }

  /* Remarcar: troca a data de uma tarefa que ja existe.
     Sem confirmar no blur de proposito. O seletor nativo de data do celular
     tira o foco do campo ao abrir; se blur cancelasse, a edicao morreria
     justamente no aparelho em que ela mais e usada. Sai por Enter, por um
     dos atalhos, pelo Escape ou pelo botao Cancelar. */
  function editarData(id){
    var no=el('[data-id="'+id+'"]');
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!no||!t)return;
    var corpo=el('.tf-corpo',no);
    var antigo=corpo.innerHTML;
    corpo.innerHTML='<div class="tf-txt">'+esc(t.txt)+'</div>'+
      '<div class="tf-dtbox">'+
        '<input type="date" class="tf-dtin" value="'+(t.data||'')+'">'+
        '<button class="chip" data-q="0">Hoje</button>'+
        '<button class="chip" data-q="1">Amanhã</button>'+
        '<button class="chip" data-q="7">+1 semana</button>'+
        (t.data?'<button class="chip" data-q="x">Sem data</button>':'')+
        '<button class="chip" data-q="c">Cancelar</button>'+
      '</div>';
    var campo=el('.tf-dtin',corpo), pronto=false;

    var cancelar=function(){
      if(pronto)return; pronto=true; corpo.innerHTML=antigo;
    };
    var aplicar=function(valor){
      if(pronto)return; pronto=true;
      valor=valor||null;
      if(valor===(t.data||null)){corpo.innerHTML=antigo;return}
      t.data=valor;t.mod=new Date().toISOString();t.sinc=false;
      salvar();   /* redesenha: a tarefa pula sozinha para o grupo certo */
      if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
    };

    campo.focus();
    campo.onchange=function(){aplicar(campo.value)};
    campo.onkeydown=function(e){
      if(e.key==='Enter'){e.preventDefault();aplicar(campo.value)}
      if(e.key==='Escape'){e.preventDefault();cancelar()}
    };
    /* mousedown, nao click: dispara antes de qualquer perda de foco */
    [].forEach.call(corpo.querySelectorAll('.chip'),function(c){
      c.onmousedown=function(e){
        e.preventDefault();
        var q=c.dataset.q;
        if(q==='c')return cancelar();
        if(q==='x')return aplicar(null);
        var d=hoje(); d.setDate(d.getDate()+parseInt(q,10));
        aplicar(iso(d));
      };
    });
  }

  /* ---------------------- divergencia com o TAREFAS.md -------------------
     A BASE e exatamente o que o arquivo diz hoje. Comparar contra ela e o
     unico jeito honesto de saber se o repositorio esta velho.
     Nao confundir com t.sinc, que e a flag do Supabase: subir para a nuvem
     nao escreve uma linha no .md. O aviso antigo usava t.sinc e por isso
     mentia dos dois lados (sumia ao sincronizar, ficava aceso sem login). */
  function divergencias(){
    var doArquivo={};
    BASE.forEach(function(b){doArquivo[norm(b.t)]=b});
    var d={novas:0,remarcadas:0,alteradas:0,excluidas:0,total:0}, vistos={};
    tarefas.forEach(function(t){
      var k=norm(t.txt); vistos[k]=1;
      var b=doArquivo[k];
      if(!b){d.novas++;return}
      if((b.d||null)!==(t.data||null))d.remarcadas++;
      else if((b.c||'')!==(t.cat||'')||!!b.f!==!!t.feito)d.alteradas++;
    });
    BASE.forEach(function(b){if(!vistos[norm(b.t)])d.excluidas++});
    d.total=d.novas+d.remarcadas+d.alteradas+d.excluidas;
    return d;
  }

  function fraseDivergencia(d){
    if(!d.total)return '';
    var p=[], n=function(q,um,varios){if(q)p.push(q+' '+(q===1?um:varios))};
    n(d.novas,'nova','novas');
    n(d.remarcadas,'remarcada','remarcadas');
    n(d.alteradas,'alterada','alteradas');
    n(d.excluidas,'excluída aqui','excluídas aqui');
    /* um tipo so: frase direta. Varios: total na frente e o detalhe atras. */
    if(p.length===1){
      return (d.total===1?'1 tarefa ':d.total+' tarefas ')+p[0].replace(/^\d+\s/,'')+
             (d.total===1?' ainda não foi':' ainda não foram')+' para o TAREFAS.md';
    }
    var lista=p.slice(0,-1).join(', ')+' e '+p[p.length-1];
    return d.total+' mudanças ainda não foram para o TAREFAS.md: '+lista;
  }

  /* agrupa por urgencia */
  function agrupar(){
    var h=hoje();
    var g={atrasadas:[],hoje:[],amanha:[],semana:[],depois:[],semdata:[],feitas:[]};
    tarefas.forEach(function(t){
      if(t.feito){g.feitas.push(t);return}
      if(!t.data){g.semdata.push(t);return}
      var n=dias(h,deIso(t.data));
      if(n<0)g.atrasadas.push(t);
      else if(n===0)g.hoje.push(t);
      else if(n===1)g.amanha.push(t);
      else if(n<=7)g.semana.push(t);
      else g.depois.push(t);
    });
    var porData=function(a,b){
      if(!a.data)return 1; if(!b.data)return -1;
      return a.data<b.data?-1:a.data>b.data?1:0;
    };
    ['atrasadas','hoje','amanha','semana','depois'].forEach(function(k){g[k].sort(porData)});
    g.feitas.sort(function(a,b){return (b.mod||'')<(a.mod||'')?-1:1});
    return g;
  }

  function itemHTML(t){
    var h=hoje(), d=t.data?deIso(t.data):null, n=d?dias(h,d):null;
    var cls='tf-item'+(t.feito?' feita':'')+
            (!t.feito&&n!==null&&n<0?' atrasada':'')+
            (!t.feito&&n===0?' hoje':'');
    var meta='';
    if(d){
      var dc=(!t.feito&&n<0)?' venc':((!t.feito&&n<=1)?' prox':'');
      meta+='<button class="tf-tag dt mud'+dc+'" data-ac="dt" '+
            'title="Mudar a data desta tarefa">'+ICO.cal+rotuloData(d)+'</button>';
    }
    if(t.cat&&CATS[t.cat]){
      meta+='<span class="tf-tag cat" style="background:'+CATS[t.cat].cor+'">'+
            CATS[t.cat].rot+'</span>';
    }
    if(!t.sinc&&window.SUPA&&SUPA.ativo()){
      meta+='<span class="tf-tag dt" title="Ainda não sincronizada">•</span>';
    }
    return '<div class="'+cls+'" data-id="'+t.id+'">'+
      '<button class="tf-check" data-ac="ok" title="Marcar como feita">'+ICO.check+'</button>'+
      '<div class="tf-corpo"><div class="tf-txt">'+esc(t.txt)+'</div>'+
      (meta?'<div class="tf-meta">'+meta+'</div>':'')+'</div>'+
      '<div class="tf-acoes">'+
        '<button class="tf-ac" data-ac="dt" title="'+
          (d?'Mudar a data':'Marcar uma data')+'">'+ICO.calbt+'</button>'+
        '<button class="tf-ac" data-ac="ed" title="Editar o texto">'+ICO.lapis+'</button>'+
        '<button class="tf-ac del" data-ac="del" title="Excluir">'+ICO.lixo+'</button>'+
      '</div></div>';
  }

  function esc(s){
    return String(s).replace(/[&<>"]/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});
  }

  function desenhar(){
    var g=agrupar();
    var out='';
    var bloco=function(chave,rot,cls){
      var arr=g[chave];
      if(!arr.length)return;
      out+='<div class="tf-grupo"><div class="tf-cab '+(cls||'')+'">'+rot+
           '<span class="n">'+arr.length+'</span></div>'+
           arr.map(itemHTML).join('')+'</div>';
    };
    bloco('atrasadas','Atrasadas','urgente');
    bloco('hoje','Hoje','hoje');
    bloco('amanha','Amanhã');
    bloco('semana','Próximos 7 dias');
    bloco('depois','Mais adiante');
    bloco('semdata','Sem data');
    bloco('feitas','Concluídas');

    if(!tarefas.length){
      out='<div class="tf-vazio">'+ICO.vazio+
          '<p>Nenhuma tarefa por aqui.</p>'+
          '<small>Escreva acima, por exemplo: "entregar artigo sexta".</small></div>';
    }
    lista.innerHTML=out;

    /* o que ainda nao foi para o TAREFAS.md */
    var dv=divergencias();
    var cx=el('#tf-pend');
    if(cx){
      cx.style.display=dv.total?'flex':'none';
      var b=el('#tf-pend-n');
      if(b)b.textContent=fraseDivergencia(dv);
    }
    /* badge da aba */
    var pend=tarefas.filter(function(t){return !t.feito}).length;
    var atras=g.atrasadas.length;
    var badge=el('nav button[data-aba="tarefas"] .pill:not(.pill-b)');
    if(badge){
      badge.textContent=pend||'';
      badge.style.display=pend?'':'none';
      badge.style.background=atras?'#fff':'';
      badge.style.color=atras?'var(--vm)':'';
      badge.title=atras?atras+' atrasada(s)':'';
    }
    /* cartao da home */
    var kv=el('#kpi-tar-val'), ks=el('#kpi-tar-sub');
    if(kv){
      kv.textContent=pend;
      ks.textContent=atras?(atras+(atras===1?' atrasada':' atrasadas')):
                     (g.hoje.length?(g.hoje.length+' para hoje'):'nenhuma atrasada');
      ks.style.color=atras?'var(--vm)':'';
    }
    /* guia do dia (cartao de abertura): mesma fonte, outra leitura */
    if(window.GUIA)GUIA.tarefas(g);
  }

  /* -------------------------- exportar / importar ------------------------ */
  function paraMarkdown(){
    var g=agrupar();
    var linha=function(t){
      var s='- ['+(t.feito?'x':' ')+'] '+t.txt;
      if(t.data){
        var d=deIso(t.data);
        s+=' ['+String(d.getDate()).padStart(2,'0')+'/'+
           String(d.getMonth()+1).padStart(2,'0')+'/'+d.getFullYear()+']';
      }
      if(t.cat)s+=' #'+t.cat;
      return s;
    };
    /* A secao (###) de cada tarefa vem do arquivo, procurada pelo texto. Sem
       isto o exportado saia como lista corrida e colar por cima apagava os
       subtitulos ("Reta final...", "Segunda, 17/08"). Tarefa criada no painel
       nao tem secao e sai solta, logo abaixo de "## Pendentes", que e o unico
       lugar onde ela cabe sem mentir sobre a secao a que pertence. */
    var secaoDe={}, ordem=[];
    BASE.forEach(function(b){
      var s=b.s||'';
      secaoDe[norm(b.t)]=s;
      if(s&&ordem.indexOf(s)<0)ordem.push(s);
    });

    var pend=g.atrasadas.concat(g.hoje,g.amanha,g.semana,g.depois,g.semdata);
    var grupos={};
    pend.forEach(function(t){
      var s=secaoDe[norm(t.txt)]||'';
      (grupos[s]=grupos[s]||[]).push(t);
    });

    var corpo='';
    if(grupos[''])corpo+=grupos[''].map(linha).join('\n')+'\n';
    ordem.forEach(function(s){
      if(!grupos[s])return;            /* secao que esvaziou sai junto */
      corpo+='\n### '+s+'\n'+grupos[s].map(linha).join('\n')+'\n';
    });
    if(!pend.length)corpo='- [ ] ...\n';

    /* o topo vem do proprio arquivo (TAR_CAB); o texto abaixo e so a rede de
       seguranca para quando o TAREFAS.md nao existe ainda */
    var cab=(window.TAR_CAB||'').trim();
    if(!cab){
      cab='# TAREFAS — CAO 2026\n\n'+
          '> Lista de tarefas correntes do curso. Marcar como feito, não apagar '+
          '(histórico do que já foi cumprido).\n> Editável aqui ou pelo painel '+
          '(aba Tarefas). Formato: `- [ ] texto [dd/mm/aaaa] #categoria`.';
    }
    /* Na tela as concluidas aparecem pela ordem em que foram mexidas, que e o
       util para conferir o que voce acabou de fazer. No arquivo elas vao pela
       data da tarefa, mais recente em cima, igual ao sincroniza_tarefas.py: se
       os dois usassem criterios diferentes, cada um reordenaria o bloco por
       cima do outro e o TAREFAS.md geraria commit sem nada ter mudado. */
    var feitas=g.feitas.slice().sort(function(a,b){
      return (b.data||'')<(a.data||'')?-1:((b.data||'')>(a.data||'')?1:0);
    });
    return cab+'\n\n## Pendentes\n'+corpo+
           '\n## Concluídas\n'+(feitas.length?feitas.map(linha).join('\n')+'\n':'');
  }

  function abrirModal(id){el(id).classList.add('on')}
  function fecharModal(id){el(id).classList.remove('on')}

  el('#tf-exportar').onclick=function(){
    el('#exp-txt').value=paraMarkdown();
    abrirModal('#modal-exp');
    setTimeout(function(){el('#exp-txt').select()},60);
  };
  el('#exp-copiar').onclick=function(){
    var ta=el('#exp-txt');
    ta.select();
    var ok=false;
    try{ok=document.execCommand('copy')}catch(e){}
    if(navigator.clipboard&&!ok){navigator.clipboard.writeText(ta.value);ok=true}
    var b=el('#exp-copiar');
    b.textContent=ok?'Copiado':'Selecione e copie';
    setTimeout(function(){b.innerHTML=ICO.copiar+'Copiar';},1800);
    /* Copiar NAO mexe em t.sinc. Aqui era o resto do desenho antigo, de quando
       exportar significava "ja esta no arquivo, considera sincronizado". Como
       t.sinc e a fila de upload (a sincronizacao sobe so quem tem sinc=false),
       marcar tudo como sincronizado aqui zerava a fila: exportar sem internet
       ou sem login jogava fora alteracoes que nunca tinham subido para a nuvem,
       e o outro aparelho nunca as recebia. Quem escreve no .md e o colar, e
       quem informa o estado da nuvem e a linha de status. Corrigido 14/08/2026. */
  };
  [].forEach.call(document.querySelectorAll('[data-fechar]'),function(b){
    b.onclick=function(){fecharModal('#'+b.dataset.fechar)};
  });
  [].forEach.call(document.querySelectorAll('.modal'),function(m){
    m.onclick=function(e){if(e.target===m)m.classList.remove('on')};
  });

  /* ------------------------------- eventos ------------------------------- */
  inp.oninput=previa;
  inp.onkeydown=function(e){if(e.key==='Enter'){e.preventDefault();adicionar()}};
  btAdd.onclick=adicionar;
  inData.onchange=function(){inData.classList.remove('tf-detectada')};

  el('#tf-cats').onclick=function(e){
    var c=e.target.closest('.chip');
    if(!c)return;
    catSel=(catSel===c.dataset.cat)?'':c.dataset.cat;
    pintaChips();
  };
  [].forEach.call(document.querySelectorAll('#tf-rapidas .chip'),function(c){
    c.onclick=function(){
      var h=hoje(), d=new Date(h);
      var q=c.dataset.q;
      if(q==='hoje'){}
      else if(q==='amanha')d.setDate(d.getDate()+1);
      else if(q==='semana')d.setDate(d.getDate()+7);
      else{inData.value='';inData.classList.remove('tf-detectada');inp.focus();return}
      inData.value=iso(d);inData.classList.remove('tf-detectada');inp.focus();
    };
  });

  lista.onclick=function(e){
    var b=e.target.closest('[data-ac]');
    if(!b)return;
    var id=b.closest('.tf-item').dataset.id;
    if(b.dataset.ac==='ok')alternar(id);
    else if(b.dataset.ac==='del')excluir(id);
    else if(b.dataset.ac==='ed')editar(id);
    else if(b.dataset.ac==='dt')editarData(id);
  };

  carregar();
  desenhar();
  previa();

  /* exposto para a camada de sincronizacao */
  window.TAREFAS={
    todas:function(){return tarefas},
    definir:function(novas){tarefas=novas;salvar()},
    redesenhar:desenhar,
    salvar:function(){gravarLS(CHAVE,tarefas)},
    modal:{abrir:abrirModal,fechar:fecharModal}
  };
})();
"""

JS_SUPABASE = r"""
/* ============ sincronizacao com Supabase (opcional, offline-first) ========
   O painel funciona 100% sem isto. Se CFG.url estiver vazio, ou se a pessoa
   nao estiver logada, tudo continua salvo apenas no navegador.
   A chave usada aqui e a "anon", publica por natureza: quem protege os dados
   e o RLS no banco (cada linha so e visivel para o dono).                    */
(function(){
  var CFG=window.SUPA_CFG||{};
  var K_SES='cao-sessao', K_DEL=window.K_APAGADAS||'cao-apagadas';
  var el=function(s){return document.querySelector(s)};
  var ses=null, sincronizando=false;

  var lerLS=function(k,p){try{var v=localStorage.getItem(k);return v?JSON.parse(v):p}
                          catch(e){return p}};
  var gravarLS=function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};

  function ativo(){return !!(CFG.url&&CFG.key&&ses&&ses.access_token)}
  function configurado(){return !!(CFG.url&&CFG.key)}

  /* ------------------------------ interface ------------------------------ */
  function estado(cls,txt,tit){
    var s=el('#tf-status');
    if(!s)return;
    s.className='tf-status'+(cls?' '+cls:'');
    el('#tf-status-txt').textContent=txt;
    s.title=tit||'';
  }
  function pintaConta(){
    /* o mesmo estado vai para a aba Tarefas e para a barra das abas de lista */
    if(ativo()){
      estado('on','Sincronizado','Suas tarefas estão salvas na nuvem');
      tic('on','Salvo na nuvem','Suas marcações estão sincronizadas');
    }else if(configurado()){
      estado('','Somente neste aparelho','Entre na conta para sincronizar');
      tic('','Somente neste aparelho',
          'Entre na conta, na aba Tarefas, para sincronizar entre aparelhos');
    }else{
      estado('','Somente neste aparelho',
             'A sincronização ainda não foi configurada neste painel');
      tic('','Somente neste aparelho',
          'A sincronização ainda não foi configurada neste painel');
    }
    var rot=el('#tf-conta-rot');
    if(rot)rot.textContent=ativo()?(ses.email||'Conta').split('@')[0]:'Entrar';
  }

  /* ------------------------------- rede ---------------------------------- */
  function api(caminho,opts){
    opts=opts||{};
    var h=opts.headers||{};
    h['apikey']=CFG.key;
    h['Content-Type']='application/json';
    if(ses&&ses.access_token)h['Authorization']='Bearer '+ses.access_token;
    opts.headers=h;
    return fetch(CFG.url.replace(/\/+$/,'')+caminho,opts).then(function(r){
      /* PostgREST com Prefer:return=minimal devolve corpo vazio em varios
         status (200, 201, 204, conforme o caso) - nao so em 204. Tentar
         fazer r.json() num corpo vazio derruba a promise com um erro de
         parse que mascara um sucesso real. */
      return r.text().then(function(txt){
        var j=null;
        if(txt){
          try{j=JSON.parse(txt)}
          catch(e){ if(r.ok)return null; }
        }
        if(!r.ok){
          var e=new Error((j&&(j.msg||j.message||j.error_description||j.error))||('HTTP '+r.status));
          e.status=r.status;
          throw e;
        }
        return j;
      });
    });
  }

  function entrar(email,senha){
    return api('/auth/v1/token?grant_type=password',{
      method:'POST',body:JSON.stringify({email:email,password:senha})
    }).then(function(j){
      ses={access_token:j.access_token,refresh_token:j.refresh_token,
           email:(j.user&&j.user.email)||email,uid:j.user&&j.user.id,
           exp:Date.now()+((j.expires_in||3600)*1000)};
      gravarLS(K_SES,ses);
      pintaConta();
      return sincronizar();
    });
  }

  function renovar(){
    if(!ses||!ses.refresh_token)return Promise.reject(new Error('sem sessão'));
    return api('/auth/v1/token?grant_type=refresh_token',{
      method:'POST',body:JSON.stringify({refresh_token:ses.refresh_token})
    }).then(function(j){
      ses.access_token=j.access_token;
      ses.refresh_token=j.refresh_token||ses.refresh_token;
      ses.exp=Date.now()+((j.expires_in||3600)*1000);
      gravarLS(K_SES,ses);
      return ses;
    });
  }

  function garantirSessao(){
    if(!ses)return Promise.reject(new Error('sem sessão'));
    if(ses.exp&&Date.now()>ses.exp-60000)return renovar();
    return Promise.resolve(ses);
  }

  function sair(){
    ses=null;
    try{localStorage.removeItem(K_SES)}catch(e){}
    pintaConta();
  }

  /* --------------------------- sincronizacao ----------------------------- */
  var paraLinha=function(t){
    return {id:t.id,txt:t.txt,data:t.data||null,cat:t.cat||'',
            feito:!!t.feito,mod:t.mod||new Date().toISOString()};
  };
  var daLinha=function(r){
    return {id:r.id,txt:r.txt,data:r.data||null,cat:r.cat||'',feito:!!r.feito,
            orig:'nuvem',mod:r.mod,sinc:true};
  };

  function enviar(t){
    if(!ativo())return Promise.resolve();
    return garantirSessao().then(function(){
      return api('/rest/v1/cao_tarefas',{
        method:'POST',
        headers:{'Prefer':'resolution=merge-duplicates,return=minimal'},
        body:JSON.stringify([paraLinha(t)])
      });
    }).then(function(){
      t.sinc=true;
      window.TAREFAS.salvar();
      window.TAREFAS.redesenhar();
    }).catch(function(e){
      estado('off','Sem conexão','Vai sincronizar sozinho quando a rede voltar');
    });
  }

  function apagar(t){
    var mortas=lerLS(K_DEL,[]);
    if(mortas.indexOf(t.id)<0){mortas.push(t.id);gravarLS(K_DEL,mortas)}
    if(!ativo())return Promise.resolve();
    return garantirSessao().then(function(){
      return api('/rest/v1/cao_tarefas?id=eq.'+encodeURIComponent(t.id),{method:'DELETE'});
    }).then(function(){
      var m=lerLS(K_DEL,[]).filter(function(x){return x!==t.id});
      gravarLS(K_DEL,m);
    }).catch(function(){});
  }

  /* -------- itens ticados das abas Compras / Mala / Rotina ---------------
     Tabela cao_ticados: uma linha por item marcado, chave (user_id, id).
     O id vem do proprio painel ("ab-compras/2de055d428"), entao e igual em
     todo aparelho - por isso a chave primaria precisa incluir o user_id.
     Vale sempre a alteracao mais recente (campo mod).                       */
  function tic(cls,txt,tit){
    if(window.TICADOS&&window.TICADOS.estado)window.TICADOS.estado(cls,txt,tit);
  }
  function sincTicados(){
    if(!ativo()||!window.TICADOS)return Promise.resolve();
    tic('','Salvando...');
    var loc=window.TICADOS.todos();
    return api('/rest/v1/cao_ticados?select=*').then(function(remotas){
      var mudou=false;
      (remotas||[]).forEach(function(r){
        var l=loc[r.id];
        if(!l||(r.mod||'')>(l.m||'')){
          loc[r.id]={n:r.n||0,m:r.mod,s:true};mudou=true;
        }
      });
      var subir=Object.keys(loc).filter(function(k){return !loc[k].s})
        .map(function(k){
          return {user_id:ses.uid,id:k,n:loc[k].n||0,mod:loc[k].m};
        });
      if(mudou)window.TICADOS.definir(loc);
      if(!subir.length)return null;
      return api('/rest/v1/cao_ticados?on_conflict=user_id,id',{
        method:'POST',
        headers:{'Prefer':'resolution=merge-duplicates,return=minimal'},
        body:JSON.stringify(subir)
      }).then(function(){
        Object.keys(loc).forEach(function(k){loc[k].s=true});
        window.TICADOS.salvar();
      });
    }).then(function(){
      tic('on','Salvo na nuvem','Suas marcações estão sincronizadas');
    }).catch(function(e){
      if(e&&(e.status===401||e.status===403))
        tic('erro','Sessão expirada','Entre na conta de novo, na aba Tarefas');
      else
        tic('off','Sem conexão','As marcações sobem sozinhas quando a rede voltar');
      throw e;
    });
  }
  /* espera o dedo parar antes de subir, para nao mandar um POST por clique */
  var tmTic=null;
  window.TICADOS_SYNC=function(){
    if(!ativo()){
      tic('','Somente neste aparelho','Entre na conta, na aba Tarefas, para sincronizar');
      return;
    }
    tic('','Salvando...');
    clearTimeout(tmTic);
    tmTic=setTimeout(function(){sincTicados().catch(function(){})},1200);
  };

  function sincronizar(){
    if(!ativo()||sincronizando)return Promise.resolve();
    sincronizando=true;
    estado('','Sincronizando...');
    return garantirSessao().then(function(){
      /* 1. apaga o que ficou pendente de exclusao */
      var mortas=lerLS(K_DEL,[]);
      var limpeza=mortas.length
        ? api('/rest/v1/cao_tarefas?id=in.('+mortas.map(encodeURIComponent).join(',')+')',
              {method:'DELETE'}).then(function(){gravarLS(K_DEL,[])}).catch(function(){})
        : Promise.resolve();
      return limpeza;
    }).then(function(){
      return api('/rest/v1/cao_tarefas?select=*');
    }).then(function(remotas){
      var locais=window.TAREFAS.todas();
      var mortas=lerLS(K_DEL,[]);
      var mapa={};
      locais.forEach(function(t){mapa[t.id]=t});

      /* 2. traz da nuvem o que for mais novo */
      (remotas||[]).forEach(function(r){
        if(mortas.indexOf(r.id)>=0)return;
        var loc=mapa[r.id];
        if(!loc){mapa[r.id]=daLinha(r);}
        else if((r.mod||'')>(loc.mod||'')){
          var n=daLinha(r);n.orig=loc.orig;mapa[r.id]=n;
        }
      });

      var juntas=Object.keys(mapa).map(function(k){return mapa[k]});
      window.TAREFAS.definir(juntas);

      /* 3. sobe o que ainda nao esta la */
      var subir=juntas.filter(function(t){return !t.sinc}).map(paraLinha);
      if(!subir.length)return null;
      return api('/rest/v1/cao_tarefas',{
        method:'POST',
        headers:{'Prefer':'resolution=merge-duplicates,return=minimal'},
        body:JSON.stringify(subir)
      }).then(function(){
        window.TAREFAS.todas().forEach(function(t){t.sinc=true});
        window.TAREFAS.salvar();
      });
    }).then(function(){
      /* 4. e, na mesma passada, os itens ticados das listas */
      return sincTicados().catch(function(){});
    }).then(function(){
      sincronizando=false;
      window.TAREFAS.redesenhar();
      pintaConta();
    }).catch(function(e){
      sincronizando=false;
      if(e&&(e.status===401||e.status===403)){
        sair();
        estado('erro','Sessão expirada','Entre na conta de novo');
      }else{
        estado('off','Sem conexão','As alterações ficam guardadas aqui até a rede voltar');
      }
    });
  }

  /* ------------------------------- eventos ------------------------------- */
  var btConta=el('#tf-conta');
  if(btConta){
    btConta.onclick=function(){
      var logado=ativo();
      el('#conta-form').style.display=logado?'none':'';
      el('#conta-logado').style.display=logado?'':'none';
      el('#conta-entrar').style.display=logado?'none':'';
      el('#conta-sair').style.display=logado?'':'none';
      el('#conta-titulo').textContent=logado?'Sua conta':'Entrar na conta';
      el('#conta-erro').classList.remove('on');
      if(logado)el('#conta-quem').textContent=ses.email||'';
      if(!configurado()){
        el('#conta-aviso').innerHTML='A sincronização ainda não foi ligada neste painel. '+
          'Peça para configurar o Supabase (o passo a passo está no arquivo '+
          '<code>SUPABASE.md</code>). Por enquanto, as tarefas ficam salvas '+
          'apenas neste aparelho, e o botão <b>Exportar</b> é o que garante que nada se perca.';
        el('#conta-entrar').disabled=true;
      }
      window.TAREFAS.modal.abrir('#modal-conta');
      if(!logado&&configurado())setTimeout(function(){el('#conta-email').focus()},80);
    };
  }
  var btEntrar=el('#conta-entrar');
  if(btEntrar){
    btEntrar.onclick=function(){
      var email=el('#conta-email').value.trim(), senha=el('#conta-senha').value;
      var erro=el('#conta-erro');
      if(!email||!senha){
        erro.textContent='Preencha e-mail e senha.';erro.classList.add('on');return;
      }
      btEntrar.disabled=true;btEntrar.textContent='Entrando...';
      entrar(email,senha).then(function(){
        el('#conta-senha').value='';
        window.TAREFAS.modal.fechar('#modal-conta');
      }).catch(function(e){
        var m=String(e.message||e);
        if(/invalid|credentials|grant/i.test(m))m='E-mail ou senha não conferem.';
        else if(/failed to fetch|networkerror/i.test(m))m='Sem conexão com o servidor.';
        erro.textContent=m;erro.classList.add('on');
      }).then(function(){
        btEntrar.disabled=false;btEntrar.textContent='Entrar';
      });
    };
  }
  var campoSenha=el('#conta-senha');
  if(campoSenha)campoSenha.onkeydown=function(e){if(e.key==='Enter')btEntrar.click()};
  var btSair=el('#conta-sair');
  if(btSair)btSair.onclick=function(){sair();window.TAREFAS.modal.fechar('#modal-conta')};

  window.addEventListener('online',function(){if(ativo())sincronizar()});
  window.addEventListener('offline',function(){
    if(ativo())estado('off','Sem conexão','As alterações ficam guardadas aqui');
  });

  window.SUPA={ativo:ativo,enviar:enviar,apagar:apagar,sincronizar:sincronizar};

  ses=lerLS(K_SES,null);
  pintaConta();
  if(ativo())sincronizar();
})();
"""

JS = r"""
(function(){
  var abas=[].slice.call(document.querySelectorAll('nav button'));
  var pans=[].slice.call(document.querySelectorAll('.aba'));

  function mostra(id,push){
    abas.forEach(function(b){b.setAttribute('aria-selected',b.dataset.aba===id)});
    pans.forEach(function(p){p.classList.toggle('on',p.id==='ab-'+id)});
    if(push!==false&&location.hash!=='#'+id)history.replaceState(null,'','#'+id);
    window.scrollTo({top:0,behavior:'smooth'});
  }
  abas.forEach(function(b){b.onclick=function(){mostra(b.dataset.aba)}});
  document.addEventListener('click',function(e){
    var a=e.target.closest('a.lnk-aba');
    if(a){e.preventDefault();mostra(a.getAttribute('href').slice(1));}
  });
  var ini=location.hash.slice(1);
  mostra(abas.some(function(b){return b.dataset.aba===ini})?ini:'painel',false);
  window.addEventListener('hashchange',function(){
    var h=location.hash.slice(1);
    if(abas.some(function(b){return b.dataset.aba===h}))mostra(h,false);
  });

  /* ---- itens ticaveis das abas geradas dos .md (Compras, Mala, Rotina...) ----
     O .md continua sendo a fonte de verdade do TEXTO; o que foi ticado fica
     salvo no proprio aparelho (localStorage), por aba + item.               */
  var K_MK='cao-ticados';
  var mkEstado={};
  try{mkEstado=JSON.parse(localStorage.getItem(K_MK)||'{}')||{}}catch(e){mkEstado={}}
  /* Cada item vira {n:quantos, m:quando mudou, s:ja subiu para a nuvem}.
     A primeira versao guardava so o numero; converte para nao perder o que
     ja estava ticado neste aparelho.                                        */
  var mkVelho=false;
  Object.keys(mkEstado).forEach(function(k){
    if(typeof mkEstado[k]==='number'){
      mkEstado[k]={n:mkEstado[k],m:'1970-01-01T00:00:00.000Z',s:false};
      mkVelho=true;
    }
  });
  function mkSalva(){try{localStorage.setItem(K_MK,JSON.stringify(mkEstado))}catch(e){}}
  if(mkVelho)mkSalva();
  function mkAgora(){return new Date().toISOString()}
  var CHECK='<svg viewBox="0 0 24 24" width="12" height="12" fill="none" '+
    'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '+
    'stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';

  function mkChave(li){
    var sec=li.closest('.aba');
    return (sec?sec.id:'?')+'/'+li.getAttribute('data-mk');
  }
  /* total do item: 0 = item simples (sim/nao); N = item com quantidade */
  function mkTotal(li){return parseInt(li.getAttribute('data-qtd')||'0',10)||0}
  function mkTenho(li){var v=mkEstado[mkChave(li)];return (v&&v.n)||0}

  /* pinta o item a partir de quantos ja tem. O contador mostra o que FALTA,
     que e o que interessa numa lista feita para zerar; so quando o item esta
     completo ele mostra o total, para fazer sentido ao reexibir os prontos. */
  function mkPinta(li,n){
    var tot=mkTotal(li), cheio=tot?n>=tot:n>0;
    li.classList.toggle('ok',cheio);
    li.classList.toggle('parcial',!cheio&&n>0);
    li.classList.toggle('pend',n===0);
    li.firstChild.innerHTML=cheio?CHECK:'';
    if(tot){
      var q=li.querySelector('.mk-qtd');
      if(q){
        q.querySelector('.n').textContent=cheio?(tot+' de '+tot):('faltam '+(tot-n));
        q.querySelector('.menos').disabled=n<=0;
        q.querySelector('.mais').disabled=n>=tot;
      }
    }
  }

  /* ------- esconder o que ja esta pronto, para a lista ir encurtando ------
     Vale por aba. O item so some quando esta completo: enquanto falta peca
     ele continua na lista, mostrando quantas faltam.                       */
  var K_ESC='cao-esconder';
  var mkEsc={};
  try{mkEsc=JSON.parse(localStorage.getItem(K_ESC)||'{}')||{}}catch(e){mkEsc={}}
  function mkEscondendo(sec){return mkEsc[sec.id]!==false} /* padrao: esconde */
  function mkEscSalva(){try{localStorage.setItem(K_ESC,JSON.stringify(mkEsc))}catch(e){}}

  /* alem do item, some tambem a lista que ficou vazia e o titulo da secao
     que ficou sem nenhuma lista visivel - senao sobra titulo solto na tela */
  function mkArruma(sec){
    var esconder=mkEscondendo(sec), prontos=0;
    [].forEach.call(sec.querySelectorAll('ul.tarefas li[data-mk]'),function(li){
      if(li.classList.contains('ok'))prontos++;
      li.classList.toggle('oculto',esconder&&li.classList.contains('ok'));
    });
    [].forEach.call(sec.querySelectorAll('ul.tarefas'),function(ul){
      var vivo=[].some.call(ul.children,function(li){
        return !li.classList.contains('oculto');
      });
      ul.classList.toggle('oculto',!vivo);
    });
    var card=sec.querySelector('.card');
    if(card){
      /* varre os blocos de cada titulo ate o proximo titulo do mesmo nivel */
      var filhos=[].slice.call(card.children), bloco=[], tit=null;
      var fecha=function(){
        if(!tit)return;
        var listas=bloco.filter(function(e){return e.matches('ul.tarefas')});
        var some=listas.length>0&&listas.every(function(u){
          return u.classList.contains('oculto');
        });
        tit.classList.toggle('oculto',some);
        bloco.forEach(function(e){
          if(!e.matches('ul.tarefas'))e.classList.toggle('oculto',some);
        });
      };
      filhos.forEach(function(e){
        if(/^H[23]$/.test(e.tagName)){fecha();tit=e;bloco=[];}
        else if(tit)bloco.push(e);
      });
      fecha();
    }
    var bt=sec.querySelector('.mk-ver');
    if(bt){
      bt.style.display=prontos?'':'none';
      bt.textContent=(esconder?'Mostrar ':'Ocultar ')+prontos+
        (prontos===1?' já pronto':' já prontos');
    }
  }
  /* grava e repinta. Guarda ate o zero (em vez de apagar a chave), senao a
     nuvem devolveria na proxima sincronizacao o que voce acabou de desmarcar. */
  function mkPoe(li,n){
    var tot=mkTotal(li);
    n=Math.max(0,Math.min(n,tot||1));
    mkEstado[mkChave(li)]={n:n,m:mkAgora(),s:false};
    mkPinta(li,n);mkSalva();
    var sec=li.closest('.aba');
    if(sec){mkConta(sec);mkArruma(sec);}
    if(window.TICADOS_SYNC)window.TICADOS_SYNC();
  }
  function mkConta(sec){
    var itens=sec.querySelectorAll('ul.tarefas li[data-mk]');
    var topo=sec.querySelector('.mk-topo');
    if(!itens.length||!topo)return;
    /* conta por peca: item com quantidade vale pelo total dele */
    var tem=0,total=0;
    [].forEach.call(itens,function(li){
      var tot=mkTotal(li)||1;
      total+=tot;tem+=Math.min(mkTenho(li),tot);
    });
    var pct=total?Math.round(tem*100/total):0;
    topo.querySelector('.mk-n').textContent=tem+' de '+total;
    topo.querySelector('.mk-barra i').style.width=pct+'%';
    /* os cartoes de Compras e Mala da abertura leem daqui */
    if(window.GUIA)GUIA.listas();
  }

  /* monta o contador no topo e os steppers dos itens com quantidade */
  pans.forEach(function(sec){
    var itens=sec.querySelectorAll('ul.tarefas li[data-mk]');
    if(!itens.length)return;
    var card=sec.querySelector('.card');
    if(!card)return;
    var topo=document.createElement('div');
    topo.className='mk-topo';
    topo.innerHTML='<span class="mk-n"></span>'+
      '<span class="mk-barra"><i style="width:0"></i></span>'+
      '<span class="tf-status mk-sinc" title="Estado da sincronização">'+
      '<span class="bola"></span><span class="txt">Somente neste aparelho</span></span>'+
      '<button type="button" class="mk-ver"></button>'+
      '<button type="button" class="mk-limpar">Limpar marcações</button>';
    card.insertBefore(topo,card.firstChild);
    topo.querySelector('.mk-ver').onclick=function(){
      mkEsc[sec.id]=!mkEscondendo(sec);
      mkEscSalva();mkArruma(sec);
    };
    topo.querySelector('.mk-limpar').onclick=function(){
      var agora=mkAgora();
      [].forEach.call(itens,function(li){
        mkEstado[mkChave(li)]={n:0,m:agora,s:false};
        mkPinta(li,0);
      });
      mkSalva();mkConta(sec);mkArruma(sec);
      if(window.TICADOS_SYNC)window.TICADOS_SYNC();
    };
    [].forEach.call(itens,function(li){
      if(mkTotal(li)){
        var q=document.createElement('span');
        q.className='mk-qtd';
        q.innerHTML='<button type="button" class="menos" aria-label="Tirar um">−</button>'+
          '<span class="n"></span>'+
          '<button type="button" class="mais" aria-label="Somar um">+</button>';
        li.appendChild(q);
      }
      mkPinta(li,mkTenho(li));
    });
    mkConta(sec);mkArruma(sec);
  });

  document.addEventListener('click',function(e){
    var bt=e.target.closest('.mk-qtd button');
    if(bt){
      /* o +/- mexe de um em um e nao deixa o clique virar toggle da linha */
      e.stopPropagation();
      var li=bt.closest('li[data-mk]');
      mkPoe(li,mkTenho(li)+(bt.classList.contains('mais')?1:-1));
      return;
    }
    var li=e.target.closest('ul.tarefas li[data-mk]');
    if(!li)return;
    /* clique na linha: tenho tudo <-> nao tenho nada */
    var tot=mkTotal(li)||1;
    mkPoe(li,mkTenho(li)>=tot?0:tot);
  });

  /* usado pela sincronizacao para redesenhar tudo depois de baixar da nuvem */
  function mkRepintaTudo(){
    pans.forEach(function(sec){
      var itens=sec.querySelectorAll('ul.tarefas li[data-mk]');
      if(!itens.length)return;
      [].forEach.call(itens,function(li){mkPinta(li,mkTenho(li))});
      mkConta(sec);mkArruma(sec);
    });
  }
  /* estado da sincronizacao mostrado na barra de cada aba de lista.
     Quem chama e o bloco do Supabase; sem ele fica no texto inicial.       */
  function mkEstadoSinc(cls,txt,tit){
    [].forEach.call(document.querySelectorAll('.mk-sinc'),function(s){
      s.className='tf-status mk-sinc'+(cls?' '+cls:'');
      s.querySelector('.txt').textContent=txt;
      s.title=tit||'';
    });
  }
  window.TICADOS={
    todos:function(){return mkEstado},
    definir:function(novo){mkEstado=novo;mkSalva();mkRepintaTudo()},
    salvar:mkSalva,
    repintar:mkRepintaTudo,
    estado:mkEstadoSinc
  };

  /* tema */
  var bt=document.getElementById('tema');
  var salvo=null;
  try{salvo=localStorage.getItem('cao-tema')}catch(e){}
  if(salvo)document.documentElement.setAttribute('data-theme',salvo);
  function pinta(){
    var esc=document.documentElement.getAttribute('data-theme')==='dark'||
      (!document.documentElement.getAttribute('data-theme')&&
       matchMedia('(prefers-color-scheme:dark)').matches);
    bt.innerHTML=esc?SOL:LUA;
    bt.title=esc?'Mudar para tema claro':'Mudar para tema escuro';
  }
  bt.onclick=function(){
    var atual=document.documentElement.getAttribute('data-theme');
    if(!atual)atual=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
    var novo=atual==='dark'?'light':'dark';
    document.documentElement.setAttribute('data-theme',novo);
    try{localStorage.setItem('cao-tema',novo)}catch(e){}
    pinta();
  };
  pinta();

  /* busca */
  var inp=document.getElementById('q');
  var alvos=[].slice.call(document.querySelectorAll('.card [data-b]'));

  function limpa(){
    alvos.forEach(function(el){
      el.style.display='';
      if(el.dataset.orig){el.innerHTML=el.dataset.orig;delete el.dataset.orig;}
    });
    document.querySelectorAll('.sem-res').forEach(function(n){n.remove()});
    document.querySelectorAll('.card').forEach(function(c){c.style.display=''});
  }
  function realca(el,termo){
    if(!el.dataset.orig)el.dataset.orig=el.innerHTML;
    var re=new RegExp('('+termo.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');
    var walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null);
    var nos=[],n;
    while(n=walk.nextNode())nos.push(n);
    nos.forEach(function(no){
      if(!re.test(no.nodeValue))return;
      re.lastIndex=0;
      var span=document.createElement('span');
      span.innerHTML=no.nodeValue.replace(/[&<>]/g,function(c){
        return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]}).replace(re,'<mark>$1</mark>');
      no.parentNode.replaceChild(span,no);
    });
  }
  var t;
  inp.oninput=function(){
    clearTimeout(t);
    t=setTimeout(function(){
      var termo=inp.value.trim();
      var barra=document.querySelector('nav');
      limpa();
      if(termo.length<2){
        barra.classList.remove('buscando');
        barra.querySelectorAll('.pill-b').forEach(function(b){b.style.display='none'});
        return;
      }
      barra.classList.add('buscando');
      var alvo=termo.toLowerCase();
      var achou=0;
      pans.forEach(function(pan){
        var n=0;
        pan.querySelectorAll('.card [data-b]').forEach(function(el){
          var bate=el.textContent.toLowerCase().indexOf(alvo)>=0;
          el.style.display=bate?'':'none';
          if(bate){realca(el,termo);n++;}
        });
        pan.querySelectorAll('.card').forEach(function(c){
          var vis=[].slice.call(c.querySelectorAll('[data-b]')).some(function(e){
            return e.style.display!=='none'});
          c.style.display=vis?'':'none';
        });
        achou+=n;
        var b=document.querySelector('nav button[data-aba="'+pan.id.slice(3)+'"] .pill-b');
        if(b){b.textContent=n||'';b.style.display=n?'':'none';}
      });
      if(!achou){
        pans.forEach(function(pan){
          var d=document.createElement('div');
          d.className='sem-res';
          d.textContent='Nada encontrado para "'+termo+'".';
          pan.appendChild(d);
        });
      }
    },140);
  };
  inp.addEventListener('keydown',function(e){
    if(e.key==='Escape'){inp.value='';inp.oninput();inp.blur();}
  });
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();inp.focus();inp.select();}
  });
})();
"""


JS_GUIA = r"""
/* ========================= guia do dia =========================
   Responde "o que eu faco hoje?" na abertura do painel.

   Regra de ouro: tudo aqui e calculado no navegador, com a data de
   quem esta olhando. O painel publicado so e regerado quando um .md
   muda, entao qualquer conta feita na geracao envelhece em silencio
   (foi o que aconteceu: o cartao ficou dias dizendo "9 dias para o
   inicio" depois que ja faltavam 6).                             */
(function(){
  var C=window.CURSO||{};
  var SEM=['domingo','segunda-feira','terça-feira','quarta-feira',
           'quinta-feira','sexta-feira','sábado'];
  var MES=['janeiro','fevereiro','março','abril','maio','junho','julho',
           'agosto','setembro','outubro','novembro','dezembro'];

  function dt(iso){var p=String(iso).split('-');
    return new Date(+p[0],+p[1]-1,+p[2]);}
  function hoje(){var d=new Date();return new Date(d.getFullYear(),d.getMonth(),d.getDate());}
  function dias(a,b){return Math.round((b-a)/864e5);}
  function curto(d){return ('0'+d.getDate()).slice(-2)+'/'+('0'+(d.getMonth()+1)).slice(-2);}
  function el(s){return document.querySelector(s);}

  var INICIO=C.inicio?dt(C.inicio):null;
  var FIM=C.fim?dt(C.fim):null;
  var VIAGEM1=C.viagem?dt(C.viagem):null;

  /* ---- onde estou na semana do curso ----
     A semana se repete: viaja domingo, aula de segunda a quinta, volta
     quinta depois das 11h30 (ROTINA.md). Antes da primeira viagem, o
     marco e ela mesma.                                              */
  function marco(h){
    var dow=h.getDay();  /* 0=domingo */
    if(VIAGEM1&&h<VIAGEM1){
      var n=dias(h,VIAGEM1);
      return {n:n,alvo:VIAGEM1,
        rot:n===0?'hoje é dia de viajar':(n===1?'dia para a viagem':'dias para a viagem'),
        sub:'primeira ida, '+SEM[VIAGEM1.getDay()]+' '+curto(VIAGEM1),
        fase:n===0?'Hoje você viaja para São Paulo. Aula amanhã, 08h15.':
             'Você está em casa. A primeira semana no CAES começa em '+
             SEM[VIAGEM1.getDay()]+', '+curto(VIAGEM1)+'.'};
    }
    if(FIM&&h>FIM)return {n:0,alvo:null,rot:'curso concluído',sub:'agosto de 2027',
                          fase:'Curso concluído.'};
    if(dow===0)return {n:0,alvo:h,rot:'hoje é dia de viajar',sub:'aula amanhã, 08h15',
      fase:'Hoje você desloca para o CAES. A semana vai até quinta, 11h30.'};
    if(dow>=1&&dow<=4){
      var qui=new Date(h);qui.setDate(h.getDate()+(4-dow));
      var n2=dias(h,qui);
      return {n:n2,alvo:qui,
        rot:n2===0?'volta hoje, 11h30':(n2===1?'dia para voltar':'dias para voltar'),
        sub:'quinta, '+curto(qui),
        fase:'Semana de aula no CAES. '+(dow===4?'Hoje você volta depois das 11h30.':
             'Você volta na quinta, depois das 11h30.')};
    }
    /* sexta ou sabado: proximo domingo */
    var dom=new Date(h);dom.setDate(h.getDate()+(7-dow));
    var n3=dias(h,dom);
    return {n:n3,alvo:dom,rot:n3===1?'dia para a viagem':'dias para a viagem',
      sub:'domingo, '+curto(dom),
      fase:'Você está em casa. Próxima ida ao CAES no domingo, '+curto(dom)+'.'};
  }

  function saudacao(){
    var h=new Date().getHours();
    return h<12?'Bom dia, Capitão':(h<18?'Boa tarde, Capitão':'Boa noite, Capitão');
  }

  function topo(){
    var h=hoje(), m=marco(h);
    var od=el('#guia-ola'), dd=el('#guia-dia'), fd=el('#guia-fase'), cd=el('#guia-conta');
    if(od)od.textContent=saudacao();
    if(dd)dd.textContent=SEM[h.getDay()].replace(/^./,function(c){return c.toUpperCase()})+
      ', '+h.getDate()+' de '+MES[h.getMonth()];
    if(fd)fd.textContent=m.fase;
    if(cd)cd.innerHTML=m.n>0?('<b>'+m.n+'</b><span>'+m.rot+'<br>'+m.sub+'</span>'):
      ('<span style="font-size:13.5px;font-weight:700">'+
       m.rot.replace(/^./,function(c){return c.toUpperCase()})+'<br>'+
       '<span style="font-weight:400;opacity:.9">'+m.sub+'</span></span>');
    /* KPI do curso: dias para comecar, ou quanto ja andou */
    var kr=el('#kpi-curso-rot'),kv=el('#kpi-curso-val'),ks=el('#kpi-curso-sub'),
        kb=el('#kpi-curso-barra');
    if(kv&&INICIO&&FIM){
      if(h<INICIO){
        var n=dias(h,INICIO);
        kr.textContent='Início do curso';kv.textContent=n;
        ks.textContent=(n===1?'dia para ':'dias para ')+curto(INICIO)+'/'+INICIO.getFullYear();
        kb.style.width='0%';
      }else if(h>FIM){
        kr.textContent='Curso';kv.textContent='Concluído';
        ks.textContent='agosto de 2027';kb.style.width='100%';
      }else{
        var pct=Math.round(dias(INICIO,h)*100/dias(INICIO,FIM));
        kr.textContent='Curso em andamento';kv.textContent=pct+'%';
        ks.textContent='faltam '+dias(h,FIM)+' dias';kb.style.width=pct+'%';
      }
    }
  }

  /* ---- o que fazer: vem das tarefas com data (TAREFAS.md + as que voce
     cadastra no painel). Quem chama e o app de tarefas, a cada desenho. */
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});}

  /* cor da categoria: o mapa do app de tarefas e privado, entao remonto aqui */
  var COR={};
  (window.CATEGORIAS||[]).forEach(function(c){COR[c[0]]=c[2]});

  function linha(t,mostraData){
    var cor=t.cat?(COR[t.cat]||''):'';
    var quando='';
    if(mostraData&&t.data){
      var d=dt(t.data), n=dias(hoje(),d);
      quando='<span class="qd">'+SEM[d.getDay()].slice(0,3)+' '+curto(d)+'</span>';
      if(n<0)quando='<span class="qd">venceu '+curto(d)+'</span>';
    }
    return '<li><span class="pt"'+(cor?' style="background:'+cor+'"':'')+'></span>'+
           '<span>'+esc(t.txt)+'</span>'+quando+'</li>';
  }

  function tarefas(g){
    var alvo=el('#guia-corpo');
    if(!alvo)return;
    var out='';
    var bloco=function(arr,rot,cls,comData){
      if(!arr||!arr.length)return;
      out+='<div class="guia-bloco '+(cls||'')+'"><div class="guia-cab">'+rot+
           '<span class="n">'+arr.length+'</span></div><ul class="guia-lista">'+
           arr.map(function(t){return linha(t,comData)}).join('')+'</ul></div>';
    };
    bloco(g.atrasadas,'Atrasado, resolver primeiro','vencido',true);
    bloco(g.hoje,'Hoje você precisa','agora',false);
    bloco(g.amanha,'Amanhã','',false);
    /* "esta semana" e ate o domingo que vem, nao "os proximos 7 dias": o que
       cai depois disso vira ruido no cartao de abertura e continua na aba
       Tarefas. Durante o curso, o domingo e justamente o dia de viajar.   */
    var h=hoje(), fim=new Date(h);
    fim.setDate(h.getDate()+(h.getDay()===0?0:7-h.getDay()));
    var perto=[],longe=[];
    (g.semana||[]).forEach(function(t){
      (t.data&&dt(t.data)<=fim?perto:longe).push(t);
    });
    longe=longe.concat(g.depois||[]);
    bloco(perto,h.getDay()===0?'Ainda hoje':'Ainda esta semana','',true);
    if(!out){
      out='<div class="guia-tudoem">'+(window.ICO&&ICO.check?ICO.check:'')+
          'Nada com prazo para hoje nem para esta semana.</div>';
    }
    /* rodape: o que existe mas nao cabe no foco de hoje */
    var resto=[];
    if(longe.length)resto.push('<b>'+longe.length+'</b> '+
      (longe.length===1?'tarefa mais adiante':'tarefas mais adiante'));
    if(g.semdata&&g.semdata.length)resto.push('<b>'+g.semdata.length+'</b> '+
      (g.semdata.length===1?'sem data marcada':'sem data marcada'));
    if(resto.length)
      out+='<p class="guia-nota">Também tem '+resto.join(' e ')+
           '. Estão na aba Tarefas.</p>';
    alvo.innerHTML=out;
  }

  /* ---- quanto falta nas listas ticaveis (Compras, Mala) ---- */
  function listas(){
    var estado=(window.TICADOS&&TICADOS.todos&&TICADOS.todos())||{};
    [].forEach.call(document.querySelectorAll('.lista-kpi'),function(k){
      var sec=document.getElementById(k.getAttribute('data-aba'));
      if(!sec){k.style.display='none';return;}
      var itens=sec.querySelectorAll('ul.tarefas li[data-mk]');
      if(!itens.length){k.style.display='none';return;}
      var tem=0,total=0;
      [].forEach.call(itens,function(li){
        var tot=parseInt(li.getAttribute('data-qtd')||'0',10)||1;
        var v=estado[sec.id+'/'+li.getAttribute('data-mk')];
        total+=tot;tem+=Math.min((v&&v.n)||0,tot);
      });
      var falta=total-tem, pct=total?Math.round(tem*100/total):0;
      k.querySelector('.val').textContent=falta?falta:'ok';
      k.querySelector('.sub').textContent=falta?
        (falta===1?'item ainda falta':'itens ainda faltam'):
        ('tudo marcado, '+total+' itens');
      k.querySelector('.barra i').style.width=pct+'%';
      k.classList.toggle('dest',falta>0&&k.getAttribute('data-aba')==='ab-compras');
    });
  }

  /* marco fica exposto para conferir o texto de cada dia da semana sem
     precisar esperar o dia chegar: GUIA.marco(new Date(2026,7,19))       */
  window.GUIA={topo:topo,tarefas:tarefas,listas:listas,marco:marco};
  topo();listas();
  /* vira o dia com o painel aberto (celular que fica na tela): refaz o topo */
  setInterval(topo,10*60*1000);
})();
"""


CARIMBO_VAGA = "@@CARIMBO@@"


def _carimbo_versao(doc):
    """Identifica esta versao do painel, para o navegador nao servir cache velho.

    E um hash do proprio documento, nao o relogio. Isso importa porque
    'docs/index.html' e arquivo gerado, esta versionado e tem dois produtores:
    a maquina do Josemar e a Action de publicacao. Com carimbo de relogio, duas
    geracoes do mesmo conteudo davam arquivos diferentes, e o Git via conflito
    em cima de nada: em 15/08/2026 um commit da Action mudou uma unica linha do
    painel, so o carimbo. Com hash, os dois produtores chegam ao mesmo byte,
    a Action nao commita quando nada mudou e a pasta local nao suja depois de
    gerar so para conferir.

    Para o cache do navegador tambem e melhor: muda quando o conteudo muda, em
    vez de forcar download novo a cada geracao.
    """
    import hashlib
    return hashlib.sha256(doc.encode("utf-8")).hexdigest()[:16]


def _papel_da_chave(key):
    """Le o campo 'role' de um JWT do Supabase. Devolve None se nao der."""
    try:
        import base64, json
        payload = key.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        dados = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
        return dados.get("role")
    except Exception:
        return None


def le_config_supabase():
    """Le supabase.json, se existir. Sem ele, o painel roda so no navegador.

    A chave gravada ali e a 'anon' (publicavel): ela identifica o projeto, nao
    da acesso a nada sozinha. Quem protege os dados e o RLS + o login.
    """
    caminho = os.path.join(RAIZ, "supabase.json")
    if not os.path.exists(caminho):
        return {}
    try:
        import json
        with open(caminho, encoding="utf-8") as f:
            cfg = json.load(f)
        url = (cfg.get("url") or "").strip()
        key = (cfg.get("anonKey") or cfg.get("key") or "").strip()
        if not url or not key:
            print("Aviso: supabase.json existe mas está incompleto (falta url ou anonKey).")
            return {}

        # trava de seguranca: a chave secreta ignora o RLS e nao pode ir para um
        # site publico. Dois formatos existem: o novo (sb_secret_...) e o antigo
        # (JWT com "role":"service_role" no payload).
        papel = None
        if key.startswith("sb_secret_"):
            papel = "secret"
        elif key.startswith("sb_publishable_"):
            papel = "anon"          # formato novo, equivalente a anon
        else:
            papel = _papel_da_chave(key)
        # Lista de permissao, nao lista de proibicao: so passa o que foi
        # reconhecido como 'anon'. Antes era "if papel and papel != 'anon'", e o
        # "papel and" tratava chave NAO RECONHECIDA (papel=None) como aprovada.
        # Passavam um token pessoal sbp_, que da acesso a conta inteira do
        # Supabase, uma connection string postgresql:// e um JWT sem campo role,
        # e qualquer um deles seria embutido no docs/index.html publicado.
        if papel != "anon":
            print("=" * 68)
            print("PAREI: nao reconheci a chave do supabase.json como publicavel")
            print("(papel detectado: %s)." % (papel or "desconhecido"))
            print("So aceito 'sb_publishable_...' ou um JWT com role 'anon'.")
            print("Qualquer outra chave (service_role, token pessoal sbp_,")
            print("connection string) ignora as regras de seguranca do banco e")
            print("NAO pode ficar num site publico.")
            print("Pegue a chave em Project Settings > API e rode de novo.")
            print("=" * 68)
            raise SystemExit(1)
        return {"url": url, "key": key}
    except Exception as e:
        print("Aviso: não consegui ler supabase.json (%s). Seguindo sem sincronização." % e)
        return {}


def app_tarefas():
    """HTML da aba Tarefas (cadastro, lista e modais)."""
    chips_cat = "".join(
        '<button class="chip" data-cat="%s"><span class="pt" style="background:%s"></span>%s</button>'
        % (chave, cor, rot) for chave, rot, cor in CATEGORIAS)

    return """
<div class="tf-topo">
  <button class="btn" id="tf-exportar" title="Gerar o texto para colar no TAREFAS.md">%(baixar)s Exportar</button>
  <button class="btn" id="tf-conta">%(users)s <span id="tf-conta-rot">Entrar</span></button>
  <div class="tf-status" id="tf-status" title="Estado da sincronização">
    <span class="bola"></span><span id="tf-status-txt">Somente neste aparelho</span>
  </div>
</div>

<div class="tf-pend" id="tf-pend" style="display:none">
  %(alerta)s
  <div>
    <b id="tf-pend-n"></b>
    Não precisa fazer nada: a sincronização roda de hora em hora e leva isso sozinha
    para o <code>TAREFAS.md</code>. Este aviso some quando ela rodar e o painel
    republicar. Se estiver com pressa, dá para levar na mão agora.
    <div><button class="btn" onclick="document.getElementById('tf-exportar').click()">
      %(baixar)s Exportar na mão</button></div>
  </div>
</div>

<div class="tf-nova">
  <div class="tf-linha">
    <input type="text" id="tf-txt" placeholder="O que precisa ser feito? Ex.: entregar artigo sexta"
           autocomplete="off" spellcheck="false">
    <button class="tf-add" id="tf-add" title="Adicionar (Enter)" disabled>%(mais)s</button>
  </div>
  <div class="tf-opts">
    <input type="date" class="tf-data" id="tf-dt" title="Data da tarefa">
    <span id="tf-rapidas" style="display:contents">
      <button class="chip" data-q="hoje">Hoje</button>
      <button class="chip" data-q="amanha">Amanhã</button>
      <button class="chip" data-q="semana">Em 7 dias</button>
      <button class="chip" data-q="limpar">Sem data</button>
    </span>
    <span style="width:1px;height:20px;background:var(--bd)"></span>
    <span id="tf-cats" style="display:contents">%(cats)s</span>
  </div>
</div>

<div id="tf-lista"></div>

<div class="modal" id="modal-exp">
  <div class="modal-cx">
    <div class="modal-cab">%(baixar)s<h3>Levar para o TAREFAS.md</h3>
      <button class="tf-ac" data-fechar="modal-exp">%(fechar)s</button></div>
    <div class="modal-corpo">
      <p>Normalmente não precisa: a sincronização escreve isto no
         <code>TAREFAS.md</code> sozinha, de hora em hora. Isto aqui é a saída de
         emergência, para quando ela estiver fora do ar ou você não quiser esperar.
         Copie e substitua o conteúdo do arquivo; é exatamente o que ela escreveria.</p>
      <textarea id="exp-txt" spellcheck="false"></textarea>
    </div>
    <div class="modal-rod">
      <button class="btn" data-fechar="modal-exp">Fechar</button>
      <button class="btn pri" id="exp-copiar">%(copiar)s Copiar</button>
    </div>
  </div>
</div>

<div class="modal" id="modal-conta">
  <div class="modal-cx">
    <div class="modal-cab">%(users)s<h3 id="conta-titulo">Entrar na conta</h3>
      <button class="tf-ac" data-fechar="modal-conta">%(fechar)s</button></div>
    <div class="modal-corpo">
      <div class="modal-erro" id="conta-erro"></div>
      <div id="conta-form">
        <div class="aviso-cx" id="conta-aviso">
          Entrando, suas tarefas passam a sincronizar entre o computador e o celular.
          Sem entrar, elas ficam salvas só neste aparelho.
        </div>
        <label for="conta-email">E-mail</label>
        <input type="email" id="conta-email" autocomplete="username" placeholder="seu@email.com">
        <label for="conta-senha">Senha</label>
        <input type="password" id="conta-senha" autocomplete="current-password" placeholder="••••••••">
      </div>
      <div id="conta-logado" style="display:none">
        <p>Conectado como <b id="conta-quem"></b>. As tarefas estão sincronizando.</p>
      </div>
    </div>
    <div class="modal-rod">
      <button class="btn" data-fechar="modal-conta">Fechar</button>
      <button class="btn" id="conta-sair" style="display:none">Sair da conta</button>
      <button class="btn pri" id="conta-entrar">Entrar</button>
    </div>
  </div>
</div>
""" % {
        "cats": chips_cat,
        "mais": svg("mais", 19),
        "baixar": svg("baixar", 15),
        "alerta": svg("alerta", 18),
        "fechar": svg("fechar", 16),
        "copiar": svg("copiar", 15),
        "users": svg("users", 15),
    }


def build():
    docs = {}
    faltando = []
    for arq, aba_id, rot, ic in ABAS:
        caminho = os.path.join(RAIZ, arq)
        if not os.path.exists(caminho):
            faltando.append(arq)
            docs[arq] = ""
            continue
        with open(caminho, encoding="utf-8") as f:
            docs[arq] = f.read()

    if faltando:
        print("Aviso: nao encontrei %s" % ", ".join(faltando))

    # Nada no painel gerado pode depender da data de hoje. O rodape mostrava a
    # data da geracao, e isso fazia a Action (que roda em UTC) e o PC (UTC-3)
    # produzirem arquivos diferentes perto da meia-noite, alem de reintroduzir
    # o conflito a cada virada de dia. Toda conta de tempo e feita no navegador.
    pend, feito = conta_tarefas(docs.get("TAREFAS.md", ""))

    # navegacao
    nav = []
    for arq, aba_id, rot, ic in ABAS:
        extra = ""
        if aba_id == "tarefas" and pend:
            extra = '<span class="pill">%d</span>' % pend
        nav.append('<button data-aba="%s" role="tab" aria-selected="false">%s%s%s'
                   '<span class="pill pill-b" style="display:none"></span></button>'
                   % (aba_id, svg(ic, 15), rot, extra))

    # ------------------------------------------------------------------ guia --
    # O cartao de abertura ("hoje voce precisa...") e montado pelo navegador, em
    # JS: ele precisa saber a data de quem esta olhando, nao a data em que o
    # painel foi gerado. O painel publicado so e regerado quando algum .md muda,
    # entao qualquer contagem calculada aqui congelaria: em 08/08 o cartao dizia
    # "9 dias para o inicio" e continuou dizendo isso no dia 11. O que sai daqui
    # e so o texto inicial, substituido assim que a pagina abre.
    home = ['<section class="guia">'
            '<div class="guia-topo"><div>'
            '<p class="guia-ola" id="guia-ola">Central do CAO</p>'
            '<h2 class="guia-dia" id="guia-dia">Carregando o dia...</h2>'
            '<p class="guia-fase" id="guia-fase"></p></div>'
            '<div class="guia-conta" id="guia-conta"></div></div>'
            '<div class="guia-corpo" id="guia-corpo"></div>'
            '</section>']

    home.append('<div class="grade">')
    home.append('<div class="kpi dest"><div class="rot" id="kpi-curso-rot">Curso</div>'
                '<div class="val" id="kpi-curso-val">...</div>'
                '<div class="sub" id="kpi-curso-sub">CAO-II/26</div>'
                '<div class="barra"><i id="kpi-curso-barra" style="width:0%"></i></div></div>')
    home.append('<div class="kpi"><div class="rot">Tarefas pendentes</div>'
                '<div class="val" id="kpi-tar-val">%d</div>'
                '<div class="sub" id="kpi-tar-sub">%s</div></div>'
                % (pend, "%d já concluída%s" % (feito, "" if feito == 1 else "s")))
    # os dois de baixo leem o que voce ja ticou nas abas Compras e Mala
    home.append('<div class="kpi lista-kpi" data-aba="ab-compras" data-rot="Compras">'
                '<div class="rot">Compras</div><div class="val">...</div>'
                '<div class="sub">antes de viajar</div>'
                '<div class="barra"><i style="width:0%"></i></div></div>')
    home.append('<div class="kpi lista-kpi" data-aba="ab-mala" data-rot="Mala">'
                '<div class="rot">Mala</div><div class="val">...</div>'
                '<div class="sub">itens separados</div>'
                '<div class="barra"><i style="width:0%"></i></div></div>')
    home.append("</div>")

    # paineis
    paineis = []
    for arq, aba_id, rot, ic in ABAS:
        if aba_id == "tarefas":
            # a aba de tarefas e um app, nao markdown convertido
            paineis.append('<section class="aba" id="ab-tarefas" role="tabpanel">%s</section>'
                           % app_tarefas())
            continue
        corpo = md_para_html(docs.get(arq, ""))
        # marca cada bloco de primeiro nivel para a busca.
        # o (?=[\s>]) evita casar dentro de <path> dos icones SVG.
        corpo = re.sub(r"<(h2|h3|p|ul|ol|pre|blockquote|hr)(?=[\s>])",
                       r"<\1 data-b", corpo)
        corpo = corpo.replace('<div class="tab-wrap">', '<div class="tab-wrap" data-b>')
        extra = "".join(home) if aba_id == "painel" else ""
        paineis.append('<section class="aba" id="ab-%s" role="tabpanel">%s'
                       '<div class="card">%s</div></section>' % (aba_id, extra, corpo))

    doc = """<!DOCTYPE html>
<html lang="pt-BR" prefix="og: http://ogp.me/ns#">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="googlebot" content="noindex,nofollow">
<meta name="theme-color" content="#c8102e">
<!-- o painel e um arquivo unico que muda a cada geracao; sem isto o navegador
     serve a versao antiga do cache e correcoes nao chegam ate o usuario -->
<meta http-equiv="Cache-Control" content="no-cache, must-revalidate">
<meta name="gerado-em" content="%(carimbo)s">
<title>Central do CAO</title>
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' rx='7' fill='%%23c8102e'/%%3E%%3Ctext x='16' y='22' font-size='15' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'%%3ECAO%%3C/text%%3E%%3C/svg%%3E">
<style>%(css)s</style>
</head>
<body>
<header class="topo">
  <div class="wrap">
    <div class="marca">
      <div class="brasao">CAO</div>
      <div>
        <h1>Central do CAO</h1>
        <p>CAO-II / 2026, CAES "Cel Nelson Freire Terra"</p>
      </div>
      <div class="acoes">
        <button class="bt" id="tema" title="Alternar tema"></button>
      </div>
    </div>
    <div class="busca">
      %(icbusca)s
      <input id="q" type="search" placeholder="Buscar em tudo (Ctrl+K)" autocomplete="off" spellcheck="false">
    </div>
    <nav role="tablist">%(nav)s</nav>
  </div>
</header>
<main>%(paineis)s
  <p class="rodape">Gerado a partir dos arquivos <code>.md</code>. Para atualizar: edite o .md e rode <code>python gerar_painel.py</code>.</p>
</main>
<script>
var SOL=%(sol)r,LUA=%(lua)r;
var CATEGORIAS=%(cats)s;
var BASE=%(base)s;
var TAR_CAB=%(tarcab)s;
var ICO=%(ico)s;
window.CURSO=%(curso)s;
window.SUPA_CFG=%(supa)s;
%(js)s
%(js_guia)s
%(js_tarefas)s
%(js_supabase)s
</script>
</body>
</html>
""" % {
        "css": CSS,
        "js": JS,
        "js_guia": JS_GUIA,
        "js_tarefas": JS_TAREFAS,
        "curso": escapa_js({"inicio": CURSO_INICIO.isoformat(),
                            "fim": CURSO_FIM.isoformat(),
                            "viagem": PRIMEIRA_VIAGEM.isoformat()}),
        "js_supabase": JS_SUPABASE,
        "nav": "".join(nav),
        "paineis": "\n".join(paineis),
        "icbusca": svg("search", 16),
        "sol": svg("sun", 17),
        "lua": svg("moon", 17),
        "carimbo": CARIMBO_VAGA,
        "cats": escapa_js([[c[0], c[1], c[2]] for c in CATEGORIAS]),
        "base": escapa_js(extrai_tarefas(docs.get("TAREFAS.md", ""))),
        "tarcab": escapa_js(extrai_cabecalho(docs.get("TAREFAS.md", ""))),
        "supa": escapa_js(le_config_supabase()),
        "ico": escapa_js({
            "check": svg("check", 13),
            "lapis": svg("lapis", 15),
            "lixo": svg("lixo", 15),
            "cal": svg("calendar", 12),
            "calbt": svg("calendar", 15),
            "vazio": svg("vazio", 46),
            "copiar": svg("copiar", 15),
        }),
    }

    # O carimbo entra por ultimo, calculado sobre o documento ja montado (com a
    # vaga ainda no lugar). Assim o mesmo conteudo sempre gera o mesmo carimbo.
    doc = doc.replace(CARIMBO_VAGA, _carimbo_versao(doc))

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    # newline="\n" e obrigatorio: sem isso o Python no Windows escreve CRLF, o
    # painel inteiro (~4.400 linhas) aparece como modificado a cada geracao, e
    # gerar em duas maquinas da conflito de merge. Ver .gitattributes.
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)

    # o Pages nao deve processar com Jekyll
    nojek = os.path.join(os.path.dirname(SAIDA), ".nojekyll")
    if not os.path.exists(nojek):
        open(nojek, "w").close()

    print("Painel gerado: %s" % SAIDA)
    print("%d abas, %d pendente%s, %d concluída%s."
          % (len(ABAS), pend, "" if pend == 1 else "s", feito, "" if feito == 1 else "s"))


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print("Erro ao gerar o painel: %s" % e, file=sys.stderr)
        raise
