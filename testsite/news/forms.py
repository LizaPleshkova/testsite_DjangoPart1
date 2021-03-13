from django import forms
from .models import Category, News  # для списка категории при созданиии новости
import re
from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    '''
    форма для отправки email
    '''
    subject = forms.CharField(label='Тема',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': None}))
    content = forms.CharField(label='Текст',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'autofocus': None, 'rows':5}))
    captcha_field= CaptchaField()

class UserLoginForm(AuthenticationForm):
    '''
    расширяет класс AuthenticationForm
    class Meta дзесь не нужен
    '''
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': None}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    '''
    пользовательская форма регистрации
    '''
    #переопределяем поля
    username= forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': None}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User#модлеь с которой связанна форма
        fields = ('username', 'email', 'password1', 'password2')# в каком порядке должны быть представленны поля
        # widgets = {# корректно раотает только поле username
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        #
        # }

# для работы с формами несвязаннх с мооделями
# class NewsForms(forms.Form):
#     title = forms.CharField(max_length=150, label='Название', widget= forms.TextInput(attrs={"class":"form-control"}))
#     content = forms.CharField(label='Текст', required=False, widget= forms.Textarea(
#         attrs={
#             "class":"form-control",
#             "rows": 5
#         }))
#     is_published = forms.BooleanField(label='Опубликованно', initial=True)
#     category = forms.ModelChoiceField(empty_label='Выберите категорию', queryset=Category.objects.all(), label='Ктегория', widget= forms.Select(attrs={"class":"form-control"}))#queryset - из какой модели получаем данные

class NewsForms(forms.ModelForm):
    class Meta:
        ''' описываем как должна выглфдеть наша форма'''
        model = News
        #fields = '__all__'# представленны все поля из модели
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={"class":"form-control","rows": 5}),
            'category': forms.Select(attrs={"class":"form-control"})#queryset - из какой модели получаем данные
        }

    def clean_title(self):
        ''' кастомный валидатор для поля title '''
        title = self.cleaned_data['title']# очищенные данные из словаря cleaned_daata
        if re.match(r'\d', title): # ищет цифру в полу title
            raise ValidationError('Название не должно начинаться с цифры')
        return title