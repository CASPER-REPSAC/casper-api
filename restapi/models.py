from django.db import models

# Create your models here.

class Restapi(models.Model):
    #study Info
    studyCreated = models.DateTimeField(auto_now_add = True)
    studyMaster = models.CharField(max_length=16, blank=False, default='')
    studyName = models.CharField(max_length=200, blank=True, default='')
    studyCode = models.IntegerField(auto_created = True)
    studySubject = models.CharField(max_length=16, blank=True)
    studyFile = models.CharField(blank=False)
    studyPlan = models.IntegerField(max = 100, default=0)
    studyProgress = models.IntegerField(max = 100, blank=False, default = 0)
    studyStatus = models.CharField(max = 100, default=0)

    #study Infoo - api ordering
    studyUpdated = models.DateTimeField()

    #release_date = models.DateTimeField()
    #api_list = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ('studyUpdated','studyName')

