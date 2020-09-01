from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add', views.add, name='add'),
    path('decks', views.decks, name='decks'),
    path('decks/get_cards/<int:deck_id>', views.get_cards, name='get-cards'),
    path('decks/get_cards', views.get_cards, name='get_all_cards'),
    path('decks/add/<int:deck_id>', views.add_to_deck, name='add_to_deck')
]