# Sincronizar as tarefas (Supabase)

## ✅ O ciclo fecha sozinho (14/08/2026)

A nuvem volta para o `TAREFAS.md` sem ninguém copiar nada. Quem faz isso é
`sincroniza_tarefas.py`, rodado de hora em hora pela Action
[sincronizar-tarefas.yml](.github/workflows/sincronizar-tarefas.yml). A explicação de como
ele decide quem manda está em [PAINEL.md](PAINEL.md).

**Os dois Secrets do repositório** (Settings → Secrets and variables → Actions):

| Secret | O que é |
|---|---|
| `SUPABASE_EMAIL` | o mesmo e-mail do login do painel |
| `SUPABASE_SENHA` | a mesma senha |

É o login normal, não chave de serviço: o RLS entrega só as suas linhas. Secret de
repositório não aparece na página, nem no log da Action, e Action de fork não enxerga.
Se um dia trocar a senha do Supabase, troque o `SUPABASE_SENHA` junto, senão a Action
começa a falhar em silêncio (ela fica vermelha na aba Actions).

Para rodar na mão, em qualquer máquina:

```powershell
$env:SUPABASE_EMAIL = "..."; $env:SUPABASE_SENHA = "..."
python sincroniza_tarefas.py --conferir   # só mostra o que faria
python sincroniza_tarefas.py              # escreve
```

## ✅ Já está ligado (04/08/2026)

- **Projeto**: `relatorio-ronda` (o mesmo dos relatórios, org `esdraaline's Org`)
- **Tabela**: `public.cao_tarefas`, com RLS ativo e política `cao_tarefas_owner`
- **Login**: o e-mail de sempre (o mesmo usuário que já existia no projeto)
- **Configuração**: arquivo `supabase.json` na raiz

## ✅ Itens ticados também sincronizam (04/08/2026)

O que você tica nas abas **Compras e Mala** sobe junto com as tarefas.

- **Tabela**: `public.cao_ticados`, RLS ativo, política `dono_faz_tudo`
- Conferido na hora de ligar: a tabela responde, as colunas `user_id, id, n, mod` existem, o
  upsert por `(user_id, id)` é aceito e **sem login não devolve nem grava nada**.
- **Testado de ponta a ponta pelo Josemar em 04/08/2026**: ticou em um aparelho e apareceu no outro.
- Em cada aparelho novo, entrar uma vez em **Tarefas → Entrar** (o mesmo login das tarefas).

O SQL usado fica abaixo, como referência caso precise refazer.

```sql
create table if not exists public.cao_ticados (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  id      text not null,
  n       integer not null default 0,
  mod     timestamptz not null default now(),
  primary key (user_id, id)
);

alter table public.cao_ticados enable row level security;

drop policy if exists "dono_faz_tudo" on public.cao_ticados;
create policy "dono_faz_tudo" on public.cao_ticados
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

> **Atenção à chave primária**: aqui ela é `(user_id, id)`, e não só `id` como na `cao_tarefas`.
> O motivo é que o `id` de um item ticado vem do texto dele (`ab-compras/2de055d428`), então é
> **igual em todos os aparelhos e para todas as pessoas**. Sem o `user_id` na chave, duas pessoas
> usando o mesmo projeto sobrescreveriam a marcação uma da outra.

Conferido na hora de ligar: sem estar logado, a chave não devolve nada, nem de `cao_tarefas`
nem de `relatorios`. As tabelas do relatório de ronda continuam protegidas.

**Para usar em outro aparelho** (celular, outro PC): abra o painel, vá em **Tarefas** →
**Entrar** e use o mesmo e-mail e senha. Só precisa fazer isso uma vez por aparelho.

O passo a passo abaixo fica como referência, caso um dia precise refazer ou mudar de projeto.

---

## 1. Escolher o projeto

Pode ser um projeto novo **ou um que você já tenha** (ex.: `relatorio-ronda`). Tabelas
diferentes não se misturam, e o RLS é por tabela, então um não atrapalha o outro. A tabela
daqui se chama `cao_tarefas` justamente para não colidir com nada.

**Se for usar um projeto novo:**
1. https://supabase.com → **New project**. Nome: `central-cao`. Região: **South America (São Paulo)**.
2. Guarde no gerenciador de senhas a senha de banco que ele gerar (é do banco, não é a do painel).
3. Espere uns 2 minutos.

**Se for aproveitar um projeto existente**, faça antes a verificação do passo 2.

## 2. Conferir a segurança do projeto (só se for reaproveitar um)

A chave `anon` é a mesma para o projeto inteiro, e ela vai ficar dentro de uma página pública.
Isso é seguro para toda tabela que tenha RLS ligado. Então antes vale conferir se **nenhuma**
tabela ficou sem.

No **SQL Editor**, rode:

```sql
select tablename,
       case when rowsecurity then 'protegida' else 'SEM RLS — CORRIGIR' end as situacao
