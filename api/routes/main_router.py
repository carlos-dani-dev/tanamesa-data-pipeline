from typing import Annotated

from starlette import status
from fastapi import APIRouter, Depends

from ..deps import get_kpi_service
from ..services.main_service import MainService


router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("/time-survey-administration",
            status_code=status.HTTP_200_OK)
def form_application(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.time_survey_administration()
    return response