from django.db import models

class Base(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    invalid = models.BooleanField(default=False)
