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

**Onde se entra na conta (21/08/2026).** No **cabeçalho**, ao lado do botão de tema, em qualquer aba.
E também clicando na própria linha de estado ("Somente neste aparelho", "Salvo na nuvem"), que existe
no topo de cada lista. Antes o login vivia dentro da aba Tarefas, e não era só o botão: o modal era
gerado dentro da seção daquela aba, que fica `display:none` nas outras. Ou seja, para entrar na conta
era preciso estar em Tarefas, mesmo quando o que você queria sincronizar era a Mala. Isso era resto de
quando só as tarefas subiam para a nuvem, não uma decisão.

**Sincronização entre aparelhos: ligada.** As marcações sobem para o Supabase (tabela `cao_ticados`)
junto com as tarefas, valendo sempre a alteração mais recente. Em cada aparelho novo, entrar uma vez em
**Tarefas → Entrar**. Sem internet continua funcionando e sobe quando a conexão voltar.

**E voltam para o `.md` sozinhas (18/08/2026).** Até então a marcação subia para a nuvem e morria lá:
o `.md` continuava mostrando em aberto o que já tinha sido comprado, e alguém tinha que reconciliar na
mão, item por item. Agora o `sincroniza_ticados.py` faz a volta, de hora em hora, na mesma Action das
tarefas. **A regra de conflito é a mesma das tarefas: quem mexeu por último ganha**, comparando a coluna
`mod` da nuvem com a data do último commit que tocou aquele `.md`.

Item que a nuvem nunca viu é decidido pelo arquivo, e esse estado **sobe**. É isso que faz uma marcação
feita à mão no `.md` aparecer no celular, em vez de ficar só no arquivo.

A própria barra de progresso mostra o estado: **Salvo na nuvem** (verde), *Salvando...*, **Sem conexão**
(âmbar), **Sessão expirada** (vermelho) ou **Somente neste aparelho** quando não está logado.

**E o painel agora enxerga o que o arquivo diz (21/08/2026).** Faltava a volta mais óbvia de todas: o
que o `.md` já sabia não chegava na tela. A pintura inicial só olhava o que aquele navegador tinha
ticado, então item marcado no `COMPRAS.md` abria **desmarcado** em qualquer aparelho que ainda não o
tivesse marcado, e marcação feita no PC do trabalho não aparecia em casa nem depois de `git pull`.
Cada item passou a carregar `data-md` (o que o arquivo diz dele) e cada aba, `data-mod` (a hora do
último commit daquele `.md`). Com isso o navegador decide item a item, pela mesma regra de todo o
resto: **quem mexeu por último ganha**, e quem nunca tocou no item não tem o que defender, vale o
arquivo. A decisão usa um espelho do que o arquivo dizia na última abertura, para separar "o arquivo
mudou" de "eu mudei aqui" antes de precisar comparar horas. As tarefas ganharam a mesma
reconciliação, no mesmo dia (ver abaixo).

**A volta estava quebrada desde o primeiro dia (corrigido em 23/08/2026).** O
`sincroniza_ticados.py` procurava cada caixinha na nuvem pela chave `2de055d428` (só o md5 do
texto), mas o painel grava `ab-compras/2de055d428` — o id da aba na frente. As duas pontas nunca
se encontravam. Como o script trata "não achei na nuvem" como *"a nuvem nunca viu este item"*, o
resultado era mudo e parecia certo: **o arquivo vencia sempre**, o tique feito no celular nunca
voltava para o `.md`, e a cada rodada o script ainda semeava na tabela uma segunda família de
linhas, só com o md5, que nenhum painel lê. Ou seja, a volta que o script existe para fazer nunca
aconteceu: as 93 chaves batem agora, batiam 0 antes. As linhas velhas ficam onde estão, sem
atrapalhar — o script passou a contá-las à parte no relatório, e apagar linha de banco é decisão
do Josemar, não de um robô que roda de hora em hora.

**Na primeira rodada depois do conserto pode sair um diff grande** nos `.md` com caixinha, com o
acumulado de tudo que foi ticado no painel e nunca desceu. É o esperado. Para olhar antes, a
Action aceita ser disparada à mão com a opção **"Só mostrar o que faria"** (`--conferir`).

