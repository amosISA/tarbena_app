# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Subvencion, Estado, Colectivo, Ente, Area, Comment
from .sites import my_admin_site

# Register your models here.
class SubvencionAdmin(admin.ModelAdmin):
    list_display = ['inicio', 'nombre', 'fin', 'cuantia_inicial', 'cuantia_final',
                    'estado', 'ente', 'user']
    list_filter = ['nombre', 'estado', 'colectivo', 'cuantia_inicial', 'cuantia_final', 'ente']
    search_fields = ('nombre',)
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True

    def save_model(self, request, obj, form, change):
        """ Add the user in request to the subsidie when we add new subsidie from the Admin Panel """

        obj.user = request.user
        super(SubvencionAdmin, self).save_model(request, obj, form, change)
my_admin_site.register(Subvencion, SubvencionAdmin)
admin.site.register(Subvencion, SubvencionAdmin)

class EstadoAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Estado, EstadoAdmin)

class ColectivoAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Colectivo, ColectivoAdmin)

class EnteAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Ente, EnteAdmin)

class AreaAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Area, AreaAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subvencion', 'contenido', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('subvencion', 'contenido')
admin.site.register(Comment, CommentAdmin)


