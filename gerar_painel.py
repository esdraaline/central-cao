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
import subprocess
import sys
from datetime import date, datetime, timezone

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
    ("ESTUDOS.md",   "estudos",   "Estudos",    "livro"),
    ("GRADE.md",     "grade",     "Grade",      "grade"),
    ("ROTINA.md",    "rotina",    "Rotina",     "clock"),
    ("CONTATOS.md",  "contatos",  "Contatos",   "users"),
    ("DUVIDAS.md",   "duvidas",   "Dúvidas",    "help"),
    ("ANOTACOES.md", "anotacoes", "Anotações",  "note"),
    ("COMPRAS.md",   "compras",   "Compras",    "carrinho"),
    ("MALA.md",      "mala",      "Mala",       "mala"),
    ("VIAGENS.md",   "viagens",   "Viagens",    "map"),
    ("ENTORNO.md",   "entorno",   "Entorno",    "garfo"),
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
    "grade":    '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M3 14h18M9 4v17M15 4v17"/>',
    "livro":    '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v16H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20v4H6.5A2.5 2.5 0 0 1 4 19.5z"/><path d="M9 7h7"/>',
    "garfo":    '<path d="M6 2v7a2 2 0 0 0 4 0V2"/><path d="M8 9v13"/><path d="M17 2c-1.7 1.4-2.5 3.3-2.5 5.5 0 1.9.8 3 2.5 3.5v11"/>',
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
    "lista":    '<path d="m3 6 1.5 1.5L7 5"/><path d="m3 12 1.5 1.5L7 11"/>'
                '<path d="m3 18 1.5 1.5L7 17"/><path d="M11 6h10M11 12h10M11 18h10"/>',
    "repete":   '<path d="m17 2 3.5 3.5L17 9"/><path d="M3.5 12v-1.5a4 4 0 0 1 4-4h13"/><path d="M7 22l-3.5-3.5L7 15"/><path d="M20.5 12v1.5a4 4 0 0 1-4 4h-13"/>',
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

    txt = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", txt)
    txt = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", txt)

    for i, cod in enumerate(guardados):
        txt = txt.replace("\x00%d\x00" % i, "<code>%s</code>" % html.escape(cod, quote=False))
    return txt


def figura_svg(alt, caminho):
    """Embute um .svg da pasta mapas/ direto no HTML.

    O conteudo vai inline em vez de virar <img src>, para o painel continuar
    abrindo sem rede e para o desenho herdar as cores do tema (claro/escuro)
    pelas variaveis CSS da pagina.
    """
    destino = os.path.join(RAIZ, *caminho.split("/"))
    if not os.path.isfile(destino):
        return '<p class="mapa-erro">[mapa nao encontrado: %s]</p>' % html.escape(caminho)
    with open(destino, encoding="utf-8") as fig:
        desenho = fig.read().strip()
    legenda = "<figcaption>%s</figcaption>" % _inline(alt) if alt else ""
    return '<figure class="mapa">%s%s</figure>' % (desenho, legenda)


# Itens de checklist que comecam com um numero ("6 camisetas...") ou terminam
# com "- 5" / "- 2 pares" viram contador, para dar para marcar so uma parte.
_QTD_INICIO = re.compile(r"^(?:\*\*)?(\d{1,2})\s+[A-Za-zÀ-ÿ]")
_QTD_FIM = re.compile(r"[—-]\s*(\d{1,2})\s*"
                      r"(?:conjuntos?|pares?|mudas?|unidades?|un\.?)?\s*$", re.I)


