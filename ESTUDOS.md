# ESTUDOS — método de estudo do CAO

> Como eu estudo, onde eu salvo e onde eu escrevo, pelos 12 meses de curso.
> Montado em 17/08/2026, no primeiro dia.

## A regra que sustenta tudo: dois lugares, sem sobreposição

| Onde | O que vive lá |
|---|---|
| **Este repositório** (os `.md` e o painel) | Logística: prazos, tarefas, rotina, contatos, uniforme |
| **Google Drive**, `10_JOSEMAR/02_TRABALHO/08_CAO_2026/` | Conteúdo: slides, minhas anotações, trabalhos, dissertação |

Na dúvida sobre onde salvar, a pergunta é: **isso é data ou é conteúdo?** Data vem para cá.
Conteúdo vai para o Drive. Conteúdo de aula nunca entra no repositório, que é público.

## Estrutura no Drive

Criada em 17/08/2026. Saiu de `02_TRABALHO/Outros/CAO 2026`, onde estava enterrada, e virou
item de primeira linha junto com 5ª Cia e Operações. Os 848 arquivos que já existiam foram
todos realocados.

```
10_JOSEMAR/02_TRABALHO/08_CAO_2026/
├── 00_CURSO/              edital, QTS de cada semana, normas, calendário
├── 01_DISCIPLINAS/
│   ├── _MODELO_DISCIPLINA/     pasta-molde: duplicar a cada disciplina nova
│   └── 2026-08_D01_NOME/
│       ├── aulas/         material do instrutor (CRU, nunca editar)
│       ├── trabalhos/     o que EU entrego
│       └── avaliacoes/    provas, gabaritos, notas
├── 02_DISSERTACAO/
│   ├── 00_orientacao/     atas das reuniões com o orientador
│   ├── 01_referencias/    artigos, teses, dissertações-modelo
│   ├── 02_texto/          o texto em si
│   ├── 03_campo/          dados, entrevistas, protocolos
│   └── PP_original/       a pasta do PP como estava na seleção
├── 03_TURMA/              formatura, comissões, escalas
├── 04_ARQUIVO_SELECAO/    inscrição, provas e material de estudo da seleção (encerrado)
└── 99_INBOX/              tudo que chega e ainda não foi arquivado
```

Três detalhes que não são enfeite:

**O `99_INBOX` é o mais importante.** Slide chega no meio da aula, por WhatsApp, do Subchefe
de Turma, com nome ruim. Se eu tiver que decidir na hora onde arquivar, não arquivo. Jogo no
INBOX e esvazio na quinta. Estrutura sem lata de despejo morre na terceira semana.

**A pasta da disciplina nasce com data na frente** (`2026-08_D01_`). Ordena sozinha na linha
do tempo do curso, que é como eu vou lembrar depois ("aquilo foi em outubro").

**`aulas/` é intocável.** O material do instrutor entra e não é editado nem renomeado por
dentro. O que é meu vai para o documento de notas, separado. Assim sempre dá para saber o que
é fonte e o que é meu.

## Onde escrevo: arquivo Markdown local, um por disciplina

**Decidido em 17/08/2026, depois de o Google Docs falhar na prática. Não é Word e não é
Google Docs.**

A primeira versão deste documento, escrita na manhã do mesmo dia, mandava anotar em Google
Docs. Estava errado, e o erro apareceu no mesmo dia, nas duas primeiras aulas.

**O que aconteceu:** dentro do CAES, na rede WCorp, o Google Docs **não abre documento que
já existe**. Foi testado à exaustão em 17/08. O que confunde é que um documento em branco
criado ali na hora abre normal, porque ele nasce dentro do próprio navegador e não precisa
buscar nada no servidor. Qualquer documento que já existe, a WCorp não deixa carregar. O
mesmo arquivo, no wi-fi de fora, abre sem reclamar. Descartados no caminho: bloqueio geral
do Google (o Drive abre), formato do arquivo (documento nativo vazio falhou igual), link
errado (abrir pela pasta falhou igual) e permissão (os arquivos são meus).

