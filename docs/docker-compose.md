# Prática 2 — Containerização Robusta com Docker & Docker Compose

> **Disciplina:** C216 — Sistemas Distribuídos
> **Módulo 1:** Fundamentos & DevOps
> **Prática 2:** Containers com Docker & Docker Compose para Ambientes Distribuídos
> **Foco:** isolamento de serviços, reprodutibilidade e orquestração local

---

## 1. Objetivos da prática

Ao final desta prática, o aluno deverá ser capaz de:

* explicar por que containers são úteis no desenvolvimento web;
* diferenciar **imagem**, **container**, **volume**, **rede** e **registro de imagens**;
* criar imagens próprias utilizando `Dockerfile`;
* entender o contexto de build e a importância do `.dockerignore`;
* executar e inspecionar containers;
* publicar portas e trabalhar com variáveis de ambiente;
* persistir dados utilizando volumes;
* criar uma aplicação com múltiplos serviços utilizando `Docker Compose`;
* compreender a comunicação entre containers por nome de serviço;
* estruturar um ambiente local próximo de um cenário distribuído;
* automatizar operações frequentes com `Makefile`;
* aplicar boas práticas para imagens menores, seguras e reproduzíveis;
* compreender como containerizar um projeto organizado em **backend**, **frontend** e arquivos de infraestrutura na raiz.

---

# 2. Onde esta prática se encaixa no laboratório

O laboratório será construído de forma **contínua**. A ideia é que as práticas seguintes não sejam projetos isolados, mas evoluções do mesmo ecossistema.

A estrutura atual do projeto possui:

```text
lab/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── poetry.lock
│   └── pyproject.toml
├── docs/
├── frontend/
├── .gitignore
├── LICENSE
├── Makefile
└── README.md
```

A partir desta prática, serão adicionados arquivos relacionados à containerização:

```text
lab/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend/
│   ├── ...
│   └── Dockerfile          # futuramente
├── docs/
├── .dockerignore
├── .env.example
├── .gitignore
├── LICENSE
├── compose.yaml
├── Makefile
└── README.md
```

A evolução do laboratório será aproximadamente:

```text
Prática 1
Git/GitHub + Poetry + Makefile
        |
        v
Prática 2
Docker + Docker Compose
        |
        v
Prática 3
FastAPI + APIs + Modelos
        |
        v
Prática 4
PostgreSQL + SQLAlchemy + Migrations
        |
        v
Prática 5
Pytest + Integração + CI
        |
        v
Prática 6
Frontend JavaScript
        |
        v
Prática 7
Integração Full-stack + CORS + E2E + Multicontêiner
```

A proposta é que o aluno perceba que **DevOps, backend, banco de dados, frontend e testes fazem parte de um mesmo ciclo de desenvolvimento**.

---

# 3. O problema: "na minha máquina funciona"

Imagine uma aplicação Python:

```text
Desenvolvedor A
Python 3.12
PostgreSQL 16
Poetry 2.x
Windows

Desenvolvedor B
Python 3.11
PostgreSQL 15
Poetry 1.x
Linux

CI
Python 3.12
PostgreSQL 16
Ubuntu
```

Mesmo código não significa necessariamente mesmo ambiente.

Podem existir diferenças em:

* versão do Python;
* sistema operacional;
* bibliotecas instaladas;
* banco de dados;
* variáveis de ambiente;
* ferramentas do sistema;
* permissões;
* configuração de rede;
* arquivos locais.

A consequência é o clássico:

> **"Funciona na minha máquina."**

Containers atacam justamente esse problema.

---

# 4. O que é um container?

Um container é um ambiente isolado para executar um processo e suas dependências.

Uma forma simples de visualizar:

```text
                 Aplicação Web
                      |
              +-------+-------+
              |               |
          Python 3.12     Dependências
              |               |
              +-------+-------+
                      |
                  Container
                      |
                  Docker
                      |
                  Sistema OS
```

O container compartilha o kernel do sistema operacional hospedeiro, mas mantém processos, filesystem, rede e outras características isoladas.

### Container não é uma máquina virtual

Comparação conceitual:

```text
MÁQUINA VIRTUAL

Hardware
   |
Hypervisor
   |
+---------------------+
| VM                  |
| Sistema Operacional |
| Aplicação           |
+---------------------+


CONTAINER

Hardware
   |
Sistema Operacional
   |
Docker / Container Runtime
   |
+-------------+-------------+
| Container A | Container B |
| Aplicação   | Aplicação   |
+-------------+-------------+
```

Em geral, containers são mais leves e rápidos para iniciar do que máquinas virtuais porque não precisam carregar um sistema operacional completo para cada aplicação.

---

# 5. A arquitetura básica do Docker

Podemos pensar no Docker em algumas peças principais:

```text
Dockerfile
    |
    | build
    v
+-----------+
|  Imagem   |
+-----------+
    |
    | run
    v
+-----------+
| Container |
+-----------+
    |
    +---- rede
    |
    +---- volume
    |
    +---- portas
```

## 5.1 Imagem

A **imagem** é um artefato imutável utilizado como base para criar containers.

Exemplo:

```text
python:3.12-slim
```

Uma imagem pode conter:

* sistema de arquivos;
* runtime;
* bibliotecas;
* arquivos da aplicação;
* configurações necessárias para execução.

## 5.2 Container

O **container** é uma instância em execução de uma imagem.

Uma mesma imagem pode originar vários containers:

```text
             imagem python:3.12
                    |
          +---------+---------+
          |         |         |
          v         v         v
       app-01    app-02    app-03
```

