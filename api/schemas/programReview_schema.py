from pydantic import BaseModel


MetricAnswerBreakdown = dict[str, int]

class ProgramReviewStats(BaseModel):
    food_quantity_review: MetricAnswerBreakdown
    protein_quantity_review: MetricAnswerBreakdown
    food_flavor_review: MetricAnswerBreakdown
    program_satisfaction_review: MetricAnswerBreakdown
    program_continuity: MetricAnswerBreakdown