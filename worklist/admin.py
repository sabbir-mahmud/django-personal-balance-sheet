# imports
from django.contrib import admin
from .models import Todo_list

# Register your models here.


@admin.register(Todo_list)
class todo_list_admin(admin.ModelAdmin):
    list_display = ('title', 'done')
    list_display_links = ('title', 'done')
