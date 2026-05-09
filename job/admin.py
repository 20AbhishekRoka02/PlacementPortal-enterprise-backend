from django.contrib import admin
from job.models import Job, Skill, Application
from users.models import UserRole
# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company__name', 'salary', 'location', 'deadline', 'posted_at', 'updated_at')

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            print("request.user.role: ", request.user.role, UserRole.COMPANY)
            return request.user.role in [UserRole.ADMIN, UserRole.UNIVERSITY, UserRole.COMPANY]

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.role in [UserRole.ADMIN, UserRole.UNIVERSITY, UserRole.COMPANY]

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            return request.user.role in [UserRole.ADMIN, UserRole.UNIVERSITY, UserRole.COMPANY]

    def has_change_permission(self, request, obj = ...):
        if request.user.is_authenticated:
            return request.user.role in [UserRole.ADMIN, UserRole.UNIVERSITY, UserRole.COMPANY]

    def has_delete_permission(self, request, obj = ...):
        if request.user.is_authenticated:
            return request.user.role in [UserRole.ADMIN, UserRole.UNIVERSITY, UserRole.COMPANY]

    # FILTER DATA
    def get_queryset(self, request):
        if request.user.is_authenticated:

            qs = super().get_queryset(request)

            if request.user.role == UserRole.ADMIN:
                return qs

            if request.user.role == UserRole.UNIVERSITY:
                return qs

            if request.user.role == UserRole.COMPANY:
                return qs.filter(company=request.user.company_profile)

            return qs.none()

admin.site.register(Job, JobAdmin)
admin.site.register(Skill)
admin.site.register(Application)
