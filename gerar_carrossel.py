# -*- coding: utf-8 -*-
"""Gera o carrossel TÉCNICO do @perffecesquadrias — 1080x1350 (4:5), 7 a 9 slides.

Herda do carrossel de mini-aula do @vendanaobra o que foi MEDIDO lá (agosto/2026):
  - 4:5 e não 1:1 — ocupa mais tela no feed do celular;
  - 7 slides é o ponto ótimo; 10 derruba a taxa de conclusão;
  - capa com FOTO e gancho de 4 a 8 palavras; uma ideia por slide dali em diante;
  - último slide pede a ação (salvar / mandar para o arquiteto).

O que é da Perffec e não do @vendanaobra:
  - identidade: preto #141414 + verde #3E7459 + branco, Archivo em tudo (a LP e o
    e-book "Compare com critério" usam exatamente esta paleta);
  - a foto da capa é OBRA DA PERFFEC (pasta fotos/, vindas da LP), nunca banco;
  - blocos herdados do e-book: "Tradução", "Sinal de alerta" e "Na Perffec".

Tipos de slide (campo "tipo" em carrosseis.json):
  capa      foto + etiqueta + gancho
  texto     título + parágrafos (padrão)
  lista     título + itens [rótulo, texto]
  traducao  fundo verde-claro, rótulo TRADUÇÃO — a frase que resume
  alerta    rótulo vermelho SINAL DE ALERTA
  perffec   fundo preto, rótulo NA PERFFEC — o fato verificável
  cta       fundo preto, pede salvar/compartilhar + contato
"""
from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONTE_TTF = os.path.join(BASE, "fontes", "Archivo.ttf")
LOGO_BRANCO = os.path.join(BASE, "logo-branco.png")
PASTA_FOTOS = os.path.join(BASE, "fotos")

LARG, ALT = 1080, 1350
MARGEM = 96
UTIL = LARG - 2 * MARGEM

ESCURO = (20, 20, 20)          # #141414
VERDE = (62, 116, 89)          # #3E7459
VERDE_ESCURO = (47, 90, 69)    # #2F5A45
VERDE_FUNDO = (233, 242, 236)  # #E9F2EC
BRANCO = (250, 250, 250)
TINTA = (20, 20, 20)
TINTA2 = (58, 58, 58)
CINZA = (128, 128, 128)
LINHA = (214, 214, 214)
ALERTA = (158, 52, 23)         # #9E3417
ALERTA_FUNDO = (250, 238, 233)

HANDLE = "@perffecesquadrias"
SITE = "perffec.com.br"
WHATS = "(19) 97122-7795"


def _f(tamanho: int, peso: int = 400, largura: int = 100) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONTE_TTF, tamanho)
    # Archivo variável: eixos wght (100..900) e wdth (62..125)
    f.set_variation_by_axes([max(100, min(900, peso)), max(62, min(125, largura))])
    return f


def _quebrar(texto: str, fonte, largura: int) -> list[str]:
    linhas: list[str] = []
    for par in texto.split("\n"):
        atual = ""
        for palavra in par.split():
            teste = (atual + " " + palavra).strip()
            if fonte.getlength(teste) <= largura:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def _altura(texto: str, fonte, largura: int, entrelinha: float, gap_par: float) -> int:
    lh = int(fonte.size * entrelinha)
    pars = [p.strip() for p in texto.split("\n\n") if p.strip()]
    total = 0
    for i, p in enumerate(pars):
        total += len(_quebrar(p, fonte, largura)) * lh
        if i < len(pars) - 1:
            total += int(fonte.size * gap_par)
    return total


def _bloco(d, texto: str, x: int, y: int, largura: int, fonte, cor,
           entrelinha: float = 1.4, gap_par: float = 0.7) -> int:
    lh = int(fonte.size * entrelinha)
    pars = [p.strip() for p in texto.split("\n\n") if p.strip()]
    for i, p in enumerate(pars):
        for linha in _quebrar(p, fonte, largura):
            d.text((x, y), linha, font=fonte, fill=cor)
            y += lh
        if i < len(pars) - 1:
            y += int(fonte.size * gap_par)
    return y


def _espacado(d, texto: str, x: int, y: int, fonte, cor, tracking: int = 4) -> int:
    for ch in texto:
        d.text((x, y), ch, font=fonte, fill=cor)
        x += int(fonte.getlength(ch)) + tracking
    return x