### Seção recolhida (`<!-- extra -->`)

Uma aba tem duas naturezas de conteúdo: **o que eu tenho que fazer** e **o que eu preciso
consultar**. Misturar as duas afoga a primeira, que é o motivo de o painel existir.

Para recolher uma seção, escreva `<!-- extra -->` na linha logo abaixo do título `##`:

```
## Estoque do armário — reponha quando acabar
<!-- extra -->

Isto mora lá e não viaja...
```

Aquele título vira uma barra clicável, fechada quando a aba abre, e a seção inteira (até o
próximo `##`) fica dentro dela. É comentário de HTML, então em qualquer outro leitor de markdown
ele é invisível e o texto continua no lugar.

**A busca enxerga o que está recolhido.** Procurar "papel higiênico" abre sozinha a seção que tem
a resposta, realça o trecho e conta na pílula da aba. Ao limpar a busca, tudo se fecha de novo.

Regra de bolso: **caixinha é ação, seção recolhida é consulta.** Se você não faz nada com aquilo
nesta semana, ou é `<!-- extra -->` ou é assunto de outro arquivo.

### Aba Tarefas (cadastro)
Dá para cadastrar tarefa direto no painel, escrevendo em linguagem normal: *"entregar artigo sexta"*,
*"prova dia 15"*, *"enviar ofício amanhã"*. Ele entende a data sozinho e agrupa por urgência
(atrasadas, hoje, amanhã, próximos 7 dias). Categorias: Curso, Dissertação, Administrativo, Pessoal.

### Tarefa que se repete (22/08/2026)

O rodízio da mala é a mesma coisa toda semana: quinta de manhã separa o que volta para casa,
domingo arruma o que sobe. Antes disso, a tarefa vencia e ficava vermelha até alguém remarcar
na mão.

**Como escrever.** No `TAREFAS.md`, a marca vai no texto: `@semanal`, `@quinzenal` ou
`@mensal`. Quem diz o dia é a data da tarefa, não a marca: `@semanal` numa quinta significa
toda quinta. No painel dá para escrever direto *"toda quinta separar a roupa"*, *"todo domingo
arrumar a mala"* ou *"todo mês pagar a mensalidade"*, que ele monta a data e a marca sozinho.

**O que acontece ao ticar.** Ela **não vai para Concluídas**. Some da lista, volta com a data
da próxima vez e aparece um recado: *"Feita desta vez. Volta na quinta, 03/09."* É de propósito:
ir para Concluídas somaria uma linha por semana no arquivo e tiraria da lista justamente o
lembrete que ela existe para dar.

**A data nova é ancorada na anterior, não em hoje.** Somar 7 dias a partir de hoje jogaria a
quinta para uma terça na primeira vez que você ticasse fora do dia. Se você pulou uma semana,
ele avança de 7 em 7 até passar de hoje, e o dia da semana se mantém.

**A etiqueta "toda quinta" é um botão**: clicada, desliga a repetição e a tarefa vira comum,
na data em que já estava. Clicada de novo, volta a repetir toda semana.

**Por que a marca fica no texto e não numa coluna nova.** A tarefa passa por três lugares: a
linha do `TAREFAS.md`, a coluna `txt` do Supabase e a Action que sincroniza os dois. Estando
dentro do texto, a recorrência atravessa os três de graça, sem migração no banco e sem mexer
no `sincroniza_tarefas.py`. Quem esconde a marca na tela é o painel; o arquivo e a nuvem nunca
precisam saber que ela existe.

### Lista de conferência dentro de uma tarefa (23/08/2026)

Arrumar a mala é **uma** tarefa, ticada uma vez por semana, mas por dentro ela é uma lista:
shampoo é um clique, energético é outro. Até 22/08/2026 isso eram duas tarefas, uma com a
lista inteira espremida numa linha só e outra recorrente com metade dos itens. Ninguém tica
meia tarefa: ou ficava aberta a semana toda, ou era ticada com peça faltando.

**Como escrever.** No `TAREFAS.md`, caixinha **indentada** logo abaixo de uma tarefa não é
tarefa nova, é item dela:

