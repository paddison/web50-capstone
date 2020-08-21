from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class User(AbstractUser):
    pass

class Card(models.Model):
    english = models.CharField(max_length=45)
    character = models.CharField(max_length=45)
    pinyin = models.CharField(max_length=45)
    comment = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    due = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='cards')

    def __str__(self):
        return f'{self.english} - {self.character}' 

class Deck(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='decks')
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        
        # add a constraint so that each user can only have one all cards deck
        constraints = [
            models.UniqueConstraint(fields=['created_by'], condition=models.Q(name='All Cards'), name='user_all_cards')
        ]

    def __str__(self):
        return f'{self.created_by}\'s {self.name} Deck'

class CardsOnDeck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='decks')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')

    class Meta:

        # make it so a card can only be on a deck once
        constraints = [
            models.UniqueConstraint(fields=['card', 'deck'], name='unique_cards_on_deck')
        ]

    def __str__(self):
        return f'{self.card} in {self.deck.name}'