## 5.3 Registry

Um registry armazena e distribui imagens.

Exemplo conceitual:

```text
Dockerfile
    |
    | docker build
    v
Imagem
    |
    | docker push
    v
Registry
    |
    | docker pull
    v
Outro computador
```

---

# 6. Primeiro contato com Docker

Verificar a instalação:

```bash
docker --version
```

Executar um container simples:

```bash
docker run hello-world
```

Listar containers em execução:

```bash
docker ps
```

Listar todos os containers:

```bash
docker ps -a
```

Listar imagens:

```bash
docker images
```

---

# 7. Primeiro container web

Vamos executar um servidor HTTP utilizando uma imagem pronta.

```bash
docker run -d --name web nginx
```

Agora:

```bash
docker ps
```

Temos:

```text
HOST
 |
 | Docker
 |
 +---- container: web
       |
       +---- nginx
```

Mas existe um problema.

O servidor está dentro do container. Para acessá-lo a partir do navegador do host, precisamos publicar uma porta.

```bash
docker run -d \
  --name web \
  -p 8080:80 \
  nginx
```

Agora:

```text
http://localhost:8080
        |
        v
HOST :8080
        |
        v
CONTAINER :80
        |
        v
Nginx
```

### Regra importante

```text
-p PORTA_HOST:PORTA_CONTAINER
```

Exemplo:

```bash
-p 8080:80
```

Significa:

> A porta `8080` do host será encaminhada para a porta `80` do container.

---

# 8. Comandos essenciais

## Criar e executar

```bash
docker run nginx
```

## Executar em background

```bash
docker run -d nginx
```

## Definir nome

```bash
docker run -d --name web nginx
```

## Publicar porta

```bash
docker run -d \
  --name web \
  -p 8080:80 \
  nginx
```

## Parar

```bash
docker stop web
```

## Iniciar novamente

```bash
docker start web
```

## Remover

```bash
docker rm web
```

## Remover forçadamente

```bash
docker rm -f web
```

## Ver logs

```bash
docker logs web
```

## Acompanhar logs

```bash
docker logs -f web
```

## Inspecionar

```bash
docker inspect web
```

## Executar comando dentro do container

```bash
docker exec -it web sh
```

Esse comando é muito útil para investigação.

---

# 9. Estrutura do nosso projeto

Diferentemente de um projeto Python simples, o laboratório possui uma separação explícita entre backend, frontend e documentação.

A estrutura atual do projeto é:

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── poetry.lock
│   └── pyproject.toml
├── docs/
│   ├── README.md
│   ├── git-github.md
│   ├── makefile.md
│   └── poetry.md
├── frontend/
├── .gitignore
├── LICENSE
├── Makefile
└── README.md
```

Nesta prática, adicionaremos os arquivos relacionados à containerização.

Como cada parte da aplicação poderá futuramente possuir seu próprio container, o `Dockerfile` do backend ficará **dentro do diretório `backend/`**:

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── docs/
├── frontend/
├── .env.example
├── .gitignore
├── compose.yaml
├── LICENSE
├── Makefile
└── README.md
```

Essa organização permite que cada serviço tenha sua própria receita de construção.

No futuro, quando o frontend também for containerizado, poderemos ter:

```text
frontend/
├── ...
├── .dockerignore
└── Dockerfile
```

Assim:

```text
backend/Dockerfile
        |
        v
Imagem do backend


frontend/Dockerfile
        |
        v
Imagem do frontend
```

Enquanto o `compose.yaml`, localizado na raiz, será responsável por orquestrar os diferentes serviços:

```text
                    compose.yaml
                         |
             +-----------+-----------+
             |                       |
             v                       v
       backend/Dockerfile      frontend/Dockerfile
             |                       |
             v                       v
       Backend image            Frontend image
```

Essa separação será importante nas práticas posteriores.

---

# 10. Imagem própria com Dockerfile

Agora vamos deixar de usar somente imagens prontas.

Nosso backend possui uma estrutura baseada em Poetry:

```text
backend/
├── app/
│   └── main.py
├── tests/
├── poetry.lock
└── pyproject.toml
```

O `Dockerfile` ficará dentro de `backend/`:

```text
backend/
├── app/
│   └── main.py
├── tests/
├── Dockerfile
├── poetry.lock
└── pyproject.toml
```

Um Dockerfile inicial:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY app ./app

CMD ["python", "app/main.py"]
```

Observe que os caminhos utilizados no `COPY` são relativos ao diretório `backend/`, que será utilizado como contexto de build.

Isso torna o Dockerfile independente da estrutura externa do repositório.

---

# 11. Anatomia do Dockerfile

## FROM

Define a imagem base.

```dockerfile
FROM python:3.12-slim
```

## WORKDIR

Define o diretório de trabalho dentro da imagem.

```dockerfile
WORKDIR /app
```

## COPY

Copia arquivos do contexto de build para a imagem.

Como o contexto será o diretório `backend/`, podemos utilizar:

```dockerfile
COPY pyproject.toml poetry.lock ./
```

e:

```dockerfile
COPY app ./app
```

Não precisamos escrever:

```dockerfile
COPY backend/app ./app
```

porque `backend/` já é o contexto disponibilizado ao Docker.

## RUN

Executa comandos durante o build.

```dockerfile
RUN pip install --no-cache-dir poetry
```

## CMD

Define o comando padrão de execução do container.

```dockerfile
CMD ["python", "app/main.py"]
```

---

# 12. Build da imagem

Como o `Dockerfile` está dentro de `backend/`, temos duas formas de executar o build.

A forma mais simples é entrar no diretório:

```bash
cd backend
```

e executar:

```bash
docker build -t laboratorio-backend:1.0 .
```

O `.` representa o diretório atual:

```text
backend/
   |
   +---- Dockerfile
   +---- pyproject.toml
   +---- poetry.lock
   +---- app/
   +---- tests/
