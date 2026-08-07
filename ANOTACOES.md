# ANOTAÇÕES — CAO 2026

> Notas soltas, recados, ideias, coisas que não se encaixam em prazo/tarefa/dúvida.

## 06/08/2026 — Publicação passou a ser automática (GitHub Actions)

**O que mudou na prática:** não precisa mais rodar `python gerar_painel.py` e
commitar para o painel publicado atualizar. Basta editar qualquer `.md` e dar
push (ou editar direto pela web do GitHub, pelo celular): o workflow
`.github/workflows/publicar-painel.yml` regenera o painel, guarda o
`docs/index.html` no repositório e publica. Rodar o gerador na mão continua
funcionando e é útil para ver o resultado antes de subir.

**Por que mudou.** Duas razões. A primeira é autonomia: com o CAO começando, o
painel editado pelo celular ficaria velho em silêncio. A segunda é que o build
antigo do Pages quebrou.

**O episódio do build quebrado, para não investigar de novo do zero.** Em
06/08/2026 o build "legacy" do Pages (servir direto da pasta `docs/` do branch)
passou a falhar com a mensagem genérica `Page build failed`, sem log nenhum.
Descartado, testando: não era conteúdo (sem symlink, `.nojekyll` no lugar,
arquivo cresceu só de 139 KB para 143 KB), não era incidente declarado (página
de status do GitHub toda operacional), não era plano nem visibilidade
(repositório público). **A prova de que não era deste repositório:** o
`mentor-univesp-com170`, mesma conta e mesmo mecanismo, começou a falhar no
mesmo dia, tendo funcionado até 00h07 UTC. Os builds duravam ~29 s antes de
falhar, dentro da faixa normal, então não era rejeição imediata.

Reaplicar a configuração de source e empurrar commit novo **não** recuperou.
Migrar para Actions resolveu o diagnóstico, porque o modo legacy não expõe log:
o log da Action mostrou o deploy preso em `deployment_in_progress` até estourar
o limite de 10 minutos da própria Action, enquanto o GitHub seguia processando.
Minutos depois o site aparecia atualizado. Ou seja, **era a Action desistindo
cedo, não o deploy falhando**. Por isso o `timeout` do `deploy-pages` está em 30
minutos no workflow.

**Se um dia a publicação parecer travada:** olhe o final da Action. O último
passo compara o carimbo `gerado-em` do arquivo local com o que está sendo
servido de verdade e falha se forem diferentes. Isso existe porque nesta sessão
o site ficou uma hora servindo a versão de 04/08 enquanto os commits subiam
normalmente, e nada avisava.

**Erro cometido no caminho, registrado para não se repetir:** a falha começou
exatamente no commit que introduziu um `.gitattributes`, e concluí que era ele a
causa. Removi o arquivo, e o build continuou falhando. Era coincidência de
timing. O `.gitattributes` foi removido por um motivo que não se confirmou; a
correção de fim de linha que importava (`newline="\n"` no `gerar_painel.py`)
ficou e está testada.

## 04/08/2026 — Criação da Central do CAO
- Pasta organizada e limpa (ver detalhes abaixo).
- Quando for criar o repositório no GitHub: **não subir a pasta `CAO 2026/Estudo/`, `CAO 2026/Inscrição/` nem `CAO 2026/PP/Trabalhos de Referencia/`** — são PDFs pesados, material de curso pago (direitos autorais) e documentos pessoais (dados de inscrição, comprovante de depósito). Colocar em `.gitignore`. Só os `.md` da raiz (STATUS/PRAZOS/DUVIDAS/TAREFAS/ANOTACOES/VIAGENS) e talvez modelos/templates leves entram no repositório.
- Limpeza feita: removidos duplicados exatos, 2 arquivos `.exe` (lixo dentro do material antigo) e ~975 MB de áudio/vídeo de aulas antigas do ciclo 2021 (WhatsApp), já que existe cópia completa no Google Drive. Total liberado: ~1 GB (de 1,66 GB para ~640 MB).
- Pasta "CAO 2021" renomeada para "Material de Ciclos Anteriores (CAO 2021)" pra ficar claro que é referência de edital anterior, não do ciclo atual.
- Criada a pasta `CAO 2026/Curso/` para material do curso em andamento (hoje só tem o aviso de recepção do SAE).

