import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ItemList } from "../../src/components/ItemList";

describe("ItemList", () => {
  it("exibe mensagem quando a lista está vazia", () => {
    render(<ItemList items={[]} />);
    expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
  });

  it("exibe nome e descrição dos itens", () => {
    const items = [
      { id: "1", name: "Notebook", description: "14 polegadas" },
      { id: "2", name: "Mouse", description: "" },
    ];
    render(<ItemList items={items} />);

    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    expect(screen.getByText("Notebook")).toBeInTheDocument();
    expect(screen.getByText("14 polegadas")).toBeInTheDocument();
    expect(screen.getByText("Mouse")).toBeInTheDocument();
  });
});
