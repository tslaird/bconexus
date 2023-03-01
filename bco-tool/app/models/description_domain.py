from typing import List
from django.db import models

class keyword(models.Model):
    value = models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='keyword'

class platform(models.Model):
    value = models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='platform'

class uri(models.Model):
    filename=models.CharField(max_length=255)
    uri = models.CharField(max_length=500)
    access_time=models.DateTimeField()
    sha1_checksum=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='uri'

class pipeline_step_prerequisite(models.Model):
    name=models.CharField(max_length=255)
    uri = models.OneToOneField(uri,verbose_name="uri")

    class Meta:
        manage = False
        db_table='pipeline_step_prerequisite'

class pipeline_step(models.Model):
    step_number = models.IntegerField()
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    version=models.CharField(max_length=50)
    prerequisite=models.ManyToManyField(pipeline_step_prerequisite,verbose_name="prerequisite")

    class Meta:
        manage = False
        db_table='pipeline_step'

class ids(models.Model):
    value=models.CharField(max_length=255)

    class Meta:
        manage = False
        db_table='ids'

class xref(models.Model):
    namespace=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    ids=models.ManyToManyField(ids,verbose_name="ids")
    access_time=models.DateTimeField()

    class Meta:
        manage = False
        db_table='xref'

class description_domain(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    keywords = models.ManyToManyField(keyword, verbose_name="keywords")
    xref = models.ManyToManyField(xref, verbose_name="xref")
    platform = models.ManyToManyField(platform, verbose_name="platform")
    pipeline_steps = models.ManyToManyField(pipeline_step, verbose_name="piepline_steps")
    input_list=models.ManyToManyField(uri,verbose_name="input_list")
    output_list = models.ManyToManyField(uri, verbose_name="output_list")

    class Meta:
        manage = False
        db_table='description_domain'




    