```
- [ ] Domingo, arrumar a mala da semana antes de viajar @semanal [23/08/2026] #pessoal
  - [ ] 5 cuecas
  - [ ] shampoo
```

**Na tela.** A tarefa continua sendo uma linha só, com uma etiqueta **"3 de 15"** ao lado da
data. A etiqueta é um botão que abre e fecha a lista, e fica verde quando tudo foi separado.
Cada item é um clique, a linha inteira é o alvo — igual às caixinhas das abas Compras e Mala.
A lista já abre aberta no que é para hoje ou está atrasado, e fechada no resto; clicou na
etiqueta, a sua escolha manda daí em diante. Ticar um item **não redesenha a aba**: são 15
cliques seguidos, e refazer a lista a cada um fazia a tela piscar e perdia a rolagem no celular.

**Onde mora o tique de cada item — não na tarefa.** Ele vai para o mesmo lugar das caixinhas
das outras abas (tabela `cao_ticados`), com a chave `tf/<id da tarefa>/<chave do item>`. Dois
motivos, e o primeiro não tem volta:

1. o id de uma tarefa nascida no arquivo é derivado do **texto** dela (`idBase`). Se o tique
   morasse no texto, cada clique geraria um id novo e arquivo, nuvem e painel parariam de se
   reconhecer — exatamente a duplicata em massa de 12/08/2026;
2. de graça vem a sincronização entre aparelhos, que a tabela de ticados já faz desde
   21/08/2026: separou o shampoo pelo celular, o PC mostra separado.

**No arquivo o item fica sempre `- [ ]`.** Ali a lista é o molde da semana, não o diário de
bordo. Quem guarda o que já foi separado é o navegador mais a nuvem. Por isso o `linha()` do
`sincroniza_tarefas.py` e o Exportar do painel devolvem os itens sempre em aberto — mas
devolvem: sem essa parte, a primeira reescrita do arquivo apagaria a lista inteira em silêncio,
que foi o que aconteceu com as notas de seção em 20/08/2026.

**Tarefa que se repete zera a própria lista** quando rola para a semana seguinte, e o recado
avisa: *"Feita desta vez. Volta no domingo, 30/08, com a lista zerada."* Sem isso ela voltaria
toda ticada e não serviria para nada.

**A lista é do arquivo.** O painel tica, mas não cria nem apaga item, então não há conflito a
resolver: a cada abertura ela é recopiada do `TAREFAS.md` por cima. Corrigir uma palavra no
arquivo chega ao painel na carga seguinte, sem exportar nada. Mudar o texto de um item zera o
tique dele, como já acontece nas outras abas.

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

### O aviso de "ainda não foi para o TAREFAS.md" foi removido (23/08/2026)

Não existe mais tarja âmbar no topo da aba Tarefas, nem a contagem de divergências que a
alimentava.

**Ela nasceu certa e envelheceu errada.** Em 12/08, levar o painel para o arquivo era trabalho
do Josemar: copiar do Exportar e colar no `.md`. A pendência era dele, e a tarja era o lembrete.
Em 14/08 a Action passou a fechar o ciclo sozinha, de hora em hora, e a tarja virou o retrato de
uma fila que não é mais de ninguém. Bastava **ticar uma tarefa** para ela subir na tela dizendo
*"1 tarefa alterada ainda não foi para o TAREFAS.md"* e, no parágrafo seguinte, *"não precisa
fazer nada"*. Alarme que ele mesmo desmente não é informação, é barulho — e barulho com cara de
pendência cobra quem lê. Foi assim que o Josemar pediu para tirar: *"odeio ele, fico angustiado
em saber que tem pendência"*.

**Não entrou um aviso menor no lugar, de propósito.** O que sobrou já diz tudo sem cobrar: a
**linha de estado** do topo ("Salvo na nuvem", "Sem conexão", "Somente neste aparelho") mostra o
único ponto onde ainda pode haver algo preso naquele aparelho, e o botão **Exportar** continua ao
lado como saída de emergência. Depois que a alteração chega à nuvem, levá-la ao arquivo é serviço
de robô, e robô não precisa de tarja.