def chave_item(texto):
    """Chave estavel de um item ticavel: md5 do texto, cortado em 10.

    E a mesma chave do `data-mk` das abas de lista e do `chave_do_item()` do
    sincroniza_ticados.py. Item so muda de identidade se o texto mudar, e o
    tique acompanha o texto em qualquer aparelho.
    """
    return hashlib.md5(texto.strip().encode("utf-8")).hexdigest()[:10]


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

    # Secao recolhida: um "<!-- extra -->" na linha logo abaixo de um "## Titulo"
    # transforma aquela secao inteira (ate o proximo "##") num <details> fechado.
    # Nasceu da aba Mala: as tres listas do que fazer nesta semana estavam
    # afogadas em referencia (tabela de alvo, estoque do armario, farda), e o que
    # ele quer ver ao abrir e o que tem que fazer. O resto continua ali, a um
    # clique, em vez de virar arquivo separado que ninguem le.
    aberto = [False]          # ha um <details> esperando fechamento?
    ultimo_h2 = [None]        # indice, em `saida`, do ultimo <h2> emitido

    def fecha_extra():
        if aberto[0]:
            saida.append("</details>")
            aberto[0] = False

    while i < len(linhas):
        ln = linhas[i]
        cru = ln.rstrip()
        strip = cru.strip()

        # marcador de secao recolhida (comentario HTML, invisivel em qualquer
        # outro leitor de markdown)
        if strip == "<!-- extra -->":
            if ultimo_h2[0] is not None:
                m2 = re.match(r"^<h2>(.*)</h2>$", saida[ultimo_h2[0]])
                if m2:
                    fecha_lista()
                    saida[ultimo_h2[0]] = ('<details class="extra">'
                                           '<summary data-b>%s</summary>' % m2.group(1))
                    aberto[0] = True
                    ultimo_h2[0] = None
            i += 1
            continue

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

        # mapa: ![legenda](mapas/arquivo.svg) sozinho na linha
        fig = re.match(r"^!\[([^\]]*)\]\((mapas/[^)]+\.svg)\)$", strip)
        if fig:
            fecha_lista()
            saida.append(figura_svg(fig.group(1), fig.group(2)))
            i += 1
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
            if n <= 2:
                fecha_extra()     # secao recolhida vai ate o proximo "##"
            saida.append("<h%d>%s</h%d>" % (n, _inline(conteudo), n))
            if n == 2:
                ultimo_h2[0] = len(saida) - 1
            i += 1
            continue

        # item de lista (com ou sem numeracao, com ou sem indentacao)
        m = re.match(r"^(\s*)(?:[-*]|(\d+)[.)])\s+(.*)$", cru)
        if m:
            indent = len(m.group(1).replace("\t", "  "))
            numerada = m.group(2) is not None
            item = m.group(3)
            # A chave e a quantidade do item ticavel saem SEMPRE desta primeira
            # linha, nunca do texto ja juntado. A identidade de uma caixinha e o
            # md5 do texto dela, e o sincroniza_ticados.py, do lado do Python, le
            # o arquivo linha a linha: se a chave passasse a incluir a
            # continuacao, as duas pontas parariam de se reconhecer e o tique
            # voltaria a nao descer para o .md. Foi exatamente o erro de
            # 18/08/2026, consertado em 23/08. Nao repetir.
            item_chave = item

            # Linha solta logo abaixo do item pertence AO ITEM (continuacao
            # preguicosa do markdown). Sem juntar aqui, um item quebrado em duas
            # linhas virava item + paragrafo solto, e um negrito aberto na
            # primeira linha e fechado na segunda aparecia com os asteriscos na
            # cara, porque o _inline roda por linha. Foi o que aconteceu com o
            # "**Mestrado Profissional...**" do STATUS.md em 23/08/2026.
            # Quebrar linha dentro de um item e coisa que qualquer um faz ao
            # escrever, entao quem tem que aguentar e o gerador.
            j = i + 1
            while j < len(linhas):
                seguinte = linhas[j].strip()
                # So quebra em MARCADOR de verdade. Testar por startswith("*")
                # cortava a continuacao que comeca em negrito ("**Julio
                # Prestes** (CPTM...")), e o item saia partido na tela.
                if (not seguinte
                        or re.match(r"^(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|>|\||```|-{3,}$)",
                                    seguinte)):
                    break
                item += " " + seguinte
                j += 1
            i = j - 1                      # o i += 1 do fim do bloco fecha a conta

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
                mk1 = re.match(r"^\[([ xX])\]\s*(.*)$", item_chave)
                base = mk1.group(2) if mk1 else mk.group(2)
                chave = chave_item(base)
                qtd = quantidade_do_item(base)
                # data-md: o que o ARQUIVO diz deste item (0 = em aberto;
                # N = quantas pecas ele considera prontas). Sem isto o painel
                # so sabia o que o proprio aparelho ja tinha ticado, e uma
                # marcacao feita em outro PC, mesmo ja dentro do .md, abria
                # desmarcada aqui. Ver a reconciliacao no JS.
                saida.append('<li class="%s" data-mk="%s" data-md="%d"%s>'
                             '<span class="box">%s</span>'
                             '<span>%s</span></li>' % (
                                 "ok" if feito else "pend", chave,
                                 (qtd or 1) if feito else 0,
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
            # Mesma correcao da lista: so MARCADOR de verdade quebra o
            # paragrafo. Testar por startswith("*") cortava a continuacao que
            # comeca em negrito, e a frase saia partida em duas na tela.
            if (not prox
                    or re.match(r"^(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|>|\||```|-{3,}$)",
                                prox)):
                break
            buf.append(prox)
            i += 1
        saida.append("<p>%s</p>" % _inline(" ".join(buf)))

    fecha_lista()
    fecha_extra()
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


def extrai_notas(texto):
    """Devolve as linhas que nao sao tarefa dentro de cada secao (###).

    O arquivo e remontado do zero toda vez que o painel ou a Action escrevem
    nele: cabecalho + secoes + linhas de tarefa. Tudo que estivesse dentro de
    uma secao sem ser tarefa se perdia calado nessa reescrita. Em 20/08/2026 foi
    o que comeu a nota da secao da Univesp, que guardava a hora do protocolo no
    SAE e o ponteiro para o outro repositorio. Robo que apaga nota nao deixa
    rastro no lugar certo: quem abre o arquivo depois nao tem como saber que
    faltou alguma coisa ali.

    Pega o que vier logo abaixo do "### ", ate a primeira tarefa daquela secao.
    Devolve {nome da secao: [linhas]}.
    """
    notas, secao, coletando = {}, None, False

    for linha in texto.splitlines():
        h = re.match(r"^(#{2,6})\s+(.*)$", linha)
        if h:
            secao = h.group(2).strip() if len(h.group(1)) >= 3 else None
            coletando = secao is not None
            continue
        if not coletando:
            continue
        if re.match(r"^\s*[-*]\s+\[[ xX]\]\s+", linha):
            coletando = False                 # da primeira tarefa em diante, para
            continue
        if linha.strip():
            notas.setdefault(secao, []).append(linha.rstrip())

    return notas


def _texto_puro(corpo):
    """Tira a sintaxe de markdown: na aba Tarefas o texto e exibido puro."""
    corpo = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", corpo)   # links
    corpo = re.sub(r"\*\*([^*]+)\*\*", r"\1", corpo)         # negrito
    corpo = re.sub(r"`([^`]+)`", r"\1", corpo)               # codigo
    return re.sub(r"\s{2,}", " ", corpo).strip(" -—")


def extrai_tarefas(texto):
    """Le as tarefas do TAREFAS.md em formato estruturado.

    Sintaxe reconhecida (a data e a categoria sao opcionais):
        - [ ] Entregar o artigo [15/09/2026] #dissertacao
        - [x] Tarefa ja concluida

    Linha de caixinha INDENTADA nao e tarefa: e item da lista de conferencia da
    tarefa logo acima ("5 cuecas", "shampoo"), e sai no campo "sub". E o que
    permite uma tarefa so, ticada de uma vez, carregar dentro dela a lista que
    se vai marcando item por item:

        - [ ] Domingo, arrumar a mala @semanal [23/08/2026] #pessoal
          - [ ] 5 cuecas
          - [ ] shampoo

    O campo "s" guarda o subtitulo (###) sob o qual a linha estava. E o que
    permite ao Exportar devolver o arquivo com as mesmas secoes, em vez de
    achatar tudo numa lista corrida.
    """
    tarefas = []
    validas = {c[0] for c in CATEGORIAS}
    secao = ""
    corrente = None            # a tarefa que esta recebendo itens indentados

    for linha in texto.splitlines():
        # "## Pendentes"/"## Concluidas" zeram a secao; "###" em diante define
        h = re.match(r"^(#{2,6})\s+(.*)$", linha)
        if h:
            secao = h.group(2).strip() if len(h.group(1)) >= 3 else ""
            # Titulo novo zera a tarefa corrente: item indentado logo abaixo de
            # um "###" nao pertence a ultima tarefa da secao ANTERIOR. Sem esta
            # linha ele grudava nela, e a reescrita automatica levava o item
            # junto, para outra secao do arquivo. Robo que muda linha de lugar
            # sem avisar e a mesma classe de erro que apagou as notas de secao
            # em 20/08/2026. Achado na auditoria de 23/08/2026.
            corrente = None
            continue

        m = re.match(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$", linha)
        if not m:
            continue
        recuo = len(m.group(1).expandtabs(4))
        feito = m.group(2).lower() == "x"
        corpo = m.group(3).strip()

        # item da lista de conferencia da tarefa anterior
        if recuo >= 2 and corrente is not None:
            item = _texto_puro(corpo)
            if item:
                corrente.setdefault("sub", []).append(
                    {"t": item, "k": chave_item(item)})
            continue

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
        corpo = _texto_puro(corpo)
        if corpo:
            corrente = {"t": corpo, "d": iso, "c": cat, "f": feito, "s": secao}
            tarefas.append(corrente)

    return tarefas


def extrai_qts(texto):
    """Le o quadro da semana no GRADE.md e devolve o que o painel precisa.

    O painel monta sozinho o cartao "hoje e quarta, voce tem isso". Quem sabe a
    data de quem esta olhando e o navegador, nao a geracao, entao o que sai
    daqui e so o dado: os dias, os blocos e os avisos. A conta de "hoje" e a de
    "que bloco esta correndo agora" ficam no JS_GUIA.

    A fonte e o GRADE.md, e nao um arquivo de dados separado, para nao existir
    duas verdades sobre a mesma semana. O formato lido e o que ja estava
    escrito la, so com a data completa no dia:

        **Quarta-feira 19/08/2026**

        | Bloco | Disciplina | Docente |
        |---|---|---|
        | 3 — 13h00 às 14h30 | D28 Policiamento Comunitario | Cel PM Barreto |

        **Aviso 19/08/2026:** embarque as 07h50 ...

    Dia declarado sem tabela e dia livre (a sexta da semana 1), o que e
    diferente de dia ausente: ausente quer dizer "o QTS dessa semana ainda nao
    entrou aqui", e o painel avisa isso em vez de dizer que nao tem aula.
    """
    dias = {}
    atual = None
    em_tabela = False

    DIA = re.compile(r"^\*\*(?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)"
                     r"(?:-feira)?\s+(\d{1,2})/(\d{1,2})/(\d{4})\*\*")
    AVISO = re.compile(r"^\*\*Aviso\s+(\d{1,2})/(\d{1,2})/(\d{4}):\*\*\s*(.+)$")
    LINHA = re.compile(r"^\|\s*(\d)\s*[—-]\s*(\d{1,2})h(\d{2})\s+às\s+"
                       r"(\d{1,2})h(\d{2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")

    def iso(d, m, a):
        try:
            return date(int(a), int(m), int(d)).isoformat()
        except ValueError:
            return None

    linhas = texto.splitlines()
    i = -1
    while i + 1 < len(linhas):
        i += 1
        linha = linhas[i]

        mv = AVISO.match(linha)
        if mv:
            k = iso(mv.group(1), mv.group(2), mv.group(3))
            # o aviso e um paragrafo, e paragrafo em markdown quebra em varias
            # linhas. Sem juntar a continuacao, o painel mostrava o texto
            # cortado no meio ("...para atividade").
            partes = [mv.group(4)]
            while i + 1 < len(linhas):
                seg = linhas[i + 1]
                if not seg.strip() or seg.lstrip()[0] in "*|#>-":
                    break
                partes.append(seg.strip())
                i += 1
            if k:
                dias.setdefault(k, {"blocos": [], "aviso": ""})
                # tira negrito/italico/codigo: o aviso e exibido como texto puro
                txt = re.sub(r"[*`_]", "", " ".join(partes))
                dias[k]["aviso"] = re.sub(r"\s{2,}", " ", txt).strip()
            em_tabela = False
            continue

        md = DIA.match(linha)
        if md:
            atual = iso(md.group(1), md.group(2), md.group(3))
            if atual:
                dias.setdefault(atual, {"blocos": [], "aviso": ""})
            em_tabela = False
            continue

        ml = LINHA.match(linha)
        if ml and atual:
            dias[atual]["blocos"].append({
                "n": int(ml.group(1)),
                "ini": "%02d:%s" % (int(ml.group(2)), ml.group(3)),
                "fim": "%02d:%s" % (int(ml.group(4)), ml.group(5)),
                "disc": re.sub(r"[*`]", "", ml.group(6)).strip(),
                "doc": re.sub(r"[*`]", "", ml.group(7)).strip(),
            })
            em_tabela = True
            continue

        # so a tabela imediatamente abaixo do dia conta. Depois que ela acaba,
        # o dia deixa de valer, senao a tabela das 31 disciplinas (que vem
        # muito depois) seria lida como se fosse do ultimo dia declarado.
        if em_tabela and not linha.lstrip().startswith("|"):
            atual = None
            em_tabela = False

    for k in dias:
        dias[k]["blocos"].sort(key=lambda b: b["n"])

    pel = ""
    mp = re.search(r"pelotão\s+\"?([A-E])\"?", texto)
    if mp:
        pel = mp.group(1)

    return {"pelotao": pel, "dias": dias}


def hora_do_md(arq):
    """Quando este .md mudou pela ultima vez, em ISO UTC.

    E a data do ultimo COMMIT que tocou o arquivo, nao a mtime: a Action faz
    checkout novo a cada rodada e toda mtime nasce "agora", entao o arquivo
    ganharia sempre de qualquer marcacao feita no navegador. Mesma regra e
    mesma fonte de hora que o sincroniza_tarefas.py usa do lado do Python.

    Exige historico no checkout (fetch-depth: 0 no publicar-painel.yml). Sem
    historico cai na mtime, que so degrada a decisao de conflito, nunca quebra
    o painel.
    """
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", arq],
                           cwd=RAIZ, capture_output=True, text=True, timeout=30)
        bruto = r.stdout.strip()
        if bruto:
            d = datetime.fromisoformat(bruto)
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except Exception:
        pass
    try:
        d = datetime.fromtimestamp(os.path.getmtime(os.path.join(RAIZ, arq)),
                                   timezone.utc)
        return d.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except OSError:
        return "1970-01-01T00:00:00.000Z"


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
/* o botao da conta leva texto ao lado do icone; o do tema continua quadrado */
#topo-conta{display:flex;gap:7px;padding:8px 11px;font:inherit;font-size:13px;font-weight:600}

/* A linha de estado da sincronizacao e clicavel em qualquer aba: e onde a
   pergunta "por que isto nao aparece no outro PC" nasce, entao e de onde se
   entra na conta. */
.tf-status{cursor:pointer}
.tf-status:hover{color:var(--tx2)}
.tf-status:hover .bola{box-shadow:0 0 0 3px rgba(127,127,127,.22)}

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
/* No desktop a barra quebra em linhas em vez de esconder aba no scroll.
   No celular segue rolando de lado, que ali funciona melhor. */
@media(min-width:900px){nav{flex-wrap:wrap;overflow-x:visible;row-gap:0}}
nav button{background:none;border:0;color:rgba(255,255,255,.72);font:600 13.5px/1 inherit;
  padding:12px 10px 13px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;
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
.tf-tag.rep{background:var(--bd);color:var(--tx2);cursor:pointer}
.tf-tag.rep svg{opacity:.9}
.tf-aviso{display:none;align-items:center;gap:8px;margin:0 0 12px;padding:10px 14px;
  border:1px solid var(--bd);border-left:3px solid var(--vd);border-radius:10px;
  background:var(--card);color:var(--tx2);font-size:13.5px}
.tf-aviso.on{display:flex}
.guia-lista{list-style:none;margin:0}
.guia-lista li{display:flex;gap:10px;align-items:flex-start;padding:9px 12px;margin:6px 0;
  border:1px solid var(--bd);border-left-width:3px;border-radius:9px;background:var(--card2);
  font-size:14.5px;color:var(--tx)}
.guia-bloco.vencido .guia-lista li{border-left-color:var(--vm)}
.guia-bloco.agora .guia-lista li{border-left-color:var(--al)}
.guia-lista li .pt{width:8px;height:8px;border-radius:50%;flex:none;margin-top:7px;background:var(--tx3)}
.guia-lista li .qd{color:var(--tx3);font-size:12.5px;white-space:nowrap;margin-left:auto;
  padding-left:8px;font-variant-numeric:tabular-nums}
/* quadro do dia: as aulas de hoje, lidas do QTS (GRADE.md). Fica entre o
   topo e as tarefas porque a pergunta "onde eu tenho que estar agora" vem
   antes de "o que eu tenho que fazer". */
.guia-aula{padding:15px 22px 0}
.qts-aviso{display:flex;gap:9px;align-items:flex-start;background:var(--al-bg);
  border:1px solid var(--al);border-radius:9px;padding:9px 12px;margin-bottom:11px;
  font-size:13.5px;color:var(--tx);line-height:1.4}
.qts-aviso b{color:var(--al);flex:none}
.qts-lista{list-style:none;margin:0}
.qts-lista li{display:flex;gap:12px;align-items:center;padding:9px 12px;margin:6px 0;
  border:1px solid var(--bd);border-left-width:3px;border-radius:9px;background:var(--card2)}
.qts-lista li .hr{font-size:13px;font-weight:700;color:var(--tx2);flex:none;width:46px;
  font-variant-numeric:tabular-nums;line-height:1.3}
.qts-lista li .hr i{display:block;font-style:normal;font-size:11px;font-weight:500;color:var(--tx3)}
.qts-lista li .ds{min-width:0;flex:1}
.qts-lista li .ds b{display:block;font-size:14.5px;font-weight:650;color:var(--tx);line-height:1.3}
.qts-lista li .ds i{font-style:normal;font-size:12.5px;color:var(--tx2)}
.qts-lista li .qd{font-size:12px;font-weight:700;color:var(--tx3);white-space:nowrap;
  margin-left:auto;padding-left:8px;text-transform:uppercase;letter-spacing:.5px}
.qts-lista li.passou{opacity:.5}
.qts-lista li.passou .ds b{text-decoration:line-through;text-decoration-color:var(--tx3)}
.qts-lista li.agora{border-color:var(--vm);border-left-color:var(--vm);background:var(--card)}
.qts-lista li.agora .qd{color:var(--vm)}
.qts-lista li.prox{border-left-color:var(--al)}
.qts-lista li.prox .qd{color:var(--al)}
.guia-tudoem{display:flex;gap:9px;align-items:center;color:var(--ok);font-size:14px;
  padding:13px 0 4px;font-weight:600}
.guia-nota{font-size:13px;color:var(--tx2);margin-top:13px;padding-top:12px;
  border-top:1px solid var(--bd)}
.guia-nota b{color:var(--tx)}
@media(max-width:560px){
  .guia-topo{padding:15px 17px}
  .guia-corpo{padding:4px 17px 16px}
  .guia-aula{padding:13px 17px 0}
  .qts-lista li{gap:10px;padding:8px 10px}
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
/* secao recolhida (<details class="extra">): referencia que nao pode disputar
   espaco com a lista do que fazer hoje. Fechada por padrao. */
.card details.extra{border:1px solid var(--bd);border-radius:11px;background:var(--card2);
  margin:11px 0;overflow:hidden}
.card details.extra>summary{cursor:pointer;list-style:none;padding:12px 15px;
  font-size:14px;font-weight:650;color:var(--tx2);display:flex;align-items:center;gap:9px;
  user-select:none}
.card details.extra>summary::-webkit-details-marker{display:none}
.card details.extra>summary::before{content:"";width:7px;height:7px;flex:none;
  border-right:2px solid var(--vm-cl);border-bottom:2px solid var(--vm-cl);
  transform:rotate(-45deg);margin-left:2px;transition:transform .15s}
.card details.extra[open]>summary::before{transform:rotate(45deg)}
.card details.extra>summary:hover{color:var(--tx)}
.card details.extra[open]>summary{border-bottom:1px solid var(--bd);color:var(--tx)}
.card details.extra>*:not(summary){margin-left:15px;margin-right:15px}
.card details.extra>*:last-child{margin-bottom:14px}
.card details.extra h3:first-of-type{margin-top:13px}
.card details.extra>ul,.card details.extra>ol{margin-left:36px}
/* a marca "extras" so aparece no primeiro <details> de uma sequencia */
.card details.extra+details.extra{margin-top:-4px}
blockquote{border-left:3px solid var(--vm);background:var(--card2);padding:11px 16px;
  border-radius:0 9px 9px 0;margin:13px 0;font-size:13.5px;color:var(--tx2)}
del{color:var(--tx3);text-decoration-thickness:1px}
code{background:var(--card2);border:1px solid var(--bd);border-radius:5px;padding:1.5px 5px;
  font:.88em/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--vm-cl)}
pre{background:var(--card2);border:1px solid var(--bd);border-radius:10px;padding:15px 17px;
  overflow-x:auto;margin:13px 0}
pre code{background:none;border:0;padding:0;color:var(--tx2);font-size:12.5px;line-height:1.55}
hr{border:0;border-top:1px solid var(--bd);margin:20px 0}
.arq{color:var(--tx2);font-size:.95em;border-bottom:1px dotted var(--tx3);cursor:help;
  overflow-wrap:anywhere}
.arq svg{flex:none;opacity:.55;vertical-align:-2px;margin-right:3px}

/* mapas desenhados (svg embutido da pasta mapas/) */
figure.mapa{margin:18px 0;padding:14px 12px 10px;border:1px solid var(--bd);
  border-radius:12px;background:var(--card2);overflow-x:auto}
/* min-width: sem isso o desenho encolhe junto com a tela e o texto do svg
   fica ilegivel no celular. Melhor manter o tamanho e deixar arrastar de lado. */
figure.mapa svg{display:block;width:100%;min-width:560px;max-width:640px;
  height:auto;margin:0 auto}
figure.mapa figcaption{margin-top:10px;text-align:center;color:var(--tx3);
  font-size:12.5px;line-height:1.5}
@media(max-width:620px){
  figure.mapa figcaption::before{content:"Arraste o desenho para o lado. ";
    color:var(--vm-cl);font-weight:600}
}
.mapa-erro{color:var(--vm-cl);font-size:13px}

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
/* lista de conferencia dentro de uma tarefa: um clique por item */
.tf-tag.lista{background:var(--card2);border:1px solid var(--bd);color:var(--tx2);
  font-family:inherit;cursor:pointer}
.tf-tag.lista:hover{border-color:var(--vm);color:var(--vm)}
.tf-tag.lista.cheia{background:rgba(15,157,88,.12);border-color:var(--ok);color:var(--ok)}
.tf-sub{list-style:none;margin:9px 0 1px;padding:0;display:grid;gap:5px}
.tf-sub.fechada{display:none}
.tf-si{display:flex;align-items:center;gap:9px;padding:7px 11px;border-radius:9px;
  border:1px solid var(--bd);background:var(--card2);font-size:13.5px;color:var(--tx2);
  cursor:pointer;user-select:none;transition:border-color .12s,background .12s}
.tf-si:hover{border-color:var(--vm);background:var(--card)}
.tf-si:active{transform:scale(.995)}
.tf-si .box{width:17px;height:17px;flex:none;border-radius:5px;
  border:2px solid var(--bd);display:grid;place-items:center;color:#fff}
.tf-si.ok{opacity:.6}
.tf-si.ok .box{background:var(--ok);border-color:var(--ok)}
.tf-si.ok>span:nth-child(2){text-decoration:line-through}
.tf-edit{width:100%;background:var(--card2);border:1px solid var(--vm);border-radius:7px;
  padding:6px 9px;color:var(--tx);font:14.5px/1.4 inherit}
.tf-edit:focus{outline:none}

/* estado vazio */
.tf-vazio{text-align:center;padding:44px 20px;color:var(--tx3)}
.tf-vazio svg{opacity:.35;margin-bottom:11px}
.tf-vazio p{font-size:14.5px;margin:0 0 4px;color:var(--tx2)}
.tf-vazio small{font-size:13px}

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
      gravarEspelho();
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
      reconciliarComArquivo();
    }
    aplicarSub();
  }

  /* A lista de conferencia de uma tarefa (as linhas indentadas do TAREFAS.md)
     e sempre do ARQUIVO. O painel tica os itens, mas nao cria nem apaga item,
     entao nao existe conflito para resolver: a cada abertura ela e recopiada
     por cima. Corrigir "shampo" para "shampoo" no .md chega ao painel na
     proxima carga, sem exportar nada.                                      */
  function aplicarSub(){
    var doArquivo={};
    BASE.forEach(function(b){
      if(b.sub&&b.sub.length)doArquivo[idBase(b.t)]=b.sub;
    });
    tarefas.forEach(function(t){
      var s=doArquivo[t.id];
      if(s)t.sub=s; else if(t.sub)delete t.sub;
    });
  }

  /* ------------------ reconciliacao com o TAREFAS.md ---------------------
     O painel sempre soube trazer tarefa NOVA do arquivo e tirar a que sumiu
     dele. O que faltava era o meio: tarefa que existe nos dois lados com
     valores diferentes. Ela ficava congelada no que este aparelho tinha
     gravado, entao remarcar uma data no PC do trabalho, deixar isso chegar ao
     TAREFAS.md e abrir o painel em casa mostrava a data velha, para sempre.
     Era o mesmo desenho das caixinhas, e as duas pontas foram corrigidas
     juntas (21/08/2026).

     Como se decide sem chutar: guardamos um ESPELHO do que o arquivo dizia na
     ultima vez que o painel abriu. Com ele da para separar "o arquivo mudou"
     de "eu mudei aqui":

       arquivo mudou, eu nao  -> vale o arquivo
       eu mudei, o arquivo nao -> vale o meu (edicao ainda nao exportada)
       os dois mudaram         -> quem mexeu por ultimo, comparando a hora do
                                  commit do .md com o `mod` da tarefa

     Sem espelho (primeira abertura depois desta versao) cai direto na regra de
     quem mexeu por ultimo, que e a mesma do sincroniza_tarefas.py. Isso e o
     que faz a correcao valer ja na primeira vez, sem descartar o que foi
     mexido aqui depois do ultimo commit.

     Quando o arquivo vence, a tarefa fica com `sinc:true` e `mod` igual a hora
     do commit: ela nao volta a subir para a nuvem. Reenviar faria o `mod` da
     nuvem REGREDIR para uma hora antiga e a rodada seguinte da Action
     desfaria a mudanca.                                                    */
  var K_ESPELHO='cao-espelho-md';

  function fotoDoArquivo(){
    var f={};
    BASE.forEach(function(b){
      f[idBase(b.t)]={d:b.d||null,c:b.c||'',f:!!b.f};
    });
    return f;
  }
  function gravarEspelho(){gravarLS(K_ESPELHO,fotoDoArquivo())}
  function mesmoValor(a,b){
    return !!a&&!!b&&(a.d||null)===(b.d||null)&&(a.c||'')===(b.c||'')&&!!a.f===!!b.f;
  }
  function horaDoArquivo(){
    var m=(window.ARQ_MOD||{})['ab-tarefas'];
    return m?(Date.parse(m)||0):0;
  }

  function reconciliarComArquivo(){
    if(!BASE.length)return 0;          /* arquivo vazio ou ilegivel: nao mexe */
    var espelho=lerLS(K_ESPELHO,null);
    var tArq=horaDoArquivo();
    var foto=fotoDoArquivo();
    var porId={};
    tarefas.forEach(function(t){porId[t.id]=t});
    var mudou=0;
    Object.keys(foto).forEach(function(id){
      var arq=foto[id], t=porId[id];
      if(!t)return;
      var loc={d:t.data||null,c:t.cat||'',f:!!t.feito};
      if(mesmoValor(loc,arq))return;
      var base=espelho&&espelho[id], venceArquivo;
      if(base){
        var arqMudou=!mesmoValor(base,arq), locMudou=!mesmoValor(base,loc);
        if(arqMudou&&!locMudou)venceArquivo=true;
        else if(locMudou&&!arqMudou)venceArquivo=false;
        else venceArquivo=tArq>(Date.parse(t.mod||'')||0);
      }else{
        venceArquivo=tArq>(Date.parse(t.mod||'')||0);
      }
      if(!venceArquivo)return;
      t.data=arq.d;t.cat=arq.c;t.feito=arq.f;
      t.mod=new Date(tArq||Date.now()).toISOString();
      t.sinc=true;
      mudou++;
    });
    gravarLS(K_ESPELHO,foto);
    if(mudou)gravarLS(CHAVE,tarefas);
    return mudou;
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

  /* proximo dia da semana pedido, a partir de hoje (hoje conta) */
  function proximoDia(idx){
    var d=hoje(); d.setDate(d.getDate()+((idx-d.getDay()+7)%7));
    return d;
  }

  function adicionar(){
    var bruto=inp.value.trim();
    if(!bruto)return;
    /* "toda quinta separar a roupa" vira tarefa que se repete: o trecho sai
       do texto antes da leitura da data, senao sobraria um "toda" solto. */
    var rp=REP.doTexto(bruto);
    var limpo=rp?bruto.replace(rp.trecho,' ').replace(/\s{2,}/g,' ').trim():bruto;
    var r=lerData(limpo);
    var d=inData.value?deIso(inData.value):r.data;
    var texto=r.data?r.texto:limpo;
    if(!texto)texto=limpo||bruto;
    if(rp){
      if(!d)d=rp.dia>=0?proximoDia(rp.dia):hoje();
      texto=REP.com(texto,rp.tipo);
    }
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
    /* Tarefa que se repete nao vai para Concluidas: ela rola para a proxima
       vez. Ir para Concluidas somaria uma linha por semana no TAREFAS.md e
       tiraria da lista justamente o lembrete que ela existe para dar.     */
    var rep=REP.de(t.txt);
    if(rep&&!t.feito){
      var prox=REP.proxima(t.data||iso(hoje()),rep);
      if(prox){
        t.data=iso(prox);t.mod=new Date().toISOString();t.sinc=false;
        /* a lista de conferencia e da vez, nao da tarefa: ao rolar para a
           semana seguinte ela volta zerada, senao voltaria toda ticada e nao
           serviria para nada */
        var zerados=subZera(t);
        salvar();
        if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
        avisar('Feita desta vez. Volta '+quandoVolta(prox)+
               (zerados?', com a lista zerada.':'.'));
        return;
      }
    }
    t.feito=!t.feito;t.mod=new Date().toISOString();t.sinc=false;
    salvar();
    if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
  }

  /* Liga e desliga a repeticao pela etiqueta, sem passar pela edicao de
     texto. Desligar nao mexe na data: a tarefa vira uma tarefa comum na
     data em que ja estava.                                              */
  function alternarRep(id){
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!t)return;
    var rep=REP.de(t.txt);
    t.txt=rep?REP.sem(t.txt):REP.com(t.txt,'semanal');
    t.mod=new Date().toISOString();t.sinc=false;
    salvar();
    if(window.SUPA&&SUPA.ativo())SUPA.enviar(t);
    avisar(rep?'Não repete mais. Virou uma tarefa comum.':
               'Passa a repetir '+REP.rotulo(t.data,'semanal')+'.');
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
    campo.value=REP.sem(t.txt);campo.focus();campo.select();
    var fim=function(ok){
      if(ok&&campo.value.trim()){
        /* a marca de recorrencia nao aparece no campo, entao ela e devolvida
           depois da edicao: sem isso, corrigir uma virgula desligaria a
           repeticao sem ninguem pedir.                                    */
        var novo=campo.value.trim(), rep=REP.de(t.txt);
        if(rep&&!REP.de(novo))novo=REP.com(novo,rep);
        t.txt=novo;t.mod=new Date().toISOString();t.sinc=false;
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
    corpo.innerHTML='<div class="tf-txt">'+esc(REP.sem(t.txt))+'</div>'+
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

  /* -------------- o aviso de "ainda nao foi para o TAREFAS.md" -----------
     Removido em 23/08/2026, com a contagem de divergencias que o alimentava.

     Ele nasceu em 12/08, quando levar o painel para o arquivo era trabalho do
     Josemar: copiar do Exportar e colar no .md. Nessa epoca a pendencia era
     dele e o aviso fazia sentido. Em 14/08 a Action passou a fechar o ciclo
     sozinha, de hora em hora, e o aviso virou o retrato de uma fila que nao e
     mais de ninguem: bastava ticar uma tarefa para a tarja amarela subir na
     tela, dizendo "1 tarefa alterada ainda nao foi" e, no paragrafo seguinte,
     "nao precisa fazer nada". Alarme que ele mesmo desmente nao e informacao,
     e barulho, e barulho com cara de pendencia cobra quem le.

     Nada foi trocado por um aviso menor de proposito. O que sobra ja diz tudo,
     sem cobrar: a linha de estado do topo ("Salvo na nuvem", "Sem conexao",
     "Somente neste aparelho") mostra o unico ponto onde ainda pode haver
     alguma coisa presa neste aparelho, e o botao Exportar continua ali do lado
     como saida de emergencia. Depois que a alteracao chega a nuvem, levar isso
     ao arquivo e servico de robo, e robo nao precisa de tarja.

     Se um dia for preciso saber se o arquivo esta velho, a conta e comparar
     `tarefas` com a BASE (o que o TAREFAS.md dizia quando o painel foi
     gerado) - era isso que a funcao divergencias() fazia. Fica registrado
     aqui para nao ser reinventado do zero, nao para voltar a tela.        */

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

  /* =============== lista de conferencia dentro de uma tarefa ==============
     "Arrumar a mala" e UMA tarefa, ticada uma vez por semana, mas por dentro
     ela e uma lista: shampoo e um clique, energetico e outro. Os itens vem
     indentados no TAREFAS.md e o painel os mostra dentro da propria tarefa.

     Onde mora o tique de cada item: NAO na tarefa. Ele vai para o mesmo lugar
     das caixinhas das abas Compras e Mala (window.TICADOS, tabela
     cao_ticados), com a chave 'tf/<id da tarefa>/<chave do item>'. Dois
     motivos, e o primeiro nao tem volta:

       1. o id de uma tarefa nascida no arquivo e derivado do TEXTO dela
          (idBase). Se o tique morasse no texto, cada clique geraria um id
          novo e o arquivo, a nuvem e o painel parariam de se reconhecer -
          exatamente a duplicata em massa de 12/08/2026;
       2. de graca vem a sincronizacao entre aparelhos, que a tabela de
          ticados ja faz desde 21/08/2026.

     No arquivo o item fica sempre "- [ ]": ali a lista e o molde, nao o
     diario de bordo. Quem guarda o que ja foi separado nesta semana e o
     navegador mais a nuvem, e a tarefa que se repete zera a propria lista
     quando rola para a semana seguinte.                                   */
  function subChave(t,s){return 'tf/'+t.id+'/'+s.k}
  function subMapa(){
    return (window.TICADOS&&TICADOS.todos&&TICADOS.todos())||{};
  }
  function subFeito(t,s){
    var v=subMapa()[subChave(t,s)];
    return !!(v&&v.n);
  }
  function subContagem(t){
    var m=subMapa(), n=0;
    (t.sub||[]).forEach(function(s){
      var v=m[subChave(t,s)];
      if(v&&v.n)n++;
    });
    return n;
  }
  function subPoe(t,s,valor){
    if(!window.TICADOS)return;
    var m=TICADOS.todos();
    /* grava ate o zero, em vez de apagar a chave: sem a linha, a nuvem
       devolveria na proxima sincronizacao o que voce acabou de desmarcar. */
    m[subChave(t,s)]={n:valor?1:0,m:new Date().toISOString(),s:false};
    TICADOS.salvar();
    if(window.TICADOS_SYNC)TICADOS_SYNC();
  }
  function subZera(t){
    if(!window.TICADOS||!(t.sub&&t.sub.length))return 0;
    var m=TICADOS.todos(), agora=new Date().toISOString(), n=0;
    t.sub.forEach(function(s){
      var k=subChave(t,s);
      if(m[k]&&m[k].n){m[k]={n:0,m:agora,s:false};n++}
    });
    if(n){TICADOS.salvar();if(window.TICADOS_SYNC)TICADOS_SYNC()}
    return n;
  }

  /* Aberta ou fechada. Uma lista de 15 itens aberta em toda tarefa viraria
     uma parede; fechada em toda tarefa esconderia justamente o que se veio
     fazer. Entao o padrao e abrir a lista do que e para hoje ou esta
     atrasado, e o clique na etiqueta manda mais que o padrao.             */
  var K_ABERTAS='cao-tf-abertas';
  var abertas=lerLS(K_ABERTAS,{})||{};
  function subAberta(t){
    if(Object.prototype.hasOwnProperty.call(abertas,t.id))return !!abertas[t.id];
    if(!t.data||t.feito)return false;
    return dias(hoje(),deIso(t.data))<=0;
  }
  function subAlternaAberta(t){
    abertas[t.id]=!subAberta(t);
    gravarLS(K_ABERTAS,abertas);
  }

  function subHTML(t){
    var sub=t.sub||[];
    if(!sub.length)return '';
    var m=subMapa();
    return '<ul class="tf-sub'+(subAberta(t)?'':' fechada')+'">'+
      sub.map(function(s,i){
        var v=m[subChave(t,s)], ok=!!(v&&v.n);
        return '<li class="tf-si'+(ok?' ok':'')+'" data-si="'+i+'">'+
               '<span class="box">'+(ok?ICO.check:'')+'</span>'+
               '<span>'+esc(s.t)+'</span></li>';
      }).join('')+'</ul>';
  }

  function alternarSub(id,i,no){
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!t||!t.sub||!t.sub[i])return;
    var s=t.sub[i], marca=!subFeito(t,s);
    subPoe(t,s,marca);
    /* pinta so a linha clicada e o contador, em vez de redesenhar a aba
       inteira. A lista tem 15 itens e sao 15 cliques seguidos: refazer a
       lista a cada um fazia a tela piscar e perdia a rolagem no celular. */
    if(no){
      no.classList.toggle('ok',marca);
      no.firstChild.innerHTML=marca?ICO.check:'';
      var cx=no.closest('.tf-item'), et=cx&&cx.querySelector('.tf-tag.lista');
      if(et){
        var q=subContagem(t);
        et.innerHTML=(ICO.lista||'')+q+' de '+t.sub.length;
        et.classList.toggle('cheia',q>=t.sub.length);
      }
      return;
    }
    desenhar();
  }

  function alternarLista(id){
    var t=tarefas.filter(function(x){return x.id===id})[0];
    if(!t)return;
    subAlternaAberta(t);
    desenhar();
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
    var rep=REP.de(t.txt);
    if(rep){
      meta+='<button class="tf-tag rep" data-ac="rep" '+
            'title="Se repete. Clique para deixar de repetir">'+
            (ICO.repete||'')+REP.rotulo(t.data,rep)+'</button>';
    }
    if(t.sub&&t.sub.length){
      var q=subContagem(t), aberta=subAberta(t);
      meta+='<button class="tf-tag lista'+(q>=t.sub.length?' cheia':'')+'" '+
            'data-ac="lista" title="'+(aberta?'Fechar a lista':'Abrir a lista')+
            '">'+(ICO.lista||'')+q+' de '+t.sub.length+'</button>';
    }
    if(t.cat&&CATS[t.cat]){
      meta+='<span class="tf-tag cat" style="background:'+CATS[t.cat].cor+'">'+
            CATS[t.cat].rot+'</span>';
    }
    if(!t.sinc&&window.SUPA&&SUPA.ativo()){
      meta+='<span class="tf-tag dt" title="Ainda não sincronizada">•</span>';
    }
    return '<div class="'+cls+'" data-id="'+t.id+'">'+
      '<button class="tf-check" data-ac="ok" title="'+
        (rep?'Marcar como feita desta vez':'Marcar como feita')+'">'+ICO.check+'</button>'+
      '<div class="tf-corpo"><div class="tf-txt">'+esc(REP.sem(t.txt))+'</div>'+
      (meta?'<div class="tf-meta">'+meta+'</div>':'')+subHTML(t)+'</div>'+
      '<div class="tf-acoes">'+
        '<button class="tf-ac" data-ac="dt" title="'+
          (d?'Mudar a data':'Marcar uma data')+'">'+ICO.calbt+'</button>'+
        '<button class="tf-ac" data-ac="ed" title="Editar o texto">'+ICO.lapis+'</button>'+
        '<button class="tf-ac del" data-ac="del" title="Excluir">'+ICO.lixo+'</button>'+
      '</div></div>';
  }

  function curtaData(d){
    return String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0');
  }

  /* "na quinta, 03/09". O dia da semana entra por extenso porque e por ele
     que o rodizio da mala e lembrado, nao pelo numero.                   */
  function quandoVolta(d){
    var g=d.getDay();
    var nome=SEMANA[g].replace('terca','terça').replace('sabado','sábado');
    return (g===0||g===6?'no ':'na ')+nome+', '+curtaData(d);
  }

  /* Recado curto acima da lista. Existe por causa da tarefa que se repete:
     ticada, ela some da lista e volta com outra data, e sem uma palavra na
     tela isso parece que o tique nao pegou.                              */
  var avisoTempo=null;
  function avisar(msg){
    var cx=el('#tf-aviso');
    if(!cx&&lista&&lista.parentNode){
      cx=document.createElement('div');
      cx.id='tf-aviso';cx.className='tf-aviso';
      lista.parentNode.insertBefore(cx,lista);
    }
    if(!cx)return;
    cx.innerHTML=(ICO.repete||'')+'<span></span>';
    cx.querySelector('span').textContent=msg;
    cx.classList.add('on');
    clearTimeout(avisoTempo);
    avisoTempo=setTimeout(function(){cx.classList.remove('on')},6000);
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
      /* A lista de conferencia volta indentada e SEMPRE em aberto. No arquivo
         ela e o molde da semana; o que ja foi separado esta gravado na nuvem
         de ticados, e nao aqui. Sem esta parte, colar o exportado por cima do
         TAREFAS.md apagaria a lista inteira em silencio.                   */
      (t.sub||[]).forEach(function(x){s+='\n  - [ ] '+x.t});
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
      /* As notas da secao voltam logo abaixo do subtitulo, do jeito que
         estavam no arquivo. Sem isto o exportado apaga toda linha que nao
         seja tarefa: em 20/08/2026 sumiu assim a nota do protocolo da Univesp. */
      var nt=(window.TAR_NOTAS||{})[s];
      corpo+='\n### '+s+'\n'+(nt&&nt.length?nt.join('\n')+'\n':'')+
             grupos[s].map(linha).join('\n')+'\n';
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
    /* item da lista de conferencia: a linha inteira e o alvo do clique, do
       jeito que ja funciona nas abas Compras e Mala */
    var si=e.target.closest('.tf-si');
    if(si){
      alternarSub(si.closest('.tf-item').dataset.id,parseInt(si.dataset.si,10),si);
      return;
    }
    var b=e.target.closest('[data-ac]');
    if(!b)return;
    var id=b.closest('.tf-item').dataset.id;
    if(b.dataset.ac==='ok')alternar(id);
    else if(b.dataset.ac==='del')excluir(id);
    else if(b.dataset.ac==='ed')editar(id);
    else if(b.dataset.ac==='dt')editarData(id);
    else if(b.dataset.ac==='rep')alternarRep(id);
    else if(b.dataset.ac==='lista')alternarLista(id);
  };

  carregar();
  desenhar();
  previa();

  /* exposto para a camada de sincronizacao */
  window.TAREFAS={
    todas:function(){return tarefas},
    /* aplicarSub de novo porque a tarefa que desce da nuvem vem sem lista: a
       coluna `txt` do Supabase nao carrega os itens, quem os tem e o
       TAREFAS.md. Sem esta linha, sincronizar fazia a lista sumir da tela
       ate a proxima vez que a pagina fosse aberta. */
    definir:function(novas){tarefas=novas;aplicarSub();salvar()},
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
      estado('on','Salvo na nuvem','Tudo o que você marcou está salvo na nuvem');
      tic('on','Salvo na nuvem','Tudo o que você marcou está salvo na nuvem');
    }else if(configurado()){
      estado('','Somente neste aparelho','Clique aqui para entrar e sincronizar');
      tic('','Somente neste aparelho',
          'Clique aqui para entrar e sincronizar entre aparelhos');
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
      estado('off','Sem conexão','Sobe sozinho quando a rede voltar');
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
      tic('on','Salvo na nuvem','Tudo o que você marcou está salvo na nuvem');
    }).catch(function(e){
      if(e&&(e.status===401||e.status===403))
        tic('erro','Sessão expirada','Clique aqui para entrar de novo');
      else
        tic('off','Sem conexão','Sobe sozinho quando a rede voltar');
      throw e;
    });
  }
  /* espera o dedo parar antes de subir, para nao mandar um POST por clique */
  var tmTic=null;
  window.TICADOS_SYNC=function(){
    if(!ativo()){
      tic('','Somente neste aparelho','Clique aqui para entrar e sincronizar');
      return;
    }
    tic('','Salvando...');
    clearTimeout(tmTic);
    tmTic=setTimeout(function(){sincTicados().catch(function(){})},1200);
  };

  var ultimaSinc=0;

  function sincronizar(){
    if(!ativo()||sincronizando)return Promise.resolve();
    sincronizando=true;
    ultimaSinc=Date.now();
    var ticOk=true;
    estado('','Salvando...');
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
      /* Guarda QUEM entrou neste lote. Antes, ao terminar o POST, o codigo
         marcava sinc=true em TODAS as tarefas. Parece detalhe e nao e: sinc
         false e a fila de reenvio. Se uma tarefa fosse ticada durante a
         requisicao, ou se o envio individual dela tivesse acabado de falhar,
         ela era marcada como sincronizada sem nunca ter subido - e, sem
         sinc=false, ninguem tentava de novo. A alteracao morria calada no
         aparelho. (23/08/2026)                                             */
      var noLote={};
      subir.forEach(function(l){noLote[l.id]=1});
      return api('/rest/v1/cao_tarefas',{
        method:'POST',
        headers:{'Prefer':'resolution=merge-duplicates,return=minimal'},
        body:JSON.stringify(subir)
      }).then(function(){
        window.TAREFAS.todas().forEach(function(t){if(noLote[t.id])t.sinc=true});
        window.TAREFAS.salvar();
      });
    }).then(function(){
      /* 4. e, na mesma passada, os itens ticados das listas */
      return sincTicados().catch(function(){ticOk=false});
    }).then(function(){
      sincronizando=false;
      window.TAREFAS.redesenhar();
      pintaConta();
      /* pintaConta pinta as duas linhas de verde so porque a sessao esta viva.
         Se as MARCACOES nao subiram, verde e mentira - e e essa linha que ele
         olha antes de desligar o PC ("ticou os 15 itens da mala, deu Salvo na
         nuvem, pode desligar"). Entao o estado de falha volta por cima.
         Achado da auditoria de 23/08/2026.                                 */
      if(!ticOk)tic('off','Sem conexão','Sobe sozinho quando a rede voltar');
    }).catch(function(e){
      sincronizando=false;
      if(e&&(e.status===401||e.status===403)){
        sair();
        estado('erro','Sessão expirada','Clique aqui para entrar de novo');
      }else{
        estado('off','Sem conexão','Fica guardado aqui até a rede voltar');
      }
    });
  }

  /* ------------------------------- eventos ------------------------------- */
  /* Abrir a conta nao e mais assunto da aba Tarefas. O gatilho e o botao do
     cabecalho e, em qualquer aba, a propria linha de estado: quem le
     "Somente neste aparelho" e quer resolver clica ali mesmo, que e onde a
     duvida aparece. Delegado no documento porque as linhas de estado das
     listas sao criadas depois, quando cada aba monta o contador.           */
  function abrirConta(){
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
        '<code>SUPABASE.md</code>). Por enquanto, tudo fica salvo apenas neste '+
        'aparelho, e o botão <b>Exportar</b> é o que garante que nada se perca.';
      el('#conta-entrar').disabled=true;
    }
    window.TAREFAS.modal.abrir('#modal-conta');
    if(!logado&&configurado())setTimeout(function(){el('#conta-email').focus()},80);
  }
  document.addEventListener('click',function(e){
    if(e.target.closest('#topo-conta,#tf-status,.mk-sinc'))abrirConta();
  });
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

  /* -------------------- voltar para a aba busca a nuvem -------------------
     O painel buscava a nuvem so quando a PAGINA abria. Aba deixada aberta no
     celular desde ontem mostrava o estado velho ate alguem recarregar na mao,
     e como ninguem recarrega uma aba que ja esta na tela, o aparelho ficava
     mentindo o dia inteiro. Agora, ao voltar para a aba, ele busca de novo.

     Duas travas, as duas por motivo concreto:

       - 30 segundos entre uma busca e outra, senao cada alt-tab viraria uma
         requisicao;
       - nada acontece com uma edicao aberta na tela. Sincronizar redesenha a
         lista inteira, e redesenhar por baixo de um campo de texto aberto
         apagaria o que estava sendo digitado. Quem sai para copiar um dado e
         volta para colar nao pode perder a frase no caminho.               */
  document.addEventListener('visibilitychange',function(){
    if(document.visibilityState!=='visible'||!ativo())return;
    if(Date.now()-ultimaSinc<30000)return;
    if(document.querySelector('.tf-edit,.tf-dtin'))return;
    sincronizar();
  });
  window.addEventListener('offline',function(){
    if(ativo())estado('off','Sem conexão','Fica guardado aqui até a rede voltar');
  });

  window.SUPA={ativo:ativo,enviar:enviar,apagar:apagar,sincronizar:sincronizar};

  ses=lerLS(K_SES,null);
  pintaConta();
  if(ativo())sincronizar();
})();
"""

JS = r"""
/* ===================== tarefa que se repete =====================
   A marca de recorrencia vive no PROPRIO TEXTO da tarefa ("@semanal",
   "@quinzenal", "@mensal"), e nao numa coluna nova. E o que faz ela
   atravessar de graca os tres lugares por onde a tarefa passa: a linha do
   TAREFAS.md, a coluna txt do Supabase e a Action que sincroniza os dois.
   Nenhum deles precisa saber que a recorrencia existe.

   Quem esconde a marca na tela, quem desenha a etiqueta "toda quinta" e
   quem rola a data quando a tarefa e ticada e o painel, aqui.            */
