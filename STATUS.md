# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 23/08/2026

## 23/08/2026: auditoria do sistema — quatro defeitos achados e corrigidos

Pedido dele: *"vamos fazer uma auditoria top, monte um exército, vasculhe código a código, linha a
linha"*. O exército foi montado (7 frentes em paralelo, cada achado julgado por um adversário) e
**morreu antes de entregar**: os sete agentes bateram no limite de sessão da conta. A auditoria foi
refeita à mão, com teste executável para cada suspeita — nada aqui é opinião, tudo foi reproduzido.

**1. A linha "Salvo na nuvem" podia mentir. (o mais grave)** Quando as TAREFAS subiam mas as
MARCAÇÕES falhavam, o erro era engolido e o `pintaConta()` pintava a linha de verde assim mesmo.
Grave porque essa linha virou, em 23/08, a confirmação que ele olha antes de desligar o PC: ela
diria "salvo" com os 15 itens da mala ainda presos no navegador. Agora o estado de falha volta por
cima do verde. Reproduzido derrubando só o POST das marcações: antes dizia "Salvo na nuvem", agora
diz "Sem conexão".

**2. O lote marcava como sincronizado até o que não subiu.** Ao terminar o POST em lote, o código
fazia `sinc=true` em TODAS as tarefas. Como `sinc=false` É a fila de reenvio, uma tarefa ticada
DURANTE a requisição (ou cujo envio individual tinha acabado de falhar) era marcada como salva sem
nunca ter subido, e ninguém tentava de novo: a alteração morria calada no aparelho. Agora só quem
entrou no lote é marcado. Reproduzido com a corrida exata: lote de 3 em voo, envio individual
falhando, tarefa ticada no meio — antes era dada como salva, agora fica na fila.

**3. Emoji no texto gerava dois ids diferentes.** O `charCodeAt()` do JS anda em unidades UTF-16 e
o `ord()` do Python devolve o code point inteiro: para emoji, os dois divergiam, e a mesma linha do
`TAREFAS.md` ganhava um id no painel e outro na Action. A tarefa aparecia duplicada, o painel podava
a cópia "que sumiu do arquivo" e mandava a nuvem apagar, e só no ciclo seguinte o casamento por
texto reconciliava. Comparados os dois algoritmos com **66 textos** (todos os reais do arquivo mais
24 adversariais): 65 batiam, o do emoji não. Corrigido no Python; agora batem 66 de 66.

**4. Item indentado migrava de seção na reescrita automática.** Item de lista de conferência escrito
logo abaixo de um `###` grudava na última tarefa da seção ANTERIOR, e a Action, ao remontar o
arquivo, levava a linha junto — para outra seção. Mesma classe de erro que apagou as notas de seção
em 20/08: robô mudando conteúdo de lugar sem avisar. Corrigido: título novo zera a tarefa corrente.

**O que foi conferido e estava certo:** o `TAREFAS.md` remonta byte a byte; as 93 chaves de caixinha
batem entre robô e painel; texto com `<img onerror=...>`, `&` e aspas é escapado e não vira HTML na
tela; nenhum dos 152 itens ticáveis dos `.md` tem texto repetido (texto repetido compartilharia o
tique); as chaves `tf/` da lista de conferência sobrevivem à reconciliação e ao "Limpar marcações".

**Três coisas ficam registradas como limitação conhecida, sem conserto por enquanto:** indentar um
item com UM espaço em vez de dois faz dele uma tarefa solta (o limiar de 2 é o do markdown, e é o
lado seguro: o contrário faria uma tarefa de verdade sumir para dentro de uma lista); dois itens de
mesmo texto na mesma lista compartilhariam o tique (hoje não existe nenhum); e apagar uma tarefa
deixa as chaves `tf/` órfãs na nuvem — recriar a tarefa com o mesmo texto faz os tiques antigos
voltarem.

**Um achado de conteúdo, e este é decisão sua:** o `TAREFAS.md` manda procurar o Cel Eglis em
**24/08 (segunda)**, mas o `PRAZOS.md`, o `STATUS.md` e o `GRADE.md` dizem que a janela é **25/08
(terça), bloco 4** — é o único horário em que ele dá aula naquela semana. A remarcação em massa de
10 tarefas para segunda levou junto uma tarefa cuja data não era arbitrária. Do jeito que está, o
guia do dia vai mandar procurar o Cel num dia em que ele não está lá.

## 23/08/2026: duas frestas fechadas na sincronização

Pergunta do Josemar, depois que a tarja saiu: *"se eu clicar numa tarefa e desligar o PC, ela vai
estar sincronizada quando eu religar em outro aparelho?"*. Fui ler o caminho do clique em vez de
responder de memória, e a resposta é sim — mas apareceram duas frestas, as duas fechadas agora.

**Os números, medidos com um Supabase de mentira levantado só para isso:** a tarefa sobe **10 ms**
depois do clique, sem fila. Os itens da lista de conferência esperam **1,23 s**, que é a pausa
herdada das caixinhas: são 15 cliques em sequência, e ele aguarda o dedo parar para mandar tudo
de uma vez em vez de disparar 15 requisições.

**Fresta 1: o tique dos itens não tinha confirmação na tela.** A linha de estado da aba Tarefas
só ouvia o canal das tarefas; o tique de um item é guardado como caixinha, no outro canal. Ticar
os 15 itens da mala e desligar o PC não dava nenhum sinal de que aquilo tinha subido. Agora a
linha ouve os dois, e os dois falam a mesma língua: "Salvando...", "Salvo na nuvem", "Sem
conexão". Antes eram dois nomes para o mesmo estado, e a linha trocava de palavra sozinha.

**Fresta 2: aba já aberta não se atualizava.** O painel buscava a nuvem só quando a página abria.
Aba deixada aberta no celular desde ontem mostrava o estado velho até alguém recarregar na mão, e
ninguém recarrega uma aba que já está na tela. Agora, ao voltar para a aba, ele busca de novo —
com trava de 30 segundos entre buscas, e sem fazer nada se houver uma edição aberta, porque
sincronizar redesenha a lista e apagaria o que estava sendo digitado.

