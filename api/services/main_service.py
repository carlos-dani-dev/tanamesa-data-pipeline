from api.repos.main_repo import MainRepo


class MainService():
    def __init__(self, db):
        self.repo = MainRepo(db)
    
    def time_survey_application(self):
        return self.repo.time_survey_application()
    
    def submissions_by_city(self):
        return self.repo.submissions_by_city()
    
    def beneficiaries_socioechonomics_stats(self):
        return self.repo.beneficiaries_socioechonomics_stats()
    
    def consistency_of_access(self):
        return self.repo.consistency_of_access()
    
    def program_dependency(self):
        return self.repo.program_dependency()
    
    def assisted_families(self):
        return self.repo.assisted_families()
    
    def local_access(self):
        return self.repo.local_access()
    
    def beneficiaries_not_eating(self):
        return self.repo.beneficiaries_not_eating()
    
    def time_on_queue(self):
        return self.repo.time_on_queue()
    
    def restaurant_menu_stats(self):
        return self.repo.restaurant_menu_stats()

    def restaurant_infrastructure_stats(self):
        return self.repo.restaurant_infrastructure_stats()

    def program_review_stats(self):
        return self.repo.program_review_stats()