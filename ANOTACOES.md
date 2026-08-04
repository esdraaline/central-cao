# ANOTAÇÕES — CAO 2026

> Notas soltas, recados, ideias, coisas que não se encaixam em prazo/tarefa/dúvida.

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
- O login do Supabase é do projeto inteiro, então o usuário `josemardp@gmail.com` que já existia serve
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
