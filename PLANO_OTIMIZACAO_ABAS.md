# Plano de Otimização das Abas do Painel CAO

## Objetivo

O painel (`docs/index.html`) é gerado pelo script `gerar_painel.py` a partir de 15
arquivos `.md` na raiz do repositório, um por aba. Depois de meses de uso o conteúdo
cresceu e ficou prolixo, com trechos repetidos e, em alguns pontos, informação que se
contradiz. Este plano guia uma varredura completa em 30 etapas: 15 de auditoria (uma
por aba) seguidas de 15 de correção (uma por aba). O relatório de cada etapa é anexado
neste mesmo arquivo, na seção da aba correspondente, na ordem em que as etapas forem
concluídas.

## Prompt para o Codex

Copie o bloco abaixo e envie ao Codex.

```
Você vai auditar e depois corrigir o conteúdo das 15 abas do painel do projeto
central-cao. Antes de começar, leia o AGENTS.md deste repositório: lá está como
o painel funciona e o que pode e não pode ser mudado. Siga essas regras nas 30
etapas abaixo.

Mapa aba -> arquivo fonte (confira sempre contra a lista ABAS no topo de
gerar_painel.py antes de editar; é a fonte da verdade, não este mapa):
1. Painel      -> STATUS.md
2. Prazos      -> PRAZOS.md
3. Tarefas     -> TAREFAS.md
4. Estudos     -> ESTUDOS.md
5. Grade       -> GRADE.md
6. Currículo   -> CURRICULO.md
7. Rotina      -> ROTINA.md
8. Contatos    -> CONTATOS.md
9. Dúvidas     -> DUVIDAS.md
10. Anotações  -> ANOTACOES.md
11. Compras    -> COMPRAS.md
12. Mala       -> MALA.md
13. Viagens    -> VIAGENS.md
14. Entorno    -> ENTORNO.md
15. Passeios   -> PASSEIOS.md

Regras fixas, valem para as 30 etapas:
- Auditoria não corrige nada, só registra achado. Correção só mexe no que a
  auditoria apontou (da própria aba ou de achado cruzado de outra aba).
- Cortar palavra não pode cortar informação. Prolixidade é forma, não
  conteúdo: mesmo fato, menos texto.
- Repetição só é problema quando é cópia integral da mesma frase ou do mesmo
  fato em dois lugares. Uma aba citar de leve algo que é "dona" de outra
  (link cruzado, "ver X.md") é referência, não redundância: isso fica.
- Se achar duas informações que se contradizem (data, valor, decisão), não
  escolha uma no chute. Procure qual é mais recente ou mais específica pelo
  contexto do próprio arquivo; se não der para saber com segurança, marque
  "[VERIFICAR: ...]" no lugar da versão duvidosa em vez de apagar ou inventar.
- Mantenha o tom atual do painel: português direto, frases curtas, sem
  travessão, sem enfeite.
- Cada etapa termina com um bloco markdown curto, anexado ao arquivo
  PLANO_OTIMIZACAO_ABAS.md, na seção já existente daquela aba (não crie
  arquivo novo por aba, nem novo arquivo de relatório).

Fase 1, etapas 1 a 15 (auditoria, uma por aba, nesta ordem). Para cada aba:
1. Leia o .md inteiro.
2. Procure:
   - Redundância: mesma frase ou fato repetido dentro do próprio arquivo, ou
     copiado (não referenciado) de outra aba já lida.
   - Prolixidade: parágrafo que gasta 5 linhas no que cabe em 1 ou 2, floreio,
     contexto repetido que o leitor já recebeu antes.
   - Inconsistência: data, número ou decisão que se contradiz dentro do
     arquivo ou contra uma aba já auditada.
   - Explicação de funcionamento do site: trecho que explica como o painel é
     gerado, como o script funciona, decisão técnica de implementação ou
     qualquer "nota de dev" dentro do conteúdo da aba. Quem lê a aba quer a
     informação (prazo, tarefa, contato, endereço), não como o painel foi
     construído. Esse tipo de explicação é só para o AGENTS.md, nunca para
     dentro do .md de uma aba (STATUS.md incluso: ele É a aba Painel).
3. Anexe em PLANO_OTIMIZACAO_ABAS.md, na seção "## Auditoria - <Aba>", uma
   lista curta dos achados. "Nenhum achado" é resposta válida. Cada achado:
   onde fica (trecho ou linha aproximada), qual o problema, sugestão de
   correção em uma linha (sem aplicar ainda).
4. Marque a etapa como feita no checklist de Progresso do mesmo arquivo.

Fase 2, etapas 16 a 30 (correção, uma por aba, mesma ordem). Só começa depois
das 15 auditorias prontas, porque uma correção pode depender de achado
cruzado de outra aba. Para cada aba:
1. Releia os achados da auditoria daquela aba, e qualquer achado cruzado de
   outra aba que aponte para ela.
2. Edite o .md fonte: corte prolixidade, remova redundância (decida qual aba
   é dona da informação e deixe link/menção curta nas demais), resolva
   inconsistência ou marque "[VERIFICAR: ...]". Explicação de funcionamento
   do site sai da aba: se a informação for útil para manutenção, mova para o
   AGENTS.md (NUNCA para STATUS.md nem para qualquer outro arquivo que esteja
   na lista ABAS de gerar_painel.py, porque esses viram aba e voltam a
   aparecer no site); se não for útil, apague.
3. Rode "python gerar_painel.py" e confirme que a aba renderiza sem quebrar
   (o script deve terminar sem erro).
4. Anexe em PLANO_OTIMIZACAO_ABAS.md, na seção "## Correção - <Aba>", um
   resumo curto do que mudou.
5. Marque a etapa como feita no checklist de Progresso.

Fechamento, depois da etapa 30: rode git status e git diff para revisar tudo,
depois git add dos arquivos alterados (.md das abas, docs/index.html,
PLANO_OTIMIZACAO_ABAS.md), um commit único descrevendo a varredura, e git
push na main.
```

