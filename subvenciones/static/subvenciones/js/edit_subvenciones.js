$(document).ready(function() {
    // If impreso is checked add class to toogle
            if ($('input#id_impreso').is(':checked')) { $('input#id_impreso + label').addClass('nested-icon-check'); }

    // Change cuantia label text
    $("#id_cuantia_inicial").prev().empty().append('Inicio:').css({'display':'block', 'text-align':'left'});
    $("#id_cuantia_solicitada").prev().empty().append('Solicitada:').css({'display':'block', 'text-align':'left'});
    $("#id_cuantia_final").prev().empty().append('Final:').css({'display':'block', 'text-align':'left'});

    // Disable button if user dont' make changes on the form
    $('form')
        .each(function(){
            $(this).data('serialized', $(this).serialize())
        })
        .on('keyup change :input', function(){
            if ($(this).serialize() == $(this).data('serialized')) { $('.button_form--submit__wrapper button').attr('disabled', 'disabled'); } else { $('.button_form--submit__wrapper button').removeAttr('disabled'); }
         })
    ;
    $('a.ajax_relation_anchor').click(function() { $('.button_form--submit__wrapper button').attr('disabled', 'disabled'); });
});