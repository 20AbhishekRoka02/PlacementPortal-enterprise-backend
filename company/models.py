from django.db import models

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    hr_phone_number = models.CharField(max_length=20, blank=True)
    hr_email = models.EmailField(blank=True)