window.REP=(function(){
  var re=/\s*@(semanal|quinzenal|mensal)\b/i;
  var DIAS=['domingo','segunda','terça','quarta','quinta','sexta','sábado'];

  function de(t){var m=(t||'').match(re);return m?m[1].toLowerCase():''}
  function sem(t){return (t||'').replace(re,'').replace(/\s{2,}/g,' ').trim()}
  function com(t,tipo){return sem(t)+' @'+(tipo||'semanal')}

  /* Proxima ocorrencia DEPOIS de hoje, ancorada na data que a tarefa ja
     tem. E a ancora que mantem o dia da semana quando uma volta e pulada:
     somar 7 dias a partir de hoje jogaria a quinta para uma terca.      */
  function proxima(isoData,tipo){
    var p=String(isoData||'').split('-');
    if(p.length!==3)return null;
    var d=new Date(+p[0],+p[1]-1,+p[2]); d.setHours(0,0,0,0);
    if(isNaN(d))return null;
    var h=new Date(); h.setHours(0,0,0,0);
    var passo=function(){
      if(tipo==='mensal')d.setMonth(d.getMonth()+1);
      else d.setDate(d.getDate()+(tipo==='quinzenal'?14:7));
    };
    var giros=0;
    do{ passo() }while(d<=h&&giros++<500);
    return d;
  }

  function rotulo(isoData,tipo){
    if(tipo==='mensal')return 'todo mês';
    var p=String(isoData||'').split('-');
    if(p.length!==3)return tipo==='quinzenal'?'a cada 15 dias':'toda semana';
    var d=new Date(+p[0],+p[1]-1,+p[2]);
    if(isNaN(d))return 'toda semana';
    var g=d.getDay(), nome=DIAS[g], art=(g===0||g===6)?'todo ':'toda ';
    return tipo==='quinzenal'?('a cada 15 dias, '+art+nome):(art+nome);
  }

  /* "toda quinta", "todo domingo", "toda semana", "todo mes" escritos na
     caixa de cadastro. Devolve o tipo e, quando houver, o dia da semana. */
  function doTexto(bruto){
    var m=String(bruto||'').match(
      /\b(toda|todo)s?\s+(?:as\s+|os\s+)?(semanas?|quinzenas?|m[eê]s(?:es)?|segundas?|ter[cç]as?|quartas?|quintas?|sextas?|s[aá]bados?|domingos?)(?:-feiras?)?\b/i);
    if(!m)return null;
    var alvo=m[2].toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    var tipo=alvo.indexOf('quinzena')===0?'quinzenal':
             (alvo.indexOf('mes')===0?'mensal':'semanal');
    var dia=-1;
    ['domingo','segunda','terca','quarta','quinta','sexta','sabado']
      .forEach(function(nm,i){if(alvo.indexOf(nm)===0)dia=i});
    return {tipo:tipo,trecho:m[0],dia:dia};
  }

  return {de:de,sem:sem,com:com,proxima:proxima,rotulo:rotulo,doTexto:doTexto};
})();

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

  /* ------------- reconciliacao das caixinhas com o .md -------------------
     O estado do aparelho mandava sozinho: item marcado no COMPRAS.md abria
     desmarcado em qualquer navegador que ainda nao o tivesse ticado, porque a
     pintura inicial so olhava o localStorage. Marcar no PC do trabalho, deixar
     a Action levar isso para o .md e abrir o painel em casa nao mostrava nada.
     Era o mesmo desenho das tarefas, e as duas pontas foram corrigidas juntas
     (21/08/2026).

     Agora cada <li> carrega `data-md` (o que o arquivo diz do item) e cada aba
     carrega `data-mod` (a hora do commit daquele .md). A decisao usa a mesma
     regra de tres vias das tarefas, com um espelho do que o arquivo dizia na
     ultima abertura:

       arquivo mudou, eu nao   -> vale o arquivo
       eu mudei, o arquivo nao -> vale o meu (marcacao ainda nao exportada)
       os dois mudaram         -> quem mexeu por ultimo (hora do commit contra
                                  o `m` da marcacao guardada aqui)

     Item que este aparelho nunca tocou nao tem o que defender: vale o arquivo.

     Quando o arquivo vence, a marcacao fica com `s:true` e `m` igual a hora do
     commit, entao ela nao volta a subir. Reenviar faria o `mod` da nuvem
     REGREDIR e a rodada seguinte da Action desfaria a mudanca. Quem sobe item
     que a nuvem nunca viu e o sincroniza_ticados.py, do lado do Python.     */
  var K_ESPMK='cao-espelho-mk';
  var mkEspelho={};
  try{mkEspelho=JSON.parse(localStorage.getItem(K_ESPMK)||'{}')||{}}catch(e){mkEspelho={}}

  function mkDoArquivo(li){return parseInt(li.getAttribute('data-md')||'0',10)||0}
  function mkHoraDaAba(sec){
    var m=sec&&sec.getAttribute('data-mod');
    return m?(Date.parse(m)||0):0;
  }

  function mkReconcilia(){
    var foto={}, mudou=false;
    pans.forEach(function(sec){
      var itens=sec.querySelectorAll('ul.tarefas li[data-mk]');
      if(!itens.length)return;
      var tArq=mkHoraDaAba(sec);
      [].forEach.call(itens,function(li){
        var k=mkChave(li), arq=mkDoArquivo(li), atual=mkEstado[k];
        foto[k]=arq;
        if(!atual){
          /* nunca ticado aqui: vale o arquivo. So grava quando ha o que
             guardar, para nao encher o armazenamento de zeros. */
          if(arq>0){
            mkEstado[k]={n:arq,m:new Date(tArq||Date.now()).toISOString(),s:true};
            mudou=true;
          }
          return;
        }
        if((atual.n||0)===arq)return;
        var temBase=Object.prototype.hasOwnProperty.call(mkEspelho,k);
        var venceArquivo;
        if(temBase){
          var base=mkEspelho[k]||0;
          var arqMudou=base!==arq, locMudou=base!==(atual.n||0);
          if(arqMudou&&!locMudou)venceArquivo=true;
          else if(locMudou&&!arqMudou)venceArquivo=false;
          else venceArquivo=tArq>(Date.parse(atual.m||'')||0);
        }else{
          venceArquivo=tArq>(Date.parse(atual.m||'')||0);
        }
        if(!venceArquivo)return;
        mkEstado[k]={n:arq,m:new Date(tArq||Date.now()).toISOString(),s:true};
        mudou=true;
      });
    });
    mkEspelho=foto;
    try{localStorage.setItem(K_ESPMK,JSON.stringify(foto))}catch(e){}
    if(mudou)mkSalva();
  }
  mkReconcilia();

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
    /* a lista de conferencia dentro de uma tarefa (aba Tarefas) guarda o
       tique aqui tambem, com chave 'tf/...', mas quem a desenha e o app de
       tarefas. Sem este aviso, o item marcado no celular so apareceria no PC
       depois de recarregar a pagina. */
    if(window.TAREFAS&&TAREFAS.redesenhar)TAREFAS.redesenhar();
  }
  /* estado da sincronizacao mostrado na barra de cada aba de lista.
     Quem chama e o bloco do Supabase; sem ele fica no texto inicial.       */
  /* A linha de estado da aba TAREFAS entra aqui junto com as das listas.
     Parece detalhe e nao e: desde 23/08/2026 uma tarefa pode ter lista de
     conferencia por dentro, e o tique de cada item e guardado como caixinha
     (cao_ticados), mas o clique acontece na aba Tarefas - que so ouvia o
     estado das TAREFAS. Ticar os 15 itens da mala e desligar o PC nao dava
     nenhuma confirmacao na tela de que aquilo tinha subido. Agora da.

     Como os dois canais escrevem na mesma linha, eles falam a mesma lingua:
     "Salvando...", "Salvo na nuvem", "Sem conexao". Ter dois nomes para o
     mesmo estado ("Sincronizado" de um lado, "Salvo na nuvem" do outro) so
     faria a linha trocar de palavra sozinha na frente de quem le.          */
  function mkEstadoSinc(cls,txt,tit){
    var alvos=[].slice.call(document.querySelectorAll('.mk-sinc'));
    var tf=document.getElementById('tf-status');
    if(tf)alvos.push(tf);
    alvos.forEach(function(s){
      /* cada linha guarda a propria classe base: a da aba Tarefas nao e
         .mk-sinc, e marca-la mudaria a fonte pelo CSS das listas */
      s.className=(s.id==='tf-status'?'tf-status':'tf-status mk-sinc')+(cls?' '+cls:'');
      var t=s.querySelector('.txt')||s.querySelector('#tf-status-txt');
      if(t)t.textContent=txt;
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
    /* secoes recolhidas voltam a ficar fechadas quando a busca sai da tela */
    document.querySelectorAll('details.extra').forEach(function(d){d.open=false});
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
          /* o titulo de uma secao recolhida nunca some: sem ele o <details>
             fica sem cabecalho e o resultado dentro dele vira bloco orfao */
          if(el.tagName!=='SUMMARY')el.style.display=bate?'':'none';
          if(bate){realca(el,termo);n++;}
        });
        /* resultado dentro de secao recolhida so aparece se ela abrir */
        pan.querySelectorAll('details.extra').forEach(function(d){
          d.open=[].slice.call(d.querySelectorAll('[data-b]')).some(function(e){
            return e.tagName!=='SUMMARY'&&e.style.display!=='none'})
            ||d.querySelector('summary').textContent.toLowerCase().indexOf(alvo)>=0;
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
    var txt=window.REP?REP.sem(t.txt):t.txt;
    return '<li><span class="pt"'+(cor?' style="background:'+cor+'"':'')+'></span>'+
           '<span>'+esc(txt)+'</span>'+quando+'</li>';
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
      /* cada aba pode dar o proprio rotulo (data-sub-falta / data-sub-ok);
         sem isso vale o texto generico de lista a zerar */
      var rf=k.getAttribute('data-sub-falta'), ro=k.getAttribute('data-sub-ok');
      k.querySelector('.sub').textContent=falta?
        (rf||(falta===1?'item ainda falta':'itens ainda faltam')):
        (ro||('tudo marcado, '+total+' itens'));
      k.querySelector('.barra i').style.width=pct+'%';
      k.classList.toggle('dest',falta>0&&k.getAttribute('data-aba')==='ab-compras');
    });
  }

  /* ---- as aulas de hoje, vindas do QTS ----
     O dado sai do GRADE.md na geracao (extrai_qts) e chega aqui como
     window.QTS. A conta de "que dia e hoje" e "que bloco esta correndo
     agora" e feita no navegador, pelo mesmo motivo do resto deste
     arquivo: o painel publicado so e regerado quando um .md muda, entao
     qualquer hora calculada na geracao ja nasce velha.

     Tres situacoes diferentes, que nao podem virar a mesma frase:
       - dia com blocos      -> a lista
       - dia declarado vazio -> "hoje nao tem aula", que e uma informacao
       - dia ausente         -> "o QTS ainda nao entrou aqui", que e o
                                painel admitindo que nao sabe            */
  var Q=window.QTS||{dias:{}};

  function chave(d){return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+
                           '-'+('0'+d.getDate()).slice(-2);}
  function min(hm){var p=String(hm).split(':');return (+p[0])*60+(+p[1]);}
  function hhmm(hm){return String(hm).replace(':','h');}
  function falta(m){
    if(m<60)return 'em '+m+' min';
    var h=Math.floor(m/60), r=m%60;
    return 'em '+h+'h'+(r?('0'+r).slice(-2):'');
  }

  /* proximo dia com aula a partir de uma data (exclusive) */
  function proximo(depois){
    var ks=Object.keys(Q.dias||{}).sort(), i;
    for(i=0;i<ks.length;i++){
      if(ks[i]>depois && Q.dias[ks[i]].blocos && Q.dias[ks[i]].blocos.length)
        return ks[i];
    }
    return null;
  }

  function rotuloDia(k){
    var d=dt(k);
    return SEM[d.getDay()]+' '+curto(d);
  }

  function listaBlocos(bl,agoraMin){
    return '<ul class="qts-lista">'+bl.map(function(b,i){
      var cls='',qd='';
      if(agoraMin!==null){
        if(agoraMin>=min(b.fim))cls='passou';
        else if(agoraMin>=min(b.ini)){cls='agora';qd='agora';}
        else{
          /* o proximo e o primeiro que ainda nao comecou */
          var eh=true,j;
          for(j=0;j<i;j++)if(agoraMin<min(bl[j].ini))eh=false;
          if(eh){cls='prox';qd=falta(min(b.ini)-agoraMin);}
        }
      }
      return '<li class="'+cls+'"><span class="hr">'+hhmm(b.ini)+
             '<i>'+hhmm(b.fim)+'</i></span><span class="ds"><b>'+esc(b.disc)+
             '</b><i>'+esc(b.doc)+'</i></span>'+
             (qd?'<span class="qd">'+qd+'</span>':'')+'</li>';
    }).join('')+'</ul>';
  }

  function aulas(){
    var alvo=el('#guia-aula');
    if(!alvo)return;
    var ag=new Date(), h=hoje(), k=chave(h), dia=(Q.dias||{})[k];
    var agoraMin=ag.getHours()*60+ag.getMinutes();
    var out='';

    if(dia&&dia.blocos&&dia.blocos.length){
      var acabou=agoraMin>=min(dia.blocos[dia.blocos.length-1].fim);
      out+='<div class="guia-cab">'+(acabou?'Hoje, já encerrado':'Hoje no CAES')+
           '<span class="n">'+dia.blocos.length+'</span></div>';
      if(dia.aviso)
        out+='<div class="qts-aviso"><b>Atenção</b><span>'+esc(dia.aviso)+'</span></div>';
      out+=listaBlocos(dia.blocos,agoraMin);
      if(acabou){
        var p1=proximo(k);
        out+='<p class="guia-nota">'+(p1?
          'Próxima aula na '+rotuloDia(p1)+', '+hhmm(Q.dias[p1].blocos[0].ini)+
          ', '+esc(Q.dias[p1].blocos[0].disc)+'.':
          'O QTS não tem mais nenhum dia depois de hoje. Quando o próximo chegar, ele entra na aba Grade.')+'</p>';
      }
    }else if(dia){
      out+='<div class="guia-cab">Hoje no CAES</div>'+
           '<div class="guia-tudoem">'+(window.ICO&&ICO.check?ICO.check:'')+
           'Hoje não tem aula no QTS.</div>';
      var p2=proximo(k);
      out+='<p class="guia-nota">'+(p2?
        'Próxima aula na '+rotuloDia(p2)+', '+hhmm(Q.dias[p2].blocos[0].ini)+', '+
        esc(Q.dias[p2].blocos[0].disc)+'.':
        'O QTS da semana que vem ainda não entrou. Ele é lançado na aba <a href="#grade" class="lnk-aba">Grade</a>.')+'</p>';
    }else{
      var p3=proximo(k), ks=Object.keys(Q.dias||{}).sort();
      out+='<div class="guia-cab">Hoje no CAES</div>';
      if(p3){
        out+='<p class="guia-nota">O QTS não tem nada marcado para hoje. A próxima aula é na '+
             rotuloDia(p3)+', '+hhmm(Q.dias[p3].blocos[0].ini)+', '+
             esc(Q.dias[p3].blocos[0].disc)+'.</p>';
      }else{
        out+='<p class="guia-nota"><b>O QTS desta semana ainda não entrou no painel.</b> '+
             (ks.length?'O último que entrou foi o de '+curto(dt(ks[0]))+' a '+
              curto(dt(ks[ks.length-1]))+'. ':'')+
             'Assim que o novo chegar, ele é lançado na aba <a href="#grade" class="lnk-aba">Grade</a> e este cartão volta sozinho.</p>';
      }
    }
    alvo.innerHTML=out;
  }

  /* marco fica exposto para conferir o texto de cada dia da semana sem
     precisar esperar o dia chegar: GUIA.marco(new Date(2026,7,19))       */
  window.GUIA={topo:topo,tarefas:tarefas,listas:listas,marco:marco,aulas:aulas};
  topo();listas();aulas();
  /* vira o dia com o painel aberto (celular que fica na tela): refaz o topo */
  setInterval(topo,10*60*1000);
  /* o cartao de aula marca "agora" e "em 25 min", entao acompanha o relogio
     de perto: de 10 em 10 minutos a aula ja teria trocado sem o painel notar */
  setInterval(aulas,60*1000);
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
  <div class="tf-status" id="tf-status" title="Estado da sincronização">
    <span class="bola"></span><span id="tf-status-txt">Somente neste aparelho</span>
  </div>
