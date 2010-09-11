from extracontent.models import ExtraContent
from extracontent.forms import ExtraContentForm
from django.db import models

class ExtraData1(models.Model):
    description = models.TextField()

    
class ExtraData2(models.Model):
    dt = models.DateField()
    
    
class MainModel(ExtraContent):
    name = models.CharField(max_length = 60)
    
    
class MainModelForm(ExtraContentForm):
    
    class Meta:
        model = MainModel 