## 04/08/2026 — Correção de turma + leitura do slide de recepção do SAE
- **Correção**: não sou da 1ª Turma (CAO-I/26, fev/26–fev/27) como eu tinha assumido pelo edital — sou da **2ª Turma (CAO-II/26, ago/26–ago/27)**, no CAES "Cel Nelson Freire Terra".
- O curso agora é um **Programa de Mestrado Profissional em Ciências Policiais de Segurança e Ordem Pública** — o PP da seleção deve virar dissertação (contato: Cap Gobbo, caespesquisa@policiamilitar.sp.gov.br).
- Todo o conteúdo do slide de recepção (organograma, contatos, rotina, SIPA, formatura, facilities) foi extraído para [CONTATOS.md](CONTATOS.md) e [ROTINA.md](ROTINA.md) — o PDF original continua em [CAO 2026/Curso/](CAO%202026/Curso/) como fonte.

## 04/08/2026 — Painel visual (docs/index.html)
- Criado o painel HTML com abas, busca global (Ctrl+K), tema claro/escuro e os prazos/tarefas em destaque na abertura.
- **Arquitetura**: os .md são a fonte de verdade, o `gerar_painel.py` lê todos eles e cospe `docs/index.html`. Editar o HTML direto não adianta, a próxima geração sobrescreve.
- O script é Python puro, sem instalar nada. Funciona em qualquer máquina que tenha Python.
- **Decisão sobre publicação**: vai para GitHub Pages público, com a ressalva de que o painel contém organograma do CAES, e-mails funcionais, código SEI e meu RE. Avaliei e segui assim. Mitigações aplicadas: `noindex/nofollow` (não entra em busca do Google) e o Pages serve **só a pasta `docs/`**, então o resto do repositório nunca vira URL acessível.
- A pasta `CAO 2026/` está no `.gitignore` inteira (PDFs pesados, material de curso pago, documentos pessoais).

## 04/08/2026 — Cadastro de tarefas no painel
- A aba Tarefas virou um app de verdade: cadastro com data em linguagem normal ("entregar artigo sexta",
  "prova dia 15", "em 3 dias"), agrupamento por urgência, categorias coloridas, editar e excluir.
- **Onde os dados ficam**: localStorage do navegador. Isso é por aparelho e por endereço, ou seja,
  o que eu cadastro no PC não aparece no celular, e o arquivo local não compartilha com o Pages.
  Por isso existe o botão **Exportar**, que devolve o `TAREFAS.md` pronto: é ele que leva as tarefas
  para o repositório e me deixa enxergar o histórico nas próximas sessões.
- O formato do TAREFAS.md ganhou data e categoria: `- [ ] texto [dd/mm/aaaa] #categoria`. É ida e volta:
  o painel lê do arquivo e escreve de volta no mesmo formato.
- **Sincronização ligada no mesmo dia**, reaproveitando o projeto Supabase `relatorio-ronda` em vez de
  criar um novo. Tabela `cao_tarefas` (nome com prefixo justamente para não colidir com `rascunho` e
  `relatorios`, que já existiam). Antes de ligar, conferi que as duas tabelas antigas têm RLS com
  política `auth.uid() = user_id`, e testei que a chave sem login não devolve nada de nenhuma delas.
- O login do Supabase é do projeto inteiro, então o usuário que já existia serve
  para os dois sistemas. O RLS é que mantém os dados separados.
- Repositório publicado em `github.com/esdraaline/central-cao` (conta esdraaline), painel no ar em
  `esdraaline.github.io/central-cao`, servido a partir da pasta `docs/`.

## 04/08/2026 — Dois bugs achados no teste da sincronização
- **Falso "Sem conexão"**: o Supabase responde com corpo vazio e status 200 quando a requisição usa
  `Prefer: return=minimal`. O código só tratava corpo vazio no status 204 exato; nos demais tentava
  `r.json()` numa string vazia, o parse quebrava, e uma gravação bem-sucedida aparecia como falha.
  A tarefa ficava salva no banco mas o painel dizia que não. Corrigido lendo como texto antes.
- **Cache do navegador servindo versão antiga**: o painel é um arquivo único regerado a cada mudança.
  Depois de publicar a correção acima, o Chrome continuou servindo a cópia velha, e o bug parecia
  não ter sido corrigido. Resolvido com cabeçalho de revalidação e um carimbo de versão no `<head>`.
  **Se um dia uma correção parecer não ter chegado, é o primeiro suspeito**: force com Ctrl+F5.
- O `gerar_painel.py` recusa gerar se a chave do `supabase.json` for a `service_role` (ela ignora o RLS
  e não pode ir para site público). Só aceita a `anon`.
- A chave `anon` fica visível no HTML publicado, e isso é esperado: ela só identifica o projeto.
  Quem protege os dados é o RLS no banco mais o login.
