from django.db import models

# Create your models here.
# models.py

from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_date = models.DateTimeField(auto_now_add=True)
    input_variables = models.CharField(max_length=500)
    prediction_result = models.IntegerField()
