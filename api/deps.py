from fastapi import Depends

from sqlalchemy.orm import Session

from .db_settings import get_db

from .services.main_service import MainService


def get_kpi_service(db: Session = Depends(get_db)):
    return MainService(db)