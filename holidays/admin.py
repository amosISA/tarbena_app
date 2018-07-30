from django.contrib import admin

from .models import Holiday

# Register your models here.
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'description']
    list_filter = ['date', 'description']
    search_fields = ('date', 'description',)
    empty_value_display = '-'
    list_display_links = ('description',)
    show_full_result_count = True

admin.site.register(Holiday, HolidayAdmin)