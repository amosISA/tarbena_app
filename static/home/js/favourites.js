$(document).ready(function() {
    $(".top-site-inner a[href^='http']").each(function() {
        imageUrl = 'https://www.google.com/s2/favicons?domain=' + this.href;
        $(this).find('.top-site-icon').css('background-image', 'url(' + imageUrl + ')');
    });
});