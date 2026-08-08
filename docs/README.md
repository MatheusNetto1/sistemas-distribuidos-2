# Prática 1 — Git/GitHub, Poetry e Makefile

## 1. Labels do repositório

As labels serão utilizadas para organizar Pull Requests e identificar rapidamente o tipo, escopo, finalidade e prática relacionada a cada entrega.

### Como criar as labels

Vocês podem criar as labels manualmente pelo GitHub ou utilizar o **GitHub CLI (`gh`)**.

> **Opção recomendada:** executar o comando abaixo dentro do diretório do repositório, após fazer login no GitHub CLI com `gh auth login`.

```bash
gh label create "Backend" --color "1D76DB" --description "Alterações relacionadas à API, regras de negócio e código do servidor." \ && 
gh label create "Frontend" --color "5319E7" --description "Alterações relacionadas à interface, JavaScript, HTML, CSS e interação com o usuário." \ &&
gh label create "Full Stack" --color "6F42C1" --description "Alterações que envolvem simultaneamente frontend e backend." \ && 
gh label create "Database" --color "0052CC" --description "Alterações relacionadas ao PostgreSQL, modelos, consultas, migrations e persistência." && \
gh label create "DevOps" --color "FBCA04" --description "Infraestrutura, Docker, Makefile, ambientes, automação e ferramentas de desenvolvimento." && \
gh label create "CI/CD" --color "F9D0C4" --description "GitHub Actions, pipelines, integração contínua e automação de entrega." && \
gh label create "Feature" --color "0E8A16" --description "Adiciona uma nova funcionalidade ao sistema." && \
gh label create "Bug" --color "D73A4A" --description "Corrige um comportamento incorreto ou problema existente." && \
gh label create "Refactor" --color "A2EEEF" --description "Melhora a estrutura interna do código sem alterar seu comportamento esperado." && \
gh label create "Test" --color "BFDADC" --description "Adiciona, altera ou melhora testes automatizados." && \
gh label create "Documentation" --color "0075CA" --description "Adiciona ou atualiza documentação do projeto." && \
gh label create "Chore" --color "FEF2C0" --description "Alterações de manutenção que não representam uma funcionalidade diretamente." && \
gh label create "Em revisão" --color "FBCA04" --description "PR aguardando revisão e avaliação." && \
gh label create "Aprovado" --color "0E8A16" --description "PR revisado e aprovado." && \
gh label create "Alterações solicitadas" --color "D93F0B" --description "A revisão encontrou problemas que precisam ser corrigidos antes da aprovação." && \
gh label create "Prática 1" --color "C5DEF5" --description "Entrega relacionada à Prática 1 — Git, dependências e Makefile." && \
gh label create "Prática 2" --color "BFD4F2" --description "Entrega relacionada à Prática 2 — Backend e APIs com FastAPI." && \
gh label create "Prática 3" --color "A9D6E5" --description "Entrega relacionada à Prática 3 — Persistência e banco de dados." && \
gh label create "Prática 4" --color "9AD9DB" --description "Entrega relacionada à Prática 4 — Testes e qualidade." && \
gh label create "Prática 5" --color "B7E4C7" --description "Entrega relacionada à Prática 5 — CI/CD e automação." && \
gh label create "Prática 6" --color "D8C3E8" --description "Entrega relacionada à Prática 6 — Frontend moderno com JavaScript." && \
gh label create "Prática 7" --color "E5C1CD" --description "Entrega relacionada à Prática 7 — Integração Full Stack, Docker e E2E." && \
gh label create "API" --color "0366D6" --description "Alterações relacionadas à criação, consumo ou comportamento de APIs." && \
gh label create "Docker" --color "2496ED" --description "Alterações relacionadas a Docker e Docker Compose." && \
gh label create "PostgreSQL" --color "336791" --description "Alterações específicas relacionadas ao PostgreSQL." && \
gh label create "Security" --color "B60205" --description "Alterações relacionadas a autenticação, autorização, validação ou segurança." && \
gh label create "Performance" --color "5319E7" --description "Melhorias voltadas a desempenho, eficiência ou redução de custos computacionais."
```

> **Importante:** no `gh label create`, a cor deve ser informada **sem o `#`**. Por exemplo, `#1D76DB` deve ser informado como `1D76DB`.

### Referência das labels

| Label | Cor | Descrição |
| :---: | :---: | :--- |
| **Backend** | `#1D76DB` | Alterações relacionadas à API, regras de negócio e código do servidor. |
| **Frontend** | `#5319E7` | Alterações relacionadas à interface, JavaScript, HTML, CSS e interação com o usuário. |
| **Full Stack** | `#6F42C1` | Alterações que envolvem simultaneamente frontend e backend. |
| **Database** | `#0052CC` | Alterações relacionadas ao PostgreSQL, modelos, consultas, migrations e persistência. |
| **DevOps** | `#FBCA04` | Infraestrutura, Docker, Makefile, ambientes, automação e ferramentas de desenvolvimento. |
| **CI/CD** | `#F9D0C4` | GitHub Actions, pipelines, integração contínua e automação de entrega. |
| **Feature** | `#0E8A16` | Adiciona uma nova funcionalidade ao sistema. |
| **Bug** | `#D73A4A` | Corrige um comportamento incorreto ou problema existente. |
| **Refactor** | `#A2EEEF` | Melhora a estrutura interna do código sem alterar seu comportamento esperado. |
| **Test** | `#BFDADC` | Adiciona, altera ou melhora testes automatizados. |
| **Documentation** | `#0075CA` | Adiciona ou atualiza documentação do projeto. |
| **Chore** | `#FEF2C0` | Alterações de manutenção que não representam uma funcionalidade diretamente. |
| **Em revisão** | `#FBCA04` | PR aguardando revisão e avaliação. |
| **Aprovado** | `#0E8A16` | PR revisado e aprovado. |
| **Alterações solicitadas** | `#D93F0B` | A revisão encontrou problemas que precisam ser corrigidos antes da aprovação. |
| **Prática 1** | `#C5DEF5` | Entrega relacionada à Prática 1 — Git, dependências e Makefile. |
| **Prática 2** | `#BFD4F2` | Entrega relacionada à Prática 2 — Backend e APIs com FastAPI. |
| **Prática 3** | `#A9D6E5` | Entrega relacionada à Prática 3 — Persistência e banco de dados. |
| **Prática 4** | `#9AD9DB` | Entrega relacionada à Prática 4 — Testes e qualidade. |
| **Prática 5** | `#B7E4C7` | Entrega relacionada à Prática 5 — CI/CD e automação. |
| **Prática 6** | `#D8C3E8` | Entrega relacionada à Prática 6 — Frontend moderno com JavaScript. |
| **Prática 7** | `#E5C1CD` | Entrega relacionada à Prática 7 — Integração Full Stack, Docker e E2E. |
| **API** | `#0366D6` | Alterações relacionadas à criação, consumo ou comportamento de APIs. |
| **Docker** | `#2496ED` | Alterações relacionadas a Docker e Docker Compose. |
| **PostgreSQL** | `#336791` | Alterações específicas relacionadas ao PostgreSQL. |
| **Security** | `#B60205` | Alterações relacionadas a autenticação, autorização, validação ou segurança. |
| **Performance** | `#5319E7` | Melhorias voltadas a desempenho, eficiência ou redução de custos computacionais. |
