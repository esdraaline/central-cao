# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 06/08/2026

## Novidade de 06/08/2026: publicação automática

O painel agora se publica sozinho. Editou um `.md` e deu push (ou editou pela
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
- [ ] **Josemar: ligar na loja de fardamento esta semana** e resolver o bloco 1 da aba
      [Compras](COMPRAS.md). É o único que depende de terceiro: 2 camisas de passeio,
      2 camisetas de serviço, aplicação de tarjeta e logomarca, 4 distintivos de OPM do CAES e
      a tarjeta administrativa de acrílico. Se não sair esta semana, não volta a tempo do dia 16/08.
      O resto (calça social, boina, camisa social e gravata do S-1) é peça pronta, dá até 12/08.
- [ ] Josemar: me contar o que está rolando no curso agora (módulo atual, próxima entrega, próxima aula presencial) pra eu atualizar [PRAZOS.md](PRAZOS.md) e este painel.
- [ ] Enviar Ofício de Apresentação pra mesa SEI 302090130 e liberar a Rotina 13 do SIPA (código 302090000), se ainda não fez — matrícula e verbas dependem disso (ver [ROTINA.md](ROTINA.md)).
- [ ] Regularizar conta Banco do Brasil pro Auxílio Financeiro a Estudantes (não pode ser "Conta Salário", nome não pode estar no CADIN).

## Prazos mais próximos
Ver [PRAZOS.md](PRAZOS.md) para a lista completa.

## Painel visual

No ar em https://esdraaline.github.io/central-cao — **gerado** a partir dos `.md`, nunca editado à mão.
Depois de mexer em qualquer `.md`, rode `python gerar_painel.py` (ou só dê push: a publicação é automática).

Como o painel funciona por dentro (caixinhas ticáveis, marcação parcial, sincronização entre aparelhos,
aba Tarefas): [`PAINEL.md`](PAINEL.md).

## Regras desta pasta
- **Os .md são a fonte de verdade.** O painel HTML é só o visor; nunca edite `docs/index.html` à mão, porque a próxima geração sobrescreve.
- Documentos pesados (PDF de estudo, edital, PP) ficam só aqui local + Google Drive. A pasta `CAO 2026/` inteira está no `.gitignore` e **não vai para o GitHub**.
- O que vira repositório: os .md, o `gerar_painel.py` e a pasta `docs/` (o painel publicado).