**Conclusão prática: não dá para depender de nuvem para anotar em sala de aula.**

Então a anotação é **um arquivo `.md` por disciplina**, dentro da pasta da disciplina no
Drive, editado em qualquer editor de texto (Bloco de Notas serve, VS Code é melhor). O
Google Drive do computador sincroniza sozinho quando a rede permitir.

Por que `.md` e não `.docx`:

- **Funciona sem rede nenhuma.** É a única exigência que realmente importa em sala.
- **O NotebookLM lê Markdown e `.txt` numa boa.** O que se perde em relação ao Docs é só a
  sincronização automática da fonte: em vez de o NotebookLM se atualizar sozinho, eu reenvio
  o arquivo quando quiser. Custo baixo.
- Eu já escrevo Markdown o dia inteiro neste repositório, então não é ferramenta nova.
- Arquivo de texto não corrompe, não trava e abre em qualquer máquina.

**Word continua existindo, só para entrega formal**: trabalho avaliado e a dissertação em
ABNT. Formatação séria é Word, anotação do dia a dia é `.md`.

Descartados: **Google Docs** pelo motivo acima; **OneNote**, porque o NotebookLM não lê e
exportar de lá é sofrido; **Notion e Obsidian**, por serem ferramenta nova em semana de
curso novo.

**Um arquivo por disciplina, não um por aula.** Trinta aulas viram trinta arquivos e eu
nunca mais acho nada. Um arquivo contínuo cresce com o semestre e o Ctrl+F resolve. E é
**1 fonte** no NotebookLM em vez de 30.

Nome: `NOTAS-D01-Nome-Da-Disciplina.md`, dentro da pasta da disciplina.

