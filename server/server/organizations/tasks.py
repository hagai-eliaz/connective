from .models import Activity

from config import celery_app

@celery_app.task()
def update_activities_distances(activity: Activity):
    return activity.add_activity_to_schools()
