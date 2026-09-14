# -*- coding: utf-8 -*-
"""Prepara o carrossel técnico do @perffecesquadrias para o Diego postar do celular.

    python preparar.py                 # a próxima peça da sequência, na próxima terça/quinta
    python preparar.py --semana        # as duas da semana (terça e quinta)
    python preparar.py --slug X        # uma peça específica (não marca como preparada)
    python preparar.py --data 2026-09-15

Saída: saida/<data>-<slug>/ (gitignorado) e uma cópia em
Perffec\\Claude\\Instagram-Perffec\\<data>-<slug>\\ com slide-01..NN.jpg, legenda.txt e
visao-geral.jpg. O que foi preparado fica em preparados.json — a sequência anda a partir
dele. A publicação é MANUAL: a página da Perffec não está no token da Graph API.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil

from gerar_carrossel import gerar, visao_geral

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE, "carrosseis.json")
PREPARADOS = os.path.join(BASE, "preparados.json")
SAIDA = os.path.join(BASE, "saida")
ENTREGA = r"C:\Users\NOTE\Desktop\Perffec\Claude\Instagram-Perffec"

DIAS = (1, 3)  # terça e quinta (segunda = 0)
HORA = "12h"


def _carregar(caminho: str, padrao):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _salvar(caminho: str, dados) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")


def proximas_datas(a_partir: dt.date, n: int) -> list[dt.date]:
    datas, d = [], a_partir
    while len(datas) < n:
        if d.weekday() in DIAS:
            datas.append(d)
        d += dt.timedelta(days=1)
    return datas


def preparar(slug: str, data: dt.date, banco: dict) -> str:
    peca = banco["pecas"][slug]
    nome = f"{data.isoformat()}-{slug}"
    pasta = os.path.join(SAIDA, nome)
    caminhos = gerar(peca, pasta)
    visao_geral(caminhos, os.path.join(pasta, "visao-geral.jpg"))
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(peca["legenda"].strip() + "\n")
    with open(os.path.join(pasta, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write(f"{peca['titulo']}\n"
                f"Publicar: {data.strftime('%d/%m/%Y')} ({['seg','ter','qua','qui','sex','sáb','dom'][data.weekday()]}) às {HORA}\n"
                f"Fonte: {peca['fonte']}\n"
                f"CTA: {peca['cta']['tipo']}\n"
                f"{len(caminhos)} slides — subir na ordem slide-01 … slide-{len(caminhos):02d}, "
                f"legenda em legenda.txt, música fixa da conta (se houver), marcar localização Amparo/SP.\n")
    destino = os.path.join(ENTREGA, nome)
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    shutil.copytree(pasta, destino)
    return destino


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--semana", action="store_true", help="prepara as duas peças da semana")
    ap.add_argument("--slug", help="prepara uma peça específica (não avança a sequência)")
    ap.add_argument("--data", help="AAAA-MM-DD da primeira publicação")
    args = ap.parse_args()

    banco = _carregar(BANCO, {})
    preparados = _carregar(PREPARADOS, [])
    feitos = {p["slug"] for p in preparados}

    hoje = dt.date.today()
    inicio = dt.date.fromisoformat(args.data) if args.data else hoje + dt.timedelta(days=1)

    if args.slug:
        destino = preparar(args.slug, inicio if args.data else proximas_datas(inicio, 1)[0], banco)
        print("preparado (avulso):", destino)
        return

    fila = [s for s in banco["sequencia"] if s not in feitos]
    if not fila:
        raise SystemExit("Sequência esgotada: escreva peças novas em carrosseis.json (ver PAUTA-CARROSSEIS.md).")
    quantos = 2 if args.semana else 1
    datas = proximas_datas(inicio, quantos)
    for slug, data in zip(fila[:quantos], datas):
        destino = preparar(slug, data, banco)
        preparados.append({"slug": slug, "data": data.isoformat(), "preparado_em": hoje.isoformat()})
        print(f"{data.isoformat()}  {slug}  ->  {destino}")
    _salvar(PREPARADOS, preparados)
    restantes = len(fila) - quantos
    print(f"restam {restantes} peça(s) escritas na sequência" + (" — ESCREVER MAIS" if restantes < 2 else ""))


if __name__ == "__main__":
    main()
