$(document).ready(function() {
    // select multiple fix height with size
    $("select#id_responsable").attr('size', '10');
    var select_resp = document.getElementById('id_responsable');
    select_resp.size = select_resp.length;

    // Print or not print awesome icon
    $("label[for='id_impreso']").text('');

    // Get Drive textarea anchor link
    $('textarea#id_drive').click(function() {
        var textarea_drive_url = $(this).val();
        window.open(textarea_drive_url, '_blank');
    }).hover(function() {
        $(this).css('text-decoration', 'underline');
    },function(){
        $(this).css("text-decoration", "none");
    });
});