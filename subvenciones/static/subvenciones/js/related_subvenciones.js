// Frist, empty the ul
$('ul#id_se_relaciona_con').text('');
// WHEN ADD SUBSIDIE
$(document).ready(function() {
    // AJAX FOR SELECT DEPARTMENT AND FILL SE RELACIONA CON
    $('.se_relaciona_con_ajax_div').css('display', 'none');
    // When you click the first filter button and modal appear
    $('.ajax_relation_anchor').on('click', function(e){
        // Made the popup appear with the insert template
        e.preventDefault();
        $('#ajaxRelationFilterModal').modal('show').find('.modal-body').load($(this).attr('href'));
    });
    // When you click on each checkbox on the modal and displays the subsidies in the
    // same modal when you check them
    $('body').on('click', '.modal-ajax-entes input:checkbox', function(){
        var checkbox = $(this);
        var dip_list = [];
        var gene_list = [];
        var gob_list = [];
        if(checkbox.is(':checked')){
            $("input[name='diputacion_ajax']:checked").each( function () {
                dip_list.push(parseInt($(this).val()));
            });
            $("input[name='generalitat_ajax']:checked").each( function () {
               gene_list.push(parseInt($(this).val()));
            });
            $("input[name='gobierno_ajax']:checked").each( function () {
               gob_list.push(parseInt($(this).val()));
            });
            $.ajax({
                method: 'GET',
                url: "{% url 'subvenciones:ajax_se_relaciona_con' %}",
                data: {
                    'diputacion_ajax': dip_list,
                    'generalitat_ajax': gene_list,
                    'gobierno_ajax': gob_list
                },
                dataType: 'json',
                success: function (data) {
                    var checkboxes_list = $('ul#content_ajax_list input:checkbox');
                    // if the checkboxes in the list are not checked they are deleted when a new checkbox is selected
                    checkboxes_list.each(function() {
                        var checkbox_list = $(this);
                        if(checkbox_list.is(':checked')){}else{checkbox_list.parent().parent().remove();}
                    });
                    $.each(data, function(key, value){
                        $('ul#content_ajax_list').append("<li><label><input type='checkbox' name='se_relaciona_con' value='"+value.pk+"' class='' id='id_se_relaciona_con_"+key+"'>"+value.fields['nombre']+"</label></li>");
                    });
                    // Aquí cuando seleccionas una subvención para que no vuelva a aparecer duplicada la q
                    // has seleccionado, la eliminamos si ya se encuentra dentro del objecto
                    // primero la metemos y luego miramos otra vez si está, y si así es, la eliminamos
                    var inputs_checkbox = {};
                    $('ul#content_ajax_list input:checkbox').each(function() {
                        var checkbox = $(this).val();
                        if(inputs_checkbox[checkbox]) {
                            $(this).parent().parent().remove();
                        } else {
                            inputs_checkbox[checkbox] = true;
                        }
                    });
                }
            });
        } else {
            dip_list = [], gene_list = [], gob_list = [];
            $("input[name='diputacion_ajax']:checked").each( function () {
                dip_list.push(parseInt($(this).val()));
            });
            $("input[name='generalitat_ajax']:checked").each( function () {
               gene_list.push(parseInt($(this).val()));
            });
            $("input[name='gobierno_ajax']:checked").each( function () {
               gob_list.push(parseInt($(this).val()));
            });
            $.ajax({
                method: 'GET',
                url: "{% url 'subvenciones:ajax_se_relaciona_con' %}",
                data: {
                    'diputacion_ajax': dip_list,
                    'generalitat_ajax': gene_list,
                    'gobierno_ajax': gob_list
                },
                dataType: 'json',
                success: function (data) {
                    var checkboxes_list = $('ul#content_ajax_list input:checkbox');
                    checkboxes_list.each(function() {
                        var checkbox_list = $(this);
                        if(checkbox_list.is(':checked')){}else{checkbox_list.parent().parent().remove();}
                    });
                    $.each(data, function(key, value){
                        $('ul#content_ajax_list').append("<li><label><input type='checkbox' name='se_relaciona_con' value='"+value.pk+"' class='' id='id_se_relaciona_con_"+key+"'>"+value.fields['nombre']+"</label></li>");
                    });
                }
            });
        }
    });
    // When you click on filter button from the modal popup
    $('#modal_ajax_button_filter_subsidies').click(function() {
        $('.se_relaciona_con_ajax_div').css('display', 'block');
        var ul_li = $('#id_se_relaciona_con');
        ul_li.text('');
        $('ul#content_ajax_list input:checkbox').each(function() {
            if($(this).is(':checked')){
                ul_li.append('<li>'+$(this).parent().parent().html()+'</li>');
            }
        });
        $('#id_se_relaciona_con input:checkbox').prop('checked', true);
    });
});