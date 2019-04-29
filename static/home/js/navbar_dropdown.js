$(document).ready(function() {
    // If window > 960 back navbar to its normal state
    $(window).resize(function() {
        if ($(window).width() > 960) {
            $('.custom-home-navbar__menus__links .custom-home-navbar__li__anchor').each(function() { $(this).remove(); });
            $('.custom-home-navbar__menus__links').removeAttr('style');
        }
    });

    // Toggle dropdown right side when user is not logged in
    $('.custom-home-navbar__menus_toogle').click(function () {
        $('.custom-home-navbar__menus__links').html('');
        $('.custom-home-navbar__left__ul li > a').css("display","block");
        $('.custom-home-navbar__menus_toogle > a').toggleClass("setting-dropdown-icon--active");
        $('.custom-home-navbar__menus__links').toggleClass('custom-home-navbar__menus__links--active').toggle();
        handle1();
    });

    // Toggle dropdown right side when user is logged in
    $('.custom-home-navbar__avatar').on('click', function() {
        var dropdown = $('.custom_navbar__avatar__dropdown');
        dropdown.hasClass('custom_navbar__avatar__dropdown--hide') ? dropdown.removeClass('custom_navbar__avatar__dropdown--hide') : dropdown.addClass('custom_navbar__avatar__dropdown--hide');
    });
});

function handle1() {
    $('.custom-home-navbar__menus__links .custom-home-navbar__li__anchor').each(function() { $(this).remove(); });
    var copy = $('.custom-home-navbar__menus ul li a').clone();
    copy.addClass('custom-home-navbar__menus__link').prependTo('.custom-home-navbar__menus__links');
}