$(document).ready(function() {
    // Mobile
    if ($(window).width() < 1180) {
        // Delete all but last and penultimate
        $('#subvenciones-nav-dropdown-toggle a:not(:last)').prev().remove();
        $('<a href="/subvenciones/" class="anchor-drop-dwn__subv menu-item"> \
            <div class="subv_inside__anchor--drop">Inicio <span class="span__drop--itm"><i class="fas fa-home"></i></span></div> \
            </a> \
            <a href="/subvenciones/new/" class="anchor-drop-dwn__subv menu-item"> \
            <div class="subv_inside__anchor--drop">Crear <span class="span__drop--itm"><i class="far fa-file"></i></span></div> \
            </a> \
            <a href="/subvenciones/favourites/" class="anchor-drop-dwn__subv menu-item"> \
            <div class="subv_inside__anchor--drop">Favoritos <span class="span__drop--itm"><i class="far fa-bookmark"></i></span></div> \
            </a>').prependTo('#subvenciones-nav-dropdown-toggle');
    }

    // If window > 960 back navbar to its normal state
    $(window).resize(function() {
        if ($(window).width() < 1180) {
            // Delete all but last and penultimate
            $('#subvenciones-nav-dropdown-toggle a:not(:last)').prev().remove();
            $('<a href="/subvenciones/" class="anchor-drop-dwn__subv menu-item"> \
                <div class="subv_inside__anchor--drop">Inicio <span class="span__drop--itm"><i class="fas fa-home"></i></span></div> \
                </a> \
                <a href="/subvenciones/new/" class="anchor-drop-dwn__subv menu-item"> \
                <div class="subv_inside__anchor--drop">Crear <span class="span__drop--itm"><i class="far fa-file"></i></span></div> \
                </a> \
                <a href="/subvenciones/favourites/" class="anchor-drop-dwn__subv menu-item"> \
                <div class="subv_inside__anchor--drop">Favoritos <span class="span__drop--itm"><i class="far fa-bookmark"></i></span></div> \
                </a>').prependTo('#subvenciones-nav-dropdown-toggle');
        }
    });

    // Toggle dropdown right side when user is logged in
    $('.dropdown-subv__icon').on('click', function() {
        var dropdown = $('#subvenciones-nav-dropdown-toggle');
        dropdown.hasClass('dropdown-menu__box--hide') ? dropdown.removeClass('dropdown-menu__box--hide') : dropdown.addClass('dropdown-menu__box--hide');
        $(this).hasClass('dropdown-menu__icon--active') ? $(this).removeClass('dropdown-menu__icon--active') : $(this).addClass('dropdown-menu__icon--active');
    });
});