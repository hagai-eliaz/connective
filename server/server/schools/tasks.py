from .models import School
from .management.commands.update_activity_distances import Command

from config import celery_app

@celery_app.task()
def update_activities_distances(school: School):
    return Command.update_school_with_activity(school)
