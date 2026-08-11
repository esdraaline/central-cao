# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 11/08/2026

## Novidade de 11/08/2026: o painel virou guia do dia

Abrir o painel agora responde à pergunta certa: **o que eu faço hoje**. A abertura
mostra a data por extenso, em que ponto da semana você está (em casa, dia de
viajar, semana de aula, dia de voltar), a contagem para o próximo marco e as
tarefas separadas em *hoje*, *amanhã* e *ainda esta semana*. Os cartões de
Compras e Mala mostram quantos itens ainda faltam, lendo o que você já ticou.

Duas regras que nasceram daí:

- **Tarefa sem data não aparece no guia.** A data em `[dd/mm/aaaa]` no
  [TAREFAS.md](TAREFAS.md) é o que faz o item ser cobrado no dia certo.
- **Toda conta de tempo é feita no navegador**, nunca na geração. O painel
  publicado só é regerado quando um `.md` muda, então contador calculado na
  geração congela: o cartão ficou de 08/08 a 11/08 dizendo "9 dias para o
  início" quando já faltavam 6. Corrigido.

## Publicação automática (06/08/2026)

O painel se publica sozinho. Editou um `.md` e deu push (ou editou pela
web do GitHub, do celular), o painel regenera e vai para o ar sem ninguém rodar
nada. Rodar `python gerar_painel.py` na mão continua valendo para conferir antes
de subir. Detalhe e o histórico do build quebrado do Pages estão em
[ANOTACOES.md](ANOTACOES.md).

## Onde estou agora
- Sou **Oficial-Aluno do CAO/II-2026** (2ª Turma) — **Programa de Mestrado Profissional em Ciências Policiais de Segurança e Ordem Pública**, no **CAES "Cel Nelson Freire Terra"** (região da Barra Funda, São Paulo — Av. Rio Branco / Av. Duque de Caxias).
- Curso roda de **ago/2026 a ago/2027** (conforme edital). Rotina 13 do SIPA liberada de **17/ago/26 a 22/jan/27** (1º bloco financeiro/administrativo).
- Fase de seleção (inscrição, prova escrita, defesa do PP) já concluída — documentos arquivados em [CAO 2026/Inscrição](CAO%202026/Inscrição/).
- Projeto de Pesquisa (PP) tem versão final entregue em [CAO 2026/PP/Projeto Pesquisa Cap Josemar Final.doc](CAO%202026/PP/Projeto%20Pesquisa%20Cap%20Josemar%20Final.doc) — tema: integração PM-Prefeituras / governança participativa no 2º BPM/I. Como agora é mestrado profissional, isso deve virar **dissertação** (ver contato de Pesquisa em [CONTATOS.md](CONTATOS.md)).
- Contatos e organograma do CAES: ver [CONTATOS.md](CONTATOS.md).
- Regras de rotina, uniforme, SIPA financeiro, formatura: ver [ROTINA.md](ROTINA.md).
- **Primeira semana: viaja domingo 16/08/2026**, aulas de segunda a quinta (entra 08h15; sai 16h seg, 18h ter e qua, 11h30 qui). A conferência de armário está **feita** (06/08, 78 das 90 peças já em casa), então sobraram duas etapas: [COMPRAS.md](COMPRAS.md) (o que falta) → [MALA.md](MALA.md) (arrumar a mala no dia).
- **Falta preencher**: em qual módulo/disciplina o curso está agora, o que já foi entregue no curso em si (não só na seleção/recepção).

## Próximo passo

O roteiro dia a dia até a viagem está em [TAREFAS.md](TAREFAS.md), com data, e é o
que o painel cobra na abertura (por isso aqui é só leitura, para não ter duas listas
dizendo a mesma coisa). O que trava tudo:

1. **Ligar hoje na loja de fardamento.** É o único bloco que depende de terceiro:
   2 camisas de passeio, 2 camisetas de serviço, aplicação de tarjeta e logomarca,
   4 distintivos de OPM do CAES e a tarjeta administrativa de acrílico. Se a
   aplicação não entrar esta semana, não volta a tempo do dia 16/08.
2. **Escrever ao SAE** com as perguntas de [DUVIDAS.md](DUVIDAS.md) (horário de
   chegada no domingo, tamanho da cama, armário, estacionamento). A resposta muda
   a mala e a hora de sair.
3. **Fechar como vou viajar** (carro ou ônibus) e preencher em [VIAGENS.md](VIAGENS.md).
   Se for de carro, o cartão de estacionamento precisa ser pedido antes.
4. Josemar: me contar o que está rolando no curso (módulo, entregas, avaliações)
   pra eu completar [PRAZOS.md](PRAZOS.md).

## Prazos mais próximos
Agosto inteiro, dia a dia, está em [PRAZOS.md](PRAZOS.md).

## Painel visual

No ar em https://esdraaline.github.io/central-cao — **gerado** a partir dos `.md`, nunca editado à mão.
Depois de mexer em qualquer `.md`, rode `python gerar_painel.py` (ou só dê push: a publicação é automática).

Como o painel funciona por dentro (caixinhas ticáveis, marcação parcial, sincronização entre aparelhos,
aba Tarefas): [`PAINEL.md`](PAINEL.md).

## Regras desta pasta
- **Os .md são a fonte de verdade.** O painel HTML é só o visor; nunca edite `docs/index.html` à mão, porque a próxima geração sobrescreve.
- Documentos pesados (PDF de estudo, edital, PP) ficam só aqui local + Google Drive. A pasta `CAO 2026/` inteira está no `.gitignore` e **não vai para o GitHub**.
- O que vira repositório: os .md, o `gerar_painel.py` e a pasta `docs/` (o painel publicado).