```

Também podemos executar o build diretamente a partir da raiz:

```bash
docker build -t laboratorio-backend:1.0 ./backend
```

Nesse caso:

```text
docker build
      |
      +---- contexto: ./backend
```

As duas formas produzem o mesmo contexto de build.

Depois:

```bash
docker images
```

Podemos executar:

```bash
docker run --rm laboratorio-backend:1.0
```

No projeto do laboratório, posteriormente utilizaremos o `docker compose` e o `Makefile` para evitar que os alunos precisem executar manualmente todos esses comandos.

---

# 13. O contexto de build

Este é um dos conceitos mais importantes desta prática.

Quando executamos:

```bash
docker build -t laboratorio-backend:1.0 ./backend
```

estamos dizendo ao Docker:

> Utilize `backend/` como contexto de build.

Podemos visualizar:

```text
laboratorio-web/
│
├── backend/             <-- contexto
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── poetry.lock
│   ├── app/
│   └── tests/
│
├── frontend/
├── docs/
├── Makefile
└── README.md
```

Dentro do Dockerfile:

```dockerfile
COPY pyproject.toml poetry.lock ./
```

significa:

```text
backend/pyproject.toml
backend/poetry.lock
        |
        v
      imagem
```

Da mesma forma:

```dockerfile
COPY app ./app
```

significa:

```text
backend/app/
     |
     v
imagem:/app/app/
```

### Por que não utilizar a raiz como contexto?

Poderíamos executar:

```bash
docker build -t laboratorio-backend:1.0 .
```

a partir da raiz.

Porém, nesse caso, o Docker receberia potencialmente todo o projeto como contexto:

```text
backend/
frontend/
docs/
.git/
README.md
Makefile
...
```

Isso não é necessário para construir o backend.

Como o backend possui tudo que precisa dentro de `backend/`, é mais adequado utilizar:

```text
./backend
```

como contexto.

Isso reduz o contexto e mantém cada serviço isolado.

### Regra importante

> **O contexto de build deve conter tudo que o Docker precisa para construir a imagem, mas não deve conter arquivos desnecessários.**

---

# 14. `.dockerignore`

Como o contexto de build do backend é:

```text
backend/
```

o `.dockerignore` deve ficar dentro de `backend/`:

```text
backend/
├── .dockerignore
├── Dockerfile
├── app/
├── tests/
├── poetry.lock
└── pyproject.toml
```

Exemplo:

```dockerignore
.git
.gitignore

__pycache__
*.pyc
.pytest_cache
.venv

.env
.env.*

coverage
dist
build

tests
```

Isso ajuda a:

- reduzir o contexto;
- acelerar builds;
- evitar arquivos desnecessários;
- impedir que segredos sejam copiados acidentalmente;
- reduzir o tamanho potencial da imagem.

Observe que não precisamos colocar:

```text
frontend
docs
Makefile
README.md
```

no `.dockerignore` do backend.

Esses arquivos nem sequer fazem parte do contexto.

O contexto é:

```text
backend/
```

e não:

```text
.
```

### E no futuro?

Quando o frontend possuir seu próprio container, ele poderá ter seu próprio `.dockerignore`:

```text
frontend/
├── .dockerignore
├── Dockerfile
└── ...
```

Assim, cada serviço controla seu próprio contexto de build.

### Atenção

`.dockerignore` **não substitui** uma política de segurança.

Segredos não devem estar no código nem em arquivos que possam ser enviados para o build.

---

# 15. Camadas de uma imagem

Um Dockerfile pode gerar várias camadas.

No nosso backend:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY app ./app

CMD ["python", "app/main.py"]
```

Conceitualmente:

```text
+-----------------------------+
| CMD                         |
+-----------------------------+
| Código: app/                |
+-----------------------------+
| Dependências do Poetry      |
+-----------------------------+
| pyproject.toml / lock       |
+-----------------------------+
| Python 3.12-slim            |
+-----------------------------+
```

O Docker consegue reutilizar camadas que não mudaram.

Por isso a ordem das instruções importa.

---

# 16. Um erro comum de cache

Considere:

```dockerfile
COPY . .

RUN pip install ...
```

Nesse caso, uma alteração qualquer dentro do contexto pode invalidar a camada anterior.

Uma abordagem melhor:

```dockerfile
COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY app ./app
```

Assim:

```text
pyproject.toml / poetry.lock não mudaram
        |
        v
camada de dependências pode ser reutilizada
        |
        v
apenas código é atualizado
```

Essa organização é especialmente importante no nosso projeto porque o `pyproject.toml` e o `poetry.lock` já estão separados do código:

```text
backend/
├── app/
├── pyproject.toml
└── poetry.lock
```

---

# 17. Multi-stage build

Em aplicações reais, podemos separar construção e execução.

Como o projeto utiliza Poetry, podemos futuramente separar a etapa de instalação das dependências da imagem final.

Exemplo conceitual:

```dockerfile
FROM python:3.12 AS builder

WORKDIR /build

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY app ./app

CMD ["python", "app/main.py"]
```

A ideia:

```text
            BUILDER
               |
        instala dependências
               |
               v
      artefatos necessários
               |
               v
          RUNTIME
               |
               v
        imagem final menor
```

O objetivo não é simplesmente "usar multi-stage porque é moderno".

