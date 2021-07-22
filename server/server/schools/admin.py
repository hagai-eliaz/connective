from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import School, SchoolMember


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    exclude = ["last_updated_by"]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class SchoolMemberTabularInline(admin.TabularInline):
    model = SchoolMember
    min_num = 1


admin.site.register(SchoolMember)