*[VERIFICAR amanhã, 18/08: se o Google Drive do computador consegue sincronizar dentro da
WCorp. Se não conseguir, os arquivos sobem sozinhos quando eu sair do quartel, o que não
atrapalha nada, mas é bom saber. Vale também marcar a pasta 08_CAO_2026 como "disponível
off-line" no Drive, para o arquivo morar no disco e não depender de streaming.]*

### Modelo de anotação em aula

Burro o suficiente para eu conseguir preencher enquanto o instrutor fala:

```
## 18/08 — Tema da aula — Instrutor

Ideia central:
Cai na prova:           #PROVA
Serve na dissertação:   #DISSERTA
Ficou dúvida:           #DUVIDA
```

**As três etiquetas são o coração do método.** Eu não vou reler doze meses de anotação em
julho de 2027. Vou buscar `#DISSERTA` e achar em dois minutos tudo que marquei como
aproveitável no ano inteiro. Custa meio segundo por anotação. Mesma coisa com `#PROVA` na
véspera da avaliação.

Não transcrever aula. Anotação boa é a ideia com as minhas palavras. O slide eu já tenho
salvo em `aulas/`.

## NotebookLM: três tipos de caderno

Não um caderno gigante, porque misturar assunto piora a resposta e há limite de fontes.

| Caderno | Fontes | Para quê |
|---|---|---|
| **Um por disciplina** (criado quando ela começa) | slides do instrutor + meu documento de notas + bibliografia | estudar para a prova, tirar dúvida sem abrir PDF |
| **CAO Dissertação** (permanente) | PP, dissertação do Cap Ferrarez, artigos, atas de orientação | pensar a dissertação o ano inteiro |
| **CAO Normas** (permanente) | edital, QTS, regras do SAE, R-5-PM | responder "quantas faltas posso ter?" em dez segundos |

### O uso que paga o esforço sozinho

Guararapes ↔ São Paulo toda semana são umas 6 a 7 horas de estrada, hoje perdidas.

Na quinta, antes de pegar a estrada, gerar o **Audio Overview** do caderno da disciplina da
semana e ouvir na volta. Revisão semanal sem gastar um minuto a mais do dia. Doze meses disso
é o curso inteiro revisado de graça.

*[VERIFICAR: limite de fontes por caderno muda conforme o plano do NotebookLM.]*
*[VERIFICAR com o Chefe de Turma: se pode gravar áudio de aula. Se puder, o NotebookLM aceita
áudio como fonte e isso muda muita coisa. Se não puder, esquecer.]*

## Ritmo semanal

Encaixado no horário real de segunda a quinta ([ROTINA.md](ROTINA.md)):

| Quando | Quanto | O quê |
|---|---|---|
| Todo dia, últimos 10 min | 10 min | Fechar o documento do dia, jogar slide e foto no `99_INBOX` |
| Quinta, depois das 11h30 | 15 min | Esvaziar o INBOX para as pastas certas. Gerar o Audio Overview |
| Quinta, na estrada | grátis | Ouvir o resumo da semana |
| Domingo à tarde, antes de sair | 30 min | Ler as notas da semana, conferir o QTS da semana seguinte, atualizar [PRAZOS.md](PRAZOS.md) |
| 1x por mês | 1 h | Buscar `#DISSERTA` em todos os documentos e mover o que prestou para `02_DISSERTACAO` |

O domingo de 30 minutos é o que amarra o Drive com o painel do celular.

## A dissertação começa agora, não em 2027

PP aprovado, tema definido (integração PM-Prefeituras / governança participativa no 2º BPM/I)
e uma dissertação-modelo já em mãos. O erro clássico é tratar isso como "ano que vem".

- **Semana 1 e 2**: criar o caderno "CAO Dissertação" no NotebookLM. Procurar o **Cap Gobbo**
  (Seção de Pesquisa) sobre transformar o PP em dissertação.
- **Setembro**: instalar o **Zotero** (grátis, plugin do Word, gera ABNT sozinho). Todo PDF de
  artigo entra nele com um clique. Sem isso, em maio serão 80 PDFs sem saber de onde veio cada
  citação. Foi deixado para setembro de propósito: ferramenta nova em semana de curso novo é
  ferramenta abandonada.
- **O mês inteiro**: a etiqueta `#DISSERTA` trabalhando sozinha.

## Orientador da dissertação — missão urgente

Aberta em 18/08/2026. **O orientador deve ser, preferencialmente, instrutor do curso.**

### O problema é de tempo, não de escolha

A informação de que preciso chega **devagar**: o QTS sai dia a dia, então o rol completo de
disciplinas e instrutores só fecha depois de semanas. Mas o recurso que quero **acaba
rápido**: bom orientador é procurado, e quem chega primeiro leva.

**Conclusão: não dá para esperar a lista completa.** A ordem certa é agir sobre o que já se
sabe e deixar o resto amadurecer.

### DECIDIDO em 18/08: o alvo é o Cel PM Elgis

Escolhido entre os sete instrutores conhecidos. **O caminho até ele é o Cap PM Simões**, que
tem o contato. Ver [CONTATOS.md](CONTATOS.md).

**Por quê**: na aula de 17/08 ele abriu perguntando *"nosso foco, visão de futuro, é polícia
repressiva ou polícia comunitária?"*. É exatamente a tensão que a minha dissertação sobre
integração PM-Prefeituras tem que sustentar. Um orientador que já formula o problema nos
mesmos termos poupa meses de tradução.

**O que não muda com a decisão:** as regras continuam sendo o primeiro passo. Chegar no Cel
Elgis sabendo se ele pode aceitar, quantos orientandos já tem e qual o prazo vale mais do que
chegar antes e no escuro. As duas conversas podem correr em paralelo, mas a do Gobbo é a que
protege a outra.

### A sequência, nesta ordem

**1. As regras, antes de qualquer nome** (Cap Gobbo, Seção de Pesquisa)

Sem isso, escolher é chute. Perguntar:

- O orientador **precisa** ser instrutor do curso, ou é só preferência?
- **Quantos orientandos** cada um pode aceitar?
- Existe **prazo** para definir? Qual?
- O pedido é **formal** ou é conversa direta com o oficial?
- Cabe **coorientador**, por exemplo um para o tema e outro para o método?

Uma dessas respostas pode eliminar metade das opções, e todas são mais baratas de obter do
que desfazer uma escolha errada.

**2. A lista curta, por afinidade com o tema**

Meu tema é **integração PM-Prefeituras e governança participativa**. Isso é política pública
e articulação interinstitucional, não é operacional puro. Dos sete instrutores conhecidos até
18/08:

| Instrutor | Disciplina | Encaixe no meu tema |
|---|---|---|
| **Cel Lucena** | Políticas Públicas | **O mais direto.** Meu tema É política pública. E na aula 1 ele abriu com modelo reativo x pró-ativo, que é o eixo do meu argumento |
| **Cel Elgis** | Planejamento Estratégico | **Forte.** Ele perguntou "nosso foco é polícia repressiva ou comunitária?", que é exatamente a tensão que a dissertação enfrenta |
| Cap Franco | Métodos Quantitativos de Pesquisa | Encaixe de **método**, não de tema. Candidato natural a coorientador se o trabalho tiver survey |
| Maj Zampronio | Fundamentos da Metodologia Científica | Idem. E é quem vai avaliar o rigor do método |
| Cel Komata | Geopolítica | Fraco para o tema |
| Cap Anderson | Mídia Training | Fraco |
| Cel Massera | Gestão de Crises de Imagem | Fraco |

**3. Sondar cedo, com o texto na mão**

Chegar com o PP aprovado e uma pergunta objetiva vale mais que "o senhor me orientaria?".
O PP já existe e está em `02_DISSERTACAO/02_texto/`.

### Uma pista que veio da dissertação de referência

A dissertação do **Cap PM José Fernando Ferrarez** (CAO/24, defendida em 2025), que está em
`02_DISSERTACAO/01_referencias/`, nomeia quem o orientou:

- **Cel PM Mario Luciano Siconeli** — orientador
- **Ten Cel PM Ivan Cesar Belentani** e **Cap PM Valdomiro Garcia Rafael Junior** —
  citados nos agradecimentos como quem o orientou sobre os caminhos do estudo

**Por que isso importa:** são oficiais que **já orientaram no CAES e conhecem o processo**.
O Cel Siconeli não apareceu (ainda) como instrutor da minha turma, mas vale perguntar ao Cap
Gobbo se ele segue orientando. Orientador experiente poupa meses.

### O que ainda falta

O **rol completo**. Cada QTS que chega acrescenta instrutores, e a tabela acima cresce junto
com a de disciplinas. Enquanto isso não fecha, os passos 1 e 3 já podem andar.

## O que não fazer

- Pasta por aula ou documento por aula: vira lixo em um mês.
- Adotar Notion ou Obsidian agora: ferramenta nova + curso novo = abandono na semana 4.
- Anotar em três lugares "para garantir".
- Copiar slide para dentro da anotação: o slide já está salvo.
- Guardar conteúdo de aula neste repositório: é público e o git guarda para sempre.

## Disciplinas do curso

### Confirmadas na prática (CAO-II/2026)

| # | Disciplina | Instrutor | Primeira aula |
|---|---|---|---|
| D01 | Políticas Públicas | Cel Lucena | 17/08, 13h00–14h30 |
| D02 | Planejamento Estratégico | Cel Elgis | 17/08, à tarde |
| D03 | Geopolítica | Cel PM Komata | 18/08, 08h15–09h45 |
| D04 | Mídia Training | Cap PM Anderson | 18/08, 10h00–11h30 |
| D05 | Gestão de Crises de Imagem | Cel PM Massera | 18/08, 13h00–14h30 |
| D06 | Métodos Quantitativos de Pesquisa | Cap PM Franco | 18/08, 14h45–16h15 |
| D07 | Fundamentos da Metodologia Científica | Maj PM Zampronio | 18/08, 16h30–18h00 |

**O QTS sai dia a dia, não por semestre.** Isso derrubou uma premissa que este documento
tinha: eu supunha disciplina em bloco, uma terminando antes da outra começar. **Não é assim.**
Elas correm em paralelo, em blocos de 45 minutos, várias por dia. Só a terça de 18/08 teve
cinco disciplinas diferentes.

**O que isso muda no método:** nada na estrutura, e muito no ritmo.

- Um arquivo por disciplina continua certo, e fica ainda mais importante: sem isso, a
  anotação de cinco matérias diferentes cairia tudo no mesmo lugar.
- **Mas o arquivo do dia não é um só.** Numa terça você abre cinco arquivos, um por bloco.
  Por isso o atalho abre a **pasta** no VS Code, e não um arquivo: você clica na matéria da
  vez na barra da esquerda.
- **A etiqueta `#DISSERTA` fica mais valiosa ainda.** Repare que D06 e D07 são
  metodologia de pesquisa pura, ou seja, aula que existe para a sua dissertação. O que sair
  dali vai direto para o texto.

*Os RE dos instrutores constam do QTS, mas não são copiados para cá: é dado pessoal de
terceiro e este repositório é público. Ficam só nome e posto.*

### O levantamento de origem

**O edital não traz a grade.** Vasculhado em 17/08/2026: o Edital DEC-005/24/25 é do processo
seletivo, e o Anexo "B" ("Conteúdo Programático") é a bibliografia da prova escrita, não a
matriz do curso. O slide de recepção do SAE também não traz. Nenhum dos 848 arquivos do Drive
traz.

O que existe são **duas fontes indiretas**, as duas provisórias até sair o QTS.

**1. Disciplinas confirmadas do CAO I/2024**, citadas em notas de rodapé da dissertação do
Cap PM Ferrarez (que está em `02_DISSERTACAO/01_referencias/`):

| Disciplina | Instrutor | Registro |
|---|---|---|
| Criminologia e Fenomenologia do Crime | TC Maurício Alves Barbosa | aula ao pelotão "A", 02/abr/2024 |
| Planejamento Operacional | Maj Hudson Arthur Rodrigues Rosa | aula ao pelotão "D", 27/jun/2024, 13h00 às 16h15 |

**2. Grade do Programa de Mestrado Profissional**, do *Manual e Código de Conduta do Aluno* do
CAES (Anexo "B"), publicado na página do CAES. **Atenção: o manual é de 2012**, então serve de
esqueleto, não de verdade atual. As duas disciplinas de 2024 acima já não batem exatamente com
ele.

Matérias comuns: Metodologia da Pesquisa; Ética e Cidadania; Direitos Humanos; Justiça,
Processo Penal e Polícia Judiciária Militares; Tiro Defensivo na Preservação da Vida "Método
Giraldi"; Direito Administrativo da Ordem Pública; Geografia do Crime; Legislação Especial
Aplicada; Planejamento Estratégico e Construção de Cenários; Políticas Públicas de Prevenção e
Controle da Criminalidade; Geopolítica do Estado de São Paulo; Direito Constitucional.

Matérias específicas da minha linha (Administração PM e Policiamento Ostensivo):

- **Teoria Geral de Ciências Policiais**, com as unidades: Teoria das Ciências Policiais,
  Fenomenologia da Violência e do Crime, Filosofia e Doutrina de Polícia Ostensiva, Polícia
  Comunitária, Mediação de Conflitos e Gerenciamento de Crises, Inteligência Policial.
- **Organização e Gestão de Polícia Ostensiva**, com as unidades: Gestão de Recursos Humanos,
  Gestão de Recursos Públicos, Gestão de Logística, Gestão pela Qualidade, Comunicação Social,
  Gestão do Conhecimento, Administração por Projetos, Tecnologia da Informação e Comunicação,
  Avaliação e Prescrição do Treinamento Físico e Saúde.
- **Exercícios de Planejamento de Polícia Ostensiva (ExPPO)**.

*(A matéria "Organização e Gestão do Sistema de Saúde Policial-Militar" é do QOS, não se
aplica a mim.)*

*[VERIFICAR: as cargas horárias saíram embaralhadas na extração do PDF de 2012 e por isso não
foram anotadas aqui. Se precisar do número, abrir o manual na página do CAES.]*

**Fonte de verdade é o QTS.** Assim que ele sair, esta seção é reescrita com os nomes reais e
as pastas de `01_DISCIPLINAS` são criadas a partir do `_MODELO_DISCIPLINA`.
