from typing import List
from django.db import models


class uri(models.Model):
    filename=models.CharField(max_length=255)
    uri = models.CharField(max_length=500)
    access_time=models.DateTimeField()
    sha1_checksum=models.CharField(max_length=500)

    class Meta:
        manage = False
        db_table='uri'


class contribution(models.Model):
    value=models.CharField(max_length=255)

class contributor(models.Model):
    name=models.CharField(max_length=500)
    affiliation=models.CharField(max_length=500)
    email=models.CharField(max_length=100)
    contribution=models.OneToOneField(contribution,verbose_name="contribution")
    orcid=models.CharField(max_length=255)


    class Meta:
        manage = False
        db_table='contributor'


class review(models.Model):
    reviewer=models.OneToOneField(contributor)
    reviewer_comment=models.OneToOneField(uri)
    status=models.CharField(max_length=500)
    date=models.DateTimeField()

    class Meta:
        manage = False
        db_table='review'

class embargo(models.Model):
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()

    class Meta:
        manage = False
        db_table='embargo'


class provenance_domain(models.Model):
    name = models.CharField(max_length=255)
    created=models.DateTimeField()
    modified=models.DateTimeField()
    version=models.CharField(max_length=50)
    license=models.CharField(max_length=500)
    review=models.ManyToManyField(review,verbose_name="review")
    contributors=models.ManyToManyField(contributor)
    obsolete_after=models.CharField(max_length=255)
    embargo=models.OneToOneField(embargo)
    derived_from=models.CharField(max_length=255)
    

    class Meta:
        manage = False
        db_table='provenance_domain'





    
