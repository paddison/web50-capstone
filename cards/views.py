import re
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Card, Deck, CardsOnDeck

# Create your views here.
def index(request):
    try:
        cards = Card.objects.filter(user=request.user)
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
        card = Card(english=english, character=character, pinyin=pinyin, comment=comment, created_by=request.user, user=request.user)

        try:
            card.save()
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

def decks(request):
    userDecks = Deck.objects.filter(user=request.user)

    if request.method == "POST":
        deckName = request.POST['deck-name']
        if Deck.objects.filter(name=deckName, user=request.user).exists():
            return render(request, 'cards/decks.html', {
                'decks': userDecks,
                'error': 'Deck with the same name already exists'
            })
        else:
            description = request.POST['deck-description']
            deck = Deck(name=deckName, description=description, created_by=request.user, user=request.user)
            deck.save()
            userDecks = Deck.objects.filter(user=request.user)
            return render(request, 'cards/decks.html', {
                'decks': userDecks,
                'success': f'Deck { deck.name } created'
            })

    return render(request, 'cards/decks.html', {
        'decks': userDecks
    })

@login_required
@csrf_exempt
def add_to_deck(request, deck_id):
    deck = Deck.objects.get(pk=deck_id)
    if request.method == 'PUT':
        card_id = json.loads(request.body)['card']
        card = Card.objects.get(pk=card_id)
        addedCard = CardsOnDeck(card=card, deck=deck)
        addedCard.save()
        return JsonResponse({'message': 'Added'})

    cards = Card.objects.exclude(decks__deck__id=deck_id)



    return render(request, 'cards/add_to_deck.html', {
        'deck': deck,
        'cards': cards
    })

@login_required
def get_cards(request, deck_id=None):
    if deck_id:
        deck = Deck.objects.get(pk=deck_id).serialize()
        cards = Card.objects.filter(decks__deck__id=deck_id)
        deck['cards'] = [card.serialize() for card in cards]
        return JsonResponse(deck, safe=False)
    else:
        print('requested all cards')
        cards = Card.objects.filter(user=request.user)
        deck = {
            'name': 'All Cards',
            'description': 'All your cards',
            'cards': [card.serialize() for card in cards]
        }
        return JsonResponse(deck, safe=False)

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