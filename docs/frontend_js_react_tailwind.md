# Prática 6 — Frontend Moderno com React, Tailwind CSS, Vitest e Playwright

> **Disciplina:** C216 — Sistemas Distribuídos  
> **Módulo:** Frontend & Consumo  
> **Prática 6:** JavaScript, React, Tailwind CSS, Biome, Vitest, Playwright e CI  
> **Objetivo:** criar um frontend independente, testado e preparado para a integração full-stack da Prática 7.

---

## 1. Contexto e objetivos

Nas práticas anteriores, organizamos o desenvolvimento do backend, com ferramentas de qualidade, testes e integração contínua. Agora vamos aplicar os mesmos princípios ao **frontend**, mas **sem consumir a API ainda**.

Ao final desta prática, teremos uma aplicação React que permite **visualizar e cadastrar itens (nome e descrição) em memória**, com validação, estilização, lint, formatação, testes unitários, de integração e E2E, e validação no GitHub Actions.

| Backend (práticas anteriores) | Frontend (Prática 6) |
| --- | --- |
| Python + FastAPI | JavaScript + React |
| Poetry | npm |
| Organização em camadas | Componentes e organização por responsabilidades |
| Ruff | Biome |
| Pytest | Vitest + React Testing Library (unitários/integração) e Playwright (E2E) |
| GitHub Actions (`ci-backend.yml`) | GitHub Actions (`ci-frontend.yml`) |
| API + banco de dados | Estado local, sem API nesta prática |

**Pré-requisitos:** Node.js 22 LTS ou superior, npm, Git e editor de código. Confirme com `node --version` e `npm --version`.

## 2. Conceitos essenciais

- **Frontend:** parte da aplicação com a qual o usuário interage, executada no navegador.
- **React:** biblioteca para construir interfaces com componentes reutilizáveis (JSX = HTML dentro do JavaScript).
- **Vite:** ferramenta de desenvolvimento e build.
- **Tailwind CSS:** classes utilitárias para estilizar diretamente no JSX.
- **Estado (`useState`):** dados que mudam ao longo da interação e provocam nova renderização.
- **Props:** dados passados de um componente pai para um filho (inclusive funções, como `onAdd`).
- **Biome:** lint e formatação em uma única ferramenta (equivalente ao Ruff).

Nesta prática, os dados são temporários e desaparecem ao atualizar a página.

## 3. Estrutura do projeto

O diretório `frontend/` fica na raiz do repositório, ao lado de `backend/`. O projeto usa JavaScript puro (sem TypeScript) e npm.

```text
repositorio/
├── backend/                       # práticas anteriores (inalterado)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ItemForm.jsx       # formulário (nome + descrição)
│   │   │   └── ItemList.jsx       # listagem e estado vazio
│   │   ├── App.jsx                # guarda o estado dos itens
│   │   ├── validation.js          # regras de validação (função pura)
│   │   ├── index.css
│   │   └── main.jsx
│   ├── tests/
│   │   ├── setup.js               # configuração do Vitest
│   │   ├── unit/                  # Vitest: funções e componentes isolados
│   │   ├── integration/           # Vitest: formulário + lista no App
│   │   └── e2e/                   # Playwright
│   ├── biome.json
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── playwright.config.js
│   └── vite.config.js             # Vite + Tailwind + Vitest
└── .github/workflows/
    ├── ci-backend.yml
    └── ci-frontend.yml
```

### Criando o projeto do zero

Se a pasta `frontend/` ainda não existir, crie-a e instale as dependências:

```bash
mkdir frontend && cd frontend
npm init -y
npm install react react-dom
npm install --save-dev vite @vitejs/plugin-react tailwindcss @tailwindcss/vite
npm install --save-dev vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install --save-dev @playwright/test
npm install --save-dev --save-exact @biomejs/biome
```

No `package.json`, defina `"type": "module"` e os scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "biome lint .",
    "format": "biome format --write .",
    "format:check": "biome format .",
    "check": "biome check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test"
  }
}
```

Crie também `frontend/.gitignore` com `node_modules/`, `dist/`, `playwright-report/` e `test-results/`, e versione o `package-lock.json` (a CI depende dele).

## 4. Vite e Tailwind CSS

O Tailwind v4 integra-se ao Vite por plugin; **não é necessário `tailwind.config.js`**. O mesmo `vite.config.js` também configura o Vitest (seção 7).

```js
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.js"],
    include: [
      "tests/unit/**/*.test.{js,jsx}",
      "tests/integration/**/*.test.{js,jsx}",
    ],
  },
});
```

`src/index.css` contém apenas:

```css
@import "tailwindcss";
```

`index.html` tem `<div id="root">` e carrega `/src/main.jsx`, que renderiza `<App />` e importa `./index.css`.

Execute `npm run dev` (ou `make frontend-dev`) e abra `http://localhost:5173`.

