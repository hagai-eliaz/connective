from .models import School


from config import celery_app

@celery_app.task()
def update_activities_distances(school: School):
    return True
