from django.contrib.auth.models import User, Group
from django.db.models import Model, OneToOneField, SET_NULL, ManyToManyField, ForeignKey, SmallIntegerField, CASCADE, \
    CharField, FloatField, DateField, Manager, QuerySet, TextField, F, Max
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
            self.initial_order = self.order
        except Exception:
            self.initial_cardlist = None
            self.initial_order = None

    def save(self, *args, **kwargs):
        """ Ensure no order fields overlap on the current cardlist """

        max_order = Card.objects.filter(cardlist=self.cardlist).aggregate(Max('order'))['order__max']
        if max_order is None:  # No cards on the current CardList
            self.order = 0
        if self.order != 0 and (self.order is None or self.order > max_order):
            self.order = max_order+1

        # TODO Kevin: Ew this:
        if self.cardlist == self.initial_cardlist and self.order >= self.initial_order:
            self.order -= 1

        super().save(*args, **kwargs)

        if self.cardlist != self.initial_cardlist:  # Moving to another cardlist
            # Fix current cardlist
            Card.objects.filter(cardlist=self.cardlist, order__gte=self.order).exclude(pk=self.pk).update(order=F('order')+1)
            # Fix old cardlist
            if self.initial_cardlist:# and self.initial_cardlist != self.cardlist:
                Card.objects.filter(cardlist=self.initial_cardlist, order__gte=self.initial_order).exclude(pk=self.pk).update(order=F('order')-1)
        else:  # Moving on the same cardlist
            if self.order >= self.initial_order:  # Moving up
                Card.objects.filter(cardlist=self.cardlist, order__lte=self.order, order__gte=self.initial_order).exclude(pk=self.pk).update(order=F('order')-1)
            else:  # Moving down
                Card.objects.filter(cardlist=self.cardlist, order__gte=self.order, order__lte=self.initial_order).exclude(pk=self.pk).update(order=F('order')+1)

        self.initial_cardlist = self.cardlist
        self.initial_order = self.order

    def __str__(self):
        return f"{self.name} [{self.cardlist.name}]"