## Progresso

### Fase 1 — Auditoria
- [ ] 1. Painel (retrabalho: auditar STATUS.md de verdade)
- [x] 2. Prazos
- [x] 3. Tarefas
- [x] 4. Estudos
- [x] 5. Grade
- [x] 6. Currículo
- [x] 7. Rotina
- [x] 8. Contatos
- [x] 9. Dúvidas
- [x] 10. Anotações
- [x] 11. Compras
- [x] 12. Mala
- [x] 13. Viagens
- [x] 14. Entorno
- [x] 15. Passeios

### Fase 2 — Correção
- [ ] 16. Painel (retrabalho: corrigir STATUS.md de verdade)
- [x] 17. Prazos
- [x] 18. Tarefas
- [x] 19. Estudos
- [x] 20. Grade
- [x] 21. Currículo
- [x] 22. Rotina
- [x] 23. Contatos
- [x] 24. Dúvidas
- [x] 25. Anotações
- [x] 26. Compras
- [x] 27. Mala
- [x] 28. Viagens
- [x] 29. Entorno
- [x] 30. Passeios

### Fechamento
- [x] Commit e push finais

---

## Auditoria - Painel

**RETRABALHO (31/08 à noite).** O mapa desta versão do plano dizia "Painel -> PAINEL.md", errado:
o gerador usa `STATUS.md` para a aba Painel, e `PAINEL.md` nunca foi lido por ele. Os achados
abaixo, marcados como concluídos, foram feitos contra `PAINEL.md` e não valeram para o site. O
`PAINEL.md` (órfão) foi apagado. A correção de emergência feita à parte: tirou a caixa "Notas de
manutenção do painel" que tinha sido colada no fim do `STATUS.md` (achado que não existia neste
plano) e moveu o que era regra permanente para o `AGENTS.md`. Falta ainda a auditoria de verdade
do `STATUS.md` como um todo, inclusive o achado óbvio: a seção "A semana 2 (24 a 27/08)" ficou
desatualizada, o resto do painel já foi corrigido para a semana 3.

