# Prática 3 — Pirâmide de Testes com Pytest & CI com GitHub Actions

> **Disciplina:** C216 — Sistemas Distribuídos  
> **Módulo:** 2 — Backend & Qualidade  
> **Prática 3:** Pirâmide de Testes (Unitarios e Integracao com Pytest) & CI com GitHub Actions  
> **Foco:** qualidade de código, validação automatizada e CI

---

## 1. Onde esta prática se encaixa

O laboratório é **contínuo**. Já temos:

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
Testes + CI
        |
        v
Prática 4
FastAPI + Arquitetura + APIs
        |
        v
Prática 5
PostgreSQL + SQLAlchemy + Migrations
        |
        v
Frontend + Integração Full-stack
```

A mudança de mentalidade desta aula é:

```text
"Eu alterei o código e parece funcionar."
                    |
                    v
"Eu alterei o código e tenho testes que verificam
se o comportamento esperado continua funcionando."
                    |
                    v
"O GitHub executa essas verificações automaticamente."
```

---

## 2. Por que testar?

À medida que o sistema cresce, uma alteração pode quebrar comportamentos que funcionavam anteriormente.

Testes automatizados funcionam como uma **rede de segurança**.

Um teste automatizado é um código que verifica outro código.

```python
def soma(a, b):
    return a + b

def test_soma():
    assert soma(2, 3) == 5
```

Podemos pensar em:

```text
Arrange → Act → Assert
Preparar → Executar → Verificar
```

O objetivo é verificar **comportamentos importantes**, e não simplesmente aumentar a quantidade de linhas testadas.

---

## 3. A pirâmide de testes

Uma estratégia clássica é:

```text
        /\
       /E2E\
      /-----\
     /       \
    /Integração\
   /------------\
  /              \
 /   Unitários    \
/__________________\
```

### Testes unitários

- rápidos;
- isolados;
- baratos;
- fáceis de diagnosticar.

### Testes de integração

Verificam a interação entre componentes, como:

```text
API → Serviço → Banco
```

### Testes E2E

Verificam um fluxo completo:

```text
Frontend → API → Banco
```

A pirâmide é um **modelo de estratégia**, não uma regra matemática. Em geral, teremos muitos testes unitários, menos testes de integração e poucos testes E2E.

---

## 4. Configurando Pytest

Como o projeto utiliza Poetry:

```bash
cd backend
poetry add --group dev pytest
```

Executar:

```bash
poetry run pytest
```

O Poetry continua responsável pelas dependências; o Pytest é responsável pela execução dos testes.

Estrutura:

```text
backend/
├── app/
│   └── main.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── poetry.lock
```

O Pytest encontra arquivos como:

```text
test_*.py
*_test.py
```

e funções como:

```python
def test_alguma_coisa():
    ...
```

---

## 5. Primeiro teste

Crie `backend/tests/test_main.py`:

```python
def soma(a, b):
    return a + b


def test_soma():
    assert soma(2, 3) == 5
```

Execute:

```bash
cd backend
poetry run pytest
```

Resultado esperado:

```text
1 passed
```

O `assert` expressa a expectativa do teste:

```python
assert resultado == esperado
```

---

## 6. Testando diferentes cenários

Devemos testar tanto casos de sucesso quanto comportamentos de erro.

### Caso normal

```python
def eh_par(numero):
    return numero % 2 == 0


def test_numero_par():
    assert eh_par(4) is True
```

### Exceções

```python
import pytest


def dividir(a, b):
    if b == 0:
        raise ValueError("divisão por zero")

    return a / b


def test_divisao_por_zero():
    with pytest.raises(ValueError):
        dividir(10, 0)
```

### Parametrização

Quando o mesmo comportamento precisa ser testado com vários valores:

```python
import pytest


@pytest.mark.parametrize(
    "numero, esperado",
    [
        (2, True),
        (3, False),
        (10, True),
        (11, False),
    ],
)
def test_eh_par(numero, esperado):
    assert (numero % 2 == 0) is esperado
```

---

## 7. Fixtures

Fixtures permitem preparar dados ou recursos reutilizáveis:

```python
import pytest


@pytest.fixture
def usuario():
    return {
        "nome": "Maria",
        "email": "maria@example.com",
    }