**Se um dia for preciso saber se o arquivo está velho**, a conta é comparar as tarefas do painel
com a `BASE` (o que o `TAREFAS.md` dizia quando o painel foi gerado). Era isso que a função
`divergencias()` fazia, e a explicação ficou registrada no código, para não ser reinventada do
zero — não para voltar à tela.

**Uma limitação daquela época, resolvida em 14/08/2026 e que continua valendo:** excluir no
painel uma tarefa que veio do `.md` não grudava, ela voltava do arquivo ao recarregar. A Action
tira a linha do `TAREFAS.md` na rodada seguinte, então a exclusão gruda sozinha (ver abaixo).

### O painel lê o arquivo de volta (21/08/2026)

O painel sempre soube trazer tarefa **nova** do `TAREFAS.md` e tirar a que **sumiu** dele. Faltava o
meio: a tarefa que existe nos dois lados com valores diferentes ficava congelada no que aquele
aparelho tinha gravado. Remarcar uma data no PC do trabalho, deixar isso chegar ao `TAREFAS.md` e
abrir o painel em casa mostrava a data velha, para sempre — mesmo depois de `git pull`. Era o mesmo
buraco das caixinhas, e os dois foram fechados juntos.

A decisão não é chute. O painel guarda um **espelho** do que o arquivo dizia na última vez que abriu,
e com ele separa três casos:

| Situação | Quem vence |
|---|---|
| O arquivo mudou, aqui não | o arquivo |
| Mudei aqui, o arquivo não | o meu (edição ainda não exportada) |
| Os dois mudaram | quem mexeu por último: hora do commit do `.md` contra o `mod` da tarefa |

Na primeira abertura ainda não existe espelho, então vale direto a regra de quem mexeu por último —
a mesma do `sincroniza_tarefas.py`. É isso que faz a correção valer já na primeira vez sem descartar
o que foi mexido no aparelho depois do último commit.

Quando o arquivo vence, a tarefa fica com `sinc: true` e `mod` igual à hora do commit: ela **não**
volta a subir para a nuvem. Reenviar faria o `mod` da nuvem regredir para uma hora antiga, e a rodada
seguinte da Action desfaria a mudança.

**A hora do commit vem do `git log` de cada `.md`**, embutida no painel pelo `hora_do_md()`. Por isso
o `publicar-painel.yml` precisa de `fetch-depth: 0`: com o checkout raso o `git log` do arquivo vem
vazio, a hora cairia na mtime do checkout (sempre "agora") e o arquivo passaria a ganhar de tudo.

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

### O ciclo se fecha sozinho (14/08/2026)

**Não precisa mais copiar e colar.** Uma Action agendada
([sincronizar-tarefas.yml](.github/workflows/sincronizar-tarefas.yml)) roda de hora em hora,
lê a `cao_tarefas` no Supabase e reescreve o [TAREFAS.md](TAREFAS.md) sozinho, preservando
cabeçalho e seções. Depois pede a republicação do painel. Você mexe no celular e o
repositório se atualiza sem você fazer nada. Editar o `.md` na mão também dispara a rodada
na hora, sem esperar a hora cheia.

Por que a Action e não o próprio painel: o painel é página estática no GitHub Pages, não tem
servidor e não pode escrever no repositório. A credencial de escrita não pode morar dentro
dele porque o repositório é público. Na Action ela fica nos Secrets.

**Quem manda quando arquivo e nuvem discordam: quem mexeu por último.** A hora da nuvem é a
coluna `mod`; a hora do arquivo é a data do último commit que tocou o `TAREFAS.md`. Sem essa
regra, a Action comeria na rodada seguinte qualquer edição feita à mão no arquivo.

**Como ela sabe que uma tarefa foi apagada no painel:** o `estado_tarefas.json` guarda os ids
da última sincronização. Tarefa que está no arquivo, sumiu da nuvem e estava no estado
anterior foi apagada no painel, então sai do arquivo. Sem esse registro, "sumiu da nuvem" e
"ainda não subiu" seriam a mesma coisa e a tarefa apagada voltaria a cada hora. **É isto que
conserta a limitação antiga** de excluir no painel não grudar. Não apague esse arquivo.

