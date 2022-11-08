from .models import Card, CardList
from .views import generic_crud, crud_overview

urlpatterns = [
    *generic_crud(Card),
    *generic_crud(CardList),
]

crud_overview(urlpatterns)
