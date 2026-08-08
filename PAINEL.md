# Painel visual e estrutura — Central do CAO

> Movido do `STATUS.md` em 08/08/2026. Manual de funcionamento do painel gerado
> (caixinhas, contadores, sincronização, aba Tarefas) e a estrutura da pasta.
> Consulta ocasional — não precisa ser lido em toda sessão.

---

## Painel visual
No ar em **https://esdraaline.github.io/central-cao** (repositório `esdraaline/central-cao`).
Também abre local com duplo clique em `docs/index.html`.
Ele é **gerado** a partir destes .md, não editado à mão. Depois de mexer em qualquer .md, rode:

```
python gerar_painel.py
```

### Caixinhas ticáveis
Nas abas geradas dos .md (Compras, Mala, Rotina), **as caixinhas são clicáveis**: clique para
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

