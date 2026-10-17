import { describe, expect, it } from "vitest";
import { NAME_MAX_LENGTH, validateItem } from "../../src/validation";

describe("validateItem", () => {
  it("aceita nome preenchido e descrição vazia", () => {
    const { errors, values } = validateItem({
      name: "Notebook",
      description: "",
    });
    expect(errors).toEqual({});
    expect(values).toEqual({ name: "Notebook", description: "" });
  });

  it("remove espaços nas extremidades", () => {
    const { values } = validateItem({
      name: "  Mouse ",
      description: " sem fio ",
    });
    expect(values).toEqual({ name: "Mouse", description: "sem fio" });
  });

  it("rejeita nome vazio ou só com espaços", () => {
    const { errors } = validateItem({ name: "   ", description: "" });
    expect(errors.name).toBeDefined();
  });

  it("rejeita nome acima do limite", () => {
    const name = "a".repeat(NAME_MAX_LENGTH + 1);
    const { errors } = validateItem({ name, description: "" });
    expect(errors.name).toBeDefined();
  });
});
