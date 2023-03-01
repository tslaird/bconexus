from typing import List
from django.db import models
from app.models import *
from app.models.description_domain import description_domain
from app.models.execution_domain import execution_domain
from app.models.io_domain import io_domain
from app.models.parametric_domain import parametric_domain
from app.models.provenance_domain import provenance_domain
from app.models.usability_domain import usability_domain

class object2791(models.Model):
    object_id = models.CharField(max_length=500)
    spec_version = models.CharField(max_length=500)
    etag=models.CharField(max_length=500)
    provenance_domain=models.OneToOneField(provenance_domain)
    usability_domain=models.OneToOneField(usability_domain)
    description_domain=models.OneToOneField(description_domain)
    execution_domain=models.OneToOneField(execution_domain)
    parametric_domain=models.OneToOneField(parametric_domain)
    io_domain=models.OneToOneField(io_domain)
    #add error domain and extension domain.

    class Meta:
        manage = False
        db_table='2791object'





    
