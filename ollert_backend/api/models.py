from django.contrib.auth.models import User, Group
from django.db.models import Model, OneToOneField, SET_NULL, ManyToManyField, ForeignKey, SmallIntegerField, CASCADE, \
    CharField, FloatField, DateField, Manager, QuerySet


# Create your models here.
class CardList(Model):
    name = CharField(max_length=128)


class CardManager(Manager):
    """ Selects related CardList by default, so we can display their names. """

    def get_queryset(self) -> QuerySet['Card']:
        return super(CardManager, self).select_related('cardlist')


class Card(Model):
    name = CharField(max_length=128)
    cardlist = ForeignKey(CardList, on_delete=CASCADE)
    #users = ManyToManyField(User)
    groups = ManyToManyField(Group)

    objects = CardManager

    def __str__(self):
        return f"{self.name} [{self.cardlist.name}]"
