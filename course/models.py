from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    semester = models.IntegerField()
    years = models.IntegerField()
    
    def __str__(self):
        return self.name


class Batch(models.Model):
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    batch_name = models.CharField(max_length=10, blank=True, editable=False)  # Auto-populated field
    
    
    def __str__(self):
        return self.batch_name
    
    def save(self, *args, **kwargs):
        if not self.batch_name:
            self.batch_name = f"{self.start_year}-{self.end_year}"
        super().save(*args, **kwargs)