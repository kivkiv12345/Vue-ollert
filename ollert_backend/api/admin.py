from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.options import InlineModelAdmin

from .models import Card, CardList


class CardInlines(TabularInline):
    model = Card
    extra = 0


class CardListAdmin(ModelAdmin):
    inlines = [CardInlines]


# Register your models here.
admin.site.register(CardList, CardListAdmin)
admin.site.register(Card)

