from django.contrib import admin
from job.models import Job, Skill, Application
# Register your models here.
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(Application)
