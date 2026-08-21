# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 21/08/2026

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
- Sou **Oficial-Aluno do CAO/II-2026** (2ª Turma) — **Programa de Mestrado Profissional em Ciências Policiais de Segurança e Ordem Pública**, no **CAES "Cel Nelson Freire Terra"**, **em frente à Praça Júlio Prestes, no centro de São Paulo** (Campos Elíseos / Santa Ifigênia). *Corrigido em 17/08/2026, no local: até então este arquivo dizia "região da Barra Funda", o que é outro bairro e chegou a produzir guia com a estação de metrô errada.* Estações a pé: **Luz** (Linhas 1-Azul e 4-Amarela), **Santa Cecília** (3-Vermelha) e **Júlio Prestes** (CPTM, na praça). Ver [ENTORNO.md](ENTORNO.md).
- Curso roda de **ago/2026 a ago/2027** (conforme edital). Rotina 13 do SIPA liberada de **17/ago/26 a 22/jan/27** (1º bloco financeiro/administrativo).
- Fase de seleção (inscrição, prova escrita, defesa do PP) já concluída — documentos arquivados em [CAO 2026/Inscrição](CAO%202026/Inscrição/).
- Projeto de Pesquisa (PP) tem versão final entregue em [CAO 2026/PP/Projeto Pesquisa Cap Josemar Final.doc](CAO%202026/PP/Projeto%20Pesquisa%20Cap%20Josemar%20Final.doc) — tema: integração PM-Prefeituras / governança participativa no 2º BPM/I. Como agora é mestrado profissional, isso deve virar **dissertação** (ver contato de Pesquisa em [CONTATOS.md](CONTATOS.md)).
- Contatos e organograma do CAES: ver [CONTATOS.md](CONTATOS.md).
- Regras de rotina, uniforme, SIPA financeiro, formatura: ver [ROTINA.md](ROTINA.md).
- **Primeira semana: viaja domingo 16/08 à tarde, chegando à noite.** Segunda 17/08 a recepção é **07h30**; da terça em diante entra 08h15 e sai 16h seg, 18h ter e qua, 11h30 qui. A conferência de armário está **feita** (06/08, 78 das 90 peças já em casa), então sobraram duas etapas: [COMPRAS.md](COMPRAS.md) (o que falta) → [MALA.md](MALA.md) (arrumar a mala no dia).
- **Módulo e disciplinas**: saem no **QTS de segunda, 17/08**. Até lá não tem o que preencher.

## Próximo passo

O roteiro dia a dia até a viagem está em [TAREFAS.md](TAREFAS.md), com data, e é o
que o painel cobra na abertura (por isso aqui é só leitura, para não ter duas listas
dizendo a mesma coisa). O que trava tudo:

Decidido em 12/08: **o fardamento inteiro fica para a tarde de segunda, na ConfecBell**,
e a viagem é **domingo à tarde**. Isso esvaziou a correria da semana.

Até 14/08 já saíram do caminho: **a P/1 foi acionada** pelo Ofício de Apresentação e
pela Rotina 13 do SIPA, **o cadeado e a etiqueta foram comprados**, **a carona está
combinada** (espaço de bagagem incluído), a **camisa de passeio está engomada** e a
conta do Banco do Brasil foi conferida. Sobrou:

1. ~~Conferir se a mesa SEI 302090130 recebeu o ofício.~~ **Recebeu — fechado em
   19/08/2026.** A cobrança do CAES aos capitães cujo Ofício de Apresentação ainda não
   tinha chegado não traz meu nome nem o 2º BPM/I. Como é desse ato eletrônico da P/1 que
   dependem matrícula, adição, Ajuda de Custo e Auxílio Financeiro a Estudantes, o assunto
   sai da lista de pendências.
2. **Sábado (15/08), separar e arrumar**: os documentos de mão, o S-1 que fica guardado no
   CAES (com a gravata, que já está em casa) e a mala inteira, seguindo a [MALA.md](MALA.md).
   O B-1 e o EPI **não** entram nessa mala: ficam separados em casa, para a viagem de 23/08.
3. **Domingo (16/08), sair de casa às 15h00.** Chegada por volta das 22h.
4. Depois do **QTS de segunda (17/08)**, me trazer módulo, entregas e avaliações
   pra eu completar [PRAZOS.md](PRAZOS.md).

Não é mais preciso escrever ao SAE: as quatro dúvidas foram fechadas em 12/08
(ver [DUVIDAS.md](DUVIDAS.md)).

**O que a mala cobra:** **boina reserva**, **camisa de passeio engomada** (é a que veste
o primeiro dia), **lençol de solteiro**, **janta de domingo** e volume contido, porque a
carona divide porta-malas. Sem coturno na mala, o **sapato preto é o único calçado de farda
da semana** — confira antes de fechar.

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
