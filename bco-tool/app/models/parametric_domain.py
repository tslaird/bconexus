from typing import List
from django.db import models


class parametric_domain(models.Model):
    param=models.CharField(max_length=255)
    value= models.CharField(max_length=500)    
    step=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='parametric_domain'





    