def test_nome_usuario(usuario):
    assert usuario["nome"] == "Maria"
```

Conceitualmente:

```text
fixture
   |
   v
prepara recurso
   |
   v
teste utiliza
```

Isso será especialmente útil quando adicionarmos banco de dados.

### Boas práticas

Os testes devem ser:

- independentes;
- determinísticos;
- pequenos;
- claros;
- relevantes.

Evite depender desnecessariamente de:

- horário atual;
- valores aleatórios;
- internet;
- serviços externos;
- estado deixado por outro teste.

---

## 8. Unitário x integração

| Característica | Unitário | Integração |
|---|---|---|
| Escopo | pequeno | múltiplos componentes |
| Velocidade | alta | menor |
| Isolamento | alto | menor |
| Banco/rede | geralmente não | pode utilizar |
| Diagnóstico | simples | mais complexo |
| Quantidade | maior | menor |

Não precisamos escolher apenas um tipo. Eles se complementam.

No futuro, poderemos testar endpoints FastAPI:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
```

Esse conceito será aprofundado quando construirmos a API.

---

## 9. Mocking

Quando uma aplicação depende de outro serviço, podemos substituir a dependência por um objeto controlado.

Exemplo:

```text
API
 |
 v
Mock do serviço externo
```

Isso permite testar cenários como:

- sucesso;
- erro;
- timeout;
- resposta inesperada.

Mas mocks não devem ser usados indiscriminadamente. Se tudo for mockado, podemos acabar testando apenas os próprios mocks.

---

## 10. Testes e Makefile

Já utilizamos Makefile na Prática 1. Agora podemos criar:

```makefile
test:
	cd backend && poetry run pytest

test-verbose:
	cd backend && poetry run pytest -v
```

Assim:

```bash
make test
```

torna-se a interface comum para executar os testes.

Mais adiante, poderemos adicionar comandos como:

```text
make lint
make format
make typecheck
make build
make up
make down
```

---

## 11. O que é CI?

**CI — Continuous Integration (Integração Contínua)** é a prática de integrar mudanças frequentemente e executar verificações automatizadas.

Fluxo:

```text
Developer
    |
    | push / Pull Request
    v
GitHub
    |
    v
GitHub Actions
    |
    +-- instalar dependências
    |
    +-- executar testes
    |
    v
PASS / FAIL
```

CI não precisa executar apenas testes. Também pode executar:

- lint;
- formatação;
- type checking;
- build;
- verificações de segurança.

Nesta prática, vamos começar pelo essencial: **testes automatizados**.

---

## 12. GitHub Actions

Workflows do GitHub Actions ficam em:

```text
.github/
└── workflows/
    └── ci.yml
```

Um workflow simples:

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Poetry
        run: pipx install poetry

      - name: Install dependencies
        working-directory: backend
        run: poetry install

      - name: Run tests
        working-directory: backend
        run: poetry run pytest
```

### Entendendo o workflow

- `name`: nome do workflow;
- `on`: eventos que disparam a execução;
- `jobs`: trabalhos realizados;
- `runs-on`: ambiente utilizado;
- `steps`: etapas do job;
- `working-directory`: diretório onde o comando será executado.

O `checkout` disponibiliza o código no runner.

O `setup-python` define a versão do Python.

O `poetry install` instala o ambiente definido pelo projeto.

O `pytest` executa os testes.

> Usar `pipx` para instalar a ferramenta Poetry no runner não significa abandonar o Poetry. O projeto continua utilizando Poetry para gerenciar suas dependências.

---

## 13. O ciclo local + CI

Localmente:

```bash
make test
```

No GitHub:

```text
Pull Request
     |
     v
GitHub Actions
     |
     v
pytest
     |
 +---+---+
 |       |
PASS    FAIL
 |       |
 v       v
revisão  corrigir
```

O ideal é executar **os mesmos testes** localmente e no CI.

Isso cria duas camadas de segurança:

```text
Desenvolvimento local → feedback rápido

GitHub Actions → validação independente
```

---

## 14. Pull Request + CI

O fluxo passa a ser:

```text
Branch
  |
  v
Commit
  |
  v
Push
  |
  v
Pull Request
  |
  v
