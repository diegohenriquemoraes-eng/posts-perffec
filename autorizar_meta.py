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
  meta_token_perffec.txt            token de página (não vence) — o publicar.py lê daqui
  config.json                       ig_user_id do @perffecesquadrias
  secret META_TOKEN_PERFFEC no repo posts-perffec (via API do GitHub, credencial do git)
"""
from __future__ import annotations

import base64
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
    curto = _ler(CURTO)
    segredo = _ler(SECRETO)

    longo = _get("oauth/access_token", grant_type="fb_exchange_token", client_id=APP_ID,
                 client_secret=segredo, fb_exchange_token=curto)["access_token"]
    print("token de usuário de longa duração: ok")

    paginas = _get("me/accounts", fields="name,id,access_token,instagram_business_account{username,id}",
                   access_token=longo)["data"]
    perffec = [p for p in paginas if (p.get("instagram_business_account") or {}).get("username") == "perffecesquadrias"]
    if not perffec:
        nomes = [f"{p['name']} (ig: {(p.get('instagram_business_account') or {}).get('username')})" for p in paginas]
        raise SystemExit("o token não alcança a Página da Perffec. Páginas no token: " + "; ".join(nomes) +
                         "\nGere o token de novo marcando a Página Perffec Esquadrias e o @perffecesquadrias.")
    pag = perffec[0]
    token_pagina = pag["access_token"]
    ig_id = pag["instagram_business_account"]["id"]

    dbg = _get("debug_token", input_token=token_pagina, access_token=longo)["data"]
    print(f"página {pag['name']} ({pag['id']}) · @perffecesquadrias {ig_id} · expira: {dbg.get('expires_at')} (0 = nunca)")
    conta = _get(ig_id, fields="username,followers_count", access_token=token_pagina)
    print(f"conferido: @{conta['username']}, {conta['followers_count']} seguidores")

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(token_pagina + "\n")
    cfg_path = os.path.join(BASE, "config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump({"ig_user_id": ig_id, "page_id": pag["id"]}, f, indent=2)
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

    os.remove(CURTO)
    print("token curto apagado. Pronto: commitar config.json e rodar o ensaio no Actions.")


if __name__ == "__main__":
    main()
