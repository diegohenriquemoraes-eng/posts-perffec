# -*- coding: utf-8 -*-
"""Transforma o token CURTO do Explorador da Graph API no token de PÁGINA da Perffec
(que não vence) e grava tudo onde o publicador precisa. Roda no PC do Diego.

Por que existe: o system user "vendanaobra-posts" não enxerga a Perffec — a
Página e o @perffecesquadrias vivem no portfólio "Perffec Esquadrias", onde o
Diego não tem controle total. Mas ele tem acesso total à PÁGINA como pessoa;
então o caminho é token de usuário → token de página.

Entrada (dois arquivos em Perffec\\Claude\\, colados pelo Diego, nunca no chat):
  meta_token_perffec_curto.txt      token gerado no Explorador (app vendanaobra,
                                    com a Página Perffec Esquadrias marcada)
  meta_app_secret_vendanaobra.txt   "Chave secreta do app" em
                                    developers.facebook.com/apps/1910368269635506/settings/basic

Saída:
  meta_token_perffec.txt            token de USUÁRIO de 60 dias — o publicar.py lê daqui.
                                    `python autorizar_meta.py --renovar` troca por mais 60
                                    (sem Explorador), enquanto o atual ainda vale.
  config.json                       ig_user_id do @perffecesquadrias
  secret META_TOKEN_PERFFEC no repo posts-perffec (via API do GitHub, credencial do git)
"""
from __future__ import annotations

import base64
from datetime import datetime
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

PASTA = r"C:\Users\NOTE\Desktop\Perffec\Claude"
CURTO = os.path.join(PASTA, "meta_token_perffec_curto.txt")
SECRETO = os.path.join(PASTA, "meta_app_secret_vendanaobra.txt")
SAIDA = os.path.join(PASTA, "meta_token_perffec.txt")
APP_ID = "1910368269635506"
IG_ID = "17841460293101375"      # @perffecesquadrias
PAGE_ID = "674057852453507"     # Perffec Esquadrias
API = "https://graph.facebook.com/v21.0"
BASE = os.path.dirname(os.path.abspath(__file__))
REPO = "diegohenriquemoraes-eng/posts-perffec"


def _ler(caminho: str) -> str:
    if not os.path.exists(caminho):
        raise SystemExit(f"falta o arquivo {caminho}")
    with open(caminho, encoding="utf-8") as f:
        return f.read().strip()


def _get(path: str, **q) -> dict:
    url = f"{API}/{path}?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def main() -> None:
    segredo = _ler(SECRETO)
    if "--renovar" in sys.argv:
        curto = _ler(SAIDA)   # um token longo ainda válido também pode ser trocado
    else:
        curto = _ler(CURTO)

    longo = _get("oauth/access_token", grant_type="fb_exchange_token", client_id=APP_ID,
                 client_secret=segredo, fb_exchange_token=curto)["access_token"]
    print("token de usuário de longa duração: ok")

    # A Página da Perffec NÃO aparece em me/accounts (o acesso do Diego a ela é
    # via portfólio, task-based), então não existe token de página. Mas o token de
    # USUÁRIO alcança o @perffecesquadrias e o content_publishing_limit responde —
    # conferido no Explorador em 14/09/2026. Vale 60 dias; renovar com --renovar.
    token_pagina = longo
    ig_id = IG_ID
    dbg = _get("debug_token", input_token=longo, access_token=longo)["data"]
    exp = dbg.get("expires_at", 0)
    quando = datetime.fromtimestamp(exp).strftime("%d/%m/%Y") if exp else "nunca"
    conta = _get(ig_id, fields="username,followers_count", access_token=longo)
    if conta.get("username") != "perffecesquadrias":
        raise SystemExit(f"token aponta para @{conta.get('username')}; abortando")
    _get(f"{ig_id}/content_publishing_limit", fields="quota_usage", access_token=longo)
    print(f"conferido: @{conta['username']}, {conta['followers_count']} seguidores · publicação liberada · vence em {quando}")

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(longo + "\n")
    cfg_path = os.path.join(BASE, "config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump({"ig_user_id": ig_id, "page_id": PAGE_ID, "token_vence_em": quando}, f, indent=2)
        f.write("\n")
    print(f"gravado: {SAIDA} e config.json")

    # secret no GitHub (precisa de pynacl; se faltar, avisa como fazer à mão)
    try:
        from nacl import encoding, public  # type: ignore
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "pynacl"], check=True)
        from nacl import encoding, public  # type: ignore
    cred = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                          capture_output=True, text=True, check=True).stdout
    gh = next(l.split("=", 1)[1] for l in cred.splitlines() if l.startswith("password="))
    hdr = {"Authorization": f"token {gh}", "Accept": "application/vnd.github+json"}
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/secrets/public-key", headers=hdr)
    with urllib.request.urlopen(req) as r:
        chave = json.loads(r.read())
    pk = public.PublicKey(chave["key"].encode(), encoding.Base64Encoder())
    cifrado = base64.b64encode(public.SealedBox(pk).encrypt(token_pagina.encode())).decode()
    body = json.dumps({"encrypted_value": cifrado, "key_id": chave["key_id"]}).encode()
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/secrets/META_TOKEN_PERFFEC",
                                 data=body, headers=hdr, method="PUT")
    with urllib.request.urlopen(req) as r:
        print("secret META_TOKEN_PERFFEC:", r.status)

    if os.path.exists(CURTO):
        os.remove(CURTO)
    print("token curto apagado. Pronto: commitar config.json e rodar o ensaio no Actions.")


if __name__ == "__main__":
    main()
