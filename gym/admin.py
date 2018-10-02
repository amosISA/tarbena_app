from django.contrib import admin

from .models import Gym

# Register your models here.
class GymAdmin(admin.ModelAdmin):
    list_display = ['user', 'edad', 'vigencia', 'cuantia', 'fecha_pagado', 'valido_hasta', 'pagado']
    list_filter = ['user', 'edad']
    search_fields = ('nombre',)
    empty_value_display = '-'
    list_display_links = ('user',)
    show_full_result_count = True

admin.site.register(Gym, GymAdmin)