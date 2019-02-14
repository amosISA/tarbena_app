from django.contrib import admin

from .models import Classe, Tipus, Museo

# Register your models here.
class MuseoAdmin(admin.ModelAdmin):
    list_display = ('n_inventari', 'nom', 'classe', 'tipus', 'utilitat', 'propietari')
    list_filter = ('classe', 'tipus')
    search_fields = ('classe__nom', 'tipus__nom')

    list_select_related = (
        'classe',
        'tipus',
    )
admin.site.register(Museo, MuseoAdmin)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
admin.site.register(Classe, ClasseAdmin)

class TipusAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
admin.site.register(Tipus, TipusAdmin)