from django import template
from news.models import Category
from django.db.models import *
from django.core.cache import cache

register = template.Library()

@register.simple_tag(name= 'get_list_categories')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1 = 'Hello', arg2 = ' Word'):
    '''
    пытаемся получить категории из кэша
    '''

    categories = Category.objects.annotate(count=Count('news', filter=F('news__is_published'))).filter(
        count__gt=0)  # кол-во новостей в категории большше 0

    # для кэша. первый вариант
    # categories = cache.get('categories')
    # if not categories: #если не достали ничего из кэща\ ниже их получаем их из БД и должны их закэщировать
    #     #categories = Category.objects.annotate(count=Count('news')).filter(count__gt=0)# кол-во новостей в категории большше 0
    #     categories = Category.objects.annotate(count=Count('news', filter=F('news__is_published'))).filter(count__gt=0)# кол-во новостей в категории большше 0
    #     cache.set('categories', categories, 30)
        # второй вариант
        # cache.get_or_set('categories', Category.objects.annotate(count=Count('news', filter=F('news__is_published'))).filter(count__gt=0), 30)
    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}