GitHub Actions
  |
  +-- testes
  |
  v
Revisão
  |
  v
Merge
```

Em um projeto real, podemos configurar regras para exigir que determinados checks passem antes do merge.

Assim, a entrega deixa de ser apenas:

```text
"Código escrito."
```

e passa a ser:

```text
Código
+
Testes
+
CI passando
+
Revisão
```

---

## 15. O que caracteriza um bom teste?

Um bom teste tende a ser:

### Claro

```python
def test_usuario_invalido_retorna_erro():
```

é mais informativo que:

```python
def test_42():
```

### Determinístico

Mesmo cenário → mesmo resultado.

### Independente

Não depende da execução de outro teste.

### Pequeno

Faz uma verificação compreensível.

### Relevante

Protege um comportamento importante.

### Fácil de diagnosticar

Quando falha, ajuda a encontrar o problema.

Evite testes gigantes como:

```text
test_tudo()
```

que executam dezenas de operações diferentes. Quando falharem, será difícil descobrir a causa.

---

## 16. Cobertura

Podemos futuramente medir cobertura com `pytest-cov`:

```bash
poetry add --group dev pytest-cov
poetry run pytest --cov=app
```

Mas atenção:

> **Cobertura alta não significa necessariamente qualidade alta.**

É possível ter 100% de cobertura e testes ruins.

Cobertura é um **indicador**, não uma garantia.

Mais importante que testar todas as linhas é testar os **cenários e comportamentos relevantes**.

---

## 17. Relação com Docker

Docker e testes são complementares.

Podemos executar testes:

### Localmente

```bash
make test
```

### Dentro do container

```bash
docker compose exec api pytest
```

A arquitetura de execução pode evoluir posteriormente. Nesta prática, o foco é compreender a estratégia de testes e CI.

---

# 18. Exercício guiado

Vamos construir a infraestrutura passo a passo.

### Etapa 1 — instalar Pytest

```bash
cd backend
poetry add --group dev pytest
```

### Etapa 2 — criar testes

```text
backend/tests/test_main.py
```

### Etapa 3 — executar

```bash
poetry run pytest
```

### Etapa 4 — adicionar Makefile

```makefile
test:
	cd backend && poetry run pytest
```

### Etapa 5 — criar CI

```text
.github/workflows/ci.yml
```

### Etapa 6 — commit e push

```bash
git add .
git commit -m "ci: add automated tests"
git push
```

### Etapa 7 — abrir Pull Request

Verificar no GitHub:

```text
Actions
  |
  v
CI
  |
  v
pytest
```

---

# 19. Atividade prática

A atividade deve utilizar o **mesmo repositório** das práticas anteriores.

## Objetivo

Criar uma primeira camada formal de qualidade para o backend.

## Requisitos mínimos

- [ ] adicionar Pytest como dependência de desenvolvimento;
- [ ] criar `backend/tests`;
- [ ] criar pelo menos **5 testes unitários**;
- [ ] utilizar `assert`;
- [ ] testar pelo menos um caso de erro;
- [ ] utilizar parametrização;
- [ ] criar pelo menos uma fixture;
- [ ] adicionar `make test`;
- [ ] criar `.github/workflows/ci.yml`;
- [ ] configurar Python no CI;
- [ ] instalar dependências com Poetry;
- [ ] executar Pytest no GitHub Actions;
- [ ] executar o workflow em `push` e `pull_request`;
- [ ] documentar como executar os testes;
- [ ] criar uma Pull Request.

---

# 20. Desafio extra — teste HTTP

Antecipando a próxima prática, podemos testar uma aplicação FastAPI.

Instalar:

```bash
poetry add --group dev fastapi httpx
```

Exemplo:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "ok"}
```

Teste:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
```

A ideia é perceber a evolução:

```text
Teste unitário
      |
      v
Teste HTTP
      |
      v
API
```

Esse conteúdo será aprofundado na próxima prática.

---

# 21. Desafio extra — falha proposital

Depois que os testes passarem:

1. altere propositalmente o código;
2. execute `make test`;
3. observe a falha;
4. faça commit e push;
5. observe o CI falhar;
6. corrija o código;
7. envie novamente;
8. observe o CI passar.

```text
Código correto → CI ✓
       |
