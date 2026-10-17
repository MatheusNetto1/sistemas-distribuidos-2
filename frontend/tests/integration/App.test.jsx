import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import App from "../../src/App";

describe("App", () => {
  it("começa com a lista vazia", () => {
    render(<App />);
    expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
  });

  it("cadastra um item e o exibe na lista", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText("Nome"), "Notebook");
    await user.type(screen.getByLabelText("Descrição"), "14 polegadas");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(screen.getByText("Notebook")).toBeInTheDocument();
    expect(screen.getByText("14 polegadas")).toBeInTheDocument();
    expect(
      screen.queryByText("Nenhum item cadastrado."),
    ).not.toBeInTheDocument();
  });

  it("não cadastra item com nome inválido", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText("Nome"), "   ");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
  });

  it("acumula vários itens", async () => {
    const user = userEvent.setup();
    render(<App />);

    for (const name of ["Notebook", "Mouse"]) {
      await user.type(screen.getByLabelText("Nome"), name);
      await user.click(screen.getByRole("button", { name: "Adicionar" }));
    }

    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });
});
