from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select
from pydantic import BaseModel

from db.models.base import Base
from schemas.common_schema import IOrderEnum

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * model: A SQLAlchemy model class
        * schema: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db_session

    def get(self, id_: Any) -> ModelType | None:
        query = Select([self.model]).where(self.model.id == id_)  # type: ignore
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: Select | None = None,
    ) -> Sequence[ModelType]:
        if query is None:
            query = Select([self.model]).offset(skip).limit(limit)
        return self.db.execute(query).scalars().all()

    def get_all_ordered(
        self,
        order_by: Any | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
    ) -> Sequence[ModelType]:
        columns = self.model.__table__.columns  # type: ignore

        if order_by is None or order_by.name not in columns:
            order_by = self.model.id  # type: ignore

        if order == IOrderEnum.ascendent:
            query = Select([self.model]).order_by(order_by.asc())  # type: ignore
        else:
            query = Select([self.model]).order_by(order_by.desc())  # type: ignore

        result = self.db.execute(query)
        return result.scalars().all()


    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        try:
            self.db.flush()
        except IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc.orig):
                raise ValueError("Uniqueness constraints not passed") from exc
            elif "FOREIGN KEY constraint failed" in str(exc.orig):
                raise ValueError("Violation of foreign key") from exc
            raise
        return db_obj

    def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        obj_data = db_obj.model_dump(exclude_unset=True)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.db.add(db_obj)
        try:
            self.db.flush()
        except IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc.orig):
                raise ValueError("Uniqueness constraints not passed") from exc
            raise
        return db_obj

    def delete(self, *, id_: Any) -> ModelType | None:
        obj = self.get(id_)
        if not obj:
            return None

        self.db.delete(obj)
        self.db.flush()
        return obj

    def commit(self):
        self.db.commit()
