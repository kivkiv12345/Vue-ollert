from django.urls import path

from .models import Card, CardList
from .views import generic_crud, crud_overview, card_move, CrudOps

urlpatterns = [
    *generic_crud(Card),
    *generic_crud(CardList),
    path(f"card-move/", card_move, name="card-move"),
]

crud_overview(urlpatterns)
