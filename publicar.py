# -*- coding: utf-8 -*-
"""Publica o carrossel técnico do dia no feed do @perffecesquadrias pela Graph API.

Roda TERÇA e QUINTA, 12h BRT (workflow `carrossel.yml`). Fluxo — o mesmo da
mini-aula do @vendanaobra, que rodou sem falha de 24/08 a 03/09/2026:

  1. escolhe a próxima peça da `sequencia` do carrosseis.json que ainda não saiu
  2. renderiza os slides em imagens/<data>/ (gerar_carrossel.py)
  3. commita e sobe as imagens — raw.githubusercontent é a URL pública que a
     Graph exige (por isso o repo é PÚBLICO; nada de segredo entra nele)
  4. containers filhos → container CAROUSEL com a legenda → media_publish
  5. registra em publicados.json (o que já saiu nunca sai de novo)

Uso:
    python publicar.py              # próxima da sequência (só ter/qui)
    python publicar.py --slug X     # peça específica, qualquer dia
    python publicar.py --ensaio     # renderiza e imprime a legenda, sem publicar
    python publicar.py --garantir   # repescagem: só publica se a de hoje não saiu

Token: META_TOKEN (secret do Actions) ou Perffec\\Claude\\meta_token_perffec.txt.
É um token de PÁGINA da Perffec Esquadrias, derivado de um token de usuário
de longa duração do app vendanaobra — o system user "vendanaobra-posts" não
enxerga a Perffec (ela vive em outro portfólio empresarial, onde o Diego não
tem controle total). Ver CLAUDE.md, "Como sai no ar".
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from gerar_carrossel import gerar, visao_geral

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE, "carrosseis.json")
PUBLICADOS = os.path.join(BASE, "publicados.json")
IG_USER_ID = os.environ.get("IG_USER_ID_PERFFEC", "").strip()  # preenchido no config abaixo
CONFIG = os.path.join(BASE, "config.json")
API = "https://graph.facebook.com/v21.0"
REPO_RAW = "https://raw.githubusercontent.com/diegohenriquemoraes-eng/posts-perffec/main"
FUSO_BR = timezone(timedelta(hours=-3))
DIAS = (1, 3)  # terça, quinta


def _log(msg: str) -> None:
    print(f"[{datetime.now(FUSO_BR):%H:%M:%S}] {msg}", flush=True)


def _carregar(caminho: str, padrao):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _salvar(caminho: str, dados) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _token() -> str:
    tok = os.environ.get("META_TOKEN", "").strip()
    if tok:
        return tok
    caminho = r"C:\Users\NOTE\Desktop\Perffec\Claude\meta_token_perffec.txt"
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            return f.read().strip()
    raise SystemExit("Sem token: defina META_TOKEN ou salve meta_token_perffec.txt")


def _ig_user_id() -> str:
    cfg = _carregar(CONFIG, {})
    return IG_USER_ID or cfg.get("ig_user_id") or ""


def _post(endpoint: str, campos: dict) -> dict:
    dados = urllib.parse.urlencode(campos).encode()
    req = urllib.request.Request(f"{API}/{endpoint}", data=dados, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        raise SystemExit(f"Graph API falhou em {endpoint}: {corpo}")


def _get(endpoint: str, campos: dict) -> dict:
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode(campos)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        raise SystemExit(f"Graph API falhou em {endpoint}: {corpo}")


def _git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=BASE, check=True)


def _commitar(mensagem: str, *caminhos: str) -> None:
    """Commita e sobe. Silencioso quando não há nada novo."""
    _git("add", *caminhos)
    pronto = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BASE).returncode != 0
    if pronto:
        _git("-c", "user.name=perffec-bot", "-c", "user.email=bot@perffec.com.br",
             "commit", "-m", mensagem)
    _git("push", "origin", "main")


def esperar_container(container_id: str, token: str, tentativas: int = 30) -> None:
    """A Graph API precisa baixar a imagem antes de deixar publicar."""
    for _ in range(tentativas):
        r = _get(container_id, {"fields": "status_code,status", "access_token": token})
        estado = r.get("status_code")
        if estado == "FINISHED":
            return
        if estado == "ERROR":
            raise SystemExit(f"Container {container_id} falhou: {r.get('status')}")
        time.sleep(4)
    raise SystemExit(f"Container {container_id} não ficou pronto a tempo")


def conferir_token(token: str, ig_id: str) -> None:
    """Falha cedo, com o nome da conta: token no canal errado é o erro que mais custa."""
    r = _get(ig_id, {"fields": "username,followers_count", "access_token": token})
    if r.get("username") != "perffecesquadrias":
        raise SystemExit(f"token aponta para @{r.get('username')} — não é a Perffec; abortando")
    _log(f"token ok — @{r['username']}, {r['followers_count']} seguidores")


def subir_e_publicar(caminhos: list[str], data: str, slug: str, legenda: str,
                     token: str, ig_id: str) -> str:
    _commitar(f"imagens do carrossel {slug}", "imagens")
    urls = [f"{REPO_RAW}/imagens/{data}/{os.path.basename(c)}" for c in caminhos]
    _log("imagens no ar: " + " | ".join(urls))
    time.sleep(5)  # folga para o CDN do raw responder

    filhos = []
    for url in urls:
        r = _post(f"{ig_id}/media", {"image_url": url, "is_carousel_item": "true",
                                     "access_token": token})
        filhos.append(r["id"])
        _log(f"container filho {r['id']}")
    for f in filhos:
        esperar_container(f, token)

    pai = _post(f"{ig_id}/media", {"media_type": "CAROUSEL", "children": ",".join(filhos),
                                   "caption": legenda, "access_token": token})["id"]
    esperar_container(pai, token)
    _log(f"container do carrossel {pai}")

    post = _post(f"{ig_id}/media_publish", {"creation_id": pai, "access_token": token})
    _log(f"PUBLICADO: {post['id']}")
    return post["id"]


def escolher(banco: dict, publicados: list, slug_forcado: str | None) -> tuple[str, dict] | None:
    if slug_forcado:
        return slug_forcado, banco["pecas"][slug_forcado]
    feitos = {p["slug"] for p in publicados}
    for slug in banco["sequencia"]:
        if slug not in feitos:
            return slug, banco["pecas"][slug]
    return None


def ja_saiu_hoje(publicados: list, hoje: str) -> bool:
    return any(p["data"] == hoje for p in publicados)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--ensaio", action="store_true")
    ap.add_argument("--garantir", action="store_true")
    a = ap.parse_args()

    agora = datetime.now(FUSO_BR)
    hoje = agora.strftime("%Y-%m-%d")
    banco = _carregar(BANCO, {})
    publicados = _carregar(PUBLICADOS, [])

    if a.slug is None and not a.ensaio and agora.weekday() not in DIAS:
        _log("carrossel só sai terça e quinta — nada a fazer")
        return
    if a.garantir and ja_saiu_hoje(publicados, hoje):
        _log("carrossel do dia já está no ar — nada a fazer")
        return

    escolha = escolher(banco, publicados, a.slug)
    if escolha is None:
        raise SystemExit("Sequência esgotada: escrever peças novas em carrosseis.json (ver PAUTA-CARROSSEIS.md).")
    slug, peca = escolha
    restantes = len([s for s in banco["sequencia"] if s not in {p["slug"] for p in publicados}]) - 1
    _log(f"peça: {slug} — {peca['titulo']} ({restantes} restantes na sequência)")

    pasta = os.path.join(BASE, "imagens", hoje)
    caminhos = gerar(peca, pasta)
    visao_geral(caminhos, os.path.join(pasta, "visao-geral.jpg"))
    _log(f"{len(caminhos)} slides em {pasta}")

    if a.ensaio:
        print("\n--- legenda ---\n" + peca["legenda"].strip() + "\n---------------\n")
        _log("ensaio: parando antes de publicar")
        return

    token = _token()
    ig_id = _ig_user_id()
    if not ig_id:
        raise SystemExit("Sem ig_user_id: preencher config.json (id da conta @perffecesquadrias)")
    conferir_token(token, ig_id)

    media_id = subir_e_publicar(caminhos, hoje, slug, peca["legenda"].strip(), token, ig_id)
    publicados.append({"slug": slug, "titulo": peca["titulo"], "data": hoje,
                       "media_id": media_id, "cta": peca["cta"]["tipo"]})
    _salvar(PUBLICADOS, publicados)
    _commitar(f"carrossel {hoje} {slug} publicado", "publicados.json")
    if restantes < 2:
        _log(f"ATENÇÃO: restam {restantes} peça(s) escritas — escrever mais em carrosseis.json")


if __name__ == "__main__":
    main()
