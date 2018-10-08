var modal;

function abrir_modal(url)
{
    modal = $('#popup').dialog(
    {
        modal: true,
        width: 500,
        resizable: false
    }).dialog('open');
}

function cerrar_modal()
{
    modal.dialog("close");
}