def _cobrir(foto: Image.Image, larg: int, alt: int) -> Image.Image:
    esc = max(larg / foto.width, alt / foto.height)
    novo = foto.resize((int(foto.width * esc) + 1, int(foto.height * esc) + 1), Image.LANCZOS)
    x = (novo.width - larg) // 2
    y = (novo.height - alt) // 2
    return novo.crop((x, y, x + larg, y + alt))


def _logo(im: Image.Image, x: int, y: int, largura: int = 250) -> None:
    logo = Image.open(LOGO_BRANCO).convert("RGBA")
    esc = largura / logo.width
    logo = logo.resize((largura, int(logo.height * esc)), Image.LANCZOS)
    im.alpha_composite(logo, (x, y - logo.height))


def _rodape(d, cor=CINZA) -> None:
    f = _f(26, 500)
    d.text((MARGEM, ALT - 92), HANDLE, font=f, fill=cor)
    d.text((LARG - MARGEM - f.getlength(SITE), ALT - 92), SITE, font=f, fill=cor)


def _cabecalho(d, n: int, total: int, rotulo: str | None, cor_rotulo, cor_num=VERDE) -> int:
    """Número do slide + rótulo opcional. Devolve o y onde o conteúdo começa."""
    f = _f(28, 600)
    d.text((MARGEM, 96), f"{n:02d} / {total:02d}", font=f, fill=cor_num)
    d.rectangle((MARGEM, 146, MARGEM + 72, 150), fill=cor_num)
    y = 196
    if rotulo:
        _espacado(d, rotulo.upper(), MARGEM, y, _f(26, 700), cor_rotulo, tracking=5)
        y += 62
    return y


# ------------------------------------------------------------------ slides

def slide_capa(s: dict, total: int) -> Image.Image:
    foto = Image.open(os.path.join(PASTA_FOTOS, s["foto"])).convert("RGB")
    im = _cobrir(foto, LARG, ALT).convert("RGBA")
    # escurecimento: leve em cima, pesado embaixo (onde vai o gancho)
    veu = Image.new("RGBA", (LARG, ALT), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veu)
    for y in range(ALT):
        t = y / ALT
        a = int(70 + 150 * (t ** 1.6))
        vd.line((0, y, LARG, y), fill=(10, 12, 11, a))
    im.alpha_composite(veu)
    d = ImageDraw.Draw(im)

    # etiqueta verde
    d.rectangle((MARGEM, 96, MARGEM + 6, 96 + 30), fill=VERDE)
    _espacado(d, "PERFFEC · ENGENHARIA EM ESQUADRIAS E VIDROS", MARGEM + 22, 96,
              _f(24, 600), (230, 236, 232), tracking=4)
    if s.get("etiqueta"):
        fe = _f(26, 700)
        larg_et = sum(int(fe.getlength(ch)) + 5 for ch in s["etiqueta"].upper()) + 40
        d.rectangle((MARGEM, 150, MARGEM + larg_et, 150 + 54), fill=(20, 20, 20, 235))
        _espacado(d, s["etiqueta"].upper(), MARGEM + 20, 162, fe, (129, 196, 160), tracking=5)

    # gancho: ancorado embaixo
    tam = s.get("tamanho", 84)
    fg = _f(tam, 750, 96)
    linhas = _quebrar(s["gancho"], fg, UTIL)
    while len(linhas) > 5 and tam > 60:
        tam -= 4
        fg = _f(tam, 750, 96)
        linhas = _quebrar(s["gancho"], fg, UTIL)
    lh = int(tam * 1.08)
    y = ALT - 236 - lh * len(linhas)
    if s.get("sub"):
        y -= 70
    for linha in linhas:
        d.text((MARGEM, y), linha, font=fg, fill=(255, 255, 255))
        y += lh
    if s.get("sub"):
        y += 14
        d.text((MARGEM, y), s["sub"], font=_f(34, 500), fill=(214, 220, 216))

    _logo(im, MARGEM, ALT - 96, 230)
    fa = _f(28, 600)
    txt = "Arraste  →"
    d.text((LARG - MARGEM - fa.getlength(txt), ALT - 128), txt, font=fa, fill=(220, 224, 222))
    return im