Na primeira rodada não existe estado anterior, então nada é apagado: ela só sobe.

Para conferir sem escrever nada, rode a Action pela aba Actions marcando a opção
"Só mostrar o que faria", ou local: `python sincroniza_tarefas.py --conferir`.

**O Exportar continua existindo como saída de emergência.** Ele gera o
[TAREFAS.md](TAREFAS.md) pronto para colar, no mesmo formato que a Action escreve, para o
caso de a automação estar fora do ar.

### Quando o clique vira nuvem, e quando o outro aparelho vê (23/08/2026)

Pergunta do Josemar: *"se eu clicar numa tarefa e desligar o PC, ela vai estar sincronizada
quando eu religar em outro aparelho?"*. A resposta estava certa no código, mas faltava a
confirmação na tela e faltava um caminho.

**A tarefa sobe no instante do clique.** Sem fila e sem espera: `alternar()` grava no navegador
e dispara o envio no mesmo instante. Medido com um Supabase de mentira: **10 ms** entre o
clique e o POST. Enquanto o envio não volta, a tarefa mostra um pontinho ao lado da data.

**Os itens da lista de conferência esperam 1,2 s.** É a mesma pausa das caixinhas das outras
abas, e existe porque são 15 cliques em sequência: ele aguarda o dedo parar e manda tudo de uma
vez, em vez de 15 requisições. Medido: **1,23 s** entre o último clique e o POST.

**O que faltava (1): confirmação na tela.** A linha de estado da aba Tarefas só ouvia o canal
das *tarefas*. O tique de um item da lista é guardado como *caixinha*, então ticar os 15 itens
da mala e desligar o PC não dava nenhum sinal de que aquilo tinha subido. Agora a linha da aba
Tarefas ouve os dois canais, e os dois passaram a falar a mesma língua — "Salvando...", "Salvo
na nuvem", "Sem conexão". Ter dois nomes para o mesmo estado ("Sincronizado" de um lado, "Salvo
na nuvem" do outro) só faria a linha trocar de palavra sozinha na frente de quem lê.

**O que faltava (2): a aba já aberta não se atualizava.** O painel buscava a nuvem só quando a
*página* abria. Aba deixada aberta no celular desde ontem mostrava o estado velho até alguém
recarregar na mão — e ninguém recarrega uma aba que já está na tela. Agora, ao voltar para a
aba, ele busca de novo, com duas travas:

- **30 segundos** entre uma busca e outra, senão cada alt-tab viraria uma requisição;
- **nada acontece com uma edição aberta.** Sincronizar redesenha a lista inteira, e redesenhar
  por baixo de um campo de texto aberto apagaria o que estava sendo digitado. Quem sai para
  copiar um dado e volta para colar não pode perder a frase no caminho.

**Se faltar internet, não se perde, mas também não vai sozinho.** Fica guardado naquele
aparelho com o pontinho aceso, e sobe quando a rede voltar (se a página continuar aberta) ou na
próxima vez que o painel for aberto ali. Ou seja: cair a rede, ticar e desligar significa que
aquilo só chega ao celular quando aquele PC for religado com o painel aberto.

**E se não estiver logado, nada disso acontece:** a linha diz "Somente neste aparelho" e é
clicável para entrar. Sem conta, o Exportar é o que garante que nada se perca.

### A tarja vermelha de contagem presa (27/08/2026)

A linha de estado do topo é discreta de propósito, e num aparelho novo ela é discreta demais.
O caso concreto: o Josemar contou o armário no celular, dentro do CAES, e domingo ia arrumar a
mala olhando o painel no notebook de casa, que nunca entrou na conta. O notebook mostraria a
lista zerada, como se faltasse tudo, sem nada na tela dizendo por quê.

Agora existe uma **tarja vermelha grande no topo de qualquer aba**, com botão **Entrar**, que
abre o mesmo modal de conta.

**Ela só acende quando as duas coisas são verdade ao mesmo tempo:** não há sessão neste
navegador **e** existe marcação feita aqui que nunca subiu (`n > 0` e `s !== true` em
`cao-ticados`). Aparelho novo com painel zerado não vê nada; aparelho já logado nunca vê. Ela
se apaga sozinha assim que o login sobe as marcações.