## 5. Implementando a interface

O recurso é **item**, com os mesmos campos do backend (`name` obrigatório com até 100 caracteres e `description` opcional), mas sem comunicação entre os projetos.

### `src/validation.js` — regra pura, fácil de testar

```js
export const NAME_MAX_LENGTH = 100;

export function validateItem({ name, description }) {
  const errors = {};
  const trimmedName = name.trim();

  if (!trimmedName) {
    errors.name = "O nome é obrigatório.";
  } else if (trimmedName.length > NAME_MAX_LENGTH) {
    errors.name = `O nome deve ter no máximo ${NAME_MAX_LENGTH} caracteres.`;
  }

  return {
    errors,
    values: { name: trimmedName, description: description.trim() },
  };
}
```

### `src/components/ItemForm.jsx`

```jsx
import { useState } from "react";
import { validateItem } from "../validation";

export function ItemForm({ onAdd }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [errors, setErrors] = useState({});

  function handleSubmit(event) {
    event.preventDefault();
    const result = validateItem({ name, description });
    setErrors(result.errors);
    if (Object.keys(result.errors).length > 0) return;

    onAdd(result.values);
    setName("");
    setDescription("");
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="space-y-1">
        <label htmlFor="item-name" className="block text-sm font-medium">Nome</label>
        <input
          id="item-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          aria-invalid={errors.name ? "true" : "false"}
          aria-describedby={errors.name ? "item-name-error" : undefined}
          className="w-full rounded border border-slate-300 p-2"
        />
        {errors.name && (
          <p id="item-name-error" role="alert" className="text-sm text-red-700">{errors.name}</p>
        )}
      </div>
      <div className="space-y-1">
        <label htmlFor="item-description" className="block text-sm font-medium">Descrição</label>
        <textarea
          id="item-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          rows={3}
          className="w-full rounded border border-slate-300 p-2"
        />
      </div>
      <button type="submit" className="w-full rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 sm:w-auto">
        Adicionar
      </button>
    </form>
  );
}
```

> O arquivo do repositório está formatado pelo Biome (JSX quebrado em várias linhas); aqui os exemplos foram compactados para leitura.

### `src/components/ItemList.jsx`

```jsx
export function ItemList({ items }) {
  if (items.length === 0) {
    return <p className="text-slate-600">Nenhum item cadastrado.</p>;
  }

  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <p className="font-medium">{item.name}</p>
          {item.description && <p className="text-sm text-slate-600">{item.description}</p>}
        </li>
      ))}
    </ul>
  );
}
```

### `src/App.jsx`

```jsx
import { useState } from "react";
import { ItemForm } from "./components/ItemForm";
import { ItemList } from "./components/ItemList";

export default function App() {
  const [items, setItems] = useState([]);

  // Na Prática 7, esta função passará a chamar a API (POST /items).
  function addItem({ name, description }) {
    setItems((current) => [...current, { id: crypto.randomUUID(), name, description }]);
  }

  return (
    <main className="mx-auto min-h-screen max-w-xl space-y-6 p-4 sm:p-6">
      <h1 className="text-3xl font-bold">Gerenciador de Itens</h1>
      <ItemForm onAdd={addItem} />
      <section aria-labelledby="items-heading" className="space-y-3">
        <h2 id="items-heading" className="text-xl font-semibold">Itens cadastrados</h2>
        <ItemList items={items} />
      </section>
    </main>
  );
}
```

**Para discutir em aula:** onde o estado está armazenado? Quais componentes recebem props? Por que usamos `key` na lista? Qual função será trocada por uma chamada HTTP na Prática 7 (`addItem`)?

## 6. Qualidade de código com Biome

Inicialize com `npx biome init` e ajuste o `biome.json` (indentação com espaços, arquivos ignorados):

```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.15/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": {
    "ignoreUnknown": true,
    "includes": ["**", "!**/node_modules", "!**/dist", "!**/coverage", "!**/playwright-report", "!**/test-results", "!**/package-lock.json"]
  },
  "formatter": { "enabled": true, "indentStyle": "space", "indentWidth": 2 },
  "linter": { "enabled": true, "rules": { "preset": "recommended" } },
  "javascript": { "formatter": { "quoteStyle": "double" } },
  "assist": { "enabled": true, "actions": { "source": { "organizeImports": "on" } } }
}
```

