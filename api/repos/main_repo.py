from sqlalchemy import text
from sqlalchemy.orm import Session


class MainRepo:
    def __init__(self, db: Session):
        self.db = db

    def time_survey_administration(self):
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

        return {
            "days_until_now": summary["days_until_now"],
            "weeks_until_now": summary["weeks_until_now"],
            "submissions_by_day": submissions_by_day,
            "submissions_by_week": submissions_by_week,
        }
