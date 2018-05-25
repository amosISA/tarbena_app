var $j = jQuery.noConflict();
$j(document).ready(function(){
    // Modify textareas
    $j("textarea[name='drive'], textarea[name='procedimiento'], textarea[name='bases'], textarea[name='solicitud'], textarea[name='nombre']").attr({'cols': '20', 'rows': '1'});
    $j("textarea[name='descripcion']").attr({'cols': '20', 'rows': '12'});
    $j("textarea[name='cuantia_inicial']").attr({'cols': '20', 'rows': '1'});
    $j("textarea[name='cuantia_final']").attr({'cols': '20', 'rows': '1'});
    $j("textarea[name='nombre_carpeta_drive']").attr({'cols': '20', 'rows': '1'});

    // Add from admin site functionality
    $j('#add_id_estado').insertAfter($j('label[for="id_estado"]'));
    $j('#add_id_ente').insertAfter($j('label[for="id_ente"]'));
    $j('#add_id_area').insertAfter($j('label[for="id_area"]'));

    // Add class to select because they lose class with admin functionality
    $j("form:first select").removeClass("form-control").addClass("form-control");

    // Quit checkbox attr form-control
    $j("#id_se_relaciona_con li label input, #id_responsable li label input, #id_colectivo li label input").removeClass("form-control");


    /* Date bussiness days 30, 25, 10 */
    var id_date_inicio = $j('#id_inicio');
    var id_date_fin = $j('#id_fin');
    var content_div_fin = '<div class="id_date_fin_anchors_bussines_day"><a href="#" onClick="businessDays(15);">+ 15 días hábiles</a><a href="#" onClick="businessDays(20);">+ 20 días hábiles</a><a href="#" onClick="businessDays(30);">+ 30 días hábiles</a></div>';
    id_date_inicio.change(function() {
        if (id_date_inicio.val()) {
            if (!$j('.id_date_fin_anchors_bussines_day').length) {
                id_date_fin.after(content_div_fin);
            }
        } else {
            console.log('error');
            $j('.id_date_fin_anchors_bussines_day').remove();
        }
    });


    // Make estado and ayuntamiento selected by default
    // $j('#id_estado option[value="4"]').attr("selected",true);
    // $j('#id_colectivo_1').prop('checked', true);


    // Unsaved changes leaving page
    var form = $j('#some-form'),
    original = form.serialize();
    form.submit(function(){
        window.onbeforeunload = null
    });
    window.onbeforeunload = function(){
        if (form.serialize() != original)
            return 'Are you sure you want to leave?'
    };

    // Hide comments user
    $('#id_comments-0-user').hide();
});

function businessDays(days) {
    var dataAvui = new Date($j('#id_inicio').val());

    var holidays = [
        "01/01/2018", "06/01/2018", "30/03/2018", "01/05/2018", "15/08/2018", "12/08/2018", "01/11/2018", "06/12/2018",
        "08/12/2018", "25/12/2018", "01/01/2019", "06/01/2019", "19/04/2019", "01/05/2019", "15/08/2019", "12/10/2019",
        "01/11/2019", "06/12/2019", "25/12/2019"
    ]

    for (var i=1;i<=days;i++)
    {
        var dataTemp = dataAvui;
        var dataFormated = ('0' + dataTemp.getDate()).slice(-2)+"/"+('0'+(dataTemp.getMonth()+1)).slice(-2)+"/"+dataTemp.getFullYear();
        //console.log(dataTemp.toString());
        dataTemp.setDate(dataTemp.getDate() + 1);
        if(dataTemp.getDay() == 6){
            dataTemp.setDate(dataTemp.getDate() + 2);
        }else if(dataTemp.getDay() == 0){
            dataTemp.setDate(dataTemp.getDate() + 1);
        }

        for (var j = 0; j < holidays.length; j++) {
            if (holidays[j] == dataFormated) {
                console.log("holidays: "+holidays[j]);
                console.log("data: "+dataFormated);
                dataTemp.setDate(dataTemp.getDate() + 1);
            }
        }

        dataAvui = dataTemp;
        $j("#id_fin").val(dataAvui.toInputFormat());
    }
}

Date.prototype.toInputFormat = function() {
   var yyyy = this.getFullYear().toString();
   var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
   var dd  = this.getDate().toString();
   return yyyy + "-" + (mm[1]?mm:"0"+mm[0]) + "-" + (dd[1]?dd:"0"+dd[0]); // padding
};