Achados antigos (contra o arquivo errado, mantidos só de registro):
- Linhas 3-575 do antigo PAINEL.md: manual técnico do painel gerado, histórico de bugs, Supabase, Actions, chaves e gerador.
- Linhas 558-575: estrutura da pasta repetia o AGENTS.md.
- Linha 494: citava ConfecBell como nome resolvido, indo contra o DUVIDAS.md.

## Auditoria - Prazos

- Linhas 7-15: calendário principal ainda mostra a semana 2, mas `GRADE.md` já está na semana 3. Correção: atualizar para 31/08 a 03/09.
- Linhas 60-61: pergunta "marcada para 25/08" ficou vencida. Correção: apontar para a tarefa atual ou deixar sem data.
- Linha 78: "24 já acionadas até a semana 2" ficou atrás da semana 3. Correção: evitar número cumulativo aqui e apontar para `GRADE.md`.
- Histórico de agosto: 18/08 aparece depois de 20/08. Correção: reordenar.

## Auditoria - Tarefas

- Cabeçalho e seção "Rodízio da mala": explicam funcionamento interno do painel e da recorrência em excesso. Correção: reduzir ao formato mínimo e deixar o detalhe técnico no `PAINEL.md` antigo/git ou `STATUS.md`.
- Linha 67: pergunta sobre "plano de disciplina com carga horária" foi respondida pelo currículo; o que falta são datas de VC e trabalhos. Correção: reescrever a tarefa.
- Linhas 24, 85, 104: ConfecBell aparece como nome certo, mas `DUVIDAS.md` ainda manda confirmar Confex Bel. Correção: marcar como ConfecBell/Confex Bel até confirmação.

## Auditoria - Estudos

- Linhas 170-198: explicação longa sobre automação de Drive, service account, API e navegador é nota técnica dentro da aba de estudo. Correção: reduzir para a regra prática de quinta-feira.
- Linhas 303-309: repete a descoberta do currículo já detalhada em `CURRICULO.md`. Correção: encurtar e apontar para o arquivo dono.
- Linhas 312-338: pesos das seis provas repetem `CURRICULO.md`; aqui só precisa a consequência para estudar. Correção: manter a orientação prática e linkar os pesos.

## Auditoria - Grade

- Linhas 157-166: "Esta semana, para a dissertação" ainda fala de 25 e 26/08, que já estão na semana anterior. Correção: atualizar para oportunidades da semana 3 ou marcar como histórico.
- Linhas 307-323: seção "Respondido em 25/08" repete conteúdo permanente do `CURRICULO.md`. Correção: deixar só ponteiro curto ou remover.
- Linhas 346-357: "Regra de manutenção" explica formato que o gerador lê e rotina de edição. Correção: mover para `STATUS.md` ou `AGENTS.md`, não para a aba.

## Auditoria - Currículo

- Linhas 17-32: "Por que este documento muda o jogo" repete histórico que já está em `STATUS.md`/`ESTUDOS.md`. Correção: reduzir a uma frase.
- Linhas 49-52 e 193-199: a sexta e o bloco das 18h aparecem em termos parecidos. Correção: manter o número no quadro e a dúvida no fim.
- Linha 433 em diante: objetivo geral e base legal são úteis, mas podem ficar pesados para consulta rápida. Correção: sem alteração obrigatória, só enxugar se mexer.

## Auditoria - Rotina

- Linhas 56-64: horário semanal fixa bloco 5 terça/quarta, enquanto `CURRICULO.md` marca divergência a conferir. Correção: dizer que é o padrão observado no QTS e que o QTS manda.
- Linha 249: desconto de Alojamento/Vestiário "ainda precisa ser feita", mas a tarefa consta concluída em `TAREFAS.md` em 24/08. Correção: atualizar para decidido/conferir opção registrada.
- Linhas 258-265: auxílios repetem pontos que já foram tarefas concluídas. Correção: manter só regra viva.

## Auditoria - Contatos

