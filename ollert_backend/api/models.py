from django.contrib.auth.models import User, Group
from django.db.models import Model, OneToOneField, SET_NULL, ManyToManyField, ForeignKey, SmallIntegerField, CASCADE, \
    CharField, FloatField, DateField, Manager, QuerySet
from ordered_model.models import OrderedModel, OrderedModelManager


# Create your models here.
class CardList(OrderedModel):
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class CardManager(OrderedModelManager):
    """ Selects related CardList by default, so we can display their names. """

    def get_queryset(self) -> QuerySet['Card']:
        return super(CardManager, self).select_related('cardlist')


class Card(OrderedModel):
    name = CharField(max_length=128)
    cardlist = ForeignKey(CardList, on_delete=CASCADE, related_name='cards')
    #users = ManyToManyField(User)
    groups = ManyToManyField(Group, null=True, blank=True)

    # objects = CardManager

    order_with_respect_to = 'cardlist'

    def __str__(self):
        return f"{self.name} [{self.cardlist.name}]"
