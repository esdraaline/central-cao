# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 04/08/2026

## Onde estou agora
- Sou **Oficial-Aluno do CAO/II-2026** (2ª Turma) — **Programa de Mestrado Profissional em Ciências Policiais de Segurança e Ordem Pública**, no **CAES "Cel Nelson Freire Terra"** (região da Barra Funda, São Paulo — Av. Rio Branco / Av. Duque de Caxias).
- Curso roda de **ago/2026 a ago/2027** (conforme edital). Rotina 13 do SIPA liberada de **17/ago/26 a 22/jan/27** (1º bloco financeiro/administrativo).
- Fase de seleção (inscrição, prova escrita, defesa do PP) já concluída — documentos arquivados em [CAO 2026/Inscrição](CAO%202026/Inscrição/).
- Projeto de Pesquisa (PP) tem versão final entregue em [CAO 2026/PP/Projeto Pesquisa Cap Josemar Final.doc](CAO%202026/PP/Projeto%20Pesquisa%20Cap%20Josemar%20Final.doc) — tema: integração PM-Prefeituras / governança participativa no 2º BPM/I. Como agora é mestrado profissional, isso deve virar **dissertação** (ver contato de Pesquisa em [CONTATOS.md](CONTATOS.md)).
- Contatos e organograma do CAES: ver [CONTATOS.md](CONTATOS.md).
- Regras de rotina, uniforme, SIPA financeiro, formatura: ver [ROTINA.md](ROTINA.md).
- **Primeira semana: viaja domingo 16/08/2026**, aulas de segunda a quinta (entra 08h15; sai 16h seg, 18h ter e qua, 11h30 qui). A preparação é em três etapas: [CONFERIR.md](CONFERIR.md) (tico o que já tenho) → [COMPRAS.md](COMPRAS.md) (o que sobrou) → [MALA.md](MALA.md) (arrumar a mala no dia).
- **Falta preencher**: em qual módulo/disciplina o curso está agora, o que já foi entregue no curso em si (não só na seleção/recepção).

## Próximo passo
- [ ] **Josemar: fazer a conferência de armário na aba [Conferir](CONFERIR.md)** (90 peças). O que sobrar
      em branco vira a lista de [Compras](COMPRAS.md) — e o que depende de costura na loja de fardamento
      (tarjeta, logomarca, distintivo do CAES) precisa sair **esta semana**, porque viaja dia 16/08.
- [ ] Josemar: me contar o que está rolando no curso agora (módulo atual, próxima entrega, próxima aula presencial) pra eu atualizar [PRAZOS.md](PRAZOS.md) e este painel.
- [ ] Enviar Ofício de Apresentação pra mesa SEI 302090130 e liberar a Rotina 13 do SIPA (código 302090000), se ainda não fez — matrícula e verbas dependem disso (ver [ROTINA.md](ROTINA.md)).
- [ ] Regularizar conta Banco do Brasil pro Auxílio Financeiro a Estudantes (não pode ser "Conta Salário", nome não pode estar no CADIN).

## Prazos mais próximos
Ver [PRAZOS.md](PRAZOS.md) para a lista completa.

## Painel visual
No ar em **https://esdraaline.github.io/central-cao** (repositório `esdraaline/central-cao`).
Também abre local com duplo clique em `docs/index.html`.
Ele é **gerado** a partir destes .md, não editado à mão. Depois de mexer em qualquer .md, rode:

```
python gerar_painel.py
```

### Caixinhas ticáveis
Nas abas geradas dos .md (Conferir, Compras, Mala, Rotina), **as caixinhas são clicáveis**: clique para
marcar, clique de novo para desmarcar.

**Item com quantidade aceita marcação parcial.** Todo item que começa com um número (`- [ ] 6 camisetas...`)
ou termina com `— 5` ganha sozinho um contador `−  faltam 4  +`. Clicar no `+`/`−` anda de um em um; clicar
no corpo da linha vai direto para "tenho tudo" ou "não tenho nada". Enquanto está no meio, o item fica
âmbar. A contagem do topo é **por peça**, não por linha: 6 camisetas contam como 6.

