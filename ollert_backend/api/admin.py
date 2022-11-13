from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.options import InlineModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from .models import Card, CardList


class CardAdmin(ModelAdmin):
    list_display = ['name', 'pk', 'order']


class CardInlines(OrderedTabularInline):
    model = Card
    fields = ('pk', 'name', 'order', 'move_up_down_links',)
    readonly_fields = ('pk', 'order', 'move_up_down_links',)
    ordering = ('order',)
    extra = 0
    show_change_link = True


class CardListAdmin(OrderedInlineModelAdminMixin, ModelAdmin):
    inlines = [CardInlines]
    list_display = ['name', 'pk', 'order']


# Register your models here.
admin.site.register(CardList, CardListAdmin)
admin.site.register(Card, CardAdmin)