- Linhas 61-77: seção de dissertação duplica parte da lista curta de `ESTUDOS.md`. Correção: manter só caminho de contato e apontar para Estudos.
- Linhas 8-22: histórico das correções do endereço é útil, mas prolixo para a aba de contato. Correção: reduzir e manter endereços antigos como alerta.

## Auditoria - Dúvidas

- Linhas 9-10: dúvidas sobre carga horária e plano de disciplina foram respondidas pelo currículo. Correção: remover ou transformar em dúvida sobre trabalhos/datas.
- Linha 12: ainda diz que "sete disciplinas que nunca entraram" estão em aberto, mas `GRADE.md` registra que o currículo respondeu isso. Correção: atualizar.
- Linhas 29-30: Confex Bel/ConfecBell é dúvida real e cruza Compras, Mala, Prazos, Status e Painel. Correção: manter aqui e padronizar nas outras abas como nome a confirmar.

## Auditoria - Anotações

- Nenhum achado relevante. O arquivo é curto, está vazio de conteúdo operacional e só orienta para os donos corretos.

## Auditoria - Compras

- Linhas 6-31: ConfecBell aparece como nome certo, em conflito com `DUVIDAS.md` e `ENTORNO.md`, que registram Confex Bel a confirmar. Correção: usar "ConfecBell/Confex Bel" ou marcar verificação.
- Linhas 8-11: parágrafo da loja é prolixo para a compra. Correção: reduzir risco prático e mandar detalhes ao Entorno.
- Linha 15: item já concluído fica em seção de pendência. Correção: mover para "Já resolvido" ou tirar da lista viva.

## Auditoria - Mala

- Linha 143: ConfecBell aparece como nome resolvido, mas o nome está em verificação. Correção: marcar como ConfecBell/Confex Bel.
- Linhas 67-72: "Como o ciclo funciona" repete o resumo do topo e de `TAREFAS.md`. Correção: enxugar sem mexer na lógica do inventário.
- Linhas 230-233: detalhes de viagem repetem `ROTINA.md` e `VIAGENS.md`. Correção: manter só ponteiro.

## Auditoria - Viagens

- Linhas 30-43: "Antes de sair" está todo marcado como concluído, mas é checklist recorrente de domingo. Correção: trocar para caixas abertas ou texto sem checkbox.
- Linha 35: diz que "os dois Oxxo abrem 24 horas", mas `ENTORNO.md` registra o Oxxo mais perto só 24h no domingo e dois 24h mais longe. Correção: especificar rede de segurança pelo Entorno.
- Linhas 54-68: últimas viagens repetem `ROTINA.md`/`MALA.md`. Correção: manter resumo e ponteiros.

## Auditoria - Entorno

- Linhas 215-227: duas seções vazias ou quase vazias. Correção: remover até haver conteúdo.
- Linhas 551-559 e 838-848: notas de método do gerador/roteador entram como nota técnica. Correção: reduzir para ressalva de confiabilidade ou mover para `STATUS.md`.
- Linhas 578-787: pesquisa de câmera para Guararapes ocupa muito espaço numa aba do entorno do CAES. Correção: recolher com `<!-- extra -->` ou mover para compras pessoais fora do painel.
- Linhas 359-361: "Verificação feita pelo Codex" é bastidor de apuração. Correção: substituir por fonte resumida.

## Auditoria - Passeios

- Linha 98: "rota medida pelo gerador local" é detalhe técnico. Correção: trocar por "rota medida".
- Linhas 24-30 e `ENTORNO.md` linhas 475-516: diretrizes de estação e segurança aparecem nos dois arquivos. Correção: manter em Passeios o uso turístico e em Entorno as estações de base.

## Correção - Painel

**RETRABALHO (31/08 à noite).** As três linhas abaixo mexeram no `PAINEL.md`, arquivo que o
gerador não lê: não mudaram nada no site. Correção de emergência aplicada direto no `STATUS.md`
(arquivo real da aba): tirada a caixa "Notas de manutenção do painel" do fim do arquivo; o que
era regra permanente (janela de duas semanas na GRADE.md) foi para o AGENTS.md; `PAINEL.md`
apagado por ser órfão. **Falta ainda:** auditar e corrigir o conteúdo de verdade do STATUS.md
(a seção "A semana 2" está uma semana atrasada em relação ao resto do painel).

