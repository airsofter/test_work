from django.contrib import admin

from lessons.models import Lesson, Product, ProductUser, LessonUser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author')
    list_editable = ('name', 'author')
    list_filter = ('name', 'author')
    search_fields = ('name', 'author')
    empty_value_display = '-пусто-'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'video', 'viewing_duration', 'product'
    )
    list_editable = ('name', 'video', 'viewing_duration', 'product')
    list_filter = ('name', 'product')
    search_fields = ('name', 'product')
    empty_value_display = '-пусто-'


@admin.register(ProductUser)
class ProductUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'user')
    list_editable = ('product', 'user')
    list_filter = ('product', 'user')
    search_fields = ('product', 'user')
    empty_value_display = '-пусто-'


@admin.register(LessonUser)
class LessonUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson', 'user', 'viewing_status', 'date_last_view')
    list_editable = ('lesson', 'user')
    list_filter = ('lesson', 'user')
    search_fields = ('lesson', 'user')
    empty_value_display = '-пусто-'
