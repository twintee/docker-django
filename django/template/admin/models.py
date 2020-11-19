from django.db import models
from .model_base import Base

class User(Base):
    name = models.CharField(max_length=128)
    mail = models.EmailField()
