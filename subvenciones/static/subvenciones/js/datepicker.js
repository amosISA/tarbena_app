$(function() {
    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '< Ant',
        nextText: 'Sig >',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['es']);

    $( ".datepicker" ).datepicker({
        changeMonth: true,
        changeYear: true,
        beforeShowDay: function(date){
            show = true;
            if(date.getDay() == 0 || date.getDay() == 6){show = false;}//No Weekends
            for (var i = 0; i < holidays.length; i++) {
                if (new Date(holidays[i]).toString() == date.toString()) {show = false;}//No Holidays
            }
            var display = [show,'',(show)?'':'No Weekends or Holidays'];//With Fancy hover tooltip!
            return display;
        }
    });

    var holidays = ["12/24/2012", "12/25/2012", "1/1/2013",
            "5/27/2013", "7/4/2013", "9/2/2013", "11/28/2013",
            "11/29/2013", "12/24/2013", "12/25/2013"];

    var id_date_inicio = $('#id_fecha_publicacion');
    var id_date_fin = $('#id_fin');
    var content_div_fin = '<div class="id_date_fin_anchors_bussines_day"><a href="#" onClick="businessDays(10);">+ 10 días hábiles</a><a href="#" onClick="businessDays(15);">+ 15 días hábiles</a><a href="#" onClick="businessDays(20);">+ 20 días hábiles</a><a href="#" onClick="businessDays(30);">+ 30 días hábiles</a></div>';
    id_date_inicio.change(function() {
        if (id_date_inicio.val()) {
            if (!$('.id_date_fin_anchors_bussines_day').length) {
                id_date_fin.after(content_div_fin);
            }
        } else {
            console.log('error');
            $('.id_date_fin_anchors_bussines_day').remove();
        }
    });
});