# STATUS — Central do CAO

> Painel principal. Ler isso primeiro em qualquer sessão nova ("onde paramos?").
> Atualizado em: 18/08/2026

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
  Cel Elgis continua sendo o alvo, e apareceram dois nomes novos fortes para o tema:
  **Cel Barreto** (Policiamento Comunitário) e **Cel Fernandes** (Relações Sociais e
  Institucionais no Brasil).

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
  Estratégico (Cel Elgis), as duas com pasta criada e notas de 17/08 salvas.
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

1. **Hoje (14/08), conferir se a mesa SEI 302090130 recebeu o ofício** e anotar o
   número do processo no celular. É do ato eletrônico da P/1 que dependem a matrícula,
   a adição, a Ajuda de Custo e o Auxílio Financeiro a Estudantes.
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
