from django.db import models

# Create your models here.

class Sport(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Sports"

    def __str__(self):
        return self.name


class Selection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    odds = models.FloatField()

    class Meta:
        verbose_name_plural = "Selections"

    def __str__(self):
        return self.name

class Market(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    selections = models.ManyToManyField(Selection,related_name="markets")

    class Meta:
        verbose_name_plural = "Markets"

    def __str__(self):
        return self.name + '-' + str(self.id)

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    markets = models.ManyToManyField(Market)

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return self.name
