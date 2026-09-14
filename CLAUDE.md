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

## Como sai no ar — MANUAL, por enquanto

A página da Perffec **não está no token da Graph API** (`me/accounts` do system user só
devolve a Venda na Obra). Então o `preparar.py` entrega slides + `legenda.txt` + `LEIA-ME.txt`
e o Diego posta/agenda pelo próprio Instagram. Para automatizar, o Diego precisa adicionar a
Página do Facebook da Perffec (e o IG vinculado) aos ativos do system user no Gerenciador de
Negócios — aí o `publicar.py` do `posts-vendanaobra` serve quase inteiro (muda só `IG_USER_ID`).
Enquanto for manual, as duas peças da semana são preparadas juntas (domingo/segunda), e quem
posta é o Diego ou a Thamiris (social media, expediente até 18h) — o carrossel entra por cima do
ciclo de 04/09 (1 Reel + 4 stories/dia), como o terceiro formato do método.

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

- Postar (ou passar à Thamiris) as duas peças da semana de 15/09 (pastas em
  `Perffec\Claude\Instagram-Perffec\`).
- Se quiser automatizar: adicionar a Página da Perffec aos ativos do system user da Meta.
- Música fixa da conta para carrossel (o método pede uma só, sempre a mesma): escolher uma.

## Rodar

```powershell
python preparar.py --semana                 # as próximas 2 (terça e quinta a partir de amanhã)
python preparar.py --semana --data 2026-09-22
python preparar.py --slug <slug> --data 2026-09-15   # refaz uma peça sem mexer na sequência
```

Escrever peça nova = adicionar em `pecas` e em `sequencia` no `carrosseis.json`, marcar ✅ na
pauta, renderizar com `--slug` e olhar `visao-geral.jpg` antes de entregar.
