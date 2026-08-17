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
| D01 | Políticas Públicas | Cel Lucena | 17/08/2026, 13h00 às 14h30 |
| D02 | Planejamento Estratégico | Cel Elgis | 17/08/2026, à tarde |

As duas **batem com o esqueleto de 2012** abaixo ("Políticas Públicas de Prevenção e
Controle da Criminalidade" e "Planejamento Estratégico e Construção de Cenários"), o que
aumenta a confiança no resto da lista. Quando sair o QTS com os nomes oficiais, conferir se
o nome completo é esse e renomear as pastas se precisar.

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
