# Prática 1 --- Git & GitHub: versionamento e colaboração

## 1. Objetivos da aula

Ao final desta prática, o aluno deverá ser capaz de:

-   compreender por que sistemas de controle de versão são importantes
    no desenvolvimento web;
-   criar e configurar um repositório Git;
-   registrar alterações com commits;
-   trabalhar com branches;
-   sincronizar um projeto local com o GitHub;
-   utilizar Pull Requests;
-   resolver conflitos simples;
-   adotar uma convenção básica de commits e branches.

> **Contexto da disciplina:** em um projeto web distribuído, o código
> muda constantemente e várias pessoas podem trabalhar no backend,
> frontend, testes e infraestrutura ao mesmo tempo. O Git permite
> registrar essas mudanças e o GitHub fornece mecanismos de colaboração
> e revisão.

------------------------------------------------------------------------

## 2. O modelo mental do Git

Uma forma simples de visualizar o Git é:

``` text
Arquivos no computador
        |
        | git add
        v
Staging Area
        |
        | git commit
        v
Histórico local
        |
        | git push
        v
Repositório remoto (GitHub)
```

E para trazer alterações do GitHub:

``` text
GitHub
  |
  | git fetch / git pull
  v
Repositório local
```

### Comandos fundamentais

``` bash
git status
git add .
git commit -m "mensagem"
git log --oneline
git push
git pull
```

------------------------------------------------------------------------

## 3. Configuração inicial

Verifique a instalação:

``` bash
git --version
```

Configure identidade:

``` bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

Confira:

``` bash
git config --list
```

### Por que isso importa?

O Git registra autor e horário dos commits. A identidade configurada
localmente será associada aos commits criados naquele computador.

------------------------------------------------------------------------

# 4. Criando um projeto web

Vamos começar com um pequeno projeto:

``` text
hello-web/
├── index.html
├── css/
│   └── style.css
└── js/
    └── app.js
```

Crie a pasta e inicialize o Git:

``` bash
mkdir hello-web
cd hello-web
git init
```

Crie um `index.html`:

``` html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello Web</title>
</head>
<body>
    <h1>Olá, Sistemas Distribuídos!</h1>
    <button id="btn">Clique aqui</button>

    <script src="js/app.js"></script>
</body>
</html>
```

Agora:

``` bash
git status
```

O Git deverá indicar que `index.html` ainda não está sendo rastreado.

------------------------------------------------------------------------

# 5. Primeiro commit

Adicione o arquivo:

``` bash
git add index.html
```

Confira o staging:

``` bash
git status
```

Crie o commit:

``` bash
git commit -m "feat: adiciona página inicial"
```

Veja o histórico:

``` bash
git log --oneline
```

### O que aconteceu?

-   `git add` colocou o arquivo na área de preparação;
-   `git commit` criou uma versão registrada do projeto;
-   o commit pode ser recuperado posteriormente.

------------------------------------------------------------------------

# 6. Commit não é simplesmente "salvar"

Um erro comum é pensar:

> "Cada vez que salvo o arquivo, tenho um commit."

Não é isso.

O fluxo é:

``` text
Editar
  ↓
git status
  ↓
git add
  ↓
git commit
```

O commit representa um **ponto relevante do histórico do projeto**.

Exemplo:

``` bash
git add .
git commit -m "feat: adiciona interação do botão"
```

Evite commits vagos:

``` text
"mudanças"
"update"
"coisas"
"teste"
```

Prefira:

``` text
feat: adiciona botão de login
fix: corrige validação do formulário
docs: atualiza instruções de execução
test: adiciona teste para autenticação
```

------------------------------------------------------------------------

# 7. `.gitignore`

Nem tudo que existe no computador deve ir para o repositório.

Crie:

``` text
.gitignore
```

Exemplo:

``` gitignore
# Dependências
node_modules/

# Ambiente virtual Python
.venv/
venv/

# Variáveis de ambiente
.env

# Cache
__pycache__/
.pytest_cache/

# IDE
.vscode/
.idea/

# Sistema operacional
.DS_Store
Thumbs.db
```

### Por que isso é importante?

Um projeto web normalmente possui:

-   dependências instaladas;
-   arquivos temporários;
-   caches;
-   credenciais;
-   configurações específicas da máquina.

Esses arquivos não devem ser versionados indiscriminadamente.

> **Atenção:** `.gitignore` não é mecanismo de segurança. Se um segredo
> já foi commitado, simplesmente adicioná-lo ao `.gitignore` não remove
> o segredo do histórico.

------------------------------------------------------------------------

# 8. Branches

Branches permitem trabalhar em funcionalidades diferentes sem modificar
diretamente a linha principal de desenvolvimento.

Visualmente:

``` text
main
 |
 o---o---o
          \
           o---o  feature/login
```

Crie uma branch:

``` bash
git switch -c feature/login
```

Confira:

``` bash
git branch
```

Faça uma alteração e registre:

``` bash
git add .
git commit -m "feat: adiciona estrutura da tela de login"
```

Volte para `main`:

``` bash
git switch main
```

Crie outra branch:

``` bash
git switch -c fix/botao
```

------------------------------------------------------------------------

# 9. Estratégia simples de branches

Para a disciplina, uma convenção simples pode ser:

``` text
main
develop
feature/nome-da-funcionalidade
fix/nome-do-problema
test/nome-do-teste
docs/nome-da-documentacao
```

Exemplos:

``` bash
git switch -c feature/cadastro-usuario
git switch -c fix/validacao-email
git switch -c test/login
git switch -c docs/readme
```

Uma branch deve representar uma mudança relativamente bem definida.

------------------------------------------------------------------------

# 10. Merge

Suponha:

``` text
main
 |
 o---o
      \
       o---o feature/login
