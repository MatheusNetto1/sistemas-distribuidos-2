# Prática 1 --- Gerenciamento de Dependências com Poetry

## 1. Objetivos da aula

Ao final desta prática, o aluno deverá ser capaz de:

-   compreender o problema de gerenciamento de dependências;
-   criar um projeto Python com Poetry;
-   criar e utilizar um ambiente virtual;
-   adicionar dependências;
-   separar dependências de desenvolvimento;
-   entender o papel do `pyproject.toml`;
-   instalar exatamente as versões registradas no projeto;
-   executar comandos dentro do ambiente do projeto.

> **Contexto:** uma aplicação web não é apenas código próprio. Ela
> depende de frameworks, bibliotecas, ferramentas de teste e outros
> componentes. O gerenciamento dessas dependências precisa ser
> reproduzível para que diferentes desenvolvedores e ambientes consigam
> executar o mesmo projeto.

------------------------------------------------------------------------

# 2. O problema que queremos resolver

Imagine um backend que utiliza:

``` text
FastAPI
Uvicorn
Pytest
```

Um desenvolvedor instala:

``` text
fastapi 1.x
uvicorn 2.x
pytest 9.x
```

Outro instala versões diferentes.

Agora temos:

``` text
Computador A → funciona
Computador B → erro
Servidor      → erro
CI            → erro
```

O objetivo do gerenciamento de dependências é aproximar todos esses
ambientes:

``` text
Projeto
  |
  +-- código
  +-- dependências
  +-- versões
  +-- configuração
        |
        v
Ambiente reproduzível
```

------------------------------------------------------------------------

# 3. O que é Poetry?

O Poetry é uma ferramenta para gerenciamento de projetos e dependências
Python.

Ele centraliza informações importantes no:

``` text
pyproject.toml
```

Um projeto pode ficar assim:

``` text
backend/
├── pyproject.toml
├── poetry.lock
├── src/
│   └── app/
│       └── main.py
└── tests/
    └── test_main.py
```

### Arquivos principais

  Arquivo            Função
  ------------------ ----------------------------------------
  `pyproject.toml`   Configuração do projeto e dependências
  `poetry.lock`      Versões resolvidas das dependências
  `src/`             Código da aplicação
  `tests/`           Testes

------------------------------------------------------------------------

# 4. Verificando a instalação

Verifique:

``` bash
poetry --version
```

Se o comando estiver disponível:

``` text
Poetry (version ...)
```

------------------------------------------------------------------------

# 5. Criando um projeto

Podemos criar um projeto:

``` bash
poetry new backend
```

Estrutura típica:

``` text
backend/
├── README.md
├── pyproject.toml
├── src/
│   └── backend/
│       └── __init__.py
└── tests/
    └── __init__.py
```

Entre no projeto:

``` bash
cd backend
```

------------------------------------------------------------------------

# 6. `pyproject.toml`

Um exemplo simplificado:

``` toml
[project]
name = "backend"
version = "0.1.0"
description = "Backend da aplicação"
requires-python = ">=3.11"

dependencies = [
    "fastapi",
    "uvicorn"
]
```

Dependendo da versão/configuração do Poetry, você também pode encontrar
projetos usando a seção tradicional:

``` toml
[tool.poetry]
name = "backend"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.1.0"
```

> **Para a disciplina:** o importante é compreender o conceito. A
> estrutura exata pode variar conforme a versão do Poetry.

------------------------------------------------------------------------

# 7. Adicionando uma dependência

Por exemplo:

``` bash
poetry add fastapi
```

Depois:

``` bash
poetry add uvicorn
```

O Poetry atualiza o projeto e resolve as dependências necessárias.

Podemos conferir:

``` bash
poetry show
```

------------------------------------------------------------------------

# 8. Dependências de desenvolvimento

Nem tudo é necessário para executar a aplicação.

Por exemplo:

``` text
FastAPI     → aplicação
Uvicorn     → servidor
Pytest      → testes
Ruff        → qualidade do código
```

Podemos adicionar ferramentas de desenvolvimento:

``` bash
poetry add --group dev pytest
```

E:

``` bash
poetry add --group dev ruff
```

A ideia é separar:

``` text
Dependências de produção
        +
Dependências de desenvolvimento
```

------------------------------------------------------------------------

# 9. Ambiente virtual

O Poetry pode criar um ambiente virtual isolado para o projeto.

Confira:

``` bash
poetry env info
```

Você pode executar comandos dentro desse ambiente com:

``` bash
poetry run python --version
```

E:

``` bash
poetry run pytest
```

Isso evita depender das instalações globais da máquina.

------------------------------------------------------------------------

# 10. Por que ambiente virtual?

Imagine dois projetos:

``` text
Projeto A
Django 4.x

Projeto B
Django 5.x
```

Instalar tudo globalmente pode gerar conflitos.

Com ambientes separados:

``` text
Projeto A
└── .venv
    └── Django 4.x

Projeto B
└── .venv
    └── Django 5.x
```

Cada projeto possui seu próprio ambiente.

------------------------------------------------------------------------

# 11. O `poetry.lock`

Quando as dependências são resolvidas, o Poetry registra as versões
específicas no:

``` text
poetry.lock
```

Isso é importante para reprodutibilidade.

Por exemplo:

``` text
pyproject.toml
    ↓
"preciso de FastAPI compatível com determinada versão"
    ↓
poetry.lock
    ↓
"esta é a versão exata resolvida"
```

