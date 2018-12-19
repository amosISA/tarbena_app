$(document).ready(function() {

    /****** AJAX FOR RIGHT SIDE *****/
    // If i dont do it by "on", this wont work, the on is for future elements,
    // this is: proj-breadcrumb anchors created after in card for clicking callback

    // WHEN YOU CLICK ON PROJECTS ON BREADCRUMBS
    var card = $('.card');
    card.on("click", ".proj-breadcrumb", function() {
        $.ajax({
            method: 'GET',
            url: ajaxproyectos_url,
            data: {
            },
            dataType: 'json',
            success: function (data) {
                var success_div = $('.card .card-header');
                var li_proj;
                success_div.html('');
                success_div.html('<ol class="breadcrumb">' +
                                    '<li class="breadcrumb-item active">Proyectos</li>' +
                                 '</ol>');

                $.each(data, function(key, value) {
                    success_div.append('<li><a class="project-name" data-id="' + value.pk + '" href="#">' + value.fields['nombre'] + '</a></li>');
                });
            }
        });
    });

    // WHEN YOU CLICK ON EACH PROJECT TO SWITCH TO SECTORES
    card.on('click', '.project-name', function() {
        $.ajax({
            method: 'GET',
            url: ajaxsectores_url,
            data: {
                'project_name': $(this).attr('data-id')
            },
            dataType: 'json',
            success: function (data) {
                var success_div = $('.card .card-header');
                success_div.html('');
                success_div.html('<ol class="breadcrumb"><li class="breadcrumb-item"><a href="#" class="proj-breadcrumb">Proyectos</a></li><li class="breadcrumb-item active">Sectores</li></ol>');

                $.each(data, function(key, value) {
                    success_div.append('<li><a class="sector-name" href="#" data-id="' + value.pk + '">' + value.fields['sector'] + '</a></li>');
                });
            }
        });
    });

    // WHEN YOU CLICK ON EACH SECTOR TO SWITCH TO PARCELAS
    card.on('click', '.sector-name', function() {
        $.ajax({
            method: 'GET',
            url: document.location.href.replace('parcelas/#', '') + 'apiparcelas/getparcelassector/' + $(this).attr('data-id'),
            data: {
            },
            dataType: 'json',
            success: function (data) {
                var success_div = $('.card .card-header');
                var table_rows = '';
                success_div.html('');
                success_div.html('<ol class="breadcrumb"><li class="breadcrumb-item"><a href="#" class="proj-breadcrumb">Proyectos</a></li><li class="breadcrumb-item"><a href="#" class="sector-breadcrumb">Sectores</a></li><li class="breadcrumb-item">Parcelas</li></ol>');

                $.each(data, function(key, value) {
                    table_rows += ('<tr class="table-success"><td><input checked class="parcela-google-maps-checkbox" type="checkbox" data-parcela="' + value['numero_parcela'] + '" data-poligono="' + value['poligono'] + '"></td>' +
                                   '<td class="p1_poblacion">' + value['poblacion'].codigo + '</td>' +
                                   '<td>' + value['poligono'] + '</td>' +
                                   '<td><a class="modify_parcela_anchor" target="_blank" title="Modificar parcela" href="' + document.location.href.replace('parcelas/#', '') + 'panel/parcelas/parcela/' +  value['id'] + '/change">' + value['numero_parcela'] + '</a></td>' +
                                   '<td>' + value['propietario'].nif + ', ' + value['propietario'].apellidos + ' ' + value['propietario'].apellidos2 + ', ' + value['propietario'].nombre + ', (' + value['propietario'].direccion + ') <span class="total_count_parcelas" onclick="getPropietarioParcelas(3)" title="Click para saber las parcelas que pertenecen a este usuario.">*</span></td>' +
                                   '<td>' + value['metros_cuadrados'] + '</td>' +
                                   '<td><a target="_blank" title="Obtener autorización" href="' + generete_some_url(value['id']) + '"><i class="fas fa-file-alt"></i></a></td>'
                               );

                    if (value['estado'] != null) {
                        table_rows += ('<td title="' + value['estado'].nombre + '">' + value['estado'].nombre.charAt(0) + '</td>');
                    }

                    table_rows += ('</tr>');
                });
                success_div.append('<table class="table table-sm" style="width:100%;font-size:0.8rem;">' +
                                        '<thead><tr><th style="width: 20px;"></th><th title="Población" style="width: 25px;">P1</th><th title="Polígono" style="width: 25px;">P2</th><th title="Parcela" style="width: 25px;">P3</th><th>Propietario</th><th style="width: 40px;">m2</th><th></th></tr></thead>' +
                                        '<tbody>' + table_rows + '</tbody>' +
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

                // First we set to null each kml
                $.each(layers, function(i,v){
                    if (v instanceof Object) {
                        layers[i].setMap(null);
                    }
                });

                // Now print all checkboxes with their kml
                $('.parcela-google-maps-checkbox').each(function() {
                    var polig = parseInt($(this).attr('data-poligono'));
                    var parc = parseInt($(this).attr('data-parcela'));

                    /*$.ajax({
                        method: 'GET',
                        url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03127A'+ pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d',
                        success: function (data) {
                            $(data).find('Style[id="Subparcela"]').each(function() {
                                var $subparcela = $(this);
                                var fill = data.createElement("fill"), outline = data.createElement("outline");
                                fill.innerHTML = '1';
                                outline.innerHTML = '1';
                                $subparcela.find('PolyStyle').append(fill);
                                $subparcela.find('PolyStyle').append(outline);
                                $subparcela.find('PolyStyle > color').text('7FAAAAAA');
                                console.log(this);
                            });
                        }
                    });*/

                    layers[parc] = new google.maps.KmlLayer({
                        url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + $('td.p1_poblacion').first().text() + 'A' + pad(polig, 3) + pad(parc, 5) + '0000BP&del=3&mun=127&tipo=3d',
                        suppressInfoWindows: false
                        //preserveViewport: true
                    });

                    layers[parc].setMap(map);
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

$('.card').on('change', '.parcela-google-maps-checkbox', function(){
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
        mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);


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