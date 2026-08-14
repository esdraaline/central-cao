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

### Guia do dia (a abertura)
A primeira coisa da aba Painel é o cartão que responde "o que eu faço hoje": saudação,
data por extenso, em que ponto da semana do curso você está e a contagem para o próximo
marco. Abaixo dele, as tarefas separadas em **Atrasado**, **Hoje você precisa**, **Amanhã**
e **Ainda esta semana** (esta semana é até o domingo seguinte, não "próximos 7 dias").

A fase da semana é calculada, não escrita: antes de 16/08 o marco é a primeira viagem;
depois disso a semana se repete sozinha (domingo viaja, segunda a quinta é aula, quinta
volta às 11h30, sexta e sábado em casa). Vale até agosto de 2027 sem ninguém mexer.

**Tarefa sem data não entra no guia.** Ela continua na aba Tarefas e o guia avisa quantas
estão assim. Para ser cobrado no dia certo, a tarefa precisa de `[dd/mm/aaaa]` no
[TAREFAS.md](TAREFAS.md) ou de data no cadastro do painel.

**Todo cálculo de tempo é feito no navegador, de propósito.** O painel publicado só é
regerado quando algum `.md` muda; contador calculado na hora da geração envelhece em
silêncio. Foi o que aconteceu entre 08/08 e 11/08, quando o cartão insistia em "9 dias
para o início" com 6 dias restantes. Se um dia for preciso mexer nisso, o código está no
bloco `JS_GUIA` do `gerar_painel.py`, e dá para conferir o texto de qualquer dia sem
esperar a data chegar: abra o console e rode `GUIA.marco(new Date(2026,7,19))`.

Os cartões **Compras** e **Mala** mostram quantos itens ainda faltam, lendo as marcações
das próprias abas (contando por peça: "6 camisetas" conta 6, não 1).

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

### Remarcar uma tarefa (mudar a data)
Toda tarefa tem **botão de calendário** ao lado do lápis, e **a própria etiqueta de data é
clicável**. Abre um campo de data com atalhos: **Hoje**, **Amanhã**, **+1 semana**,
**Sem data** (só aparece se a tarefa tiver data) e **Cancelar**. Confirmou, a tarefa pula
sozinha para o grupo certo e o guia do dia lá em cima se refaz na hora, sem recarregar.

Sai também por **Enter** (confirma) e **Esc** (cancela). Não confirma ao perder o foco de
propósito: no celular, abrir o seletor de data tira o foco do campo, e confirmar no blur
mataria a edição justamente no aparelho onde ela mais é usada.

**A data nova fica só no painel até você exportar.** O `TAREFAS.md` continua com a data
antiga, e isso é o desenho de sempre: o painel lê do arquivo, mas quem escreve de volta é o
botão **Exportar**. A mescla é por texto da tarefa, então o `.md` com a data velha **não**
sobrescreve o que você remarcou (testado: remarcada para 19/08 com o `.md` dizendo 11/08,
sobreviveu ao recarregamento).

### O aviso de "ainda não foi para o TAREFAS.md"
A tarja âmbar no topo da aba compara, item a item, o que está no painel com o que o
`TAREFAS.md` diz, e conta quatro tipos: **nova**, **remarcada** (mudou a data), **alterada**
(mudou categoria ou o feito/não feito) e **excluída aqui**. Sem divergência, ela não aparece.

**Ela olha o arquivo, não a nuvem.** Antes essa mesma tarja contava a flag do Supabase, e
mentia dos dois lados: sumia quando a tarefa subia para a nuvem, mesmo sem nunca ter ido para
o `.md`, e ficava acesa para sempre em aparelho sem login. Quem informa o estado da nuvem é a
linha de status ("Salvo na nuvem", "Sem conexão"); a tarja é só sobre o arquivo do
repositório. Corrigido em 12/08/2026.

