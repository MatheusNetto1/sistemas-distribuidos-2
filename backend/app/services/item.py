from app.models.item import Item
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemNotFoundError(Exception):
    pass


class ItemAlreadyExistsError(Exception):
    pass


class ItemService:
    """Regras de negócio dos itens. Não conhece HTTP nem SQL."""

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create(self, data: ItemCreate) -> Item:
        # Regra de negócio: o nome do item deve ser único.
        if self.repository.get_by_name(data.name):
            raise ItemAlreadyExistsError(data.name)
        return self.repository.create(data.name, data.description)

    def get(self, item_id: int) -> Item:
        item = self.repository.get_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item

    def list(self, skip: int = 0, limit: int = 100) -> list[Item]:
        return self.repository.get_all(skip, limit)

    def update(self, item_id: int, data: ItemUpdate) -> Item:
        item = self.get(item_id)
        changes = data.model_dump(exclude_unset=True)
        if changes.get("name") is None:
            changes.pop("name", None)  # name é obrigatório no banco
        elif changes["name"] != item.name and self.repository.get_by_name(
            changes["name"]
        ):
            raise ItemAlreadyExistsError(changes["name"])
        return self.repository.update(item, changes)

    def delete(self, item_id: int) -> None:
        self.repository.delete(self.get(item_id))
