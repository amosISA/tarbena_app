// var mapa = null;
// var oldmap = null;
// function loadMap(){
//     var alicante = new google.maps.LatLng(38.345628,-0.480759);
//     var myOptions = {
//         zoom: 17,
//         center: alicante,
//         mapTypeId: google.maps.MapTypeId.ROADMAP
//     };
//     mapa = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
//
//     //AQUÍ INDICAMOS LOS EVENTOS QUE ESCUHARÁ EL MAPA
//     google.maps.event.addListener(mapa, 'dragend',
//         function(){
//             overlay()
//         }
//     )
//
//     google.maps.event.addListener(mapa, 'zoom_changed',
//         function(){
//             overlay()
//         }
//     )
//
//     google.maps.event.addListenerOnce(mapa, 'tilesloaded',
//         function(){
//             overlay()
//         }
//     ) //Sólo me interesa tenerlo cuando se carga el mapa por primera vez
// }
//

// function loadMap() {
//     var myOptions = {
//         zoom: 5,
//         center: {lat: 41.876, lng: -87.624},
//         mapTypeId: google.maps.MapTypeId.SATELLITE
//     };
//     map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
//
//     var kmlLayer = new google.maps.KmlLayer({
//         url: 'https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03127A010000460000BP&del=3&mun=127&tipo=3d',
//         map: map
//     });
//     console.log(kmlLayer);
// }
