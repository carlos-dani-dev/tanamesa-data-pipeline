from typing import Annotated

from starlette import status
from fastapi import APIRouter, Depends

from ..deps import get_kpi_service
from ..services.main_service import MainService


router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("/form-application/time",
            status_code=status.HTTP_200_OK)
def time_form_application(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.time_survey_administration()
    return response

@router.get("/form-application/cities",
            status_code=status.HTTP_200_OK)
def submissions_by_city(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.submissions_by_city()
    return response

@router.get("/beneficiaries-socioechonomics/main-stats",
            status_code=status.HTTP_200_OK)
def beneficiaries_socioechonomics_main_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.beneficiaries_socioechonomics_stats()
    return response