from django.db import models
from django.urls import reverse

class News(models.Model):
    ''' вторичная модель '''
    title = models.CharField(max_length=50, verbose_name='Наименование') # обязательный аргумент
    content = models.TextField(blank = True, verbose_name='Контент') # blank = True -необязательный для заполнения
    created_at = models.DateTimeField(auto_now_add= True,verbose_name='Дата публикации')# при редактировании дата не изменяется
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')# время каждого сохраннения записи
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', verbose_name='Фото', blank = True)# куда именно сохранять картинки
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?', blank = True)# черновик, значение по умолчанию - тру
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)# models.PROTECT - защита от удаления совместных данных
    # related_name = ' get_news' -  переназначили атрибут news3.news_set -> news3.get_news
    views = models.IntegerField(default=0)# количество просмотров с лефолнтым щначенем 0

    def __str__(self):
        return self.title #+ ' ' + self.content

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})# kwargs={'news_id': self.pk}

    class Meta:
        ''' мета описание модели ?? '''
        verbose_name = 'Новость'# наименование модели в единственном числе
        verbose_name_plural = 'Новости'# наименование для множественного числа
        ordering = ['created_at']# сортировка записей по нескольким полям

class Category(models.Model):
    ''' первичная модель '''
    title = models.CharField(max_length=50, db_index=True, verbose_name='Категория') # db_Index = true - индексирует это поле, делает более быстрым для поиска

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title #+ ' ' + self.content

    class Meta:
        ''' мета описание модели ?? '''
        verbose_name = 'Категория'# наименование модели в единственном числе
        verbose_name_plural = 'Категории'# наименование для множественного числа
        ordering = ['title']# сортировка записей по нескольким полям