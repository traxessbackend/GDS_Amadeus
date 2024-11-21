import logging
from typing import Any

from sqlalchemy import delete
from sqlalchemy.exc import ArgumentError, DataError, IntegrityError
from sqlalchemy.orm import Session

from db.crud.base_crud import BaseCrud
from db.models.gds_reports import GDSReports
from db.schemas.gds_reports_schema import (
    GDSReportSchemaCreate,
    GDSReportSchemaUpdate
)

logger = logging.getLogger(__name__)


class GDSReportCrud(BaseCrud[GDSReports, GDSReportSchemaCreate, GDSReportSchemaUpdate]):
    def __init__(self, db_session: Session):
        self.db = db_session
        super().__init__(model=GDSReports, db_session=db_session)

    def create(self, *, obj_in: GDSReportSchemaCreate) -> GDSReports | dict[str, str]:
        try:
            db_phone_model = GDSReports(**obj_in.model_dump())
            self.db.add(db_phone_model)
            self.db.flush()
            return db_phone_model
        except IntegrityError as ie:
            if "foreign key constraint" in str(ie.orig):
                return {"error": "Invalid foreign key constraint."}
            elif "duplicate key value" in str(ie.orig):
                return {"error": "Duplicate key value."}
            else:
                return {"error": "Integrity error."}
        except ArgumentError:
            return {"error": "Invalid Argument passed."}
        except DataError:
            return {"error": "Invalid Data passed."}
        except Exception as e:
            return {"error": str(e)}

    def update(self, *, db_obj: GDSReports, obj_in: GDSReportSchemaUpdate | dict[str, Any]) -> GDSReports | dict[str, str]:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True, exclude_defaults=True)
            return super().update(db_obj=db_obj, obj_in=update_data)
        except IntegrityError as ie:
            if "foreign key constraint" in str(ie.orig):
                return {"error": "Invalid foreign key constraint."}
            elif "duplicate key value" in str(ie.orig):
                return {"error": "Duplicate key value."}
            else:
                return {"error": "Integrity error."}
        except ArgumentError:
            return {"error": "Invalid Argument passed."}
        except DataError:
            return {"error": "Invalid Data passed."}
        except Exception as e:
            return {"error": str(e)}

    def delete(self, id_: int) -> GDSReports | str:
        delete_result = "NotFound"
        try:
            with self.db.begin_nested() as nested:
                deleted_row = self.db.execute(
                    delete(GDSReports)
                    .returning(GDSReports)
                    .where(GDSReports.id == id_)
                ).scalar()
                if deleted_row is not None:
                    delete_result = deleted_row
                nested.commit()
        except IntegrityError:
            nested.rollback()
            delete_result = "IntegrityError"
        except Exception as error:
            nested.rollback()
            logger.error("Unexpected error when deleting GDSReports record with id `%s` - `%s`", id_, error)
            raise error
        return delete_result
