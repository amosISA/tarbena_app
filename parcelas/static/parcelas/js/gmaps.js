global_sector_clicked_id = '';
global_sector_clicked_txt = '';
global_project_clicked_txt = '';

$(document).ready(function() {

    // Global Breadcrumbs Variables
    var global_project_txt;
    var global_sector_txt;
    var global_sector_by_id;
    var global_project_by_id;

    /****** AJAX FOR RIGHT SIDE *****/
    // If i dont do it by "on", this wont work, the on is for future elements,
    // this is: proj-breadcrumb anchors created after in card for clicking callback

    // WHEN YOU CLICK ON PROJECTS ON BREADCRUMBS
    var card = $('#widget');
    card.on("click", ".proj-breadcrumb", function() {
        // Remove download sector as kml button if exists
        if ($('.button_download_sector_kml')) $('.button_download_sector_kml').remove();

        $.ajax({
            method: 'GET',
            url: ajaxproyectos_url,
            data: {
            },
            dataType: 'json',
            success: function (data) {
                var header = $('.widget-header__breadcrumb');
                var body_widget = $('#widget .widget-body .line');
                body_widget.html('');
                header.html('');
                header.html('Proyectos');

                $.each(data, function(key, value) {
                    body_widget.append('<a class="legend accordion-toggle project-name" data-id="' + value.pk + '" href="#">' + value.fields['nombre'] + '</a>');
                });
            }
        });
    });

    // WHEN YOU CLICK ON SECTORS ON BREADCRUMBS
    card.on("click", ".sector-breadcrumb", function() {
        // Remove download sector as kml button if exists
        if ($('.button_download_sector_kml')) $('.button_download_sector_kml').remove();

        $.ajax({
            method: 'GET',
            url: ajaxsectores_url,
            data: {
                'project_name': global_project_by_id
            },
            dataType: 'json',
            success: function (data) {
                var header = $('.widget-header__breadcrumb');
                var body_widget = $('#widget .widget-body .line');
                body_widget.html('');
                header.html('');
                header.html('<a href="#" class="proj-breadcrumb">Proyectos (' + global_project_txt + ')</a> / <a href="#" class="active">Sectores</a>');

                $.each(data, function(key, value) {
                    body_widget.append('<div class="fieldset line"><a class="legend accordion-toggle sector-name" href="#" data-id="' + value.pk + '">' + value.fields['sector'] + '</a></div>');
                });
            }
        });
    });

    // WHEN YOU CLICK ON EACH PROJECT TO SWITCH TO SECTORES
    card.on('click', '.project-name', function() {
        // Remove download sector as kml button if exists
        if ($('.button_download_sector_kml')) $('.button_download_sector_kml').remove();

        global_project_txt = null;
        global_project_txt = $(this).text();
        global_project_clicked_txt = $(this).text();
        global_project_by_id = null;
        global_project_by_id = $(this).attr('data-id');

        $.ajax({
            method: 'GET',
            url: ajaxsectores_url,
            data: {
                'project_name': $(this).attr('data-id')
            },
            dataType: 'json',
            success: function (data) {
                var header = $('.widget-header__breadcrumb');
                var body_widget = $('#widget .widget-body .line');
                body_widget.html('');
                header.html('');
                header.html('<a href="#" class="proj-breadcrumb">Proyectos (' + global_project_txt + ')</a> / <a href="#" class="active">Sectores</a>');

                $.each(data, function(key, value) {
                    body_widget.append('<div class="fieldset line"><a class="legend accordion-toggle sector-name" href="#" data-id="' + value.pk + '">' + value.fields['sector'] + '</a></div>');
                });
            }
        });
    });

    // WHEN YOU CLICK ON EACH SECTOR TO SWITCH TO PARCELAS
    card.on('click', '.sector-name', function() {
        global_sector_clicked_id = $(this).attr('data-id');
        global_sector_clicked_txt = $(this).text();
        global_sector_txt = null;
        global_sector_txt = $(this).text();
        global_sector_by_id = null;
        global_sector_by_id = $(this).attr('data-id');

        if (!!geoXml && !!geoXml.docs){
            for (var i=0;i<geoXml.docs.length;i++) {
                geoXml.hideDocument(geoXml.docs[i]);
            }
        }

        geoXml = new geoXML3.parser({
            map: map,
            zoom: true,
            suppressInfoWindows: false,
            afterParse: functionAfterParseFindParcela
        });

        $.ajax({
            method: 'GET',
            url: document.location.href.replace('parcelas/#', '') + 'apiparcelas/getparcelassector/' + $(this).attr('data-id'),
            data: {
            },
            dataType: 'json',
            success: function (data) {
                var header = $('.widget-header__breadcrumb');
                var body_widget = $('#widget .widget-body .line');
                body_widget.html('');
                var table_rows = '';
                var color_polygon = '';
                header.html('');
                header.html('<a href="#" class="proj-breadcrumb">Proyectos (' + global_project_txt + ')</a><a href="#" class="sector-breadcrumb"> / Sectores (' + global_sector_txt + ')</a> / <a href="#" class="active">Parcelas</a>');

                $.each(data, function(key, value) {
                    //console.log(value);
                    //generate layers in map and add content onclick
                    var kml_bbdd = value['kml'];
                    var coord_start = kml_bbdd.indexOf('<coordinates>');
                    var coord_end = kml_bbdd.indexOf('</coordinates>');
                    var kml_coordinates = kml_bbdd.substring(coord_start, coord_end) + "</coordinates>";
                    //var ref_cat = '03' + value['poblacion'].codigo + 'A' + pad(value['poligono'], 3) + pad(value['numero_parcela'], 5) + '0000BP';
                    var ref_cat = value['ref_catastral'];
                    // poblacion selected option
                    var e_inp_pobl = document.getElementById("inputPoblacion");
                    var e_inp_pobl_value = e_inp_pobl.options[e_inp_pobl.selectedIndex].value;

                    // Info parcela with
//                    $.ajax({
//                        method: 'GET',
//                        url: ajaxparcela_info,
//                        data: {
//                            'poblacion': e_inp_pobl_value,
//                            'poligono': pad(value['poligono'], 3),
//                            'parcela': pad(value['numero_parcela'], 5)
//                        },
//                        dataType: 'json',
//                        success: function (data) {
//                            console.log(data.m2);
//                        }
//                    });

                    if (value['estado'] != null) {
                        if (value['estado'].nombre == 'Aceptado') {
                            table_rows += ('<tr class="tr-table-aprobado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#c3e6cb" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'No aceptado') {
                            table_rows += ('<tr class="tr-table-noaceptado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#ff8787" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'Intermedio') {
                            table_rows += ('<tr class="tr-table-intermedio"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#cccc0061" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'Pendiente') {
                            table_rows += ('<tr class="tr-table-pendiente"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#A0A0A0" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else {
                            table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#ffffff" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        }
                    } else {
                        table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                    }

                    if(value['estado']) {
                        var color_kml = '';
                        table_rows += ('<td class="p1_poblacion">' + value['poblacion'].codigo + '</td>' +
                                       '<td>' + value['poligono'] + '</td>' +
                                       '<td><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['numero_parcela'] + '</a></td>' +
                                       '<td><a class="modify_propietario_anchor" target="_blank" title="' + value['get_full_name'] + '" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + '</td>' +
                                       '<td>' + value['metros_cuadrados'] + '</td>' +
                                       '<td><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></td>'
                                       //'<td><a href="javascript:kmlHighlightPoly('+j+','+i+','+value['estado'].color+');">highlight</a></td>'
                                   );

                        if (value['estado'] != null) {
                            table_rows += ('<td title="' + value['estado'].nombre + '">' + value['estado'].nombre.charAt(0) + '</td>');
                        }

                        table_rows += ('</tr>');
                        //highlightPoly(doc[j].gpolygons[i], value['estado'].color);

                        //https://stackoverflow.com/questions/5445085/understanding-colors-on-android-six-characters/11019879#11019879
                        //table for transparency in hex colors at the beggining 66...
                        if (value['estado'].nombre == 'No aceptado') { color_kml = '1400E6'; } else if (value['estado'].nombre == 'Aceptado') { color_kml = '78C878'; } else if (value['estado'].nombre == 'Intermedio') { color_kml = '78E6F0' } else if (value['estado'].nombre == 'Pendiente') { color_kml = 'A0A0A0' }

                        var full_kml = '<?xml version="1.0" encoding="ISO-8859-1"  ?>' +
                                           '<kml xmlns="http://www.opengis.net/kml/2.2">' +
                                       '<Document>' +
                                           '<Style id="polygon_style"><LineStyle><color>' + color_kml + '</color><width>2</width></LineStyle><PolyStyle><color>B3' + color_kml + '</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                           '<name>' + ref_cat + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                           '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + ref_cat + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + ', ' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong>' + value['estado'].nombre + '<br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                            '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                            '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                            '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>';
                    } else {
                        table_rows += ('<td class="p1_poblacion">' + value['poblacion'].codigo + '</td>' +
                                   '<td>' + value['poligono'] + '</td>' +
                                   '<td><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['numero_parcela'] + '</a></td>' +
                                   '<td><a class="modify_propietario_anchor" target="_blank" title="' + value['propietario'].nombre + ', (' + value['propietario'].nombre_via + ')" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + '</td>' +
                                   '<td>' + value['metros_cuadrados'] + '</td>' +
                                   '<td><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></td>'
                                   //'<td><a href="javascript:kmlHighlightPoly('+j+','+i+',ffffff);">highlight</a></td>'
                               );

                        if (value['estado'] != null) {
                            table_rows += ('<td title="' + value['estado'].nombre + '">' + value['estado'].nombre.charAt(0) + '</td>');
                        }

                        table_rows += ('</tr>');
                        //highlightPoly(doc[j].gpolygons[i], 'ffffff');

                        var full_kml = '<?xml version="1.0" encoding="ISO-8859-1"  ?>' +
                                           '<kml xmlns="http://www.opengis.net/kml/2.2">' +
                                       '<Document>' +
                                           '<Style id="polygon_style"><LineStyle><color>ffffff</color><width>2</width></LineStyle><PolyStyle><color>66ffffff</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                            '<name>' + ref_cat + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                            '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + ref_cat + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + ', ' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong><br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                            '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                            '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                            '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>';
                    }
                    //console.log(full_kml);
                    geoXml.parseKmlString(full_kml);
                });
                body_widget.append('<table class="table table-sm panel_table_parcelas" style="width:100%;font-size:0.8rem;background-color: #ffff;color:#000;max-height:400px;overflow-y:scroll;display:block;">' +
                                        '<thead><tr><th style="width: 20px;"></th><th title="Población" style="width: 25px;">P1</th><th title="Polígono" style="width: 25px;">P2</th><th title="Parcela" style="width: 25px;">P3</th><th>Propietario</th><th style="width: 40px;">m2</th><th></th><th></th></tr></thead>' +
                                        '<tbody style="font-size:12px;">' + table_rows + '</tbody>' +
                                   '</table>'
                );

                // Create download button to download all checked parcels in one KML
                if ($('.button_download_sector_kml')) $('.button_download_sector_kml').remove();
                $('.widget-body').before('<button class="button_download_sector_kml" style="font-size: .7rem;margin-bottom: 2px;">Descargar Sector (KML)</button>');

                //$('#widget').on('click', '.button_download_sector_kml', function(){
                var array_checks_parcelas = [];
                var file_export_kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Folder><name>' + global_sector_txt + '</name><open>1</open><Style><ListStyle><listItemType>check</listItemType><ItemIcon><state>open</state><href>:/mysavedplaces_open.png</href></ItemIcon><ItemIcon><state>closed</state><href>:/mysavedplaces_closed.png</href></ItemIcon><bgColor>00ffffff</bgColor><maxSnippetLines>2</maxSnippetLines></ListStyle></Style>';
                $('.button_download_sector_kml').click(function() {
                    array_checks_parcelas = [];
                    $('input.parcela-google-maps-checkbox:checkbox:checked').each(function () {
                        array_checks_parcelas.push($(this).attr("data-parcela"));
                    });

                    $.each(data, function(key, value) {
                        if($.inArray(value['numero_parcela'], array_checks_parcelas) !== -1) {
                            var kml_bbdd = value['kml'];
                            var coord_start = kml_bbdd.indexOf('<coordinates>');
                            var coord_end = kml_bbdd.indexOf('</coordinates>');
                            var kml_coordinates = kml_bbdd.substring(coord_start, coord_end) + "</coordinates>";

                            if(value['estado']) {
                                var color_kml = '';
                                if (value['estado'].nombre == 'No aceptado') { color_kml = '1400E6'; } else if (value['estado'].nombre == 'Aceptado') { color_kml = '78C878'; } else if (value['estado'].nombre == 'Intermedio') { color_kml = '78E6F0' } else if (value['estado'].nombre == 'Pendiente') { color_kml = 'A0A0A0' }
                                file_export_kml += '<Document>' +
                                                   '<Style id="polygon_style"><LineStyle><color>' + color_kml + '</color><width>2</width></LineStyle><PolyStyle><color>B3' + color_kml + '</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                                   '<name>' + value['ref_catastral'] + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                                   '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + value['ref_catastral'] + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + ', ' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong>' + value['estado'].nombre + '<br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                                   '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                                   '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                                   '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document>';
                            } else {
                                file_export_kml += '<Document>' +
                                                   '<Style id="polygon_style"><LineStyle><color>ffffff</color><width>2</width></LineStyle><PolyStyle><color>66ffffff</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                                   '<name>' + value['ref_catastral'] + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                                   '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + value['ref_catastral'] + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['get_identificacion'] + ', ' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong>' + '<br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                                   '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                                   '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                                   '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document>';
                            }
                        }
                    });
                    file_export_kml += '</Folder></kml>';
                    download(global_sector_txt+'.kml', file_export_kml);
                });
            }
        });
    });
});

function pad (str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}

var layers = [];
var layersForm = [];
var map;
var array_ref_catas = [];
var geoXml = null;
var geoXmlDoc = null;
var infowindow = new google.maps.InfoWindow();

$('#widget').on('change', '.parcela-google-maps-checkbox', function(){
    var polig = parseInt($(this).attr('data-poligono'));
    var parc = parseInt($(this).attr('data-parcela'));
    if($(this).is(':checked')) {
        layers[parc] = new google.maps.KmlLayer({
            url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03127A'+ pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d',
            suppressInfoWindows: false
            //preserveViewport: true
        });

        if (layers[parc].getMap() == null) {
            layers[parc].setMap(map);
        } else {
            layers[parc].setMap(null);
        }
    } else {
        if (layers[parc].getMap() == null) {
            layers[parc].setMap(map);
        } else {
            layers[parc].setMap(null);
        }
    }
});

$('.button-kml-download').click(function() {
    var polig = $('#inputPoligono');
    var parc = $('#inputParcela');
    var inputPobacion = $( "#inputPoblacion option:selected" ).val();
    var inputPolig = polig.val();
    var inputParc = parc.val();
    if (inputPolig.length === 0 || inputParc.length === 0) {
        if (window.confirm('Rellene los inputs de parcela o polígono'))
        {
            inputParc.length === 0 ? parc.focus() : polig.focus()
            inputPolig.length === 0 ? polig.focus() : parc.focus()
        }
    } else {
        window.open('https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + inputPobacion + 'A'+ pad(inputPolig, 3) + pad(inputParc, 5) + '0000BP&del=3&mun=' + inputPobacion + '&tipo=3d');
    }
});

$('.formButtonCheckParcela').click(function() {
    var inputPolig = $('#inputPoligono').val();
    var inputParc = $('#inputParcela').val();
    var inputPobacion = $( "#inputPoblacion option:selected" ).val();
    //console.log(layersForm);

    $.each(layersForm, function(i,v){
        if (v instanceof Object) {
            layersForm[i].setMap(null);
        }
        //console.log(i + ' ' + v instanceof Object);
    });

    layersForm[inputParc] = new google.maps.KmlLayer({
        url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + inputPobacion + 'A'+ pad(inputPolig, 3) + pad(inputParc, 5) + '0000BP&del=3&mun=' + inputPobacion + '&tipo=3d',
        suppressInfoWindows: false
    });
    //console.log('https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + inputPobacion + 'A'+ pad(inputPolig, 3) + pad(inputParc, 5) + '0000BP&del=3&mun=' + inputPobacion + '&tipo=3d');

    layersForm[inputParc].setMap(map);
});

function initialize(){
    var myOptions = {
        zoom: 11,
        center: {lat: 38.691351, lng: -0.100658},
        mapTypeId: google.maps.MapTypeId.SATELLITE,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP
        },
    };
    map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
}
google.maps.event.addDomListener(window, 'load', initialize);

function functionAfterParseFindParcela(doc){
    for (var j = 0; j < doc.length ; j++) { // Added by me to parse all kml files to the map
        geoXmlDoc = doc;

//        for (var i = 0; i < doc[j].gpolygons.length; i++) {
//            //console.log(doc[j].gpolygons[i].fillOpacity);
//            google.maps.event.addListener(doc[j].gpolygons[i], "mouseover", function() {
//                this.setOptions({fillOpacity: "0"});
//            });
//            google.maps.event.addListener(doc[j].gpolygons[i], "mouseout", function() {
//                this.setOptions({fillOpacity: "0.69"});
//            });
//        }
    }
}

/* Pop up Ayuntamiento Parcelas */
/* Pop up ayto parcelas if checkbox is checked */
$('input#aytoParcelasCheck').click(function() {
    if ($(this).is(':checked')) {
        aytoParc();
    } else {
        if (!!geoXml && !!geoXml.docs){
            for (var i=0;i<geoXml.docs.length;i++) {
                geoXml.hideDocument(geoXml.docs[i]);
            }
        }
    }
});

function moveToLocation(lat, lng){
    var center = new google.maps.LatLng(lat, lng);
    map.panTo(center);
}

function aytoParc() {
    geoXml = new geoXML3.parser({
        map: map,
        zoom: true,
        disableAutoPan: true,
        suppressInfoWindows: false,
        afterParse: functionAfterParseFindParcela
    });

    $.ajax({
        method: 'GET',
        url: document.location.href.replace('parcelas/#', '') + 'apiparcelas/getparcelassector/9',
        data: {
        },
        dataType: 'json',
        success: function (data) {
            $.each(data, function(key, value) {
                //console.log(value);
                //generate layers in map and add content onclick
                var kml_bbdd = value['kml'];
                var coord_start = kml_bbdd.indexOf('<coordinates>');
                var coord_end = kml_bbdd.indexOf('</coordinates>');
                var kml_coordinates = kml_bbdd.substring(coord_start, coord_end) + "</coordinates>";
                //var ref_cat = '03' + value['poblacion'].codigo + 'A' + pad(value['poligono'], 3) + pad(value['numero_parcela'], 5) + '0000BP';
                var ref_cat = value['ref_catastral'];
                // poblacion selected option
                var e_inp_pobl = document.getElementById("inputPoblacion");
                var e_inp_pobl_value = e_inp_pobl.options[e_inp_pobl.selectedIndex].value;

                //https://stackoverflow.com/questions/5445085/understanding-colors-on-android-six-characters/11019879#11019879
                //table for transparency in hex colors at the beggining 66...
                if(value['estado']) {
                    //console.log(value['estado'].color);
                    var full_kml = '<?xml version="1.0" encoding="ISO-8859-1"  ?>' +
                                       '<kml xmlns="http://www.opengis.net/kml/2.2">' +
                                   '<Document>' +
                                       '<Style id="polygon_style"><LineStyle><color>ffffff</color><width>2</width></LineStyle><PolyStyle><color>66ffffff</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                       '<name>' + ref_cat + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                       '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + ref_cat + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong>' + value['estado'].nombre + '<br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                        '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                        '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                        '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>';
                } else {
                    var full_kml = '<?xml version="1.0" encoding="ISO-8859-1"  ?>' +
                                       '<kml xmlns="http://www.opengis.net/kml/2.2">' +
                                   '<Document>' +
                                       '<Style id="polygon_style"><LineStyle><color>ffffff</color><width>2</width></LineStyle><PolyStyle><color>66ffffff</color><fill>1</fill><outline>1</outline></PolyStyle></Style>' +
                                        '<name>' + ref_cat + '</name><Placemark>' + '<name><![CDATA[<font size=+1><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['localizacion'] + '</a></font>]]></name>' +
                                        '<description><![CDATA[<font size=+0><A href="' + value['url']  + '" target="_blank">' + ref_cat + '</a></font><br><font size=+0><span style="margin-top:10px;"><strong>Propietario</strong>: <a class="modify_propietario_anchor" target="_blank" href="' + document.location.href.replace('parcelas/#', '') + 'panel/terceros/terceros/' +  value['propietario'].id + '/change">' + value['propietario'].nombre + ',<br> (' + value['propietario'].nombre_via + ')</a><br><strong>Estado: </strong><br><strong>m2: </strong>' + value['metros_cuadrados'] + ' m2<br><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></font>]]></description>' +
                                        '<Polygon>' + '<styleUrl>#polygon_style</styleUrl>' +
                                        '<tessellate>1</tessellate><outerBoundaryIs><LinearRing>' + kml_coordinates +
                                        '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>';
                }
                geoXml.parseKmlString(full_kml);
            });
        }
    });

    //moveToLocation( -34, 150 );
}

function kmlHighlightPoly(doc,poly,color) {
  for (var j=0; j < geoXmlDoc.length; j++) {
    for (var i = 0; i < geoXmlDoc[doc].gpolygons.length; i++) {
        if ((j == doc) && (i == poly)) {
            geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: color, strokeColor: color });
        } else {
            geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: color, strokeColor: color, fillOpacity: 0.4 });
        }
    }
  }
}

