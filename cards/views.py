import re

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Card, Deck, CardsOnDeck

# Create your views here.
def index(request):
    try:
        cards = Card.objects.filter(decks__deck__name='All Cards', decks__deck__created_by=request.user)
    except:
        cards = []
    return render(request, 'cards/index.html', {
        'cards': cards
    })

def add(request):
    if request.method == 'POST':

        print(request.POST)
        english = request.POST['english']
        character = request.POST['character']
        pinyin = request.POST['pinyin']
        comment = request.POST['comment']

        # Check if submitted character is an actual chinese character by using their unicode
        foundChars = re.findall(u'[\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]', character)
        if len(foundChars) is not len(character):
            print('tried to submit non Chinese character')
            return render(request, 'cards/add.html', {
                'error': 'Only Chinese characters are allowed in character field',
                'form': {
                    'english': english,
                    'character': character,
                    'pinyin': pinyin,
                    'comment': comment
                }
            })

        # create a new card
        card = Card(english=english, character=character, pinyin=pinyin, comment=comment, created_by=request.user)

        # if this is this users first card, create a new 'all cards' deck for him
        if not Deck.objects.filter(created_by=request.user, name='All Cards').exists():
            Deck(created_by=request.user, name='All Cards', description='All your cards').save()
        
        allCards = Deck.objects.get(created_by=request.user, name='All Cards')

        try:
            card.save()
            CardsOnDeck(card=card, deck=allCards).save()
            if 'add_another' in request.POST:
                return render(request, 'cards/add.html', {
                    'success': f'Card: {card} added succesfully'
                })
            else:
                return HttpResponseRedirect(reverse('index'))


        except IntegrityError:
            return render(request, 'cards/add.html', {
                'error': 'Some error occured (tried to add the same card twice?',
                'form': {
                    'english': english,
                    'character': character,
                    'pinyin': pinyin,
                    'comment': comment
                }
            })

    return render(request, 'cards/add.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'cards/login.html', {
                'error': 'Wrong Username and/or Password'
            })
    return render(request, 'cards/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmation = request.POST['password-repeat']
        email = request.POST['email']
        
        # See if passwords match
        if confirmation != password:
            return render(request, 'cards/register.html', {
                'error': 'Passwords must match'
            })
        
        # Try to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'cards/register.html', {
                'error': 'Username already taken'
            })
            
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'cards/register.html')