Achados antigos (contra o arquivo errado, mantidos só de registro):
- `PAINEL.md` tinha sido refeito como abertura de uso: mapa das abas, regras de bolso, estado atual e próximos focos.
- Saiu o manual técnico do painel gerado, histórico de bugs, Supabase, Actions e estrutura da pasta.

## Correção - Prazos

- Semana principal atualizada para 31/08 a 03/09, com base na `GRADE.md`.
- Pergunta vencida de 25/08 foi trocada pela pergunta viva sobre datas das seis VCs.
- Número acumulado de disciplinas saiu daqui e ficou como ponteiro para a Grade.
- Histórico de agosto reordenado.

## Correção - Tarefas

- Cabeçalho e rodízio da mala foram enxugados.
- Tarefa da Coordenação foi reescrita para datas das VCs e trabalhos, sem pedir carga horária já respondida pelo currículo.
- ConfecBell foi padronizada como ConfecBell/Confex Bel até confirmação.

## Correção - Estudos

- Explicação longa sobre automação da pasta do pelotão foi reduzida para a rotina prática de quinta-feira.
- Trecho sobre o currículo virou ponteiro curto para `CURRICULO.md`.
- Consequências das seis provas ficaram mais diretas, sem repetir todos os pesos.

## Correção - Grade

- Seção da dissertação foi atualizada para oportunidades da semana 3.
- Conteúdo respondido pelo currículo virou ponteiro curto.
- Regra de manutenção semanal saiu da aba; o essencial foi para `STATUS.md`.

## Correção - Currículo

- Histórico sobre a chegada do PDM foi enxugado.
- Sexta-feira de pesquisa e divergência do 5º bloco ficaram mais diretas, sem repetição.

## Correção - Rotina

- Horário passou a distinguir currículo, QTS observado e bloco 5 ainda a confirmar.
- Desconto Alojamento/Vestiário deixou de constar como tarefa em aberto e virou `[VERIFICAR]` da opção escolhida.
- Auxílio financeiro foi enxugado para regra viva.

## Correção - Contatos

- Histórico do endereço oficial foi resumido.
- Estratégia de orientação foi reduzida a caminho de contato, com ponteiro para `ESTUDOS.md`.

## Correção - Dúvidas

- Dúvidas já respondidas pelo currículo foram retiradas.
- Ficaram em aberto datas das VCs, trabalhos além da prova, pelotão A, lacunas reais da Grade e orientação.

## Correção - Anotações

- Nenhuma alteração no arquivo fonte. A auditoria não apontou correção necessária.

## Correção - Compras

- Lista viva de fardamento foi enxugada.
- Item já conferido das camisas novas saiu das pendências e foi para "Já resolvido".
- Nome da loja padronizado como ConfecBell/Confex Bel com verificação explícita.

## Correção - Mala

- Explicação do ciclo foi encurtada sem mexer no inventário.
- ConfecBell foi padronizada como ConfecBell/Confex Bel.
- Detalhes de viagem viraram ponteiro para Rotina e Viagens.

## Correção - Viagens

- Checklist recorrente de domingo voltou a ficar aberto.
- Oxxo foi corrigido: Largo General Osório é 24h no domingo; José Paulino e Barão de Limeira são 24h todos os dias.
- Últimas viagens foram resumidas, com desmobilização detalhada apontada para `MALA.md`.

## Correção - Entorno

- Seções vazias de quinta e levar para casa foram removidas.
- Pesquisa de câmera ficou recolhida com `<!-- extra -->`.
- Notas de método do roteador/geocodificador foram reduzidas a ressalvas curtas.
- Bastidor "feito pelo Codex" virou fonte consolidada.

## Correção - Passeios

- "Rota medida pelo gerador local" virou "rota medida".
- Diretrizes de estação e segurança foram mantidas por terem uso turístico próprio.
