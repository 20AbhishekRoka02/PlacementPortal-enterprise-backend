from django.contrib import admin
from company.models import Company
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user__email', 'website', 'hr_phone_number','hr_email')
admin.site.register(Company, CompanyAdmin)
