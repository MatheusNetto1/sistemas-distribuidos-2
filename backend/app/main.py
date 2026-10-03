from fastapi import FastAPI

from app.api.routes.items import router as items_router

app = FastAPI()

app.include_router(items_router)


@app.get("/")
def root():
    return {"message": "Laboratório distribuído funcionando!"}
