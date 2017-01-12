from django.db import models

from ..accounts.models import Account


class Moment(models.Model):
	# Basic
	content = models.CharField(max_length=200)
	images = models.TextField(default='[]')
	creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='moments', null=True, blank=True)
	flagged = models.IntegerField(default=False)
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)