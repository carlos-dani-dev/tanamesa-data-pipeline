from sqlalchemy import text
from sqlalchemy.orm import Session

from ..schemas.application_schema import (TimeSurveyApplicationResponse,
                                          SubmissionsByDay, SubmissionsByWeek,
                                           SubmissionsByCity, SubmissionsByCityResponse)

from ..schemas.socioechonomics_schema import (BeneficiariesSocioeconomicsStats, ConsistencyOfAccessRow,
                                              ConsistencyOfAccessResponse, ProgramDependencyRow, ProgramDependencyResponse,
                                              EntireServedFamilyConfiguration, AssistedFamiliesResponse, DifficultyOfAccessByRegion,
                                              LocalAccessResponse, BeneficiariesNotEatingStats, ResidenceProgramServing)

from ..schemas.restaurants_schema import (TimeOnQueueRow, TimeOnQueueResponse, RestaurantMenuStats, RestaurantInfrastructureStats)

from ..schemas.programReview_schema import (ProgramReviewStats)


class MainRepo:

    def __init__(self, db: Session):
        self.db = db


    def time_survey_application(self):
        summary = self.db.execute(text("""
            SELECT days_until_now, weeks_until_now
            FROM kpi_time_survey_administration_summary
        """)).mappings().one()

        submissions_by_day = self.db.execute(text("""
            SELECT day_offset, submissions
            FROM kpi_submissions_by_day
        """)).mappings().all()

        submissions_by_week = self.db.execute(text("""
            SELECT week_offset, submissions
            FROM kpi_submissions_by_week
        """)).mappings().all()

        return TimeSurveyApplicationResponse(
            days_until_now=summary["days_until_now"],
            weeks_until_now=summary["weeks_until_now"],
            submissions_by_day=[SubmissionsByDay(**row) for row in submissions_by_day],
            submissions_by_week=[SubmissionsByWeek(**row) for row in submissions_by_week],
        )

    def submissions_by_city(self):
        submissions_by_city = self.db.execute(text("""
            SELECT city, submissions
            FROM kpi_submissions_by_city
        """)).mappings().all()
        
        return SubmissionsByCityResponse(
            submissions_by_city=[SubmissionsByCity(**row) for row in submissions_by_city]
        )
        
    
    def beneficiaries_socioechonomics_stats(self) -> BeneficiariesSocioeconomicsStats:
        stats = self.db.execute(text("""
            SELECT
                beneficiaries_on_vag, beneficiaries_on_cadunico, beneficiaries_on_cadunico_on_vag
            FROM kpi_beneficiaries_socioechonomics_stats
        """)).mappings().one()

        return BeneficiariesSocioeconomicsStats(**stats)

    def consistency_of_access(self) -> ConsistencyOfAccessResponse:
        rows = self.db.execute(text("""
            SELECT
                is_vag, freq_access, total
            FROM kpi_consistency_of_access
        """)).mappings().all()

        return ConsistencyOfAccessResponse(
            consistency_of_access=[ConsistencyOfAccessRow(**row) for row in rows]
        )

    def program_dependency(self) -> ProgramDependencyResponse:
        rows = self.db.execute(text("""
            SELECT
                is_vag, is_dependent, total
            FROM kpi_program_dependency
        """)).mappings().all()

        return ProgramDependencyResponse(
            program_dependency=[ProgramDependencyRow(**row) for row in rows]
        )

    def assisted_families(self) -> AssistedFamiliesResponse:
        residence_serving = self.db.execute(
            text("SELECT serving_status, total FROM kpi_residence_program_serving")
        ).mappings().all()

        family_config = self.db.execute(
            text("SELECT family_size, total FROM kpi_entire_served_family_configuration")
        ).mappings().all()

        return AssistedFamiliesResponse(
            residence_program_serving=[ResidenceProgramServing(**row) for row in residence_serving],
            entire_served_family_configuration=[EntireServedFamilyConfiguration(**row) for row in family_config],
        )

    def local_access(self) -> LocalAccessResponse:
        rows = self.db.execute(
            text("SELECT region, difficulty_type, total FROM kpi_difficulty_of_access_by_region")
        ).mappings().all()

        return LocalAccessResponse(
            difficulty_of_access_by_region=[DifficultyOfAccessByRegion(**row) for row in rows]
        )

    def beneficiaries_not_eating(self) -> BeneficiariesNotEatingStats:
        stats = self.db.execute(
            text("""
                SELECT
                    await_and_eat,
                    await_and_not_eat,
                    await_and_not_eat_on_vag
                FROM kpi_beneficiaries_not_eating_stats
            """)
        ).mappings().one()

        return BeneficiariesNotEatingStats(**stats)


    def time_on_queue(self) -> TimeOnQueueResponse:
        queue_stats = self.db.execute(
            text("SELECT queue_time, total FROM kpi_time_on_queue_stats")
        ).mappings().all()

        average_time = self.db.execute(
            text("SELECT average_queue_time_minutes FROM kpi_average_time_on_queue")
        ).scalar()

        return TimeOnQueueResponse(
            time_on_queue=[TimeOnQueueRow(**row) for row in queue_stats],
            average_time_on_queue=average_time or 0,
        )

    def restaurant_menu_stats(self) -> RestaurantMenuStats:
        rows = self.db.execute(
            text("SELECT metric, answer, total FROM kpi_restaurant_menu_summary")
        ).mappings().all()

        result: dict[str, dict[str, int]] = {
            "menu_change_suggestions": {},
            "daily_menu_realization": {},
            "menu_variety": {},
            "menu_satisfaction": {},
            "action_when_beneficiary_dislikes_food": {},
        }
        for row in rows:
            metric = row["metric"]
            if metric in result:
                result[metric][row["answer"]] = row["total"]

        return RestaurantMenuStats(**result)

    def restaurant_infrastructure_stats(self) -> RestaurantInfrastructureStats:
        rows = self.db.execute(
            text("SELECT metric, answer, total FROM kpi_restaurant_infrastructure_summary")
        ).mappings().all()

        result: dict[str, dict[str, int]] = {
            "beneficiary_knows_maximum_daily_food_served": {},
            "payment_and_serving_separation": {},
            "restaurant_program_signposted": {},
            "restaurant_cleaning": {},
            "cold_food": {},
            "package_integrity": {},
            "food_integrity": {},
            "difficulty_on_waiting": {},
        }
        for row in rows:
            metric = row["metric"]
            if metric in result:
                result[metric][row["answer"]] = row["total"]

        return RestaurantInfrastructureStats(**result)
    
    def program_review_stats(self) -> ProgramReviewStats:
        rows = self.db.execute(
            text("SELECT metric, answer, total FROM kpi_program_evaluation_summary")
        ).mappings().all()

        result: dict[str, dict[str, int]] = {
            "food_quantity_review": {},
            "protein_quantity_review": {},
            "food_flavor_review": {},
            "program_satisfaction_review": {},
            "program_continuity": {},
        }
        for row in rows:
            metric = row["metric"]
            if metric in result:
                result[metric][row["answer"]] = row["total"]

        return ProgramReviewStats(**result)