O objetivo é:

> **levar para a imagem final somente o que é necessário para executar a aplicação.**

---

# 18. Variáveis de ambiente

Aplicações web frequentemente precisam de configurações:

```text
DATABASE_URL
SECRET_KEY
API_URL
ENVIRONMENT
PORT
```

Não devemos fixar tudo diretamente no código.

Ruim:

```python
DATABASE_URL = "postgresql://admin:senha@localhost:5432/app"
```

Melhor:

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
```

No container:

```bash
docker run \
  -e DATABASE_URL="postgresql://admin:senha@db:5432/app" \
  laboratorio-backend:1.0
```

---

# 19. O problema do `localhost`

Este é um dos conceitos mais importantes da prática.

Imagine:

```text
HOST
 |
 +---- API
 |
 +---- PostgreSQL
```

Quando a API roda em um container e o PostgreSQL em outro:

```text
+----------------+       +----------------+
| API container  | ----> | DB container   |
|                |       |                |
| localhost      |       | PostgreSQL     |
+----------------+       +----------------+
```

Dentro do container da API:

```text
localhost
```

significa:

> **o próprio container da API.**

Não significa o container do PostgreSQL.

Por isso:

```text
DATABASE_HOST=localhost
```

normalmente estará errado nesse cenário.

---

# 20. Redes Docker

Podemos criar uma rede:

```bash
docker network create laboratorio-network
```

Executar o banco:

```bash
docker run -d \
  --name db \
  --network laboratorio-network \
  postgres:16
```

Executar a API na mesma rede:

```bash
docker run -d \
  --name api \
  --network laboratorio-network \
  laboratorio-backend:1.0
```

Agora a API pode acessar:

```text
db
```

como hostname.

```text
+----------------------------+
| Docker network             |
|                            |
|  +---------+               |
|  | API     |               |
|  +----+----+               |
|       |                    |
|       | db:5432            |
|       v                    |
|  +---------+               |
|  | Postgres|               |
|  +---------+               |
+----------------------------+
```

---

# 21. Por que Docker Compose?

Executar manualmente:

```bash
docker build -t laboratorio-backend ./backend

docker network create laboratorio-network

docker run ...
docker run ...
docker run ...
```

funciona, mas rapidamente fica difícil de manter.

Imagine:

```text
frontend
backend
postgres
redis
worker
nginx
```

Precisaríamos controlar:

- nomes;
- redes;
- portas;
- volumes;
- variáveis;
- dependências;
- comandos;
- configurações;
- contextos de build;
- Dockerfiles.

O Docker Compose permite declarar tudo isso em um arquivo.

No nosso projeto, o `compose.yaml` ficará na raiz:

```text
laboratorio-web/
├── backend/
│   └── Dockerfile
├── frontend/
├── compose.yaml
└── ...
```

O Compose será responsável por conectar os diferentes componentes do laboratório.

---

# 22. Primeiro `compose.yaml`

Como o `Dockerfile` está dentro de `backend/`, o serviço deve informar que seu contexto de build é `./backend`:

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
```

Observe:

```yaml
context: ./backend
```

Isso significa:

```text
compose.yaml
      |
      v
./backend
      |
      +---- Dockerfile
      +---- pyproject.toml
      +---- poetry.lock
      +---- app/
```

Executar:

```bash
docker compose up
```

Em background:

```bash
docker compose up -d
```

Parar:

```bash
docker compose down
```

---

# 23. Compose como declaração de arquitetura

O arquivo:

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile

  db:
    image: postgres:16
```

pode ser entendido como:

```text
                    compose.yaml
                         |
             +-----------+-----------+
             |                       |
             v                       v
        service api             service db
             |                       |
             |                       |
     ./backend/Dockerfile       postgres:16
             |                       |
             v                       v
       API container            DB container
             |                       |
             +-------- rede ---------+
```

O Compose cria uma rede para os serviços do projeto.

Por isso:

```text
api -> db:5432
```

funciona.

---

# 24. Compose completo para Backend + PostgreSQL

Um exemplo mais realista:

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+psycopg://app:app@db:5432/app
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Temos aqui:

- build da imagem do backend;
- contexto de build específico;
- publicação de porta;
- variável de ambiente;
- comunicação entre serviços;
- dependência;
- volume persistente.

Observe novamente:

```yaml
build:
  context: ./backend
  dockerfile: Dockerfile
```

O Docker não precisa receber o projeto inteiro.

Ele recebe somente:

```text
backend/
```

como contexto.

---

# 25. `depends_on` não significa "banco pronto"

Este ponto é importante para evitar uma falsa impressão.

```yaml
depends_on:
  - db
```

significa essencialmente que o serviço `db` deve ser iniciado antes da criação/inicialização do serviço dependente.

Isso **não garante** que o PostgreSQL já esteja pronto para aceitar conexões.

Podemos visualizar:

```text
Compose
   |
   +---- inicia db
   |
   +---- inicia api
             |
             +---- tenta conectar
                      |
                      X
                DB ainda inicializando
```

Em aplicações robustas, devemos tratar a disponibilidade do serviço com mecanismos apropriados, como:

* healthcheck;
* retry/backoff na aplicação;
* scripts de inicialização quando fizer sentido.

---

# 26. Healthcheck

Exemplo:

```yaml
services:

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 5s
      retries: 5
```

E a API:

```yaml
  api:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
```

Fluxo:

```text
db inicia
   |
   v
healthcheck
   |
   +---- não pronto --> tenta novamente
   |
   +---- pronto -----> API pode iniciar
