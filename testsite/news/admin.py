from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News, Category
from django import forms

class NewsAdminForm(forms.ModelForm):
    '''
    класс, который связанн с моделью NEWs,
    который определит новую настройку поля для этой модели

    '''
    content = forms.CharField(widget= CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    '''
    класс редактор, в котором можно допольнительно представление админки

    '''
    form = NewsAdminForm

    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title') # какие поля должны быть ссылками на соответствующие модели
    search_fields = ('title', 'content') # по каким полям осуществляется поиск
    list_editable = ('is_published', ) # редактировать прямо из спика
    list_filter = ('is_published', 'category')# фильтровать по каким полям
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at')
    #список полей для вывод внутри новости (только те поля, которые редактируемый)
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at') # поля толкьо для чтения\ нельзя редактировать
    save_on_top = True

    def get_photo(self, obj):
        '''
        obj - photo
        '''
        if obj.photo:# если есть фото
            return mark_safe(f'<img src="{obj.photo.url}" width="55">')
        else:
            return 'Фото не установленно'

    get_photo.short_description = 'Миниатюра'# название столбца

class CategoryAdmin(admin.ModelAdmin):
    '''
    класс редактор, в котором можно допольнительно представление админки

    '''
    list_display = ('id', 'title')
    list_display_links = ('id', 'title') # какие поля должны быть ссылками на соответствующие модели
    search_fields = ('title',) # по каким полям осуществляется поиск - это кортеж -> , в конце если один элемент


# важен порядок
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'

