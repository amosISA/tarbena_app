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
        global_project_txt = null;
        global_project_txt = $(this).text();
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
        global_sector_txt = null;
        global_sector_txt = $(this).text();
        global_sector_by_id = null;
        global_sector_by_id = $(this).attr('data-id');

        $.each(layers, function(i,v){
            if (v instanceof Object) {
                layers[i].setMap(null);
            }
        });

        if (!!geoXml && !!geoXml.docs){
            for (var i=0;i<geoXml.docs.length;i++) {
                geoXml.hideDocument(geoXml.docs[i]);
            }
        }

        geoXml = new geoXML3.parser({
            map: map,
            zoom: true,
            suppressInfoWindows: false,
            afterParse: functionAfterParseFindParcela,
            markerOptions: {
                icon: "http://maps.google.com/mapfiles/ms/micons/blue.png"
              }
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
                header.html('');
                header.html('<a href="#" class="proj-breadcrumb">Proyectos (' + global_project_txt + ')</a><a href="#" class="sector-breadcrumb"> / Sectores (' + global_sector_txt + ')</a> / <a href="#" class="active">Parcelas</a>');

                $.each(data, function(key, value) {
                    if (value['estado'] != null) {
                        if (value['estado'].nombre == 'Aceptado') {
                            table_rows += ('<tr class="tr-table-aprobado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#c3e6cb" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'No aceptado') {
                            table_rows += ('<tr class="tr-table-noaceptado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#ff8787" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'Intermedio') {
                            table_rows += ('<tr class="tr-table-intermedio"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#cccc0061" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else {
                            table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-color="#ffffff" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        }
                    } else {
                        table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                    }

                    table_rows += ('<td class="p1_poblacion">' + value['poblacion'].codigo + '</td>' +
                                   '<td>' + value['poligono'] + '</td>' +
                                   '<td><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['numero_parcela'] + '</a></td>' +
                                   '<td><a class="modify_propietario_anchor" target="_blank" title="' + value['propietario'].apellidos + ' ' + value['propietario'].apellidos2 + ', ' + value['propietario'].nombre + ', (' + value['propietario'].direccion + ')" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/propietario/' +  value['propietario'].id + '/change">' + value['propietario'].nif + '</td>' +
                                   '<td>' + value['metros_cuadrados'] + '</td>' +
                                   '<td><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></td>'
                               );

                    if (value['estado'] != null) {
                        table_rows += ('<td title="' + value['estado'].nombre + '">' + value['estado'].nombre.charAt(0) + '</td>');
                    }

                    table_rows += ('</tr>');


                    //generate layers in map and add content onclick
                    //geoXml.parseKmlString(value['kml']);
                });
                body_widget.append('<table class="table table-sm panel_table_parcelas" style="width:100%;font-size:0.8rem;background-color: #ffff;color:#000;max-height:400px;overflow-y:scroll;display:block;">' +
                                        '<thead><tr><th style="width: 20px;"></th><th title="Población" style="width: 25px;">P1</th><th title="Polígono" style="width: 25px;">P2</th><th title="Parcela" style="width: 25px;">P3</th><th>Propietario</th><th style="width: 40px;">m2</th><th></th></tr></thead>' +
                                        '<tbody style="font-size:12px;">' + table_rows + '</tbody>' +
                                   '</table>'
                );

                // Change poblacion ID for CODIGO
                $("#inputPoblacion > option").each(function() {
                    var outside_this = $(this);

                    $("table td.p1_poblacion").each(function() {
                        $(this).text() == outside_this.attr("data-id") ? $(this).text(outside_this.val()) : $(this).text();
                        if ($(this).text() == 'null') { $(this).text(''); }
                    });
                });

                // Now print all checkboxes with their kml
                $('.parcela-google-maps-checkbox').each(function() {
                    var polig = parseInt($(this).attr('data-poligono'));
                    var parc = parseInt($(this).attr('data-parcela'));
                    var data_color = $(this).attr('data-color');
                    var ref_cat = '03' + $('td.p1_poblacion').first().text() + 'A' + pad(polig, 3) + pad(parc, 5) + '0000BP';

                    array_ref_catas.push({color:data_color, ref_catas:ref_cat});

                    /*

                    How to Hack CORS / CORB
                    https://medium.com/netscape/hacking-it-out-when-cors-wont-let-you-be-great-35f6206cc646
                    https://cors-anywhere.herokuapp.com/

                    I use the above url and then I pase my kml_url live in my vairbale my_kml_url and
                    it does the trick!!!

                    */
                    var my_kml_url = 'https://cors-anywhere.herokuapp.com/http://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + $('td.p1_poblacion').first().text() + 'A' + pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d';
                    //console.log(my_kml_url);
                    geoXml.parse(my_kml_url);
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

    // Setting the markers invisible
    for (var j=0; j<doc.length; j++) {
        for (var i=0;i<doc[j].markers.length;i++) {
            doc[j].markers[i].setVisible(false);
            //console.log(doc[j].markers[i].setVisible(false));
        }
    }

    for (var j=0; j<doc.length; j++) {
        for (var i=0; i<doc[j].gpolygons.length; i++) {
            // remove subparcelas and leave only the main one
            //console.log(doc[j].gpolygons[i]);
            if (doc[j].gpolygons[i].title.length < 15) {
                doc[j].gpolygons[i].setMap(null);
            } else {
                var pol_title = doc[j].gpolygons[i].title;
                var pol_prov = parseInt(pol_title.substring(0, 2));
                var pol_mun = parseInt(pol_title.substring(2, 5));
                var pol_sector = parseInt(pol_title.substring(5, 6));
                var pol_polg = parseInt(pol_title.substring(6, 9));
                var pol_parc = parseInt(pol_title.substring(9, 14));
                var pol_constr = parseInt(pol_title.substring(14,18));
                var pol_control = parseInt(pol_title.substring(18,20));
                doc[j].gpolygons[i].infoWindow.content = '<div><h3>' + pol_title + '</h3></div>';
                doc[j].gpolygons[i].infoWindowOptions.content = '<div><h3><a style="font-size:23px;font-weight:300;" href="https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx?del=' + pad(pol_prov, 1) + '&amp;muni=' + pol_mun + '&amp;rc1=' + pol_title.substring(0,7) + '&amp;rc2=' + pol_title.substring(7, 14) +  '" target="_blank">' + pol_title + '</a></h3></div>';
            }

            // clear polygons colors so that I can set a new ones in the loop of array_ref_catas
            // dynamic colors for each layer
            doc[j].gpolygons[i].setOptions({ fillColor: "", strokeColor: "", fillOpacity: ".2"});

            array_ref_catas.forEach((element, index, array) => {
                if (doc[j].placemarks[i].name == element.ref_catas) {
                    //console.log(element.ref_catas + " : " + element.color);
                    doc[j].gpolygons[i].setOptions({ fillColor: element.color, strokeColor: element.color, fillOpacity: ".3"});
                }
            });
            //console.log(doc[j].placemarks[doc[j].placemarks.length-1]);
            //console.log(doc[j].markers);

            // on click load
//            google.maps.event.addListenerOnce(map, 'idle', function () {
//                console.log("Clicking now.");
//                if (typeof(doc[j].markers) != 'undefined')
//                    google.maps.event.trigger(doc[j].markers, 'click');
//
//            });

            //doc[j].gpolygons[i].setOptions({ fillColor: "#FF0000", strokeColor: "#FF0000", fillOpacity: ".5"});

            // Another form of setting the markers not visible
            /*if (typeof(doc[j].markers[i]) != 'undefined')
                doc[j].markers[i].visible=false;*/

            google.maps.event.addListener(doc[j].gpolygons[i], "click", function() {
                this.setOptions({fillOpacity: "1"});

            });
            google.maps.event.addListener(doc[j].gpolygons[i], "mouseover", function() {
                this.setOptions({fillOpacity: "0"});
            });
            google.maps.event.addListener(doc[j].gpolygons[i], "mouseout", function() {
                this.setOptions({fillOpacity: ".3"});
            });
        }
    }
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