```

---

# 27. Volumes

Containers são, por padrão, efêmeros.

Se o container do PostgreSQL for removido, seus dados não devem depender apenas da camada gravável daquele container.

Precisamos de persistência.

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Conceitualmente:

```text
+----------------+
| PostgreSQL     |
| container      |
+-------+--------+
        |
        | mount
        v
+----------------+
| postgres_data  |
| volume         |
+----------------+
```

Remover o container:

```bash
docker compose down
```

não significa necessariamente remover o volume.

Para remover volumes também:

```bash
docker compose down -v
```

### Cuidado

`down -v` pode apagar os dados persistidos do ambiente.

---

# 28. Bind mount x volume

Existem duas ideias diferentes.

### Bind mount

Liga um diretório do host ao container:

```yaml
volumes:
  - ./backend/app:/app/app
```

Muito útil para desenvolvimento.

### Named volume

Gerenciado pelo Docker:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Muito comum para dados persistentes de serviços.

Resumo:

```text
Bind mount

Host <----------> Container


Named volume

Docker Volume <---> Container
```

---

# 29. Desenvolvimento x produção

Uma das decisões mais importantes:

> O ambiente de desenvolvimento não precisa ser igual ao ambiente de produção.

No nosso projeto, podemos utilizar diferentes estratégias.

### Desenvolvimento

Podemos querer:

- hot reload;
- código montado como volume;
- ferramentas de debug;
- logs detalhados;
- dependências de desenvolvimento.

Por exemplo:

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - ./backend/app:/app/app
    command:
      [
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload"
      ]
```

### Produção

Queremos:

- imagem enxuta;
- poucos processos;
- configuração externa;
- usuário não-root;
- builds reproduzíveis;
- sem ferramentas desnecessárias;
- logs apropriados.

Uma possibilidade futura é utilizar diferentes arquivos Compose ou diferentes configurações de build.

---

# 30. Exemplo de Dockerfile para FastAPI

Antecipando a Prática 3, nosso backend será baseado em FastAPI.

O projeto possui:

```text
backend/
├── app/
│   └── main.py
├── poetry.lock
└── pyproject.toml
```

O `Dockerfile` ficará em:

```text
backend/Dockerfile
```

Portanto:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY app ./app

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

Pontos importantes:

```text
0.0.0.0
```

é utilizado para que o servidor aceite conexões vindas da interface de rede do container.

Usar apenas:

```text
127.0.0.1
```

pode fazer o serviço ficar acessível somente dentro do próprio container.

---

# 31. Exemplo de Compose para FastAPI

O `compose.yaml` permanece na raiz:

```text
laboratorio-web/
├── backend/
│   ├── Dockerfile
│   └── ...
├── compose.yaml
└── ...
```

Um ambiente de desenvolvimento:

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      ENVIRONMENT: development
    volumes:
      - ./backend/app:/app/app
    command:
      [
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload"
      ]
```

Com isso:

```text
Navegador
    |
localhost:8000
    |
    v
Docker Compose
    |
    v
API container
    |
    v
/app/app
    ^
    |
./backend/app
```

O bind mount:

```yaml
- ./backend/app:/app/app
```

faz com que alterações realizadas no código do host sejam refletidas no container.

---

# 32. Um ambiente multicontêiner

A partir daqui podemos imaginar nosso laboratório evoluindo para:

```text
                         Internet
                            |
                            v
                       +---------+
                       | Frontend|
                       +----+----+
                            |
                            v
                       +---------+
                       |   API   |
                       +----+----+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
           +-----------+         +-----------+
           | PostgreSQL|         |   Redis   |
           +-----------+         +-----------+
```

O repositório já possui um diretório:

```text
frontend/
```

que será utilizado nas práticas posteriores.

Nesta prática, o foco principal é o **backend containerizado + PostgreSQL**.

Cada componente possui uma responsabilidade.

Isso é uma introdução prática à ideia de **sistemas distribuídos**.

---

# 33. Containerizar não significa "microserviços"

É importante diferenciar os conceitos.

Podemos ter:

```text
1 aplicação
1 container
```

ou:

```text
1 aplicação
+
1 banco
+
1 cache
```

ou ainda:

```text
serviço A
serviço B
serviço C
serviço D
```

Containers são uma tecnologia de empacotamento e isolamento.

**Microserviços são uma decisão arquitetural.**

Não devemos transformar tudo em microserviços apenas porque estamos utilizando Docker.

---

# 34. Logs

Uma aplicação containerizada deve produzir logs de forma adequada.

Exemplo:

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("Servidor iniciado")
```

No Docker:

```bash
docker logs api
```

No Compose:

```bash
docker compose logs
```

Somente API:

```bash
docker compose logs api
```

Acompanhar em tempo real:

```bash
docker compose logs -f api
```

---

# 35. O processo principal do container

Uma regra importante:

> Um container deve ter um processo principal claramente definido.

Por exemplo:

```dockerfile
CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

O processo principal é o servidor da aplicação.

Se ele termina:

```text
Processo principal
      |
      X
      |
Container termina
```

Isso é diferente de pensar em um container como uma pequena máquina virtual que precisa ficar rodando vários serviços internamente.

---

# 36. Usuário não-root

Por padrão, devemos evitar executar aplicações como `root` quando não é necessário.

Exemplo:

```dockerfile
FROM python:3.12-slim

RUN useradd --create-home appuser

WORKDIR /app

COPY --chown=appuser:appuser backend/app ./app

USER appuser

CMD [
    "python",
    "app/main.py"
]
```

Conceito:

```text
root
 |
 +-- possui privilégios elevados