**Conferido de ponta a ponta**, com um Supabase de mentira e duas pontas simuladas: entrar na
conta, ticar tarefa, ticar itens da lista, os POSTs chegando com a chave certa
(`tf/<id da tarefa>/<item>`), a trava de 30 s segurando o segundo alt-tab, o campo de edição
aberto bloqueando a busca e o texto digitado sobrevivendo, e — a prova que interessava — a aba
já aberta pegando sozinha o que "o outro aparelho" tinha feito: a data pulou de 30/08 para 20/09
e a lista foi de 3 para 5, com shampoo e Pepsi Black chegando ticados. Nenhum erro no console.

## 23/08/2026: a tarja "ainda não foi para o TAREFAS.md" saiu da tela

Pedido do Josemar, direto: *"e esse aviso, odeio ele. Resolve esse bô de vez, eu fico angustiado
aflito em saber que tem pendência"*.

**Ele tinha razão, e não era só incômodo: a tarja estava velha.** Ela nasceu em 12/08, quando
levar o painel para o arquivo era trabalho dele — copiar do Exportar e colar no `.md`. A
pendência era de verdade e a tarja era o lembrete. Em **14/08 a Action passou a fazer isso
sozinha**, de hora em hora, e ninguém tirou o lembrete da tela. Resultado: bastava **ticar uma
tarefa** para a tarja âmbar subir dizendo *"1 tarefa alterada ainda não foi para o TAREFAS.md"*
e, no parágrafo seguinte, *"não precisa fazer nada"*. Um alarme que ele mesmo desmente não é
informação, é barulho — e barulho com cara de pendência cobra quem lê, todo dia, por uma fila
que é de robô.

