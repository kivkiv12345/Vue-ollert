from django.contrib.auth.models import User, Group
from django.db.models import Model, OneToOneField, SET_NULL, ManyToManyField, ForeignKey, SmallIntegerField, CASCADE, \
    CharField, FloatField, DateField, Manager, QuerySet, TextField
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
    description = TextField(blank=True, null=True)
    cardlist = ForeignKey(CardList, on_delete=CASCADE, related_name='cards')
    #users = ManyToManyField(User)
    groups = ManyToManyField(Group, blank=True)

    # objects = CardManager

    order_with_respect_to = 'cardlist'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.initial_cardlist = self.cardlist
        except Exception:
            self.initial_cardlist = None

    def save(self, *args, **kwargs):
        """ Ensure no order fields overlap on the current cardlist """

        super().save(*args, **kwargs)

        for index, card in enumerate(Card.objects.filter(cardlist=self.cardlist)):
            card.order = index
            super(Card, card).save()

        for index, card in enumerate(Card.objects.filter(cardlist=self.initial_cardlist)):
            card.order = index
            super(Card, card).save()

        self.initial_cardlist = self.cardlist

    def __str__(self):
        return f"{self.name} [{self.cardlist.name}]"
