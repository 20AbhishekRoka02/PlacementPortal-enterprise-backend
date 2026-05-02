from django.db import models
# Create your models here.
class ScreenName(models.TextChoices):
    DASHBOARD = 'dashboard', 'Dashboard'
    COMPANIES = 'companies', 'Companies'
    STUDENTS = 'students', 'Students'
    JOBS = 'jobs', 'Job Postings'
    COURSES = 'courses', 'Courses'
    BATCHES = 'batches', 'Batches'
    APPLICATIONS = 'applications', 'Applications'
    PROFILE = 'profile', 'Profile'


class SideNavItem(models.Model):
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100, choices=ScreenName.choices)

    def __str__(self):
        return self.name