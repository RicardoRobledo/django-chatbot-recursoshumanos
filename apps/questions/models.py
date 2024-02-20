from django.db import models

# Create your models here.
class Procedure(models.Model):

    title = models.CharField(max_length=150)


class ProcedureURL(models.Model):

    description = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    procedure_id = models.ForeignKey("Procedure", on_delete=models.CASCADE)
