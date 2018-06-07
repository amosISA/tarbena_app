$(document).ready(function() {
    // If window > 960 back navbar to its normal state
    $(window).resize(function() {
        if ($(window).width() > 960) {
            $('.custom-home-navbar__menus__links .custom-home-navbar__li__anchor').each(function() { $(this).remove(); });
            $('.custom-home-navbar__menus__links').removeAttr('style');
        }
    });

    // Toggle dropdown right side
    $('.custom-home-navbar__menus_toogle').click(function () {
        $('.custom-home-navbar__menus_toogle > a').toggleClass("setting-dropdown-icon--active");
        $('.custom-home-navbar__menus__links').toggleClass('custom-home-navbar__menus__links--active').toggle();
        handle1();
    });
});

function handle1() {
    $('.custom-home-navbar__menus__links .custom-home-navbar__li__anchor').each(function() { $(this).remove(); });
    var copy = $('.custom-home-navbar__menus ul li a').clone();
    copy.addClass('custom-home-navbar__menus__link').prependTo('.custom-home-navbar__menus__links');
}