### Regra prática

Em uma aplicação, normalmente:

``` text
pyproject.toml → versionamento
poetry.lock    → versionamento
.venv/         → NÃO versionar
```

------------------------------------------------------------------------

# 12. Instalando um projeto existente

Imagine que você clonou um projeto:

``` bash
git clone https://github.com/exemplo/backend.git
cd backend
```

Você não precisa instalar cada biblioteca manualmente.

Use:

``` bash
poetry install
```

O Poetry utilizará os arquivos do projeto para reconstruir o ambiente.

------------------------------------------------------------------------

# 13. Criando um pequeno backend

Vamos criar:

``` text
src/app/main.py
```

Conteúdo:

``` python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Olá, Sistemas Distribuídos!"}
```

Execute:

``` bash
poetry run uvicorn app.main:app --reload
```

O backend deverá iniciar localmente.

------------------------------------------------------------------------

# 14. Primeira API

Adicione:

``` python
@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Olá, {name}!"}
```

Agora podemos acessar:

``` text
/hello/Matheus
```

E receber:

``` json
{
    "message": "Olá, Matheus!"
}
```

### O que estamos fazendo?

O navegador/cliente envia:

``` http
GET /hello/Matheus
```

O backend processa:

``` text
FastAPI
  ↓
rota /hello/{name}
  ↓
função hello()
```

E devolve:

``` http
200 OK
Content-Type: application/json
```

------------------------------------------------------------------------

# 15. Testes

Adicione Pytest:

``` bash
poetry add --group dev pytest
```

Crie:

``` text
tests/test_main.py
```

Exemplo:

``` python
def soma(a, b):
    return a + b


def test_soma():
    assert soma(2, 3) == 5
```

Execute:

``` bash
poetry run pytest
```

------------------------------------------------------------------------

# 16. Dependências transitivas

Quando instalamos:

``` bash
poetry add fastapi
```

Não estamos necessariamente instalando apenas um pacote.

FastAPI possui outras dependências.

Visualmente:

``` text
FastAPI
├── dependência A
├── dependência B
└── dependência C
```

O gerenciador resolve essa árvore.

Esse é um dos motivos pelos quais instalar dependências manualmente pode
se tornar difícil em projetos maiores.

------------------------------------------------------------------------

# 17. Atualizando dependências

Para consultar:

``` bash
poetry show --outdated
```

Depois, conforme a necessidade do projeto, podemos atualizar
dependências.

Uma atualização deve ser tratada como mudança potencialmente relevante.

Em aplicações reais:

``` text
Atualizar dependência
        ↓
Executar testes
        ↓
Revisar mudanças
        ↓
CI
        ↓
Merge
```

Não devemos atualizar tudo indiscriminadamente antes de uma entrega.

------------------------------------------------------------------------

# 18. Scripts e comandos do projeto

O projeto pode centralizar comandos frequentes.

Por exemplo, podemos ter:

``` text
poetry run uvicorn app.main:app --reload
poetry run pytest
```

Na próxima prática veremos como um `Makefile` pode criar atalhos:

``` bash
make run
make test
make lint
```

Isso reduz comandos longos e padroniza o desenvolvimento.

------------------------------------------------------------------------

# 19. Exercício guiado

Crie um projeto:

``` bash
poetry new api-distribuida
cd api-distribuida
```

Adicione:

``` bash
poetry add fastapi
poetry add uvicorn
poetry add --group dev pytest
```

Crie um endpoint:

``` text
GET /status
```

Resposta esperada:

``` json
{
    "status": "online"
}
```

Depois:

1.  execute o servidor;
2.  teste o endpoint;
3.  crie um teste;
4.  execute o Pytest;
5.  faça commit do `pyproject.toml`;
6.  faça commit do `poetry.lock`;
7.  confirme que o ambiente virtual não está no Git.

------------------------------------------------------------------------

# 20. Desafio

Crie uma API simples de produtos.

Endpoint:

``` text
GET /products
```

Resposta:

``` json
[
    {
        "id": 1,
        "name": "Notebook"
    },
    {
        "id": 2,
        "name": "Teclado"
    }
]
```

Depois crie:

``` text
GET /products/{id}
```

O objetivo desta atividade não é criar um sistema completo.

O objetivo é entender a relação:

``` text
Projeto Python
    ↓
Dependências
    ↓
Ambiente isolado
    ↓
Aplicação web
    ↓
Testes
```

------------------------------------------------------------------------

# 21. Checklist

-   [ ] Sei explicar o problema de dependências.
-   [ ] Sei o que é Poetry.
-   [ ] Sei para que serve `pyproject.toml`.
-   [ ] Sei para que serve `poetry.lock`.
-   [ ] Sei adicionar dependências.
-   [ ] Sei separar dependências de desenvolvimento.
-   [ ] Sei executar comandos com `poetry run`.
-   [ ] Sei instalar um projeto existente com `poetry install`.
-   [ ] Sei por que ambientes virtuais são importantes.
-   [ ] Sei executar testes pelo ambiente do projeto.

## Conexão com as próximas aulas

``` text
Git
 ↓
Poetry
 ↓
Makefile
 ↓
FastAPI
 ↓
PostgreSQL
 ↓
Testes
 ↓
Docker
```

O objetivo é que o projeto deixe de depender de configurações manuais na
máquina de cada desenvolvedor.
