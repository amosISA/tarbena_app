from django.contrib import admin
from django.contrib.auth.models import User
from .models import Favourite, FavouriteTypes

# Register your models here.
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['name', 'user', 'type']
    search_fields = ('name', 'type__name',)
    empty_value_display = '-'
    list_display_links = ('name', 'type',)
    show_full_result_count = True

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'type',
    )

    # Show only user favorites, not all
    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = super(FavouritesAdmin, self).get_queryset(request)
            return qs
        else:
            qs = super(FavouritesAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)

    def add_view(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('user', 'type',)
        return super(FavouritesAdmin, self).add_view(request, *args, **kwargs)

    def change_view(self, request, object_id, extra_context=None):
        if not request.user.is_superuser:
            self.exclude = ('user', 'type',)
        return super(FavouritesAdmin, self).change_view(request, object_id, extra_context)

    def save_model(self, request, obj, form, change):
        obj.type = FavouriteTypes.objects.get(name="Personalizado")
        super(FavouritesAdmin, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Save current user
        super(FavouritesAdmin, self).save_related(request, form, formsets, change)
        user = User.objects.get(pk=request.user.pk)
        form.instance.user.add(user)
admin.site.register(Favourite, FavouritesAdmin)

class FavouritesTypesAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ('name',)
    empty_value_display = '-'
    list_display_links = ('name',)
    show_full_result_count = True
admin.site.register(FavouriteTypes, FavouritesTypesAdmin)