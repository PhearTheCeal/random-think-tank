
from derp.models import Player
from derp.models import User
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from random import shuffle
from django import forms
from random import choice
from random import randint
import time

# Here is where all the main code takes place
# Functions are ran, pages are rendered, etc.

# FORMS: These are so you don't break my system

class IdeaForm(forms.Form):
	idea = forms.CharField(max_length=140)

class VoteForm(forms.Form):
	winner = forms.IntegerField()
	loser = forms.IntegerField()

# This renders the homepage
# It works by selecting a random idea
# and pitting it against an idea slightly better

def view_battle(request):
	try:
		objects = Player.objects.order_by('rating')
		objects = list(objects)
		x = randint(0, len(objects)-2)
		player1 = objects[x]
		player2 = objects[x+1]
	except IndexError:
		# This will probably only happen if no ideas have been added
		return render(request, "addidea.html", {"status":"Voting is broken :( Add an idea instead?", "color":"black"})

	return render(request, "battle.html", {"idea1":player1.idea, "idea2":player2.idea, "id1":player1.id, "id2":player2.id, "board":choice(["pol", "g"]), "users":randint(7,19)})

# Ah, the beauty of the Elo rating system. Let me break it down
# Request is verified, shit gets calculatd, shit gets saved to db
# if for some reason it doen't work I redirect to the leaderboard 
# for no reason in particular

def vote_battle(request):
	form = VoteForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			winnerID = form.cleaned_data['winner']
			loserID = form.cleaned_data['loser']

			winner = Player.objects.get(pk=winnerID)
			loser = Player.objects.get(pk=loserID)

			winnerChanceOfWinning = 1.0 / ( 10**(( loser.rating - winner.rating)/400) + 1 )
			loserChanceOfWinning = 1.0 / ( 10**(( winner.rating - loser.rating)/400) + 1 )
			K = 20

			# Winner's new rating
			a = winner.rating + (K * (1 - winnerChanceOfWinning))

			# Loser's new rating
			b = loser.rating + (K * (0 - loserChanceOfWinning))

			# Set players' scores
			winner.rating = int(a + 0.5)
			loser.rating = int(b + 0.5)

			winner.save()
			loser.save()

			return HttpResponseRedirect("/battle/")
		else:
			return HttpResponseRedirect("/leaderboard/")

# Self explanatory. 

def view_leaderboard(request):
	leaders = Player.objects.order_by('rating').reverse()

	return render_to_response("leaderboard.html", {"c":leaders})

def view_adder(request):
	return render(request, "addidea.html", {})

# This is for when people try to actually use their
# brains and add new idea. Basically right now the only
# thing stopping someone from submitting data is a 140 character
# limit and a 30 second cool-down time

def add_idea(request):
	form = IdeaForm(request.POST)
	if request.method == 'POST' and form.is_valid():
		form = IdeaForm(request.POST)
		if form.is_valid():
			all_entries = User.objects.all()
			print request.META['REMOTE_ADDR'], '"', form.cleaned_data['idea'], '"'
			for lol in all_entries:
				if lol.ip == request.META['REMOTE_ADDR'] and lol.last_post != None and time.time() - int(lol.last_post) <= 30:
					print "FLOOD DETECTED"
					return render(request, "addidea.html", {"status":"Flood Detected.", "color":"red"})
			new_idea = Player()
			new_idea.idea = form.cleaned_data['idea']

			new_idea.rating = 1800

			u = User()
			u.ip = request.META['REMOTE_ADDR']
			u.last_post = time.time()
			u.save()

			new_idea.save()
			return render(request, "addidea.html", {"status":"Successfully added!", "color":"green"})
	else:
		return render(request, "addidea.html", {"status":"Submission Failure.", "color":"red"})