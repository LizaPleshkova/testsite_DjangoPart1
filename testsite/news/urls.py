from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('register/', register, name='register'),# Registration\Authorization
    path('login/', user_login, name='login'),  # Registration\Authorization
    path('logout/', user_logout, name='logout'),  # Registration\Authorizatio
    path('contact/', contact, name='contact'),#for Paginator
    #path('', index, name='home'),# контроллеры функций
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),#контроллеры класса + кэширование главной страницы
    path('', HomeNews.as_view(), name='home'),#контроллеры класса
    #path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title': 'Какой-то тайтл'}), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),#'news/<int:news_id>/'
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news')
    ]