# Prática 1 --- Makefile: automação de comandos

## 1. Objetivos da aula

Ao final desta prática, o aluno deverá ser capaz de:

-   compreender o problema de automação de tarefas;
-   entender a estrutura de um `Makefile`;
-   criar comandos padronizados para um projeto web;
-   executar instalação, testes, lint e servidor por atalhos;
-   utilizar variáveis e dependências simples;
-   combinar Makefile com Poetry;
-   preparar o projeto para futuras práticas de Docker e CI/CD.

> **Contexto:** conforme um projeto web cresce, surgem vários comandos
> repetitivos. Um desenvolvedor pode precisar lembrar comandos
> diferentes para instalar dependências, executar testes, iniciar o
> backend, verificar qualidade do código e limpar arquivos temporários.
> O Makefile cria uma interface simples para essas tarefas.

------------------------------------------------------------------------

# 2. O problema

Imagine que para trabalhar no projeto seja necessário executar:

``` bash
poetry install
poetry run pytest
poetry run ruff check .
poetry run uvicorn app.main:app --reload
```

Isso funciona.

Mas imagine um projeto maior com:

``` text
instalação
testes
lint
format
servidor
migrações
Docker
logs
limpeza
build
```

A quantidade de comandos aumenta.

Podemos criar atalhos:

``` bash
make install
make test
make lint
make run
```

------------------------------------------------------------------------

# 3. O que é um Makefile?

Um `Makefile` contém regras.

Estrutura:

``` makefile
alvo:
    comando
```

Exemplo:

``` makefile
hello:
    echo "Olá, Sistemas Distribuídos!"
```

Execute:

``` bash
make hello
```

Resultado:

``` text
Olá, Sistemas Distribuídos!
```

> **Atenção:** em Makefiles, a linha do comando deve normalmente começar
> com uma tabulação (`TAB`), não com espaços.

------------------------------------------------------------------------

# 4. Primeiro Makefile para um projeto Python

Considere:

``` text
backend/
├── Makefile
├── pyproject.toml
├── poetry.lock
├── src/
└── tests/
```

Podemos começar com:

``` makefile
install:
    poetry install

test:
    poetry run pytest

run:
    poetry run uvicorn app.main:app --reload
```

Agora:

``` bash
make install
```

ou:

``` bash
make test
```

ou:

``` bash
make run
```

------------------------------------------------------------------------

# 5. Por que isso é útil?

Compare:

``` bash
poetry run uvicorn app.main:app --reload
```

com:

``` bash
make run
```

O segundo é mais fácil de memorizar.

Além disso, se a forma de executar o servidor mudar:

``` bash
poetry run uvicorn app.main:app --reload --port 8000
```

o desenvolvedor não precisa decorar a mudança.

O Makefile passa a ser a interface do projeto:

``` text
Desenvolvedor
     ↓
make run
     ↓
Makefile
     ↓
comando real
```

------------------------------------------------------------------------

# 6. Targets

Um `Makefile` pode ter vários targets:

``` makefile
install:
    poetry install

test:
    poetry run pytest

lint:
    poetry run ruff check .

format:
    poetry run ruff format .

run:
    poetry run uvicorn app.main:app --reload
```

Agora temos:

``` bash
make install
make test
make lint
make format
make run
```

------------------------------------------------------------------------

# 7. Um target padrão

Podemos criar um target `help`:

``` makefile
help:
    @echo "Comandos disponíveis:"
    @echo "  make install  - instala dependências"
    @echo "  make test     - executa testes"
    @echo "  make lint     - verifica código"
    @echo "  make format   - formata código"
    @echo "  make run      - inicia servidor"
```

Execute:

``` bash
make help
```

O `@` evita que o próprio comando seja impresso antes da saída.

------------------------------------------------------------------------

# 8. `.PHONY`

Alguns targets não representam arquivos.

Por exemplo:

``` makefile
test:
    poetry run pytest
```

Queremos que `make test` execute o teste sempre.

Podemos declarar:

``` makefile
.PHONY: install test lint format run help
```

Exemplo completo:

``` makefile
.PHONY: install test lint format run help

install:
    poetry install

test:
    poetry run pytest

lint:
    poetry run ruff check .

format:
    poetry run ruff format .

run:
    poetry run uvicorn app.main:app --reload

help:
    @echo "make install"
    @echo "make test"
    @echo "make lint"
    @echo "make format"
    @echo "make run"
```

------------------------------------------------------------------------

# 9. Dependências entre targets

Um target pode depender de outro.

Exemplo:

``` makefile
test: install
    poetry run pytest
```

Isso significa:

``` text
make test
    ↓
make install
    ↓
pytest
```

Porém, em projetos reais devemos tomar cuidado para não reinstalar tudo
desnecessariamente.

Uma alternativa simples é manter:

``` makefile
install:
    poetry install

test:
    poetry run pytest
```

e deixar o desenvolvedor executar:

``` bash
make install
make test
```

------------------------------------------------------------------------

# 10. Variáveis

Podemos evitar repetir comandos:

``` makefile
PYTHON := poetry run python
PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
```

Depois:

``` makefile
test:
    $(PYTEST)

run:
    $(UVICORN) app.main:app --reload
```

Isso facilita alterações futuras.

------------------------------------------------------------------------

# 11. Exemplo mais completo

Um Makefile inicial para a disciplina:

