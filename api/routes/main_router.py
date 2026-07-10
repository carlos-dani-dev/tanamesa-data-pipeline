from typing import Annotated

from starlette import status
from fastapi import APIRouter, Depends

from ..deps import get_kpi_service
from ..services.main_service import MainService


router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("/application/time",
            status_code=status.HTTP_200_OK)
def time_survey_application(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.time_survey_application()
    return response

@router.get("/application/cities",
            status_code=status.HTTP_200_OK)
def submissions_by_city(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.submissions_by_city()
    return response

@router.get("/socioechonomics/main-stats",
            status_code=status.HTTP_200_OK)
def beneficiaries_socioechonomics_main_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.beneficiaries_socioechonomics_stats()
    return response

@router.get("/socioechonomics/access",
            status_code=status.HTTP_200_OK)
def consistency_of_access(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.consistency_of_access()
    return response

@router.get("/socioechonomics/dependency",
            status_code=status.HTTP_200_OK)
def program_dependency(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.program_dependency()
    return response

@router.get("/socioechonomics/assisted-families",
            status_code=status.HTTP_200_OK)
def assisted_families_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.assisted_families()
    return response

@router.get("/socioechonomics/local-access",
            status_code=status.HTTP_200_OK)
def local_access_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.local_access()
    return response

@router.get("/socioechonomics/not-eating",
            status_code=status.HTTP_200_OK)
def beneficiaries_not_eating_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.beneficiaries_not_eating()
    return response

@router.get("/restaurants/queue-time",
            status_code=status.HTTP_200_OK)
def time_on_queue_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.time_on_queue()
    return response

@router.get("/restaurants/menu",
            status_code=status.HTTP_200_OK)
def get_restaurant_menu_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.restaurant_menu_stats()
    return response

@router.get("/restaurants/infrastructure",
            status_code=status.HTTP_200_OK)
def get_restaurant_infrastructure_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.restaurant_infrastructure_stats()
    return response

#

@router.get("/program/review",
            status_code=status.HTTP_200_OK)
def get_program_review_stats(service: Annotated[MainService, Depends(get_kpi_service)]):
    response = service.program_review_stats()
    return response