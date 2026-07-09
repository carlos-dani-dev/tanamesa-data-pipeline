from ..repos.main_repo import MainRepo


class MainService():
    def __init__(self, db):
        self.repo = MainRepo(db)
    
    def time_survey_administration(self):
        return self.repo.time_survey_administration()
    
    def submissions_by_city(self):
        return self.repo.submissions_by_city()
    
    def beneficiaries_socioechonomics_stats(self):
        return self.repo.beneficiaries_socioechonomics_stats()