> Use a mesma versão do pacote instalado no campo `$schema` (veja `npx biome --version`).

```bash
npm run format        # aplica a formatação
npm run lint          # regras de lint
npm run format:check  # verifica a formatação sem alterar arquivos (usado na CI)
npm run check         # lint + formatação + organização de imports
```

Assim como o Ruff no backend, **a CI falha se o código não estiver formatado**: rode `npm run format` antes de commitar. Não use ESLint nem Prettier.

## 7. Testes com Vitest e React Testing Library

### Tipos de teste

| Tipo | O que valida | Ferramenta | Onde roda |
| --- | --- | --- | --- |
| **Unitário** | Uma unidade isolada: uma função ou um componente | Vitest + RTL | jsdom (rápido) |
| **Integração** | Vários componentes trabalhando juntos (ex.: formulário + lista no `App`) | Vitest + RTL + user-event | jsdom |
| **E2E** | O fluxo completo, na aplicação real | Playwright | Navegador real |

Quanto mais acima na lista, mais rápido e mais barato; quanto mais abaixo, mais próximo do uso real. Usamos os três de forma complementar.

### O que é Vitest

**Vitest** é um executor de testes para projetos Vite (equivalente ao Pytest do backend). Reaproveita o `vite.config.js`, tem API parecida com a do Jest (`describe`, `it`, `expect`, `vi.fn`) e suporta JSX sem configuração extra. O **jsdom** simula o DOM do navegador no Node. A **React Testing Library (RTL)** renderiza componentes e os consulta como o usuário os enxerga (por rótulo, papel, texto), e o **user-event** simula digitação e cliques.

### Configuração

A seção `test` do `vite.config.js` (seção 4) ativa o jsdom e o arquivo de setup. O `tests/setup.js` registra os matchers do `jest-dom` (`toBeInTheDocument`, `toHaveValue`...) e limpa o DOM após cada teste:

```js
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(cleanup);
```

O `include` limita o Vitest a `tests/unit` e `tests/integration`, para que ele não tente executar os testes do Playwright.

### Teste unitário

Função pura (`tests/unit/validation.test.js`):

```js
import { describe, expect, it } from "vitest";
import { validateItem } from "../../src/validation";

describe("validateItem", () => {
  it("rejeita nome vazio ou só com espaços", () => {
    const { errors } = validateItem({ name: "   ", description: "" });
    expect(errors.name).toBeDefined();
  });
});
```

Componente isolado (`tests/unit/ItemForm.test.jsx`), usando `vi.fn()` no lugar do pai:

```jsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { ItemForm } from "../../src/components/ItemForm";

it("mostra erro e não chama onAdd com nome vazio", async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
  render(<ItemForm onAdd={onAdd} />);

  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(screen.getByRole("alert")).toHaveTextContent("O nome é obrigatório.");
  expect(onAdd).not.toHaveBeenCalled();
});
```

### Teste de integração: formulário + listagem

Renderiza o `App` inteiro e verifica o comportamento visível (`tests/integration/App.test.jsx`):

```jsx
it("cadastra um item e o exibe na lista", async () => {
  const user = userEvent.setup();
  render(<App />);

  await user.type(screen.getByLabelText("Nome"), "Notebook");
  await user.type(screen.getByLabelText("Descrição"), "14 polegadas");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(screen.getByText("Notebook")).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();
  expect(screen.queryByText("Nenhum item cadastrado.")).not.toBeInTheDocument();
});
```

Repare que o teste **não** olha o estado interno nem os nomes das funções: apenas o que o usuário vê. Isso o mantém válido mesmo se a implementação mudar (por exemplo, na Prática 7).

### Executando

```bash
npm run test         # execução única (modo CI)
npm run test:watch   # reexecuta ao salvar (desenvolvimento)
make frontend-test   # a partir da raiz
```

Na CI, `npm run test` roda sem interação, depois do Biome e antes do build.

## 8. Testes E2E com Playwright

Um teste E2E valida o fluxo completo **no navegador**. Instale o Chromium (uma vez por máquina):

```bash
npx playwright install chromium
```

`playwright.config.js`:

