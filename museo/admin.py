from django.contrib import admin

from .models import Classe, Tipus, Museo, Imatge

# Register your models here.
class ImatgeInline(admin.StackedInline):
    model = Imatge
    extra = 0

class MuseoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'classe', 'tipus', 'utilitat', 'propietari')
    list_filter = ('classe', 'tipus')
    search_fields = ('classe__nom', 'tipus__nom')

    list_select_related = (
        'classe',
        'tipus',
    )
    inlines = [ImatgeInline]

    def save_model(self, request, obj, form, change):
        super(MuseoAdmin, self).save_model(request, obj, form, change)
        # obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.imatges.create(imatge=afile)
admin.site.register(Museo, MuseoAdmin)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
admin.site.register(Classe, ClasseAdmin)

class TipusAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
admin.site.register(Tipus, TipusAdmin)