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
                            table_rows += ('<tr class="tr-table-aprobado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'No aceptado') {
                            table_rows += ('<tr class="tr-table-noaceptado"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else if (value['estado'].nombre == 'Intermedio') {
                            table_rows += ('<tr class="tr-table-intermedio"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        } else {
                            table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                        }
                    } else {
                        table_rows += ('<tr><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>');
                    }

                    table_rows += ('<td class="p1_poblacion">' + value['poblacion'].codigo + '</td>' +
                                   '<td>' + value['poligono'] + '</td>' +
                                   '<td><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['numero_parcela'] + '</a></td>' +
                                   '<td><a class="modify_propietario_anchor" target="_blank" title="Modificar propietario" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/propietario/' +  value['propietario'].id + '/change">' + value['propietario'].nif + ', ' + value['propietario'].apellidos + ' ' + value['propietario'].apellidos2 + ', ' + value['propietario'].nombre + ', (' + value['propietario'].direccion + ')</td>' +
                                   '<td>' + value['metros_cuadrados'] + '</td>' +
                                   '<td><a class="anchor_autorizacion_parcelas" target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></td>'
                               );

                    if (value['estado'] != null) {
                        table_rows += ('<td title="' + value['estado'].nombre + '">' + value['estado'].nombre.charAt(0) + '</td>');
                    }

                    table_rows += ('</tr>');
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

                // load layers
                // First I clear all geoXML layers that are shown
                /*if (geoXml)
                    geoXml.hideDocument();*/
                if (!!geoXml && !!geoXml.docs){
                    for (var i=0;i<geoXml.docs.length;i++) {
                        geoXml.hideDocument(geoXml.docs[i]);
                    }
                }

                geoXml = new geoXML3.parser({
                    map: map,
                    zoom: true,
                    suppressInfoWindows: true,
                    afterParse: functionAfterParseParcelas
                });

                // Now print all checkboxes with their kml
                var checkboxes_length = $('.parcela-google-maps-checkbox').length;
                $('.parcela-google-maps-checkbox').each(function(index) {
                    var polig = parseInt($(this).attr('data-poligono'));
                    var parc = parseInt($(this).attr('data-parcela'));
                    //var pobl = parseInt($(this).attr('data-poblacion'));

                    var kml_url = 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + $('td.p1_poblacion').first().text() + 'A' + pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d';

                    layers[parc] = new google.maps.KmlLayer({
                        url: kml_url,
                        suppressInfoWindows: false
                        //preserveViewport: true
                    });

                    geoXml.parse(layers[parc]['url']);
                    //console.log(kml_url);
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
var geoXml = null;
var geoXmlDoc = null;
var sidebarHtml = "";
var mapOverlays = [];
var infWindow = new google.maps.InfoWindow();

$('#widget').on('change', '.parcela-google-maps-checkbox', function(){
    var polig = parseInt($(this).attr('data-poligono'));
    var parc = parseInt($(this).attr('data-parcela'));
    if($(this).is(':checked')) {
        layers[parc] = new google.maps.KmlLayer({
            url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03127A'+ pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d',
            suppressInfoWindows: false
            //preserveViewport: true
        });

        if (!!geoXml && !!geoXml.docs){
            for (var i=0;i<geoXml.docs.length;i++) {
                geoXml.hideDocument(geoXml.docs[i]);
            }
        }
        geoXml.parse(layers[parc]['url']);
    } else {
        if (!!geoXml && !!geoXml.docs){
            for (var i=0;i<geoXml.docs.length;i++) {
                geoXml.hideDocument(geoXml.docs[i]);
            }
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

    // load layers
    // First I clear all geoXML layers that are shown
    //    if (geoXml)
    //        geoXml.hideDocument();
    if (!!geoXml && !!geoXml.docs){
        for (var i=0;i<geoXml.docs.length;i++) {
            geoXml.hideDocument(geoXml.docs[i]);
        }
    }

    geoXml = new geoXML3.parser({
        map: map,
        zoom: false,
        suppressInfoWindows: true,
        afterParse: functionAfterParseFindParcela
    });

    var format_kml = '<kml><Document><Placemark id="Tester">';
    var kml_url = 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + inputPobacion + 'A'+ pad(inputPolig, 3) + pad(inputParc, 5) + '0000BP&del=3&mun=' + inputPobacion + '&tipo=3d';
    //console.log(kml_url);
    $.ajax(kml_url).done(function(xml) {
        var geojson = toGeoJSON.kml(xml);
        var name, coordinates, properties_var, geometry_var;
        var all_coordinates = "";

        /*
            Name =>           properties_var.name
            Coordinates =>    geometry_var.coordinates

            This is what object has => value[0]:
                0:
                    geometry: {type: "Polygon", coordinates: Array(1)}
                    properties: {name: "03127A010000840000BP", styleUrl: "#linea_parcela", styleHash: "29f78728", stroke: "#000000", stroke-opacity: 1, …}
                    type: "Feature"
        */

        $.each(geojson, function(key, value) {
            properties_var = value[0].properties;
            geometry_var = value[0].geometry;
        });
        //console.log(geometry_var.coordinates);

        format_kml += ('<name>' + properties_var.name + '</name><Polygon><outerBoundaryIs><LinearRing><tessellate>0</tessellate><coordinates>');

        // Recursive function to get all values inside array of arrays
        function printArray(arr){
            for(var i = 0; i < arr.length; i++){
                if(arr[i] instanceof Array){
                    // console.log(arr[i] + " HOLA");
                    if (arr[i].length <= 3) {
                        all_coordinates += (arr[i]+" ");
                    }
                    printArray(arr[i]);
                } else {
                    arr[i];
                }
            }
        }

        printArray(geometry_var.coordinates);
        format_kml += (all_coordinates + '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>');
        geoXml.parseKmlString(format_kml);

        var tmpOverlay, ovrOptions;
        for (var m = 0; m < geoXml.docs[0].placemarks.length; m++) {
            if (geoXml.docs[0].placemarks[m].Polygon) {
                tmpOverlay = geoXml.docs[0].placemarks[m].polygon;
                tmpOverlay.type = "polygon";
            } else if (geoXml.docs[0].placemarks[m].LineString) {
                tmpOverlay = geoXml.docs[0].placemarks[m].polyline;
                tmpOverlay.type = "polyline";
            } else if (geoXml.docs[0].placemarks[m].Point) {
                tmpOverlay = geoXml.docs[0].placemarks[m].marker;
                tmpOverlay.type = "marker";
            }

            if (geoXml.docs[0].placemarks[m].name) {
                tmpOverlay.title = geoXml.docs[0].placemarks[m].name;
            } else {
                tmpOverlay.title = "";
            }

            if (geoXml.docs[0].placemarks[m].description) {
                tmpOverlay.content = geoXml.docs[0].placemarks[m].description;
            } else {
                tmpOverlay.content = "Polígono " + inputPolig + " Parcela " + inputParc + ", " + $( "#inputPoblacion option:selected" ).text();
            }

            //attach the click listener to the overlay
            AttachClickListener(tmpOverlay);

            //save the overlay in the array
            mapOverlays.push(tmpOverlay);
        }
        map.fitBounds(geoXml.docs[0].bounds);
    });
});

function functionAfterParseFindParcela(doc){
    //console.log(doc[0].gpolygons[0]);
    var polygons = doc[0].gpolygons;
    doc[0].gpolygons[0].fillColor = "#c3e6cb"; // change polygon color
    doc[0].gpolygons[0].fillOpacity = ".5"; // change polygon opacity

    // On hover change color polygon
    for (polygonindex = 0, loopend = polygons.length; polygonindex < loopend; polygonindex++) {
        google.maps.event.addListener(polygons[polygonindex], "mouseover", function() {
            this.setOptions({fillOpacity: ".8"});
        });
        google.maps.event.addListener(polygons[polygonindex], "mouseout", function() {
            this.setOptions({fillOpacity: ".5"});
        });
    }
}

function kmlHighlightPoly(doc,poly) {
          for (var j=0; j < geoXmlDoc.length; j++) {
            for (var i = 0; i < geoXmlDoc[doc].gpolygons.length; i++) {
                if ((j == doc) && (i == poly)) {
                    geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: "#FF0000", strokeColor: "#FF0000" });
                } else {
                    geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: "#78A04C", strokeColor: "#78A04C", fillOpacity: 0.4 });
                }
            }
          }
        }

        function showAll() {
          var bounds = geoXmlDoc[0].bounds;
          for (var j = 0; j < geoXmlDoc.length; j++) {
            bounds.union(geoXmlDoc[j].bounds);
            for (var i = 0; i < geoXmlDoc[j].gpolygons.length; i++) {
                geoXmlDoc[j].gpolygons[i].setMap(map);
            }
          }
          map.fitBounds(bounds);
        }

        function highlightPoly(poly) {
          google.maps.event.addListener(poly, "mouseover", function () {
            for (var j=0; j < geoXmlDoc.length; j++) {
              for (var i = 0; i < geoXmlDoc[j].gpolygons.length; i++) {
                if (poly == geoXmlDoc[j].gpolygons[i]) {
                    geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: "#FF0000", strokeColor: "#FF0000" });
                } else {
                    geoXmlDoc[j].gpolygons[i].setOptions({ fillColor: "#78A04C", strokeColor: "#78A04C", fillOpacity: 0.4 });
                }
              }
            }
            poly.setOptions({ fillColor: "#FF0000", strokeColor: "#FF0000" });
          });
          google.maps.event.addListener(poly, "mouseout", function () {
            poly.setOptions({ fillColor: "#78A04C", strokeColor: "#78A04C", fillOpacity: 0.4 });
          });
        }

