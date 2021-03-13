from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForms, UserRegisterForm,UserLoginForm, ContactForm
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.core.mail import send_mail


# Registration\Authorization
def register(request):
    if request.method == 'POST':  # метод запроса пост(отправляем данные из формы), принимаем даннные и сохраняем их
        form = UserRegisterForm(request.POST)
        #form = UserCreationForm(request.POST)  # забираем данные из POSTформы#создаем экземпляр UserCreationForm:
        if form.is_valid():  # прошла ли форма валидна
            user = form.save()
            login(request, user)# для авторизации
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')  # перенаправлет на именованный урл\т.е. на страницу авторизации
        else:
            messages.error(request, 'Ошибка регистрации')
    else:  # если запрос гет =просто опказывваем форму
        form = UserRegisterForm()
        #form = UserCreationForm()  # создаем экземпляр UserCreationForm\это будет несвязанная форма
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# контроллер функция для Paginator
def contact(request):
    '''
    методы get_page() and page() =
    но если работаем с пустым списком get_page() не будет выдавать исключения
    :param request:
    :return:
    '''
    if request.method == 'POST':  # метод запроса пост(отправляем данные из формы), принимаем даннные и сохраняем их
        form = ContactForm(request.POST)
        # form = UserCreationForm(request.POST)  # забираем данные из POSTформы#создаем экземпляр UserCreationForm:
        if form.is_valid():  # прошла ли форма валидна
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'liz.pleshkova@yandex.by', ['pl.1.el.vas@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмл отправлено!')
                return redirect('contact')  # перенаправлет на именованный урл\т.е. на страницу авторизации
            else:
                messages.error(request, 'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:  # если запрос гет =просто опказывваем форму
        form = ContactForm()
        # form = UserCreationForm()  # создаем экземпляр UserCreationForm\это будет несвязанная форма
    return render(request, 'news/test.html', {"form": form})
    # objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']
    # paginator = Paginator(objects, 2)  # вторым арг. - количество записей для одной стр
    # page_num = request.GET.get('page', 1)  # получаем номер страницы
    # page_objects = paginator.get_page(page_num)
    # return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):
    ''' атрибуты, которые мы должны переопределить'''
    model = News  # будут полученны все данные из этой модели
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'  # вместо object_list
    # extra_context = {'title':'Главная'}# желательно использовать только для каких-то статичных данных\для динамичных данных не рекомендуется
    mixin_prob = 'hello word'
    paginate_by = 2  # for Paginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # вернет нам родительский метод\ сохраняем в переременную все то, что было там до этого
        context['title'] = self.get_upper('Главаная страница')  # дополняем нашими данными
        context['mixin_prob'] = self.get_prob()
        return context

    def get_queryset(self):
        '''
        переопределяем метод, для изменения вывода новоостей
        выводим только ности опубликованные
        .select_related('category') - загружает связанные данные сразу\для работыы со связь ForeignKey
        '''
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    '''
    фактически автоматически помогт получть некий набор данных, список дданных
    нужно переопределить атрибуты классаб
    переопределить get-context_data - для того чтобы передать некоторый набор данны:
        к существующему контексту добавляем новый контекст
    переопределить get_queryset - подкорректировать запрос на получение данных
    '''
    model = Category
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'  # вместо object_list
    allow_empty = False  # неразрешаем показ пустых списков
    paginate_by = 2  # for Paginator

    def get_queryset(self):
        '''
        переsопределяем метод, для изменения вывода новоостей
        выводим только ности опубликованные
        '''
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # вернет нам родительский метод\ сохраняем в переременную все то, что было там до этого
        context['title'] = self.get_upper(
            Category.objects.get(pk=self.kwargs['category_id']))  # дополняем нашими данными
        return context


class ViewNews(DetailView):
    model = News
    # template_name = 'news/news_detail.html' # и так работает с ним по умолчанию
    # pk_url_kwarg = 'news_id' # for path('news/<int:news_id>/', view_news, name='view_news'),


class CreateNews(LoginRequiredMixin, CreateView):
    '''
    связываес класс с классом формы

    LoginRequiredMixin- ограничеваем доступ к неавторизованному польз (сейчас, только для админа):
        1.перенаправлять пользователя на форму авторизации
        2.выдавать ошибку 403 доступ запрещен(можем определить raise_exceptiion  в True)

    '''
    form_class = NewsForms
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')

    # for LoginRequiredMixin
    login_url = '/admin/'  # определить куда перенаправлять пользователя
    # redirect_field_name = ''#опр
    # raise_exception =


# вызывается в ответ на клиентский запрос\обрабатывает этот запрос\и возвращает ответ в виде представления?
# связующие звено между моделями  и представлениями\  данными и их отображением

#
def index(request):
    # print(request)
    # news = News.objects.all()
    # res = '<h1>List of news</h1>'
    # for new in news:
    #     res += f'<div>\n<p>{new.title}</p>\n<p>{new.content}</p>\n</div><hr>\n'
    # return HttpResponse(res)
    news = News.objects.all()
    # categories = Category.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
        # 'categories': categories,
    }
    return render(request, 'news/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    # categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


# для работы с формой не свфзанной с моделями

# def add_news(request):
#     if request. method == 'POST':# метод запроса пост(отправляем данные из формы), принимаем даннные и сохраняем их
#         form = NewsForms(request.POST)# забираем данные из формы
#         if form.is_valid():# прошла ли форма валидацию
#             print(form.cleaned_data)# если все ок, записываем в словарь cleaned-data
#             news = News.objects.create(**form.cleaned_data)# распаковка словарей в Python
#             # title = form.cleaned_data['title']
#             return redirect(news)# перенаправлет на созданную страницу
#     else:# если запрос гет =просто опказывваем форму
#         form = NewsForms()
#     return render(request, 'news/add_news.html', {'form': form})


# для работы с модель, связанной с моделью
def add_news(request):
    if request.method == 'POST':  # метод запроса пост(отправляем данные из формы), принимаем даннные и сохраняем их
        form = NewsForms(request.POST)  # забираем данные из формы
        if form.is_valid():  # прошла ли форма валидацию
            print(form.cleaned_data)  # если все ок, записываем в словарь cleaned-data
            news = form.save()
            return redirect(news)  # перенаправлет на созданную страницу
    else:  # если запрос гет =просто опказывваем форму
        form = NewsForms()
    return render(request, 'news/add_news.html', {'form': form})

# def test(request):
#     return HttpResponse('<h1>Test page!</h1>')
