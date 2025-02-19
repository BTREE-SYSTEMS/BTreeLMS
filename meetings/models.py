from django.db import models

class Meeting(models.Model):
    subject = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    join_url = models.URLField()
