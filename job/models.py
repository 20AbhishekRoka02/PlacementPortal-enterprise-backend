from django.db import models

# Create your models here.
class Job(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    skill = models.ManyToManyField('Skill', related_name='jobs', blank=True)
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Skill(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Application(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.email} applied for {self.job.title}"