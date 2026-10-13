from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import create_database, get_session
from app.models import Base, Item
from app.schemas import ItemCreate, ItemRead, ItemUpdate


def create_app(database_url: str | None = None) -> FastAPI:
    engine, session_factory = create_database(database_url)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield
        engine.dispose()

    app = FastAPI(title="Imtiaz API", lifespan=lifespan)

    def session_dependency():
        yield from get_session(session_factory)

    SessionDependency = Annotated[Session, Depends(session_dependency)]

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
    def create_item(payload: ItemCreate, session: SessionDependency) -> Item:
        item = Item(**payload.model_dump())
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    @app.get("/items", response_model=list[ItemRead])
    def list_items(session: SessionDependency) -> list[Item]:
        return list(session.scalars(select(Item).order_by(Item.id)))

    @app.get("/items/{item_id}", response_model=ItemRead)
    def get_item(item_id: int, session: SessionDependency) -> Item:
        item = session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @app.put("/items/{item_id}", response_model=ItemRead)
    def update_item(item_id: int, payload: ItemUpdate, session: SessionDependency) -> Item:
        item = session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for field, value in payload.model_dump().items():
            setattr(item, field, value)
        session.commit()
        session.refresh(item)
        return item

    @app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, session: SessionDependency) -> Response:
        item = session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()