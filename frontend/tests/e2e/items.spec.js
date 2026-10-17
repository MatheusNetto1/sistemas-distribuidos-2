import { expect, test } from "@playwright/test";

test("carrega a interface com a lista vazia", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Gerenciador de Itens" }),
  ).toBeVisible();
  await expect(page.getByText("Nenhum item cadastrado.")).toBeVisible();
});

test("cadastra um item e o exibe na listagem", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Nome").fill("Notebook");
  await page.getByLabel("Descrição").fill("14 polegadas");
  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("listitem")).toContainText("Notebook");
  await expect(page.getByText("14 polegadas")).toBeVisible();
  await expect(page.getByText("Nenhum item cadastrado.")).toBeHidden();
});

test("não cadastra item sem nome", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("alert")).toHaveText("O nome é obrigatório.");
  await expect(page.getByText("Nenhum item cadastrado.")).toBeVisible();
});