```js
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["github"], ["html", { open: "never" }]] : "list",
  use: { baseURL: "http://127.0.0.1:5173", trace: "on-first-retry" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run dev -- --host 127.0.0.1 --port 5173 --strictPort",
    url: "http://127.0.0.1:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
```

`tests/e2e/items.spec.js` (fluxo principal):

```js
import { expect, test } from "@playwright/test";

test("cadastra um item e o exibe na listagem", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Nome").fill("Notebook");
  await page.getByLabel("Descrição").fill("14 polegadas");
  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("listitem")).toContainText("Notebook");
  await expect(page.getByText("Nenhum item cadastrado.")).toBeHidden();
});
```

O arquivo completo também cobre o carregamento da interface e a validação de nome vazio. Execute `npm run test:e2e` (ou `make frontend-test-e2e`): o Playwright inicia o Vite sozinho via `webServer`. Os diretórios `playwright-report/` e `test-results/` são ignorados pelo Git.

## 9. Makefile

Os comandos do backend foram mantidos; foram adicionados os do frontend (que usam `npm --prefix frontend`, então funcionam a partir da raiz):

| Comando | Ação |
| --- | --- |
| `make frontend-install` | `npm ci` |
| `make frontend-dev` | servidor de desenvolvimento (Vite) |
| `make frontend-lint` | `biome lint` |
| `make frontend-format` | `biome format --write` |
| `make frontend-check` | lint + formatação sem alterar arquivos |
| `make frontend-test` | Vitest |
| `make frontend-test-e2e` | Playwright |
| `make frontend-build` | build de produção |
| `make check-all` | backend (Ruff + Pytest) + frontend (Biome, Vitest, build, E2E) |

## 10. Integração contínua com GitHub Actions

Já existe `ci-backend.yml`. Criamos `.github/workflows/ci-frontend.yml`, com o mesmo estilo, executado em pull requests (e em pushes na `main`) que alterem `frontend/**`:

```yaml
name: CI - Frontend

on:
  pull_request:
    paths:
      - "frontend/**"
      - ".github/workflows/ci-frontend.yml"
  push:
    branches:
      - main
    paths:
      - "frontend/**"
      - ".github/workflows/ci-frontend.yml"

jobs:
  frontend:
    name: Biome, Vitest, Build e Playwright
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm run test
      - run: npm run build
      - run: npx playwright install --with-deps chromium
      - run: npm run test:e2e
      - name: Upload Playwright Report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 7
```

(O arquivo real nomeia cada passo com `name:`.)

```text
Push / Pull Request
        ↓
     npm ci
        ↓
  Biome (lint + format)
        ↓
 Vitest (unit + integração)
        ↓
    Vite build
        ↓
 Playwright E2E
        ↓
   CI aprovada ✓
```

Como os dois workflows usam `paths`, **um PR que só altera `frontend/` não executa a CI do backend (e vice-versa)**. Se algum check for obrigatório na proteção de branch, lembre-se de que ele ficará "pendente" quando o workflow não for disparado. A CI depende do `frontend/package-lock.json` versionado.

## 11. Docker

A containerização do frontend e a execução conjunta com o backend ficam para a **Prática 7**. O `compose.yml` e o backend não foram alterados.

## 12. Atividade prática e critérios de entrega

**Desafio:** implementar o gerenciador de itens (nome e descrição) com validação, Tailwind, Biome, testes em três níveis e CI, **sem** chamadas ao backend.

**Checklist antes da entrega** (a partir da raiz, ou `make check-all`):

```bash
cd frontend
npm ci
npm run lint
npm run format:check
npm run test
npm run build
npm run test:e2e
```

**Critérios de aceite:** interface funcional e responsiva, componentes organizados, nenhuma chamada ao backend, testes unitários, de integração e E2E passando, e workflow de CI aprovado. Registre as evidências no pull request, com as labels `Frontend`, `Test` e `Prática 6`.

## 13. Próxima prática: integração full-stack

Na **Prática 7**, `addItem` e a listagem passarão a usar a API FastAPI, com CORS, Docker Compose multicontêiner e E2E envolvendo frontend, backend e banco.

---

### Referências

- [React — documentação](https://react.dev/learn)
- [Vite — guia](https://vite.dev/guide/)
- [Vitest — guia](https://vitest.dev/guide/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Tailwind CSS — instalação com Vite](https://tailwindcss.com/docs/installation/using-vite)
- [Biome — documentação](https://biomejs.dev/)
- [Playwright — introdução](https://playwright.dev/docs/intro)
- [GitHub Actions — documentação](https://docs.github.com/actions)