Código quebrado → CI ✗
       |
Correção → CI ✓
```

Esse exercício demonstra o principal valor da automação: **feedback rápido sobre regressões**.

---

# 22. Estrutura esperada

```text
laboratorio-web/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   │   └── test_main.py
│   ├── poetry.lock
│   └── pyproject.toml
│
├── frontend/
│
├── docs/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── LICENSE
├── Makefile
└── README.md
```

A estrutura agora possui:

```text
Código
  +
Testes
  +
Automação
```

---

# 23. Testes em sistemas distribuídos

Esta prática também se conecta diretamente à disciplina.

Em um sistema distribuído:

```text
Serviço A
   |
   v
Serviço B
   |
   v
Banco
```

Existem várias possibilidades de falha:

- serviço indisponível;
- resposta inválida;
- timeout;
- banco inacessível;
- comunicação interrompida.

Testes de integração podem verificar parte desses comportamentos.

CI permite repetir essas verificações automaticamente a cada mudança.

---

# 24. Perguntas para discussão

1. Por que testes unitários tendem a ser mais rápidos?
2. Qual a diferença entre teste unitário e teste de integração?
3. Por que não testar tudo somente com E2E?
4. O que uma fixture resolve?
5. Por que testes independentes são importantes?
6. Por que mocks não devem ser usados indiscriminadamente?
7. O que significa CI?
8. Qual a diferença entre testar localmente e no CI?
9. Por que o workflow precisa conhecer o diretório `backend`?
10. Cobertura de 100% significa que o sistema está bem testado?
11. O que acontece quando um teste falha em uma Pull Request?
12. Por que testes não substituem code review?
13. Como esta prática se conecta com Docker?

---

# 25. Conceitos essenciais

### Teste unitário
Verifica uma pequena unidade de comportamento, preferencialmente de forma isolada.

### Teste de integração
Verifica a interação entre diferentes componentes.

### E2E
Verifica um fluxo completo do sistema.

### Pytest
Framework utilizado para escrever e executar testes em Python.

### Fixture
Recurso reutilizável para preparar dados ou contexto de testes.

### Mock
Substituto controlado para uma dependência durante um teste.

### CI
Prática de integrar alterações frequentemente e executar verificações automatizadas.

### GitHub Actions
Plataforma de automação integrada ao GitHub.

### Regressão
Quando uma alteração quebra um comportamento que anteriormente funcionava.

---

# 26. Checklist de entrega

```text
[ ] Pytest configurado
[ ] Dependência adicionada via Poetry
[ ] Diretório tests criado
[ ] Pelo menos 5 testes unitários
[ ] Caso de sucesso testado
[ ] Caso de erro testado
[ ] Parametrização utilizada
[ ] Fixture utilizada
[ ] make test funcionando
[ ] CI configurado
[ ] CI executa em push
[ ] CI executa em pull_request
[ ] Poetry utilizado no CI
[ ] Testes passando localmente
[ ] Testes passando no GitHub
[ ] README atualizado
[ ] Pull Request criada
```

---

# 27. Encerramento

Nas práticas anteriores aprendemos a declarar:

```text
Código
+
Dependências
+
Infraestrutura
```

Agora adicionamos:

```text
Código
+
Dependências
+
Infraestrutura
+
Testes
+
Automação
```

A mudança de mentalidade é:

```text
"Funciona na minha máquina."
          |
          v
"Consigo reproduzir o ambiente."
          |
          v
"Consigo verificar o comportamento."
          |
          v
"O GitHub verifica automaticamente."
```

Nosso fluxo passa a ser:

```text
Desenvolvedor
     |
     v
Código
     |
     v
Testes
     |
     v
Commit / Pull Request
     |
     v
GitHub Actions
     |
 +---+---+
 |       |
FAIL    PASS
 |       |
 v       v
Corrigir Revisão
          |
          v
        Merge
```

A partir da próxima prática, começaremos a construir a aplicação web com **FastAPI, endpoints, modelos e arquitetura de API**.

A infraestrutura criada aqui será reaproveitada. A ideia é que novas funcionalidades possam nascer acompanhadas de testes e sejam automaticamente validadas pelo CI.
