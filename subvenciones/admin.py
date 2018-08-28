# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .models import Subvencion, Estado, Colectivo, Ente, Area, Comment
from .sites import my_admin_site

import xlwt
import datetime

# Subvencion PDF
def subvencion_pdf(obj):
    return '<a href="{}">PDF</a>'.format(
        reverse('subvenciones:admin_subvencion_pdf', args=[obj.id])
    )
subvencion_pdf.allow_tags = True
subvencion_pdf.short_description = 'PDF'

def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=subvenciones.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Subvenciones")

    row_num = 0

    columns = [
        ('ID', 1000), ('Fecha publicación', 3000), ('Nombre', 12000),
        ('Fecha fin', 3000), ('Cuantía inicial', 3000),
        ('Cuantía final', 3000), ('Estado', 3000), ('Ente', 3000)
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
        row_num += 1
        row = [
            str(obj.pk),
            obj.fecha_publicacion,
            obj.nombre,
            obj.fin,
            obj.cuantia_inicial,
            obj.cuantia_final,
            obj.estado.nombre,
            obj.ente.nombre,
        ]
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.date):
                font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center;border: left thin,right thin,top thin,bottom thin\
                                                     ', num_format_str='DD-MM-YYYY')
            elif col_num == 0:
                font_style = xlwt.easyxf(
                    'align: wrap on,vert centre, horiz center;border: left thin,right thin,top thin,bottom thin')
            else:
                font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center ; pattern: pattern solid,\
                                      fore-colour light_yellow;border: left thin,right thin,top thin,bottom thin')
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

export_xls.short_description = "Exportar a Excel"

class SubvencionAdmin(admin.ModelAdmin):
    list_display = ['fecha_publicacion', 'nombre', 'fin', 'cuantia_inicial', 'cuantia_final',
                    'estado', 'ente', 'user', subvencion_pdf]
    list_filter = ['nombre', 'estado', 'colectivo', 'cuantia_inicial', 'cuantia_final', 'ente']
    search_fields = ('nombre',)
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'estado',
        'ente',
        'user',
    )

    actions = [export_xls]

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


