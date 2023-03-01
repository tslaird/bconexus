from typing import List
from django.db import models

class usability_domain(models.Model):
    values = models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='usability_domain'





    
