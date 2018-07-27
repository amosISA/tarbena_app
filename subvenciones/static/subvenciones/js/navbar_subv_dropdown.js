$(document).ready(function() {
    // Toggle dropdown right side when user is logged in
    $('.dropdown-subv__icon').on('click', function() {
        var dropdown = $('#subvenciones-nav-dropdown-toggle');
        dropdown.hasClass('dropdown-menu__box--hide') ? dropdown.removeClass('dropdown-menu__box--hide') : dropdown.addClass('dropdown-menu__box--hide');
        $(this).hasClass('dropdown-menu__icon--active') ? $(this).removeClass('dropdown-menu__icon--active') : $(this).addClass('dropdown-menu__icon--active');
    });
    //handle1();
});

function handle1() {
    var copy = $('ul.subvenciones-ul-nav li a').clone();
    copy.addClass('anchor-drop-dwn__subv menu-item').prependTo('#subvenciones-nav-dropdown-toggle');

    /*
    copy.each(function() {
        $(this).children().wrapAll("<div class='subv_inside__anchor--drop'></div>").end();
    });
    */
}