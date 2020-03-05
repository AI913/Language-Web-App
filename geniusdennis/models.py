import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Spanish(models.Model):
    word_esp = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date added')
    # timeswrong = models.IntegerField(default=0)

    def __str__(self):
        return self.word_esp
    def freshvocab(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=1) <= self.pub_date <= now
    freshvocab.admin_order_field = 'pub_date'
    freshvocab.boolean = True
    freshvocab.short_description = 'Added recently?'


class English(models.Model):
	spanish = models.ForeignKey(Spanish, on_delete=models.CASCADE)
	word_eng = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.word_eng