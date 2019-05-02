# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.forms import CheckboxSelectMultiple

from import_export.admin import ImportExportModelAdmin
from .models import Parcela, SectorTrabajo, Estado, Proyecto, Poblacion, Estado_Parcela_Trabajo, Provincia, PoblacionesFavoritas
from .sites import my_admin_site

import urllib.request
import re
import ssl
import xlwt

import sys
sys.path.append("..")
from terceros.models import Terceros

def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=parcelas.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Parcelas")

    row_num = 0

    columns = [
        ('ID', 2000), ('Población', 4000), ('Polígono', 3000),
        ('Parcela', 3000), ('Propietario', 16000),
        ('Metros cuadrados', 3000), ('Estado', 3000), ('Estado parcela trabajo', 3000),
    ]

    font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                   fore-colour light_orange;border: left thin,right thin,top thin,bottom thin')
    font_style.font.bold = True
    font_style.alignment.wrap = 1

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        if obj.estado:
            row_num += 1
            row = [
                str(obj.pk),
                obj.poblacion.nombre,
                obj.poligono,
                obj.numero_parcela,
                '{}, {} {}, {}, ({})'.format(obj.propietario.nif, obj.propietario.apellidos, obj.propietario.apellidos2, obj.propietario.nombre, obj.propietario.direccion),
                obj.metros_cuadrados,
                obj.estado.nombre,
                obj.estado_parcela_trabajo.nombre
            ]
            for col_num in range(len(row)):
                font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center ; pattern: pattern solid,\
                                      fore-colour light_yellow;border: left thin,right thin,top thin,bottom thin')
                ws.write(row_num, col_num, row[col_num], font_style)
        else:
            row_num += 1
            row = [
                str(obj.pk),
                obj.poblacion.nombre,
                obj.poligono,
                obj.numero_parcela,
                '{}, {} {}, {}, ({})'.format(obj.propietario.nif, obj.propietario.apellidos, obj.propietario.apellidos2,
                                             obj.propietario.nombre, obj.propietario.direccion),
                obj.metros_cuadrados,
                '',
                obj.estado_parcela_trabajo.nombre
            ]
            for col_num in range(len(row)):
                font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center ; pattern: pattern solid,\
                                                  fore-colour light_yellow;border: left thin,right thin,top thin,bottom thin')
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

export_xls.short_description = "Exportar a Excel"

class ParcelaInline(admin.TabularInline):
    model = Parcela
    max_num = 0
    show_change_link = True

class SectorTrabajoInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#working-with-many-to-many-models
    # Guide to inline with ManyToMany relationship
    model = Parcela.sector_trabajo.through
    extra = 0