def _slide_base(cor_fundo) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (LARG, ALT), cor_fundo + (255,))
    return im, ImageDraw.Draw(im)


def _ajustar_corpo(texto: str, largura: int, disponivel: int, tam: int = 46) -> ImageFont.FreeTypeFont:
    """Reduz o corpo até caber na altura disponível (mínimo 34px)."""
    while tam > 34 and _altura(texto, _f(tam, 400), largura, 1.42, 0.7) > disponivel:
        tam -= 2
    return _f(tam, 400)


def _centrar(y_topo: int, altura_conteudo: int, y_fim: int = ALT - 170) -> int:
    """Desloca o bloco para o centro ótico entre o cabeçalho e o rodapé (um pouco acima do meio)."""
    sobra = (y_fim - y_topo) - altura_conteudo
    return y_topo + max(0, int(sobra * 0.38))


def slide_texto(s: dict, n: int, total: int, fundo=BRANCO, cor_titulo=TINTA, cor_corpo=TINTA2,
                rotulo: str | None = None, cor_rotulo=VERDE, escuro=False) -> Image.Image:
    im, d = _slide_base(fundo)
    y = _cabecalho(d, n, total, rotulo or s.get("rotulo"), cor_rotulo,
                   cor_num=(129, 196, 160) if escuro else VERDE)
    y += 8
    ft = _f(s.get("tamanho_titulo", 62), 700, 96)
    h_tit = (_altura(s["titulo"], ft, UTIL, 1.12, 0) + 40) if s.get("titulo") else 0
    fc = _ajustar_corpo(s["texto"], UTIL, ALT - 170 - y - h_tit) if s.get("texto") else None
    h_txt = _altura(s["texto"], fc, UTIL, 1.42, 0.7) if fc else 0
    y = _centrar(y, h_tit + h_txt)
    if s.get("titulo"):
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, cor_titulo, entrelinha=1.12) + 40
    if fc:
        _bloco(d, s["texto"], MARGEM, y, UTIL, fc, cor_corpo, entrelinha=1.42)
    if escuro:
        _logo(im, MARGEM, ALT - 96, 200)
        f = _f(26, 500)
        d.text((LARG - MARGEM - f.getlength(SITE), ALT - 92), SITE, font=f, fill=(160, 170, 164))
    else:
        _rodape(d)
    return im


def slide_lista(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(BRANCO)
    y = _cabecalho(d, n, total, s.get("rotulo"), VERDE) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 60), 700, 96)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 34
    itens = s["itens"]
    disponivel = ALT - 170 - y
    tam = 44
    while True:
        fr, fc = _f(tam, 700), _f(tam, 400)
        h = 0
        for rot, txt in itens:
            h += _altura(txt, fc, UTIL - 44, 1.36, 0.6) + _altura(rot, fr, UTIL - 44, 1.2, 0) + 30
        if h <= disponivel or tam <= 32:
            break
        tam -= 2
    y = _centrar(y, h)
    for rot, txt in itens:
        d.rectangle((MARGEM, y + int(tam * 0.32), MARGEM + 14, y + int(tam * 0.32) + 14), fill=VERDE)
        y = _bloco(d, rot, MARGEM + 44, y, UTIL - 44, fr, TINTA, entrelinha=1.2) + int(tam * 0.16)
        y = _bloco(d, txt, MARGEM + 44, y, UTIL - 44, fc, TINTA2, entrelinha=1.36) + 30
    _rodape(d)
    return im


def slide_traducao(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(VERDE_FUNDO)
    y = _cabecalho(d, n, total, s.get("rotulo", "Tradução"), VERDE_ESCURO) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 60), 700, 96)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 36
    fc = _ajustar_corpo(s["texto"], UTIL - 40, ALT - 170 - y, tam=52)
    h = _altura(s["texto"], fc, UTIL - 40, 1.42, 0.7)
    y = _centrar(y, h)
    d.rectangle((MARGEM, y, MARGEM + 8, y + h), fill=VERDE)
    _bloco(d, s["texto"], MARGEM + 40, y, UTIL - 40, fc, TINTA, entrelinha=1.42)
    _rodape(d, cor=VERDE_ESCURO)
    return im


