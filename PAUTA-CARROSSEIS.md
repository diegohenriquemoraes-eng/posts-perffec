# Banco de carrosséis técnicos do @perffecesquadrias — pauta e origem

2 por semana (terça e sexta, 7h). Cada linha é um carrossel 4:5 de 7 a 9 slides. **Todo
carrossel sai de material já publicado pela Perffec** — a coluna Fonte diz de onde. Nada é
inventado: quando a fonte não cobre, a peça não entra no banco, eu pergunto ao Diego.

Fontes válidas hoje:

- **E-book "Compare com critério"** (`Perffec\Claude\Ebook-Guia-Esquadrias\curto\miolo.html`,
  12 capítulos + 2 anexos, aprovado pelo Diego em 04/09/2026). É a fonte mais densa e a única
  com fatos da Perffec (linhas, prazos, garantia, engenharia).
- **Blog perffec.com.br** — os 7 posts do robô (repo `blog-perffec`, arquivado em
  `Projetos\_arquivo-morto\blog-perffec.git`, `content/posts/`) e os posts antigos do site
  (`/as-normas-tecnicas-do-vidro/`, `/vidro-temperado-tudo-que-voce-precisa-saber/`,
  `/vidros-para-fachada-quais-sao-as-melhores-opcoes/`).
- **Páginas de serviço do site** (esquadrias, guarda-corpos, brises/ripados, controle térmico).

CTA = o ciclo salvar → enviar → pergunta (ver `_regras` em `carrosseis.json`).
Status: ✅ escrita em `carrosseis.json` · ⬜ pautada

| # | Título | Fonte | CTA | Status |
|---|---|---|---|---|
| 1 | Por que a mesma janela tem três preços | E-book cap. 3 + cap. 9 | salvar | ✅ |
| 2 | Onde o vidro de segurança é obrigatório | E-book cap. 4 + blog normas do vidro | enviar | ✅ |
| 3 | Você não está comprando janela: os 4 componentes | E-book cap. 1 | pergunta | ⬜ |
| 4 | Como a janela abre muda a sua vida (as 6 tipologias) | E-book cap. 2 + blog correr/guilhotina/pivotante | salvar | ⬜ |
| 5 | Peça o laudo: as 5 normas e o que cada uma protege | E-book cap. 5 | enviar | ⬜ |
| 6 | O prazo só começa quando duas coisas acontecem | E-book cap. 7 | pergunta | ⬜ |
| 7 | O que precisa estar pronto para medir | E-book cap. 7 | salvar | ⬜ |
| 8 | 12 perguntas para fazer ao seu arquiteto | E-book cap. 6 | enviar | ⬜ |
| 9 | Compare na mesma régua: a ficha de 15 itens | E-book cap. 9 | pergunta | ⬜ |
| 10 | Contrato: o que tem que estar escrito | E-book cap. 10 | salvar | ⬜ |
| 11 | O dia da instalação: confira antes de assinar | E-book cap. 11 | enviar | ⬜ |
| 12 | Os 10 erros que mais custam caro | E-book cap. 12 | pergunta | ⬜ |
| 13 | Fábrica, revenda ou serralheria: com quem você está falando | E-book cap. 8 | salvar | ⬜ |
| 14 | Proposta 30% mais barata: onde a diferença está escondida | E-book cap. 8 | enviar | ⬜ |
| 15 | Oito palavras que vão aparecer no orçamento | E-book cap. 1 + glossário | pergunta | ⬜ |
| 16 | Vidro insulado: quando ele se paga | Blog vidro-insulado | salvar | ⬜ |
| 17 | PVB acústico: como a janela certa reduz o ruído da rua | Blog pvb-acustico | enviar | ⬜ |
| 18 | Vidro de controle solar: como comparar as linhas | Blog controle-solar | pergunta | ⬜ |
| 19 | Montante oculto: vale o investimento? | Blog minimalista + linha Chroma | salvar | ⬜ |
| 20 | Guarda-corpo de vidro: o que a NBR 14718 exige | E-book cap. 4 + página guarda-corpos | enviar | ⬜ |
| 21 | Manutenção que preserva a garantia (e o que destrói o alumínio) | E-book cap. 11 | pergunta | ⬜ |
| 22 | Mudou o projeto depois da medição: como funciona o aditivo | E-book cap. 7 + cap. 10 | salvar | ⬜ |
| 23 | NBR 7199:2025: o que muda no vidro de portas | Blog nbr-7199 — **conferir a norma antes de escrever** | enviar | ⬜ |
| 24 | NBR 10821: como ler o laudo de ensaio | Blog nbr-10821 — **conferir as classes na norma antes de escrever**; o post cita "classes A, B e C" sem fonte | pergunta | ⬜ |

## Regra de sequência

Nunca duas seguidas do mesmo capítulo/fonte, e alternar "compra" (orçamento, contrato, prazo)
com "técnica" (vidro, norma, tipologia) — o perfil não pode virar um único assunto. A ordem de
publicação vive em `sequencia` no `carrosseis.json`; o `preparar.py` anda por ela.

## O que NÃO entra

- Vendas, gestão comercial, Raio-X, Venda 10x, @vendanaobra — isso é a outra marca.
- Número, percentual, obra nomeada ou depoimento que não esteja em fonte publicada.
- Norma citada sem conferir número e título. Em dúvida, cita-se a norma pelo código sem
  detalhar cláusula.
