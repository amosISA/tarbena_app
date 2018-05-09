var $j = jQuery.noConflict();
$j(document).ready(function(){
    $j("#id_ente").change(function () {
        var url = $j("#some-form").attr("data-area-url"); // get the url of the `load_areas` view
        var enteId = $j(this).val();  // get the selected area ID from the HTML input

        if (enteId) {
            $j.ajax({                       // initialize an AJAX request
                url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
                data: {
                    'ente': enteId       // add the ente id to the GET parameters
                },
                success: function (data) {   // `data` is the return of the `load_areas` view function
                    $j("#id_area").html(data);  // replace the contents of the city input with the data that came from the server
                }
            });
        }

    });
});