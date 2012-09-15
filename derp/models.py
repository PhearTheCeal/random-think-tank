from django.db import models

# Models. These are basically tables in the db

class Player(models.Model):

	idea = models.CharField(max_length=140)
	rating = models.IntegerField()

class User(models.Model):

	last_post = models.IntegerField()
	ip = models.CharField(max_length=100, primary_key=True)