appuser
 |
 +-- privilégios mínimos necessários
```

Isso faz parte do princípio de **least privilege**.

---

# 37. Imagens pequenas

Compare:

```dockerfile
FROM python:3.12
```

com:

```dockerfile
FROM python:3.12-slim
```

A segunda normalmente possui menos componentes desnecessários.

Mas "imagem menor" não deve ser uma obsessão.

Precisamos equilibrar:

```text
Tamanho
   +
Segurança
   +
Compatibilidade
   +
Tempo de build
   +
Facilidade de manutenção
```

Uma imagem extremamente pequena, mas difícil de manter, pode ser uma escolha pior.

---

# 38. Reprodutibilidade

Uma das grandes vantagens de containers é poder declarar o ambiente.

Em vez de:

```text
Instale Python
Instale Poetry
Instale dependência X
Instale dependência Y
Configure variável Z
```

temos:

```text
Dockerfile
compose.yaml
backend/pyproject.toml
backend/poetry.lock
```

E o ambiente pode ser reconstruído.

```bash
docker compose build
docker compose up
```

A ideia é aproximar o ambiente de:

```text
Código + Dependências + Configuração + Infraestrutura
                         |
                         v
                Ambiente reproduzível
```

---

# 39. Tags e versões

Evite depender indiscriminadamente de:

```dockerfile
FROM python:latest
```

Prefira versões explícitas:

```dockerfile
FROM python:3.12-slim
```

E, dependendo do nível de controle necessário, versões ainda mais específicas podem ser utilizadas.

A vantagem é reduzir mudanças inesperadas.

Imagine:

```text
Hoje:
latest -> Python X

Amanhã:
latest -> Python Y
```

O mesmo Dockerfile pode produzir um ambiente diferente.

---

# 40. `docker compose up` x `docker compose down`

Fluxo típico:

```bash
docker compose up -d
```

Ver status:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Parar/remover containers e rede do projeto:

```bash
docker compose down
```

Rebuild:

```bash
docker compose build
```

Rebuild + execução:

```bash
docker compose up --build
```

---

# 41. Makefile como interface do projeto

Como já trabalhamos com Makefile na Prática 1, podemos evoluir o conceito.

O `Makefile` continua localizado na raiz:

```text
laboratorio-web/
├── backend/
├── frontend/
├── compose.yaml
├── Makefile
└── ...
```

Em vez de pedir:

```bash
docker compose up --build
```

podemos criar:

```makefile
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

ps:
	docker compose ps
```

Então:

```bash
make up
make logs
make down
```

A equipe passa a ter uma interface comum para operações frequentes.

Uma evolução possível:

```makefile
up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

ps:
	docker compose ps

shell:
	docker compose exec api sh
```

Observe que o `Makefile` não precisa conhecer os detalhes internos do Dockerfile.

Ele apenas fornece uma interface para operar o ambiente:

```text
make
 |
 +-- docker compose
       |
       +-- backend
       +-- PostgreSQL
       +-- futuramente frontend
```

---

# 42. Uma estrutura de projeto sugerida

Ao finalizar esta prática, a estrutura esperada será aproximadamente:

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── docs/
│   ├── README.md
│   ├── git-github.md
│   ├── makefile.md
│   └── poetry.md
├── frontend/
├── .env.example
├── .gitignore
├── compose.yaml
├── LICENSE
├── Makefile
└── README.md
```

A ideia é que cada diretório relacionado a uma aplicação possa futuramente possuir seus próprios arquivos de containerização.

### Backend

```text
backend/
├── Dockerfile
└── .dockerignore
```

### Frontend — futuramente

```text
frontend/
├── Dockerfile
└── .dockerignore
```

### Infraestrutura do ambiente

```text
compose.yaml
Makefile
.env.example
```

Essa separação permite diferenciar:

```text
Dockerfile
    |
    +-- Como construir um serviço


compose.yaml
    |
    +-- Como executar vários serviços juntos


Makefile
    |
    +-- Como facilitar operações frequentes
```

---

# 43. `.env` e `.env.example`

Configurações locais podem ser carregadas por ambiente.

Como o projeto utiliza um diretório `backend/`, as configurações de infraestrutura continuam sendo centralizadas na raiz.

Exemplo de `.env.example`:

```env
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg://app:change-me@db:5432/app
```

O arquivo real:

```text
.env
```

normalmente não deve ser versionado quando contém credenciais reais.

No `.gitignore`:

```gitignore
.env
```

Mas mantemos:

```text
.env.example
```

para documentar quais configurações são necessárias.

---

# 44. Compose usando `.env`

Podemos escrever:

```yaml
services:

  api:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: ${DATABASE_URL}

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

E:

```env
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
```

O Compose substitui as variáveis durante a configuração.

---

# 45. O que não devemos colocar na imagem

Evite:

```dockerfile
ENV DATABASE_PASSWORD=senha-super-secreta
```

Também não devemos:

```dockerfile
COPY .env .
```

A imagem pode ser armazenada, distribuída e analisada por outras pessoas ou sistemas.

A regra geral:

> **Configuração e segredos devem ser fornecidos em runtime, não incorporados desnecessariamente na imagem.**

---

# 46. Segurança: visão geral

Containerização não torna uma aplicação automaticamente segura.

Precisamos considerar:

* imagens confiáveis;
* dependências atualizadas;
* menor privilégio;
* ausência de segredos na imagem;
* `.dockerignore`;
* usuário não-root;
* portas realmente necessárias;
* atualização de imagens;
* validação das entradas da aplicação;
* permissões de volumes.

Docker resolve isolamento e empacotamento.

Segurança continua sendo responsabilidade do sistema como um todo.

---

# 47. Debugging: roteiro mental

Quando um serviço não funciona, não comece alterando tudo.

Siga uma sequência.

### 1. O container está rodando?

```bash
docker compose ps
```

### 2. Existem erros?

```bash
docker compose logs api
```

### 3. A porta está publicada?

```yaml
ports:
  - "8000:8000"