</div>

<div class="tf-nova">
  <div class="tf-linha">
    <input type="text" id="tf-txt" placeholder="O que precisa ser feito? Ex.: entregar artigo sexta, ou toda quinta separar a roupa"
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

""" % {
        "cats": chips_cat,
        "mais": svg("mais", 19),
        "baixar": svg("baixar", 15),
        "fechar": svg("fechar", 16),
        "copiar": svg("copiar", 15),
        "users": svg("users", 15),
    }


def modal_conta():
    """HTML do login. Fica FORA das abas, no corpo da pagina.

    Ate 21/08/2026 ele era gerado dentro da secao da aba Tarefas, que e
    `display:none` em qualquer outra aba. Ou seja, entrar na conta so era
    possivel estando em Tarefas - e a sincronizacao vale para o painel inteiro,
    inclusive as caixinhas de Compras, Mala e Rotina. Era resto de quando so as
    tarefas subiam para a nuvem, nao uma decisao.
    """
    return """
<div class="modal" id="modal-conta">
  <div class="modal-cx">
    <div class="modal-cab">%(users)s<h3 id="conta-titulo">Entrar na conta</h3>
      <button class="tf-ac" data-fechar="modal-conta">%(fechar)s</button></div>
    <div class="modal-corpo">
      <div class="modal-erro" id="conta-erro"></div>
      <div id="conta-form">
        <div class="aviso-cx" id="conta-aviso">
          Entrando, este aparelho passa a sincronizar com os outros: as tarefas e também
          as marcações das listas (Compras, Mala, Rotina). Sem entrar, tudo continua
          salvo só neste navegador.
        </div>
        <label for="conta-email">E-mail</label>
        <input type="email" id="conta-email" autocomplete="username" placeholder="seu@email.com">
        <label for="conta-senha">Senha</label>
        <input type="password" id="conta-senha" autocomplete="current-password" placeholder="••••••••">
      </div>
      <div id="conta-logado" style="display:none">
        <p>Conectado como <b id="conta-quem"></b>. Tarefas e marcações estão sincronizando.</p>
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
        "fechar": svg("fechar", 16),
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

    # Hora do ultimo commit de cada .md, por aba. Vai embutida no painel e e o
    # que permite ao navegador decidir, item a item, se quem esta mais novo e o
    # arquivo do repositorio ou a marcacao guardada naquele aparelho.
    arq_mod = {"ab-" + aba_id: hora_do_md(arq) for arq, aba_id, _, _ in ABAS}

    # Nada no painel gerado pode depender da data de hoje. O rodape mostrava a
    # data da geracao, e isso fazia a Action (que roda em UTC) e o PC (UTC-3)
    # produzirem arquivos diferentes perto da meia-noite, alem de reintroduzir
    # o conflito a cada virada de dia. Toda conta de tempo e feita no navegador.
    pend, feito = conta_tarefas(docs.get("TAREFAS.md", ""))
    qts = extrai_qts(docs.get("GRADE.md", ""))

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
            '<div class="guia-aula" id="guia-aula"></div>'
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
    # O cartao da Mala nao conta "item de lista": conta PECA DE ROUPA que falta
    # no armario, que e a mala de domingo. Por isso ele tem rotulo proprio: dizer
    # "12 itens ainda faltam" para uma lista de rodizio semanal soa a pendencia
    # atrasada, quando e so a carga da proxima viagem.
    home.append('<div class="kpi lista-kpi" data-aba="ab-mala" data-rot="Mala"'
                ' data-sub-falta="peças na mala de domingo"'
                ' data-sub-ok="armário completo">'
                '<div class="rot">Mala</div><div class="val">...</div>'
                '<div class="sub">peças na mala de domingo</div>'
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
        # data-mod: quando este .md mudou pela ultima vez. A reconciliacao das
        # caixinhas compara essa hora com a hora da marcacao guardada no
        # aparelho para saber quem mexeu por ultimo.
        paineis.append('<section class="aba" id="ab-%s" role="tabpanel" data-mod="%s">%s'
                       '<div class="card">%s</div></section>'
                       % (aba_id, arq_mod.get("ab-" + aba_id, ""), extra, corpo))

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
        <!-- A conta vive no cabecalho porque a sincronizacao vale para o painel
             inteiro, nao so para a aba Tarefas, que era onde ela ficava. -->
        <button class="bt" id="topo-conta" title="Sincronizar entre aparelhos">
          %(users)s <span id="tf-conta-rot">Entrar</span></button>
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
%(modalconta)s
<script>
var SOL=%(sol)r,LUA=%(lua)r;
var CATEGORIAS=%(cats)s;
var BASE=%(base)s;
var TAR_CAB=%(tarcab)s;
var TAR_NOTAS=%(tarnotas)s;
var ICO=%(ico)s;
window.CURSO=%(curso)s;
window.QTS=%(qts)s;
window.SUPA_CFG=%(supa)s;
window.ARQ_MOD=%(arqmod)s;
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
        "qts": escapa_js(qts),
        "js_supabase": JS_SUPABASE,
        "nav": "".join(nav),
        "paineis": "\n".join(paineis),
        "icbusca": svg("search", 16),
        "users": svg("users", 15),
        "modalconta": modal_conta(),
        "sol": svg("sun", 17),
        "lua": svg("moon", 17),
        "carimbo": CARIMBO_VAGA,
        "cats": escapa_js([[c[0], c[1], c[2]] for c in CATEGORIAS]),
        "base": escapa_js(extrai_tarefas(docs.get("TAREFAS.md", ""))),
        "tarcab": escapa_js(extrai_cabecalho(docs.get("TAREFAS.md", ""))),
        "tarnotas": escapa_js(extrai_notas(docs.get("TAREFAS.md", ""))),
        "supa": escapa_js(le_config_supabase()),
        "arqmod": escapa_js(arq_mod),
        "ico": escapa_js({
            "check": svg("check", 13),
            "lapis": svg("lapis", 15),
            "lixo": svg("lixo", 15),
            "cal": svg("calendar", 12),
            "calbt": svg("calendar", 15),
            "vazio": svg("vazio", 46),
            "copiar": svg("copiar", 15),
            "repete": svg("repete", 12),
            "lista": svg("lista", 12),
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
