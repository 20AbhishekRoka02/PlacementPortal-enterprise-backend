from django.db import models

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='student_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    course = models.ForeignKey('course.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    batch = models.ForeignKey('course.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')


    def __str__(self):
        return self.user.email