```

Para incorporar a funcionalidade:

``` bash
git switch main
git merge feature/login
```

Depois:

``` bash
git branch -d feature/login
```

### Merge na prática

``` bash
git switch main
git pull origin main

git merge feature/login

git push origin main
```

------------------------------------------------------------------------

# 11. Rebase: introdução

Outra possibilidade é utilizar `rebase` para atualizar uma branch em
relação à base mais recente.

Exemplo:

``` bash
git switch feature/login
git fetch origin
git rebase origin/main
```

O objetivo é atualizar a branch antes de abrir um Pull Request.

### Merge x Rebase

**Merge:**

``` text
main:    A---B---C
              \
feature:       D---E
                    \
                     M
```

**Rebase:**

``` text
main:    A---B---C
                  \
feature:           D'---E'
```

Para iniciantes, o mais importante é compreender:

-   `merge` preserva a junção entre históricos;
-   `rebase` reorganiza a base dos commits;
-   rebase exige mais cuidado quando a branch já foi compartilhada com
    outras pessoas.

------------------------------------------------------------------------

# 12. GitHub

Crie um repositório no GitHub e conecte o projeto local:

``` bash
git remote add origin https://github.com/SEU_USUARIO/hello-web.git
```

Verifique:

``` bash
git remote -v
```

Envie a branch:

``` bash
git push -u origin main
```

Depois disso, normalmente:

``` bash
git push
```

e:

``` bash
git pull
```

------------------------------------------------------------------------

# 13. `fetch` x `pull`

Esta diferença é muito importante em projetos colaborativos.

### `git fetch`

Baixa informações do repositório remoto sem alterar diretamente sua
branch atual:

``` bash
git fetch origin
```

Depois você pode analisar:

``` bash
git log --oneline origin/main
```

### `git pull`

É uma operação de atualização da branch local, normalmente equivalente a
buscar alterações e integrá-las:

``` bash
git pull origin main
```

Uma prática interessante é usar:

``` bash
git fetch origin
```

antes de decidir como integrar as alterações.

------------------------------------------------------------------------

# 14. Pull Request

Em um projeto colaborativo, normalmente não é necessário permitir que
todos alterem `main` diretamente.

Fluxo:

``` text
1. Atualizar main/develop
        ↓
2. Criar branch
        ↓
3. Implementar
        ↓
4. Commit
        ↓
5. Push
        ↓
6. Pull Request
        ↓
7. Code Review
        ↓
8. Merge
```

Exemplo:

``` bash
git switch develop
git pull origin develop

git switch -c feature/listagem-produtos

# desenvolver...

git add .
git commit -m "feat: adiciona listagem de produtos"
git push -u origin feature/listagem-produtos
```

Depois, abrir um Pull Request no GitHub.

------------------------------------------------------------------------

# 15. Pull Request como ferramenta de engenharia

Um PR não serve apenas para "mandar código".

Ele pode conter:

-   descrição do problema;
-   solução adotada;
-   evidências;
-   testes realizados;
-   possíveis impactos;
-   checklist;
-   revisão por outros desenvolvedores.

Exemplo de descrição:

``` markdown
## Objetivo

Adicionar a tela de listagem de produtos.

## Alterações

- adiciona estrutura HTML;
- adiciona estilos CSS;
- adiciona carregamento dos produtos;
- adiciona tratamento para lista vazia.

## Como testar

1. executar a aplicação;
2. acessar `/produtos`;
3. verificar a listagem;
4. verificar o comportamento quando não existem produtos.

## Testes

- [x] Teste manual da listagem
- [x] Teste de lista vazia
```

------------------------------------------------------------------------

# 16. Conflitos

Um conflito acontece quando o Git não consegue decidir automaticamente
qual alteração deve permanecer.

Exemplo:

``` text
<<<<<<< HEAD
<h1>Produtos</h1>
=======
<h1>Meus produtos</h1>
>>>>>>> feature/titulo
```

O desenvolvedor deve decidir o resultado final:

``` html
<h1>Meus produtos</h1>
```

Depois:

``` bash
git add index.html
git commit
```

### Regra importante

Não "resolva" um conflito simplesmente escolhendo qualquer lado.

Entenda o que cada alteração representa.

------------------------------------------------------------------------

# 17. Comandos para diagnóstico

Durante uma aula prática, estes comandos serão muito úteis:

``` bash
git status
git log --oneline --graph --all
git branch
git remote -v
git diff
git diff --staged
```

### `git diff`

Mostra alterações ainda não adicionadas:

``` bash
git diff
```

### `git diff --staged`

Mostra alterações que entrarão no próximo commit:

``` bash
git diff --staged
```

------------------------------------------------------------------------

# 18. Checklist

-   [ ] Sei explicar o que é Git.
-   [ ] Sei diferenciar Git e GitHub.
-   [ ] Sei criar um repositório.
-   [ ] Sei fazer um commit.
-   [ ] Sei criar e trocar de branch.
-   [ ] Sei fazer push e pull.
-   [ ] Sei explicar `fetch` x `pull`.
-   [ ] Sei abrir um Pull Request.
-   [ ] Sei resolver um conflito simples.
-   [ ] Sei criar um `.gitignore`.
-   [ ] Sei escrever commits descritivos.

## Conexão com as próximas aulas

O código que versionamos nesta aula será a base para as próximas
práticas:

``` text
Git/GitHub
    ↓
Ambiente reprodutível
    ↓
Poetry / Dependências
    ↓
Makefile / Automação
    ↓
Backend FastAPI
    ↓
PostgreSQL
    ↓
Testes
    ↓
Docker
    ↓
Frontend JavaScript
    ↓
Integração Full-Stack
```
