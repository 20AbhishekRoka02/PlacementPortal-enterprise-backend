from django.contrib import admin
from job.models import Job, Skill, Application
from users.models import UserRole
from django.http import HttpResponse
import csv
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

    def get_exclude(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.role == UserRole.COMPANY:
                return ("company",)

        return ()

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

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            if request.user.role == UserRole.COMPANY:
                obj.company = request.user.company_profile

            super().save_model(request, obj, form, change)

class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "student_name",
        "student_email",
        "student_phone",
        "job_title",
        "applied_at",
    )

    readonly_fields = (
        "applied_at",

        # Student
        "student_name",
        "student_email",
        "student_phone",
        "student_course",
        "student_batch",

        # Resume
        "resume_social_media",
        "resume_education",
        "resume_experience",
        "resume_projects",
        "resume_misc",

        # Job
        "job_title",
        "job_company",
        "job_description",
    )

    actions = ["export_as_csv"]

    fieldsets = (
        (
            "Application Information",
            {
                "fields": (
                    "applied_at",
                )
            }
        ),

        (
            "Student Information",
            {
                "fields": (
                    "student_name",
                    "student_email",
                    "student_phone",
                    "student_course",
                    "student_batch",
                )
            }
        ),

        (
            "Resume Information",
            {
                "fields": (
                    "resume_social_media",
                    "resume_education",
                    "resume_experience",
                    "resume_projects",
                    "resume_misc",
                )
            }
        ),

        (
            "Job Information",
            {
                "fields": (
                    "job_title",
                    "job_company",
                    "job_description",
                )
            }
        ),
    )

    # =========================
    # PERMISSIONS
    # =========================

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            return request.user.role in [
                UserRole.ADMIN,
                UserRole.UNIVERSITY,
                UserRole.COMPANY
            ]

        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.role in [
                UserRole.ADMIN,
                UserRole.UNIVERSITY,
                UserRole.COMPANY
            ]

        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.role == UserRole.COMPANY:
                return False

    # =========================
    # FILTER DATA
    # =========================

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if not request.user.is_authenticated:
            return qs.none()

        if request.user.role == UserRole.ADMIN:
            return qs

        if request.user.role == UserRole.UNIVERSITY:
            return qs

        if request.user.role == UserRole.COMPANY:
            return qs.filter(
                job__company=request.user.company_profile
            )

        return qs.none()

    # =========================
    # LIST DISPLAY METHODS
    # =========================

    def student_name(self, obj):
        return obj.student.resume.name

    student_name.short_description = "Student Name"

    def student_email(self, obj):
        return obj.student.resume.email

    student_email.short_description = "Email"

    def student_phone(self, obj):
        return obj.student.resume.phone

    student_phone.short_description = "Phone"

    def job_title(self, obj):
        return obj.job.title

    job_title.short_description = "Job Title"

    # =========================
    # DETAIL VIEW METHODS
    # =========================

    def student_course(self, obj):
        return obj.student.course

    def student_batch(self, obj):
        return obj.student.batch

    def resume_social_media(self, obj):
        return obj.student.resume.social_media

    def resume_education(self, obj):
        return obj.student.resume.education

    def resume_experience(self, obj):
        return obj.student.resume.experience

    def resume_projects(self, obj):
        return obj.student.resume.projects

    def resume_misc(self, obj):

        resume = obj.student.resume

        return f"""
Title:
{resume.misc_title}

Description:
{resume.misc_description}
"""

    def job_company(self, obj):
        return obj.job.company

    def job_description(self, obj):
        return obj.job.description

    # =========================
    # EXPORT CSV
    # =========================

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = (
            'attachment; filename=applications.csv'
        )

        writer = csv.writer(response)

        writer.writerow([
            "Student Name",
            "Email",
            "Phone",
            "Course",
            "Batch",

            "Job Title",
            "Company",
            "Applied At",

            "Social Media",
            "Education",
            "Experience",
            "Projects",

            "Misc Title",
            "Misc Description",
        ])

        for obj in queryset:

            resume = obj.student.resume

            writer.writerow([
                resume.name,
                resume.email,
                resume.phone,

                obj.student.course,
                obj.student.batch,

                obj.job.title,
                obj.job.company,

                obj.applied_at,

                resume.social_media,
                resume.education,
                resume.experience,
                resume.projects,

                resume.misc_title,
                resume.misc_description,
            ])

        return response

    export_as_csv.short_description = "Export selected applications as CSV"


admin.site.register(Job, JobAdmin)
admin.site.register(Skill)
admin.site.register(Application, ApplicationAdmin)
