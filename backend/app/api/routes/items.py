from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item import (
    ItemAlreadyExistsError,
    ItemNotFoundError,
    ItemService,
)

router = APIRouter(prefix="/items", tags=["Items"])

NOT_FOUND = "Item não encontrado"
ALREADY_EXISTS = "Já existe um item com esse nome"


def get_item_service(db: Annotated[Session, Depends(get_db)]) -> ItemService:
    return ItemService(ItemRepository(db))


ServiceDep = Annotated[ItemService, Depends(get_item_service)]


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, service: ServiceDep):
    try:
        return service.create(data)
    except ItemAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, ALREADY_EXISTS) from None


@router.get("/", response_model=list[ItemRead])
def list_items(service: ServiceDep, skip: int = 0, limit: int = 100):
    return service.list(skip, limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ServiceDep):
    try:
        return service.get(item_id)
    except ItemNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND) from None


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    data: ItemUpdate,
    service: ServiceDep,
):
    try:
        return service.update(item_id, data)
    except ItemNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND) from None
    except ItemAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, ALREADY_EXISTS) from None


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ServiceDep):
    try:
        service.delete(item_id)
    except ItemNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND) from None
    return Response(status_code=status.HTTP_204_NO_CONTENT)