from pg_tables
where schemaname = 'public'
order by rowsecurity, tablename;
```

Se aparecer alguma linha **SEM RLS**, me avise antes de continuar: aquela tabela ficaria
legível por quem tivesse a chave. Se estiver tudo "protegida", pode seguir tranquilo.

## 3. Criar a tabela

No **SQL Editor** → **New query**, cole o bloco abaixo inteiro e clique em **Run**.

```sql
create table if not exists public.cao_tarefas (
  id      text primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  txt     text not null,
  data    date,
  cat     text default '',
  feito   boolean not null default false,
  mod     timestamptz not null default now()
);

alter table public.cao_tarefas enable row level security;

-- cada pessoa enxerga e mexe apenas nas proprias tarefas
drop policy if exists "dono_faz_tudo" on public.cao_tarefas;
create policy "dono_faz_tudo" on public.cao_tarefas
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create index if not exists cao_tarefas_user_idx on public.cao_tarefas (user_id);
```

Precisa aparecer **Success. No rows returned**.

> A linha `enable row level security` é a que protege tudo: mesmo o painel sendo público,
> ninguém enxerga suas tarefas sem estar logado com a sua conta.

## 4. Criar o seu usuário

1. Menu lateral: **Authentication** → **Users** → **Add user** → **Create new user**.
2. Coloque seu e-mail e escolha uma senha. Marque **Auto Confirm User** (assim não precisa
   confirmar por e-mail).
3. Essa é a senha que você vai digitar no painel, no botão **Entrar**.

## 5. Pegar as chaves do projeto

Menu lateral: **Project Settings** (engrenagem) → **API**. Você vai precisar de dois valores:

- **Project URL**, algo como `https://abcdefgh.supabase.co`
- **anon public** (em Project API keys), uma chave longa começando com `eyJ...`

⚠️ Pegue a chave **anon public**. **Nunca** a `service_role`: essa ignora todas as regras
de segurança e não pode sair do servidor.

## 6. Ligar no painel

Crie o arquivo `supabase.json` na pasta `Central CAO` com este conteúdo, trocando pelos
seus valores:

```json
{
  "url": "https://SEU-PROJETO.supabase.co",
  "anonKey": "eyJ..."
}
```

Depois rode:

```
python gerar_painel.py
```

Abra o painel, vá em **Tarefas** → **Entrar**, coloque o e-mail e a senha do passo 4.
O indicador no canto deve mudar para **Sincronizado**.

No celular, abra o painel e entre com o mesmo e-mail e senha. Você só faz isso **uma vez
por aparelho**: depois a sessão fica salva.

---

## Perguntas que vão aparecer

**A chave anon fica visível no site público. Isso é problema?**
Não. Ela foi feita para ficar no navegador, ela só identifica o projeto. Quem protege os
dados é o RLS do passo 2 mais o seu login. Sem estar logado com a sua conta, a chave não
mostra nada.

**E se eu ficar sem internet?**
O painel continua funcionando: as tarefas são salvas no aparelho na hora e sobem sozinhas
quando a conexão voltar.

**Se eu editar a mesma tarefa no PC e no celular?**
Vale a alteração mais recente.

**Preciso continuar usando o Exportar?**
Com a sincronização ligada, não é mais obrigatório para não perder dados. Mas continua
sendo útil de vez em quando, porque é o que coloca as tarefas dentro do repositório e me
permite ler o histórico nas próximas sessões.

**Posso usar o mesmo projeto de outro sistema meu?**
Pode. A tabela `cao_tarefas` não conversa com as outras, e o RLS é definido tabela a tabela.
O único cuidado é o do passo 2: garantir que nenhuma tabela daquele projeto esteja sem RLS,
já que a chave `anon` passa a circular numa página pública.

**O login vale para os dois sistemas?**
Sim, o Authentication é do projeto inteiro. Quem tem conta lá consegue entrar aqui também,
mas por causa do RLS só enxerga as próprias tarefas, ou seja, nada suas.

**Quero desligar tudo isso.**
Apague o `supabase.json` e rode `python gerar_painel.py` de novo. O painel volta ao modo
somente local, sem perder nada do que está no aparelho.
