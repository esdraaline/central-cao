#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador dos mapas de trajeto a pe da aba Entorno.

Desenha um .svg por destino, tracado sobre a malha viaria real do
OpenStreetMap, com a rota calculada por roteador de pedestre. Os .svg
ficam nesta pasta e o gerar_painel.py os embute no painel.

Uso:
    python mapas/gerar_mapas.py            # so o que faltar
    python mapas/gerar_mapas.py --refazer  # rebaixa tudo e redesenha

Por que nao print do Google Maps: licenca, e principalmente porque nao
abre sem rede, que e quando ele mais precisa do mapa na calcada. Desenho
proprio abre offline e acompanha o tema claro/escuro do painel.

Duas armadilhas ja pagas, nao troque de servico sem reler isto:

1. O servidor publico do OSRM roteia como CARRO mesmo no perfil "foot".
   Dava 1.080 m em 2 min (32 km/h) e mandava 1.880 m ate a Santa Cecilia
   porque respeitava mao unica. Por isso aqui e Valhalla, com
   costing=pedestrian.
2. O Nominatim sem viewbox geocodificou "Rua 25 de Marco" em Santa
   Catarina, a 143 km. Por isso toda busca vai presa na CAIXA_SP.

Atencao: o feira-de-trem.svg desta pasta NAO sai daqui. Ele e desenhado a
mao, porque mostra baldeacao de trem e nao caminhada. Se mudar horario ou
estacao, edite aquele arquivo direto.

