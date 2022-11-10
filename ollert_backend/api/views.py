""" Generic creation of CRUD based web API views """
from enum import Enum
from itertools import chain
# TODO Kevin: This is copied from ProjectManager (https://github.com/kivkiv12345/ProjectManager), not really ideal.

from typing import Type, Iterable

from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor, ReverseOneToOneDescriptor, \
    ManyToManyDescriptor
from django.urls import path
from rest_framework import status
from django.db.models import Model, QuerySet
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import ModelSerializer

from .models import CardList, Card

_LIST_SUFFIX = '-list'
_DETAIL_SUFFIX = '-detail'
_CREATE_SUFFIX = '-create'
_UPDATE_SUFFIX = '-update'
_DELETE_SUFFIX = '-delete'


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'order']


class CardListSerializer(ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = CardList
        fields = ['id', 'name', 'cards', 'order']


def serialize_cardlists(instances: QuerySet[CardList] = None) -> dict:
    if instances is None:
        instances = CardList.objects.all()
    serializer = CardListSerializer(instances, many=True)
    return serializer.data


@api_view(['GET'])
def cardlist_list(request: Request):
    return Response(serialize_cardlists())


@api_view(['POST'])
# def card_move(request: Request, card_pk: int, list_pk: int, order_id: int):
def card_move(request: Request):
    error = None
    try:
        data = request.data
        card = Card.objects.get(pk=data['card_id'])
        card_list = CardList.objects.get(pk=data['list_id'])
        card.cardlist = card_list
        if 'row' in data:
            card.to(data['row'])
        else:
            card.bottom()
    except Exception as e:
        error = e

    # TODO Kevin: Pretty dumb to serialize the exception like this
    return Response(serialize_cardlists(), status=status.HTTP_200_OK, exception=error)


def generic_serializer(crud_model: Type[Model], depth_limit: int = 0) -> Type[ModelSerializer]:
    """
    Creates a Generic recursive ModelSerializer for the provided model

    :param crud_model: Model subclass for which a serializer should be created.
    :param depth_limit: Maximum relation depth, below which objects won't be nested.

    :returns: The new ModelSerializer class.
    """

    class GenericSerializer(ModelSerializer):

        class Meta:
            model = crud_model
            fields = '__all__'
            depth = depth_limit

    return GenericSerializer


class CrudOps(Enum):
    CREATE = 0
    LIST = 1
    DETAIL = 2
    UPDATE = 3
    DELETE = 4


def generic_crud(crud_model: Type[Model], exclude: set[CrudOps] = None) -> Iterable[path]:
    """
    Creates generic CRUD views for the specified model

    :param crud_model: Model to create web API CRUD operations for

    :returns: A tuple of path() instances to be inserted into your app's urlpatterns
    """

    # TODO Kevin: Subclass ModelSerializer to support saving nested
    GenericSerializer = generic_serializer(crud_model, 2)

    @api_view(['GET'])
    def generic_get_list(request: Request):
        instances = crud_model.objects.all()
        serializer = GenericSerializer(instances, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def generic_get_detail(request: Request, pk: int):
        instance = crud_model.objects.get(pk=pk)
        serializer = GenericSerializer(instance, many=False)
        return Response(serializer.data)

    @api_view(['POST'])
    def generic_create(request: Request):
        serializer = GenericSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    @api_view(['POST'])
    def generic_update(request: Request, pk: int):
        instance = crud_model.objects.get(pk)
        serializer = GenericSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    @api_view(['DELETE'])
    def generic_delete(request: Request, pk: int):
        crud_model.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    model_name = crud_model.__name__.lower()

    list_url = f"{model_name}{_LIST_SUFFIX}"
    detail_url = f"{model_name}{_DETAIL_SUFFIX}"
    create_url = f"{model_name}{_CREATE_SUFFIX}"
    update_url = f"{model_name}{_UPDATE_SUFFIX}"
    delete_url = f"{model_name}{_DELETE_SUFFIX}"

    operations: list[path] = []
    if exclude is None or CrudOps.LIST not in exclude:
        operations.append(path(f"{list_url}/", generic_get_list, name=list_url))
    if exclude is None or CrudOps.DETAIL not in exclude:
        operations.append(path(f"{detail_url}/<str:pk>/", generic_get_detail, name=detail_url))
    if exclude is None or CrudOps.CREATE not in exclude:
        operations.append(path(f"{create_url}/", generic_create, name=create_url))
    if exclude is None or CrudOps.UPDATE not in exclude:
        operations.append(path(f"{update_url}/<str:pk>/", generic_update, name=update_url))
    if exclude is None or CrudOps.DELETE not in exclude:
        operations.append(path(f"{delete_url}/<str:pk>/", generic_delete, name=delete_url))

    return operations


def crud_overview(urls: list[path]) -> None:
    """
    Generate a view listing web API CRUD operations.
    The new view will be appended to the provided list.

    :param urls: urlpatterns list to generate the view for.
    """

    overview_dict = {
        'LIST': [url.pattern._route for url in urls if url.name.endswith(_LIST_SUFFIX)],
        'DETAIL': [url.pattern._route for url in urls if url.name.endswith(_DETAIL_SUFFIX)],
        'CREATE': [url.pattern._route for url in urls if url.name.endswith(_CREATE_SUFFIX)],
        'UPDATE': [url.pattern._route for url in urls if url.name.endswith(_UPDATE_SUFFIX)],
        'DELETE': [url.pattern._route for url in urls if url.name.endswith(_DELETE_SUFFIX)],
    }
    # overview_dict['OTHER'] = [url.pattern._route for url in urls if url.pattern._route not in set(chain(overview_dict.values()))]

    url_name = 'crud_overview'

    @api_view(['GET'])
    def overview_get(request):
        """ Mutate the overview dictionary with absolute URLs """

        # Show absolute URLs for the web API
        full_url = request._request.path
        url_prefix = full_url[:full_url.index(url_name)]
        abs_url_dict = {key: [f"{url_prefix}{url}" for url in urls] for key, urls in overview_dict.items()}
        return Response(abs_url_dict)

    # TODO Kevin: Not sure how I want to mutate the urlpatterns
    urls.append(path(url_name, overview_get, name=url_name))
