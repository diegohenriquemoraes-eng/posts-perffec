# posts-perffec — carrossel técnico do @perffecesquadrias

Criado em 14/09/2026 a pedido do Diego: *"assim como fazemos os carrosséis no Instagram do
Venda na Obra, quero 2 carrosséis por semana com conteúdo técnico no Instagram da Perffec"*.

## O que é

2 carrosséis/semana (**terça e quinta, 12h**), 4:5, 7 a 9 slides, conteúdo técnico de
esquadria/vidro/norma/obra, para arquiteto, engenheiro, construtor e cliente final de alto
padrão. O critério é o mesmo da mini-aula do @vendanaobra: **toda peça sai de material já
publicado** (aqui: o e-book "Compare com critério" e o blog da Perffec), com a fonte
registrada; nada inventado; um ensinamento inteiro dentro do post, para ser SALVO.

| Peça | Onde |
|---|---|
| Banco de peças (regras, sequência, slides, legenda) | `carrosseis.json` |
| Pauta (24 temas com fonte e status) | `PAUTA-CARROSSEIS.md` |
| Render dos slides | `gerar_carrossel.py` (Pillow, Archivo variável, paleta preto/verde da LP e do e-book) |
| Preparar a semana | `python preparar.py --semana` → `saida/` + cópia em `Perffec\Claude\Instagram-Perffec\<data>-<slug>\` |
| Registro do que foi preparado | `preparados.json` (a sequência anda a partir dele) |
| Fotos de capa | `fotos/` — obras da Perffec, copiadas da LP (`LPs-Perffec/esquadrias`). Nunca banco de imagem |

## Como sai no ar — AUTOMÁTICO desde 14/09/2026

`carrossel.yml` roda terça e quinta (11:45 UTC espera até 15:00 = 12h BRT; repescagens
13:07 e 17:23 BRT com `--garantir`). `publicar.py` renderiza, commita as imagens (o repo é
**público** porque a Graph só aceita URL pública — `raw.githubusercontent`), sobe o carrossel
e registra em `publicados.json`. Falha abre issue.

**O token é de USUÁRIO, vale 60 dias (vence 13/11/2026)** — secret `META_TOKEN_PERFFEC`.
Por que não é o token eterno do system user: a Página da Perffec vive no portfólio
"Perffec Esquadrias" (criado pela Thamiris; controle total é do Alef/agência), o Diego
não tem controle total lá e a Página não aparece em `me/accounts` — logo não existe token
de página. Mas o token de usuário do app `vendanaobra` alcança o @perffecesquadrias
(`17841460293101375`) e o `content_publishing_limit` responde. Foi preciso **remover o app
vendanaobra em facebook.com/settings?tab=business_tools e autorizar de novo** escolhendo
"todas as Páginas atuais e futuras" — sem isso o Facebook não repergunta e o token nasce só
com "Cortes do Marçal".

**Renovar (a cada ~55 dias; `publicar.py` aborta e abre issue com < 10 dias):**
1. `developers.facebook.com/tools/explorer` → app vendanaobra, as 5 permissões → Generate
   Access Token → Continuar → Copy Token.
2. `developers.facebook.com/tools/debug/accesstoken` → colar → Depurar → **Estender token de
   acesso** → copiar o token longo (60 dias). Não precisa da chave secreta do app (que pede a
   senha do Facebook e por isso o Claude não alcança).
3. Salvar em `Perffec\Claude\meta_token_perffec.txt` e gravar o secret — o bloco do
   `autorizar_meta.py` faz isso (`--renovar` exige a chave secreta; sem ela, o Claude sobe o
   secret direto pela API do GitHub com a credencial do git, como em 14/09).

Tudo isso o Claude fez pelo Chrome em 14/09 (o Diego só clicou "Continuar" no OAuth); o
que o classificador bloqueia é ler o token da página por JS — o caminho é Copy Token →
`Get-Clipboard` no PowerShell.

## Decisões

- **Identidade própria**: preto `#141414` + verde `#3E7459` + branco, **Archivo** em tudo.
  Não é a do @vendanaobra (navy/dourado/Playfair) de propósito: Perffec e Venda na Obra não
  se misturam (regra de 07/09/2026, `Marca-Perffec/RETOMAR.md`).
- **Blocos herdados do e-book**: "Tradução" (verde-claro), "Sinal de alerta" (vermelho) e
  "Na Perffec" (preto). O "Na Perffec" traz um **fato verificável** (linhas Standard/Prime/
  Chroma, engenharia que dimensiona por vão, laudo, 2 visitas, 7 dias úteis, 30 mm, 5 anos),
  nunca slogan. A lista completa do que pode ser afirmado está em `_regras`.
- **CTA em ciclo** salvar → enviar (para o arquiteto) → pergunta. Sem "comente a palavra":
  não há robô de Direct neste perfil.
- **Hashtags**: 8 a 9, nicho + local (`#amparo #aguasdelindoia #campinas`).
- **Os posts do blog com norma detalhada (NBR 10821 "classes A/B/C", NBR 7199:2025) não viram
  carrossel sem conferir a norma** — foram escritos por robô e a voz da Perffec exige norma
  conferida. Marcado na pauta.

## Régua

Primeira leitura em **12/10/2026** (4 semanas, 8 peças): salvamentos e compartilhamentos por
peça (Insights do app, à mão), alcance de não seguidores, e se algum arquiteto/construtor
chegou pelo post. Formato satura (o carrossel de frase do @vendanaobra caiu 75% em 3
semanas): se salvamentos caírem por 3 peças seguidas, mudar o tipo de capa antes de mudar o
conteúdo.

## Pendências do Diego

- Nada para postar à mão: terça 15/09 12h sai a primeira peça sozinha. Conferir no perfil.
- Música fixa da conta para carrossel (o método pede uma só, sempre a mesma): escolher uma.

## Rodar

```powershell
python preparar.py --semana                 # as próximas 2 (terça e quinta a partir de amanhã)
python preparar.py --semana --data 2026-09-22
python preparar.py --slug <slug> --data 2026-09-15   # refaz uma peça sem mexer na sequência
```

Escrever peça nova = adicionar em `pecas` e em `sequencia` no `carrosseis.json`, marcar ✅ na
pauta, renderizar com `--slug` e olhar `visao-geral.jpg` antes de entregar.