function functionAfterParseParcelas(doc){
    var sidebarHtml = '<table><tr><td><a href="javascript:showAll();">Show All</a></td></tr>';

    for (var j=0; j < doc.length; j++) {
        geoXmlDoc = doc;

        for (var i=0; i < doc[j].gpolygons.length; i++) {
            sidebarHtml += '<tr><td>' + doc[j].placemarks[i].name + ' - <a   href="javascript:kmlHighlightPoly('+j+','+i+');">highlight</a><br></td></tr>';
        }
    }

    sidebarHtml += "</table>";
    $('#widget .widget-body .line').append(sidebarHtml);
}

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

function AttachClickListener(overlay) {
  google.maps.event.addListener(overlay, "click", function(clkEvent) {
    console.log("i clicked!");
    var infContent = GetContent(overlay);
    openInfowindow(overlay, clkEvent.latLng, infContent);
  });
}

function GetContent(overlay) {
  var content = '<div><h3>' + overlay.title + '</h3>' + overlay.content + '<br></div>';
  return content;
}

function openInfowindow(overlay, latLng, content) {
  var div = document.createElement('div');
  div.innerHTML = content;
  //div.style.backgroundColor="red";
  infWindow.setContent(div);
  infWindow.setPosition(latLng);
  infWindow.relatedOverlay = overlay;
  var t = overlay.get('fillColor');
  infWindow.open(map);
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