**A tarja não apaga ao exportar, e isso é de propósito.** Ela compara com o arquivo que
estava no repositório na hora em que o painel foi gerado. Só some depois que o `TAREFAS.md`
novo subir e o painel for regerado. Copiar o texto e não colar não conta.

**Limitação conhecida:** excluir no painel uma tarefa que veio do `.md` não gruda. A tarja
acusa a exclusão, mas ao recarregar a tarefa volta do arquivo e o aviso some junto, porque a
mescla traz de volta tudo que está no `.md` e não está aqui. Enquanto isso não mudar, para
apagar de vez é preciso tirar a linha do `TAREFAS.md`.

### Quem manda em cada tarefa (corrigido em 12/08/2026)
Tarefa que **nasceu no arquivo** tem id derivado do próprio texto (prefixo `md`). Tarefa criada
**no painel** tem id de sorteio (prefixo `t`). A regra passou a ser: **para o que nasceu no
arquivo, o arquivo manda**. Se a linha some do `TAREFAS.md`, ou se o texto dela é reescrito, o
registro antigo é removido do aparelho e marcado para a nuvem apagar junto. Tarefa criada no
painel nunca é removida por isso.

**O bug que isso conserta.** Antes, a mescla só somava: reescrever o texto de uma tarefa no
`.md` gerava id novo e o registro velho ficava para sempre. Como o id também é a chave no
Supabase, a duplicata subia e se espalhava para todos os aparelhos. Em 12/08/2026 o `.md`
tinha 21 pendentes e a aba mostrava **38**, porque as tarefas foram reescritas várias vezes no
mesmo dia. Ao abrir o painel atualizado, a limpeza é automática: não precisa apagar nada à mão.

**O preço:** se você remarcar uma data no painel e depois o texto daquela tarefa for reescrito
no `.md`, a remarcação se perde junto com o registro antigo. É a mesma regra que já valia para
as caixinhas das outras abas, onde editar o texto do item zera a marcação.

**Sincronização entre aparelhos: ligada.** As tarefas sincronizam pelo Supabase (projeto
`relatorio-ronda`, tabela `cao_tarefas`). Em cada aparelho novo, entrar uma vez em
**Tarefas → Entrar** com o e-mail e senha de sempre. Detalhes em [SUPABASE.md](SUPABASE.md).

**Mesmo assim, use o Exportar de vez em quando.** Ele gera o [TAREFAS.md](TAREFAS.md) pronto para
colar, e é o que coloca as tarefas dentro do repositório para eu enxergar o histórico nas próximas
sessões. Sem internet, o painel continua funcionando e sobe as alterações quando a conexão voltar.

### Dois consertos no Exportar (14/08/2026)

**Copiar zerava a fila de upload.** O botão Copiar marcava todas as tarefas como já
sincronizadas. Só que essa marca é a fila do Supabase: a sincronização sobe apenas o que
está fora dela. Exportar sem internet ou sem login jogava fora alterações que nunca tinham
subido, elas ficavam presas naquele aparelho, e se o outro aparelho mexesse na mesma tarefa
depois, a versão dele vencia. Era resto de quando exportar significava "já está no arquivo".
Agora Copiar só copia.

**O exportado achatava o arquivo.** O cabeçalho vinha de uma cópia escrita dentro do código,
que envelheceu, e as seções (`###`) sumiam. Colar por cima apagava os subtítulos e as linhas
sobre categorias e sobre a data não ser enfeite. Agora o topo vem do próprio `TAREFAS.md` e
cada tarefa volta para a seção de onde saiu; seção que ficou sem tarefa some junto. Tarefa
criada no painel não tem seção e sai solta logo abaixo de `## Pendentes`. Dentro de cada
seção a ordem passa a ser por data, que é a mesma da lista na tela.

## Estrutura da pasta
```
Central CAO/
├── STATUS.md         <- painel principal, o "onde paramos"
├── PAINEL.md         <- este arquivo (manual do painel gerado)
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