**Por que esta pode ser vermelha e a âmbar de 12/08 não podia** (acima, "O aviso de ainda não
foi para o TAREFAS.md"): aquela anunciava uma fila que um robô já esvaziava, e se desmentia no
parágrafo seguinte. Esta anuncia uma pendência real, que **só o Josemar resolve**, com um
clique, e some no instante em que ele clica. Alarme que some quando resolvido é informação;
alarme que fica é barulho.

### O inventário de quinta vira a mala de domingo (23/08/2026)

A carga do domingo deixou de ser lista fixa. Ela é **calculada**, e quem calcula é o contador que
as caixinhas já tinham desde o começo.

**Como funciona.** Na aba Mala, cada peça de roupa é um item com quantidade (`- [ ] 8 cuecas`), e o
número é o **alvo no armário**, não o que ele tem. Quinta de manhã, antes de descer, ele abre o
armário e põe no contador **quantas peças limpas ficaram lá**. O painel mostra o que falta para
fechar o alvo, e esse "faltam N" é exatamente a carga do domingo: contador dizendo *faltam 5
cuecas* significa cinco cuecas na mala.

**Por que isso resolve a reclamação dele** (*"tem coisa que eu já tiquei e já está no CAES, não tem
que ficar aparecendo todo domingo"*): item que fecha o alvo **some da lista sozinho**, porque a aba
esconde o que está pronto. Só continua na tela o que precisa dele. No domingo, ao chegar e guardar
a roupa nova, ele clica no meio de cada linha, que marca "tenho tudo" e deixa a conta da quinta
seguinte começar limpa.

**Nenhuma linha de código foi escrita para isso.** O stepper, a contagem por peça e o esconder o
que está pronto existem desde as abas Compras e Mala. O que faltava era usar o número como *alvo* e
não como *quantidade a levar*, e dizer isso em uma frase dentro do arquivo.

**As duas tarefas do rodízio foram religadas ao ciclo.** A de quinta ganhou o inventário como
primeiro passo, antes da roupa suja; a de domingo perdeu os números fixos ("5 cuecas" virou "cuecas,
na quantidade que o inventário de quinta apontou"). Sem isso, o painel teria duas fontes brigando
para dizer quanta cueca vai na mala.

**A mala de domingo passou a aparecer escrita (27/08/2026).** Até aqui ela existia só como leitura
do "faltam N", linha por linha, na seção 1. Funcionava, mas obrigava a fazer a conta com o olho
enquanto enchia a sacola. Agora a seção 3 mostra a lista pronta, em fichas: *3 cuecas*, *1 par de
meia social preta*, *2 camisetas de serviço*.

**Continua não sendo uma segunda lista.** Não há nada novo para manter, nem no arquivo nem no
banco: o bloco é montado no navegador a cada clique no contador e a cada chegada da nuvem. Se o
inventário fecha completo, ele diz *"nada de roupa para levar"* e pronto. É a mesma regra de sempre,
só que dita em voz alta em vez de deduzida.

**Como se liga no `.md`.** Dois comentários HTML, invisíveis em qualquer outro leitor de markdown:
`<!-- inventario -->` marca a lista que o painel lê, `<!-- mala-domingo -->` marca onde a mala
aparece. Nada de achar a lista "pela posição", que quebraria no dia em que alguém reordenasse a aba.

**Dois cuidados que o bloco toma.** Quando falta uma peça só, o nome vai para o singular (*1 toalha
de banho*, não *1 toalhas*; *1 par*, não *1 pares*), porque essa lista é lida de relance. E quando
nada foi contado ainda, ele mostra o jogo inteiro **com um aviso**: sem isso, o painel pareceria ter
calculado uma mala que na verdade é só o alvo de todas as peças.

**A ficha virou clique, e o clique fecha o ciclo (27/08/2026).** Clicar numa ficha é dizer "esta já
está dentro da mala". Ela fica marcada, riscada, e **a linha dela no inventário de quinta volta a
zero**, já pronta para a contagem da semana seguinte. Clicar de novo desfaz tudo, inclusive o
inventário, que volta exatamente para onde estava: erro de dedo não pode custar a contagem inteira.

Com isso a instrução antiga saiu do `MALA.md`. Ela mandava, no domingo, *"voltar à seção 1 e clicar
no meio de cada linha"*, que marcava a peça como **completa** no armário. Fazia sentido antes de a
mala existir escrita; agora seriam dois caminhos para a mesma coisa, apontando para lados opostos.

**Onde isso fica guardado, e por que não numa tabela nova.** Guardar a peça **zera** a linha do
inventário, então uma lista que só calculasse "alvo menos o que há no armário" mandaria a peça de
volta para a mala no instante seguinte. Ela precisa de memória própria: a **quantidade** que foi
para a mala, gravada na mesma tabela `cao_ticados`, com o prefixo `md/` na chave, do mesmo jeito que
a aba Tarefas já usa `tf/` para os itens de conferência. De graça, isso sincroniza entre os
aparelhos junto com o resto; uma tabela nova exigiria migração no banco para meia dúzia de números.

Só a quantidade basta para desfazer: o inventário volta para *alvo menos o que foi*, que é onde
estava antes do clique. Não há segundo número guardado.

**Como a lista se renova sozinha na quinta seguinte.** Peça guardada **com o inventário já contando
de novo** (`n > 0`) é resto da semana passada, e o registro dela é apagado na hora de desenhar. Ou
seja: o primeiro clique no contador da quinta já limpa a mala do domingo anterior. Ele não precisa
lembrar de zerar nada, e não existe botão de "começar semana nova" para ele esquecer de apertar.

**A ficha guardada não some**, ao contrário de toda outra lista do painel, onde item pronto se
esconde. Aqui sumir seria o mesmo que travar: ficha escondida não dá para clicar de novo, e o
desfazer é justamente o que ele pediu ("posso errar no clique").

### A aba Mala vira o ciclo de três lugares (23/08/2026)

O inventário já calculava a mala de domingo (seção acima), mas ele estava afogado. A aba tinha
**60 caixinhas e 94 peças** no contador, e só 30 dessas peças eram do rodízio semanal. As outras
64 eram a conferência de armário concluída em 06/08 (cama, higiene, limpeza, copa, estudo,
documentos) e a doutrina de uniforme do R-5. Toda semana o painel cobrava tudo isso de novo, e o
cartão da abertura mostrava um número que não queria dizer nada.

**A aba passou a ser o ciclo dele**, na ordem em que a semana acontece: quinta conta o armário,
quinta desce o que vai lavar, domingo sobe o que faltou. Só essas três listas continuam ticáveis,
e o contador caiu para **30 peças**, que é exatamente o rodízio. O resto virou texto de consulta:
o estoque do armário é *"a memória do que tem, para reconhecer o que acabou"*, e o que faltar vira
item em `COMPRAS.md`, que é quem cobra compra.

**A doutrina de uniforme saiu daqui e foi para o `ROTINA.md`.** Os dois arquivos descreviam P-1,
B-1, S-1 e agasalho, cada um mandando ler o outro. Agora `ROTINA.md` é dono de *qual uniforme em
qual ocasião e o que vai montado em cada peça* (a tabela de insígnias foi junto), e `MALA.md`
guarda só *quantas peças e onde elas estão*. É a regra de fonte única do `AGENTS.md`, aplicada ao
assunto que mais tinha cópia no repositório.

**Um erro de número apareceu na limpeza:** o inventário pedia **4 camisas de passeio**, mas o jogo
é de **3** (a antiga mais as 2 da ConfecBell, como o próprio `COMPRAS.md` registra, e como a seção
do P-1 dizia três linhas abaixo). O painel ia cobrar para sempre uma camisa que não existe. Alvo
corrigido para 3. Duplicata não confunde só a leitura: ela inventa falta.

**Segundo passo, no mesmo dia: o que sobrou foi recolhido.** Enxugar não bastou. Ao ver a aba
pronta, o Josemar apontou que a referência ainda estava em primeiro plano: *"isso tudo tem que
ficar escondido numa aba, informações extras, não em primeiro plano na mala"*. A aba agora abre
com **três listas e mais nada** (contar o armário, o que desce para lavar, o que sobe domingo), e
as seis seções de consulta viraram barras recolhidas no fim: como o ciclo funciona, de onde vêm os
alvos, o que não entra no rodízio, a farda do armário, o estoque e os detalhes de viagem. A aba
inteira cabe em uma tela. Foi para isso que o gerador ganhou o `<!-- extra -->`, documentado mais
acima, que agora serve qualquer aba.

**O cartão da Mala na abertura ganhou rótulo próprio** (`data-sub-falta` / `data-sub-ok`). Dizer
"12 itens ainda faltam" soava a pendência atrasada; agora diz **"12 peças na mala de domingo"**,
que é o que o número significa. Sem rótulo, o cartão continua com o texto genérico das listas a
zerar, como o de Compras.

### Item de lista quebrado em duas linhas (23/08/2026)

Quebrar a linha no meio de um item de lista é coisa que qualquer um faz ao escrever, e o gerador
não aguentava: a segunda linha virava parágrafo solto, fora da bolinha. Pior, um negrito aberto na
primeira linha e fechado na segunda aparecia com os asteriscos na cara, porque a formatação inline
roda por linha. Foi assim que o `**Mestrado Profissional em Ciências Policiais...**` apareceu cru
na primeira tela do painel. Agora o gerador junta a continuação ao item, como manda o markdown.

**Duas armadilhas dentro do conserto**, as duas encontradas ao conferir e não ao escrever:

1. **A chave da caixinha continua saindo só da primeira linha.** A identidade de um item ticável é
   o md5 do texto dele, e o `sincroniza_ticados.py` lê o arquivo linha a linha. Se a chave passasse
   a incluir a continuação, as duas pontas parariam de se reconhecer e o tique voltaria a não
   descer para o `.md` — exatamente o erro de 18/08, consertado horas antes. A contagem caiu de
   81 para 76 chaves batendo e denunciou na hora.
2. **Linha que começa em negrito não é marcador de lista.** O teste inicial cortava a continuação
   sempre que ela começava com `*`, e `**Júlio Prestes** (CPTM, na praça)` saía partido. Agora só
   marcador de verdade (`- `, `* `, `1. `, `#`, `>`, `|`) interrompe a junção.

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

**A ordem no arquivo é sempre pela data da tarefa, nunca pela hora da nuvem.** Vale para as
Pendentes e para as Concluídas, e o `sincroniza_tarefas.py` usa o mesmo critério. Se os dois
divergissem, cada um reordenaria o bloco por cima do outro e o `TAREFAS.md` geraria commit
sem nada ter mudado. Foi o que o modo conferência pegou em 14/08 antes de virar commit: as
24 tarefas antigas subiram todas juntas na primeira carga, então a hora da nuvem delas virou
o horário daquela carga, e as concluídas de 04/08 iam parar em cima das de 14/08. Na tela a
aba continua mostrando as concluídas pela ordem em que foram mexidas, que é o útil ali.

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
├── MALA.md           <- rodízio semanal: armário do CAES, roupa para lavar, mala de domingo
├── VIAGENS.md         <- deslocamentos (módulos presenciais, provas etc.)
├── PASSEIOS.md        <- guia turístico/gastronômico para a janela livre da semana
├── SUPABASE.md       <- como ligar a sincronização das tarefas
├── gerar_painel.py   <- gera o painel a partir dos .md acima
├── sincroniza_tarefas.py  <- traz as tarefas da nuvem de volta para o TAREFAS.md
├── estado_tarefas.json    <- ids da última sincronização (não apagar)
├── docs/index.html   <- o painel (gerado; é o que vai para o GitHub Pages)
└── CAO 2026/
    ├── Inscrição/    <- documentos da fase de seleção (arquivo morto)
    ├── PP/            <- Projeto de Pesquisa / Monografia
    ├── Curso/         <- material do curso em andamento (avisos SAE, módulos)
    └── Estudo/
        ├── Curso Nakaharada CAO 2024/                       <- curso pago, material atual
        └── Material de Ciclos Anteriores (CAO 2021)/         <- referência de edital anterior
```