**A lista vai encurtando.** Item completo sai de vista; se a seção inteira ficou pronta, o título dela sai
junto. Enquanto ainda faltam peças o item continua na lista, mostrando quantas faltam. O botão
**Mostrar N já prontos** traz tudo de volta (é assim que se desfaz um engano).

Cada aba mostra no topo quanto já foi marcado e tem um botão "Limpar marcações". O texto continua
vindo do .md — se eu editar o texto de um item, aquele item volta a ficar desmarcado.

**Sincronização entre aparelhos: ligada.** As marcações sobem para o Supabase (tabela `cao_ticados`)
junto com as tarefas, valendo sempre a alteração mais recente. Em cada aparelho novo, entrar uma vez em
**Tarefas → Entrar**. Sem internet continua funcionando e sobe quando a conexão voltar.

A própria barra de progresso mostra o estado: **Salvo na nuvem** (verde), *Salvando...*, **Sem conexão**
(âmbar), **Sessão expirada** (vermelho) ou **Somente neste aparelho** quando não está logado.

### Aba Tarefas (cadastro)
Dá para cadastrar tarefa direto no painel, escrevendo em linguagem normal: *"entregar artigo sexta"*,
*"prova dia 15"*, *"enviar ofício amanhã"*. Ele entende a data sozinho e agrupa por urgência
(atrasadas, hoje, amanhã, próximos 7 dias). Categorias: Curso, Dissertação, Administrativo, Pessoal.

**Sincronização entre aparelhos: ligada.** As tarefas sincronizam pelo Supabase (projeto
`relatorio-ronda`, tabela `cao_tarefas`). Em cada aparelho novo, entrar uma vez em
**Tarefas → Entrar** com o e-mail e senha de sempre. Detalhes em [SUPABASE.md](SUPABASE.md).

**Mesmo assim, use o Exportar de vez em quando.** Ele gera o [TAREFAS.md](TAREFAS.md) pronto para
colar, e é o que coloca as tarefas dentro do repositório para eu enxergar o histórico nas próximas
sessões. Sem internet, o painel continua funcionando e sobe as alterações quando a conexão voltar.

## Estrutura da pasta
```
Central CAO/
├── STATUS.md        <- este arquivo (painel)
├── PRAZOS.md         <- calendário/prazos vivos
├── CONTATOS.md       <- organograma do CAES e contatos por assunto
├── ROTINA.md         <- regras do dia a dia (uniforme, SIPA, formatura, facilities)
├── DUVIDAS.md        <- dúvidas em aberto sobre o curso
├── TAREFAS.md        <- lista de tarefas correntes
├── ANOTACOES.md      <- notas soltas, recados, ideias
├── CONFERIR.md       <- conferência de armário: tico o que já tenho
├── COMPRAS.md        <- o que sobrou da conferência e precisa comprar
├── MALA.md           <- lista do dia de arrumar a mala (o que levar)
├── VIAGENS.md         <- deslocamentos (módulos presenciais, provas etc.)
├── SUPABASE.md       <- como ligar a sincronização das tarefas
├── gerar_painel.py   <- gera o painel a partir dos .md acima
├── docs/index.html   <- o painel (gerado; é o que vai para o GitHub Pages)
└── CAO 2026/
    ├── Inscrição/    <- documentos da fase de seleção (arquivo morto)
    ├── PP/            <- Projeto de Pesquisa / Monografia
    ├── Curso/         <- material do curso em andamento (avisos SAE, módulos)
    └── Estudo/
        ├── Curso Nakaharada CAO 2024/                       <- curso pago, material atual
        └── Material de Ciclos Anteriores (CAO 2021)/         <- referência de edital anterior
```

## Regras desta pasta
- **Os .md são a fonte de verdade.** O painel HTML é só o visor; nunca edite `docs/index.html` à mão, porque a próxima geração sobrescreve.
- Documentos pesados (PDF de estudo, edital, PP) ficam só aqui local + Google Drive. A pasta `CAO 2026/` inteira está no `.gitignore` e **não vai para o GitHub**.
- O que vira repositório: os .md, o `gerar_painel.py` e a pasta `docs/` (o painel publicado).