def slide_alerta(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(BRANCO)
    y = _cabecalho(d, n, total, s.get("rotulo", "Sinal de alerta"), ALERTA, cor_num=ALERTA) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 60), 700, 96)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 36
    # caixa
    fc = _ajustar_corpo(s["texto"], UTIL - 96, ALT - 270 - y, tam=46)
    h = _altura(s["texto"], fc, UTIL - 96, 1.42, 0.7) + 96
    y = _centrar(y, h)
    d.rectangle((MARGEM, y, LARG - MARGEM, y + h), fill=ALERTA_FUNDO)
    d.rectangle((MARGEM, y, MARGEM + 8, y + h), fill=ALERTA)
    _bloco(d, s["texto"], MARGEM + 48, y + 48, UTIL - 96, fc, TINTA, entrelinha=1.42)
    _rodape(d)
    return im


def slide_perffec(s: dict, n: int, total: int) -> Image.Image:
    return slide_texto(s, n, total, fundo=ESCURO, cor_titulo=(255, 255, 255),
                       cor_corpo=(214, 218, 216), rotulo=s.get("rotulo", "Na Perffec"),
                       cor_rotulo=(129, 196, 160), escuro=True)


def slide_cta(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(ESCURO)
    y = _cabecalho(d, n, total, s.get("rotulo", "Guarde este guia"), (129, 196, 160),
                   cor_num=(129, 196, 160)) + 8
    ft = _f(64, 750, 96)
    fx = _f(40, 400)
    h = _altura(s["titulo"], ft, UTIL, 1.1, 0) + 40
    if s.get("texto"):
        h += _altura(s["texto"], fx, UTIL, 1.42, 0.7) + 56
    h += 40 + 52 + 62 + 44
    y = _centrar(y, h)
    y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, (255, 255, 255), entrelinha=1.1) + 40
    if s.get("texto"):
        y = _bloco(d, s["texto"], MARGEM, y, UTIL, fx, (200, 206, 202), entrelinha=1.42) + 56
    d.rectangle((MARGEM, y, MARGEM + 72, y + 4), fill=VERDE)
    y += 40
    f1 = _f(30, 600)
    d.text((MARGEM, y), "Apoio técnico para especificar e orçar", font=f1, fill=(160, 170, 164))
    y += 52
    d.text((MARGEM, y), f"WhatsApp {WHATS}", font=_f(40, 700), fill=(255, 255, 255))
    y += 62
    d.text((MARGEM, y), f"{SITE}  ·  Amparo e Águas de Lindóia (SP)", font=_f(30, 500), fill=(200, 206, 202))
    _logo(im, MARGEM, ALT - 96, 230)
    f = _f(26, 500)
    d.text((LARG - MARGEM - f.getlength(HANDLE), ALT - 92), HANDLE, font=f, fill=(160, 170, 164))
    return im


RENDER = {
    "capa": None,
    "texto": slide_texto,
    "lista": slide_lista,
    "traducao": slide_traducao,
    "alerta": slide_alerta,
    "perffec": slide_perffec,
    "cta": slide_cta,
}


def gerar(peca: dict, pasta_saida: str) -> list[str]:
    os.makedirs(pasta_saida, exist_ok=True)
    slides = peca["slides"]
    total = len(slides)
    caminhos = []
    for i, s in enumerate(slides, start=1):
        tipo = s.get("tipo", "texto")
        if tipo == "capa":
            im = slide_capa(s, total)
        else:
            im = RENDER[tipo](s, i, total)
        caminho = os.path.join(pasta_saida, f"slide-{i:02d}.jpg")
        im.convert("RGB").save(caminho, quality=92, subsampling=0)
        caminhos.append(caminho)
    return caminhos


def visao_geral(caminhos: list[str], destino: str) -> None:
    """Folha de contato (4 por linha) para conferir a peça inteira de uma vez."""
    w, h = 360, 450
    por_linha = 4
    linhas = (len(caminhos) + por_linha - 1) // por_linha
    folha = Image.new("RGB", (w * por_linha + 12 * (por_linha + 1), h * linhas + 12 * (linhas + 1)), (230, 230, 230))
    for i, c in enumerate(caminhos):
        im = Image.open(c).resize((w, h), Image.LANCZOS)
        folha.paste(im, (12 + (i % por_linha) * (w + 12), 12 + (i // por_linha) * (h + 12)))
    folha.save(destino, quality=85)