Sem dependencias externas. Python 3.8+. Precisa de internet.
"""

import io
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(AQUI, ".cache")
UA = {"User-Agent": "central-cao-guia/1.0 (uso pessoal, mapas do guia do CAO)"}

# Saida do CAES, confirmada no local em 17/08/2026:
# Praca Julio Prestes, 142, Campos Eliseos, CEP 01218-020.
ORIGEM = (-23.53437, -46.64168)

# Prende a geocodificacao no centro de Sao Paulo (ver armadilha 2).
CAIXA_SP = "-46.70,-23.50,-46.56,-23.58"

ESPELHOS_OVERPASS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# (arquivo, rotulo no mapa, texto da busca, grupo de malha, titulo)
DESTINOS = [
    ("estacao-da-luz", "Luz", "Estação da Luz, Luz, São Paulo",
     "perto", "Do CAES até a Estação da Luz"),
    ("santa-ifigenia", "Santa Ifigênia", "Rua Santa Ifigênia, 300, São Paulo",
     "perto", "Do CAES até a Rua Santa Ifigênia"),
    ("santa-cecilia", "Santa Cecília", "Estação Santa Cecília, São Paulo",
     "perto", "Do CAES até a Estação Santa Cecília"),
    ("ccb-bom-retiro", "CCB Bom Retiro", "Rua Anhaia, 613, Bom Retiro, São Paulo",
     "perto", "Do CAES até a CCB do Bom Retiro"),
    ("25-de-marco", "25 de Março", "Rua 25 de Março, Sé, São Paulo",
     "marco", "Do CAES até a 25 de Março"),
    ("feira-madrugada", "Feira", "Rua Oriente, 500, Brás, São Paulo",
     "feira", "Do CAES até a Feira da Madrugada"),
]

# Caixa pequena leva rua residencial; as grandes so via principal, senao a
# consulta estoura no Overpass e o desenho fica ilegivel de tanta linha.
GRUPOS = {
    "perto": ("motorway|trunk|primary|secondary|tertiary|residential|unclassified|"
              "living_street|pedestrian"),
    "marco": "motorway|trunk|primary|secondary|tertiary|residential|pedestrian",
    "feira": "motorway|trunk|primary|secondary|tertiary",
}

L, A = 640.0, 470.0          # tela do svg
MARGEM = 26.0
ESPESSURA = {"motorway": 4.4, "trunk": 4.0, "primary": 3.6, "secondary": 3.0,
             "tertiary": 2.4, "residential": 1.5, "unclassified": 1.4,
             "living_street": 1.2, "pedestrian": 1.2}
GRANDES = {"motorway", "trunk", "primary", "secondary"}

ESTILO = """<style>
  .fundo{fill:var(--card)}
  .via{fill:none;stroke:var(--tx3);opacity:.30;stroke-linecap:round;stroke-linejoin:round}
  .viaf{fill:none;stroke:var(--tx3);opacity:.45;stroke-linecap:round}
  .capa{fill:none;stroke:var(--card);stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
  .rota{fill:none;stroke:var(--vm-cl);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
  .tit{fill:var(--tx);font:700 15px system-ui,sans-serif}
  .sub{fill:var(--tx2);font:12.5px system-ui,sans-serif}
  .rot{fill:var(--tx2);font:600 10.5px system-ui,sans-serif}
  .esc{fill:var(--tx3);font:10.5px system-ui,sans-serif}
  .pin{fill:var(--vm-cl);stroke:var(--card);stroke-width:2.5}
  .pin2{fill:var(--card);stroke:var(--vm-cl);stroke-width:3.5}
  .marc{fill:var(--tx);font:700 11.5px system-ui,sans-serif}
</style>"""


# ------------------------------------------------------------------ rede

def _busca(url, tempo=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=tempo) as r:
        return json.load(r)


def geocodifica(consulta):
    """Nominatim, preso a CAIXA_SP para nao cair em outra cidade."""
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": consulta, "format": "json", "limit": 1,
        "viewbox": CAIXA_SP, "bounded": 1})
    d = _busca(url, 40)
    if not d:
        raise RuntimeError("nao geocodificou: %s" % consulta)
    return float(d[0]["lat"]), float(d[0]["lon"]), d[0]["display_name"][:60]


def _decodifica(s, precisao=1e6):
    """Polyline codificada do Valhalla (precisao 6)."""
    pontos, i, lat, lon = [], 0, 0, 0
    while i < len(s):
        for alvo in range(2):
            shift = resultado = 0
            while True:
                b = ord(s[i]) - 63
                i += 1
                resultado |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(resultado >> 1) if resultado & 1 else (resultado >> 1)
            if alvo == 0:
                lat += delta
            else:
                lon += delta
        pontos.append([lon / precisao, lat / precisao])
    return pontos


def rota_a_pe(a, b):
    """Valhalla com costing=pedestrian (ver armadilha 1 no cabecalho)."""
    q = {"locations": [{"lat": a[0], "lon": a[1]}, {"lat": b[0], "lon": b[1]}],
         "costing": "pedestrian",
         "directions_options": {"units": "kilometers", "language": "pt-BR"}}
    url = "https://valhalla1.openstreetmap.de/route?json=" + urllib.parse.quote(json.dumps(q))
    d = _busca(url, 60)
    perna = d["trip"]["legs"][0]
    passos = []
    for m in perna["maneuvers"]:
        nomes = m.get("street_names") or []
        passos.append({"rua": nomes[0] if nomes else "",
                       "m": round(m.get("length", 0) * 1000)})
    return {"m": round(d["trip"]["summary"]["length"] * 1000),
            "min": round(d["trip"]["summary"]["time"] / 60),
            "geo": _decodifica(perna["shape"]),
            "passos": passos}


def malha(caixa, tipos):
    """Ruas do OpenStreetMap na caixa, via Overpass, com espelhos."""
    s, w, n, e = caixa
    q = ('[out:json][timeout:120];way["highway"~"^(%s)$"](%f,%f,%f,%f);out geom;'
         % (tipos, s, w, n, e))
    for _ in range(2):
        for espelho in ESPELHOS_OVERPASS:
            try:
                d = _busca(espelho + "?data=" + urllib.parse.quote(q), 180)
                vias = []
                for el in d.get("elements", []):
                    g = el.get("geometry")
                    if g and len(g) >= 2:
                        vias.append({"nome": el.get("tags", {}).get("name", ""),
                                     "tipo": el.get("tags", {}).get("highway", ""),
                                     "pts": [[p["lon"], p["lat"]] for p in g]})
                return vias
            except Exception as erro:
                print("     espelho falhou: %s" % str(erro)[:50])
                time.sleep(4)
    raise RuntimeError("Overpass nao respondeu em nenhum espelho")


# --------------------------------------------------------------- desenho

def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _curto(nome):
    for longo, breve in (("Avenida ", "Av. "), ("Alameda ", "Al. "),
                         ("Rua ", "R. "), ("Viaduto ", "Vd. ")):
        nome = nome.replace(longo, breve)
    return nome


def _caixa_da_rota(geo, folga=0.0007):
    lats = [p[1] for p in geo]
    lons = [p[0] for p in geo]
    s, n = min(lats) - folga, max(lats) + folga
    w, e = min(lons) - folga, max(lons) + folga
    # ajusta a proporcao para o mapa nao sair espremido na tela
    kx = math.cos(math.radians((s + n) / 2.0))
    alvo = (L - 2 * MARGEM) / (A - 2 * MARGEM - 34)
    larg, alt = (e - w) * kx, (n - s)
    if larg / alt < alvo:
        falta = (alt * alvo - larg) / kx / 2.0
        w, e = w - falta, e + falta
    else:
        falta = (larg / alvo - alt) / 2.0
        s, n = s - falta, n + falta
    return (s, w, n, e)


def _projetor(caixa):
    s, w, n, e = caixa
    kx = math.cos(math.radians((s + n) / 2.0))
    larg, alt = (e - w) * kx, (n - s)
    k = min((L - 2 * MARGEM) / larg, (A - 2 * MARGEM - 34) / alt)
    dx = (L - larg * k) / 2.0
    dy = (A - 34 - alt * k) / 2.0 + 34
    return (lambda lon, lat: ((lon - w) * kx * k + dx, (n - lat) * k + dy)), k


def _dentro(pts, caixa):
    s, w, n, e = caixa
    return any(w <= p[0] <= e and s <= p[1] <= n for p in pts)


def _traco(pts, proj):
    return " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % proj(p[0], p[1])
                    for i, p in enumerate(pts))


def desenha(arquivo, rotulo, titulo, rota, vias):
    cx = _caixa_da_rota(rota["geo"])
    proj, k = _projetor(cx)
    em_vista = [v for v in vias if _dentro(v["pts"], cx)]

    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (L, A, _esc(titulo)),
           ESTILO,
           '<rect class="fundo" x="0" y="0" width="%d" height="%d"/>' % (L, A)]

    for v in em_vista:
        out.append('<path class="%s" d="%s" stroke-width="%.1f"/>'
                   % ("viaf" if v["tipo"] in GRANDES else "via",
                      _traco(v["pts"], proj), ESPESSURA.get(v["tipo"], 1.3)))

    d = _traco(rota["geo"], proj)
    out.append('<path class="capa" d="%s"/>' % d)
    out.append('<path class="rota" d="%s"/>' % d)

    # rotulo de rua: primeiro as do trajeto, depois as maiores em volta
    usadas, postos = set(), []

    def rotula(nome, via, classe):
        mp = via["pts"][len(via["pts"]) // 2]
        x, y = proj(mp[0], mp[1])
        if not (MARGEM < x < L - MARGEM and 46 < y < A - 34):
            return
        if any(abs(x - ax) < 92 and abs(y - ay) < 16 for ax, ay in postos):
            return
        postos.append((x, y))
        out.append('<text class="%s" x="%.0f" y="%.0f" text-anchor="middle" '
                   'paint-order="stroke" stroke="var(--card)" stroke-width="3.5">%s</text>'
                   % (classe, x, y - 4, _esc(_curto(nome))))

    for p in rota["passos"]:
        nome = p["rua"]
        if not nome or p["m"] < 90 or nome in usadas:
            continue
        iguais = [v for v in em_vista if v["nome"] == nome]
        if iguais:
            usadas.add(nome)
            rotula(nome, max(iguais, key=lambda v: len(v["pts"])), "rot")

    candidatas = {}
    for v in em_vista:
        nome = v["nome"]
        if not nome or nome in usadas:
            continue
        comp = sum(abs(v["pts"][i][0] - v["pts"][i - 1][0])
                   + abs(v["pts"][i][1] - v["pts"][i - 1][1])
                   for i in range(1, len(v["pts"])))
        if comp > candidatas.get(nome, (0, None))[0]:
            candidatas[nome] = (comp, v)
    for nome, (_, v) in sorted(candidatas.items(), key=lambda kv: -kv[1][0])[:14]:
        if len(postos) >= 11:
            break
        rotula(nome, v, "esc")

    ox, oy = proj(ORIGEM[1], ORIGEM[0])
    dx_, dy_ = proj(rota["lon"], rota["lat"])
    out.append('<circle class="pin" cx="%.0f" cy="%.0f" r="8"/>' % (ox, oy))
    out.append('<circle class="pin2" cx="%.0f" cy="%.0f" r="8"/>' % (dx_, dy_))
    for x, y, texto in ((ox, oy, "CAES"), (dx_, dy_, rotulo)):
        anc = "start" if x < L / 2 else "end"
        out.append('<text class="marc" x="%.0f" y="%.0f" text-anchor="%s" '
                   'paint-order="stroke" stroke="var(--card)" stroke-width="4">%s</text>'
                   % (x + (12 if anc == "start" else -12), y + 4, anc, _esc(texto)))

    metros = rota["m"]
    txt = "%d" % metros if metros < 1000 else "%d.%03d" % (metros // 1000, metros % 1000)
    out.append('<text class="tit" x="16" y="22">%s</text>' % _esc(titulo))
    out.append('<text class="sub" x="16" y="40">%s m a pé, cerca de %d min</text>'
               % (txt, rota["min"]))

    barra = 200 if metros < 1500 else 500
    px = barra / 111320.0 * k
    bx, by = L - MARGEM - px, A - 16
    out.append('<path d="M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f" '
               'stroke="var(--tx3)" stroke-width="2" fill="none"/>'
               % (bx, by, bx + px, by, bx, by - 4, bx, by + 4,
                  bx + px, by - 4, bx + px, by + 4))
    out.append('<text class="esc" x="%.1f" y="%.1f" text-anchor="middle">%d m</text>'
               % (bx + px / 2, by - 8, barra))
    out.append('<text class="esc" x="16" y="%d">Dados: OpenStreetMap · rota a pé Valhalla</text>'
               % (A - 12))
    out.append("</svg>")

    io.open(os.path.join(AQUI, arquivo + ".svg"), "w", encoding="utf-8").write("\n".join(out))


# ------------------------------------------------------------------ fluxo

def cache_le(nome):
    p = os.path.join(CACHE, nome)
    return json.load(io.open(p, encoding="utf-8")) if os.path.isfile(p) else None


def cache_grava(nome, dado):
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    io.open(os.path.join(CACHE, nome), "w", encoding="utf-8").write(
        json.dumps(dado, ensure_ascii=False))


def main():
    refazer = "--refazer" in sys.argv

    rotas = None if refazer else cache_le("rotas.json")
    if rotas is None:
        rotas = {}
        for arq, _rot, consulta, _g, _t in DESTINOS:
            lat, lon, achou = geocodifica(consulta)
            time.sleep(1.2)                      # Nominatim pede 1 req/s
            r = rota_a_pe(ORIGEM, (lat, lon))
            r.update({"lat": lat, "lon": lon, "achou": achou})
            rotas[arq] = r
            print("  rota  %-16s %5d m  %2d min  |  %s" % (arq, r["m"], r["min"], achou[:38]))
            time.sleep(0.8)
        cache_grava("rotas.json", rotas)

    malhas = {}
    for grupo, tipos in GRUPOS.items():
        nome = "vias_%s.json" % grupo
        v = None if refazer else cache_le(nome)
        if v is None:
            lats = [ORIGEM[0]]
            lons = [ORIGEM[1]]
            for arq, _r, _c, g, _t in DESTINOS:
                if g != grupo:
                    continue
                for lon, lat in rotas[arq]["geo"]:
                    lats.append(lat)
                    lons.append(lon)
            caixa = (min(lats) - 0.0016, min(lons) - 0.0016,
                     max(lats) + 0.0016, max(lons) + 0.0016)
            v = malha(caixa, tipos)
            cache_grava(nome, v)
            print("  malha %-16s %4d vias" % (grupo, len(v)))
            time.sleep(3)
        malhas[grupo] = v

    for arq, rotulo, _c, grupo, titulo in DESTINOS:
        desenha(arq, rotulo, titulo, rotas[arq], malhas[grupo])
        print("  mapa  %s.svg" % arq)

    print("\n%d mapas em %s" % (len(DESTINOS), AQUI))
    print("Agora rode: python gerar_painel.py")


if __name__ == "__main__":
    main()