```

### 4. O serviço está ouvindo em `0.0.0.0`?

```text
0.0.0.0:8000
```

### 5. A aplicação consegue resolver o hostname?

```text
db
```

### 6. A aplicação está tentando usar `localhost`?

Se sim, provavelmente há um problema de rede entre serviços.

### 7. O banco está pronto?

Healthcheck e logs podem ajudar.

---

# 48. Erro clássico: `localhost`

Considere:

```yaml
services:

  api:
    ...

  db:
    ...
```

Errado:

```env
DATABASE_HOST=localhost
```

Correto:

```env
DATABASE_HOST=db
```

Porque:

```text
api container
    |
    | localhost
    v
api container
```

Enquanto:

```text
api container
    |
    | db
    v
db container
```

Essa distinção será fundamental na Prática 4, quando adicionarmos PostgreSQL e ORM.

---

# 49. Exemplo completo: API + PostgreSQL

Estrutura:

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend/
├── compose.yaml
├── .env.example
└── Makefile
```

### `backend/app/main.py`

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Laboratório distribuído funcionando!"}
```

### `backend/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY app ./app

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

### `compose.yaml`

```yaml
services:

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Executar:

```bash
docker compose up --build
```

Acessar:

```text
http://localhost:8000
```

---

# 50. Exemplo completo: Backend + PostgreSQL

Estrutura:

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── Makefile
```

### `backend/app/main.py`

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Laboratório distribuído funcionando!"}
```

### `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/pyproject.toml backend/poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY backend/app ./app

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

### `compose.yaml`

```yaml
services:

  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Executar:

```bash
docker compose up --build
```

Acessar:

```text
http://localhost:8000
```

---

# 51. Evolução desse exemplo

Na próxima prática, o backend será aprofundado.

Hoje:

```text
FastAPI
   |
   X
PostgreSQL
```

O banco já está presente na infraestrutura, mas a API ainda não precisa utilizá-lo.

Depois:

```text
FastAPI
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
```

Depois:

```text
FastAPI
   |
   +---- SQLAlchemy
   |
   +---- Pydantic
   |
   +---- PostgreSQL
   |
   +---- Alembic
```

E mais adiante:

```text
Frontend
    |
    v
FastAPI
    |
    v
PostgreSQL
```

A prática de Docker prepara a infraestrutura para essa evolução.

---

# 52. Atividade prática sugerida

A atividade deve evoluir o repositório contínuo iniciado na Prática 1.

## Objetivo

Containerizar o backend e criar um ambiente local com:

```text
Backend
   +
PostgreSQL
```

Mesmo que a API ainda não utilize o banco nesta prática, a infraestrutura deve estar preparada para a Prática 4.

O projeto já possui um diretório reservado para o frontend:

```text
frontend/
```

Porém, a containerização do frontend será trabalhada posteriormente.

### Requisitos mínimos

- [ ] Criar `backend/Dockerfile`;
- [ ] Criar `backend/.dockerignore`;
- [ ] Criar `compose.yaml` na raiz;
- [ ] Utilizar `./backend` como contexto de build;
- [ ] Executar o backend dentro de um container;
- [ ] Publicar a porta da aplicação;
- [ ] Adicionar PostgreSQL ao Compose;
- [ ] Criar volume persistente para o PostgreSQL;
- [ ] Configurar variáveis de ambiente;
- [ ] Utilizar comunicação entre serviços pelo nome do serviço;
- [ ] Criar comandos relacionados ao Docker no `Makefile` da raiz;
- [ ] Documentar como executar o ambiente;
- [ ] Garantir que o projeto possa ser reconstruído em outra máquina;
- [ ] Manter a estrutura existente de `backend/`, `frontend/` e `docs/`.

---

# 53. Critérios de qualidade

Não avaliar apenas:

> "O Docker sobe."

Observar também:

### Organização

```text
backend/
├── Dockerfile
└── .dockerignore

compose.yaml
.env.example
Makefile
```

### Contexto de build

O backend utiliza:

```yaml
build:
  context: ./backend
