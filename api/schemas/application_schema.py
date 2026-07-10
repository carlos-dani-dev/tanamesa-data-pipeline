from pydantic import BaseModel


class SubmissionsByDay(BaseModel):
    day_offset: int
    submissions: int

class SubmissionsByWeek(BaseModel):
    week_offset: int
    submissions: int

class TimeSurveyApplicationResponse(BaseModel):
    days_until_now: int
    weeks_until_now: int
    submissions_by_day: list[SubmissionsByDay]
    submissions_by_week: list[SubmissionsByWeek]

class SubmissionsByCity(BaseModel):
    city: str
    submissions: int

class SubmissionsByCityResponse(BaseModel):
    submissions_by_city: list[SubmissionsByCity]