def cleanhtml(raw_html):
    """
    Function to remove tags from a string

    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

class ParcelaAdmin(ImportExportModelAdmin):
    list_display = ['poblacion' ,'poligono', 'numero_parcela', 'propietario',
                    'metros_cuadrados', 'estado_parcela_trabajo', 'estado']
    #list_editable = ('propietario',)
    raw_id_fields = ('propietario',)
    list_filter = ['sector_trabajo', 'estado_parcela_trabajo']
    search_fields = ('propietario__nombre', 'propietario__identificacion', 'propietario__primer_apellido', 'propietario__segundo_apellido',
                     'metros_cuadrados', 'poligono', 'numero_parcela', 'poblacion__nombre',
                     'sector_trabajo__sector')
    empty_value_display = '-'
    list_display_links = ('numero_parcela',)
    show_full_result_count = True
    list_max_show_all = 4000
    #list_per_page = 4000

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'poblacion',
        'propietario',
        'estado',
        'estado_parcela_trabajo',
        'poblacion__provincia',
    )

    inlines = [SectorTrabajoInline]
    actions = [export_xls]

    def sectores_trabajo(self, obj):
        return "\n".join([p.sector for p in obj.sector_trabajo.all()])

    # Make kml for each parcela and save their localizacion and url
    def save_model(self, request, obj, form, change):
        super(ParcelaAdmin, self).save_model(request, obj, form, change)
        #https://stackoverflow.com/questions/3813735/in-python-how-to-specify-a-format-when-converting-int-to-string

        # Add same value to field poseedor as field propietario
        # if not obj.poseedor:
        #     terceros = Terceros.objects.all()
        #     for t in terceros:
        #         if t.identificacion == obj.propietario.nif:
        #             obj.poseedor = t
        #             obj.save()

        # OR THIS BY THE shell of python
        # >> > from terceros.models import *
        # >> > from parcelas.models import *
        # >> > terceros = Terceros.objects.all()
        # >> > parcelas = Parcela.objects.all().prefetch_related('sector_trabajo'
        #                                                        ...).select_related(
        #     ...
        # 'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
        #     ...             )
        #
        # >> for t in terceros:
        #     ...
        #     for p in parcelas:
        #         ...
        #     if t.identificacion == p.propietario.nif:
        #         ...
        #     p.poseedor = t
        # ...
        # p.save()

        if not obj.kml:
            context = ssl._create_unverified_context()
            kml_url='https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=0' + obj.poblacion.provincia.codigo + obj.poblacion.codigo + 'A'+ "{:03n}".format(int(obj.poligono)) + "{:05n}".format(int(obj.numero_parcela)) + '0000BP&del=3&mun=' + obj.poblacion.codigo + '&tipo=3d'
            fp = urllib.request.urlopen(kml_url,context=context)
            mybytes = fp.read()
            mykml = mybytes.decode('unicode_escape').encode('utf-8')
            obj.kml = mykml
            obj.save()

        if not obj.localizacion:
            my_url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCConCiud.aspx?del=3&mun=" + obj.poblacion.codigo + "&UrbRus=&RefC=0" + obj.poblacion.provincia.codigo + obj.poblacion.codigo + "A" + "{:03n}".format(int(obj.poligono)) + "{:05n}".format(int(obj.numero_parcela)) + "0000BL&Apenom=&esBice=&RCBice1=&RCBice2=&DenoBice=&latitud=&longitud=&gradoslat=&minlat=&seglat=&gradoslon=&minlon=&seglon=&x=&y=&huso=&tipoCoordenadas="
            uClient = urllib.request.urlopen(my_url)
            page_html = uClient.read()
            uClient.close()
            obj.url = my_url

            page_soup = BeautifulSoup(page_html, "html.parser")
            labels_page = page_soup.find_all("label")
            for index, item in enumerate(labels_page, start=0):
                if index == 2:
                    remove_br = re.sub('<br/>', ' ', str(item))
                    obj.localizacion = cleanhtml(remove_br)
                    obj.save()

        if not obj.ref_catastral:
            my_url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCConCiud.aspx?del=3&mun=" + obj.poblacion.codigo + "&UrbRus=&RefC=0" + obj.poblacion.provincia.codigo + obj.poblacion.codigo + "A" + "{:03n}".format(int(obj.poligono)) + "{:05n}".format(int(obj.numero_parcela)) + "0000BL&Apenom=&esBice=&RCBice1=&RCBice2=&DenoBice=&latitud=&longitud=&gradoslat=&minlat=&seglat=&gradoslon=&minlon=&seglon=&x=&y=&huso=&tipoCoordenadas="
            uClient = urllib.request.urlopen(my_url)
            page_html = uClient.read()
            uClient.close()
            obj.url = my_url

            page_soup = BeautifulSoup(page_html, "html.parser")
            labels_page = page_soup.find_all("label")
            for index, item in enumerate(labels_page, start=0):
                if index == 1:
                    obj.ref_catastral = item.get_text()
                    obj.save()

    # Massive parcelas upload bbdd to add their kml if not exist
    # This function pops the save button for the editable_list option of admin
    # This functions also add localizacion and the url to parcela where we can find her in the catastro if not exists those fields
    # def changelist_view(self, request, extra_context=None):
    #     #if request.POST.has_key("_save"):
    #     if "_save" in request.POST:
    #         parcelas = Parcela.objects.all().prefetch_related('sector_trabajo'
    #         ).select_related(
    #             'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
    #         )
    #         for p in parcelas:
    #             # if not p.kml:
    #             #     context = ssl._create_unverified_context()
    #             #     kml_url = 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + p.poblacion.codigo + 'A' + "{:03n}".format(
    #             #         int(p.poligono)) + "{:05n}".format(
    #             #         int(p.numero_parcela)) + '0000BP&del=3&mun=' + p.poblacion.codigo + '&tipo=3d'
    #             #     fp = urllib.request.urlopen(kml_url, context=context)
    #             #     mybytes = fp.read()
    #             #     mykml = mybytes.decode('unicode_escape').encode('utf-8')
    #             #     p.kml = mykml
    #             #     p.save()
    #             my_url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCConCiud.aspx?del=3&mun=" + p.poblacion.codigo + "&UrbRus=&RefC=0" + p.poblacion.provincia.codigo + p.poblacion.codigo + "A" + "{:03n}".format(int(p.poligono)) + "{:05n}".format(int(p.numero_parcela)) + "0000BL&Apenom=&esBice=&RCBice1=&RCBice2=&DenoBice=&latitud=&longitud=&gradoslat=&minlat=&seglat=&gradoslon=&minlon=&seglon=&x=&y=&huso=&tipoCoordenadas="
    #             uClient = urllib.request.urlopen(my_url)
    #             page_html = uClient.read()
    #             uClient.close()
    #             p.url = my_url
    #
    #             page_soup = BeautifulSoup(page_html, "html.parser")
    #             labels_page = page_soup.find_all("label")
    #             for index, item in enumerate(labels_page, start=0):
    #                 if index == 2:
    #                     remove_br = re.sub('<br/>', ' ', str(item))
    #                     p.localizacion = cleanhtml(remove_br)
    #                     p.save()
    #                 if index == 1:
    #                     p.ref_catastral = item.get_text()
    #                     p.save()
    #     return admin.ModelAdmin.changelist_view(self, request, extra_context)

my_admin_site.register(Parcela, ParcelaAdmin)
admin.site.register(Parcela, ParcelaAdmin)

# class PropietarioAdmin(ImportExportModelAdmin):
#     list_display = ['nombre', 'apellidos', 'apellidos2', 'poblacion', 'direccion', 'nif',
#                     'telefono_fijo', 'telefono_movil', 'comentarios']
#     list_filter = ['nombre']
#     #list_editable = ('poblacion',)
#     search_fields = ('nombre', 'apellidos', 'nif', 'poblacion__nombre',
#                      'telefono_fijo', 'telefono_movil', 'comentarios',)
#     empty_value_display = '-'
#     show_full_result_count = True
#     inlines = [ParcelaInline]
#
#     list_select_related = (
#         'poblacion',
#         'poblacion__provincia',
#     )
# admin.site.register(Propietario, PropietarioAdmin)

class SectorTrabajoAdmin(admin.ModelAdmin):
    list_display = ['sector']
    list_filter = ['sector']
    search_fields = ('sector',)
    empty_value_display = '-'
    show_full_result_count = True
    inlines = [SectorTrabajoInline]
admin.site.register(SectorTrabajo, SectorTrabajoAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'comentarios']
    list_filter = ['nombre']
    search_fields = ('nombre', 'descripcion', 'comentarios',)
    empty_value_display = '-'
    show_full_result_count = True

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
admin.site.register(Proyecto, ProyectoAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color']
    list_editable = ('color',)
    list_filter = ['nombre']
    search_fields = ('nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Estado, EstadoAdmin)

class EstadoParcelaTrabajoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'porcentaje']
    list_filter = ['nombre']
    search_fields = ('nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Estado_Parcela_Trabajo, EstadoParcelaTrabajoAdmin)

class PoblacionAdmin(ImportExportModelAdmin):
    list_display = ['codigo', 'nombre', 'provincia']
    #list_filter = ['codigo', 'nombre', 'provincia']
    list_display_links = ('nombre',)
    search_fields = ('codigo', 'nombre', 'provincia',)
    empty_value_display = '-'
    show_full_result_count = True

    list_select_related = (
        'provincia',
    )
admin.site.register(Poblacion, PoblacionAdmin)

class ProvinciaAdmin(ImportExportModelAdmin):
    list_display = ['codigo', 'nombre']
    #list_editable = ('codigo',)
    #list_filter = ['codigo', 'nombre']
    list_display_links = ('nombre',)
    search_fields = ('codigo', 'nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Provincia, ProvinciaAdmin)

class PoblacionesFavoritasAdmin(admin.ModelAdmin):
    list_display = ['user', 'poblaciones_favoritas', 'superfavorita']
    #list_filter = ['user', 'poblacion']
    search_fields = ('user__username', 'poblacion__nombre',)
    empty_value_display = '-'
    show_full_result_count = True
    exclude = ('user',)

    list_select_related = (
        'user',
        'superfavorita',
    )

    def save_model(self, request, obj, form, change):
        # save user because has a hidden field
        obj.user = request.user
        super(PoblacionesFavoritasAdmin, self).save_model(request, obj, form, change)
admin.site.register(PoblacionesFavoritas, PoblacionesFavoritasAdmin)