```

em vez de enviar desnecessariamente todo o projeto como contexto.

### Reprodutibilidade

Um colega consegue executar:

```bash
make up
```

e obter o ambiente?

### Persistência

O banco utiliza volume?

### Configuração

Credenciais estão fora do código?

### Comunicação

A aplicação utiliza:

```text
db
```

em vez de:

```text
localhost
```

para acessar outro container?

### Boas práticas

- imagem adequada;
- camadas bem organizadas;
- `.dockerignore`;
- usuário não-root quando aplicável;
- ausência de segredos na imagem;
- contexto de build adequado;
- Dockerfile específico para o serviço.

---

# 54. Checklist de entrega

```text
[ ] backend/Dockerfile funcional
[ ] Build da imagem funcionando
[ ] Container do backend funcionando
[ ] Porta publicada corretamente
[ ] backend/.dockerignore configurado
[ ] compose.yaml funcional
[ ] Contexto de build configurado como ./backend
[ ] PostgreSQL configurado
[ ] Volume persistente configurado
[ ] Variáveis de ambiente configuradas
[ ] Comunicação por nome de serviço
[ ] Makefile atualizado
[ ] README atualizado
[ ] Estrutura backend/frontend/docs preservada
[ ] Ambiente reconstruído do zero com sucesso
```

---

# 55. Desafio extra — tornar a solução mais robusta

### Desafio 1

Adicionar healthcheck à API.

### Desafio 2

Adicionar healthcheck ao PostgreSQL.

### Desafio 3

Criar um usuário não-root no container.

### Desafio 4

Separar dependências de desenvolvimento e produção no ambiente Python.

### Desafio 5

Criar um segundo serviço simples, como:

```text
worker
```

e fazê-lo conversar com a API ou com outro serviço.

### Desafio 6

Adicionar uma rede explicitamente nomeada no Compose.

### Desafio 7

Criar comandos no `Makefile`:

```bash
make shell
make clean
```

---

# 56. Conceitos que o aluno precisa levar

Ao terminar a prática, o aluno deve conseguir explicar:

### Imagem

> Artefato imutável utilizado como base para criar containers.

### Container

> Instância em execução de uma imagem, com isolamento de processos e recursos.

### Dockerfile

> Receita declarativa para construir uma imagem de um serviço.

### Volume

> Mecanismo para persistir ou compartilhar dados além do ciclo de vida do container.

### Rede

> Mecanismo que permite a comunicação entre containers.

### Compose

> Forma declarativa de definir e executar aplicações compostas por múltiplos serviços.

### Registry

> Serviço utilizado para armazenar e distribuir imagens.

### Contexto de build

> Conjunto de arquivos disponibilizados ao Docker durante a construção de uma imagem.

No nosso backend:

```text
docker build ./backend
```

faz com que:

```text
backend/
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── app/
└── tests/
```

seja o contexto disponibilizado ao Docker.

Isso permite utilizar:

```dockerfile
COPY pyproject.toml poetry.lock ./
COPY app ./app
```

sem precisar referenciar:

```text
backend/...
```

dentro do Dockerfile.

---

# 57. Relação com Sistemas Distribuídos

Esta prática não é apenas sobre Docker.

Ela introduz problemas que serão recorrentes na disciplina:

```text
Serviço A
    |
    | rede
    v
Serviço B
```

Agora existem questões como:

* O serviço B está disponível?
* Qual endereço devo utilizar?
* Qual porta?
* O serviço iniciou?
* O que acontece se B cair?
* Como persistir dados?
* Como observar logs?
* Como reproduzir o ambiente?
* Como configurar cada ambiente?
* Como escalar uma parte do sistema?

Esses problemas aparecem em sistemas distribuídos reais.

---

# 58. Mapa mental da prática

```text
                    CONTAINERIZAÇÃO
                           |
        +------------------+------------------+
        |                  |                  |
      Docker            Compose           Makefile
        |                  |                  |
   +----+----+        +----+----+        +----+----+
   |    |    |        |    |    |        |    |    |
Imagem Rede Volume   API   DB  Config    up  down logs
   |
Dockerfile
   |
+--+-----------------------+
|                          |
Build                    Runtime
|                          |
COPY/RUN                 CMD
WORKDIR                  ENV
Multi-stage              USER
```

---

# 59. Perguntas para discussão em aula

1. Qual é a diferença entre uma imagem e um container?
2. Por que `localhost` muda de significado dentro de um container?
3. Por que precisamos publicar portas?
4. Qual a diferença entre `COPY` e `RUN`?
5. Por que a ordem das instruções do Dockerfile pode afetar o cache?
6. Para que serve `.dockerignore`?
7. Por que o PostgreSQL precisa de um volume?
8. Qual a vantagem do Compose em relação a vários `docker run`?
9. `depends_on` garante que o banco esteja pronto?
10. Por que não devemos colocar senhas diretamente no Dockerfile?
11. Containerização significa necessariamente microserviços?
12. Qual a diferença entre ambiente de desenvolvimento e produção?
13. O que é o contexto de build?
14. Por que o contexto do backend é `./backend`?
15. Por que o `Dockerfile` do backend está dentro de `backend/`?
16. Qual seria a vantagem de o frontend possuir seu próprio `Dockerfile`?
17. Qual é a responsabilidade do `Dockerfile` e qual é a responsabilidade do `compose.yaml`?
18. Por que não precisamos enviar `frontend/` e `docs/` no contexto de build do backend?

---

# 60. Encerramento

A principal mudança de mentalidade desta prática é sair de:

```text
"Eu instalei tudo na minha máquina."
```

para:

```text
"Eu consigo declarar e reproduzir o ambiente da aplicação."
```

O objetivo não é decorar comandos Docker.

O objetivo é compreender:

```text
Código
  +
Dependências
  +
Configuração
  +
Infraestrutura
       |
       v
Ambiente reproduzível
```

No nosso projeto, essa infraestrutura passa a ser organizada por responsabilidade:

```text
backend/
    |
    +-- Dockerfile
    +-- .dockerignore
    |
    +-- código Python


frontend/
    |
    +-- Dockerfile       # futuramente
    +-- .dockerignore    # futuramente
    |
    +-- código frontend


compose.yaml
    |
    +-- orquestra os serviços


Makefile
    |
    +-- fornece comandos comuns
```

Essa organização será especialmente importante quando o frontend for adicionado ao ambiente Docker.

Na próxima prática, esse ambiente receberá uma aplicação web real com **FastAPI, endpoints, modelos e arquitetura de API**.

A partir daí, o laboratório deixa de ser apenas infraestrutura e passa a construir progressivamente uma aplicação web completa.