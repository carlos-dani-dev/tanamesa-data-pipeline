from pydantic import BaseModel


class TimeOnQueueRow(BaseModel):
    queue_time: str
    total: int

class TimeOnQueueResponse(BaseModel):
    time_on_queue: list[TimeOnQueueRow]
    average_time_on_queue: float

MetricAnswerBreakdown = dict[str, int]

class RestaurantMenuStats(BaseModel):
    menu_change_suggestions: MetricAnswerBreakdown
    daily_menu_realization: MetricAnswerBreakdown
    menu_variety: MetricAnswerBreakdown
    menu_satisfaction: MetricAnswerBreakdown
    action_when_beneficiary_dislikes_food: MetricAnswerBreakdown

class RestaurantInfrastructureStats(BaseModel):
    beneficiary_knows_maximum_daily_food_served: MetricAnswerBreakdown
    payment_and_serving_separation: MetricAnswerBreakdown
    restaurant_program_signposted: MetricAnswerBreakdown
    restaurant_cleaning: MetricAnswerBreakdown
    cold_food: MetricAnswerBreakdown
    package_integrity: MetricAnswerBreakdown
    food_integrity: MetricAnswerBreakdown
    difficulty_on_waiting: MetricAnswerBreakdown