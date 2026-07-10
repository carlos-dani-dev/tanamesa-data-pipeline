from fastapi import Depends

from sqlalchemy.orm import Session

from api.db_settings import get_db

from api.services.main_service import MainService


def get_kpi_service(db: Session = Depends(get_db)):
    return MainService(db)