``` makefile
.PHONY: help install test lint format run clean

PYTHON := poetry run python
PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
RUFF := poetry run ruff

help:
    @echo "Comandos disponíveis:"
    @echo "  make install  - instala dependências"
    @echo "  make test     - executa testes"
    @echo "  make lint     - verifica o código"
    @echo "  make format   - formata o código"
    @echo "  make run      - inicia o servidor"
    @echo "  make clean    - remove arquivos temporários"

install:
    poetry install

test:
    $(PYTEST)

lint:
    $(RUFF) check .

format:
    $(RUFF) format .

run:
    $(UVICORN) app.main:app --reload

clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
```

------------------------------------------------------------------------

# 12. Atenção ao sistema operacional

O comando:

``` bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

é comum em ambientes Unix/Linux/macOS.

No Windows, dependendo do shell utilizado, ele pode não funcionar da
mesma maneira.

Isso é uma boa oportunidade para discutir um problema importante:

> **Automação também precisa considerar o ambiente de execução.**

Para uma disciplina que utilizará Docker futuramente, podemos reduzir
essa diferença colocando determinadas tarefas dentro de containers.

------------------------------------------------------------------------

# 13. Makefile e desenvolvimento web

Nosso fluxo começa a ficar:

``` text
                 ┌──────────────┐
                 │ Desenvolvedor│
                 └──────┬───────┘
                        │
                     make
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
     install           test            run
        │               │               │
     Poetry           Pytest          Uvicorn
        │               │               │
        └───────────────┼───────────────┘
                        ↓
                    Backend
```

O Makefile funciona como uma camada de automação sobre as ferramentas do
projeto.

------------------------------------------------------------------------

# 14. Comandos úteis

Descobrir os targets:

``` bash
make help
```

Instalar:

``` bash
make install
```

Testar:

``` bash
make test
```

Verificar qualidade:

``` bash
make lint
```

Formatar:

``` bash
make format
```

Executar:

``` bash
make run
```

------------------------------------------------------------------------

# 15. Integração com Git

O Makefile também faz parte do código do projeto.

Portanto:

``` bash
git add Makefile
git commit -m "build: adiciona automação com Makefile"
```

E o arquivo deve ser compartilhado com a equipe.

Assim, todos podem usar os mesmos comandos:

``` text
Aluno A ──┐
Aluno B ──┼──→ Makefile ──→ comandos padronizados
Aluno C ──┘
```

------------------------------------------------------------------------

# 16. Makefile + Poetry + Git

Agora podemos visualizar o papel de cada ferramenta:

``` text
Git
 │
 ├── versionamento
 ├── branches
 └── colaboração
        │
        ↓
Poetry
 │
 ├── dependências
 ├── ambiente
 └── projeto Python
        │
        ↓
Makefile
 │
 ├── comandos padronizados
 ├── testes
 ├── lint
 └── execução
```

Cada ferramenta resolve um problema diferente.

------------------------------------------------------------------------

# 17. Makefile e CI

Mais tarde, o GitHub Actions poderá executar:

``` yaml
- name: Install dependencies
  run: make install

- name: Run tests
  run: make test

- name: Lint
  run: make lint
```

Isso é interessante porque o mesmo comando usado pelo desenvolvedor
local pode ser utilizado na integração contínua.

``` text
Desenvolvedor
     │
     └── make test
            │
            ↓
       mesmo comando
            ↑
            │
GitHub Actions
     │
     └── make test
```

Essa padronização reduz diferenças entre:

``` text
"funciona na minha máquina"
```

e:

``` text
"funciona no CI"
```

------------------------------------------------------------------------

# 18. Makefile e Docker

Nas próximas práticas, podemos adicionar:

``` makefile
docker-up:
    docker compose up -d

docker-down:
    docker compose down
```

Depois:

``` bash
make docker-up
```

O fluxo começa a ficar:

``` text
make
 ├── Poetry
 ├── Pytest
 ├── Ruff
 ├── Uvicorn
 └── Docker Compose
```

O Makefile não substitui essas ferramentas.

Ele organiza a forma como a equipe as utiliza.

------------------------------------------------------------------------

# 19. Exercício guiado

Crie:

``` makefile
.PHONY: install test run

install:
    poetry install

test:
    poetry run pytest

run:
    poetry run uvicorn app.main:app --reload
```

Teste:

``` bash
make install
make test
make run
```

------------------------------------------------------------------------

# 20. Desafio

Expanda o Makefile para possuir:

``` text
make help
make install
make test
make lint
make format
make run
```

Depois faça um commit:

``` bash
git add Makefile
git commit -m "build: adiciona comandos de desenvolvimento"
```

Finalmente, abra um Pull Request.

------------------------------------------------------------------------

# 21. Checklist

-   [ ] Sei o que é um Makefile.
-   [ ] Sei criar um target.
-   [ ] Sei executar `make <target>`.
-   [ ] Sei utilizar `.PHONY`.
-   [ ] Sei criar variáveis.
-   [ ] Sei criar comandos para testes e execução.
-   [ ] Sei integrar Makefile com Poetry.
-   [ ] Entendo como Makefile pode ser usado no CI.
-   [ ] Entendo como Makefile pode facilitar o uso de Docker.

## Conexão com o restante do laboratório

A partir destas três ferramentas:

``` text
Git/GitHub
    ↓
Poetry
    ↓
Makefile
```

o laboratório pode evoluir para:

``` text
Backend FastAPI
       ↓
PostgreSQL
       ↓
ORM / Migrations
       ↓
Testes unitários
       ↓
Testes de integração
       ↓
GitHub Actions
       ↓
Docker / Docker Compose
       ↓
Frontend JavaScript
       ↓
Fetch API
       ↓
Testes E2E
       ↓
Integração Full-Stack
```

Esse encadeamento permite que as práticas seguintes apresentem
desenvolvimento web de forma progressiva, partindo da organização do
projeto até a construção e integração de uma aplicação distribuída.