function highlightPoly(poly, color) {
  google.maps.event.addListener(poly, "mouseover", function () {
    for (var j=0; j < geoXmlDoc.length; j++) {
      for (var i = 0; i < geoXmlDoc[j].gpolygons.length; i++) {
        if (poly == geoXmlDoc[j].gpolygons[i]) {
            geoXmlDoc[j].gpolygons[i].setOptions({ fillOpacity: 0.1 });
        } else {
            geoXmlDoc[j].gpolygons[i].setOptions({ fillOpacity: 0.1 });
        }
      }
    }
    poly.setOptions({ fillOpacity: 0.4 });
  });
  google.maps.event.addListener(poly, "mouseout", function () {
    poly.setOptions({ fillColor: color, strokeColor: color, fillOpacity: 0.5 });
  });
}

// Click on download sector parcelas as KML
function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

////////////////////////
///// GEOLOCATION /////
///////////////////////
function locError(error) {
    // the current position could not be located
    alert("The current position could not be found!");
}

function setCurrentPosition(pos) {
    currentPositionMarker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(
            pos.coords.latitude,
            pos.coords.longitude
        ),
        title: "Current Position"
    });
    map.panTo(new google.maps.LatLng(
            pos.coords.latitude,
            pos.coords.longitude
        ));
}

function displayAndWatch(position) {
    // set current position
    setCurrentPosition(position);
    // watch position
    watchCurrentPosition();
}

function watchCurrentPosition() {
    var positionTimer = navigator.geolocation.watchPosition(
        function (position) {
            setMarkerPosition(
                currentPositionMarker,
                position
            );
        });
}

function setMarkerPosition(marker, position) {
    marker.setPosition(
        new google.maps.LatLng(
            position.coords.latitude,
            position.coords.longitude)
    );
}

function initLocationProcedure() {
    initialize();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(displayAndWatch, locError);
    } else {
        alert("Your browser does not support the Geolocation API");
    }
}

$('#preloader').click(function() {
    initLocationProcedure();
});