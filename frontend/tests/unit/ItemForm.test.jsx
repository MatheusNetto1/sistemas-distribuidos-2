import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ItemForm } from "../../src/components/ItemForm";

describe("ItemForm", () => {
  it("renderiza os campos e o botão", () => {
    render(<ItemForm onAdd={() => {}} />);
    expect(screen.getByLabelText("Nome")).toBeInTheDocument();
    expect(screen.getByLabelText("Descrição")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Adicionar" }),
    ).toBeInTheDocument();
  });

  it("chama onAdd com os valores e limpa o formulário", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<ItemForm onAdd={onAdd} />);

    await user.type(screen.getByLabelText("Nome"), "Notebook");
    await user.type(screen.getByLabelText("Descrição"), "14 polegadas");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(onAdd).toHaveBeenCalledWith({
      name: "Notebook",
      description: "14 polegadas",
    });
    expect(screen.getByLabelText("Nome")).toHaveValue("");
  });

  it("mostra erro e não chama onAdd com nome vazio", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<ItemForm onAdd={onAdd} />);

    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "O nome é obrigatório.",
    );
    expect(onAdd).not.toHaveBeenCalled();
  });
});
