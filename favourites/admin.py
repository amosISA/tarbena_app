from django.contrib import admin
from .models import Favourite, FavouriteTypes

# Register your models here.
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['name', 'user', 'type']
    search_fields = ('name', 'type',)
    empty_value_display = '-'
    list_display_links = ('name', 'type',)
    show_full_result_count = True

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'type',
    )
admin.site.register(Favourite, FavouritesAdmin)

class FavouritesTypesAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ('name',)
    empty_value_display = '-'
    list_display_links = ('name',)
    show_full_result_count = True
admin.site.register(FavouriteTypes, FavouritesTypesAdmin)