**Removida a tarja e a contagem de divergências que a alimentava**, sem colocar um aviso menor no
lugar. O que sobra já diz tudo sem cobrar: a linha de estado do topo ("Salvo na nuvem", "Sem
conexão", "Somente neste aparelho") mostra o único ponto onde ainda pode haver algo preso naquele
aparelho, e o botão Exportar continua ao lado como saída de emergência. O raciocínio da conta
ficou escrito no código, para não ser reinventado do zero se um dia fizer falta.

**Conferido no navegador:** ticar tarefa, ticar a tarefa que se repete e criar tarefa nova — os
gatilhos que faziam a tarja subir — não produzem mais nada na tela, e nenhum erro no console.

## 23/08/2026: a volta das caixinhas estava quebrada desde o primeiro dia

Achado enquanto se mexia na lista de conferência, e confirmado no HTML gerado: o
`sincroniza_ticados.py` procurava cada caixinha na nuvem pela chave `2de055d428` (só o md5 do
texto do item), mas o painel grava `ab-compras/2de055d428`, com o id da aba na frente. **As duas
pontas nunca se encontraram: 0 de 93 chaves batiam.**

**O erro era mudo, e é isso que o torna grave.** O script trata "não achei na nuvem" como *"a
nuvem nunca viu este item"*, e nesse caso o arquivo manda. Então tudo parecia funcionar: a Action
rodava verde de hora em hora, dizia quantas caixinhas leu, e o `.md` nunca mudava porque o arquivo
vencia sempre. O tique feito no celular ia para a nuvem e morria lá — exatamente o problema que
esse script foi escrito para resolver em 18/08. De quebra, cada rodada semeava na tabela uma
segunda família de linhas, só com o md5, que nenhum painel lê.

**Corrigido:** a chave passou a ser montada como o painel monta, `"ab-" + id da aba + "/" + md5`.
Conferido contra o `docs/index.html` gerado: 93 de 93 chaves agora batem, nas três abas com
caixinha (Rotina 7, Compras 17, Mala 69). As linhas velhas ficam onde estão, sem atrapalhar, e o
script passou a contá-las à parte no relatório: apagar linha de banco é decisão sua, não de um robô
de hora em hora.

**Atenção na primeira rodada:** pode sair um diff grande nos `.md` com caixinha, com o acumulado
de tudo que foi ticado no painel desde 18/08 e nunca desceu. É o esperado. Para olhar antes de
deixar acontecer, dispare a Action "Sincronizar tarefas e caixinhas" à mão com a opção **"Só
mostrar o que faria"** marcada.

## 23/08/2026: a mala virou uma tarefa só, com lista de conferência por dentro

Pedido do Josemar, olhando as duas tarefas do domingo na tela: *"só uma está como recorrente,
a de cima é um complemento. Funde as duas, e cada item entra com um check list que eu vou
clicando: shampoo um item um clique, energético outro item outro clique, mas tudo dentro de
uma tarefa só"*.

**Eram duas tarefas para o mesmo domingo.** Uma recorrente com metade da carga ("2 toalhas,
fronha limpa, roupa lavada, whey e creatina") e outra de uma vez só com a lista inteira
espremida numa linha de seis linhas de tela. Ninguém tica meia tarefa: ou ela ficava aberta a
semana toda, ou era ticada com peça faltando.

**Agora é uma tarefa `@semanal` no domingo, com 15 itens indentados abaixo dela.** No arquivo,
caixinha indentada não é tarefa nova, é item da tarefa de cima. Na tela a tarefa continua sendo
uma linha só, com a etiqueta **"3 de 15"** ao lado da data — botão que abre e fecha a lista e
fica verde quando tudo foi separado.

**A decisão que sustenta o resto: o tique de cada item não mora na tarefa.** Ele vai para a
tabela de ticados (`cao_ticados`), a mesma das abas Compras e Mala, com a chave
`tf/<id da tarefa>/<chave do item>`. O id de uma tarefa nascida no arquivo é derivado do texto
dela; se o tique morasse no texto, cada clique geraria um id novo e arquivo, nuvem e painel
parariam de se reconhecer — a duplicata em massa de 12/08/2026 de novo. De quebra, a
sincronização entre aparelhos veio de graça: separou o shampoo no celular, o PC mostra separado.

**No `TAREFAS.md` o item fica sempre em aberto.** Ali a lista é o molde da semana, não o diário
de bordo. Mas ela **volta** na reescrita: o `linha()` do `sincroniza_tarefas.py` e o Exportar do
painel devolvem os itens indentados. Sem isso, a primeira rodada da Action apagaria a lista
inteira em silêncio, que foi o que aconteceu com as notas de seção em 20/08/2026. Tem teste de
ida e volta: o arquivo remonta byte a byte.

**Ticada, a tarefa rola para o domingo seguinte e zera a própria lista**, avisando *"Feita desta
vez. Volta no domingo, 30/08, com a lista zerada."* Sem zerar, ela voltaria toda ticada e não
serviria para nada.

**Conferido no navegador**, tema claro e escuro, 1280 e 390 px: 15 itens desenhados, clique
marca e desmarca, contador vira "15 de 15" em verde, ticar a tarefa rola para 30/08 e zera as 15
chaves, a lista abre e fecha pela etiqueta, o Exportar devolve os itens indentados, nenhum erro
no console e nenhum aviso falso de divergência com o arquivo. Detalhe em [PAINEL.md](PAINEL.md).

## 22/08/2026: as tarefas do rodízio da mala passaram a se repetir sozinhas

Pergunta do Josemar, olhando a tarefa da quinta vencida de novo: *"tem como cadastrar como
recorrência, toda quinta de manhã? e aquilo que coloco na mala todo domingo também"*. As duas
são rodízio semanal, e vinham envelhecendo como se fossem tarefa de uma vez só: venciam,
ficavam vermelhas no guia de abertura e alguém tinha que remarcar na mão toda semana.

**A marca de recorrência vive no texto da tarefa**, não numa coluna nova: `@semanal`,
`@quinzenal` ou `@mensal`. A escolha é o ponto do desenho. A tarefa passa por três lugares (a
linha do `TAREFAS.md`, a coluna `txt` do Supabase e a Action que sincroniza os dois), e estando
dentro do texto ela atravessa os três sem migração no banco e sem uma linha nova no
`sincroniza_tarefas.py`. Quem esconde a marca na tela e desenha a etiqueta "toda quinta" é o
painel.

**Ticada, ela não vai para Concluídas**: rola para a próxima vez e avisa *"Feita desta vez.
Volta na quinta, 03/09."* Ir para Concluídas somaria uma linha por semana no arquivo e tiraria
da lista justamente o lembrete que a tarefa existe para dar. A data nova é contada a partir da
data anterior, e não de hoje, senão a primeira vez que ele ticasse fora do dia jogaria a quinta
para uma terça.

**Conferido no navegador**, nos dois temas e nos dois tamanhos: ticar rola a data e mantém as
Concluídas em 28; a etiqueta liga e desliga a repetição; *"toda quinta"*, *"todo domingo"*,
*"toda semana"* e *"todo mês"* escritos na caixa viram tarefa com data e marca certas; o guia
de abertura e o Exportar não vazam o `@semanal` na tela; e o `TAREFAS.md` continua remontando
byte a byte pelo robô da sincronização. Detalhe em [PAINEL.md](PAINEL.md).

## 22/08/2026: o STATUS e o PRAZOS pararam no domingo da viagem

Tarefa escrita em 17/08 e vencida em 20/08: *"Atualizar STATUS.md e PRAZOS.md com a situação real
do curso (módulo, disciplinas, entregas)"*. Ela nasceu antes de o QTS sair, quando o fundo deste
arquivo ainda dizia "Módulo e disciplinas: saem no QTS de segunda, 17/08. Até lá não tem o que
preencher".

**O QTS saiu, e nada disso subiu para cá.** Entre 18 e 21/08 nasceram as 31 disciplinas, os 117
docentes, a dedução do pelotão A e as duas semanas lançadas, tudo na [Grade](GRADE.md) e em
[ESTUDOS.md](ESTUDOS.md). O fundo deste arquivo continuou dizendo que a viagem era domingo 16/08 e
que a mala precisava ser arrumada no sábado 15/08.

**Isso não é detalhe de arquivo, é a home do painel.** O `gerar_painel.py` renderiza o STATUS
inteiro na aba de abertura. O cartão "hoje no CAES", que lê a Grade, mostrava a semana certa; o
texto logo abaixo dele mostrava a semana anterior à viagem.

**A causa: este arquivo tem duas naturezas e só uma vinha sendo mantida.** O topo é diário, cresce
por cima, uma seção por dia, e está em dia. O fundo ("Onde estou agora" e "Próximo passo") é estado
atual: precisa ser **reescrito**, não acrescentado. Ninguém reescrevia, então o cabeçalho podia
dizer "atualizado em 21/08" e a mesma tela mentir logo abaixo.

**Regra que fica:** "Onde estou agora" e "Próximo passo" entram na manutenção semanal do QTS, no
mesmo passo em que a semana nova troca de lugar na [Grade](GRADE.md). Seção datada se acrescenta,
seção de estado se reescreve.

**"Módulo" era premissa morta.** A palavra não aparece em nenhum arquivo do repositório porque não
existe no curso: são 31 disciplinas em paralelo, em blocos de 45 minutos, com QTS saindo semana a
semana. Ficou escrito assim no [PRAZOS.md](PRAZOS.md), para a pergunta não voltar daqui a um mês.

**"Entregas" não tinha como ser respondido, e continua sem.** O QTS não diz quem tem prova e quem
tem trabalho, e a [Grade](GRADE.md) já registrava isso na lista do que não se sabe. Não é lacuna de
preenchimento, é fonte que falta: a Seç Avaliação e Concurso do CAES, Cap PM Diego Almeida, que por
sinal é quem assina o QTS como Ch Sec Coord. Virou tarefa com data para terça 25/08, dia em que já
vou estar atrás do Cel Eglis e do Cap Gobbo.

## 21/08/2026: o painel não lia o repositório de volta

Queixa do Josemar, com estas palavras: *"editei a Central do CAO em outro PC, fiz push e pull, mas as
edições não aparecem no PC de casa; está uma sincronização burra local"*. Estava certo, e o problema
era de desenho, não de git.

**O painel só somava.** Ele sabia trazer do `.md` a tarefa nova e tirar a que sumiu, mas a tarefa que
existe nos dois lados com valores diferentes ficava **congelada no que aquele navegador tinha
gravado**. O mesmo valia para as caixinhas de Compras, Mala e Rotina, e ali era pior: a pintura
inicial só olhava o `localStorage`, então item marcado dentro do `.md` abria **desmarcado** em
qualquer aparelho que ainda não o tivesse marcado. Ou seja, o `git pull` trazia o arquivo certo e a
tela mostrava o estado velho.

**O que foi feito:**

- **`hora_do_md()`** no `gerar_painel.py`: a hora do último commit de cada `.md` vai embutida no
  painel (`window.ARQ_MOD` e `data-mod` em cada aba). É a mesma fonte de hora que o
  `sincroniza_tarefas.py` já usava, de propósito: duas regras de conflito diferentes no mesmo
  repositório seria pedir para errar.
- **`reconciliarComArquivo()`** nas tarefas e **`mkReconcilia()`** nas caixinhas: decidem item a item
  com um espelho do que o arquivo dizia na última abertura, separando "o arquivo mudou" de "eu mudei
  aqui" antes de comparar horas. Quem nunca tocou no item não tem o que defender: vale o arquivo.
- **`data-md` em cada caixinha**: o que o arquivo diz daquele item passou a chegar na tela.
- **`fetch-depth: 0` no `publicar-painel.yml`**: sem histórico o `git log` do arquivo vem vazio, a
  hora cairia na mtime do checkout (sempre "agora") e o arquivo ganharia de qualquer marcação feita
  no navegador. O `sincronizar-tarefas.yml` já exigia isso pelo mesmo motivo.

Detalhe do mecanismo em [PAINEL.md](PAINEL.md).

**A segunda causa, que nenhum código conserta:** o painel de casa estava **"Somente neste aparelho"**,
sem login. Sem entrar em **Tarefas → Entrar**, o que é marcado ali não sai daquele navegador — nem por
git, porque `git` não carrega `localStorage`. A reconciliação faz o repositório chegar na tela; o
login é o que faz o caminho de volta existir em minutos em vez de depender da Action de hora em hora.

**No mesmo dia, o login saiu de dentro da aba Tarefas.** Perguntado pelo Josemar: *"por que essa
lógica: Tarefas → Entrar?"*. Não havia lógica. O modal de conta era gerado dentro da seção da aba
Tarefas, que é `display:none` nas outras, então entrar na conta exigia estar naquela aba — mesmo
quando o que se queria sincronizar era a Mala. Agora o modal vive fora das abas, o botão **Entrar**
fica no cabeçalho ao lado do tema, e a linha de estado da sincronização virou clicável em qualquer
aba: quem lê "Somente neste aparelho" resolve ali mesmo, que é onde a dúvida aparece.

**Conferido no navegador em 21/08/2026, e passou nos cinco pontos.** No Chrome, tamanho de notebook
(1366) e de celular (390), nos dois temas:

- **O botão Entrar no cabeçalho** fica ao lado do tema sem apertar nenhum dos dois, com o texto
  inteiro e sem estourar a largura da tela. No celular o cabeçalho quebra em duas linhas e os dois
  botões descem juntos para a segunda, alinhados à direita.
- **O modal abre de qualquer aba.** Testado a partir da **Mala**, que era exatamente o caso que não
  funcionava antes.
- **A linha de estado da sincronização abre o mesmo modal**, clicada no topo da lista de Compras e
  da de Mala, no notebook e no celular.
- **Console sem erro e sem aviso.** O único registro é uma dica *verbose* do próprio Chrome dizendo
  que o campo de senha não está dentro de um `<form>`. Não é erro, e mexer nisso só muda o
  comportamento do gerenciador de senhas.
- **As caixinhas abrem com o que o `.md` diz**, que era o ponto principal. Num navegador de
  armazenamento zerado, **os 93 itens bateram um a um** com o arquivo: 17 em Compras (12 já
  marcados), 69 na Mala e 7 na Rotina, nenhuma divergência.

A prova do aparelho novo foi feita numa cópia do painel servida em `localhost`, byte a byte igual à
publicada (mesmo md5), de propósito: zerar o `localStorage` do painel de casa apagaria marcação de
verdade. E o painel de casa **entrou na conta durante o teste**, saindo de "Somente neste aparelho"
para "Salvo na nuvem", que era a segunda causa descrita acima.

*Detalhe do método, para a próxima vez: a janela do Chrome precisa estar visível na tela. Minimizada
ou coberta, o navegador congela o desenho e o screenshot expira sem tirar nada.*

## 21/08/2026: o QTS da semana 2 voltou alterado, e a semana não mudou

Chegou o **`QTS_CAOII_2_Alterado_2.pdf`**, revisão da folha de 24 a 28/08 que já estava
lançada na [Grade](GRADE.md). O arquivo foi gerado pela Coordenação em 20/08 às 20h39, um dia
depois de a seção ter sido escrita, então tinha que ser conferido antes de valer.

**Foi conferido célula a célula, e não mudou nada.** As 16 aulas do pelotão A estão iguais,
uma a uma; o corpo docente continua com os mesmos 117 nomes; o rodapé mantém os embarques de
07h50 nos pelotões C (24/08) e E (26/08), nenhum deles o meu; quinta 27/08 segue acabando às
11h30 e sexta 28/08 segue vazia. Duas decisões que dependiam desta semana continuam de pé: a
mala sem item de Ed. Física ([MALA.md](MALA.md)) e a abordagem ao orientador na terça 25/08,
bloco 4 ([ESTUDOS.md](ESTUDOS.md)).

**E o nome do orientador estava errado aqui dentro.** A revisão escreve o docente de D14 como
**"Cel PM Eglis"**; este repositório vinha escrevendo **"Elgis"** desde 17/08, inclusive na
decisão de orientação. **O Josemar confirmou no mesmo 21/08 que "Eglis" é o correto**, e a
grafia foi acertada nos cinco arquivos que citavam o nome: [Grade](GRADE.md), este STATUS,
[CONTATOS.md](CONTATOS.md), [ESTUDOS.md](ESTUDOS.md) e [TAREFAS.md](TAREFAS.md). Ia entrar
assim no pedido formal de orientação, que é conversa da terça 25/08.

**O que ficou de regra:** revisão de semana já lançada não se reescreve, se confere — e o
resultado da conferência fica registrado mesmo quando dá "igual", com data e nome do arquivo.
Sem isso, a próxima revisão obrigaria a reler a folha inteira do zero. A regra está no fim da
[Grade](GRADE.md), junto com a manutenção semanal.

## 20/08/2026: o robô do painel estava comendo linha do TAREFAS.md

Descoberto na volta da semana 1, ao rebasear em cima do commit
`53fa894` do **painel-cao-bot**: ele tinha apagado a nota da seção da Univesp, a linha que
guardava a hora do protocolo no SAE (19/08, 20h02) e o ponteiro para o repositório
`mentor-univesp`. Sem ela não dava para saber quando o prazo dos 10 dias úteis começou a
correr, e a prova é 22/09.

**A causa é de desenho, não de sorte.** O `TAREFAS.md` não é editado, é **remontado do zero**
a cada sincronização: cabeçalho + subtítulos + linhas de tarefa, e nada mais. Qualquer linha
dentro de uma seção que não fosse tarefa desaparecia calada. Valia para os dois caminhos que
escrevem no arquivo: a Action (`sincroniza_tarefas.py`) e o botão Exportar do painel.

O que foi feito:

- **`extrai_notas()` em `gerar_painel.py`**: lê o que vem logo abaixo de cada `###` até a
  primeira tarefa da seção e devolve `{seção: [linhas]}`.
- **As duas pontas passaram a devolver essas linhas**: o `para_markdown()` do Python e o
  `paraMarkdown()` do JavaScript. Tinham que ser as duas, porque o próprio código já registra
  que, se os dois gerarem saídas diferentes, cada um reescreve por cima do outro e o arquivo
  entra em commit de barulho eterno.
- **A nota da Univesp foi restaurada** a partir de `f404ce9`.
- **Conferido de ida e volta**: ler o `TAREFAS.md` e remontá-lo devolve o arquivo byte a byte
  igual, pelos dois caminhos. Sem a correção, some exatamente aquela linha.

**Regra que fica:** robô que reescreve arquivo tem que devolver o que não entendeu, não
descartar. Apagar em silêncio é pior que falhar, porque não deixa rastro no lugar onde a
pessoa vai procurar.

*Sobra um detalhe conhecido, e este é de propósito: o texto da tarefa é gravado sem markdown
(`extrai_tarefas` tira negrito, link e code). O painel mostra texto puro. Então não vale
escrever `**assim**` dentro de uma linha de tarefa, porque some na primeira sincronização.*

## 19/08/2026: o Drive ganhou mapa e as duas pontas passaram a se enxergar

Diagnóstico pedido pelo Josemar depois de a IA errar três vezes seguidas no mesmo dia:
pesquisou igreja na web em vez de ler o `ENTORNO.md`, não sabia o endereço do CAES e ofereceu
criar um arquivo de notas que já existia.

**A causa não era excesso de conteúdo.** Era isto: a regra de território ("repo guarda
logística, Drive guarda conteúdo") estava escrita **só aqui dentro**, no STATUS de 17/08.
Quando a sessão abre no Drive, que é onde se anota aula, essa regra era invisível. A IA
trabalhava sem saber que este repositório existia.

O que foi feito:

- **Nasceu o `08_CAO_2026/CLAUDE.md`**, no Drive. É o mapa: estrutura das pastas, a regra de
  território e uma tabela de "qual pergunta se responde em qual arquivo daqui". Sessão aberta
  em qualquer pasta do CAO agora começa sabendo que este repositório existe.
- **Este `AGENTS.md` ganhou a mesma regra**, na direção contrária, para quem abrir a sessão
  deste lado.
- **Duas skills novas**: `cao` (situar no curso: que aula é agora, prazo, entorno, rota) e
  `aula-cao` (anotar aula no arquivo da disciplina, no formato padrão, com `#PROVA`,
  `#DISSERTA` e `[VERIFICAR]`).
- **A cópia órfã das casas de oração virou ponteiro.** O `00_CURSO/CASAS-DE-ORACAO.md` no
  Drive ficou dois dias afirmando que o dado tinha saído do repositório público, quando a
  decisão foi revertida no mesmo 17/08 e a seção voltou inteira ao `ENTORNO.md`. Quem lesse a
  cópia concluiria o contrário do que é verdade.

**Regra que ficou:** uma informação, um dono. Quando o mesmo assunto existir dos dois lados,
um é dono e o outro é ponteiro de uma linha. Duplicar não confunde só a IA, apaga decisão.

**Pendência:** os três `mapas/ccb-*.svg` estão duplicados byte a byte em `00_CURSO/mapas/` no
Drive. Como o arquivo que os usava virou ponteiro, as cópias ficaram órfãs. Aguardando o
Josemar decidir se apaga.

## 18/08/2026: o QTS chegou e o curso deixou de ser um mistério

O primeiro QTS completo (semana 1, 17 a 21/08) resolveu de uma vez o levantamento que vinha
sendo feito a conta-gotas desde 17/08.

- **São 31 disciplinas**, não sete, com o corpo docente inteiro de cada uma. Rol completo na
  aba nova [Grade](GRADE.md), que também traz como se lê o QTS e o quadro da semana.
- **Eu sou do pelotão "A".** Não está escrito no QTS: foi deduzido cruzando as cinco aulas
  que assisti na terça 18/08 com as células marcadas "A". Cinco de cinco. Com isso o quadro
  de cinco pelotões vira agenda pessoal. **Falta confirmar de viva voz na Coordenação.**
- **Quarta 19/08 tem embarque às 07h50**, 25 minutos antes do normal, para atividade externa
  de Ed Física. O rodapé do QTS diz "pelotões A", e é só o meu.
- **As 31 pastas de disciplina foram criadas no Drive**, cada uma com `aulas/`, `trabalhos/`,
  `avaliacoes/` e o arquivo de notas já cabeçalhado com o corpo docente.
- **A numeração das pastas mudou:** saiu o prefixo de data (`2026-08_D01_`) e entrou
  `D01_` a `D31_`, na ordem da grade oficial. Motivo em [ESTUDOS.md](ESTUDOS.md): as 31
  disciplinas correm em paralelo, então a data não ordenava nada. As sete pastas que já
  existiam foram renumeradas e as notas de 17 e 18/08 foram preservadas.
- **A caça ao orientador destravou.** Ela esperava "o rol completo", que agora existe. O
  Cel Eglis continua sendo o alvo, e apareceram dois nomes novos fortes para o tema:
  **Cel Barreto** (Policiamento Comunitário) e **Cel Fernandes** (Relações Sociais e
  Institucionais no Brasil).

### O painel passou a montar o dia sozinho

A home agora abre com **"hoje no CAES"**: os blocos do dia, com a aula que está correndo
marcada como *agora* e a próxima com *em 25 min*. Sai do QTS lançado na aba
[Grade](GRADE.md), e a conta é feita no navegador, com a data de quem está olhando, então
não envelhece entre uma geração e outra.

Três respostas diferentes, de propósito: dia com aula mostra a lista; dia declarado sem aula
diz que não tem; e dia que o QTS ainda não cobriu **avisa que não sabe**, em vez de dizer que
está livre.

**O que isso pede de você:** mandar o QTS assim que ele sair. O resto é trocar a seção da
semana no GRADE.md e rodar o gerador.

**Próximo passo:** procurar o Cap Gobbo (Seção de Pesquisa) com as cinco perguntas das regras,
que estão em [ESTUDOS.md](ESTUDOS.md). Ele dá aula em duas disciplinas, D05 e D20.

## 17/08/2026, fim do dia: auditoria do que foi produzido

Revisão dos três eixos (mecânica, fatos e fontes, risco) sobre tudo que foi escrito hoje.
**12 achados, todos aplicados.** Três mereciam ficar registrados aqui:

- **A Linha 13-Jade não para em Tatuapé**, ao contrário do que o guia dizia. E a **janela da
  Feira da Madrugada não existia**: a recomendação era quinta 11h30, que é exatamente o
  horário em que eu pego a estrada para casa. Duas informações que se contradiziam dentro do
  próprio repositório.
- **15 números publicados como "medidos" não tinham fonte** guardada aqui. Agora estão no
  gerador e podem ser reconferidos.
- **As casas de oração saíram do repositório público** e foram para o Drive. Ver abaixo.

### Decisão de privacidade: levantada e revertida

Cheguei a mover as casas de oração para o Drive alegando padrão de vida. **O Josemar
reverteu, e com razão.** Dois furos no meu argumento:

1. **Nenhum daquele dado é secreto.** Endereço de igreja e horário de culto são públicos.
2. **Eu tirei o previsor mais fraco e deixei o mais forte.** O horário de aula é 4 dias por
   semana, todo ano, em endereço fixo. O culto é uma possibilidade. Removi o menos
   informativo e mantive o mais informativo, o que torna a remoção quase simbólica.

O único ponto que continua válido, e fica registrado sem virar ação: **convicção religiosa é
"dado pessoal sensível" na LGPD** (Lei 13.709/2018, art. 5º, II). Não é motivo para esconder,
é motivo para ele saber que está ali por escolha dele, e não por descuido meu.

**Conclusão: a seção voltou inteira ao guia, com os três mapas.** E o histórico do git fica
como está: reescrever custaria alto (105 commits mudam de identidade, as outras máquinas
quebram) para um ganho pequeno.

## 17/08/2026: primeiro dia de curso e método de estudo definido

O curso começou. Junto com ele nasceu a aba [ESTUDOS.md](ESTUDOS.md), que responde
"onde eu salvo, onde eu escrevo e como eu reviso" pelos próximos 12 meses. O resumo:

- **Divisão de território**: este repositório guarda logística (prazo, tarefa, rotina).
  O Google Drive guarda conteúdo (slide, anotação, trabalho, dissertação). Conteúdo de
  aula nunca entra aqui, porque o repositório é público.
- **A pasta do curso saiu de `02_TRABALHO/Outros/CAO 2026`**, onde estava enterrada, e
  virou `02_TRABALHO/08_CAO_2026`, de primeira linha junto com 5ª Cia e Operações. Os
  848 arquivos foram realocados por assunto e a pasta antiga foi removida.
- **Anotação é em arquivo `.md`, um por disciplina**, dentro da pasta da disciplina no
  Drive. Word fica só para entrega formal e para a dissertação em ABNT.
- **Correção do mesmo dia**: de manhã a recomendação era Google Docs, e ela caiu à tarde.
  **Dentro do CAES, na WCorp, o Google Docs não abre documento que já existe** (documento
  em branco criado na hora abre, porque nasce dentro do navegador). Testado nas duas
  primeiras aulas, com bloqueio de Google, formato, link e permissão todos descartados.
  Fora do quartel, o mesmo arquivo abre. Não dá para depender de nuvem em sala de aula.
- **As duas primeiras disciplinas**: D01 Políticas Públicas (Cel Lucena) e D02 Planejamento
  Estratégico (Cel Eglis), as duas com pasta criada e notas de 17/08 salvas.
- **Três etiquetas em toda anotação**: `#PROVA`, `#DISSERTA` e `#DUVIDA`. É o que evita
  reler doze meses de caderno em julho de 2027.
- **Audio Overview do NotebookLM ouvido na estrada de quinta**, que hoje é tempo morto.

**A grade do curso não está no edital.** Foi vasculhado: o Edital DEC-005/24/25 é do
processo seletivo e o Anexo "B" é a bibliografia da prova escrita. O que existe é um
esqueleto provisório (2 disciplinas confirmadas do CAO I/2024 pela dissertação do Cap
Ferrarez, mais a grade do manual do CAES de 2012), tudo registrado em
[ESTUDOS.md](ESTUDOS.md). **Quem manda é o QTS de hoje**: assim que ele sair, aquela
seção é reescrita e as pastas das disciplinas são criadas.

## Decisões de 14/08/2026 (o que vai na mala)

- **B-1 e EPI ficam para a segunda semana** (viagem de 23/08). Gandola, calça operacional,
  coturno e principalmente o colete são o conjunto mais volumoso da mala, e a carona divide
  porta-malas. A primeira semana vai de **P-1**, mais o **S-1** que fica guardado no CAES.
  *Risco assumido*: se o QTS de segunda marcar atividade externa já nesta semana, vai de P-1,
  avisa o chefe de turma e o B-1 sobe no domingo. Pelo bizu, o B-1 saiu 3 vezes no curso todo.
  *Revertido em 20/08/2026: o conjunto não sobe no dia 23 e fica em casa sem data nova, porque o
  QTS da semana 2 não traz Ed. Física nem atividade externa para o pelotão A ([MALA.md](MALA.md)).*
- **A gravata cinza-bandeirante já está em casa** e vai na mala. Saiu da lista da ConfecBell:
  da compra de segunda o S-1 passa a depender só da **camisa social**.
- **As 2 calças sociais também já existem em casa** (uma do P-1 e a do social), corrigindo o
  "já tenho 1" da conferência de armário. A calça saiu da compra de segunda, e as duas vão na
  mala: uma roda a semana com o P-1, a outra fica guardada no CAES junto com o social. Sobrou
  na ConfecBell só camisa de passeio, camiseta de serviço, boina e a camisa social.
- **Na segunda semana sobem também whey protein, creatina e energético**, com coqueteleira e
  etiqueta de nome (a geladeira é dividida pela turma).
- **Detalhe que isso criou**: o 4º distintivo de OPM do CAES é o da gandola, e a gandola não
  vai estar em São Paulo na segunda. Ele sai solto da ConfecBell ou fica lá esperando a peça —
  ver [COMPRAS.md](COMPRAS.md).

## Decisões de 12/08/2026 (fim do dia)

- **Viagem: domingo 16/08, saindo de casa às 15h00**, de carona com um amigo, chegando por volta das 22h. O alojamento abre desde sábado, mas o sábado fica em casa.
- **Fardamento: tudo na ConfecBell, na tarde de segunda 17/08.** Nada de loja antes de viajar.
- **Cama de solteiro** confirmada, então o lençol é de solteiro.
- **Boina reserva** vai na mala, então a boina nova é reposição, não urgência.
- **Ofício de Apresentação: acionar a P/1 amanhã, 13/08.** Não precisa de via impressa no dia 17.
- **"Passeio completo" na atividade externa é o P-1**, não o S-1. O quepe segue sendo peça de cerimônia.
- **EPI do curso: cinto, colete e bota**, com o B-1.

## Novidade de 12/08/2026: chegaram as orientações do SAE

O Cap Hiran (SAE) repassou as orientações da recepção. Quatro coisas mudam o planejamento
que estava aqui:

1. **O alojamento abre a partir de sábado à tarde.** Chegou a virar opção de viajar dia 15,
   mas a decisão do fim do dia foi ir no domingo (ver o bloco acima).
2. **A segunda começa 07h30, não 08h15**: recepção, café da manhã bancado pela turma do
   CAO-I/26, lista de presença por pelotão e palestra. À tarde, tempo livre para social,
   ConfecBell, alojamento e armário. **O QTS sai neste dia.**
3. **O armário não tem chave: o cadeado é seu.** Item novo, ninguém tinha previsto.
4. **A farda social vai junto e fica guardada no CAES.** Não se usa na segunda, mas o curso
   tem visitas. A [MALA.md](MALA.md) não tinha S-1 nenhum; agora tem.

As dúvidas que isso levantou foram todas fechadas no mesmo dia, e estão em
[DUVIDAS.md](DUVIDAS.md) com a marca de que a fonte foi o Josemar, não a Seção.

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

## As tarefas voltam sozinhas para o repositório (14/08/2026)

Marcar, remarcar ou criar tarefa no painel não exige mais copiar e colar no
[TAREFAS.md](TAREFAS.md). Uma Action roda de hora em hora, lê o Supabase e reescreve o
arquivo, preservando cabeçalho e seções. Mexeu no celular, em até uma hora o repositório
está em dia e o painel republicado. Como funciona e quem manda quando arquivo e nuvem
discordam: [PAINEL.md](PAINEL.md) e [SUPABASE.md](SUPABASE.md).

## Publicação automática (06/08/2026)

O painel se publica sozinho. Editou um `.md` e deu push (ou editou pela
web do GitHub, do celular), o painel regenera e vai para o ar sem ninguém rodar
nada. Rodar `python gerar_painel.py` na mão continua valendo para conferir antes
de subir. Detalhe e o histórico do build quebrado do Pages estão em
[ANOTACOES.md](ANOTACOES.md).

## Onde estou agora
- Sou **Oficial-Aluno do CAO-II/2026** (2ª Turma), do **Programa de Mestrado Profissional em Ciências Policiais de Segurança e Ordem Pública**, no **CAES "Cel Nelson Freire Terra"**, **em frente à Praça Júlio Prestes, no centro de São Paulo** (Campos Elíseos / Santa Ifigênia). *Corrigido em 17/08/2026, no local: até então este arquivo dizia "região da Barra Funda", o que é outro bairro e chegou a produzir guia com a estação de metrô errada.* Estações a pé: **Luz** (Linhas 1-Azul e 4-Amarela), **Santa Cecília** (3-Vermelha) e **Júlio Prestes** (CPTM, na praça). Ver [ENTORNO.md](ENTORNO.md).
- **Estou entrando na semana 2 de um curso de um ano.** A semana 1 (17 a 21/08) está cumprida. Amanhã, **domingo 23/08**, é a viagem da semana 2, que leva a roupa lavada e a carga da copa. **O B-1 e o EPI ficam em casa**, por decisão de 20/08 que reverteu a de 14/08: o QTS da semana 2 não traz Ed. Física nem atividade externa para o pelotão A (ver [MALA.md](MALA.md)).
- **O curso não tem módulo.** São **31 disciplinas correndo em paralelo**, em blocos de 45 minutos, várias por dia, e o **QTS sai semana a semana**, não por semestre. **24 das 31 já foram acionadas** em algum pelotão até a semana 2. A mesma disciplina volta em semanas diferentes, às vezes com outro docente. Rol completo, corpo docente e quadro da semana na [Grade](GRADE.md).
- **Sou do pelotão A.** Deduzido em 18/08 cruzando as cinco aulas que assisti com as células marcadas "A" no QTS, cinco de cinco. *[VERIFICAR: falta ratificar de viva voz na Coordenação.]*
- **Horário real do dia:** blocos 1 a 4 todo dia (08h15, 10h00, 13h00 e 14h45), e o bloco 5 (16h30 às 18h00) só na terça e na quarta. Segunda e sexta acabam 16h15, **quinta acaba 11h30**, que é quando pego a estrada para casa. Na semana 2 a sexta 28/08 está vazia no QTS, para todos os pelotões.
- **A semana 2 é mais pesada que a 1:** 16 aulas contra 14, com terça e quarta cheias até as 18h00. Os dois embarques de 07h50 do rodapé do QTS são dos pelotões C e E, **nenhum é o meu**, então não tem Ed. Física para mim nesta semana e a mala vai sem item de educação física.
- **Dissertação:** PP aprovado, tema mantido (integração PM-Prefeituras / governança participativa no 2º BPM/I), versão final em [CAO 2026/PP/Projeto Pesquisa Cap Josemar Final.doc](CAO%202026/PP/Projeto%20Pesquisa%20Cap%20Josemar%20Final.doc). Alvo de orientação decidido em 18/08: **Cel PM Eglis** (D14 Planejamento Estratégico), que dá aula na **terça 25/08, bloco 4**. Método e sequência das conversas em [ESTUDOS.md](ESTUDOS.md).
- **O que ainda não sei do curso:** a carga horária de cada disciplina, quais têm prova e quais têm trabalho, e se as sete que nunca entraram são do segundo semestre. A lista está no fim da [Grade](GRADE.md), e nada disso sai do QTS: sai da Coordenação.
- Curso roda de **ago/2026 a ago/2027** (conforme edital). Rotina 13 do SIPA liberada de **17/ago/26 a 22/jan/27** (1º bloco financeiro/administrativo).
- Fase de seleção (inscrição, prova escrita, defesa do PP) concluída, documentos arquivados em [CAO 2026/Inscrição](CAO%202026/Inscrição/). Contatos e organograma do CAES: [CONTATOS.md](CONTATOS.md). Rotina, uniforme, SIPA financeiro e formatura: [ROTINA.md](ROTINA.md).

## Próximo passo

O roteiro dia a dia está em [TAREFAS.md](TAREFAS.md), com data, e é o que o painel cobra na
abertura (por isso aqui é só leitura, para não ter duas listas dizendo a mesma coisa). O que
está de pé agora:

1. **Domingo 23/08, viagem da semana 2.** Sobe a roupa lavada e a carga da copa; o **B-1** e o
   **EPI** ficam em casa (decisão de 20/08). Faltam duas compras: o **energético zero** e, do
   fardamento, a **camisa social cinza-claro do S-1** com a **boina de reposição**, que não
   saíram na ida à ConfecBell. O rodízio da mala está em [MALA.md](MALA.md), e as duas linhas
   dele já estão em [TAREFAS.md](TAREFAS.md), com data.
2. **Terça 25/08, bloco 4, das 14h45 às 16h15: o Cel Eglis dá aula.** É a janela da semana para a
   abordagem de orientação, com o PP aprovado na mão e uma pergunta objetiva, não um "o senhor me
   orientaria?". A sequência completa está em [ESTUDOS.md](ESTUDOS.md).
3. **Cap Gobbo (Seção de Pesquisa), as perguntas das regras:** o orientador precisa ser instrutor
   do curso, quantos orientandos cada um aceita, se há prazo para escolher, como é o pedido formal
   e se o Cel Siconeli ainda orienta. Ele dá aula em D05 e D20, então dá para achá-lo em sala em
   vez de caçá-lo na seção.
4. **Perguntar na Coordenação quais disciplinas têm prova e quais têm trabalho**, e se existe plano
   de disciplina com carga horária. É o pedaço da situação do curso que o QTS não responde, e é o
   que falta para o [PRAZOS.md](PRAZOS.md) deixar de ser calendário só de logística.
5. **Univesp, 03/09:** vencem os 10 dias úteis do pedido protocolado no SAE em 19/08, às 20h02.
   Sem resposta, cobrar pelo 0800 051 3333 ou pelo WhatsApp. A prova é 22/09 e cai em dia de curso.

**O que o painel precisa de você durante a semana:** o QTS da semana 3, assim que sair. Com ele o
cartão de abertura monta o dia sozinho; sem ele, o painel avisa que não sabe, em vez de dizer que
o dia está livre.

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
